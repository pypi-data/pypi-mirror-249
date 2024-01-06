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

from typing_extensions import Buffer

import codecs
import collections
import ctypes
import errno
import io
import itertools
import json
import logging
import os
import random
import sys
import threading
import time
import typing
import warnings

import dataclasses as dc

from abc import abstractmethod
from collections.abc import Sequence, Callable, Sized, Iterator
from datetime import datetime

import userspacefs.abc as fsabc

from userspacefs import simple_main_from_argv
from userspacefs.path_common import Path
from userspacefs.util_dumpster import PositionIO, null_context, quick_container, datetime_now, NewStat, NewDirectory, WriteableBuffer, ReadableBuffer, OldDirectoryProtocol, OldDirStatProtocol, datetime_from_ts


log = logging.getLogger(__name__)

try:
    O_ACCMODE = os.O_ACCMODE
except AttributeError:
    if sys.platform == 'win32':
        O_ACCMODE = 3
    else:
        raise

MDDict = typing.Dict[str, typing.Any]

def get_size(md: MDDict) -> int:
    if md["type"] == "directory":
        return 0
    else:
        assert md["type"] == "file"
        return len(md.get("data", b''))

def get_children(md: MDDict) -> typing.List[typing.Tuple[str, MDDict]]:
    assert md["type"] == "directory"
    ret = md.get("children", [])
    return typing.cast(typing.List[typing.Tuple[str, MDDict]], ret)

def get_rev(md: MDDict) -> str:
    if md['type'] == 'directory':
        return ''
    else:
        return 'rev:' + codecs.encode(json.dumps((get_id(md), len(md['revs']) - 1)).encode('utf-8'), 'hex').decode('ascii')

def decode_rev(rev: str) -> typing.Tuple[int, int]:
    if not rev.startswith('rev:'):
        raise ValueError("bad rev! %r" % (rev,))
    ret = json.loads(codecs.decode(rev[4:].encode('ascii'), 'hex').decode('utf-8'))
    return tuple(ret)

def get_id(md: MDDict) -> str:
    ret = md['id']
    assert isinstance(ret, str)
    return ret

class _File(PositionIO):
    def __init__(self, md: MDDict, mode: int):
        super().__init__()

        self._md = md
        self._mode = mode

    def preadinto(self, buf_: WriteableBuffer, offset: int) -> int:
        if not self.readable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        if self._md["type"] == "directory":
            raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))
        d = memoryview(self._md["data"])
        bufm = memoryview(buf_)
        size = len(bufm)
        buf = d[offset:
                len(d) if size < 0 else offset + size]
        bufm[:len(buf)] = buf
        return len(buf)

    def readable(self) -> bool:
        return (self._mode & O_ACCMODE) in (os.O_RDONLY, os.O_RDWR)

    def _file_length(self) -> int:
        return len(self._md["data"])

    def pwrite(self, buf: ReadableBuffer, offset: int) -> int:
        if not self.writable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        with self._md['lock']:
            header = self._md['data'][:offset]
            if len(header) < offset:
                header = b'%s%s' % (header, b'\0' * (offset - len(header)))
            blen = len(typing.cast(Sized, buf))
            d = self._md["data"] = b'%s%s%s' % (header, buf,
                                                self._md['data'][offset + blen:])
            m = self._md['mtime'] = datetime_now()
            self._md['ctime'] = datetime_now()
            self._md['revs'].append((m, d))
            return blen

    def writable(self) -> bool:
        return (self._mode & O_ACCMODE) in (os.O_WRONLY, os.O_RDWR)

    def ptruncate(self, offset: int) -> int:
        if not self.writable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        with self._md['lock']:
            if offset <= len(self._md['data']):
                d = self._md["data"] = self._md['data'][:offset]
            else:
                d = self._md["data"] = (self._md['data'] +
                                        b'\0' * (offset - len(self._md['data'])))
            m = self._md['mtime'] = datetime_now()
            self._md['ctime'] = datetime_now()
            self._md['revs'].append((m, d))
            return len(d)

ATTRS = ['name', 'mtime', 'type', 'size', 'id', 'ctime', 'rev']
Stat = collections.namedtuple("Stat", ['name', 'mtime', 'type', 'size', 'id', 'ctime', 'rev', 'attrs'])
_Stat = Stat

def _map_entry(md: MDDict, name: typing.Optional[str] = None) -> _Stat:
    mtime = md['mtime']
    ctime = md['ctime']
    type = md["type"]
    size = get_size(md)
    rev = get_rev(md)

    return _Stat(name, mtime, type, size, id=get_id(md), ctime=ctime, rev=rev,
                 attrs=ATTRS)

class _Directory(OldDirectoryProtocol):
    def __init__(self, md: MDDict):
        self._md = md
        self.reset()

    def reset(self) -> None:
        # copy list of children, n/s exactly what ext2/POSIX others do
        # in concurrent situations
        with self._md['lock']:
            l = list(get_children(self._md))
        # NB: I apologize if you're about to grep for _map_entry()
        self._iter = iter(map(lambda tup: _map_entry(tup[1], tup[0]), l))

    def close(self) -> None:
        pass

    def read(self) -> typing.Optional[_Stat]:
        try:
            return next(self)
        except StopIteration:
            return None

    def __iter__(self) -> typing.Self:
        return self

    def __next__(self) -> _Stat:
        return next(self._iter)

    def readmany(self, size: typing.Optional[int] = None) -> typing.List[_Stat]:
        ret = typing.cast(Iterator[_Stat], self)
        if size is not None:
            ret = itertools.islice(ret, size)
        return list(ret)

class _ReadStream(PositionIO):
    def __init__(self, data: bytes):
        super().__init__()
        self._data = data

    def pread(self, size: int, offset: int) -> memoryview:
        b = self._data[offset:
                       len(self._data) if size < 0 else offset + size]
        return memoryview(b)

    def readable(self) -> bool:
        return True

    def pwrite(self, buf: ReadableBuffer, offset: int) -> int:
        raise io.UnsupportedOperation()

    def ptruncate(self, offset: int) -> int:
        raise io.UnsupportedOperation()

    def _file_length(self) -> int:
        return len(self._data)

DropboxMD = collections.namedtuple(
    "DropboxMD",
    ["path_lower", "name", "client_modified",
     "size", "server_modified", "rev", "id"])

class MdRetriever(typing.Protocol):
    @abstractmethod
    def _get_file(self, path: Path, mode: int = 0, remove: typing.Optional[str] = None, directory: bool = False) -> MDDict:
        ...

    @abstractmethod
    def _md_from_id(self, id_: int) -> MDDict:
        ...

class _WriteStream(object):
    def __init__(self, fs: MdRetriever):
        self._fs = fs
        self._buf = io.BytesIO()

    def write(self, data: Buffer) -> None:
        self._buf.write(data)

    def close(self) -> None:
        pass

    def finish(self, resolver: Path | int, mode: str = "add", strict_conflict: bool = False,
               mtime: typing.Optional[datetime] = None) -> NewStat:
        # this reads a snapshotted file resolved by resolver
        if isinstance(resolver, Path):
            mode_ = 0
            if mode == "add":
                mode_ = mode_ | os.O_CREAT
                if strict_conflict:
                    mode_ = mode_ | os.O_EXCL
            elif mode == "overwrite":
                mode_ = mode_ | os.O_CREAT
            else:
                assert (isinstance(mode, tuple) and
                        mode[0] == 'update' and
                        mode[1][:4] == 'rev:')

            md = self._fs._get_file(resolver, mode=mode_)
        else:
            assert (isinstance(mode, tuple) and
                    mode[0] == 'update' and
                    mode[1][:4] == 'rev:')

            md = self._fs._md_from_id(resolver)

        if mode == "add":
            if get_size(md):
                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
        elif mode == "overwrite":
            pass
        else:
            if ((strict_conflict or get_size(md)) and
                mode[1] != get_rev(md)):
                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))

        if mtime is None:
            mtime = datetime_now()

        with md['lock']:
            d = md['data'] = self._buf.getvalue()
            m = md['mtime'] = mtime
            c = md['ctime'] = datetime_now()
            md['revs'].append((m, d))
            rev = get_rev(md)
            assert rev is not None
        self._buf.close()

        return NewStat(_map_entry(md))

@dc.dataclass
class StatVFSDC:
    f_frsize: int
    f_blocks: int
    f_bavail: int

class FileSystem(fsabc.FileSystemG[Path, _File]):
    def _new_id(self) -> str:
        while True:
            pid = random.randint(0, 2 ** 128 - 1)
            if pid not in self._id_to_file:
                break
        toret = ''.join(reversed(str(pid)))
        return toret

    def __init__(self, tree: Sequence[typing.Tuple[str, MDDict]] = ()) -> None:
        self._id_to_file = {}

        self._parent: MDDict = {
            "type": "directory", "children": [],
            'lock': threading.Lock(),
            'id': self._new_id(),
            'mtime': datetime_now(), 'ctime': datetime_now(),
        }
        self._id_to_file[self._parent['id']] = self._parent

        # give all files a lock
        # and an id
        files: typing.List[typing.Tuple[Path, MDDict, MDDict]]
        files = [(self.create_path(),
                  self._parent,
                  {"type": "directory", "children": tree})]
        while files:
            (dir_path, new_dir, dir_) = files.pop()
            for (name, child) in get_children(dir_):
                new_child = dict(child)
                new_child['path'] = dir_path.joinpath(name)
                new_child['name'] = name
                if 'mtime' not in new_child:
                    new_child['mtime'] = datetime_now()
                if 'ctime' not in new_child:
                    new_child['ctime'] = datetime_now()

                new_child['lock'] = threading.Lock()
                new_child['id'] = self._new_id()
                self._id_to_file[new_child['id']] = new_child

                if child['type'] == 'file':
                    new_child['revs'] = [(new_child['mtime'], new_child['data'])]
                else:
                    assert child['type'] == 'directory'
                    new_child['children'] = []
                    files.append((new_child['path'], new_child, child))
                new_dir['children'].append((name, new_child))

    def _map_entry(self, md: MDDict, name: typing.Optional[str] = None) -> _Stat:
        return _map_entry(md, name)


    def _get_file(self, path: Path, mode: int = 0, remove: typing.Optional[str] = None, directory: bool = False) -> MDDict:
        assert not (remove is not None and mode),\
            "Only one of mode/remove should be specified"
        parent = self._parent
        real_comps = []
        for comp in itertools.islice(path.parts, 1, None):
            if parent["type"] != "directory":
                raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

            with parent['lock']:
                for (idx, (name, md)) in enumerate(get_children(parent)):
                    if name.lower() == comp.lower():
                        real_comps.append(name)
                        if len(real_comps) == len(path.parts) - 1:
                            if (mode & os.O_CREAT) and (mode & os.O_EXCL):
                                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
                            if remove is not None:
                                if remove == 'unlink':
                                    if md['type'] != 'file':
                                        raise OSError(errno.EPERM, os.strerror(errno.EPERM))
                                elif remove == 'rmdir':
                                    if md['type'] != 'directory':
                                        raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))
                                    if get_children(md):
                                        raise OSError(errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY))
                                else:
                                    assert False, "Bad remove value!"
                                del self._id_to_file[md['id']]
                                del parent['children'][idx]

                        parent = md
                        break
                else:
                    real_comps.append(comp)
                    if (remove is None and
                        len(real_comps) == len(path.parts) - 1 and
                        (mode & os.O_CREAT)):
                        t = datetime_now()
                        if directory:
                            md = dict(type='directory',
                                      children=[],
                                      path=self.create_path(*real_comps),
                                      name=comp,
                                      mtime=t,
                                      ctime=t,
                                      id=self._new_id(),
                                      lock=threading.Lock())
                        else:
                            md = dict(type='file',
                                      data=b'',
                                      path=self.create_path(*real_comps),
                                      name=comp,
                                      mtime=t,
                                      ctime=t,
                                      lock=threading.Lock(),
                                      id=self._new_id(),
                                      revs=[(t, b'')])
                        self._id_to_file[md['id']] = md
                        parent.setdefault('children', []).append((comp, md))
                        parent = md
                        break
                    raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

        if mode & os.O_TRUNC and parent['type'] == 'file':
            with parent['lock']:
                parent['data'] = b''
                parent['revs'].append((datetime_now(), b''))

        return parent

    def parse_path(self, path: str) -> Path:
        return Path.parse_path(path, fn_norm=self.file_name_norm)

    def create_path(self, *args: str) -> Path:
        return Path.root_path(fn_norm=self.file_name_norm).joinpath(*args)

    def file_name_norm(self, fn: str) -> str:
        return fn.lower()

    def open(self, path: Path, mode: int = os.O_RDONLY, directory: bool = False) -> _File:
        md = self._get_file(path, mode, directory=directory)
        return _File(md, mode)

    def _md_from_id(self, id_: int) -> MDDict:
        try:
            return self._id_to_file[id_]
        except KeyError:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

    def x_open_by_id(self, id_: int, mode: int = os.O_RDONLY) -> _File:
        return _File(self._md_from_id(id_), mode)

    def x_open_by_rev(self, resolver: str, offset: typing.Optional[int] = None) -> _ReadStream:
        (md_id, rev_idx) = decode_rev(resolver)
        md = self._md_from_id(md_id)

        if rev_idx is None:
            d = md['data']
        else:
            d = md['revs'][rev_idx][1]

        if offset is not None:
            d = d[offset:]

        return _ReadStream(d)

    def x_write_stream(self) -> _WriteStream:
        return _WriteStream(self)

    def open_directory(self, path: Path) -> NewDirectory:
        md = self._get_file(path)
        if md['type'] != "directory":
            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

        return NewDirectory(_Directory(md))

    def x_stat_create(self, path: Path, mode: int, directory: bool = False) -> NewStat:
        return NewStat(self._map_entry(self._get_file(path, mode & ~os.O_TRUNC, directory=directory)))

    def stat(self, path: Path) -> NewStat:
        return self.x_stat_create(path, 0)

    def fstat(self, fobj: _File) -> NewStat:
        return NewStat(self._map_entry(fobj._md))

    def unlink(self, path: Path) -> None:
        self._get_file(path, remove='unlink')

    def mkdir(self, path: Path) -> None:
        st = self._get_file(path, mode=os.O_CREAT | os.O_EXCL, directory=True)
        assert st['type'] == 'directory'

    def rmdir(self, path: Path) -> None:
        self._get_file(path, remove='rmdir')

    def x_rename_stat(self, old_path: Path, new_path: Path, replace: bool = False) -> NewStat:
        parent = self._get_file(old_path.parent)
        target_parent = self._get_file(new_path.parent)

        if parent['type'] != 'directory' or target_parent['type'] != 'directory':
            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

        if id(parent) == id(target_parent):
            first, second = parent['lock'], null_context()
        elif id(parent) < id(target_parent):
            first, second = parent['lock'], target_parent['lock']
        else:
            first, second = target_parent['lock'], parent['lock']

        with first, second:
            for (idx, (name, md)) in enumerate(get_children(target_parent)):
                if name.lower() == new_path.name.lower() and old_path.name.lower() != name.lower():
                    if replace:
                        del self._id_to_file[md['id']]
                        del target_parent['children'][idx]
                    else:
                        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
            for (idx, (name, md)) in enumerate(get_children(parent)):
                if name.lower() == old_path.name.lower():
                    del parent['children'][idx]
                    break
            else:
                # In the period between the original get_file and now
                # the file was deleted
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

            get_children(target_parent).append((new_path.name, md))

            return NewStat(self._map_entry(md))

    def replace(self, old_path: Path, new_path: Path) -> None:
        self.x_rename_stat(old_path, new_path, replace=True)

    def statvfs(self) -> StatVFSDC:
        return StatVFSDC(f_frsize=2 ** 16,
                         f_blocks=2 ** 32 - 1,
                         f_bavail=2 ** 32 - 1)

    def preadinto(self, handle: _File, buf: Buffer, offset: int) -> int:
        datab = typing.cast(WriteableBuffer, buf)  # type: ignore[redundant-cast]
        return handle.preadinto(datab, offset)

    def pwrite(self, handle: _File, data: Buffer, offset: int) -> int:
        datab = typing.cast(ReadableBuffer, data)  # type: ignore[redundant-cast]
        return handle.pwrite(datab, offset)

    def fsync(self, _: _File) -> None:
        pass

    def futimes(self, handle: _File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        if times is not None:
            new_mtime_ts = times[1]
        else:
            new_mtime_ts = time.time()

        handle._md['mtime'] = datetime_from_ts(new_mtime_ts)
        handle._md['ctime'] = datetime_now()

    def close(self) -> None:
        pass

def _make_memory_fs(args: typing.Dict[str, typing.Any]) -> FileSystem:
    return FileSystem()

def main(argv: typing.Optional[Sequence[str]] = None) -> int:
    return simple_main_from_argv("memoryfs", ("userspacefs.memoryfs._make_memory_fs", {}), argv=argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
