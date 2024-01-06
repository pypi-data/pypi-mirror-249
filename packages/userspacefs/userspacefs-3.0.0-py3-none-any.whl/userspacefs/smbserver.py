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

import asyncio
import contextlib
import errno
import functools
import itertools
import os
import logging
import random
import socket
import sqlite3
import struct
import sys
import typing

import dataclasses as dc

from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from collections.abc import Callable, Sequence, Collection, Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from typing_extensions import TypedDict

import userspacefs.abc as fsabc

from userspacefs.util_dumpster import datetime_now, OldStat, OldDirectory, trans, SharedLock, ConnPool

log = logging.getLogger(__name__)

T = typing.TypeVar('T')

def _check_methods(C: typing.Type[typing.Any], *methods: str) -> bool:
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True

class MyBuffer(ABC):
    @abstractmethod
    def __buffer__(self, flags: int) -> memoryview:
        raise NotImplementedError()

    @classmethod
    def __subclasshook__(cls: typing.Type[typing.Self], C: typing.Type[typing.Any]) -> bool:
        if cls is MyBuffer:
            return _check_methods(C, "__buffer__")
        return NotImplemented

# this is not necessary in >= 3.12
MyBuffer.register(memoryview)
MyBuffer.register(bytes)
MyBuffer.register(bytearray)

class AsyncWorkerPool(object):
    def __init__(self, loop: asyncio.AbstractEventLoop, size: int = 1):
        self.loop = loop
        self.executor = ThreadPoolExecutor(None if size < 0 else size)

    async def run_async(self, f: Callable[..., T], *n: typing.Any, **kw: typing.Any) -> T:
        f = functools.partial(f, *n, **kw)
        fut = self.loop.run_in_executor(self.executor, f)
        return (await fut)

    def close(self) -> None:
        self.executor.shutdown(wait=False)

class AsyncFile:
    def __init__(self, obj: fsabc.File, worker_pool: AsyncWorkerPool):
        self._obj = obj
        self._worker_pool = worker_pool

    async def readinto(self, buf: memoryview | bytearray) -> int | None:
        return (await self._worker_pool.run_async(self._obj.readinto, buf))

    async def write(self, buf: memoryview | bytearray | bytes) -> int | None:
        return (await self._worker_pool.run_async(self._obj.write, buf))

    async def close(self) -> None:
        await self._worker_pool.run_async(self._obj.close)

    async def truncate(self, size: typing.Optional[int] = None) -> int:
        return (await self._worker_pool.run_async(self._obj.truncate, size=size))

class AsyncDirectory:
    def __init__(self, obj: fsabc.Directory, worker_pool: AsyncWorkerPool):
        self._obj = obj
        self._worker_pool = worker_pool

@dc.dataclass
class JustNameDirStat:
    name: str

class AsyncOldDirectory:
    def __init__(self, obj: OldDirectory, worker_pool: AsyncWorkerPool):
        self._obj = obj
        self._worker_pool = worker_pool

    async def readmany(self, amt: int) -> typing.List[JustNameDirStat]:
        ret = []
        for ds in (await self._worker_pool.run_async(self._obj.readmany, amt)):
            # NB: we can't use OldDirStat because it does blocking calls
            #     during property accesses
            ret.append(JustNameDirStat(ds.name))
        return ret

    async def read(self) -> typing.Optional[JustNameDirStat]:
        dirents = await self.readmany(1)
        if not dirents:
            return None
        return dirents[0]

    async def close(self) -> None:
        await self._worker_pool.run_async(self._obj.close)

class AsyncFS:
    def __init__(self, obj: fsabc.FileSystem, worker_pool: AsyncWorkerPool):
        self._obj = obj
        self._worker_pool = worker_pool

    async def old_open_directory(self, path: fsabc.Path) -> AsyncOldDirectory:
        new_dir_handle = (await self.open_directory(path))._obj

        old_dir_handle = OldDirectory(new_dir_handle)

        return AsyncOldDirectory(old_dir_handle, self._worker_pool)

    async def fstat(self, handle: AsyncFile) -> fsabc.Stat:
        # NB: we have to unwrap the async handle
        return (await self._worker_pool.run_async(self._obj.fstat,
                                                       handle._obj))

    async def fsync(self, handle: AsyncFile) -> None:
        # NB: we have to unwrap the async handle
        return (await self._worker_pool.run_async(self._obj.fsync,
                                                       handle._obj))

    async def preadinto(self, handle: AsyncFile, buf: bytearray | memoryview, offset: int) -> int:
        # NB: we have to unwrap the async handle
        return (await self._worker_pool.run_async(self._obj.preadinto,
                                                       handle._obj, buf, offset))

    async def pwrite(self, handle: AsyncFile, data: bytes, offset: int) -> int:
        # NB: we have to unwrap the async handle
        return (await self._worker_pool.run_async(self._obj.pwrite,
                                                       handle._obj, data, offset))

    async def futimes(self, handle: AsyncFile,
                      times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        # NB: we have to unwrap the async handle
        return (await self._worker_pool.run_async(self._obj.futimes,
                                                  handle._obj, times=times))

    def x_create_watch(self, cb: Callable[[fsabc.ChangeList], None],
                       dir_handle: AsyncFile, completion_filter: int, watch_tree: bool) -> Callable[[], None]:
        if not hasattr(self._obj, 'x_create_watch'):
            raise NotImplementedError()

        # NB: it would be better to guard the proceeding code on
        #     the condition that self._obj is an instance of CreateWatchExt
        #     instead of casting here but isinstance() currently doesn't work
        #     with generic protocols for some reason.
        obj = typing.cast(fsabc.CreateWatchExt, self._obj)

        is_stopped = [False]

        def on_main(changes: fsabc.ChangeList) -> None:
            if is_stopped[0]: return
            return cb(changes)

        def wrapped_cb(changes: fsabc.ChangeList) -> None:
            self._worker_pool.loop.call_soon_threadsafe(functools.partial(on_main, changes))

        stop = obj.x_create_watch(wrapped_cb, dir_handle._obj, completion_filter, watch_tree)

        def wrapped_stop() -> None:
            is_stopped[0] = True
            return stop()

        return wrapped_stop

    async def create_path(self, *parts : str) -> fsabc.Path:
        return (await self._worker_pool.run_async(self._obj.create_path,
                                                  *parts))

    async def open_directory(self, path: fsabc.Path) -> AsyncDirectory:
        handle = (await self._worker_pool.run_async(self._obj.open_directory, path))
        return AsyncDirectory(handle, self._worker_pool)

    async def statvfs(self) -> fsabc.StatVFS:
        return (await self._worker_pool.run_async(self._obj.statvfs))

    async def stat(self, path: fsabc.Path) -> fsabc.Stat:
        return (await self._worker_pool.run_async(self._obj.stat, path))

    async def open(self, path: fsabc.Path, mode: int) -> AsyncFile:
        handle = await self._worker_pool.run_async(self._obj.open, path, mode)
        return AsyncFile(handle, self._worker_pool)

    async def mkdir(self, path: fsabc.Path) -> None:
        await self._worker_pool.run_async(self._obj.mkdir, path)

    async def unlink(self, path: fsabc.Path) -> None:
        await self._worker_pool.run_async(self._obj.unlink, path)

    async def rmdir(self, path: fsabc.Path) -> None:
        await self._worker_pool.run_async(self._obj.rmdir, path)

    async def replace(self, path: fsabc.Path, pathb: fsabc.Path) -> None:
        await self._worker_pool.run_async(self._obj.replace, path, pathb)

class Backend(ABC):
    @abstractmethod
    def tree_connect(self, path: str) -> fsabc.FileSystem:
        raise NotImplementedError()

    @abstractmethod
    def tree_disconnect(self, fs: fsabc.FileSystem) -> None:
        raise NotImplementedError()

    @abstractmethod
    def tree_disconnect_hard(self, fs: fsabc.FileSystem) -> None:
        raise NotImplementedError()

class AsyncBackend:
    def __init__(self, backend: Backend, worker_pool: AsyncWorkerPool):
        self._obj = backend
        self._worker_pool = worker_pool

    async def tree_connect(self, path: str) -> AsyncFS:
        fs = await self._worker_pool.run_async(self._obj.tree_connect, path)
        return AsyncFS(fs, self._worker_pool)

    async def tree_disconnect(self, fs: AsyncFS) -> None:
        # unwraps the real fs out of fs
        return (await self._worker_pool.run_async(self._obj.tree_disconnect, fs._obj))

    async def tree_disconnect_hard(self, fs: AsyncFS) -> None:
        # unwraps the real fs out of fs
        return (await self._worker_pool.run_async(self._obj.tree_disconnect_hard, fs._obj))

SMB_COM_CLOSE = 0x04
SMB_COM_DELETE = 0x06
SMB_COM_RENAME = 0x07
SMB_COM_TRANSACTION = 0x25
SMB_COM_ECHO = 0x2B
SMB_COM_OPEN_ANDX = 0x2D
SMB_COM_READ_ANDX = 0x2E
SMB_COM_WRITE_ANDX = 0x2F
SMB_COM_TRANSACTION2 = 0x32
SMB_COM_NEGOTIATE = 0x72
SMB_COM_SESSION_SETUP_ANDX = 0x73
SMB_COM_TREE_CONNECT_ANDX = 0x75
SMB_COM_NT_TRANSACT = 0xA0
SMB_COM_NT_CREATE_ANDX = 0xA2
SMB_COM_QUERY_INFORMATION_DISK = 0x80
SMB_COM_CHECK_DIRECTORY = 0x10
SMB_COM_TREE_DISCONNECT = 0x71
SMB_COM_FLUSH = 0x05
SMB_COM_CREATE_DIRECTORY = 0x0
SMB_COM_DELETE_DIRECTORY = 0x1
SMB_COM_NO_ANDX_COMMAND = 0xff

SMB_COMMAND_TO_NAME = dict((v, k) for (k, v) in globals().items()
                           if k.startswith('SMB_COM_'))

SMB_FLAGS_REPLY = 0x80
SMB_FLAGS2_NT_STATUS = 0x4000
SMB_FLAGS2_UNICODE = 0x8000
SMB_FLAGS2_EXTENDED_SECURITY = 0x0800

CAP_RAW_MODE = 0x01
CAP_MPX_MODE = 0x02
CAP_UNICODE = 0x04
CAP_LARGE_FILES = 0x08
CAP_NT_SMBS = 0x10
CAP_RPC_REMOTE_APIS = 0x20
CAP_STATUS32 = 0x40
CAP_LEVEL_II_OPLOCKS = 0x80
CAP_LOCK_AND_READ = 0x0100
CAP_NT_FIND = 0x0200
CAP_DFS = 0x1000
CAP_INFOLEVEL_PASSTHRU = 0x2000
CAP_LARGE_READX = 0x4000
CAP_LARGE_WRITEX = 0x8000
CAP_LWIO = 0x010000
CAP_UNIX = 0x800000
CAP_COMPRESSED = 0x02000000
CAP_DYNAMIC_REAUTH = 0x20000000
CAP_PERSISTENT_HANDLES = 0x40000000
CAP_EXTENDED_SECURITY = 0x80000000

SMB_TREE_CONNECTX_SUPPORT_SEARCH = 0x0001

SMB_FILE_ATTRIBUTE_DIRECTORY = 0x10

SMB_MAX_DATA_PAYLOAD = 2 ** 16 - 1
DATA_BYTE_COUNT_LENGTH = 2

def parse_zero_terminated_utf16(buf: bytes, offset: int) -> typing.Tuple[str, int]:
    s = offset
    while True:
        next_offset = buf.index(b'\0\0', s)
        if (next_offset - offset) % 2: s = next_offset + 1
        else: break
    return (buf[offset:next_offset].decode("utf-16-le"), next_offset + 2)

SMBHeader = namedtuple('SMBHeader',
                       ['protocol', 'command',
                        'status', 'flags', 'flags2', 'pid',
                        'security_features', 'tid', 'uid', 'mid'])

def generate_simple_params_decoder(fmt: str, type_: type[T]) -> Callable[[SMBHeader, int, bytes], T]:
    def decode_params(_: SMBHeader, __: int, buf: bytes) -> T:
        try:
            return type_(*struct.unpack(fmt, buf))
        except Exception as e:
            raise Exception("Error while unpacking %s:%s" %
                            (type_.__name__, fmt)) from e
    return decode_params

SMBParameters = object
SMBData = object

@dc.dataclass
class SMBMessage(object):
    header: SMBHeader
    commands: typing.List[typing.Tuple[SMBParameters, SMBData]]

    def __init__(self,
                 header: SMBHeader,
                 parameters: SMBParameters,
                 data: SMBData):
        self.header = header
        self.commands = [(parameters, data)]

    @classmethod
    def from_commands(cls,
                      header: SMBHeader,
                      commands: typing.List[typing.Tuple[SMBParameters, SMBData]]) -> typing.Self:
        obj = super(SMBMessage, cls).__new__(cls)
        obj.header = header
        obj.commands = commands
        return obj

    # NB: this returns typing.Any for now. later we'll return SMBParameters
    #     and fix up all usage sites
    @property
    def parameters(self) -> typing.Any:
        assert len(self.commands) == 1, (
            "More than one command, use commands attribute"
        )
        return self.commands[0][0]

    # NB: this returns typing.Any for now. later we'll return SMBData
    #     and fix up all usage sites
    @property
    def data(self) -> typing.Any:
        assert len(self.commands) == 1, (
            "More than one command, use commands attribute"
        )
        return self.commands[0][1]

SMB_HEADER_STRUCT_FORMAT = "<4sBIBHHQxxHHHH"
SMB_HEADER_STRUCT_SIZE = struct.calcsize(SMB_HEADER_STRUCT_FORMAT)

def decode_smb_header(buf: bytes) -> SMBHeader:
    kw = {}
    (kw['protocol'], kw['command'], kw['status'],
     kw['flags'], kw['flags2'], pid_high, kw['security_features'], kw['tid'],
     pid_low, kw['uid'], kw['mid']) = struct.unpack(SMB_HEADER_STRUCT_FORMAT, buf)

    if kw['protocol'] != b'\xFFSMB':
        raise Exception('Invalid 4-byte protocol field: %r' % (kw['protocol'],))

    kw['pid'] = (pid_high << 16) | pid_low

    return SMBHeader(**kw)

def decode_null_params(_: SMBHeader, __: int, buf: bytes) -> None:
    if buf:
        raise Exception("Exception 0-length parameters")
    return None

def decode_null_data(_: SMBHeader, __: SMBParameters, ___: int, buf: bytes) -> None:
    if buf:
        raise Exception("Exception 0-length parameters")
    return None

def decode_byte_data(_: SMBHeader, __: SMBParameters, ___: int, buf: bytes) -> bytes:
    return buf

SMBNegotiateRequestData = namedtuple('SMBNegotiateRequestData', ['dialects'])
def decode_negotiate_request_data(_: SMBHeader, __: SMBParameters, ___: int, buf: bytes) -> SMBNegotiateRequestData:
    dialects = buf.split(b'\0')
    a = dialects.pop()
    if a: raise Exception("Non-trailing null byte!")
    dialects_s = [d.lstrip(b"\x02").decode("ascii") for d in dialects]
    return SMBNegotiateRequestData(dialects=dialects_s)

SMBSessionSetupAndxRequestParameters = namedtuple(
    'SMBSessionSetupAndxRequestParameters',
    ['andx_command', 'andx_reserved', 'andx_offset',
     'max_buffer_size', 'max_mpx_count',
     'vc_number', 'session_key',
     'oem_password_len', 'unicode_password_len',
     'reserved', 'capabilities'])

decode_session_setup_andx_request_params = generate_simple_params_decoder(
    '<BBHHHHIHHII',
    SMBSessionSetupAndxRequestParameters
)

SMBSessionSetupAndxRequestData = namedtuple(
    'SMBSessionSetupAndxRequestData',
    ['password', 'account_name', 'primary_domain',
     'native_os', 'native_lan_man'])
def decode_session_setup_andx_request_data(smb_header: SMBHeader, smb_parameters: SMBParameters,
                                           buf_offset: int, buf: bytes) -> SMBSessionSetupAndxRequestData:
    assert isinstance(smb_parameters, SMBSessionSetupAndxRequestParameters)
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only supports unicode!")

    if smb_parameters.oem_password_len:
        # NB: Mac OS X sends oem_password_len == 1 even when SMB_FLAGS2_UNICODE is
        #     set, even though this is against spec
        log.warning("OEM Password len must be 0 when SMB_FLAGS2_UNICODE is set: %r, %r" %
                    (smb_parameters.oem_password_len,
                     buf[:smb_parameters.oem_password_len]))

    # Linux CIFS_VFS client sends NTLMv2 even when we ask it not to
    password: typing.Optional[str]
    password = None
    #password = message.data[oem_password_len:oem_password_len + unicode_password_len].decode("utf-16-le")

    # read padding
    raw_offset = (buf_offset + smb_parameters.oem_password_len +
                  smb_parameters.unicode_password_len)
    if raw_offset % 2:
        if buf[raw_offset - buf_offset] != 0:
            raise Exception("Was expecting null byte!: %r" %
                            (buf[raw_offset - buf_offset],))
        raw_offset += 1

    kw: typing.Dict[str, typing.Optional[str]]
    kw = {'password' : password}

    rel_offset = raw_offset - buf_offset
    for n in ["account_name", "primary_domain", "native_os", "native_lan_man"]:
        (kw[n], rel_offset) = parse_zero_terminated_utf16(buf, rel_offset)

    return SMBSessionSetupAndxRequestData(**kw)

SMBTreeConnectAndxRequestParameters = namedtuple(
    'SMBTreeConnectAndxRequestParameters',
    ['andx_command', 'andx_reserved', 'andx_offset',
     'flags', 'password_len'])
decode_tree_connect_andx_request_params = generate_simple_params_decoder(
    "<BBHHH",
    SMBTreeConnectAndxRequestParameters
)

SMBTreeConnectAndxRequestData = namedtuple('SMBTreeConnectAndxRequestData',
                                           ['password', 'path', 'service'])
def decode_tree_connect_andx_request_data(smb_header: SMBHeader, smb_parameters: SMBParameters,
                                          buf_offset: int, buf: bytes) -> SMBTreeConnectAndxRequestData:
    assert isinstance(smb_parameters, SMBTreeConnectAndxRequestParameters)

    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only supports unicode!")

    # Linux CIFS_VFS client sends NTLMv2 even when we ask it not to
    password: typing.Optional[str]
    password = None
    #password = message.data[oem_password_len:oem_password_len + unicode_password_len].decode("utf-16-le")

    # read padding
    raw_offset = (buf_offset + smb_parameters.password_len)
    if raw_offset % 2:
        if buf[raw_offset - buf_offset] != 0:
            raise Exception("Was expecting null byte!: %r" %
                            (buf[raw_offset - buf_offset],))
        raw_offset += 1

    kw: typing.Dict[str, typing.Optional[str]]
    kw = {'password' : password}

    rel_offset = raw_offset - buf_offset
    (kw['path'], rel_offset) = parse_zero_terminated_utf16(buf, rel_offset)

    kw['service'] = buf[rel_offset:-1].decode("ascii")

    return SMBTreeConnectAndxRequestData(**kw)

SMBEchoRequestParameters = namedtuple('SMBEchoRequestParameters', ['echo_count'])
decode_echo_request_params = generate_simple_params_decoder(
    '<H',
    SMBEchoRequestParameters,
)

SMBTransaction2RequestParameters = namedtuple(
    'SMBTransaction2RequestParameters',
    ['total_parameter_count', 'total_data_count',
     'max_parameter_count', 'max_data_count',
     'max_setup_count', 'flags', 'timeout',
     'parameter_count', 'parameter_offset',
     'data_count', 'data_offset', 'setup'])
def decode_transaction_2_request_params(_: SMBHeader, __: int, buf: bytes) -> SMBTransaction2RequestParameters:
    fmt = '<HHHHBBHIHHHHHH'
    fmt_size = struct.calcsize(fmt)

    kw = {}
    (kw['total_parameter_count'], kw['total_data_count'],
     kw['max_parameter_count'], kw['max_data_count'],
     kw['max_setup_count'], _, kw['flags'], kw['timeout'],
     _, kw['parameter_count'], kw['parameter_offset'], kw['data_count'],
     kw['data_offset'], setup_words_len) = struct.unpack(fmt, buf[:fmt_size])


    kw['setup'] = struct.unpack("<%dH" % (setup_words_len,),
                                buf[fmt_size : fmt_size + setup_words_len * 2])

    return SMBTransaction2RequestParameters(**kw)


SMBTransaction2RequestData = \
    namedtuple('SMBTransaction2RequestData',
               ['parameters', 'data'])
def decode_transaction_2_request_data(smb_header: SMBHeader, smb_parameters: SMBParameters,
                                      buf_offset: int, buf: bytes) -> SMBTransaction2RequestData:
    assert isinstance(smb_parameters, SMBTransaction2RequestParameters)
    params = buf[smb_parameters.parameter_offset - buf_offset :
                 smb_parameters.parameter_offset - buf_offset + smb_parameters.parameter_count]

    data = buf[smb_parameters.data_offset - buf_offset :
               smb_parameters.data_offset - buf_offset + smb_parameters.data_count]

    return SMBTransaction2RequestData(params, data)


SMBNTCreateAndxRequestParameters = namedtuple(
    'SMBNTCreateAndxRequestParameters',
    ['andx_command', 'andx_reserved', 'andx_offset',
     'reserved1', 'name_length', 'flags',
     'root_directory_fid', 'desired_access',
     'allocation_size', 'ext_file_attributes',
     'share_access', 'create_disposition',
    'create_options', 'impersonation_level',
     'security_flags'])
decode_nt_create_andx_request_params = generate_simple_params_decoder(
    "<BBHBHIIIQIIIIIB",
    SMBNTCreateAndxRequestParameters,
)

SMBNTCreateAndxRequestData = \
    namedtuple('SMBNTCreateAndxRequestData', ['filename'])
def decode_nt_create_andx_request_data(smb_header: SMBHeader, smb_parameters: SMBParameters,
                                       buf_offset: int, buf: bytes) -> SMBNTCreateAndxRequestData:
    assert isinstance(smb_parameters, SMBNTCreateAndxRequestParameters)
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only support unicode!")

    raw_offset = buf_offset
    if raw_offset % 2:
        raw_offset += 1

    filename = buf[raw_offset - buf_offset :
                   raw_offset - buf_offset + smb_parameters.name_length].decode("utf-16-le").rstrip("\0")
    return SMBNTCreateAndxRequestData(filename)

SMBReadAndxRequestParameters = \
    namedtuple('SMBReadAndxRequestParameters',
               ['andx_command', 'andx_reserved', 'andx_offset',
                'fid', 'offset',
                'max_count_of_bytes_to_return',
                'min_count_of_bytes_to_return',
                'timeout', 'remaining'])
def decode_read_andx_request_params(_: SMBHeader, __: int, buf: bytes) -> SMBReadAndxRequestParameters:
    kw = {}

    fmt = "<BBHHLHHLH"
    fmt_size = struct.calcsize(fmt)
    (kw['andx_command'], kw['andx_reserved'], kw['andx_offset'],
     kw['fid'], kw['offset'],
     kw['max_count_of_bytes_to_return'],
     kw['min_count_of_bytes_to_return'],
     kw['timeout'], kw['remaining']) = struct.unpack(fmt, buf[:fmt_size])

    if len(buf) > fmt_size:
        (offset_high,) = struct.unpack("<I", buf[fmt_size:])
        kw['offset'] = (offset_high << 32) | kw['offset']

    return SMBReadAndxRequestParameters(**kw)

SMBComCloseRequestParameters = namedtuple('SMBComCloseRequestParameters',
                                          ['fid', 'last_modified_time'])
decode_close_request_params = generate_simple_params_decoder(
    "<HL",
    SMBComCloseRequestParameters,
)
SMBNTTransactRequestParameters = \
    namedtuple('SMBNTTransactRequestParameters',
               ['max_setup_count',
                'total_parameter_count', 'total_data_count',
                'max_parameter_count', 'max_data_count',
                'parameter_count', 'parameter_offset',
                'data_count', 'data_offset',
                'function',
                'setup'])
def decode_nt_transact_request_params(smb_header: SMBHeader, _: int, buf: bytes) -> SMBNTTransactRequestParameters:
    fmt = "<BHLLLLLLLLBH"
    fmt_size = struct.calcsize(fmt)

    kw = {}
    (kw['max_setup_count'], _,
     kw['total_parameter_count'], kw['total_data_count'],
     kw['max_parameter_count'], kw['max_data_count'],
     kw['parameter_count'], kw['parameter_offset'],
     kw['data_count'], kw['data_offset'],
     setup_count,
     kw['function']) = struct.unpack(fmt, buf[:fmt_size])

    kw['setup'] = buf[fmt_size : fmt_size + setup_count * 2]

    return SMBNTTransactRequestParameters(**kw)

SMBNTTransactRequestData = namedtuple(
    'SMBNTTransactRequestData', ['parameters', 'data'])
def decode_nt_transact_request_data(smb_header: SMBHeader, smb_parameters: SMBParameters,
                                    buf_offset: int, buf: bytes) -> SMBNTTransactRequestData:
    assert isinstance(smb_parameters, SMBNTTransactRequestParameters)
    params = buf[smb_parameters.parameter_offset - buf_offset :
                 smb_parameters.parameter_offset - buf_offset + smb_parameters.parameter_count]

    data = buf[smb_parameters.data_offset - buf_offset :
               smb_parameters.data_offset - buf_offset + smb_parameters.data_count]

    return SMBNTTransactRequestData(params, data)

SMBCheckDirectoryRequestData = namedtuple('SMBCheckDirectoryRequestData', ['filename'])
def decode_check_directory_request_data(smb_header: SMBHeader, __: SMBParameters,
                                        ___: int, buf: bytes) -> SMBCheckDirectoryRequestData:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only support unicode!")

    filename = buf.decode('utf-16-le').rstrip('\0')
    return SMBCheckDirectoryRequestData(filename=filename)

SMBWriteAndxRequestParameters = namedtuple(
    'SMBWriteAndxRequestParameters',
    ['andx_command', 'andx_reserved', 'andx_offset',
     'fid', 'offset', 'timeout', 'write_mode', 'remaining',
     'data_length', 'data_offset'])
def decode_write_andx_request_params(_: SMBHeader, __: int, buf: bytes) -> SMBWriteAndxRequestParameters:
    kw = {}

    fmt = "<BBHHLLHHHHH"
    fmt_size = struct.calcsize(fmt)
    (kw['andx_command'], kw['andx_reserved'], kw['andx_offset'],
     kw['fid'], kw['offset'],
     kw['timeout'], kw['write_mode'],
     kw['remaining'], _reserved, kw['data_length'],
     kw['data_offset']) = struct.unpack(fmt, buf[:fmt_size])

    if len(buf) > fmt_size:
        (offset_high,) = struct.unpack("<L", buf[fmt_size:])
        kw['offset'] = (offset_high << 32) | kw['offset']

    return SMBWriteAndxRequestParameters(**kw)

def decode_write_andx_request_data(_: SMBHeader, params: SMBParameters, __: int, buf: bytes) -> bytes:
    assert isinstance(params, SMBWriteAndxRequestParameters)
    # NB: skip pad byte
    if (len(buf) - 1) < params.data_length:
        raise Exception("Not enough data! %r vs %r" %
                        (len(buf) - 1, params.data_length))
    elif (len(buf) - 1) > params.data_length:
        log.warn("Got more data than was expecting %r %r",
                 len(buf) - 1, params.data_length)
    return buf[1:1 + params.data_length]

SMBComFlushParameters = namedtuple('SMBComFlushParameters',
                                   ['fid'])
decode_flush_request_params = generate_simple_params_decoder(
    "<H",
    SMBComFlushParameters
)

SMBDeleteRequestParameters = namedtuple(
    'SMBDeleteRequestParameters',
    ['search_attributes'])
decode_delete_request_params = generate_simple_params_decoder(
    "<H",
    SMBDeleteRequestParameters,
)

SMBDeleteRequestData = namedtuple('SMBDeleteRequestData',
                                  ['buffer_format', 'filename'])
def decode_delete_request_data(smb_header: SMBHeader, _: SMBParameters,
                               __: int, buf: bytes) -> SMBDeleteRequestData:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only support unicode!")

    (buffer_format,) = struct.unpack("<B", buf[:1])
    filename = buf[1:].decode('utf-16-le').rstrip('\0')
    return SMBDeleteRequestData(buffer_format, filename)

# It's the same structure
decode_create_directory_request_data = decode_delete_request_data
decode_delete_directory_request_data = decode_delete_request_data

# same structure
decode_rename_request_params = decode_delete_request_params

SMBRenameRequestData = namedtuple('SMBRenameRequestData',
                                  ['buffer_format_1', 'old_filename',
                                   'buffer_format_2', 'new_filename'])
def decode_rename_request_data(smb_header: SMBHeader, _: SMBParameters, __: int, buf: bytes) -> SMBRenameRequestData:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only support unicode!")

    (buffer_format_1,) = struct.unpack("<B", buf[:1])
    (old_filename, new_offset) = parse_zero_terminated_utf16(buf, 1)
    (buffer_format_2,) = struct.unpack("<B", buf[new_offset:new_offset + 1])
    (new_filname, _) = parse_zero_terminated_utf16(buf, new_offset + 2)

    return SMBRenameRequestData(buffer_format_1, old_filename,
                                buffer_format_2, new_filname)

REQUEST = False
REPLY = True
_decoder_dispatch: typing.Dict[typing.Tuple[int, bool],
                               typing.Tuple[Callable[[SMBHeader, int, bytes], SMBParameters],
                                            Callable[[SMBHeader, SMBParameters, int, bytes], SMBData]]]
_decoder_dispatch = {
    (SMB_COM_NEGOTIATE, REQUEST): (decode_null_params,
                                   decode_negotiate_request_data),
    (SMB_COM_SESSION_SETUP_ANDX, REQUEST): (decode_session_setup_andx_request_params,
                                            decode_session_setup_andx_request_data),
    (SMB_COM_TREE_CONNECT_ANDX, REQUEST): (decode_tree_connect_andx_request_params,
                                           decode_tree_connect_andx_request_data),
    (SMB_COM_TREE_DISCONNECT, REQUEST): (decode_null_params,
                                         decode_null_data),
    (SMB_COM_ECHO, REQUEST): (decode_echo_request_params,
                              decode_byte_data),
    (SMB_COM_TRANSACTION2, REQUEST): (decode_transaction_2_request_params,
                                      decode_transaction_2_request_data),
    (SMB_COM_QUERY_INFORMATION_DISK, REQUEST): (decode_null_params,
                                                decode_null_data),
    (SMB_COM_NT_CREATE_ANDX, REQUEST): (decode_nt_create_andx_request_params,
                                        decode_nt_create_andx_request_data),
    (SMB_COM_READ_ANDX, REQUEST): (decode_read_andx_request_params,
                                   decode_null_data),
    (SMB_COM_CLOSE, REQUEST): (decode_close_request_params,
                               decode_null_data),
    (SMB_COM_NT_TRANSACT, REQUEST): (decode_nt_transact_request_params,
                                     decode_nt_transact_request_data),
    (SMB_COM_CHECK_DIRECTORY, REQUEST): (decode_null_params,
                                         decode_check_directory_request_data),
    (SMB_COM_WRITE_ANDX, REQUEST): (decode_write_andx_request_params,
                                    decode_write_andx_request_data),
    (SMB_COM_FLUSH, REQUEST): (decode_flush_request_params,
                               decode_null_data),
    (SMB_COM_DELETE, REQUEST): (decode_delete_request_params,
                                decode_delete_request_data),
    (SMB_COM_CREATE_DIRECTORY, REQUEST): (decode_null_params,
                                          decode_create_directory_request_data),
    (SMB_COM_DELETE_DIRECTORY, REQUEST): (decode_null_params,
                                          decode_delete_directory_request_data),
    (SMB_COM_RENAME, REQUEST): (decode_rename_request_params,
                                decode_rename_request_data),
}

def get_decoder(command: int, is_reply: bool) -> typing.Tuple[Callable[[SMBHeader, int, bytes], SMBParameters],
                                                              Callable[[SMBHeader, SMBParameters, int, bytes], SMBData]]:
    try:
        return _decoder_dispatch[(command, is_reply)]
    except KeyError:
        raise ProtocolError(STATUS_NOT_SUPPORTED)

def decode_smb_payload(smb_header: SMBHeader, buf: bytes) -> typing.List[typing.Tuple[SMBParameters, SMBData]]:
    cur_offset = SMB_HEADER_STRUCT_SIZE

    command = smb_header.command
    is_reply = bool(smb_header.flags & SMB_FLAGS_REPLY)

    commands: typing.List[typing.Tuple[SMBParameters, SMBData]] = []

    while True:
        (params_decoder, data_decoder) = get_decoder(command, is_reply)

        params_size = buf[cur_offset] * 2
        cur_offset += 1

        smb_parameters = params_decoder(smb_header, cur_offset,
                                        buf[cur_offset : cur_offset + params_size])
        cur_offset += params_size

        (data_size,) = struct.unpack("<H", buf[cur_offset : cur_offset + 2])
        cur_offset += 2

        smb_data = data_decoder(smb_header, smb_parameters, cur_offset,
                                buf[cur_offset : cur_offset + data_size])
        cur_offset += data_size

        commands.append((smb_parameters, smb_data))

        if hasattr(smb_parameters, 'andx_command'):
            assert hasattr(smb_parameters, 'andx_offset')
            command = smb_parameters.andx_command
            if command == SMB_COM_NO_ANDX_COMMAND:
                break
            else:
                cur_offset = smb_parameters.andx_offset
        else:
            break

    return commands

def decode_smb_message(buf: bytes) -> SMBMessage:
    smb_header = decode_smb_header(buf[:SMB_HEADER_STRUCT_SIZE])
    commands = decode_smb_payload(smb_header, buf)

    return SMBMessage.from_commands(smb_header, commands)

def encode_null_params(header: SMBHeader, buf_offset: int, parameters: SMBParameters) -> bytes:
    assert parameters is None
    return b''

def encode_null_data(header: SMBHeader, parameters: SMBParameters, buf_offset: int, data: SMBData) -> bytes:
    assert data is None
    return b''

def encode_byte_data(header: SMBHeader, parameters: SMBParameters, buf_offset: int, data: SMBData) -> bytes:
    assert isinstance(data, MyBuffer), "Data is not a buffer: %r" % (data,)
    return bytes(memoryview(data))

def generate_simple_parameter_encoder(fmt: str, attrs: Sequence[typing.Optional[str]]) -> typing.Callable[[SMBHeader, int, SMBParameters], bytes]:
    def encoder(_: SMBHeader, buf_offset: int, parameters: SMBParameters) -> bytes:
        return struct.pack(fmt, *[getattr(parameters, a) if a is not None else 0
                                  for a in attrs])
    return encoder

SMBNegotiateReplyParameters = namedtuple(
    'SMBNegotiateReplyParameters',
    ['dialect_index', 'security_mode', 'max_mpx_count',
     'max_number_vcs', 'max_buffer_size', 'max_raw_size',
     'session_key', 'capabilities', 'system_time',
     'server_time_zone', 'challenge_length']
)

encode_negotiate_reply_parameters = generate_simple_parameter_encoder(
    '<HBHHIIIIQhB',
    SMBNegotiateReplyParameters._fields,
)

SMBNegotiateReplyData = namedtuple('SMBNegotiateReplyData',
                                   ['challenge', 'domain_name'])

def encode_negotiate_reply_data(header: SMBHeader, parameters: SMBParameters,
                                buf_offset: int, data: SMBData) -> bytes:
    assert isinstance(parameters, SMBNegotiateReplyParameters)
    assert isinstance(data, SMBNegotiateReplyData)
    if not (header.flags2 & SMB_FLAGS2_UNICODE):
        raise NotImplementedError("non-unicode not implemented!")

    assert parameters.challenge_length == len(data.challenge)
    return b''.join([data.challenge,
                     (data.domain_name + "\0").encode('utf-16-le')])

SMBSessionSetupAndxReplyParameters = namedtuple(
    'SMBSessionSetupAndxReplyParameters',
    ['andx_command', 'andx_reserved', 'andx_offset', 'action'],
)

encode_session_setup_andx_reply_params = generate_simple_parameter_encoder(
    '<BBHH',
    SMBSessionSetupAndxReplyParameters._fields,
)

SMBSessionSetupAndxReplyData = namedtuple(
    'SMBSessionSetupAndxReplyData',
    ['native_os', 'native_lan_man', 'primary_domain'])
def encode_session_setup_andx_reply_data(header: SMBHeader, parameters: SMBParameters,
                                         buf_offset: int, data: SMBData) -> bytes:
    assert isinstance(data, SMBSessionSetupAndxReplyData)
    if not (header.flags2 & SMB_FLAGS2_UNICODE):
        raise NotImplementedError("non-unicode not implemented!")

    prefix = b''
    if buf_offset % 2:
        prefix += b'\0'

    return b''.join(itertools.chain([prefix],
                                    (x.encode('utf-16-le')
                                     for x in [data.native_os, "\0",
                                               data.native_lan_man, "\0",
                                               data.primary_domain, "\0"])))

SMBTreeConnectAndxReplyParameters = namedtuple(
    'SMBTreeConnectAndxReplyParameters',
    ['andx_command', 'andx_reserved', 'andx_offset', 'optional_support'],
)

encode_tree_connect_reply_params = generate_simple_parameter_encoder(
    '<BBHH',
    SMBTreeConnectAndxReplyParameters._fields,
    )


SMBTreeConnectAndxReplyData = namedtuple(
    'SMBTreeConnectAndxReplyData',
    ['service', 'native_file_system'])
def encode_tree_connect_reply_data(header: SMBHeader, parameters: SMBParameters,
                                   buf_offset: int, data: SMBData) -> bytes:
    assert isinstance(data, SMBTreeConnectAndxReplyData)
    if not (header.flags2 & SMB_FLAGS2_UNICODE):
        raise NotImplementedError("non-unicode not implemented!")

    return b''.join([data.service.encode("ascii"),
                     b"\0",
                     data.native_file_system.encode("utf-16-le"),
                     b'\0\0'])

SMBEchoReplyParameters = namedtuple(
    'SMBEchoReplyParameters',
    ["sequence_number"],
)

encode_echo_reply_params = generate_simple_parameter_encoder(
    "<H",
    SMBEchoReplyParameters._fields,
)

SMBTransaction2ReplyParameters = namedtuple(
    'SMBTransaction2ReplyParameters',
    ['total_parameter_count', 'total_data_count',
     'parameter_count', 'parameter_displacement',
     'data_count', 'data_displacement',
     'setup']
)
def encode_transaction_2_reply_params(header: SMBHeader, buf_offset: int, parameters: SMBParameters) -> bytes:
    assert isinstance(parameters, SMBTransaction2ReplyParameters)

    fmt = "<HHHHHHHHHBB"

    data_offset = (buf_offset +
                   struct.calcsize(fmt) +
                   len(parameters.setup) * 2 +
                   DATA_BYTE_COUNT_LENGTH)

    trans2_params_offset = data_offset
    if trans2_params_offset % 4:
        trans2_params_offset += 4 - trans2_params_offset % 4

    trans2_data_offset = trans2_params_offset + parameters.parameter_count
    if trans2_data_offset % 4:
        trans2_data_offset += 4 - trans2_data_offset % 4

    return b''.join([struct.pack(fmt,
                                 parameters.total_parameter_count,
                                 parameters.total_data_count,
                                 0,
                                 parameters.parameter_count,
                                 trans2_params_offset,
                                 parameters.parameter_displacement,
                                 parameters.data_count,
                                 trans2_data_offset,
                                 parameters.data_displacement,
                                 len(parameters.setup), 0),
                     struct.pack('<%dH' % (len(parameters.setup),),
                                 *parameters.setup)])

SMBTransaction2ReplyData = namedtuple(
    'SMBTransaction2ReplyData',
    ['parameters', 'data'])
def encode_transaction_2_reply_data(header: SMBHeader, parameters: SMBParameters,
                                    buf_offset: int, data: SMBData) -> bytes:
    assert isinstance(data, SMBTransaction2ReplyData)
    trans2_params_offset = buf_offset
    if trans2_params_offset % 4:
        trans2_params_offset += 4 - trans2_params_offset % 4

    trans2_data_offset = trans2_params_offset + len(data.parameters)
    if trans2_data_offset % 4:
        trans2_data_offset += 4 - trans2_data_offset % 4

    return b''.join([(trans2_params_offset - buf_offset) * b'\0',
                     data.parameters,
                     (trans2_data_offset - (trans2_params_offset + len(data.parameters))) * b'\0',
                     data.data])

SMBQueryInformationDiskReplyParameters = namedtuple(
    'SMBQueryInformationDiskReplyParameters',
    ["total_units", "blocks_per_unit", "block_size", "free_units"],
)

encode_query_information_disk_reply_params = generate_simple_parameter_encoder(
    "<HHHHH",
    SMBQueryInformationDiskReplyParameters._fields,
)


SMBNTCreateAndxReplyData = namedtuple(
    'SMBNTCreateAndxReplyData',
    ["andx_command", "andx_reserved", "andx_offset",
     'op_lock_level', 'fid', 'create_disposition', 'create_time',
     'last_access_time', 'last_write_time', 'last_change_time',
     'ext_file_attributes', 'allocation_size', 'end_of_file',
     'resource_type', 'nm_pipe_status', 'directory'],
)

encode_nt_create_andx_reply_params = generate_simple_parameter_encoder(
    "<BBHBHLQQQQLQQHHB",
    SMBNTCreateAndxReplyData._fields,
)

SMBReadAndxReplyParameters = namedtuple(
    'SMBReadAndxReplyParameters',
    ['andx_command', 'andx_reserved', 'andx_offset',
     'available', 'data_length']
)
def encode_read_andx_reply_params(header: SMBHeader, buf_offset: int, parameters: SMBParameters) -> bytes:
    assert isinstance(parameters, SMBReadAndxReplyParameters)
    fmt = "<BBHHHHHHHHHHH"

    offset = buf_offset + struct.calcsize(fmt) + DATA_BYTE_COUNT_LENGTH
    if offset % 2:
        offset += 1

    p = parameters
    return struct.pack(fmt,
                       p.andx_command, p.andx_reserved, p.andx_offset,
                       p.available, 0, 0, p.data_length, offset,
                       0, 0, 0, 0, 0)

def encode_read_andx_reply_data(header: SMBHeader, parameters: SMBParameters,
                                buf_offset: int, data_pre: SMBData) -> bytes:
    assert isinstance(data_pre, MyBuffer), "data is not a Buffer: %r" % (data_pre,)
    assert isinstance(parameters, SMBReadAndxReplyParameters)
    data = memoryview(data_pre)
    assert parameters.data_length == len(data)

    pad = b''
    if buf_offset % 2:
        pad += b'\0'

    return b''.join([pad, data])

SMBNTTransactReplyParameters = namedtuple(
    'SMBNTTransactReplyParameters',
    ['total_parameter_count', 'total_data_count',
     'parameter_count', 'parameter_displacement',
     'data_count', 'data_displacement',
     'setup']
)
def encode_nt_transact_reply_params(header: SMBHeader, buf_offset: int, parameters: SMBParameters) -> bytes:
    assert isinstance(parameters, SMBNTTransactReplyParameters)

    fmt = "<BBBLLLLLLLLB"

    data_offset = (buf_offset +
                   struct.calcsize(fmt) +
                   len(parameters.setup) * 2 +
                   DATA_BYTE_COUNT_LENGTH)

    nt_transact_params_offset = data_offset
    if nt_transact_params_offset % 4:
        nt_transact_params_offset += 4 - nt_transact_params_offset % 4

    nt_transact_data_offset = nt_transact_params_offset + parameters.parameter_count
    if nt_transact_data_offset % 4:
        nt_transact_data_offset += 4 - nt_transact_data_offset % 4

    assert not (len(parameters.setup) % 2)

    return b''.join([struct.pack(fmt,
                                 0, 0, 0,
                                 parameters.total_parameter_count,
                                 parameters.total_data_count,
                                 parameters.parameter_count,
                                 nt_transact_params_offset,
                                 parameters.parameter_displacement,
                                 parameters.data_count,
                                 nt_transact_data_offset,
                                 parameters.data_displacement,
                                 len(parameters.setup) // 2),
                     parameters.setup])

SMBNTTransactReplyData = namedtuple(
    'SMBNTTransactReplyData', ['parameters', 'data'])
def encode_nt_transact_reply_data(header: SMBHeader, parameters: SMBParameters,
                                  data_offset: int, data: SMBData) -> bytes:
    assert isinstance(data, SMBNTTransactReplyData)
    nt_transact_params_offset = data_offset
    if nt_transact_params_offset % 4:
        nt_transact_params_offset += 4 - nt_transact_params_offset % 4

    nt_transact_data_offset = nt_transact_params_offset + len(data.parameters)
    if nt_transact_data_offset % 4:
        nt_transact_data_offset += 4 - nt_transact_data_offset % 4

    return b''.join([(nt_transact_params_offset - data_offset) * b'\0',
                     data.parameters,
                     (nt_transact_data_offset - (nt_transact_params_offset +
                                                 len(data.parameters))) * b'\0',
                     data.data])

SMBWriteAndxReplyParameters = namedtuple(
    'SMBWriteAndxReplyParameters',
    ["andx_command", "andx_reserved", "andx_offset",
     "count", "available"],
)

encode_write_andx_reply_params = generate_simple_parameter_encoder(
    "<BBHHHL",
    list(SMBWriteAndxReplyParameters._fields) + [None],
)

_encoder_dispatch: typing.Dict[typing.Tuple[int, bool],
                               typing.Tuple[Callable[[SMBHeader, int, SMBParameters], bytes],
                                            Callable[[SMBHeader, SMBParameters, int, SMBData], bytes]]]
_encoder_dispatch = {
    (SMB_COM_NEGOTIATE, REPLY): (encode_negotiate_reply_parameters,
                                 encode_negotiate_reply_data),
    (SMB_COM_SESSION_SETUP_ANDX, REPLY): (encode_session_setup_andx_reply_params,
                                          encode_session_setup_andx_reply_data),
    (SMB_COM_TREE_CONNECT_ANDX, REPLY): (encode_tree_connect_reply_params,
                                         encode_tree_connect_reply_data),
    (SMB_COM_TREE_DISCONNECT, REPLY): (encode_null_params,
                                       encode_null_data),
    (SMB_COM_ECHO, REPLY): (encode_echo_reply_params,
                            encode_byte_data),
    (SMB_COM_TRANSACTION2, REPLY): (encode_transaction_2_reply_params,
                                    encode_transaction_2_reply_data),
    (SMB_COM_QUERY_INFORMATION_DISK, REPLY): (encode_query_information_disk_reply_params,
                                              encode_null_data),
    (SMB_COM_NT_CREATE_ANDX, REPLY): (encode_nt_create_andx_reply_params,
                                      encode_null_data),
    (SMB_COM_READ_ANDX, REPLY): (encode_read_andx_reply_params,
                                 encode_read_andx_reply_data),
    (SMB_COM_CLOSE, REPLY): (encode_null_params,
                             encode_null_data),
    (SMB_COM_NT_TRANSACT, REPLY): (encode_nt_transact_reply_params,
                                   encode_nt_transact_reply_data),
    (SMB_COM_CHECK_DIRECTORY, REPLY): (encode_null_params,
                                       encode_null_data),
    (SMB_COM_WRITE_ANDX, REPLY): (encode_write_andx_reply_params,
                                  encode_null_data),
    (SMB_COM_FLUSH, REPLY): (encode_null_params,
                             encode_null_data),
    (SMB_COM_DELETE, REPLY): (encode_null_params,
                              encode_null_data),
    (SMB_COM_CREATE_DIRECTORY, REPLY): (encode_null_params,
                                        encode_null_data),
    (SMB_COM_DELETE_DIRECTORY, REPLY): (encode_null_params,
                                        encode_null_data),
    (SMB_COM_RENAME, REPLY): (encode_null_params,
                              encode_null_data),
}

def get_encoder(command: int, is_reply: bool) -> typing.Tuple[Callable[[SMBHeader, int, SMBParameters], bytes],
                                                   Callable[[SMBHeader, SMBParameters, int, SMBData], bytes]]:
    return _encoder_dispatch[(command, is_reply)]

def encode_smb_header(header: SMBHeader) -> bytes:
    return struct.pack(SMB_HEADER_STRUCT_FORMAT,
                       b'\xFFSMB', header.command, header.status, header.flags,
                       header.flags2, (header.pid >> 16) & 0xFFFF,
                       header.security_features, header.tid,
                       header.pid & 0xFFFF, header.uid, header.mid)

def encode_smb_message(msg: SMBMessage) -> bytes:
    cur_offset = 0

    header = encode_smb_header(msg.header)
    cur_offset += len(header)

    bufs = [header]

    if msg.header.status:
        # This is an "error response" message
        cur_offset += 1
        params = b''
        cur_offset += DATA_BYTE_COUNT_LENGTH
        buf = b''

        bufs.extend([struct.pack("<B", len(params) // 2), params,
                     struct.pack("<H", len(buf)), buf])
    else:
        command, is_reply = (msg.header.command, bool(msg.header.flags & SMB_FLAGS_REPLY))
        for (parameters, data) in msg.commands:
            (params_encoder, data_encoder) = get_encoder(command, is_reply)

            # account for word-length prefix
            cur_offset += 1

            params = params_encoder(msg.header, cur_offset, parameters)
            assert not (len(params) % 2)
            cur_offset += len(params)

            # account for byte-length prefix
            cur_offset += DATA_BYTE_COUNT_LENGTH
            assert DATA_BYTE_COUNT_LENGTH == 2

            buf = data_encoder(msg.header, parameters, cur_offset, data)
            cur_offset += len(buf)

            pre_buf = b''.join([struct.pack("<B", len(params) // 2), params,
                                struct.pack("<H", len(buf)), buf])
            buf = bytearray(pre_buf)

            # now encode andxoffset
            if hasattr(parameters, 'andx_offset'):
                buf[3:5] = struct.pack("<H", cur_offset)

            bufs.append(bytes(buf))

            if hasattr(parameters, 'andx_command'):
                command = parameters.andx_command
            else:
                command = SMB_COM_NO_ANDX_COMMAND


    toret = b''.join(bufs)

    assert len(toret) == cur_offset

    return toret

SMBTransaction2FindFirstRequestParameters = namedtuple(
    'SMBTransaction2FindFirstRequestParameters',
    ['search_attributes', 'search_count',
     'flags', 'information_level',
     'search_storage_type', 'filename'])
def decode_transaction_2_find_first_request_params(smb_header: SMBHeader, _: SMBParameters, buf: bytes) -> SMBTransaction2FindFirstRequestParameters:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only supports unicode!")

    kw = {}

    fmt = "<HHHHI"
    fmt_size = struct.calcsize(fmt)
    (kw['search_attributes'], kw['search_count'],
     kw['flags'], kw['information_level'],
     kw['search_storage_type']) = struct.unpack(fmt, buf[:fmt_size])

    kw['filename'] = buf[fmt_size:].decode("utf-16-le")[:-1]
    return SMBTransaction2FindFirstRequestParameters(**kw)

def decode_transaction_2_find_first_request_data(_: SMBHeader, __: SMBParameters, trans2_params: typing.Any, buf: bytes) -> None:
    assert hasattr(trans2_params, 'information_level')

    if trans2_params.information_level == SMB_INFO_QUERY_EAS_FROM_LIST:
        raise Exception("Not supported")

    if buf:
        raise Exception("buf should be empty")

    return None

SMBTransaction2FindNextRequestParameters = namedtuple(
    'SMBTransaction2FindNextRequestParameters',
    ['sid', 'search_count', 'information_level', 'resume_key',
     'flags', 'filename'])
def decode_transaction_2_find_next_request_params(smb_header: SMBHeader, _: SMBParameters, buf: bytes) -> SMBTransaction2FindNextRequestParameters:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only supports unicode!")

    kw = {}

    fmt = "<HHHIH"
    fmt_size = struct.calcsize(fmt)
    (kw['sid'], kw['search_count'],
     kw['information_level'], kw['resume_key'],
     kw['flags']) = struct.unpack(fmt, buf[:fmt_size])

    kw['filename'] = buf[fmt_size:].decode("utf-16-le")[:-1]
    return SMBTransaction2FindNextRequestParameters(**kw)

decode_transaction_2_find_next_request_data = \
    decode_transaction_2_find_first_request_data

def decode_transaction_2_null_request_data(_: SMBHeader, __: SMBParameters, ___: typing.Any, buf: bytes) -> None:
    if buf:
        raise Exception("buf should be empty")
    return None

SMBTransaction2QueryFSInformationRequestParameters = \
    namedtuple('SMBTransaction2QueryFSInformationRequestParameters',
               ['information_level'])
def decode_transaction_2_query_fs_information_request_params(_: SMBHeader, __: SMBParameters, buf: bytes) -> SMBTransaction2QueryFSInformationRequestParameters:
    return SMBTransaction2QueryFSInformationRequestParameters(*struct.unpack("<H", buf))

SMBTransaction2QueryPathInformationRequestParams = \
    namedtuple('SMBTransaction2QueryPathInformationRequestParams',
               ['information_level', 'filename'])
def decode_transaction_2_query_path_information_request_params(smb_header: SMBHeader, _: SMBParameters, buf: bytes) -> SMBTransaction2QueryPathInformationRequestParams:
    if not (smb_header.flags2 & SMB_FLAGS2_UNICODE):
        raise Exception("Only supports unicode!")

    kw = {}

    fmt = "<HI"
    fmt_size = struct.calcsize(fmt)

    (kw['information_level'], _reserved) = struct.unpack(fmt, buf[:fmt_size])

    kw['filename'] = buf[fmt_size:].decode("utf-16-le")[:-1]

    return SMBTransaction2QueryPathInformationRequestParams(**kw)

decode_transaction_2_query_path_information_request_data = \
    decode_transaction_2_find_first_request_data

SMBTransaction2QueryFileInformationRequestParams = \
    namedtuple('SMBTransaction2QueryFileInformationRequestParams',
               ['fid', 'information_level'])
def decode_transaction_2_query_file_information_request_params(smb_header: SMBHeader, _: SMBParameters, buf: bytes) -> SMBTransaction2QueryFileInformationRequestParams:
    fmt = "<HH"
    return SMBTransaction2QueryFileInformationRequestParams(*struct.unpack(fmt, buf))

decode_transaction_2_query_file_information_request_data = \
    decode_transaction_2_find_first_request_data

def win32_to_datetime(ft : int) -> datetime:
    ts = (ft / 10000000) - 11644473600
    return datetime.fromtimestamp(ts, tz=timezone.utc)

SMBTransaction2SetFileInformationEndOfFileRequestData = \
    namedtuple('SMBTransaction2SetFileInformationEndOfFileRequestData',
               ['end_of_file'])
SMBTransaction2SetFileInformationBasicInfoRequestData = \
    namedtuple('SMBTransaction2SetFileInformationBasicInfoRequestData',
               ['creation_time', 'last_access_time', 'last_write_time',
                'change_time', 'ext_file_attributes'])

# This can be any file information structure
SMBTransaction2SetFileInformationRequestData = object

SMB_INFO_PASSTHROUGH = 0x3e8
FileBasicInformation = 4
FileStandardInformation = 5
FileInternalInformation = 6
FileAllocationInformation = 19
FileNetworkOpenInformation = 34
FileEaInformation = 7
FileDispositionInformation = 13

FILE_ALLOCATION_INFORMATION = \
    namedtuple('FILE_ALLOCATION_INFORMATION',
               ['allocation_size'])

FILE_DISPOSITION_INFORMATION = namedtuple(
    'FILE_DISPOSITION_INFORMATION',
    ['delete_pending']
)

def parse_set_file_data(information_level: int, buf: bytes) -> SMBTransaction2SetFileInformationRequestData:
    if information_level in (SMB_SET_FILE_END_OF_FILE_INFO,
                             SMB_SET_FILE_END_OF_FILE_INFORMATION):
        fmt = "<Q"
        (end_of_file,) = struct.unpack(fmt, buf)
        return SMBTransaction2SetFileInformationEndOfFileRequestData(end_of_file=end_of_file)
    elif information_level in (SMB_SET_FILE_BASIC_INFO,
                               SMB_SET_FILE_BASIC_INFORMATION):
        fmt = "<QQQQLL"
        fmt_size = struct.calcsize(fmt)
        (creation_time, last_access_time,
         last_write_time, change_time,
         ext_file_attributes, _) = struct.unpack(fmt, buf)
        return SMBTransaction2SetFileInformationBasicInfoRequestData(
            creation_time=creation_time,
            last_access_time=last_access_time,
            last_write_time=last_write_time,
            change_time=change_time,
            ext_file_attributes=ext_file_attributes)
    elif information_level == (SMB_INFO_PASSTHROUGH + FileAllocationInformation):
        fmt = "<Q"
        return FILE_ALLOCATION_INFORMATION(*struct.unpack(fmt, buf))
    elif information_level == (SMB_INFO_PASSTHROUGH + FileDispositionInformation):
        fmt = "<B"
        return FILE_DISPOSITION_INFORMATION(*struct.unpack(fmt, buf))
    else:
        raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                            "Set File Data Information level not supported: %r" %
                            (information_level,))

SMBTransaction2SetFileInformationRequestParameters = \
    namedtuple('SMBTransaction2SetFileInformationRequestParameters',
               ['fid', 'information_level', 'reserved'])
def decode_transaction_2_set_file_information_request_params(smb_header: SMBHeader, _: SMBParameters, buf: bytes) -> SMBTransaction2SetFileInformationRequestParameters:
    fmt = "<HHH"
    return SMBTransaction2SetFileInformationRequestParameters(*struct.unpack(fmt, buf))

def decode_transaction_2_set_file_information_request_data(smb_header: SMBHeader, smb_params: SMBParameters,
                                                           trans2_params: typing.Any, buf: bytes) -> SMBTransaction2SetFileInformationRequestData:
    return parse_set_file_data(trans2_params.information_level, buf)

SMB_TRANS2_FIND_FIRST2 = 0x1
SMB_TRANS2_FIND_NEXT2 = 0x2
SMB_TRANS2_QUERY_FS_INFORMATION = 0x3
SMB_TRANS2_QUERY_PATH_INFORMATION = 0x5
SMB_TRANS2_QUERY_FILE_INFORMATION = 0x7
SMB_TRANS2_SET_FILE_INFORMATION = 0x8

SMB_TRANS2_TO_NAME = dict((v, k) for (k, v) in globals().items()
                          if k.startswith('SMB_TRANS2_'))

SMBTransaction2Parameters = object
SMBTransaction2Data = object

_TRANS_2_DECODERS: typing.Dict[int,
                               typing.Tuple[Callable[[SMBHeader, SMBParameters, bytes], SMBTransaction2Parameters],
                                            Callable[[SMBHeader, SMBParameters, SMBTransaction2Parameters, bytes], SMBTransaction2Data]]]
_TRANS_2_DECODERS = {
    SMB_TRANS2_FIND_FIRST2: (decode_transaction_2_find_first_request_params,
                             decode_transaction_2_find_first_request_data),
    SMB_TRANS2_FIND_NEXT2: (decode_transaction_2_find_next_request_params,
                            decode_transaction_2_find_next_request_data),
    SMB_TRANS2_QUERY_FS_INFORMATION: (decode_transaction_2_query_fs_information_request_params,
                                      decode_transaction_2_null_request_data),
    SMB_TRANS2_QUERY_PATH_INFORMATION: (decode_transaction_2_query_path_information_request_params,
                                        decode_transaction_2_query_path_information_request_data),
    SMB_TRANS2_QUERY_FILE_INFORMATION: (decode_transaction_2_query_file_information_request_params,
                                        decode_transaction_2_query_file_information_request_data),
    SMB_TRANS2_SET_FILE_INFORMATION: (decode_transaction_2_set_file_information_request_params,
                                      decode_transaction_2_set_file_information_request_data),
}
def get_transaction2_request_decoder(smb_parameters: SMBParameters) -> typing.Tuple[Callable[[SMBHeader, SMBParameters, bytes], SMBTransaction2Parameters],
                                                                                    Callable[[SMBHeader, SMBParameters, SMBTransaction2Parameters, bytes], SMBTransaction2Data]]:
    assert isinstance(smb_parameters, SMBTransaction2RequestParameters)
    try:
        return _TRANS_2_DECODERS[smb_parameters.setup[0]]
    except KeyError:
        raise ProtocolError(STATUS_NOT_SUPPORTED,
                            "Trans 2 request not supported: %r" % (smb_parameters.setup,))

def decode_transaction_2_request_message(msg: SMBMessage) -> typing.Tuple[int, SMBTransaction2Parameters, SMBTransaction2Data]:
    assert (msg.parameters.total_parameter_count == msg.parameters.parameter_count and
            msg.parameters.total_data_count == msg.parameters.data_count), \
            "only supports single smb-message transaction 2 requests"

    (params_decoder, data_decoder) = get_transaction2_request_decoder(msg.parameters)

    params = params_decoder(msg.header, msg.parameters, msg.data.parameters)
    data = data_decoder(msg.header, msg.parameters, params, msg.data.data)

    return (msg.parameters.setup[0], params, data)

SMBNTTransactSetup = object
SMBNTTransactParameters = object
SMBNTTransactData = object

SMBNTTransactNotifyChangeRequestSetup = namedtuple(
    'SMBNTTransactNotifyChangeRequestSetup',
    ['completion_filter', 'fid', 'watch_tree'])
def decode_nt_transact_notify_change_request_setup(_: SMBHeader, parameters: SMBParameters) -> SMBNTTransactNotifyChangeRequestSetup:
    assert isinstance(parameters, SMBNTTransactRequestParameters)
    return SMBNTTransactNotifyChangeRequestSetup(
        *struct.unpack("<LH?", parameters.setup[:7]))

def decode_nt_transact_null_request_params(_: SMBHeader, __: SMBParameters, ___: SMBNTTransactSetup, buf: bytes) -> None:
    if buf:
        raise Exception("there should be no buf!")
    return None

def decode_nt_transact_null_request_data(_: SMBHeader, __: SMBParameters, ___: SMBNTTransactSetup, ____: SMBNTTransactParameters, buf: bytes) -> None:
    if buf:
        raise Exception("there should be no buf!")
    return None

SMBNTTransactIoctlRequestSetup = namedtuple(
    'SMBNTTransactIoctlRequestSetup',
    ['function_code', 'fid', 'is_fsctl', 'is_flags'])
def decode_nt_transact_ioctl_request_setup(_: SMBHeader, parameters: SMBParameters) -> SMBNTTransactIoctlRequestSetup:
    assert isinstance(parameters, SMBNTTransactRequestParameters)
    fmt = "<LH??"
    return SMBNTTransactIoctlRequestSetup(*struct.unpack(fmt, parameters.setup))

def decode_nt_transact_byte_request_data(_: SMBHeader, __: SMBParameters, ___: SMBNTTransactSetup, ____: SMBNTTransactParameters, buf: bytes) -> bytes:
    return buf

RequestDecoderMapEntry = typing.Tuple[
    Callable[[SMBHeader, SMBParameters], SMBNTTransactSetup],
    Callable[[SMBHeader, SMBParameters, SMBNTTransactSetup, bytes], SMBNTTransactParameters],
    Callable[[SMBHeader, SMBParameters, SMBNTTransactSetup, SMBNTTransactParameters, bytes], SMBNTTransactData]
]

def get_nt_transact_request_decoder(smb_parameters: SMBParameters) -> RequestDecoderMapEntry:
    assert isinstance(smb_parameters, SMBNTTransactRequestParameters)
    try:
        return {
            NT_TRANSACT_NOTIFY_CHANGE: (decode_nt_transact_notify_change_request_setup,
                                        decode_nt_transact_null_request_params,
                                        decode_nt_transact_null_request_data),
            NT_TRANSACT_IOCTL: (decode_nt_transact_ioctl_request_setup,
                                decode_nt_transact_null_request_params,
                                decode_nt_transact_byte_request_data),
        }[smb_parameters.function]
    except KeyError:
        raise ProtocolError(STATUS_NOT_SUPPORTED,
                            "NT Transact function not supported: %r" %
                            (smb_parameters.function,))

def decode_nt_transact_request_message(msg: SMBMessage) -> typing.Tuple[int,
                                                                        SMBNTTransactSetup,
                                                                        SMBNTTransactParameters,
                                                                        SMBNTTransactData]:
    assert (msg.parameters.total_parameter_count == msg.parameters.parameter_count and
            msg.parameters.total_data_count == msg.parameters.data_count), \
            "only supports single smb-message nt transact requests"

    (setup_decoder, params_decoder, data_decoder) = \
        get_nt_transact_request_decoder(msg.parameters)

    setup = setup_decoder(msg.header, msg.parameters)
    params = params_decoder(msg.header, msg.parameters, setup, msg.data.parameters)
    data = data_decoder(msg.header, msg.parameters, setup, params, msg.data.data)

    return (msg.parameters.function, setup, params, data)

def header_from_header(header: SMBHeader, **kw: typing.Any) -> SMBHeader:
    for x in SMBHeader._fields:
        if x not in kw:
            kw[x] = getattr(header, x)
    return SMBHeader(**kw)

def reply_header_from_request_header(header: SMBHeader, **kw: typing.Any) -> SMBHeader:
    kw.setdefault('flags', header.flags | SMB_FLAGS_REPLY)
    kw.setdefault('flags2', header.flags2 & ~SMB_FLAGS2_EXTENDED_SECURITY)
    kw.setdefault('status', STATUS_SUCCESS)
    return header_from_header(header, **kw)

def reply_header_from_request(msg: SMBMessage, **kw: typing.Any) -> SMBHeader:
    return reply_header_from_request_header(msg.header, **kw)

STATUS_SUCCESS = 0x0
STATUS_NOT_FOUND = 0xc0000225
STATUS_SMB_BAD_COMMAND = 0x160002
STATUS_NOT_SUPPORTED = 0xc00000bb
STATUS_NO_SUCH_FILE = 0xc000000f
STATUS_TOO_MANY_OPENED_FILES = 0xc000011f
STATUS_FILE_IS_A_DIRECTORY = 0xc00000ba
STATUS_SHARING_VIOLATION = 0xc0000043
STATUS_INVALID_HANDLE = 0xc0000008
STATUS_ACCESS_DENIED = 0xc0000022
STATUS_INSUFF_SERVER_RESOURCES = 0xc00000cf
STATUS_OBJECT_PATH_NOT_FOUND = 0xc000003a
STATUS_SMB_BAD_TID = 0x50002
STATUS_SMB_BAD_UID = 0x5b0002
STATUS_NOTIFY_ENUM_DIR = 0x10c
STATUS_OS2_INVALID_LEVEL = 0x7c0001
STATUS_NOT_A_DIRECTORY = 0xC0000000 | 0x0103
STATUS_UNSUCCESSFUL = 0xc0000001
STATUS_OBJECT_NAME_COLLISION = 0xc0000035
STATUS_OBJECT_PATH_SYNTAX_BAD = 0xc000003B
STATUS_OBJECT_PATH_INVALID = 0xc0000039
STATUS_DIRECTORY_NOT_EMPTY = 0xC0000101

TREE_CONNECT_ANDX_DISCONNECT_TID = 0x1
SMB_INFO_STANDARD = 0x1
SMB_INFO_QUERY_EAS_FROM_LIST = 0x3
SMB_FIND_FILE_DIRECTORY_INFO = 0x101
SMB_FIND_FILE_BOTH_DIRECTORY_INFO = 0x104
SMB_FIND_RETURN_RESUME_KEYS = 0x4
SMB_FIND_CLOSE_AT_EOS = 0x2
SMB_FIND_CLOSE_AFTER_REQUEST = 0x1
ATTR_DIRECTORY = 0x10
ATTR_NORMAL = 0x80
SMB_QUERY_FS_VOLUME_INFO = 0x102
SMB_QUERY_FS_SIZE_INFO = 0x103
SMB_QUERY_FS_DEVICE_INFO = 0x104
SMB_QUERY_FS_ATTRIBUTE_INFO = 0x105
SMB_QUERY_FILE_BASIC_INFO = 0x101
SMB_QUERY_FILE_ALL_INFO = 0x107
NT_TRANSACT_IOCTL = 0x2
NT_TRANSACT_NOTIFY_CHANGE = 0x4

NT_CREATE_REQUEST_OPLOCK = 0x2
NT_CREATE_REQUEST_OPBATCH = 0x4
NT_CREATE_OPEN_TARGET_DIR = 0x8

FILE_WRITE_DATA = 0x2
FILE_APPEND_DATA = 0x4
FILE_WRITE_EA = 0x10
FILE_WRITE_ATTRIBUTES = 0x100
DELETE = 0x10000
WRITE_DAC = 0x40000
WRITE_OWNER = 0x80000
ACCESS_SYSTEM_SECURITY = 0x1000000
GENERIC_ALL = 0x1000000
GENERIC_EXECUTE = 0x20000000
GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000
FILE_READ_DATA = 0x1
MAXIMUM_ALLOWED = 0x02000000

FILE_SUPERSEDE = 0x0
FILE_OPEN = 0x1
FILE_CREATE = 0x2
FILE_OPEN_IF = 0x3
FILE_OVERWRITE = 0x4
FILE_OVERWRITE_IF = 0x5

FILE_DELETE_ON_CLOSE = 0x1000
FILE_OPEN_BY_FILE_ID = 0x2000

FILE_DIRECTORY_FILE = 0x1
FILE_NON_DIRECTORY_FILE = 0x40

FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
FILE_SHARE_DELETE = 0x4

FILE_ACTION_ADDED = 0x1
FILE_ACTION_REMOVED = 0x2
FILE_ACTION_MODIFIED = 0x3
FILE_ACTION_RENAMED_OLD_NAME = 0x4
FILE_ACTION_RENAMED_NEW_NAME = 0x5

FSCTL_CREATE_OR_GET_OBJECT_ID = 0x900c0

DEFAULT_ANDX_PARAMETERS = dict(andx_reserved=0,
                               andx_offset=0)

SMB_SET_FILE_END_OF_FILE_INFO = 0x104
SMB_SET_FILE_BASIC_INFO = 0x101
SMB_SET_FILE_END_OF_FILE_INFORMATION = 1020
SMB_SET_FILE_BASIC_INFORMATION = 1004

def encode_smb_datetime(dt: datetime) -> typing.Tuple[int, int]:
    log.debug("date is %r", dt)
    date = 0
    date |= (dt.year - 1980) << 9
    date |= (dt.month & 0xf) << 5
    date |= dt.day & 0x1f
    assert date < 2 ** 16
    time = 0
    time |= dt.hour << 11
    time |= dt.minute << 5
    time |= int(dt.second / 2)
    assert time < 2 ** 16
    return (date, time)

def error_response(header: SMBHeader, status: int = STATUS_UNSUCCESSFUL) -> SMBMessage:
    assert status, "Status must be an error!"
    return SMBMessage(
        reply_header_from_request_header(
            header,
            status=status,
            flags2=header.flags2 | SMB_FLAGS2_NT_STATUS),
        None, None)

def datetime_to_win32(dt: datetime) -> int:
    # Assumes dt is a non-naive datetime
    assert dt.tzinfo is not None
    return (int(dt.timestamp()) + 11644473600) * 10000000

class NormalStat:
    def __init__(self, birthtime: datetime, mtime: datetime,
                 ctime: datetime, atime: datetime,
                 type: str, size: int) -> None:
        self.birthtime = birthtime
        self._mtime = mtime
        self.ctime = ctime
        self.atime = atime
        self._type = type
        self._size = size

    @property
    def mtime(self) -> datetime:
        return self._mtime

    @property
    def type(self) -> str:
        return self._type

    @property
    def size(self) -> int:
        return self._size

def get_size(md: NormalStat) -> int:
    return md.size

InfoGeneratorType = Callable[[int, int, int, str, NormalStat, int], Sequence[bytes]]

def generate_info_standard(idx: int, offset: int, flags: int, name: str, md: NormalStat, _: int) -> typing.List[bytes]:
    include_resume_key = flags & SMB_FIND_RETURN_RESUME_KEYS

    # SMB_INFO_STANDARD
    fmt = "<"
    args = []
    if include_resume_key:
        fmt += "I"
        args.append(idx)
    fmt += "HHHHHHIIHB"
    name += '\0'
    file_name_encoded = name.encode("utf-16-le")

    (creation_date, creation_time) = encode_smb_datetime(md.birthtime)
    (last_access_date, last_access_time) = encode_smb_datetime(md.atime)
    (last_write_date, last_write_time) = encode_smb_datetime(md.mtime)

    file_data_size = get_size(md)
    allocation_size = 4096
    attributes = (ATTR_DIRECTORY
                  if md.type == "directory" else
                  ATTR_NORMAL)

    args.extend([creation_date, creation_time,
                 last_access_date, last_access_time,
                 last_write_date, last_write_time,
                 file_data_size, allocation_size,
                 attributes, len(file_name_encoded)])

    bufs = []
    bufs.append(struct.pack(fmt, *args))
    offset += len(bufs[-1])
    if offset % 2:
        bufs.append(b' ')
        offset += 1
    bufs.append(file_name_encoded)
    offset += len(bufs[-1])

    return bufs

def generate_find_file_directory_info(idx: int, offset: int, flags: int, name: str, md: NormalStat, is_last: int) -> typing.List[bytes]:
    fmt = "<IIQQQQQQII"

    encoded_file_name = (name + "\0").encode("utf-16-le")
    fmt_size = struct.calcsize(fmt)

    next_entry_offset = (0
                         if is_last else
                         fmt_size + len(encoded_file_name))

    file_data_size = get_size(md)

    allocation_size = 4096
    ext_file_attributes = (ATTR_DIRECTORY
                           if md.type == "directory" else
                           ATTR_NORMAL)

    buf = struct.pack(fmt, next_entry_offset,
                      # FileIndex is set to zero because there is not guarantee
                      # on directory sort order
                      0,
                      datetime_to_win32(md.birthtime),
                      datetime_to_win32(md.atime),
                      datetime_to_win32(md.mtime),
                      datetime_to_win32(md.ctime),
                      file_data_size,
                      allocation_size,
                      ext_file_attributes,
                      len(encoded_file_name))

    return [buf, encoded_file_name]

def generate_find_file_both_directory_info(idx: int, offset: int, flags: int, name: str, md: NormalStat, is_last: int) -> typing.List[bytes]:
    fmt = "<IIQQQQQQIIIBB"

    encoded_file_name = (name + "\0").encode("utf-16-le")
    fmt_size = struct.calcsize(fmt)
    SHORT_NAME_SIZE = 24

    next_entry_offset = (0
                         if is_last else
                         fmt_size + SHORT_NAME_SIZE + len(encoded_file_name))

    file_data_size = get_size(md)

    allocation_size = 4096
    ext_file_attributes = (ATTR_DIRECTORY
                           if md.type == "directory" else
                           ATTR_NORMAL)
    ea_size = 0

    buf = struct.pack(fmt, next_entry_offset, 0,
                      datetime_to_win32(md.birthtime),
                      datetime_to_win32(md.atime),
                      datetime_to_win32(md.mtime),
                      datetime_to_win32(md.ctime),
                      file_data_size,
                      allocation_size,
                      ext_file_attributes,
                      len(encoded_file_name),
                      ea_size,
                      0, 0)

    bufs = []
    bufs.append(buf)
    bufs.append(b'\0' * 24)
    bufs.append(encoded_file_name)

    return bufs

INFO_GENERATORS = {
    SMB_INFO_STANDARD: generate_info_standard,
    SMB_FIND_FILE_DIRECTORY_INFO: generate_find_file_directory_info,
    SMB_FIND_FILE_BOTH_DIRECTORY_INFO: generate_find_file_both_directory_info,
}

async def generate_fs_size_info(fs: AsyncFS) -> bytes:
    st = await fs.statvfs()
    return struct.pack("<QQII",
                       min(2 ** 64 - 1, st.f_blocks), # total allocation units
                       min(2 ** 64 - 1, st.f_bavail), # total free allocation units
                       min(2 ** 32 - 1, st.f_frsize // 512), # sectors per allocation unit
                       512, # bytes per sector
                       )

FILE_DEVICE_DISK = 0x7

async def generate_fs_device_info(fs: AsyncFS) -> bytes:
    # TODO: there are a whole bunch of options we can use for the
    #       "characteristics" field
    return struct.pack("<II",
                         FILE_DEVICE_DISK,
                         0)

FILE_CASE_SENSITIVE_SEARCH = 0x1
FILE_CASE_PRESERVED_NAMES = 0x2
FILE_UNICODE_ON_DISK = 0x4

async def generate_fs_attribute_info(fs: AsyncFS) -> bytes:
    file_system_attributes = FILE_UNICODE_ON_DISK | FILE_CASE_PRESERVED_NAMES
    max_file_name_length_in_bytes = 255 * 2
    file_system_name = "NTFS"
    file_system_name_encoded = file_system_name.encode("utf-16-le")
    header = struct.pack("<LlL",
                         file_system_attributes,
                         max_file_name_length_in_bytes,
                         len(file_system_name_encoded))
    return header + file_system_name_encoded

async def generate_fs_volume_info(fs: AsyncFS) -> bytes:
    volume_creation_time = 0
    serial_number = 0
    volume_label_size = 2
    reserved = 0
    return struct.pack("<QLLH",
                       volume_creation_time,
                       serial_number,
                       volume_label_size,
                       reserved) + b"\0\0"

async def generate_fs_object_id_info(fs: AsyncFS) -> bytes:
    # volume ID is 0
    return struct.pack("<QQQQQQQQ", 0, 0,
                       0, 0, 0, 0, 0, 0)

FileFsObjectIdInformation = 8

FS_INFO_GENERATORS = {
    SMB_QUERY_FS_SIZE_INFO: generate_fs_size_info,
    SMB_QUERY_FS_DEVICE_INFO: generate_fs_device_info,
    SMB_QUERY_FS_ATTRIBUTE_INFO: generate_fs_attribute_info,
    SMB_QUERY_FS_VOLUME_INFO: generate_fs_volume_info,
    SMB_INFO_PASSTHROUGH + FileFsObjectIdInformation: generate_fs_object_id_info,
}

QueryResult = typing.Tuple[int, bytes]

def generate_query_file_basic_info(path: str, md: NormalStat) -> QueryResult:
    creation_time = datetime_to_win32(md.birthtime)
    last_access_time = datetime_to_win32(md.atime)
    last_write_time = datetime_to_win32(md.mtime)
    last_change_time = datetime_to_win32(md.ctime)
    ext_file_attributes = (ATTR_DIRECTORY
                           if md.type == "directory" else
                           ATTR_NORMAL)
    buf = struct.pack("<QQQQLL",
                      creation_time, last_access_time,
                      last_write_time, last_change_time,
                      ext_file_attributes,
                      0)

    return (0, buf)

def generate_query_file_all_info(path: str, md: NormalStat) -> QueryResult:
    creation_time = datetime_to_win32(md.birthtime)
    last_access_time = datetime_to_win32(md.atime)
    last_write_time = datetime_to_win32(md.mtime)
    last_change_time = datetime_to_win32(md.ctime)
    ext_file_attributes = (ATTR_DIRECTORY
                           if md.type == "directory" else
                           ATTR_NORMAL)
    allocation_size = 4096
    file_data_size = get_size(md)

    reserved = 0

    number_of_links = 1
    delete_pending = 0
    directory = int(md.type == "directory")

    ea_size = 0

    encoded_file_name = (path + "\0").encode("utf-16-le")

    buf = struct.pack("<QQQQLLQQLBBHLL",
                      creation_time, last_access_time,
                      last_write_time, last_change_time,
                      ext_file_attributes,
                      reserved, allocation_size,
                      file_data_size,
                      number_of_links,
                      delete_pending,
                      directory,
                      reserved,
                      ea_size,
                      len(encoded_file_name))
    buf += encoded_file_name

    return (0, buf)

def generate_query_file_standard_info(path: str, md: NormalStat) -> QueryResult:
    allocation_size = 4096
    file_data_size = get_size(md)

    number_of_links = 1
    delete_pending = 0
    directory = int(md.type == "directory")

    buf = struct.pack("<qqIBBH",
                      allocation_size,
                      file_data_size,
                      number_of_links,
                      delete_pending,
                      directory,
                      0)

    return (0, buf)

def generate_query_file_internal_info(path: str, md: NormalStat) -> QueryResult:
    # set to 0 if we don't support it
    index_number = 0
    buf = struct.pack("<q", index_number)
    return (0, buf)

def generate_query_file_allocation_info(path: str, md: NormalStat) -> QueryResult:
    allocation_size = 4096
    buf = struct.pack("<q", allocation_size)
    return (0, buf)

def generate_query_file_network_open_info(path: str, md: NormalStat) -> QueryResult:
    creation_time = datetime_to_win32(md.birthtime)
    last_access_time = datetime_to_win32(md.atime)
    last_write_time = datetime_to_win32(md.mtime)
    last_change_time = datetime_to_win32(md.ctime)
    ext_file_attributes = (ATTR_DIRECTORY
                           if md.type == "directory" else
                           ATTR_NORMAL)
    allocation_size = 4096
    file_data_size = get_size(md)

    buf = struct.pack("<QQQQqqII",
                      creation_time, last_access_time,
                      last_write_time, last_change_time,
                      allocation_size,
                      file_data_size,
                      ext_file_attributes,
                      0)

    return (0, buf)

def generate_query_file_ea_info(path: str, md: NormalStat) -> QueryResult:
    # no ea information
    buf = struct.pack("<I", 0)
    return (0, buf)

QUERY_FILE_INFO_GENERATORS = {
    SMB_QUERY_FILE_BASIC_INFO: generate_query_file_basic_info,
    SMB_QUERY_FILE_ALL_INFO: generate_query_file_all_info,
    SMB_INFO_PASSTHROUGH + FileBasicInformation: generate_query_file_basic_info,
    SMB_INFO_PASSTHROUGH + FileStandardInformation: generate_query_file_standard_info,
    SMB_INFO_PASSTHROUGH + FileInternalInformation: generate_query_file_internal_info,
    SMB_INFO_PASSTHROUGH + FileAllocationInformation: generate_query_file_allocation_info,
    SMB_INFO_PASSTHROUGH + FileNetworkOpenInformation: generate_query_file_network_open_info,
    SMB_INFO_PASSTHROUGH + FileEaInformation: generate_query_file_ea_info,
}

class ProtocolError(Exception):
    def __init__(self, error: int, message: typing.Optional[str] = None):
        self.error = error
        self.message = message
        self.args = (error, message)

    def __repr__(self) -> str:
        return 'ProtocolError(0x%x, %r)' % (self.error, self.message)

async def cant_fail(on_fail: Callable[[], None], future: asyncio.Future[T]) -> None:
    try:
        await future
    except Exception:
        log.exception("Process-stopping exception!")
        on_fail()

INVALID_UIDS = (0x0, 0xfffe)
INVALID_TIDS = (0x0, 0xffff)
INVALID_SIDS = (0xffff,)
INVALID_FIDS = (0xffff,)

class StatIDMapper(object):
    def __init__(self) -> None:
        self._db_lock = SharedLock()
        self._pool = ConnPool(self._create_db_conn)

    def _create_db_conn(self) -> sqlite3.Connection:
        db_path = "file:dbxfs.FileSystem-%d?mode=memory&cached=shared" % (id(self),)
        conn = sqlite3.connect(db_path, uri=True, check_same_thread=False)

        conn.execute("""\
create table if not exists id_id_map
(int_id integer primary key,
 db_id text unique)
""")

        return conn

    def map_id(self, id_: str) -> int:
        mutate = False
        while True:
            with self._pool.get_conn() as conn, \
                 trans(conn, self._db_lock, is_exclusive=mutate), \
                 contextlib.closing(conn.cursor()) as cursor:
                cursor.execute("select int_id from id_id_map where db_id = ?", (id_,))
                row = cursor.fetchone()
                if row is not None:
                    assert isinstance(row[0], int)
                    return row[0]
                if not mutate:
                    mutate = True
                    continue
                while True:
                    # NB: 2 ** 63 - 1 is the highest integer value sqlite3 can store natively
                    pid = random.randint(0, 2 ** 63 - 1)
                    cursor.execute("select count(*) from id_id_map where int_id = ?", (pid,))
                    (amt,) = cursor.fetchone()
                    if not amt:
                        break
                cursor.execute("insert into id_id_map (int_id, db_id) values (?, ?)",
                               (pid, id_))
                return pid

    def _ext_id_to_db_id(self, ext_id: int) -> str:
        with self._pool.get_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=False), \
             contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("select db_id from id_id_map where int_id = ?", (ext_id,))
            row = cursor.fetchone()
            if row is None:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))
            assert isinstance(row[0], str)
            return row[0]

    def close(self) -> None:
        self._pool.close()

class AsyncStatIDMapper(object):
    def __init__(self, obj: StatIDMapper, worker_pool: AsyncWorkerPool):
        self._obj = obj
        self._worker_pool = worker_pool

    async def map_id(self, id_: str) -> int:
        return (await self._worker_pool.run_async(self._obj.map_id, id_))

    async def close(self) -> None:
        return (await self._worker_pool.run_async(self._obj.close))

OpenFile = TypedDict(
    'OpenFile',
    {
        'path': str,
        'ref': int,
        'handle': AsyncFile,
        'closing': typing.Optional[asyncio.Future[None]],
        'is_closing': asyncio.Future[typing.Literal[True]],
        'tid': int,
    }
)

OpenSearch = TypedDict(
    'OpenSearch',
    {
        'handle': typing.Optional[AsyncOldDirectory],
        'entry': typing.Optional[typing.Tuple[str, NormalStat]],
        'next_entry': typing.Optional[typing.Tuple[str, NormalStat]],
        'buffered_entries': typing.List[typing.Tuple[str, NormalStat]],
        'buffered_entries_idx': int,
        'idx': typing.Any,
        'tid': int,
        'lock': asyncio.Lock,
        'closing': bool,
    }
)

OpenTid = TypedDict(
    'OpenTid',
    {
        'closing': typing.Optional[asyncio.Future[None]],
        'ref': int,
        'fs': AsyncFS,
        'idm': AsyncStatIDMapper,
    },
)

class SMBClientHandler(object):
    def __init__(self, worker_pool: AsyncWorkerPool) -> None:
        self._open_uids: typing.Set[int] = set()
        self._open_tids: typing.Dict[int, OpenTid] = {}
        self._open_find_trans: typing.Dict[int, OpenSearch] = {}
        self._open_files: typing.Dict[int, OpenFile] = {}
        self._worker_pool = worker_pool

    async def get_trans2_fn(self, trans2_params: typing.Any) -> str:
        fn: str
        try:
            fn = '%r' % (trans2_params.filename,)
        except AttributeError:
            try:
                fn = await self.fid_to_file_name(trans2_params.fid)
                fn = '%r (0x%x)' % (fn, trans2_params.fid)
            except AttributeError:
                fn = ''
            except KeyError:
                fn = '<invalid-fid: 0x%x>' % (trans2_params.fid,)
        return fn

    async def get_msg_fn(self, msg: SMBMessage) -> str:
        fn = ''
        for (parameters, data) in msg.commands:
            try:
                fn = '%r' % (data.filename,)  # type: ignore
            except AttributeError:
                try:
                    fid = parameters.fid  # type: ignore
                    fn = await self.fid_to_file_name(fid)
                    fn = '%r (0x%x)' % (fn, fid)
                    break
                except AttributeError:
                    pass
                except KeyError:
                    fn = '<invalid-fid: 0x%x>' % (fid,)
                    break
        return fn

    async def verify_tid_mapper(self, req: SMBMessage) -> typing.Tuple[AsyncFS, AsyncStatIDMapper]:
        try:
            toret = self._open_tids[req.header.tid]
            if toret['closing']: raise KeyError()
            toret['ref'] += 1
            assert isinstance(toret['fs'], AsyncFS)
            assert isinstance(toret['idm'], AsyncStatIDMapper)
            return (toret['fs'], toret['idm'])
        except KeyError:
            raise ProtocolError(STATUS_SMB_BAD_TID)

    async def verify_tid(self, req: SMBMessage) -> AsyncFS:
        return (await self.verify_tid_mapper(req))[0]

    async def deref_tid(self, tid: int) -> None:
        toret = self._open_tids[tid]
        toret['ref'] -= 1
        if (toret['closing'] is not None and
            not toret['ref']):
            toret['closing'].set_result(None)

    async def verify_uid(self, req: SMBMessage) -> None:
        if req.header.uid not in self._open_uids:
            raise ProtocolError(STATUS_SMB_BAD_UID)

    def _create_id(self, set_: Collection[int], invalid: Collection[int], error: int = STATUS_INSUFF_SERVER_RESOURCES) -> int:
        assert len(set_) <= 2 ** 16 - len(invalid)
        if len(set_) == 2 ** 16 - len(invalid):
            raise ProtocolError(error)

        uid = random.randint(0, 2 ** 16)
        while uid in set_ or uid in invalid:
            uid = random.randint(0, 2 ** 16)

        return uid

    async def create_session(self) -> int:
        uid = self._create_id(self._open_uids, INVALID_UIDS)
        self._open_uids.add(uid)
        return uid

    async def destroy_session(self, uid: int) -> None:
        self._open_uids.remove(uid)

    async def create_tree(self, fs: AsyncFS) -> int:
        tid = self._create_id(self._open_tids, INVALID_TIDS)
        self._open_tids[tid] = dict(closing=None,
                                    ref=0,
                                    fs=fs,
                                    idm=AsyncStatIDMapper(StatIDMapper(), self._worker_pool))
        return tid

    async def destroy_tree(self, tid: int) -> AsyncFS:
        ret = self._open_tids[tid]

        if ret['closing']: raise KeyError()

        # mark tid as closing
        all_closed: asyncio.Future[None]
        all_closed = asyncio.Future()
        ret['closing'] = all_closed

        # close all resources associated with tid (in parallel)
        waiting: typing.List[asyncio.Future[None]]
        waiting = []

        async def destroy_close_file(fid: int) -> None:
            try:
                fidmd = await self.destroy_file(fid)
            except KeyError:
                return
            await fidmd['handle'].close()

        for fid, value in self._open_files.items():
            if value['tid'] != tid: continue
            waiting.append(asyncio.ensure_future(destroy_close_file(fid)))

        async def destroy_close_search(sid: int) -> None:
            try:
                searchmd = await self.destroy_search(sid)
            except KeyError:
                return
            if searchmd['handle'] is not None:
                await searchmd['handle'].close()

        for sid, tvalue in self._open_find_trans.items():
            if tvalue['tid'] != tid: continue
            waiting.append(asyncio.ensure_future(destroy_close_search(sid)))

        if ret['ref']:
            # wait for all tids to be dereffed
            waiting.append(all_closed)

        if waiting:
            await asyncio.wait(waiting)

        assert not ret['ref']

        await ret['idm'].close()

        popped = self._open_tids.pop(tid)
        assert popped is ret
        assert isinstance(ret['fs'], AsyncFS)
        return ret['fs']

    async def hard_destroy_all_trees(self, backend: AsyncBackend) -> None:
        async def destroy_tid(tid: int) -> None:
            try:
                fs = await self.destroy_tree(tid)
            except KeyError:
                return
            await backend.tree_disconnect_hard(fs)

        waiting = []
        for tid in self._open_tids:
            waiting.append(asyncio.ensure_future(destroy_tid(tid)))

        if waiting:
            await asyncio.wait(waiting)

    async def create_search(self, os: OpenSearch) -> int:
        sid = self._create_id(self._open_find_trans, INVALID_SIDS)
        self._open_find_trans[sid] = os
        return sid

    async def ref_search(self, sid: int) -> OpenSearch:
        toret = self._open_find_trans[sid]
        if toret['closing']: raise KeyError()
        await toret['lock'].acquire()
        return toret

    async def deref_search(self, sid: int) -> None:
        toret = self._open_find_trans[sid]
        toret['lock'].release()

    async def destroy_search(self, sid: int) -> OpenSearch:
        # flag file as closing
        ret = self._open_find_trans[sid]
        if ret['closing']: raise KeyError()

        ret['closing'] = True

        await ret['lock'].acquire()
        try:
            popped = self._open_find_trans.pop(sid)
            assert popped is ret
            return ret
        finally:
            ret['lock'].release()

    async def ref_file(self, fid: int) -> OpenFile:
        # KeyError is okay for now
        toret = self._open_files[fid]
        if toret['closing'] is not None: raise KeyError()
        toret['ref'] += 1
        return toret

    async def deref_file(self, fid: int) -> None:
        toret = self._open_files[fid]
        toret['ref'] -= 1
        if (toret['closing'] is not None and
            not toret['ref']):
            toret['closing'].set_result(None)

    async def create_file(self, path: str, handle: AsyncFile, tid: int) -> int:
        fid = self._create_id(self._open_files, INVALID_FIDS)
        self._open_files[fid] = dict(path=path,
                                     ref=0,
                                     handle=handle,
                                     closing=None,
                                     is_closing=asyncio.Future(),
                                     tid=tid)
        return fid

    async def destroy_file(self, fid: int) -> OpenFile:
        # flag file as closing
        ret = self._open_files[fid]
        if ret['closing'] is not None: raise KeyError()
        all_closed: asyncio.Future[None]
        all_closed = asyncio.Future()
        ret['closing'] = all_closed
        if not ret['ref']:
            all_closed.set_result(None)

        # flag to all blockers that this file is closing
        ret['is_closing'].set_result(True)

        # wait for all files to be dereffed
        await all_closed
        assert not ret['ref']
        popped = self._open_files.pop(fid)
        assert popped is ret
        return ret

    async def watch_file(self, fid: int, fs: AsyncFS, *n: typing.Any, **kw: typing.Any) -> fsabc.ChangeList:
        ret = self._open_files[fid]
        if ret['closing'] is not None: raise KeyError()

        changes_event = asyncio.Event()
        changes: typing.List[fsabc.Change] | str = []
        def handle_changes(changes_: fsabc.ChangeList) -> None:
            nonlocal changes
            if isinstance(changes_, str):
                assert changes_ == "reset"
                changes = "reset"
            else:
                if not isinstance(changes, str):
                    changes.extend(changes_)
                else:
                    assert changes == "reset"
            changes_event.set()

        try:
            stop_new_watch = fs.x_create_watch(handle_changes, ret['handle'],
                                               *n, **kw)
        except NotImplementedError:
            raise ProtocolError(STATUS_NOT_SUPPORTED)

        ret['ref'] += 1

        wait_for_changes = asyncio.ensure_future(changes_event.wait())

        (done, pending) = await asyncio.wait([wait_for_changes,
                                                   ret['is_closing']],
                                                  return_when=asyncio.FIRST_COMPLETED,
        )

        assert (fid in self._open_files and
                self._open_files[fid] is ret)

        wait_for_changes.cancel()

        ret['ref'] -= 1
        if (ret['closing'] is not None and
            not ret['ref']):
            ret['closing'].set_result(None)

        stop_new_watch()

        return changes

    async def fid_to_file_name(self, fid: int) -> str:
        ret = self._open_files[fid]['path']
        assert isinstance(ret, str)
        return ret

    @classmethod
    async def read_message(cls, reader: asyncio.StreamReader) -> typing.Optional[bytes]:
        data = await reader.read(4)
        # Signal EOF
        if not data: return None
        (length,) = struct.unpack(">I", data)
        out = []
        while length:
            data = (await reader.read(length))
            if not data:
                raise Exception("Unexpected EOF")
            out.append(data)
            length -= len(data)
        return b''.join(out)

    @classmethod
    async def send_message(cls, writer: asyncio.StreamWriter, raw_data: bytes) -> None:
        writer.writelines([struct.pack(">I", len(raw_data)),
                           raw_data])

    async def run(self, backend: AsyncBackend,
                  master_kill: asyncio.Future[None],
                  reader: asyncio.StreamReader,
                  writer: asyncio.StreamWriter) -> None:
        # first negotiate SMB protocol
        negotiate_req_raw = await self.read_message(reader)
        if negotiate_req_raw is None:
            raise Exception("Received client EOF!")

        negotiate_req = decode_smb_message(negotiate_req_raw)

        if negotiate_req.header.command != SMB_COM_NEGOTIATE:
            raise Exception("Got unexpected request: %s" % (negotiate_req,))

        server_capabilities = (CAP_UNICODE |
                               CAP_LARGE_FILES |
                               CAP_STATUS32 |
                               CAP_NT_SMBS |
                               CAP_NT_FIND)

        # NB: we don't fully support passthrough but we need to say
        #     we do to get the smbfs on darwin to rename open files
        #     (instead of failing fast with EBUSY)
        #     (don't ask how long it took to figure that out)
        server_capabilities = (server_capabilities |
                               CAP_INFOLEVEL_PASSTHRU)

        # win32 time
        now = datetime_now()
        win32_time = datetime_to_win32(now)
        negotiate_reply_params = SMBNegotiateReplyParameters(
            # TODO: catch this and throw a friendlier error
            dialect_index=negotiate_req.data.dialects.index('NT LM 0.12'),
            security_mode=0, # we support NO SECURITY FEATURES
            max_mpx_count=2 ** 16 - 1, # unlimited clients baby
            max_number_vcs=2 ** 16 - 1, # not sure what this means
            max_buffer_size=2 ** 16 - 1, # this doesn't matter
            max_raw_size=2 ** 16 - 1, # this doesn't matter
            session_key=0, # can be anything, we don't use it
            capabilities=server_capabilities,
            system_time=win32_time,
            server_time_zone=0,
            challenge_length=0,
        )

        negotiate_resp = SMBMessage(reply_header_from_request(negotiate_req),
                                    negotiate_reply_params,
                                    SMBNegotiateReplyData(challenge=b'', domain_name=''))

        await self.send_message(writer, encode_smb_message(negotiate_resp))

        # okay now kick off SMB connection machinery

        async def read_client(reader: asyncio.StreamReader,
                              writer_queue: asyncio.Queue[typing.Optional[bytes]]) -> None:
            try:
                read_future = asyncio.ensure_future(self.read_message(reader))
                in_flight_requests: typing.Set[asyncio.Future[typing.Any]] = set()
                while True:
                    wait_arg: Iterable[asyncio.Future[typing.Any]]
                    wait_arg = itertools.chain([read_future, master_kill],
                                               in_flight_requests)
                    (done, pending) = await asyncio.wait(wait_arg,
                                                              return_when=asyncio.FIRST_COMPLETED)
                    for fut in done:
                        try:
                            in_flight_requests.remove(fut)
                        except KeyError:
                            pass

                    if master_kill in done:
                        break

                    if read_future in done:
                        raw_msg = read_future.result()

                        if not raw_msg:
                            log.debug("EOF from client, closing connection")
                            break

                        header = decode_smb_header(raw_msg[:SMB_HEADER_STRUCT_SIZE])

                        # kick off concurrent request handler
                        async def real_handle_request(header: SMBHeader, payload: bytes) -> None:
                            msg = None
                            fn = ''
                            try:
                                commands = decode_smb_payload(header, payload)
                                msg = SMBMessage.from_commands(header, commands)

                                fn = await self.get_msg_fn(msg)

                                ret = await handle_request(server_capabilities,
                                                                self, backend, msg)

                                retb = encode_smb_message(ret)
                            except ProtocolError as e:
                                if e.error not in (STATUS_NO_SUCH_FILE,):
                                    try:
                                        command_name = SMB_COMMAND_TO_NAME[header.command]
                                    except KeyError:
                                        command_name = '0x%x' % (header.command,)

                                    log.debug("Failed request: %s %r %r",
                                              command_name, fn, e)
                                retb = encode_smb_message(error_response(header, e.error))
                            except Exception:
                                log.exception("Unexpected exception!")
                                retb = encode_smb_message(error_response(header))

                            await writer_queue.put(retb)

                        reqfut = asyncio.ensure_future(
                            real_handle_request(header,
                                                raw_msg)
                        )
                        in_flight_requests.add(reqfut)
                        read_future = asyncio.ensure_future(self.read_message(reader))
            finally:
                # release resources associated with connection
                await self.hard_destroy_all_trees(backend)

                # wait for all in flight requests to be done
                if in_flight_requests:
                    await asyncio.wait(in_flight_requests)

                # we have died, signal to writer coroutine to die as well
                await writer_queue.put(None)

        async def write_client(writer: asyncio.StreamWriter,
                               queue: asyncio.Queue[typing.Optional[bytes]]) -> None:
            while True:
                msg = await queue.get()
                if msg is None: break
                await self.send_message(writer, msg)

        writer_queue: asyncio.Queue[typing.Optional[bytes]] = asyncio.Queue()

        # start up reader/writer coroutines
        read_client_future = asyncio.ensure_future(read_client(reader, writer_queue))
        try:
            await write_client(writer, writer_queue)
        finally:
            # make sure read client is dead
            (done, pending) = await asyncio.wait([read_client_future])
            assert len(done) == 1
            # propagate client reader exception (if any)
            done.pop().result()

async def handle_request(server_capabilities: int,
                         cs: SMBClientHandler,
                         backend: AsyncBackend,
                         req: SMBMessage) -> SMBMessage:
    header = req.header
    commands = []
    original_command = req.header.command
    for (parameters, data) in req.commands:
        req = SMBMessage(header, parameters, data)

        # NB: do it before executing request in case this is SMB_CLOSE
        if header.command != SMB_COM_TRANSACTION2:
            fn = await cs.get_msg_fn(req)

        msg = await low_handle_request(server_capabilities, cs, backend, req)

        if header.command != SMB_COM_TRANSACTION2:
            log.debug("Handled request: %s %s",
                      SMB_COMMAND_TO_NAME[header.command],
                      fn)

        commands.append((msg.parameters, msg.data))

        if msg.header.command == SMB_COM_SESSION_SETUP_ANDX:
            header = header_from_header(header, uid=msg.header.uid)
        elif msg.header.command == SMB_COM_TREE_CONNECT_ANDX:
            header = header_from_header(header, tid=msg.header.tid)

        if hasattr(parameters, 'andx_command'):
            command = parameters.andx_command
        else:
            command = SMB_COM_NO_ANDX_COMMAND

        header = header_from_header(header, command=command)

    header = reply_header_from_request_header(header, command=original_command)

    return SMBMessage.from_commands(header, commands)

def create_nt_transact_reply_message(req: SMBMessage, setup_bytes: bytes, param_bytes: bytes, data_bytes: bytes) -> SMBMessage:
    parameters = SMBNTTransactReplyParameters(
        total_parameter_count=len(param_bytes),
        total_data_count=len(data_bytes),
        parameter_count=len(param_bytes),
        parameter_displacement=0,
        data_count=len(data_bytes),
        data_displacement=0,
        setup=setup_bytes,
    )

    data = SMBNTTransactReplyData(parameters=param_bytes,
                                  data=data_bytes)

    return SMBMessage(reply_header_from_request(req),
                      parameters, data)

async def low_handle_request(server_capabilities: int,
                             cs: SMBClientHandler,
                             backend: AsyncBackend,
                             req: SMBMessage) -> SMBMessage:
    async def smb_path_to_fs_path(path: str) -> fsabc.Path:
        comps = path[1:].split("\\")
        if comps and not comps[-1]:
            comps.pop()
        return (await fs.create_path(*comps))

    def normalize_stat(stat: OldStat) -> NormalStat:
        birthtime = getattr(stat, "birthtime", datetime.fromtimestamp(0, tz=timezone.utc))
        mtime = getattr(stat, "mtime", birthtime)
        ctime = getattr(stat, "ctime", mtime)
        atime = getattr(stat, "atime", ctime)

        type = getattr(stat, "type")
        size = getattr(stat, "size")

        return NormalStat(birthtime, mtime, ctime, atime, type, size)

    async def normalize_dir_entry(entry: JustNameDirStat) -> NormalStat:
        # TODO: use new dir entry interface so we can call .stat() on it
        to_normalize = OldStat((await fs.stat(path / entry.name)))
        return normalize_stat(to_normalize)

    def verify_andx(req: SMBMessage) -> None:
        pass

    parameters: SMBParameters
    data: SMBData
    if req.header.command == SMB_COM_SESSION_SETUP_ANDX:
        verify_andx(req)

        if req.parameters.capabilities & ~server_capabilities:
            log.warning("Client's capabilities aren't a subset of Server's: 0x%x vs 0x%x",
                        req.parameters.capabilities, server_capabilities)

        uid = await cs.create_session()

        header = reply_header_from_request(req, uid=uid)
        parameters = SMBSessionSetupAndxReplyParameters(action=1,
                                                        andx_command=req.parameters.andx_command,
                                                        **DEFAULT_ANDX_PARAMETERS)
        data = SMBSessionSetupAndxReplyData(native_os='Unix', native_lan_man='userspacefs',
                                            primary_domain=req.data.primary_domain)
        return SMBMessage(header, parameters, data)
    elif req.header.command == SMB_COM_TREE_CONNECT_ANDX:
        verify_andx(req)

        await cs.verify_uid(req)

        if req.parameters.flags & TREE_CONNECT_ANDX_DISCONNECT_TID:
            try:
                fs = await cs.destroy_tree(req.header.tid)
            except KeyError:
                # NB: this is allowed to fail silently
                pass
            else:
                await backend.tree_disconnect(fs)

        if req.data.service not in ("?????", "A:"):
            log.debug("Client attempted to connect to %r service",
                      req.data.service)
            raise ProtocolError(STATUS_OBJECT_PATH_NOT_FOUND)

        try:
            fs = await backend.tree_connect(req.data.path)
        except KeyError:
            log.debug("Error tree connect: %r", req.data.path)
            raise ProtocolError(STATUS_OBJECT_PATH_NOT_FOUND)

        tid = await cs.create_tree(fs)

        header = reply_header_from_request(req, tid=tid)
        parameters = SMBTreeConnectAndxReplyParameters(
            optional_support=SMB_TREE_CONNECTX_SUPPORT_SEARCH,
            andx_command=req.parameters.andx_command,
            **DEFAULT_ANDX_PARAMETERS,
        )
        data = SMBTreeConnectAndxReplyData(
            service="A:",
            native_file_system="FAT",
        )
        return SMBMessage(header, parameters, data)
    elif req.header.command == SMB_COM_TREE_DISCONNECT:
        await cs.verify_uid(req)

        try:
            fs = await cs.destroy_tree(req.header.tid)
        except KeyError:
            raise ProtocolError(STATUS_SMB_BAD_TID)

        await backend.tree_disconnect(fs)

        return SMBMessage(reply_header_from_request(req), None, None)
    elif req.header.command == SMB_COM_CHECK_DIRECTORY:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            fspath = await smb_path_to_fs_path(req.data.filename)

            try:
                stat = OldStat((await fs.stat(fspath)))
            except FileNotFoundError:
                raise ProtocolError(STATUS_NO_SUCH_FILE)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_NOT_FOUND)
            except PermissionError:
                raise ProtocolError(STATUS_ACCESS_DENIED)

            if stat.type != 'directory':
                raise ProtocolError(STATUS_NOT_A_DIRECTORY)

            return SMBMessage(reply_header_from_request(req), None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_ECHO:
        log.debug("echo...")
        if req.parameters.echo_count > 1:
            raise Exception("Echo count is too high: %r" %
                            (req.parameters.echo_count,))

        return SMBMessage(reply_header_from_request(req),
                          SMBEchoReplyParameters(sequence_number=0),
                          req.data)
    elif req.header.command == SMB_COM_TRANSACTION2:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if req.parameters.timeout:
                raise Exception("Transaction2 Delayed request not supported!")

            if (req.parameters.total_parameter_count != req.parameters.parameter_count or
                req.parameters.total_data_count != req.parameters.data_count):
                raise Exception("Multiple TRANSACTION2 packets not supported!")

            if req.parameters.flags:
                # NBL we don't current support DISCONNECT_TID nor NO_RESPONSE
                raise Exception("Transaction 2 flags not supported!")

            (trans2_type, trans2_params, trans2_data) = decode_transaction_2_request_message(req)

            async def generate_find_data(max_data: int, search_count: int, handle: typing.Optional[AsyncOldDirectory],
                                   info_generator: InfoGeneratorType, idx: int,
                                   entry: typing.Optional[typing.Tuple[str, NormalStat]],
                                   next_entry: typing.Optional[typing.Tuple[str, NormalStat]],
                                   buffered_entries: typing.List[typing.Tuple[str, NormalStat]],
                                   buffered_entries_idx: int) -> typing.Tuple[typing.List[bytes],
                                                                              int,
                                                                              typing.Optional[typing.Tuple[str, NormalStat]],
                                                                              typing.Optional[typing.Tuple[str, NormalStat]],
                                                                              typing.List[typing.Tuple[str, NormalStat]],
                                                                              int]:
                async def get_next_entry() -> typing.Optional[typing.Tuple[str, NormalStat]]:
                    nonlocal buffered_entries_idx, buffered_entries
                    try:
                        toret = buffered_entries[buffered_entries_idx]
                    except IndexError:
                        buffered_entries = []
                        buffered_entries_idx = 0

                        if handle is not None:
                            # NB: 512 is roughly a single FIND_{FIRST,NEXT}2 request
                            entries = await handle.readmany(512)
                            for ent in entries:
                                nstat = await normalize_dir_entry(ent)
                                buffered_entries.append((ent.name, nstat))

                        if not buffered_entries:
                            return None

                        toret = buffered_entries[buffered_entries_idx]
                    buffered_entries_idx += 1
                    return toret

                num_entries_to_ret = 0
                offset = 0
                data: typing.List[bytes] = []

                # XXX: what's the right index to use here?
                for i in range(idx, idx + search_count):
                    if entry is None:
                        break

                    (name, md) = entry

                    is_last = next_entry is None

                    bufs = info_generator(i, offset, flags, name, md, is_last)
                    new_data_len = sum(map(len, bufs))
                    if new_data_len + offset > max_data:
                        break

                    data.extend(bufs)
                    offset += new_data_len
                    num_entries_to_ret += 1

                    entry = next_entry
                    next_entry = await get_next_entry()

                return (data, num_entries_to_ret,
                        entry, next_entry,
                        buffered_entries, buffered_entries_idx)

            MAX_ALIGNMENT_PADDING = 6

            fn = await cs.get_trans2_fn(trans2_params)
            log.debug("Handled request: %s %s",
                      SMB_TRANS2_TO_NAME[trans2_type], fn)

            setup: typing.List[int]
            params_bytes: bytes
            # go through another layer of parsing
            if trans2_type == SMB_TRANS2_FIND_FIRST2:
                assert isinstance(trans2_params, SMBTransaction2FindFirstRequestParameters)
                (search_attributes, search_count,
                 flags, information_level,
                 ) = (trans2_params.search_attributes,
                       trans2_params.search_count,
                       trans2_params.flags,
                       trans2_params.information_level,
                       )
                filename = trans2_params.filename

                if not (search_attributes & SMB_FILE_ATTRIBUTE_DIRECTORY):
                    raise NotImplementedError("Search attributes not implemented: 0x%x" % (search_attributes,))

                try:
                    info_generator = INFO_GENERATORS[information_level]
                except KeyError:
                    raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                        "Find First Information level not supported: %r" %
                                        (information_level,))

                if filename == "\\":
                    is_directory_search = False
                else:
                    comps = filename[1:].split("\\")
                    for c in comps[:-1]:
                        if '*' in c or '?' in c:
                            raise Exception("unsupported search path: %r" % (filename,))

                    if '*' in comps[-1] and comps[-1] not in ["*", "*.*", ""]:
                        raise Exception("unsupported search path: %r" % (filename,))

                    is_directory_search = comps[-1] in ["*", "*.*", ""]
                    if is_directory_search:
                        comps = comps[:-1]

                buffered_entries: typing.List[typing.Tuple[str, NormalStat]]
                buffered_entries_idx: int
                path = await fs.create_path(*comps)
                try:
                    if is_directory_search:
                        handle = await fs.old_open_directory(path)

                        entry: typing.Optional[typing.Tuple[str, NormalStat]]
                        entry = None
                        next_entry: typing.Optional[typing.Tuple[str, NormalStat]]
                        next_entry = None

                        entries = await handle.readmany(2)
                        for idx, ent in enumerate(entries):
                            nstat = await normalize_dir_entry(ent)
                            if idx == 0:
                                entry = (ent.name, nstat)
                            else:
                                assert idx == 1
                                next_entry = (ent.name, nstat)

                        buffered_entries = []
                        buffered_entries_idx = 0
                    else:
                        handle = None
                        stat = OldStat((await fs.stat(path)))
                        entry = (path.name, normalize_stat(stat))
                        next_entry = None
                        buffered_entries = []
                        buffered_entries_idx = 0
                except FileNotFoundError:
                    raise ProtocolError(STATUS_NO_SUCH_FILE)
                except NotADirectoryError:
                    raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

                PARAMS_FMT = "<HHHHH"
                PARAMS_SIZE = struct.calcsize(PARAMS_FMT)

                max_data_count = min(req.parameters.max_data_count,
                                     SMB_MAX_DATA_PAYLOAD - MAX_ALIGNMENT_PADDING -
                                     PARAMS_SIZE)

                (bufl, num_entries_to_ret, entry, next_entry,
                 buffered_entries, buffered_entries_idx) = \
                    await generate_find_data(max_data_count,
                                                  search_count,
                                                  handle,
                                                  info_generator, 0,
                                                  entry, next_entry,
                                                  buffered_entries, buffered_entries_idx)

                is_search_over = next_entry is None

                if (is_search_over and flags & SMB_FIND_CLOSE_AT_EOS or
                    flags & SMB_FIND_CLOSE_AFTER_REQUEST):
                    if handle is not None:
                        await handle.close()
                        handle = None
                    sid = 0
                    is_search_over = True
                else:
                    sid = await cs.create_search(dict(handle=handle,
                                                      entry=entry,
                                                      next_entry=next_entry,
                                                      buffered_entries=buffered_entries,
                                                      buffered_entries_idx=buffered_entries_idx,
                                                      idx=num_entries_to_ret,
                                                      tid=req.header.tid,
                                                      lock=asyncio.Lock(),
                                                      closing=False))


                data_bytes = b''.join(bufl)
                last_name_offset = (0
                                    if is_search_over else
                                    len(data_bytes) - len(bufl[-1]))

                assert information_level != SMB_INFO_QUERY_EAS_FROM_LIST
                ea_error_offset = 0

                setup = []
                params_bytes = struct.pack(PARAMS_FMT,
                                           sid, num_entries_to_ret,
                                           int(is_search_over),
                                           ea_error_offset,
                                           0 if is_search_over else
                                           last_name_offset)
            elif trans2_type == SMB_TRANS2_FIND_NEXT2:
                assert isinstance(trans2_params, SMBTransaction2FindNextRequestParameters)
                (sid, search_count, information_level,
                 resume_key, flags) = (trans2_params.sid, trans2_params.search_count,
                                       trans2_params.information_level,
                                       trans2_params.resume_key, trans2_params.flags)
                if resume_key:
                    raise NotImplementedError("resume key is not yet handled")

                filename = trans2_params.filename

                try:
                    info_generator = INFO_GENERATORS[information_level]
                except KeyError:
                    raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                        "Find First Information level not supported: %r" %
                                        (information_level,))


                search_md = await cs.ref_search(sid)
                try:
                    PARAMS_FMT = "<HHHH"
                    PARAMS_SIZE = struct.calcsize(PARAMS_FMT)

                    max_data_count = min(req.parameters.max_data_count,
                                         SMB_MAX_DATA_PAYLOAD - MAX_ALIGNMENT_PADDING
                                         - PARAMS_SIZE)

                    (bufl, num_entries_to_ret,
                     entry, next_entry,
                     search_md['buffered_entries'], search_md['buffered_entries_idx']) = \
                        await generate_find_data(max_data_count,
                                                      search_count,
                                                      search_md['handle'],
                                                      info_generator,
                                                      search_md['idx'],
                                                      search_md['entry'],
                                                      search_md['next_entry'],
                                                      search_md['buffered_entries'],
                                                      search_md['buffered_entries_idx'])

                    search_md['idx'] += num_entries_to_ret
                    search_md['entry'] = entry
                    search_md['next_entry'] = next_entry

                    is_search_over = next_entry is None
                finally:
                    if (is_search_over and flags & SMB_FIND_CLOSE_AFTER_REQUEST or
                        flags & SMB_FIND_CLOSE_AFTER_REQUEST):
                        if search_md['handle'] is not None:
                            await search_md['handle'].close()
                            search_md['handle'] = None
                        await cs.deref_search(sid)
                        await cs.destroy_search(sid)
                        is_search_over = True
                    else:
                        await cs.deref_search(sid)

                data_bytes = b''.join(bufl)
                last_name_offset = (0
                                    if is_search_over else
                                    len(data_bytes) - len(bufl[-1]))

                assert information_level != SMB_INFO_QUERY_EAS_FROM_LIST
                ea_error_offset = 0

                setup = []
                params_bytes = struct.pack(PARAMS_FMT,
                                           num_entries_to_ret,
                                           int(is_search_over),
                                           ea_error_offset,
                                           last_name_offset)
            elif trans2_type == SMB_TRANS2_QUERY_FS_INFORMATION:
                assert isinstance(trans2_params, SMBTransaction2QueryFSInformationRequestParameters)
                (information_level,) = (trans2_params.information_level,)

                try:
                    fs_info_generator = FS_INFO_GENERATORS[information_level]
                except KeyError:
                    raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                        "QUERY FS Information level not supported: %r" %
                                        (information_level,))

                data_bytes = await fs_info_generator(fs)

                setup = []
                params_bytes = b''
            elif trans2_type == SMB_TRANS2_QUERY_PATH_INFORMATION:
                assert isinstance(trans2_params, SMBTransaction2QueryPathInformationRequestParams)
                (information_level,) = (trans2_params.information_level,)

                try:
                    query_path_info_generator = QUERY_FILE_INFO_GENERATORS[information_level]
                except KeyError:
                    raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                        "QUERY PATH Information level not supported: %r" %
                                        (information_level,))

                spath = trans2_params.filename
                fspath = await smb_path_to_fs_path(spath)

                try:
                    md = OldStat((await fs.stat(fspath)))
                except FileNotFoundError:
                    raise ProtocolError(STATUS_NO_SUCH_FILE)
                except NotADirectoryError:
                    raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

                setup = []
                name = fspath.name if fspath.name else '\\'
                (ea_error_offset, data_bytes) = query_path_info_generator(name, normalize_stat(md))
                params_bytes = struct.pack("<H", ea_error_offset)
            elif trans2_type == SMB_TRANS2_QUERY_FILE_INFORMATION:
                assert isinstance(trans2_params, SMBTransaction2QueryFileInformationRequestParams)
                try:
                    query_file_info_generator = QUERY_FILE_INFO_GENERATORS[trans2_params.information_level]
                except KeyError:
                    raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                        "QUERY FILE Information level not supported: %r" %
                                        (trans2_params.information_level,))

                try:
                    fid_md = await cs.ref_file(trans2_params.fid)
                except KeyError:
                    raise ProtocolError(STATUS_INVALID_HANDLE)

                try:
                    file_path = fid_md['path']
                    md = OldStat((await fs.fstat(fid_md['handle'])))
                finally:
                    await cs.deref_file(trans2_params.fid)

                setup = []
                fspath = await smb_path_to_fs_path(file_path)
                name = fspath.name if fspath.name else '\\'
                (ea_error_offset, data_bytes) = query_file_info_generator(name, normalize_stat(md))
                params_bytes = struct.pack("<H", ea_error_offset)
            elif trans2_type == SMB_TRANS2_SET_FILE_INFORMATION:
                assert isinstance(trans2_params, SMBTransaction2SetFileInformationRequestParameters)
                try:
                    fid_md = await cs.ref_file(trans2_params.fid)
                except KeyError:
                    raise ProtocolError(STATUS_INVALID_HANDLE)
                try:
                    if trans2_params.information_level in (SMB_SET_FILE_BASIC_INFO,
                                                           SMB_SET_FILE_BASIC_INFORMATION):
                        assert isinstance(trans2_data, SMBTransaction2SetFileInformationBasicInfoRequestData)
                        # NB: this call is advisory and can be ignored per
                        #     SetFileTime documentation, e.g. FAT can't record
                        #     these times.
                        if True:
                            stn = await fs.fstat(fid_md['handle'])

                            def tt(f: int, o: float) -> float:
                                # TODO: support 2 ** 64 - 1
                                # set 'sticky time' for file handle per samba
                                if f in (0, 2 ** 64 - 1):
                                    return o
                                return win32_to_datetime(f).timestamp()
                            await fs.futimes(fid_md['handle'],
                                             times=(tt(trans2_data.last_access_time, stn.st_atime),
                                                    tt(trans2_data.last_write_time, stn.st_mtime)))
                    elif trans2_params.information_level in (SMB_SET_FILE_END_OF_FILE_INFO,
                                                             SMB_SET_FILE_END_OF_FILE_INFORMATION):
                        assert isinstance(trans2_data, SMBTransaction2SetFileInformationEndOfFileRequestData)
                        await fid_md['handle'].truncate(trans2_data.end_of_file)
                    elif trans2_params.information_level == (SMB_INFO_PASSTHROUGH + FileAllocationInformation):
                        # don't need to do anything nor can we
                        pass
                    elif trans2_params.information_level == (SMB_INFO_PASSTHROUGH + FileDispositionInformation):
                        # can't really honor this for now
                        # TODO: we can implement this on-server
                        pass
                    else:
                        raise ProtocolError(STATUS_OS2_INVALID_LEVEL,
                                            "SET FILE INFORMATION Information level not supported: %r" %
                                            (trans2_params.information_level,))
                finally:
                    await cs.deref_file(trans2_params.fid)

                setup = []
                data_bytes = b''
                params_bytes = b''
            else:
                log.info("TRANS2 Sub command not supported: %02x, %s" % (trans2_type, req))
                raise ProtocolError(STATUS_NOT_SUPPORTED)

            assert len(setup) * 2 <= req.parameters.max_setup_count, "TRANSACTION2 setup bytes count is too large %r vs required %r" % (len(setup) * 2, req.parameters.max_setup_count)
            assert len(params_bytes) <= req.parameters.max_parameter_count, "TRANSACTION2 params bytes count is too large %r vs required %r" % (len(params_bytes), req.parameters.max_parameter_count)
            assert len(data_bytes) <= req.parameters.max_data_count, "TRANSACTION2 data bytes count is too large %r vs required %r" % (len(data_bytes), req.parameters.max_data_count)

            parameters = SMBTransaction2ReplyParameters(
                total_parameter_count=len(params_bytes),
                total_data_count=len(data_bytes),
                parameter_count=len(params_bytes),
                parameter_displacement=0,
                data_count=len(data_bytes),
                data_displacement=0,
                setup=setup,
            )
            data = SMBTransaction2ReplyData(
                parameters=params_bytes,
                data=data_bytes,
            )
            return SMBMessage(reply_header_from_request(req),
                              parameters,
                              data)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_QUERY_INFORMATION_DISK:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            parameters = SMBQueryInformationDiskReplyParameters(
                total_units=2 ** 16 - 1,
                blocks_per_unit=16384,
                block_size=512,
                free_units=0,
            )
            return SMBMessage(reply_header_from_request(req),
                              parameters, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_NT_CREATE_ANDX:
        verify_andx(req)

        rparams = req.parameters

        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if (rparams.flags &
                (
                 NT_CREATE_OPEN_TARGET_DIR)):
                raise Exception("SMB_COM_NT_CREATE_ANDX doesn't support flags! 0x%x" % (rparams.flags,))

            # NB: We only support full sharing for now.
            #     2.2.4.64.1 of MS-CIFS says we SHOULD respect
            #     rparams.share_access but since our FS interface does
            #     not implement that, we ignore it.

            mode = 0

            wants_read = (rparams.desired_access &
                          (GENERIC_READ | FILE_READ_DATA | MAXIMUM_ALLOWED | GENERIC_EXECUTE |
                           GENERIC_ALL))
            wants_write = (rparams.desired_access &
                           (GENERIC_WRITE | FILE_WRITE_DATA | MAXIMUM_ALLOWED | GENERIC_ALL))

            if wants_read and wants_write:
                mode = mode | os.O_RDWR
            elif wants_read:
                mode = mode | os.O_RDONLY
            elif wants_write:
                mode = mode | os.O_WRONLY
            else:
                log.info("Isn't requesting any READ/WRITE privileges: 0x%x", rparams.desired_access)

            # we don't support supersede for now
            if rparams.create_disposition == FILE_SUPERSEDE:
                raise ProtocolError(STATUS_ACCESS_DENIED)
            elif rparams.create_disposition == FILE_CREATE:
                mode = mode | os.O_CREAT | os.O_EXCL
            elif rparams.create_disposition == FILE_OPEN_IF:
                mode = mode | os.O_CREAT
            elif rparams.create_disposition == FILE_OVERWRITE:
                mode = mode | os.O_TRUNC
            elif rparams.create_disposition == FILE_OVERWRITE_IF:
                mode = mode | os.O_CREAT | os.O_TRUNC

            if rparams.create_options & FILE_DELETE_ON_CLOSE:
                raise ProtocolError(STATUS_ACCESS_DENIED)

            if rparams.create_options & FILE_OPEN_BY_FILE_ID:
                raise ProtocolError(STATUS_NOT_SUPPORTED)

            if rparams.root_directory_fid:
                try:
                    root_md = await cs.ref_file(rparams.root_directory_fid)
                except KeyError:
                    raise ProtocolError(STATUS_INVALID_HANDLE)
                try:
                    root_path = root_md['path']
                finally:
                    await cs.deref_file(rparams.root_directory_fid)
            else:
                root_path = ""

            file_path = root_path + req.data.filename

            is_directory = False
            path = await smb_path_to_fs_path(file_path)
            try:
                if (mode & os.O_CREAT) and (rparams.create_options & FILE_DIRECTORY_FILE):
                    try:
                        await fs.mkdir(path)
                    except FileExistsError:
                        if mode & os.O_EXCL:
                            raise
                    mode &= ~(os.O_EXCL | os.O_CREAT)

                fhandle = await fs.open(path, mode)
                md = OldStat((await fs.fstat(fhandle)))
            except FileExistsError:
                raise ProtocolError(STATUS_OBJECT_NAME_COLLISION)
            except FileNotFoundError:
                raise ProtocolError(STATUS_NO_SUCH_FILE)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

            is_directory = md.type == "directory"

            # NB: if the directory we created was removed before we opened the
            #     file, then flag an error since the client expects this to be
            #     a directory handle.
            if (not is_directory and
                rparams.create_options & FILE_DIRECTORY_FILE):
                raise ProtocolError(STATUS_UNSUCCESSFUL)

            if (is_directory and
                rparams.create_options & FILE_NON_DIRECTORY_FILE):
                await fhandle.close()
                raise ProtocolError(STATUS_FILE_IS_A_DIRECTORY)

            fid = await cs.create_file(file_path,
                                            fhandle,
                                            req.header.tid)

            directory = int(is_directory)
            ext_attr = (ATTR_DIRECTORY
                        if directory else
                        ATTR_NORMAL)

            file_data_size = md.size

            FILE_TYPE_DISK = 0

            md2 = normalize_stat(md)

            parameters = SMBNTCreateAndxReplyData(
                op_lock_level=0,
                fid=fid,
                create_disposition=rparams.create_disposition,
                create_time=datetime_to_win32(md2.birthtime),
                last_access_time=datetime_to_win32(md2.atime),
                last_write_time=datetime_to_win32(md2.mtime),
                last_change_time=datetime_to_win32(md2.ctime),
                ext_file_attributes=ext_attr,
                allocation_size=4096,
                end_of_file=file_data_size,
                resource_type=FILE_TYPE_DISK,
                nm_pipe_status=0,
                directory=directory,
                andx_command=req.parameters.andx_command,
                **DEFAULT_ANDX_PARAMETERS)
            return SMBMessage(reply_header_from_request(req),
                              parameters, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_READ_ANDX:
        verify_andx(req)

        request = req.parameters
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            try:
                fid_md = await cs.ref_file(request.fid)
            except KeyError:
                raise ProtocolError(STATUS_INVALID_HANDLE)
            try:
                buf = memoryview(bytearray(request.max_count_of_bytes_to_return))
                amt = await fs.preadinto(fid_md['handle'], buf, request.offset)
                buf = buf[:amt]
            finally:
                await cs.deref_file(request.fid)

            parameters = SMBReadAndxReplyParameters(available=0,
                                                    data_length=len(buf),
                                                    andx_command=req.parameters.andx_command,
                                                    **DEFAULT_ANDX_PARAMETERS)

            return SMBMessage(reply_header_from_request(req),
                              parameters, buf)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_CLOSE:
        request = req.parameters
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            try:
                fidmd = await cs.destroy_file(request.fid)
                assert 'handle' in fidmd
            except KeyError:
                raise ProtocolError(STATUS_INVALID_HANDLE)

            # Close asynchronously
            def on_fail() -> None:
                log.warning("Closing %r failed!", fidmd['handle'])
            asyncio.ensure_future(cant_fail(on_fail, asyncio.ensure_future(fidmd['handle'].close())))

            return SMBMessage(reply_header_from_request(req), None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_NT_TRANSACT:
        await cs.verify_uid(req)
        (fs, idm) = await cs.verify_tid_mapper(req)
        try:
            (function, nt_transact_setup,
             nt_transact_parameters, nt_transact_data) = \
                decode_nt_transact_request_message(req)

            if function == NT_TRANSACT_NOTIFY_CHANGE:
                assert isinstance(nt_transact_setup, SMBNTTransactNotifyChangeRequestSetup)
                (completion_filter, fid, watch_tree) = (
                    nt_transact_setup.completion_filter,
                    nt_transact_setup.fid,
                    nt_transact_setup.watch_tree,
                    )

                try:
                    changes = await cs.watch_file(fid, fs, completion_filter, watch_tree)
                except KeyError:
                    raise ProtocolError(STATUS_INVALID_HANDLE)

                if isinstance(changes, str):
                    assert changes == 'reset'
                    raise ProtocolError(STATUS_NOTIFY_ENUM_DIR)

                bufl = []
                curoffset = 0
                for (idx, change) in enumerate(changes):
                    if curoffset % 4:
                        bufl.append(b'\0' * (4 - curoffset % 4))
                        curoffset += len(bufl[-1])
                    action = {"added": FILE_ACTION_ADDED,
                              "removed": FILE_ACTION_REMOVED,
                              "modified": FILE_ACTION_MODIFIED,
                              "renamed_from": FILE_ACTION_RENAMED_OLD_NAME,
                              "renamed_to": FILE_ACTION_RENAMED_NEW_NAME,}[change.action]

                    filename_encoded = '\\'.join(change.path).encode("utf-16-le")
                    potential_next_entry_offset = 4 + 4 + 4 + len(filename_encoded)
                    if potential_next_entry_offset % 4:
                        potential_next_entry_offset += 4 - potential_next_entry_offset % 4
                    next_entry_offset = (potential_next_entry_offset
                                         if idx != len(changes) - 1 else
                                         0)
                    bufl.append(struct.pack("<III", next_entry_offset, action,
                                            len(filename_encoded)))
                    curoffset += len(bufl[-1])
                    bufl.append(filename_encoded)
                    curoffset += len(bufl[-1])

                param_bytes = b''.join(bufl)
                data_bytes = b''

                return create_nt_transact_reply_message(req, b'', param_bytes, data_bytes)
            elif function == NT_TRANSACT_IOCTL:
                assert isinstance(nt_transact_setup, SMBNTTransactIoctlRequestSetup)

                if nt_transact_setup.is_fsctl:
                    if nt_transact_setup.function_code == FSCTL_CREATE_OR_GET_OBJECT_ID:

                        try:
                            fid_md = await cs.ref_file(nt_transact_setup.fid)
                        except KeyError:
                            raise ProtocolError(STATUS_INVALID_HANDLE)
                        try:
                            md = OldStat((await fs.fstat(fid_md['handle'])))

                            iid = await idm.map_id(md.id)

                            # FILE_OBJECTID_BUFFER Type
                            data_bytes = struct.pack(
                                "<QQQQQQQQ",
                                iid & 0xffffffffffffffff,
                                iid >> 64,
                                # volume ID is just 0
                                0, 0,
                                # birth file id is the same as the current file id
                                iid & 0xffffffffffffffff,
                                iid >> 64,
                                # domain id is just 0,
                                0, 0)
                        finally:
                            await cs.deref_file(nt_transact_setup.fid)

                        # the client must ignore this but the server
                        # is specified to send it
                        setup_bytes = struct.pack("<H", len(data_bytes))

                        return create_nt_transact_reply_message(req, setup_bytes, b'', data_bytes)

                raise ProtocolError(STATUS_ACCESS_DENIED,
                                    "ioctl not understood %r" %
                                    (nt_transact_setup,))
            else:
                assert False
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_WRITE_ANDX:
        verify_andx(req)
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            try:
                fid_md = await cs.ref_file(req.parameters.fid)
            except KeyError:
                raise ProtocolError(STATUS_INVALID_HANDLE)
            try:
                if req.parameters.timeout:
                    log.info("Got timeout value for SMB_COM_WRITE: %r, ignoring...",
                             req.parameters.timeout)

                amt = await fs.pwrite(fid_md['handle'], req.data, req.parameters.offset)

                WRITE_THROUGH_MODE = 0x1
                if req.parameters.write_mode & WRITE_THROUGH_MODE:
                    await fs.fsync(fid_md['handle'])
            finally:
                await cs.deref_file(req.parameters.fid)

            parameters = SMBWriteAndxReplyParameters(count=amt,
                                                     available=0xffff,
                                                     andx_command=req.parameters.andx_command,
                                                     **DEFAULT_ANDX_PARAMETERS)

            return SMBMessage(reply_header_from_request(req),
                              parameters, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_FLUSH:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            try:
                fid_md = await cs.ref_file(req.parameters.fid)
            except KeyError:
                raise ProtocolError(STATUS_INVALID_HANDLE)
            try:
                await fs.fsync(fid_md['handle'])
            finally:
                await cs.deref_file(req.parameters.fid)


            return SMBMessage(reply_header_from_request(req),
                              None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_DELETE:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if req.data.buffer_format != 0x4:
                raise Exception("Buffer format not accepted!")
            path = await smb_path_to_fs_path(req.data.filename)

            try:
                await fs.unlink(path)
            except FileNotFoundError:
                raise ProtocolError(STATUS_NO_SUCH_FILE)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

            return SMBMessage(reply_header_from_request(req),
                              None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_CREATE_DIRECTORY:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if req.data.buffer_format != 0x4:
                raise Exception("Buffer format not accepted!")
            path = await smb_path_to_fs_path(req.data.filename)

            try:
                await fs.mkdir(path)
            except FileNotFoundError:
                raise ProtocolError(STATUS_OBJECT_PATH_NOT_FOUND)
            except FileExistsError:
                raise ProtocolError(STATUS_OBJECT_NAME_COLLISION)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

            return SMBMessage(reply_header_from_request(req),
                              None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_DELETE_DIRECTORY:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if req.data.buffer_format != 0x4:
                raise Exception("Buffer format not accepted!")
            path = await smb_path_to_fs_path(req.data.filename)

            try:
                await fs.rmdir(path)
            except FileNotFoundError:
                raise ProtocolError(STATUS_NO_SUCH_FILE)
            except FileExistsError:
                raise ProtocolError(STATUS_DIRECTORY_NOT_EMPTY)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_INVALID)
            except OSError as e:
                if e.errno == errno.ENOTEMPTY:
                    raise ProtocolError(STATUS_DIRECTORY_NOT_EMPTY)
                else:
                    raise

            return SMBMessage(reply_header_from_request(req),
                              None, None)
        finally:
            await cs.deref_tid(req.header.tid)
    elif req.header.command == SMB_COM_RENAME:
        await cs.verify_uid(req)
        fs = await cs.verify_tid(req)
        try:
            if (req.data.buffer_format_1 != 0x4 or
                req.data.buffer_format_2 != 0x4):
                raise Exception("Buffer format not accepted!")
            old_path = await smb_path_to_fs_path(req.data.old_filename)
            new_path = await smb_path_to_fs_path(req.data.new_filename)

            try:
                await fs.stat(new_path)
            except FileNotFoundError:
                pass
            else:
                raise ProtocolError(STATUS_OBJECT_NAME_COLLISION)

            try:
                await fs.replace(old_path, new_path)
            except FileNotFoundError:
                raise ProtocolError(STATUS_NO_SUCH_FILE)
            except NotADirectoryError:
                raise ProtocolError(STATUS_OBJECT_PATH_SYNTAX_BAD)

            return SMBMessage(reply_header_from_request(req),
                              None, None)
        finally:
            await cs.deref_tid(req.header.tid)

    raise ProtocolError(STATUS_NOT_SUPPORTED)

# SMBServer abstracts away the fact that it is implemented using
# asyncio. It expects to be used in normal python code.
class SMBServer(object):
    def __init__(self,
                 backend: Backend,
                 address: typing.Optional[typing.Tuple[str, int]] = None,
                 sock: typing.Optional[socket.socket] = None) -> None:
        kw: typing.Dict[str, typing.Any] = {}

        if address is not None:
            assert sock is None, 'address and sock should not be specified at the same time'
            kw['host'] = address[0]
            kw['port'] = address[1]
        else:
            assert sock is not None, "neither address nor sock were specified"
            kw['sock'] = sock

        self._loop = asyncio.new_event_loop()

        self._worker_pool = AsyncWorkerPool(self._loop, 8)

        async_backend = AsyncBackend(backend, self._worker_pool)
        self._master_kill: asyncio.Future[None] = asyncio.Future(loop=self._loop)

        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            try:
                await SMBClientHandler(self._worker_pool).run(async_backend,
                                                  self._master_kill,
                                                  reader, writer)
            except Exception:
                log.exception("Client handler failed!")
            else:
                log.debug("client done!")
            finally:
                writer.close()

        start_server_coro = asyncio.start_server(handle_client,
                                                 **kw,
        )
        self._server = self._loop.run_until_complete(start_server_coro)

    def stop(self) -> None:
        async def _on_main_thread() -> None:
            self._master_kill.set_result(None)
            self._server.close()
        asyncio.run_coroutine_threadsafe(_on_main_thread(), self._loop)

    def run(self) -> None:
        # NB: due to a quirk in asyncio, we need to call wait_closed()
        #     before close() is called so that it waits for all
        #     open client connections to close before returning after close()
        #     is called
        self._loop.run_until_complete(self._server.wait_closed())

    def close(self) -> None:
        self._server.close()
        self._loop.close()
        self._worker_pool.close()

PathT = typing.TypeVar('PathT', bound=fsabc.Path)
FileT = typing.TypeVar('FileT', bound=fsabc.File)

class SimpleSMBBackend(Backend):
    def __init__(self, path: str, fs: fsabc.FileSystemG[PathT, FileT]) -> None:
        self._path = path
        # NB: we use file system correctly (only passing it file
        #     handles and paths it created) so we can cast to generic
        #     type here (Without having to parameterize the entire file)
        self._fs = fsabc.safe_cast_file_system(fs)

    def tree_connect(self, path: str) -> fsabc.FileSystem:
        ipath = path.rsplit("\\", 1)[-1].upper()
        if ipath == self._path.rsplit("\\", 1)[-1].upper():
            return self._fs
        raise KeyError()

    def tree_disconnect(self, fs: fsabc.FileSystem) -> None:
        pass

    def tree_disconnect_hard(self, fs: fsabc.FileSystem) -> None:
        pass

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

    backend = SimpleSMBBackend("\\\\127.0.0.1\\userspacefs", fs)

    with contextlib.closing(SMBServer(backend, address=('127.0.0.1', 8888))) as server:
        server.run()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
