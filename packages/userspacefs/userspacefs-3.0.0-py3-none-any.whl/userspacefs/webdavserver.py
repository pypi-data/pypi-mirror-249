#!/usr/bin/env python3

# This file is part of userspacefs.

# userspacefs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# userspacefs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with userspacefs.  If not, see <http://www.gnu.org/licenses/>.

import userspacefs.abc as fsabc

from userspacefs.path_common import is_parent
from userspacefs.smbserver import AsyncWorkerPool, AsyncFS, AsyncFile, cant_fail, JustNameDirStat
from userspacefs.util_dumpster import OldStat, datetime_from_ts

from aiohttp import web

import asyncio
import contextlib
import datetime
import dataclasses as dc
import errno
import itertools
import logging
import functools
import os
import re
import socket
import sys
import time
import typing
import urllib.parse
import uuid

import xml.etree.ElementTree as ET

from http import HTTPStatus
from collections.abc import Sequence, Mapping, Callable
from collections import defaultdict

log = logging.getLogger(__name__)

@dc.dataclass
class NormalStat:
    birthtime: datetime.datetime
    mtime: datetime.datetime
    ctime: datetime.datetime
    atime: datetime.datetime
    type: str
    size: int

def normalize_stat(stat: OldStat) -> NormalStat:
    birthtime = getattr(stat, "birthtime", datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc))
    mtime = getattr(stat, "mtime", birthtime)
    ctime = getattr(stat, "ctime", mtime)
    atime = getattr(stat, "atime", ctime)

    type = getattr(stat, "type")
    size = getattr(stat, "size")

    return NormalStat(birthtime, mtime, ctime, atime, type, size)

async def normalize_dir_entry(fs: AsyncFS, path: fsabc.Path, entry: JustNameDirStat) -> NormalStat:
    to_normalize = OldStat((await fs.stat(path / entry.name)))
    return normalize_stat(to_normalize)

@dc.dataclass
class WebDAVLock:
    timeout: typing.Optional[int]
    path: fsabc.Path
    token: str
    is_exclusive: bool
    depth: typing.Optional[int]
    owner_xml: ET.Element
    is_collection: bool

@dc.dataclass
class WebDAVServerCtx:
    fs: AsyncFS
    locks: typing.List[WebDAVLock]
    path_root_parts: typing.List[str]

def get_rel_path_parts(ctx: WebDAVServerCtx, ipath: str) -> typing.List[str]:
    parts = ipath[1:].split('/')
    if parts[:len(ctx.path_root_parts)] != ctx.path_root_parts:
        raise web.HTTPNotFound()
    parts = parts[len(ctx.path_root_parts):]
    return parts

async def path_from_url_path(ctx: WebDAVServerCtx, ipath: str) -> fsabc.Path:
    parts = get_rel_path_parts(ctx, ipath)
    if parts and not parts[-1]:
        parts.pop()
    path = await ctx.fs.create_path(*map(urllib.parse.unquote, parts))
    return path

async def path_from_req(ctx: WebDAVServerCtx,
                        req: web.Request) -> fsabc.Path:
    p = await path_from_url_path(ctx, req.url.raw_path)
    return p

def close_asynchronously(f: AsyncFile) -> None:
    # Close asynchronously
    def on_fail() -> None:
        log.warning("Closing %r failed!", f)
    asyncio.ensure_future(cant_fail(on_fail, asyncio.ensure_future(f.close())))

def create_response(
        status: int = 200,
        headers: typing.Optional[Mapping[str, typing.Any]] = None,
        body: typing.Optional[bytes] = None,
        content_type: typing.Optional[str] = None,
) -> web.Response:
    resp = web.Response(
        status=status,
        headers=headers,
        body=body,
        content_type=content_type,
    )
    resp.force_close()
    return resp

async def _get_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    path = await path_from_req(ctx, req)

    try:
        f = await fs.open(path, os.O_RDONLY)
    except FileNotFoundError:
        return create_response(status=HTTPStatus.NOT_FOUND)

    try:
        st = OldStat((await fs.fstat(f)))
        if (req.if_modified_since is not None and
            st.mtime <= req.if_modified_since):
            return create_response(status=HTTPStatus.NOT_MODIFIED)

        # TODO: we can display a directory listing if we want
        if st.type == 'directory':
            return create_response(
                body=b'',
            )

        # TODO: send E-tag
        resp = create_response()

        resp.last_modified = st.mtime

        resp.enable_chunked_encoding()

        await resp.prepare(req)

        if req.method == 'GET':
            buf = memoryview(bytearray(4096))
            while True:
                amt = await f.readinto(buf)
                if not amt:
                    break

                await resp.write(buf[:amt])

        await resp.write_eof()

        return resp
    finally:
        close_asynchronously(f)

def get_public_root(ctx: WebDAVServerCtx, req: web.Request) -> str:
    # default for now, we can iterate on this later
    return '%s://%s/%s%s' % (req.scheme, req.host,
                             '/'.join(ctx.path_root_parts), '/' if ctx.path_root_parts else '')

DEFAULT_PROPS_TO_GET = [
    "{DAV:}getlastmodified", "{DAV:}creationdate",
    "{DAV:}getcontentlength", "{DAV:}resourcetype",
]

def join_public_root(public_root: str, path: fsabc.Path, is_collection: bool) -> str:
    to_add = '/'.join(map(urllib.parse.quote, path.parts[1:]))
    return public_root + to_add + ('/' if is_collection and to_add else '')

def add_propfind_ent_from_stat(req_type: str, public_root: str, root: ET.Element, path: fsabc.Path, st: NormalStat, props_to_get: Sequence[str]) -> None:
    response_elt = ET.SubElement(root, '{DAV:}response')

    ET.SubElement(response_elt, '{DAV:}href').text = join_public_root(public_root, path, st.type == 'directory')

    propstat_not_found_elt = ET.SubElement(response_elt, '{DAV:}propstat')
    prop_not_found_elt = ET.SubElement(propstat_not_found_elt, '{DAV:}prop')
    ET.SubElement(propstat_not_found_elt, '{DAV:}status').text = "HTTP/1.1 404 Not Found"

    propstat_success_elt = ET.SubElement(response_elt, '{DAV:}propstat')
    prop_success_elt = ET.SubElement(propstat_success_elt, '{DAV:}prop')
    ET.SubElement(propstat_success_elt, '{DAV:}status').text = "HTTP/1.1 200 OK"

    for prop in props_to_get:
        if prop == '{DAV:}getlastmodified':
            t = st.mtime.strftime("%a, %d %b %Y %H:%M:%S GMT")
            ET.SubElement(prop_success_elt, '{DAV:}getlastmodified').text = t
        elif prop == '{DAV:}creationdate':
            t = st.birthtime.strftime("%Y-%m-%dT%H:%M:%SZ")
            ET.SubElement(prop_success_elt, '{DAV:}creationdate').text = t
        elif prop == '{DAV:}getcontentlength':
            t = str(st.size)
            ET.SubElement(prop_success_elt, '{DAV:}getcontentlength').text = t
        elif prop == '{DAV:}resourcetype':
            rsrctype = ET.SubElement(prop_success_elt, '{DAV:}resourcetype')
            if st.type == 'directory':
                ET.SubElement(rsrctype, '{DAV:}collection')
        else:
            ET.SubElement(prop_not_found_elt, prop)

    if req_type == 'allprop':
        supported_lock_elt = ET.SubElement(prop_success_elt, '{DAV:}supportedlock')
        lockentry_exclusive_elt = ET.SubElement(supported_lock_elt, '{DAV:}lockentry')
        lockscope_exclusive_elt = ET.SubElement(lockentry_exclusive_elt, '{DAV:}lockscope')
        ET.SubElement(lockscope_exclusive_elt, '{DAV:}exclusive')
        locktype_exclusive_elt = ET.SubElement(lockentry_exclusive_elt, '{DAV:}locktype')
        ET.SubElement(locktype_exclusive_elt, '{DAV:}write')

        lockentry_shared_elt = ET.SubElement(supported_lock_elt, '{DAV:}lockentry')
        lockscope_shared_elt = ET.SubElement(lockentry_shared_elt, '{DAV:}lockscope')
        ET.SubElement(lockscope_shared_elt, '{DAV:}shared')
        locktype_shared_elt = ET.SubElement(lockentry_shared_elt, '{DAV:}locktype')
        ET.SubElement(locktype_shared_elt, '{DAV:}write')

    if not len(prop_not_found_elt):
        response_elt.remove(propstat_not_found_elt)

    if not len(prop_success_elt):
        response_elt.remove(propstat_success_elt)

def _get_depth(req: web.Request) -> typing.Optional[int]:
    depth = req.headers.get('Depth')
    if depth is None or depth.lower() == "infinity":
        return None

    depth_i = int(depth)

    if depth_i < 0 or depth_i > 1:
        raise ValueError()

    return depth_i

async def _propfind_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    public_root = get_public_root(ctx, req)

    path = await path_from_req(ctx, req)

    try:
        depth_i = _get_depth(req)
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    if depth_i is None:
        # we don't support infinite depth
        return create_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    parser = ET.XMLParser()

    str_ = req.content
    fed_to_parser = 0
    while True:
        body = await str_.read(4096)
        if not body:
            break
        # TODO: forbid !ENTITY tags to avoid billion laughs
        #       just throw exception if we find one
        parser.feed(body)
        fed_to_parser += len(body)

    propfind_req_type: str
    props_to_get: typing.List[str]

    if not fed_to_parser:
        propfind_req_type = 'allprop'
        props_to_get = DEFAULT_PROPS_TO_GET
    else:
        xml_body = parser.close()

        if xml_body.tag != "{DAV:}propfind":
            return create_response(status=HTTPStatus.BAD_REQUEST)

        propname_request = xml_body.find("./{DAV:}propname")
        if propname_request is not None:
            propfind_req_type = 'propname'
            # XXX: not yet supported
            return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            propname_request = xml_body.find("./{DAV:}allprop")
            if propname_request is not None:
                propfind_req_type = 'allprop'
                props_to_get = DEFAULT_PROPS_TO_GET
            else:
                propfind_req_type = 'prop'
                props_to_get = []
                for prop in xml_body.findall("./{DAV:}prop/*"):
                    props_to_get.append(prop.tag)

    try:
        st = OldStat((await fs.stat(path)))
    except FileNotFoundError:
        return create_response(status=HTTPStatus.NOT_FOUND)

    multistatus_elt = ET.Element('{DAV:}multistatus')

    # add the root directory first
    # NB: this actually matters for win32 clients...
    add_propfind_ent_from_stat(
        propfind_req_type, public_root,
        multistatus_elt, path,
        normalize_stat(st), props_to_get
    )

    if depth_i:
        try:
            dir_handle = await fs.old_open_directory(path)
        except NotADirectoryError:
            pass
        else:
            try:
                while True:
                    dirent = await dir_handle.read()
                    if dirent is None:
                        break
                    stc = await normalize_dir_entry(fs, path, dirent)
                    add_propfind_ent_from_stat(
                        propfind_req_type, public_root,
                        multistatus_elt, path / dirent.name,
                        stc, props_to_get
                    )
            finally:
                await dir_handle.close()

    return create_response(
        status=HTTPStatus.MULTI_STATUS,
        body=ET.tostring(multistatus_elt),
        content_type='application/xml',
    )

async def _options_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    if req.url.raw_path != '/':
        path = await path_from_req(ctx, req)

        try:
            st = OldStat((await fs.stat(path)))
        except FileNotFoundError:
            return create_response(
                status=HTTPStatus.NOT_FOUND,
            )

    return create_response(
        headers={
            'DAV': "1,2",
            # tell microsoft clients that we only support webdav and not frontpage extensions
            'MS-Author-Via': 'DAV',
            'Allow': "LOCK,UNLOCK,PROPFIND,DELETE,MOVE,COPY,OPTIONS,PROPPATCH,GET,PUT",
        },
    )

async def _copy_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    resp = await _copy_move_handler(ctx, req, False)
    return resp

async def _copy_move_handler(ctx: WebDAVServerCtx, req: web.Request, is_move: bool) -> web.Response:
    fs = ctx.fs

    path = await path_from_req(ctx, req)

    (succeeded, resp) = parse_and_verify_if_header(ctx, req, path)
    if not succeeded:
        return typing.cast(web.Response, resp)

    parsed_if_header = typing.cast(None | typing.List[ResourceConditionList], resp)

    try:
        st = OldStat((await fs.stat(path)))
    except FileNotFoundError:
        return create_response(status=HTTPStatus.NOT_FOUND)

    if is_move:
        resp = await fail_if_cant_unlink_header(ctx, req, path, parsed_if_header, is_collection=st is not None and st.type == 'directory')
        if resp is not None:
            return resp

    dest = req.headers.get('Destination')
    if dest is None:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    try:
        dest_url = urllib.parse.urlparse(dest)
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    dest_path = await path_from_url_path(ctx, dest_url.path)

    try:
        std = OldStat((await fs.stat(dest_path)))
    except FileNotFoundError:
        std = None

    resp = await fail_if_cant_unlink_header(ctx, req, dest_path, parsed_if_header, is_collection=std is not None and std.type == 'directory')
    if resp is not None:
        return resp

    try:
        depth_i = _get_depth(req)
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    if not (depth_i is None or (depth_i == 0 and not is_move)):
        return create_response(status=HTTPStatus.BAD_REQUEST)

    overwriteh = req.headers.get('Overwrite')
    overwrite = not (overwriteh is not None and overwriteh == "f")

    if is_move:
        # TODO: destroy all locks held for source
        #       for now just fail the operation if it's locked
        locked = False
        for lock in ctx.locks:
            if (lock.path == path or
                (lock.depth is None and is_parent(lock.path, path))):
                locked = True
                break

        if locked:
            return create_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        stp = OldStat((await fs.stat(dest_path.parent)))
    except FileNotFoundError:
        return create_response(status=HTTPStatus.CONFLICT)

    # if this is a move, first attempt native fs method
    # NB: This is not an optimization, we need this for correctness when
    # the user is changing the case of a file on a case-insensitive FS
    # (otherwise we'll delete the source inadvertently while trying to
    # delete whatever is at the destination)
    if is_move:
        try:
            await fs.replace(path, dest_path)
        except OSError:
            log.debug("Error while eagerly calling replace(%r, %r)",
                      path, dest_path, exc_info=True)
        else:
            return create_response(
                status=HTTPStatus.CREATED if std is None else HTTPStatus.NO_CONTENT,
            )

    if std is not None and not overwrite:
        return create_response(
            status=HTTPStatus.PRECONDITION_FAILED,
        )

    await delete_tree(fs, dest_path)

    copy_failed = True
    if is_move:
        try:
            await fs.replace(path, dest_path)
        except OSError as e:
            if e.errno != errno.EXDEV:
                log.debug("Error while calling replace(%r, %r) for move",
                          path, dest_path, exc_info=True)
                return create_response(
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
        else:
            copy_failed = False

    if copy_failed:
        try:
            if depth_i == 0:
                if st.type == 'directory':
                    await fs.mkdir(dest_path)
                else:
                    await copy_file(fs, path, dest_path)
            else:
                await copy_tree(fs, path, dest_path)
        except OSError:
            log.debug("Error while calling copying %r to %r",
                      path, dest_path, exc_info=True)
            copy_failed = True
        else:
            copy_failed = False

    return create_response(
        status=(HTTPStatus.INTERNAL_SERVER_ERROR
                if copy_failed else
                HTTPStatus.CREATED
                if std is None else
                HTTPStatus.NO_CONTENT),
    )

def any_descendant_locked(ctx: WebDAVServerCtx, path: fsabc.Path) -> bool:
    for lock in ctx.locks:
        if is_parent(path, lock.path):
            return True
    return False

async def fail_if_cant_modify_with_lock(ctx: WebDAVServerCtx, req: web.Request, path: fsabc.Path, is_collection: typing.Optional[bool] = None) -> typing.Tuple[bool, web.Response | typing.Optional[WebDAVLock]]:
    public_root = get_public_root(ctx, req)

    if is_collection is None:
        st: typing.Optional[OldStat]
        try:
            st = OldStat((await ctx.fs.stat(path)))
        except FileNotFoundError:
            st = None

        is_collection = st is not None and st.type == 'directory'

    try:
        parsed_if_header = get_if_lock_token(ctx, req)
    except ValueError:
        return (False, create_response(status=HTTPStatus.BAD_REQUEST))

    try:
        _verify_if_header(ctx, path, parsed_if_header)
    except ValueError:
        return (False, create_response(status=HTTPStatus.PRECONDITION_FAILED))

    try:
        (locked, lock) = check_lock(ctx, public_root, path, parsed_if_header)
    except ValueError:
        return (False, create_response(status=HTTPStatus.BAD_REQUEST))

    if locked and lock is None:
        return (False, generate_locked_response(
            public_root,
            path,
            is_collection,
        ))

    return (True, lock)

async def fail_if_cant_modify(ctx: WebDAVServerCtx, req: web.Request, path: fsabc.Path, is_collection: typing.Optional[bool] = None) -> typing.Optional[web.Response]:
    (can_modify, lock_or_resp) = await fail_if_cant_modify_with_lock(ctx, req, path, is_collection=is_collection)
    if not can_modify:
        assert isinstance(lock_or_resp, web.Response)
        return lock_or_resp
    return None

async def fail_if_cant_unlink(ctx: WebDAVServerCtx, req: web.Request, path: fsabc.Path, is_collection: typing.Optional[bool] = None) -> typing.Optional[web.Response]:
    (succeeded, resp) = parse_and_verify_if_header(ctx, req, path)
    if not succeeded:
        return typing.cast(web.Response, resp)

    parsed_if_header = typing.cast(None | typing.List[ResourceConditionList], resp)

    ret = await fail_if_cant_unlink_header(ctx, req, path, parsed_if_header,
                                           is_collection=is_collection)

    return ret

async def copy_file(fs: AsyncFS, path: fsabc.Path, dest_path: fsabc.Path) -> None:
    fsrc = None
    fdst = None
    try:
        fsrc = await fs.open(path, os.O_RDONLY)
        fdst = await fs.open(dest_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        buf = memoryview(bytearray(4096))
        while True:
            amt = await fsrc.readinto(buf)
            if not amt:
                break
            await fdst.write(buf[:amt])
    finally:
        if fdst is not None:
            await fdst.close()
        if fsrc is not None:
            await fsrc.close()

async def copy_tree(fs: AsyncFS, path: fsabc.Path, dest_path: fsabc.Path) -> None:
    # delete entire tree
    # use pre-order DFS
    root_dest_path = dest_path.parent
    root_path = path.parent

    child_path = [path.name]

    q = [child_path]
    while q:
        pparts = q.pop()

        cpath = root_path.joinpath(**pparts)
        cdest_path = root_dest_path.joinpath(*pparts)

        try:
            f = await fs.old_open_directory(cpath)
        except FileNotFoundError:
            continue
        except NotADirectoryError:
            await copy_file(fs, cpath, cdest_path)
        else:
            await fs.mkdir(cdest_path)

            try:
                while True:
                    dirent = await f.read()
                    if dirent is None:
                        break
                    q.append(list(pparts) + [dirent.name])
            finally:
                await f.close()

async def delete_tree(fs: AsyncFS, path: fsabc.Path) -> None:
    # delete entire tree
    # use post-order DFS
    q = [(path, False)]
    while q:
        (cpath, visited) = q.pop()

        if not visited:
            q.append((cpath, True))

            try:
                f = await fs.old_open_directory(cpath)
            except FileNotFoundError:
                pass
            except NotADirectoryError:
                pass
            else:
                try:
                    while True:
                        dirent = await f.read()
                        if dirent is None:
                            break
                        q.append((cpath / dirent.name, False))
                finally:
                    await f.close()
        else:
            try:
                await fs.unlink(cpath)
            except FileNotFoundError:
                pass
            except PermissionError:
                # TODO: if this fails, then we need to return a 207 multi-status
                #       with the specific resource that failed to delete and why
                await fs.rmdir(cpath)

async def _delete_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    depth = _get_depth(req)

    if depth is not None:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    path = await path_from_req(ctx, req)

    resp = await fail_if_cant_unlink(ctx, req, path)
    if resp is not None:
        return resp

    await delete_tree(fs, path)

    return create_response(status=HTTPStatus.NO_CONTENT)

MAX_TIMEOUT = 60

def get_timeout(req: web.Request) -> int:
    timeouts: typing.List[typing.Optional[int]] = []

    for timeout in req.headers.get('Timeout', 'Second-%d' % (MAX_TIMEOUT,)).split(","):
        ti: typing.Optional[int]
        if timeout.startswith("Second-"):
            ti = int(timeout[len("Second-"):])
        elif timeout == 'Infinite':
            ti = None
        else:
            raise ValueError()
        timeouts.append(ti)

    selected_timeout = min(MAX_TIMEOUT, MAX_TIMEOUT if timeouts[0] is None else timeouts[0])

    return selected_timeout

@dc.dataclass
class Condition:
    inverted: bool
    is_state_token: bool
    body: str

@dc.dataclass
class ResourceConditionList:
    resource: str
    condition_list: typing.List[typing.List[Condition]]

def get_if_lock_token_inner(if_header: str, default_resource_tag: str) -> typing.List[ResourceConditionList]:
    toret: typing.List[ResourceConditionList] = []

    if_header_offset = 0

    # first parse optional resource tag
    mo = re.search(r"^\s*(<([^>]+)>)?", if_header[if_header_offset:])
    if mo is None:
        raise ValueError()

    if_header_offset += mo.end(0)

    if mo[1] is not None:
        resource_tag = mo[1]
        allows_new_resource_tags = True
    else:
        resource_tag = default_resource_tag
        allows_new_resource_tags = False

    top_list: typing.List[typing.List[Condition]] = []
    while True:
        if allows_new_resource_tags:
            mo = re.search(r"^\s*(<([^>]+)>)?", if_header[if_header_offset:])
            if mo is None:
                raise ValueError()

            if_header_offset += mo.end(0)

            if mo[1] is not None:
                # parse new resource tag
                toret.append(ResourceConditionList(resource_tag, top_list))
                resource_tag = mo[1]
                top_list = []

        cur_list: typing.List[Condition] = []
        # parse list
        mo = re.search(r"^\s*(\(|$)", if_header[if_header_offset:])
        if mo is None:
            print(if_header[if_header_offset:])
            raise ValueError()

        if_header_offset += mo.end(0)

        if not mo[0]:
            break

        while True:
            mo = re.search(r"^\s*((Not)?\s*(<([^>]+)>|\[([^\]]+)\])|\))", if_header[if_header_offset:])
            if mo is None:
                raise ValueError()

            if_header_offset += mo.end(0)

            if mo[0] == ')':
                break

            inverted = mo[2] is not None
            body: str
            if mo[4] is not None:
                body = mo[4]
                is_state_token = True
            else:
                assert mo[5] is not None
                body = mo[5]
                is_state_token = False
            cond = Condition(inverted, is_state_token, body)

            cur_list.append(cond)

        top_list.append(cur_list)

    toret.append(ResourceConditionList(resource_tag, top_list))

    return toret

def get_if_lock_token(ctx: WebDAVServerCtx, req: web.Request) -> typing.Optional[typing.List[ResourceConditionList]]:
    public_root = get_public_root(ctx, req)

    default_resource_tag = public_root + '/'.join(get_rel_path_parts(ctx, req.url.raw_path))

    try:
        if_header = req.headers["if"]
    except KeyError:
        return None

    return get_if_lock_token_inner(if_header, default_resource_tag)

def generate_locked_response(public_root: str, path: fsabc.Path, is_collection: bool) -> web.Response:
    error_elt = ET.Element('{DAV:}error')

    ET.SubElement(error_elt, '{DAV:}lock-token-submitted')

    ET.SubElement(error_elt, '{DAV:}href').text = join_public_root(public_root, path, is_collection)

    return create_response(
        status=HTTPStatus.LOCKED,
        body=ET.tostring(error_elt),
        content_type='application/xml',
    )

def generate_failed_lock_response(public_root: str,
                                  path: fsabc.Path, path_is_collection: bool,
                                  status_path: fsabc.Path, status_path_is_collection: bool) -> web.Response:
    multistatus_elt = ET.Element('{DAV:}multistatus')

    response_elt_0 = ET.SubElement(multistatus_elt, '{DAV:}response')

    ET.SubElement(response_elt_0, '{DAV:}href').text = join_public_root(
        public_root,
        status_path,
        status_path_is_collection,
    )
    ET.SubElement(response_elt_0, '{DAV:}status').text = "HTTP/1.1 423 Locked"

    response_elt_1 = ET.SubElement(multistatus_elt, '{DAV:}response')

    ET.SubElement(response_elt_1, '{DAV:}href').text = join_public_root(
        public_root,
        path,
        path_is_collection,
    )
    ET.SubElement(response_elt_1, '{DAV:}status').text = "HTTP/1.1 424 Failed Dependency"

    return create_response(
        status=HTTPStatus.MULTI_STATUS,
        body=ET.tostring(multistatus_elt),
        content_type='application/xml',
    )

def generate_success_lock_response(public_root: str, created: bool, lock: WebDAVLock) -> web.Response:
    prop_elt = ET.Element('{DAV:}prop')

    lockdiscovery_elt = ET.SubElement(prop_elt, '{DAV:}lockdiscovery')
    activelock_elt = ET.SubElement(lockdiscovery_elt, '{DAV:}activelock')
    locktype_elt = ET.SubElement(activelock_elt, '{DAV:}locktype')

    ET.SubElement(locktype_elt, '{DAV:}write')

    lockscope_elt = ET.SubElement(activelock_elt, '{DAV:}lockscope')

    ET.SubElement(lockscope_elt, '{DAV:}exclusive' if lock.is_exclusive else '{DAV:}shared')

    ET.SubElement(activelock_elt, '{DAV:}depth').text = 'infinity' if lock.depth is None else str(lock.depth)

    for child in lock.owner_xml:
        activelock_elt.append(child)

    ET.SubElement(activelock_elt, '{DAV:}timeout').text = (
        'Infinite'
        if lock.timeout is None else
        'Second-%d' % (lock.timeout,)
    )

    locktoken_elt = ET.SubElement(activelock_elt, '{DAV:}locktoken')
    ET.SubElement(locktoken_elt, '{DAV:}href').text = lock.token

    lockroot_elt = ET.SubElement(activelock_elt, '{DAV:}lockroot')

    ET.SubElement(lockroot_elt, '{DAV:}href').text = join_public_root(
        public_root,
        lock.path,
        lock.is_collection,
    )

    headers = {}
    if created:
        headers['Lock-Token'] = '<%s>' % (lock.token,)

    return create_response(
        status=HTTPStatus.CREATED if created else HTTPStatus.OK,
        body=ET.tostring(prop_elt),
        content_type='application/xml',
        headers=headers,
    )

async def open_or_create(fs: AsyncFS, path: fsabc.Path, mode: int) -> typing.Tuple[AsyncFile, bool]:
    while True:
        try:
            f = await fs.open(path, mode)
            created = False
            break
        except FileNotFoundError:
            pass

        try:
            f = await fs.open(path, mode | os.O_CREAT | os.O_EXCL)
            created = True
            break
        except FileExistsError:
            pass

    return (f, created)

def _verify_if_header(ctx: WebDAVServerCtx, path: fsabc.Path, lock_token: typing.Optional[typing.List[ResourceConditionList]]) -> None:
    # verify if condition
    if lock_token is not None:
        for resource_condition in lock_token:
            resource = resource_condition.resource
            for and_conditions in resource_condition.condition_list:
                for cond in and_conditions:
                    if cond.is_state_token:
                        # check if this resource is in the scope
                        # of the lock
                        for lock in ctx.locks:
                            if (lock.token == cond.body and
                                (lock.path == path or
                                 (lock.depth is None and is_parent(lock.path, path)))):
                                this_eval = True
                                break
                        else:
                            this_eval = False
                    else:
                        # we don't send e-tags with files yet
                        this_eval = False
                    if cond.inverted:
                        this_eval = not this_eval
                    if not this_eval:
                        and_eval = False
                        break
                else:
                    and_eval = True

                if and_eval:
                    total_eval = True
                    break
            else:
                total_eval = False

            if total_eval:
                resource_eval = True
                break
        else:
            resource_eval = False

        if not resource_eval:
            raise ValueError()

def parse_and_verify_if_header(ctx: WebDAVServerCtx, req: web.Request, path: fsabc.Path) -> typing.Tuple[bool, web.Response | None | typing.List[ResourceConditionList]]:
    try:
        parsed_if_header = get_if_lock_token(ctx, req)
    except ValueError:
        return (False, create_response(status=HTTPStatus.BAD_REQUEST))

    try:
        _verify_if_header(ctx, path, parsed_if_header)
    except ValueError:
        return (False, create_response(status=HTTPStatus.PRECONDITION_FAILED))

    return (True, parsed_if_header)

async def fail_if_cant_unlink_header(ctx: WebDAVServerCtx, req: web.Request, path: fsabc.Path, parsed_if_header: typing.Optional[typing.List[ResourceConditionList]], is_collection: typing.Optional[bool] = None) -> typing.Optional[web.Response]:
    # check if we have write access to all of the paths for which we need write access
    # to unlink this path

    path_to_locks: typing.Dict[fsabc.Path, typing.List[WebDAVLock]] = {}

    for lock in ctx.locks:
        if ((lock.depth is None and is_parent(lock.path, path)) or
            lock.path in [path, path.parent] or
            is_parent(path, lock.path)):
            path_to_locks.setdefault(path, []).append(lock)

    if not path_to_locks:
        return None

    public_root = get_public_root(ctx, req)

    if parsed_if_header is None:
        (spath, locks) = next(iter(path_to_locks.items()))
        return generate_locked_response(
            public_root,
            spath,
            locks[0].is_collection,
        )

    submitted_locks = map_header_to_submitted(parsed_if_header)

    for (spath, locks) in path_to_locks.items():
        for lock in locks:
            if submitted_locks_unlock_lock(public_root, lock, submitted_locks):
                break
        else:
            return generate_locked_response(
                public_root,
                spath,
                locks[0].is_collection,
            )

    return None

def submitted_locks_unlock_lock(public_root: str, lock: WebDAVLock, submitted_locks: typing.List[typing.Tuple[str, str]]) -> bool:
    lock_uri = join_public_root(public_root, lock.path, lock.is_collection)

    # see if any resource specified in the list of resource conditions
    # contains a lock token
    for (resource_uri, lock_token) in submitted_locks:
        if (resource_uri == lock_uri and
            lock_token == lock.token):
            return True

    return False

def map_header_to_submitted(parsed_if_header: typing.List[ResourceConditionList]) -> typing.List[typing.Tuple[str, str]]:
    # see if any resource specified in the list of resource conditions
    # contains a lock token
    submitted_locks: typing.List[typing.Tuple[str, str]] = []
    for rsrc_list in parsed_if_header:
        if (len(rsrc_list.condition_list) == 1 and
            len(rsrc_list.condition_list[0]) == 1 and
            rsrc_list.condition_list[0][0].is_state_token and
            not rsrc_list.condition_list[0][0].inverted):
            submitted_locks.append((rsrc_list.resource, rsrc_list.condition_list[0][0].body))

    return submitted_locks

def header_unlocks_lock(public_root: str, lock: WebDAVLock, parsed_if_header: typing.List[ResourceConditionList]) -> bool:
    return submitted_locks_unlock_lock(public_root, lock, map_header_to_submitted(parsed_if_header))

def check_lock(ctx: WebDAVServerCtx, public_root: str, path: fsabc.Path, parsed_if_header: typing.Optional[typing.List[ResourceConditionList]]) -> typing.Tuple[bool, typing.Optional[WebDAVLock]]:
    if parsed_if_header is None:
        submitted_locks = []
    else:
        submitted_locks = map_header_to_submitted(parsed_if_header)

    return check_lock_against_submitted(ctx, public_root, path, submitted_locks)

def check_lock_against_submitted(ctx: WebDAVServerCtx, public_root: str, path: fsabc.Path, submitted_locks: typing.List[typing.Tuple[str, str]]) -> typing.Tuple[bool, typing.Optional[WebDAVLock]]:
    # check if there are any locks on this path
    potential_locks = []
    for lock in ctx.locks:
        if (lock.path == path or
            (lock.depth is None and is_parent(lock.path, path))):
            potential_locks.append(lock)

    if potential_locks:
        for lock in potential_locks:
            if submitted_locks_unlock_lock(public_root, lock, submitted_locks):
                return (True, lock)

        # the submitted lock token doesn't match any of the locks
        # for the current resource
        return (True, None)
    else:
        return (False, None)

async def _lock_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    public_root = get_public_root(ctx, req)

    parser = ET.XMLParser()

    str_ = req.content
    fed_to_parser = 0
    while True:
        body = await str_.read(4096)
        if not body:
            break
        # TODO: forbid !ENTITY tags to avoid billion laughs
        #       just throw exception if we find one
        parser.feed(body)
        fed_to_parser += len(body)

    try:
        selected_timeout = get_timeout(req)
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    fs = ctx.fs

    path = await path_from_req(ctx, req)

    st: typing.Optional[OldStat]
    try:
        st = OldStat((await fs.stat(path)))
    except FileNotFoundError:
        st = None

    is_collection = st is not None and st.type == 'directory'

    try:
        lock_token = get_if_lock_token(ctx, req)
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    try:
        _verify_if_header(ctx, path, lock_token)
    except ValueError:
        return create_response(status=HTTPStatus.PRECONDITION_FAILED)

    if not fed_to_parser:
        if (lock_token is None or
            len(lock_token) > 1 or
            len(lock_token[0].condition_list) > 1 or
            len(lock_token[0].condition_list[0]) > 1 or
            lock_token[0].condition_list[0][0].inverted or
            not lock_token[0].condition_list[0][0].is_state_token):
            return create_response(status=HTTPStatus.BAD_REQUEST)

        (is_locked, lock) = check_lock(ctx, public_root, path, lock_token)
        if not is_locked or lock is None:
            return create_response(status=HTTPStatus.PRECONDITION_FAILED)

        lock.timeout = selected_timeout

        was_created = False
        return generate_success_lock_response(public_root, was_created, lock)

    try:
        depth_i = _get_depth(req)
        if depth_i is not None and depth_i > 0:
            raise ValueError()
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    xml_body = parser.close()

    if xml_body.tag != '{DAV:}lockinfo':
        return create_response(status=HTTPStatus.BAD_REQUEST)

    is_exclusive = xml_body.find('./{DAV:}lockscope/{DAV:}exclusive') is not None
    owner_xml = xml_body.find('./{DAV:}owner')
    if owner_xml is None:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    # acquire write lock

    # go through lock list and see if this path (or any descendants if depth != 0)
    # have an incompatible lock
    # if so then set that path as the status_path and return *is_locked = true
    for lock in ctx.locks:
        parent_locks_us = False
        if ((lock.path == path or
             (depth_i is None and is_parent(path, lock.path)) or
             (lock.depth is None and is_parent(lock.path, path))) and
            (is_exclusive or lock.is_exclusive)):
            parent_locks_us = (lock.depth is None and is_parent(lock.path, path))
            status_path = path if parent_locks_us else lock.path
            status_path_is_collection = is_collection if parent_locks_us else lock.is_collection

            if status_path == path:
                return generate_locked_response(
                    public_root,
                    path,
                    is_collection,
                )
            else:
                return generate_failed_lock_response(
                    public_root,
                    path,
                    is_collection,
                    status_path,
                    status_path_is_collection,
                )
    else:
        # generate a lock token
        lock_token_str = 'urn:uuid:%s' % (uuid.uuid4(),)

        lock = WebDAVLock(
            timeout=selected_timeout,
            path=path,
            token=lock_token_str,
            is_exclusive=is_exclusive,
            depth=depth_i,
            owner_xml=owner_xml,
            is_collection=is_collection,
        )

        ctx.locks.append(lock)

        # touch file
        (f, created) = await open_or_create(fs, path, 0)
        close_asynchronously(f)

        return generate_success_lock_response(
            public_root,
            created,
            lock,
        )

async def _mkcol_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    if req.body_exists:
        return create_response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    path = await path_from_req(ctx, req)

    try:
        await fs.mkdir(path)
    except FileNotFoundError:
        status = HTTPStatus.CONFLICT
    except NotADirectoryError:
        status = HTTPStatus.FORBIDDEN
    except FileExistsError:
        status = HTTPStatus.METHOD_NOT_ALLOWED
    except OSError as e:
        if e.errno == errno.ENOSPC:
            status = HTTPStatus.INSUFFICIENT_STORAGE
        else:
            raise
    else:
        status = HTTPStatus.CREATED

    return create_response(status=status)

async def _move_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    resp = await _copy_move_handler(ctx, req, True)
    return resp

def generate_proppatch_response(public_root: str, path: fsabc.Path, is_collection: bool,
                                valid_props: Sequence[ET.Element],
                                invalid_props: Sequence[ET.Element],
                                unknown_props: Sequence[ET.Element],
                                props_to_remove: Sequence[ET.Element]) -> web.Response:
    multistatus_elt = ET.Element("{DAV:}multistatus")

    response_elt = ET.SubElement(multistatus_elt, "{DAV:}response")

    ET.SubElement(response_elt, "{DAV:}href").text = join_public_root(public_root, path, is_collection)

    ok_propstat_elt = ET.SubElement(response_elt, "{DAV:}propstat")
    ok_new_prop_elt = ET.SubElement(ok_propstat_elt, "{DAV:}prop")
    ET.SubElement(ok_propstat_elt, "{DAV:}status").text = "HTTP/1.1 200 OK"

    for prop in valid_props:
        ET.SubElement(ok_new_prop_elt, prop.tag)

    bad_propstat_elt = ET.SubElement(response_elt, "{DAV:}propstat")
    bad_new_prop_elt = ET.SubElement(bad_propstat_elt, "{DAV:}prop")
    ET.SubElement(bad_propstat_elt, "{DAV:}status").text = "HTTP/1.1 400 Bad Request"

    for prop in invalid_props:
        ET.SubElement(bad_new_prop_elt, prop.tag)

    propstat_elt = ET.SubElement(response_elt, "{DAV:}propstat")
    new_prop_elt = ET.SubElement(propstat_elt, "{DAV:}prop")
    ET.SubElement(propstat_elt, "{DAV:}status").text = "HTTP/1.1 403 Forbidden"

    for prop in itertools.chain(unknown_props, props_to_remove):
        ET.SubElement(new_prop_elt, prop.tag)

    return create_response(
        status=HTTPStatus.MULTI_STATUS,
        body=ET.tostring(multistatus_elt),
        content_type='application/xml',
    )

async def _proppatch_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    public_root = get_public_root(ctx, req)
    path = await path_from_req(ctx, req)

    st: typing.Optional[OldStat]
    try:
        st = OldStat((await fs.stat(path)))
    except FileNotFoundError:
        st = None

    is_collection = st is not None and st.type == 'directory'

    resp = await fail_if_cant_modify(ctx, req, path, is_collection=is_collection)
    if resp is not None:
        return resp

    parser = ET.XMLParser()

    # parse submitted body
    str_ = req.content
    while True:
        body = await str_.read(4096)
        if not body:
            break
        # TODO: forbid !ENTITY tags to avoid billion laughs
        #       just throw exception if we find one
        parser.feed(body)

    xml_body = parser.close()

    if xml_body.tag != '{DAV:}propertyupdate':
        return create_response(status=HTTPStatus.BAD_REQUEST)

    props_to_set = xml_body.findall('./{DAV:}set/{DAV:}prop/*')
    props_to_remove = xml_body.findall('./{DAV:}remove/{DAV:}prop/*')

    # TODO: at least use FS.x_f_set_file_times()

    times: typing.Dict[str, datetime.datetime] = {}

    invalid_props = []
    valid_props = []
    unknown_props = []

    LAST_ACCESS_TIME_TAG = "{urn:schemas-microsoft-com:}Win32LastAccessTime"
    LAST_MODIFIED_TIME_TAG = "{urn:schemas-microsoft-com:}Win32LastModifiedTime"

    for prop in props_to_set:
        if prop.tag in [
                LAST_ACCESS_TIME_TAG,
                LAST_MODIFIED_TIME_TAG,
        ]:
            try:
                times[prop.tag] = datetime.datetime.strptime(prop.text, "%a, %d %b %Y %H:%M:%S %Z")
                if prop.text.endswith("GMT") or prop.text.endswith("UTC"):
                    times[prop.tag] = times[prop.tag].replace(tzinfo=datetime.timezone.utc)
                else:
                    # If it was a successful parse and the timezone wasn't GMT/UTC
                    # then it was a synonym for our local timezone, so just make datetime
                    # an aware one.
                    times[prop.tag] = times[prop.tag].astimezone(None)
            except ValueError:
                invalid_props.append(prop)
            else:
                valid_props.append(prop)
        else:
            unknown_props.append(prop)

    if times:
        try:
            f = await fs.open(path, os.O_RDONLY)
        except FileNotFoundError:
            return create_response(HTTPStatus.NOT_FOUND)
        try:
            stn = await fs.fstat(f)

            dt_to_ts: Callable[[datetime.datetime], float] = lambda x: x.timestamp()

            await fs.futimes(f,
                             times=(dt_to_ts(times.get(LAST_ACCESS_TIME_TAG,
                                                       datetime_from_ts(stn.st_atime))),
                                    dt_to_ts(times.get(LAST_MODIFIED_TIME_TAG,
                                                       datetime_from_ts(stn.st_mtime)))))
        except OSError as e:
            if e.errno not in [errno.ENOSYS,]:
                log.warning("Couldn't set utimes()", exc_info=True)
            unknown_props.extend(valid_props)
            valid_props = []
        finally:
            close_asynchronously(f)

    return generate_proppatch_response(public_root, path, is_collection, valid_props, invalid_props, unknown_props, props_to_remove)

async def _put_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    path = await path_from_req(ctx, req)

    resp = await fail_if_cant_modify(ctx, req, path)
    if resp is not None:
        return resp

    created: bool
    try:
        (f, created) = await open_or_create(fs, path, os.O_WRONLY | os.O_TRUNC)
    except (FileNotFoundError, NotADirectoryError):
        status = HTTPStatus.CONFLICT
    except IsADirectoryError:
        status = HTTPStatus.METHOD_NOT_ALLOWED
    else:
        try:
            while True:
                buf = await req.content.read(4096)
                if not buf:
                    break
                bbuf = memoryview(buf)
                while bbuf:
                    amt = await f.write(bbuf)
                    bbuf = bbuf[amt:]
        finally:
            await f.close()
        status = HTTPStatus.CREATED if created else HTTPStatus.OK

    return create_response(status)

async def _unlock_handler(ctx: WebDAVServerCtx, req: web.Request) -> web.Response:
    fs = ctx.fs

    path = await path_from_req(ctx, req)

    try:
        st = OldStat((await fs.stat(path)))
    except FileNotFoundError:
        st = None

    is_collection = st is not None and st.type == 'directory'

    lock_token_header = req.headers.get('Lock-Token')
    if lock_token_header is None:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    mo = re.search(r"^\s*<([^>]+)>\s*$", lock_token_header)
    if mo is None:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    lock_token = mo[1]

    public_root = get_public_root(ctx, req)
    resource_uri = join_public_root(public_root, path, is_collection)

    try:
        (locked, lock) = check_lock_against_submitted(ctx, public_root, path, [(resource_uri, lock_token)])
    except ValueError:
        return create_response(status=HTTPStatus.BAD_REQUEST)

    if lock is None:
        return create_response(
            status=HTTPStatus.CONFLICT,
        )

    assert locked

    ctx.locks.remove(lock)

    return create_response(status=HTTPStatus.NO_CONTENT)

PathT = typing.TypeVar('PathT', bound=fsabc.Path)
FileT = typing.TypeVar('FileT', bound=fsabc.File)

# WebDAVServer abstracts away the fact that it is implemented using
# asyncio. It expects to be used in normal python code.
class WebDAVServer(object):
    def __init__(self,
                 fs_: fsabc.FileSystemG[PathT, FileT],
                 path_root: typing.Optional[str] = None,
                 address: typing.Optional[typing.Tuple[str, int]] = None,
                 sock: typing.Optional[socket.socket] = None) -> None:
        self._loop = asyncio.new_event_loop()

        # NB: we use file system correctly (only passing it file
        #     handles and paths it created) so we can cast to generic
        #     type here (Without having to parameterize the entire file)
        fs = fsabc.safe_cast_file_system(fs_)
        self._worker_pool = AsyncWorkerPool(self._loop, 8)
        afs = AsyncFS(fs, self._worker_pool)

        if path_root is None:
            path_root = '/'

        path_root_parts = path_root.split("/")
        if not path_root_parts[0]:
            path_root_parts = path_root_parts[1:]
        if path_root_parts and not path_root_parts[-1]:
            path_root_parts = path_root_parts[:-1]

        ctx = WebDAVServerCtx(afs, [], path_root_parts)

        app = web.Application()

        routes_table = []
        for (name, meth) in [
                ('GET', _get_handler),
                ('PROPFIND', _propfind_handler),
                ('OPTIONS', _options_handler),
                ('COPY', _copy_handler),
                ('DELETE', _delete_handler),
                ('LOCK', _lock_handler),
                ('MKCOL', _mkcol_handler),
                ('MOVE', _move_handler),
                ('PROPPATCH', _proppatch_handler),
                ('PUT', _put_handler),
                ('UNLOCK', _unlock_handler),
        ]:
            routes_table.append(web.route(name, '/{tail:.*}', functools.partial(meth, ctx)))

        app.add_routes(routes_table)

        self._master_kill: asyncio.Future[None] = asyncio.Future(loop=self._loop)

        self.runner = web.AppRunner(app, debug=True)

        async def start_server_coro() -> None:
            await self.runner.setup()
            site: web.BaseSite
            if address is not None:
                assert sock is None, 'address and sock should not be specified at the same time'
                site = web.TCPSite(self.runner, address[0], address[1])
            else:
                assert sock is not None, "neither address nor sock were specified"
                site = web.SockSite(self.runner, sock)
            await site.start()

        self._loop.run_until_complete(start_server_coro())

    def stop(self) -> None:
        async def _on_main_thread() -> None:
            self._master_kill.set_result(None)
        asyncio.run_coroutine_threadsafe(_on_main_thread(), self._loop)

    def run(self) -> None:
        async def _run() -> None:
            await self._master_kill
            await self.runner.cleanup()
        self._loop.run_until_complete(_run())

    def close(self) -> None:
        self._loop.close()
        self._worker_pool.close()

def main(argv: Sequence[str]) -> int:
    logging.basicConfig(level=logging.DEBUG)

    # This runtime import is okay because it happens in main()
    from userspacefs.memoryfs import FileSystem as MemoryFileSystem

    fs = MemoryFileSystem([("foo", {"type": "directory",
                                    "children" : [
                                        ("baz", {"type": "file", "data": b"YOOOO"}),
                                        ("quux", {"type": "directory"}),
                                    ]
    }),
                           ("bar", {"type": "file", "data": b"f"})])

    with contextlib.closing(WebDAVServer(fs, address=('127.0.0.1', 8888))) as server:
        server.run()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
