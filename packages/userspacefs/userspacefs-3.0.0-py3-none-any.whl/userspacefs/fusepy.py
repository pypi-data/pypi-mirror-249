# This file is part of userspacefs.

# Copyright (c) 2018-2023 Rian Hunter <rian@alum.mit.edu>

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

# Copyright (c) 2012 Terence Honles <terence@honles.com> (maintainer)
# Copyright (c) 2008 Giorgos Verigakis <verigak@gmail.com> (author)
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

from __future__ import print_function, absolute_import, division

import ctypes
import errno
import functools
import logging
import os
import sys
import warnings

from abc import ABC
from ctypes.util import find_library
from platform import machine, system
from signal import signal, SIGINT, SIG_DFL, SIGTERM
from stat import S_IFDIR
from traceback import print_exc

import typing
import typing_extensions

from collections.abc import Callable, Iterator

from functools import partial

log = logging.getLogger("fuse")
_system = system()
_machine = machine()

# NOTE:
#
# sizeof(long)==4 on Windows 32-bit and 64-bit
# sizeof(long)==4 on Cygwin 32-bit and ==8 on Cygwin 64-bit
#
# We have to fix up c_long and c_ulong so that it matches the
# Cygwin (and UNIX) sizes when run on Windows.
import sys

c_win_long: typing.Type[typing.Any]
c_win_ulong: typing.Type[typing.Any]

if sys.maxsize > 0xffffffff:
    c_win_long = ctypes.c_int64
    c_win_ulong = ctypes.c_uint64
else:
    c_win_long = ctypes.c_int32
    c_win_ulong = ctypes.c_uint32

class c_win_timespec(ctypes.Structure):
    _fields_ = [('tv_sec', c_win_long), ('tv_nsec', c_win_long)]

c_openbsd_time_t = ctypes.c_int64
class c_openbsd_timespec(ctypes.Structure):
    _fields_ = [('tv_sec', c_openbsd_time_t), ('tv_nsec', ctypes.c_long)]

class c_std_timespec(ctypes.Structure):
    _fields_ = [('tv_sec', ctypes.c_long), ('tv_nsec', ctypes.c_long)]

if sys.platform == 'win32':
    c_timespec = c_win_timespec
elif sys.platform.startswith("openbsd"):
    c_timespec = c_openbsd_timespec
else:
    c_timespec = c_std_timespec

class c_utimbuf(ctypes.Structure):
    _fields_ = [('actime', c_timespec), ('modtime', c_timespec)]

FuseFieldsType = typing.List[typing.Union[typing.Tuple[str, typing.Type[typing.Any]], typing.Tuple[str, typing.Type[typing.Any], int]]]

_libfuse_path = os.environ.get('FUSE_LIBRARY_PATH')
if not _libfuse_path:
    if _system == 'Darwin':
        # libfuse dependency
        _libiconv = ctypes.CDLL(find_library('iconv'), ctypes.RTLD_GLOBAL)

        _libfuse_path = (find_library('fuse4x') or find_library('osxfuse') or
                         find_library('fuse'))
    elif sys.platform == "win32" and _system == 'Windows':
        import winreg as reg
        def Reg32GetValue(rootkey, keyname, valname):
            key, val = None, None
            try:
                key = reg.OpenKey(rootkey, keyname, 0, reg.KEY_READ | reg.KEY_WOW64_32KEY)
                val = str(reg.QueryValueEx(key, valname)[0])
            except WindowsError:
                pass
            finally:
                if key is not None:
                    reg.CloseKey(key)
            return val
        _libfuse_path = Reg32GetValue(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WinFsp", r"InstallDir")
        if _libfuse_path:
            _libfuse_path += r"bin\winfsp-%s.dll" % ("x64" if sys.maxsize > 0xffffffff else "x86")
    else:
        _libfuse_path = find_library('fuse')

if not _libfuse_path:
    raise EnvironmentError('Unable to find libfuse')
else:
    _libfuse = ctypes.CDLL(_libfuse_path)

if _system == 'Darwin' and hasattr(_libfuse, 'macfuse_version'):
    _system = 'Darwin-MacFuse'

c_dev_t: typing.Type[typing.Any]
c_fsblkcnt_t: typing.Type[typing.Any]
c_fsfilcnt_t: typing.Type[typing.Any]
c_gid_t: typing.Type[typing.Any]
c_mode_t: typing.Type[typing.Any]
c_off_t: typing.Type[typing.Any]
c_pid_t: typing.Type[typing.Any]
c_uid_t: typing.Type[typing.Any]
c_stat_fields: FuseFieldsType

if _system in ('Darwin', 'Darwin-MacFuse', 'FreeBSD'):
    ENOTSUP = 45

    c_dev_t = ctypes.c_int32
    c_fsblkcnt_t = ctypes.c_ulong
    c_fsfilcnt_t = ctypes.c_ulong
    c_gid_t = ctypes.c_uint32
    c_mode_t = ctypes.c_uint16
    c_off_t = ctypes.c_int64
    c_pid_t = ctypes.c_int32
    c_uid_t = ctypes.c_uint32
    if _system == 'FreeBSD':
        setxattr_t = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t, ctypes.c_int)

        getxattr_t = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t)
    else:
        setxattr_t = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t, ctypes.c_int,
            ctypes.c_uint32)

        getxattr_t = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t, ctypes.c_uint32)
    if _system == 'Darwin':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_uint16),
            ('st_ino', ctypes.c_uint64),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_birthtimespec', c_timespec),
            ('st_size', c_off_t),
            ('st_blocks', ctypes.c_int64),
            ('st_blksize', ctypes.c_int32),
            ('st_flags', ctypes.c_int32),
            ('st_gen', ctypes.c_int32),
            ('st_lspare', ctypes.c_int32),
            ('st_qspare', ctypes.c_int64)]
    else:
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_ino', ctypes.c_uint32),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_uint16),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_size', c_off_t),
            ('st_blocks', ctypes.c_int64),
            ('st_blksize', ctypes.c_int32)]
elif _system == 'Linux':
    ENOTSUP = 95

    c_dev_t = ctypes.c_ulonglong
    c_fsblkcnt_t = ctypes.c_ulonglong
    c_fsfilcnt_t = ctypes.c_ulonglong
    c_gid_t = ctypes.c_uint
    c_mode_t = ctypes.c_uint
    c_off_t = ctypes.c_longlong
    c_pid_t = ctypes.c_int
    c_uid_t = ctypes.c_uint
    setxattr_t = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t, ctypes.c_int)

    getxattr_t = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t)

    if _machine == 'x86_64':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_ino', ctypes.c_ulong),
            ('st_nlink', ctypes.c_ulong),
            ('st_mode', c_mode_t),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('__pad0', ctypes.c_int),
            ('st_rdev', c_dev_t),
            ('st_size', c_off_t),
            ('st_blksize', ctypes.c_long),
            ('st_blocks', ctypes.c_long),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    elif _machine == 'mips':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('__pad1_1', ctypes.c_ulong),
            ('__pad1_2', ctypes.c_ulong),
            ('__pad1_3', ctypes.c_ulong),
            ('st_ino', ctypes.c_ulong),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_ulong),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2_1', ctypes.c_ulong),
            ('__pad2_2', ctypes.c_ulong),
            ('st_size', c_off_t),
            ('__pad3', ctypes.c_ulong),
            ('st_atimespec', c_timespec),
            ('__pad4', ctypes.c_ulong),
            ('st_mtimespec', c_timespec),
            ('__pad5', ctypes.c_ulong),
            ('st_ctimespec', c_timespec),
            ('__pad6', ctypes.c_ulong),
            ('st_blksize', ctypes.c_long),
            ('st_blocks', ctypes.c_long),
            ('__pad7_1', ctypes.c_ulong),
            ('__pad7_2', ctypes.c_ulong),
            ('__pad7_3', ctypes.c_ulong),
            ('__pad7_4', ctypes.c_ulong),
            ('__pad7_5', ctypes.c_ulong),
            ('__pad7_6', ctypes.c_ulong),
            ('__pad7_7', ctypes.c_ulong),
            ('__pad7_8', ctypes.c_ulong),
            ('__pad7_9', ctypes.c_ulong),
            ('__pad7_10', ctypes.c_ulong),
            ('__pad7_11', ctypes.c_ulong),
            ('__pad7_12', ctypes.c_ulong),
            ('__pad7_13', ctypes.c_ulong),
            ('__pad7_14', ctypes.c_ulong)]
    elif _machine == 'ppc':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_ino', ctypes.c_ulonglong),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', ctypes.c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', ctypes.c_long),
            ('st_blocks', ctypes.c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    elif _machine == 'ppc64' or _machine == 'ppc64le':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_ino', ctypes.c_ulong),
            ('st_nlink', ctypes.c_ulong),
            ('st_mode', c_mode_t),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('__pad', ctypes.c_uint),
            ('st_rdev', c_dev_t),
            ('st_size', c_off_t),
            ('st_blksize', ctypes.c_long),
            ('st_blocks', ctypes.c_long),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    elif _machine == 'aarch64':
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('st_ino', ctypes.c_ulong),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad1', ctypes.c_ulong),
            ('st_size', c_off_t),
            ('st_blksize', ctypes.c_int),
            ('__pad2', ctypes.c_int),
            ('st_blocks', ctypes.c_long),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    else:
        # i686, use as fallback for everything else
        c_stat_fields = [
            ('st_dev', c_dev_t),
            ('__pad1', ctypes.c_ushort),
            ('__st_ino', ctypes.c_ulong),
            ('st_mode', c_mode_t),
            ('st_nlink', ctypes.c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', ctypes.c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', ctypes.c_long),
            ('st_blocks', ctypes.c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_ino', ctypes.c_ulonglong)]
elif _system == 'Windows' or _system.startswith('CYGWIN'):
    ENOTSUP = 129 if _system == 'Windows' else 134
    c_dev_t = ctypes.c_uint
    c_fsblkcnt_t = c_win_ulong
    c_fsfilcnt_t = c_win_ulong
    c_gid_t = ctypes.c_uint
    c_mode_t = ctypes.c_uint
    c_off_t = ctypes.c_longlong
    c_pid_t = ctypes.c_int
    c_uid_t = ctypes.c_uint
    setxattr_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t, ctypes.c_int)
    getxattr_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t)
    c_stat_fields = [
        ('st_dev', c_dev_t),
        ('st_ino', ctypes.c_ulonglong),
        ('st_mode', c_mode_t),
        ('st_nlink', ctypes.c_ushort),
        ('st_uid', c_uid_t),
        ('st_gid', c_gid_t),
        ('st_rdev', c_dev_t),
        ('st_size', c_off_t),
        ('st_atimespec', c_timespec),
        ('st_mtimespec', c_timespec),
        ('st_ctimespec', c_timespec),
        ('st_blksize', ctypes.c_int),
        ('st_blocks', ctypes.c_longlong),
        ('st_birthtimespec', c_timespec)]
elif _system == 'OpenBSD':
    ENOTSUP = 91
    c_dev_t = ctypes.c_int32
    c_uid_t = ctypes.c_uint32
    c_gid_t = ctypes.c_uint32
    c_mode_t = ctypes.c_uint32
    c_off_t = ctypes.c_int64
    c_pid_t = ctypes.c_int32
    c_ino_t = ctypes.c_uint64
    c_nlink_t = ctypes.c_uint32
    c_blkcnt_t = ctypes.c_int64
    c_blksize_t = ctypes.c_int32
    setxattr_t = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t, ctypes.c_int)
    getxattr_t = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_byte),
        ctypes.c_size_t)
    c_fsblkcnt_t = ctypes.c_uint64
    c_fsfilcnt_t = ctypes.c_uint64
    c_stat_fields = [
        ('st_mode', c_mode_t),
        ('st_dev', c_dev_t),
        ('st_ino', c_ino_t),
        ('st_nlink', c_nlink_t),
        ('st_uid', c_uid_t),
        ('st_gid', c_gid_t),
        ('st_rdev', c_dev_t),
        ('st_atimespec', c_timespec),
        ('st_mtimespec', c_timespec),
        ('st_ctimespec', c_timespec),
        ('st_size', c_off_t),
        ('st_blocks', c_blkcnt_t),
        ('st_blksize', c_blksize_t),
        ('st_flags', ctypes.c_uint32),
        ('st_gen', ctypes.c_uint32),
        ('st_birthtimespec', c_timespec),
    ]
else:
    raise NotImplementedError('%s is not supported.' % _system)

class c_stat(ctypes.Structure):
    _fields_ = c_stat_fields

c_freebsd_fsblkcnt_t = ctypes.c_uint64
c_freebsd_fsfilcnt_t = ctypes.c_uint64
class c_freebsd_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bavail', c_freebsd_fsblkcnt_t),
        ('f_bfree', c_freebsd_fsblkcnt_t),
        ('f_blocks', c_freebsd_fsblkcnt_t),
        ('f_favail', c_freebsd_fsfilcnt_t),
        ('f_ffree', c_freebsd_fsfilcnt_t),
        ('f_files', c_freebsd_fsfilcnt_t),
        ('f_bsize', ctypes.c_ulong),
        ('f_flag', ctypes.c_ulong),
        ('f_frsize', ctypes.c_ulong)]

class c_win_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', c_win_ulong),
        ('f_frsize', c_win_ulong),
        ('f_blocks', c_fsblkcnt_t),
        ('f_bfree', c_fsblkcnt_t),
        ('f_bavail', c_fsblkcnt_t),
        ('f_files', c_fsfilcnt_t),
        ('f_ffree', c_fsfilcnt_t),
        ('f_favail', c_fsfilcnt_t),
        ('f_fsid', c_win_ulong),
        ('f_flag', c_win_ulong),
        ('f_namemax', c_win_ulong)]

class c_std_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', ctypes.c_ulong),
        ('f_frsize', ctypes.c_ulong),
        ('f_blocks', c_fsblkcnt_t),
        ('f_bfree', c_fsblkcnt_t),
        ('f_bavail', c_fsblkcnt_t),
        ('f_files', c_fsfilcnt_t),
        ('f_ffree', c_fsfilcnt_t),
        ('f_favail', c_fsfilcnt_t),
        ('f_fsid', ctypes.c_ulong),
        # ('unused', ctypes.c_int),
        ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong)]

if sys.platform.startswith("freebsd"):
    c_statvfs = c_freebsd_statvfs
elif sys.platform == "win32":
    c_statvfs = c_win_statvfs
else:
    c_statvfs = c_std_statvfs

class fuse_file_info_win(ctypes.Structure):
    _fields_ = [
        ('flags', ctypes.c_int),
        ('fh_old', ctypes.c_int),
        ('writepage', ctypes.c_int),
        ('direct_io', ctypes.c_uint, 1),
        ('keep_cache', ctypes.c_uint, 1),
        ('flush', ctypes.c_uint, 1),
        ('padding', ctypes.c_uint, 29),
        ('fh', ctypes.c_uint64),
        ('lock_owner', ctypes.c_uint64)]

class fuse_file_info_openbsd(ctypes.Structure):
    _fields_ = [
        ('flags', ctypes.c_int32),
        ('fh_old', ctypes.c_uint32),
        ('writepage', ctypes.c_int32),
        ('direct_io', ctypes.c_uint32, 1),
        ('keep_cache', ctypes.c_uint32, 1),
        ('flush', ctypes.c_uint32, 1),
        ('nonseekable', ctypes.c_uint32, 1),
        ('padding', ctypes.c_uint32, 27),
        ('flock_release', ctypes.c_uint32, 1),
        ('fh', ctypes.c_uint64),
        ('lock_owner', ctypes.c_uint64)]

class fuse_file_info_std(ctypes.Structure):
    _fields_ = [
        ('flags', ctypes.c_int),
        ('fh_old', ctypes.c_ulong),
        ('writepage', ctypes.c_int),
        ('direct_io', ctypes.c_uint, 1),
        ('keep_cache', ctypes.c_uint, 1),
        ('flush', ctypes.c_uint, 1),
        ('nonseekable', ctypes.c_uint, 1),
        ('flock_release', ctypes.c_uint, 1),
        ('padding', ctypes.c_uint, 27),
        ('fh', ctypes.c_uint64),
        ('lock_owner', ctypes.c_uint64)]

if sys.platform == 'win32':
    fuse_file_info = fuse_file_info_win
elif sys.platform.startswith("openbsd"):
    fuse_file_info = fuse_file_info_openbsd
else:
    fuse_file_info = fuse_file_info_std

class fuse_context_openbsd(ctypes.Structure):
    _fields_ = [
        ('fuse', ctypes.c_void_p),
        ('uid', c_uid_t),
        ('gid', c_gid_t),
        ('pid', c_pid_t),
        ('private_data', ctypes.c_void_p),
        ('umask', c_mode_t),
    ]

class fuse_context_std(ctypes.Structure):
    _fields_ = [
        ('fuse', ctypes.c_void_p),
        ('uid', c_uid_t),
        ('gid', c_gid_t),
        ('pid', c_pid_t),
        ('private_data', ctypes.c_void_p)]

fuse_context: typing.Type[typing.Any]
if _system == "OpenBSD":
    fuse_context = fuse_context_openbsd
else:
    fuse_context = fuse_context_std

_libfuse.fuse_get_context.restype = ctypes.POINTER(fuse_context)

bmap_ret_t: typing.Type[typing.Any]
extra_fields: FuseFieldsType

if _system == "OpenBSD":
    bmap_ret_t = ctypes.c_uint64
    extra_fields = []
else:
    bmap_ret_t = ctypes.c_ulonglong
    extra_fields = [
        ('flag_nullpath_ok', ctypes.c_uint, 1),
        ('flag_nopath', ctypes.c_uint, 1),
        ('flag_utime_omit_ok', ctypes.c_uint, 1),
        ('flag_reserved', ctypes.c_uint, 29),

        ('ioctl', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p,
            ctypes.POINTER(fuse_file_info), ctypes.c_uint, ctypes.c_void_p)),
    ]

class fuse_operations(ctypes.Structure):
    _core_fields: FuseFieldsType = [
        ('getattr', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(c_stat))),

        ('readlink', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t)),

        ('getdir', ctypes.c_void_p),    # Deprecated, use readdir

        ('mknod', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, c_mode_t, c_dev_t)),

        ('mkdir', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, c_mode_t)),
        ('unlink', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)),
        ('rmdir', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)),

        ('symlink', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)),

        ('rename', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)),

        ('link', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)),

        ('chmod', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, c_mode_t)),

        ('chown', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, c_uid_t, c_gid_t)),

        ('truncate', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, c_off_t)),

        ('utime', ctypes.c_void_p),     # Deprecated, use utimens
        ('open', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info))),

        ('read', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t, c_off_t, ctypes.POINTER(fuse_file_info))),

        ('write', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t, c_off_t, ctypes.POINTER(fuse_file_info))),

        ('statfs', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(c_statvfs))),

        ('flush', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info))),

        ('release', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info))),

        ('fsync', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
            ctypes.POINTER(fuse_file_info))),

        ('setxattr', setxattr_t),
        ('getxattr', getxattr_t),

        ('listxattr', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t)),

        ('removexattr', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)),

        ('opendir', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info))),

        ('readdir', ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_void_p,
            ctypes.CFUNCTYPE(
                ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p,
                ctypes.POINTER(c_stat), c_off_t),
            c_off_t,
            ctypes.POINTER(fuse_file_info))),

        ('releasedir', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info))),

        ('fsyncdir', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
            ctypes.POINTER(fuse_file_info))),

        ('init', ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)),
        ('destroy', ctypes.CFUNCTYPE(None, ctypes.c_void_p)),

        ('access', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_int)),

        ('create', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, c_mode_t,
            ctypes.POINTER(fuse_file_info))),

        ('ftruncate', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, c_off_t,
            ctypes.POINTER(fuse_file_info))),

        ('fgetattr', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(c_stat),
            ctypes.POINTER(fuse_file_info))),

        ('lock', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(fuse_file_info),
            ctypes.c_int, ctypes.c_void_p)),

        ('utimens', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(c_utimbuf))),

        ('bmap', ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t,
            ctypes.POINTER(bmap_ret_t))),
    ]

    _fields_ = _core_fields + extra_fields

class pointer_fix:
    @classmethod
    def __class_getitem__(cls: typing.Type[typing.Self], item: typing.Type[typing.Any]) -> typing.Type[typing.Any]:
        return ctypes.POINTER(item)

if typing.TYPE_CHECKING:
    PointerType = ctypes._Pointer
else:
    PointerType = pointer_fix

if sys.platform.startswith("openbsd"):
    def fuse_main_real(argc: int,
                       argv: PointerType[ctypes.c_char_p],
                       fuse_ops_v: PointerType[fuse_operations],
                       sizeof_fuse_ops: int,
                       ctx_p: ctypes.c_void_p) -> int:
        return _libfuse.fuse_main(argc, argv, fuse_ops_v, ctx_p)
else:
    fuse_main_real =_libfuse.fuse_main_real

def time_of_timespec(ts: c_timespec,
                     use_ns: bool = False) -> float:
    sec = typing.cast(int, ts.tv_sec)
    nsec = typing.cast(int, ts.tv_nsec)
    if use_ns:
        return sec * 10 ** 9 + nsec
    else:
        return sec + nsec / 1E9

def set_st_attrs(st: c_stat,
                 attrs: typing.Dict[str, typing.Any],
                 use_ns: bool = False) -> None:
    for key, val in attrs.items():
        if key in ('st_atime', 'st_mtime', 'st_ctime', 'st_birthtime'):
            timespec = getattr(st, key + 'spec', None)
            if timespec is None:
                continue

            if use_ns:
                timespec.tv_sec, timespec.tv_nsec = divmod(int(val), 10 ** 9)
            else:
                timespec.tv_sec = int(val)
                timespec.tv_nsec = int((val - timespec.tv_sec) * 1E9)
        elif hasattr(st, key):
            setattr(st, key, val)


def fuse_get_context() -> typing.Tuple[int, int, int]:
    'Returns a (uid, gid, pid) tuple'

    ctxp = _libfuse.fuse_get_context()
    ctx = ctxp.contents
    return ctx.uid, ctx.gid, ctx.pid


def fuse_exit() -> None:
    '''
    This will shutdown the FUSE mount and cause the call to FUSE(...) to
    return, similar to sending SIGINT to the process.

    Flags the native FUSE session as terminated and will cause any running FUSE
    event loops to exit on the next opportunity. (see fuse.c::fuse_exit)
    '''
    # OpenBSD doesn't have fuse_exit
    # instead fuse_loop() gracefully catches SIGTERM
    if _system == "OpenBSD":
        os.kill(os.getpid(), SIGTERM)
        return

    fuse_ptr = ctypes.c_void_p(_libfuse.fuse_get_context().contents.fuse)
    _libfuse.fuse_exit(fuse_ptr)

def FuseOSError(errno: int) -> OSError:
    return OSError(errno, os.strerror(errno))

CStatPointer = PointerType[c_stat]

class _PrivateNoSys(Exception): pass

class Operations(ABC):
    '''
    This class should be subclassed and passed as an argument to FUSE on
    initialization. All operations should raise a FuseOSError exception on
    error.

    When in doubt of what an operation should do, check the FUSE header file
    or the corresponding system call man page.
    '''

    @property
    def flag_nopath(self) -> bool:
        return False

    @property
    def flag_nullpath_ok(self) -> bool:
        return False

    @property
    def flag_utime_omit_ok(self) -> bool:
        return False

    def access(self, path: str, amode: int) -> int:
        raise _PrivateNoSys()

    def bmap(self, path: str, blocksize: int, idx: int) -> int:
        raise _PrivateNoSys()

    def chmod(self, path: str, mode: int) -> int:
        raise _PrivateNoSys()

    def chown(self, path: str, uid: int, gid: int) -> int:
        raise _PrivateNoSys()

    def create(self, path: str, mode: int, fi: typing.Optional[fuse_file_info] = None) -> int:
        '''
        When raw_fi is False (default case), fi is None and create should
        return a numerical file handle.

        When raw_fi is True the file handle should be set directly by create
        and return 0.
        '''
        raise _PrivateNoSys()

    def destroy(self, path: str) -> None:
        'Called on filesystem destruction. Path is always /'
        pass

    def flush(self, path: typing.Optional[str], fh: int | fuse_file_info) -> int:
        raise _PrivateNoSys()

    def fsync(self, path: typing.Optional[str], datasync: int, fh: int | fuse_file_info) -> int:
        raise _PrivateNoSys()

    def fsyncdir(self, path: typing.Optional[str], datasync: int, fh: int | fuse_file_info) -> int:
        raise _PrivateNoSys()

    def getattr(self, path: typing.Optional[str], fh: typing.Optional[int | fuse_file_info] = None) -> typing.Dict[str, typing.Any]:
        '''
        Returns a dictionary with keys identical to the stat C structure of
        stat(2).

        st_atime, st_mtime and st_ctime should be floats.

        NOTE: There is an incompatibility between Linux and Mac OS X
        concerning st_nlink of directories. Mac OS X counts all files inside
        the directory, while Linux counts only the subdirectories.
        '''
        raise _PrivateNoSys()

    def getxattr(self, path: str, name: str, position: int = 0) -> bytes:
        raise _PrivateNoSys()

    def init(self, path: str) -> None:
        '''
        Called on filesystem initialization. (Path is always /)

        Use it instead of __init__ if you start threads on initialization.
        '''
        pass

    def ioctl(self, path: typing.Optional[str], cmd: int, arg: int, fip: int | fuse_file_info, flags: int, data: int) -> int:
        raise _PrivateNoSys()

    def link(self, target: str, source: str) -> int:
        'creates a hard link `target -> source` (e.g. ln source target)'
        raise _PrivateNoSys()

    def listxattr(self, path: str) -> typing.List[str]:
        raise _PrivateNoSys()

    def lock(self, path: typing.Optional[str], fip: int | fuse_file_info, cmd: int, lock: int) -> int:
        raise _PrivateNoSys()

    def mkdir(self, path: str, mode: int) -> int:
        raise _PrivateNoSys()

    def mknod(self, path: str, mode: int, dev: int) -> int:
        raise _PrivateNoSys()

    def open(self, path: str, flags_or_fi: int | fuse_file_info) -> int:
        '''
        When raw_fi is False (default case), open should return a numerical
        file handle.

        When raw_fi is True the signature of open becomes:
            open(self, path, fi)

        and the file handle should be set directly.
        '''
        raise _PrivateNoSys()

    def opendir(self, path: str) -> int:
        'Returns a numerical file handle.'
        raise _PrivateNoSys()

    def read(self, path: typing.Optional[str], buf: bytearray | memoryview, offset: int, fh: int | fuse_file_info) -> int:
        'Returns a string containing the data requested.'
        raise _PrivateNoSys()

    def readdir(self,
                path: typing.Optional[str],
                fh: int) -> typing.List[str | typing.Tuple[str, typing.Dict[str, typing.Any], int]]:
        '''
        Can return either a list of names, or a list of (name, attrs, offset)
        tuples. attrs is a dict as in getattr.
        '''
        raise _PrivateNoSys()

    def readlink(self, path: str) -> str:
        raise _PrivateNoSys()

    def release(self, path: typing.Optional[str], fhp: int | fuse_file_info) -> int:
        raise _PrivateNoSys()

    def releasedir(self, path: typing.Optional[str], fh: int) -> int:
        raise _PrivateNoSys()

    def removexattr(self, path: str, name: str) -> int:
        raise _PrivateNoSys()

    def rename(self, old: str, new: str) -> int:
        raise _PrivateNoSys()

    def rmdir(self, path: str) -> int:
        raise _PrivateNoSys()

    def setxattr(self, path: str, name: str, value: bytes, options: int, position: int = 0) -> int:
        raise _PrivateNoSys()

    def statfs(self, path: str) -> typing.Dict[str, typing.Any]:
        '''
        Returns a dictionary with keys identical to the statvfs C structure of
        statvfs(3).

        On Mac OS X f_bsize and f_frsize must be a power of 2
        (minimum 512).
        '''
        raise _PrivateNoSys()

    def symlink(self, target: str, source: str) -> int:
        'creates a symlink `target -> source` (e.g. ln -s source target)'
        raise _PrivateNoSys()

    def truncate(self,
                 path: typing.Optional[str],
                 length: int,
                 fh: typing.Optional[int | fuse_file_info] = None) -> int:
        raise _PrivateNoSys()

    def unlink(self, path: str) -> int:
        raise _PrivateNoSys()

    def utimens(self, path: str, times: typing.Optional[typing.Tuple[float, float]] = None) -> int:
        'Times is a (atime, mtime) tuple. If None use current time.'
        raise _PrivateNoSys()

    def write(self,
              path: typing.Optional[str],
              data: bytes,
              offset: int,
              fhp: int | fuse_file_info) -> int:
        raise _PrivateNoSys()

PyBUF_READ = 0x100
PyBUF_WRITE = 0x200
PyMemoryView_FromMemory_proto = ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.POINTER(ctypes.c_byte), ctypes.c_ssize_t, ctypes.c_int)
PyMemoryView_FromMemory = PyMemoryView_FromMemory_proto(("PyMemoryView_FromMemory", ctypes.pythonapi))

log_mixin = logging.getLogger('fuse.log-mixin')

def log_mixin_wrap(fn: Callable[..., int]) -> Callable[..., int]:
    @functools.wraps(fn)
    def toret(*args: typing.Any) -> int:
        op = fn.__name__
        log_mixin.debug('-> %s %r', op, args)
        ret: str | Exception | int = '[Unhandled Exception]'
        try:
            ret = reti = fn(*args)
            return reti
        except OSError as e:
            ret = e
            raise
        finally:
            log_mixin.debug('<- %s %r', op, ret)
    return toret

class FUSE(object):
    '''
    This class is the lower level interface and should not be subclassed under
    normal use. Its methods are called by fuse.

    Assumes API version 2.6 or later.
    '''

    OPTIONS = (
        ('foreground', '-f'),
        ('debug', '-d'),
        ('nothreads', '-s'),
    )

    __deletable__ = ['operations']

    def __init__(self,
                 operations: Operations,
                 mountpoint: str,
                 debug_logging: bool = False,
                 raw_fi: bool = False,
                 **kwargs: bool | str) -> None:
        '''
        Setting raw_fi to True will cause FUSE to pass the fuse_file_info
        class as is to Operations, instead of just the fh field.

        This gives you access to direct_io, keep_cache, etc.
        '''

        # NB: this used to be in the argument list but mypy didn't like that
        #     for some reason
        encoding = typing.cast(str, kwargs.pop('encoding', 'utf-8'))

        self.operations = operations
        self.raw_fi = raw_fi
        self.encoding = encoding

        self.use_ns = getattr(operations, 'use_ns', False)
        if not self.use_ns:
            warnings.warn(
                'Time as floating point seconds for utimens is deprecated!\n'
                'To enable time as nanoseconds set the property "use_ns" to '
                'True in your operations class or set your fusepy '
                'requirements to <4.',
                DeprecationWarning)

        args = ['fuse']

        args.extend(flag for arg, flag in self.OPTIONS
                    if kwargs.pop(arg, False))

        kwargs.setdefault('fsname', operations.__class__.__name__)
        args.append('-o')
        args.append(','.join(self._normalize_fuse_options(**kwargs)))
        args.append(mountpoint)

        argsb = [arg.encode(encoding) for arg in args]
        argv = (ctypes.c_char_p * len(argsb))(*argsb)

        op_decorator = log_mixin_wrap if debug_logging else (lambda x: x)

        fuse_ops = fuse_operations()
        for ent in fuse_operations._fields_:
            name, prototype = ent[:2]

            check_name = name

            # ftruncate()/fgetattr() are implemented in terms of their
            # non-f-prefixed versions in the operations object
            if check_name in ["ftruncate", "fgetattr"]:
                check_name = check_name[1:]

            val = getattr(operations, check_name, None)
            if val is None:
                continue

            # Function pointer members are tested for using the
            # getattr(operations, name) above but are dynamically
            # invoked using self.operations(name)
            if hasattr(prototype, 'argtypes'):
                if typing.TYPE_CHECKING:
                    prototypef = typing.cast(ctypes._FuncPointer, prototype)
                else:
                    prototypef = prototype
                val = prototypef(partial(self._wrapper, op_decorator(getattr(self, name))))

            setattr(fuse_ops, name, val)

        try:
            old_handler = signal(SIGINT, SIG_DFL)
        except ValueError:
            old_handler = SIG_DFL

        err = fuse_main_real(
            len(argsb), argv, ctypes.pointer(fuse_ops),
            ctypes.sizeof(fuse_ops),
            None)

        try:
            signal(SIGINT, old_handler)
        except ValueError:
            pass

        del self.operations     # Invoke the destructor
        if err:
            raise RuntimeError(err)

    @staticmethod
    def _normalize_fuse_options(**kargs: bool | str) -> Iterator[str]:
        for key, value in kargs.items():
            if isinstance(value, bool):
                if value is True:
                    yield key
            else:
                yield '%s=%s' % (key, value)

    def _wrapper(self, func: Callable[..., int], *args: typing.Any, **kwargs: typing.Any) -> int:
        'Decorator for the methods that follow'

        try:
            if func.__name__ == "init":
                # init may not fail, as its return code is just stored as
                # private_data field of struct fuse_context
                return func(*args, **kwargs) or 0

            else:
                try:
                    return func(*args, **kwargs) or 0
                except _PrivateNoSys:
                    return -errno.ENOSYS
                except OSError as e:
                    if e.errno is not None and e.errno > 0:
                        log.debug(
                            "FUSE operation %s raised a %s, returning errno %s.",
                            func.__name__, type(e), e.errno, exc_info=True)
                        return -e.errno
                    else:
                        log.error(
                            "FUSE operation %s raised an OSError with an invalid "
                            "errno %s, returning errno.EINVAL.",
                            func.__name__, e.errno, exc_info=True)
                        return -errno.EINVAL

                except Exception as e:
                    log.error("Uncaught exception from FUSE operation %s, "
                              "returning errno.EINVAL: %s",
                              func.__name__, e, exc_info=True)
                    return -errno.EINVAL

        except BaseException as e:
            log.critical(
                "Uncaught critical exception from FUSE operation %s, aborting: %s.",
                func.__name__, e, exc_info=True)
            # the raised exception (even SystemExit) will be caught by FUSE
            # potentially causing SIGSEGV, so tell system to stop/interrupt FUSE
            fuse_exit()
            return -errno.EFAULT

    def _decode_optional_path(self, path: typing.Optional[bytes]) -> typing.Optional[str]:
        # NB: this method is intended for fuse operations that
        #     allow the path argument to be NULL,
        #     *not* as a generic path decoding method
        if path is None:
            return None
        return path.decode(self.encoding)

    def getattr(self, path: bytes, buf: PointerType[c_stat]) -> int:
        return self.fgetattr(path, buf, None)

    def readlink(self, path: bytes, buf: PointerType[ctypes.c_byte], bufsize: int) -> int:
        ret = self.operations.readlink(path.decode(self.encoding)) \
                  .encode(self.encoding)

        # copies a string into the given buffer
        # (null terminated and truncated if necessary)
        data = ctypes.create_string_buffer(ret[:bufsize - 1])
        ctypes.memmove(buf, data, len(data))
        return 0

    def mknod(self, path: bytes, mode: int, dev: int) -> int:
        return self.operations.mknod(path.decode(self.encoding), mode, dev)

    def mkdir(self, path: bytes , mode: int) -> int:
        return self.operations.mkdir(path.decode(self.encoding), mode)

    def unlink(self, path: bytes) -> int:
        return self.operations.unlink(path.decode(self.encoding))

    def rmdir(self, path: bytes) -> int:
        return self.operations.rmdir(path.decode(self.encoding))

    def symlink(self, source: bytes, target: bytes) -> int:
        'creates a symlink `target -> source` (e.g. ln -s source target)'

        return self.operations.symlink(target.decode(self.encoding),
                                          source.decode(self.encoding))

    def rename(self, old: bytes, new: bytes) -> int:
        return self.operations.rename(old.decode(self.encoding),
                                         new.decode(self.encoding))

    def link(self, source: bytes, target: bytes) -> int:
        'creates a hard link `target -> source` (e.g. ln source target)'

        return self.operations.link(target.decode(self.encoding),
                                       source.decode(self.encoding))

    def chmod(self, path: bytes, mode: int) -> int:
        return self.operations.chmod(path.decode(self.encoding), mode)

    def chown(self, path: bytes, uid: int, gid: int) -> int:
        # Check if any of the arguments is a -1 that has overflowed
        if c_uid_t(uid + 1).value == 0:
            uid = -1
        if c_gid_t(gid + 1).value == 0:
            gid = -1

        return self.operations.chown(path.decode(self.encoding), uid, gid)

    def truncate(self, path: bytes, length: int) -> int:
        return self.operations.truncate(path.decode(self.encoding), length)

    def open(self, path: bytes, fip: PointerType[fuse_file_info]) -> int:
        fi = fip.contents
        if self.raw_fi:
            return self.operations.open(path.decode(self.encoding), fi)
        else:
            fi.fh = self.operations.open(path.decode(self.encoding),
                                            fi.flags)

            return 0

    def read(self,
             path: typing.Optional[bytes],
             buf: PointerType[ctypes.c_byte],
             size: int,
             offset: int,
             fip: PointerType[fuse_file_info]) -> int:
        if self.raw_fi:
          fh = fip.contents
        else:
          fh = fip.contents.fh

        buf_memview = PyMemoryView_FromMemory(buf, size, PyBUF_WRITE)

        retsize = self.operations.read(self._decode_optional_path(path), buf_memview,
                                      offset, fh)

        assert retsize <= size, \
            'actual amount read %d greater than expected %d' % (retsize, size)

        return retsize

    def write(self,
              path: typing.Optional[bytes],
              buf: PointerType[ctypes.c_byte],
              size: int,
              offset: int,
              fip: PointerType[fuse_file_info]) -> int:
        data = PyMemoryView_FromMemory(buf, size, PyBUF_READ)

        if self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        return self.operations.write(self._decode_optional_path(path), data,
                                        offset, fh)

    def statfs(self, path: bytes, buf: PointerType[c_statvfs]) -> int:
        stv = buf.contents
        attrs = self.operations.statfs(path.decode(self.encoding))
        for key, val in attrs.items():
            if hasattr(stv, key):
                setattr(stv, key, val)

        return 0

    def flush(self, path: typing.Optional[bytes], fip: PointerType[fuse_file_info]) -> int:
        if self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        return self.operations.flush(self._decode_optional_path(path), fh)

    def release(self, path: typing.Optional[bytes], fip: PointerType[fuse_file_info]) -> int:
        if self.raw_fi:
          fh = fip.contents
        else:
          fh = fip.contents.fh

        return self.operations.release(self._decode_optional_path(path), fh)

    def fsync(self, path: typing.Optional[bytes], datasync: int, fip: PointerType[fuse_file_info]) -> int:
        if self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        return self.operations.fsync(self._decode_optional_path(path), datasync,
                                        fh)

    def setxattr(self,
                 path: bytes,
                 name: bytes,
                 value: PointerType[ctypes.c_byte],
                 size: int,
                 options: int, *args: typing.Any) -> int:
        return self.operations.setxattr(path.decode(self.encoding),
                               name.decode(self.encoding),
                               ctypes.string_at(value, size), options, *args)

    def getxattr(self,
                 path: bytes,
                 name: bytes,
                 value: PointerType[ctypes.c_byte],
                 size: int, *args: typing.Any) -> int:
        ret = self.operations.getxattr(path.decode(self.encoding),
                                          name.decode(self.encoding), *args)

        retsize = len(ret)
        # allow size queries
        if not value:
            return retsize

        # do not truncate
        if retsize > size:
            return -errno.ERANGE

        # Does not add trailing 0
        buf = ctypes.create_string_buffer(ret, retsize)
        ctypes.memmove(value, buf, retsize)

        return retsize

    def listxattr(self,
                  path: bytes,
                  namebuf: PointerType[ctypes.c_byte],
                  size: int) -> int:
        attrs = self.operations.listxattr(path.decode(self.encoding)) or ''
        ret = '\x00'.join(attrs).encode(self.encoding)
        if len(ret) > 0:
            ret += '\x00'.encode(self.encoding)

        retsize = len(ret)
        # allow size queries
        if not namebuf:
            return retsize

        # do not truncate
        if retsize > size:
            return -errno.ERANGE

        buf = ctypes.create_string_buffer(ret, retsize)
        ctypes.memmove(namebuf, buf, retsize)

        return retsize

    def removexattr(self, path: bytes, name: bytes) -> int:
        return self.operations.removexattr(path.decode(self.encoding),
                                              name.decode(self.encoding))

    def opendir(self, path: bytes, fip: PointerType[fuse_file_info]) -> int:
        # Ignore raw_fi
        fip.contents.fh = self.operations.opendir(
                                          path.decode(self.encoding))

        return 0

    def readdir(self,
                path: typing.Optional[bytes],
                buf: int,
                filler: Callable[[int, bytes, CStatPointer, int], int],
                offset: int,
                fip: PointerType[fuse_file_info]) -> int:
        # Ignore raw_fi
        for item in self.operations.readdir(self._decode_optional_path(path),
                                               fip.contents.fh):

            if isinstance(item, str):
                name, st, offset = item, None, 0
            else:
                name, attrs, offset = item
                if attrs:
                    st = c_stat()
                    set_st_attrs(st, attrs, use_ns=self.use_ns)
                else:
                    st = None

            # NB: there is no good way to typecheck None or result of byref
            # into PointerType[c_stat] so just manually cast
            stp = typing.cast(CStatPointer, None if st is None else ctypes.byref(st))

            if filler(buf, name.encode(self.encoding), stp, offset) != 0:
                break

        return 0

    def releasedir(self, path: typing.Optional[bytes], fip: PointerType[fuse_file_info]) -> int:
        # Ignore raw_fi
        return self.operations.releasedir(self._decode_optional_path(path),
                                             fip.contents.fh)

    def fsyncdir(self, path: typing.Optional[bytes], datasync: int, fip: PointerType[fuse_file_info]) -> int:
        # Ignore raw_fi
        return self.operations.fsyncdir(self._decode_optional_path(path),
                                           datasync, fip.contents.fh)

    def init(self, conn: int) -> int:
        self.operations.init('/')
        return 0

    def destroy(self, private_data: int) -> None:
        self.operations.destroy('/')

    def access(self, path: bytes, amode: int) -> int:
        return self.operations.access(path.decode(self.encoding), amode)

    def create(self, pathb: bytes, mode: int, fip: PointerType[fuse_file_info]) -> int:
        fi = fip.contents
        path = pathb.decode(self.encoding)

        if self.raw_fi:
            return self.operations.create(path, mode, fi)
        else:
            fi.fh = self.operations.create(path, mode)
            return 0

    def ftruncate(self, path: typing.Optional[bytes], length: int, fip: PointerType[fuse_file_info]) -> int:
        if self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        return self.operations.truncate(self._decode_optional_path(path),
                                           length, fh)

    def fgetattr(self, path: typing.Optional[bytes], buf: PointerType[c_stat], fip: typing.Optional[PointerType[fuse_file_info]]) -> int:
        ctypes.memset(buf, 0, ctypes.sizeof(c_stat))

        st = buf.contents
        if not fip:
            fh = None
        elif self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        attrs = self.operations.getattr(self._decode_optional_path(path), fh)
        set_st_attrs(st, attrs, use_ns=self.use_ns)
        return 0

    def lock(self, path: typing.Optional[bytes], fip: PointerType[fuse_file_info], cmd: int, lock: int) -> int:
        if self.raw_fi:
            fh = fip.contents
        else:
            fh = fip.contents.fh

        return self.operations.lock(self._decode_optional_path(path), fh, cmd,
                                       lock)

    def utimens(self, path: bytes, buf: PointerType[c_utimbuf]) -> int:
        if buf:
            atime = time_of_timespec(buf.contents.actime, use_ns=True)
            mtime = time_of_timespec(buf.contents.modtime, use_ns=True)
            times = (atime, mtime)
        else:
            times = None

        return self.operations.utimens(path.decode(self.encoding), times=times)

    def bmap(self, path: bytes, blocksize: int, idx: int) -> int:
        return self.operations.bmap(path.decode(self.encoding), blocksize,
                                       idx)

    def ioctl(self, path: typing.Optional[bytes], cmd: int, arg: int, fip: PointerType[fuse_file_info], flags: int, data: int) -> int:
        if self.raw_fi:
          fh = fip.contents
        else:
          fh = fip.contents.fh

        return self.operations.ioctl(self._decode_optional_path(path),
            cmd, arg, fh, flags, data)
