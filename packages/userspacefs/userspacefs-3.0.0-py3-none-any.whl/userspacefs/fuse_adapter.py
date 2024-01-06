#!/usr/bin/env python3

# This file is part of userspacefs.

# userspacefs is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# userspacefs is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with userspacefs.  If not, see <http://www.gnu.org/licenses/>.

import contextlib
import datetime
import errno
import itertools
import logging
import os
import random
import threading
import typing
import stat
import sys

from collections.abc import Callable

from userspacefs.abc import FileSystem, Path, File, Stat, Directory
from userspacefs.fusepy import FUSE, fuse_file_info, Operations
from userspacefs.util_dumpster import datetime_from_ts

log = logging.getLogger(__name__)

def check_mode(mode: int) -> None:
    if ((stat.S_IFCHR | stat.S_IFBLK | stat.S_IFIFO | stat.S_IFLNK | stat.S_IFSOCK) & mode) == (stat.S_IFCHR | stat.S_IFBLK | stat.S_IFIFO | stat.S_IFLNK | stat.S_IFSOCK):
        raise OSError(errno.EPERM, os.strerror(errno.EPERM))

class FUSEAdapter(Operations):
    flag_nopath = True

    def __init__(self, create_fs: Callable[[], FileSystem], on_init: typing.Optional[Callable[[], None]] = None) -> None:
        self._create_fs = create_fs
        self._fh_to_file: typing.Dict[int, File] = {}
        self._fh_to_dir: typing.Dict[int, Directory] = {}
        self._lock = threading.Lock()
        self._on_init = on_init
        self._fs: typing.Optional[FileSystem] = None

    def _get_unused(self, d: typing.Dict[int, typing.Any]) -> int:
        while True:
            r = random.randint(0, 2 ** 32 - 1)
            if r not in d:
                break
        return r

    def _save_file(self, f: File) -> int:
        with self._lock:
            r = self._get_unused(self._fh_to_file)
            self._fh_to_file[r] = f
            return r

    def _delete_file(self, fh: int) -> File:
        with self._lock:
            return self._fh_to_file.pop(fh)

    def _save_dir(self, f: Directory) -> int:
        with self._lock:
            r = self._get_unused(self._fh_to_dir)
            self._fh_to_dir[r] = f
            return r

    def _delete_dir(self, fh: int) -> Directory:
        with self._lock:
            return self._fh_to_dir.pop(fh)

    def _conv_path(self, path: str) -> Path:
        assert self._fs is not None
        toret = self._fs.create_path()
        if path == '/':
            return toret
        return toret.joinpath(*path[1:].split('/'))

    def _fs_stat_to_fuse_attrs(self, st: Stat) -> typing.Dict[str, typing.Any]:
        toret = {}

        toret['st_birthtime'] = getattr(st, "st_birthtime", 0)
        toret['st_mtime'] = getattr(st, "st_mtime", toret['st_birthtime'])
        toret['st_ctime'] = getattr(st, "st_ctime", toret['st_mtime'])
        toret['st_atime'] = getattr(st, "st_atime", toret['st_ctime'])

        toret['st_size'] = st.st_size

        # NB: only the type bits apply, not the permission bits
        toret['st_mode'] = stat.S_IFMT(st.st_mode) | 0o777

        # NB: st_nlink on directories is really inconsistent across filesystems
        #     and OSes. it arguably doesn't matter at all but we set it to
        #     non-zero just in case
        toret['st_nlink'] = 1
        toret['st_uid'] = os.getuid()
        toret['st_gid'] = os.getgid()

        return toret

    def init(self, _: str) -> None:
        if self._on_init is not None:
            self._on_init()
        self._fs = self._create_fs()

    def destroy(self, _: str) -> None:
        if self._fs is not None:
            self._fs.close()
            self._fs = None

    def getattr(self, path: typing.Optional[str], fh: typing.Optional[int | fuse_file_info] = None) -> typing.Dict[str, typing.Any]:
        assert self._fs is not None
        if fh is not None:
            assert isinstance(fh, fuse_file_info)
            fhp = fh.fh
            if fhp not in self._fh_to_file:
                raise Exception("Fuse passed us invalid file handle!: %r" % (fhp,))
            st = self._fs.fstat(self._fh_to_file[fhp])
        else:
            assert path is not None
            st = self._fs.stat(self._conv_path(path))
        return self._fs_stat_to_fuse_attrs(st)

    def mknod(self, path: str, mode: int, dev: int) -> int:
        assert self._fs is not None
        # Not all fuse implementations call create()
        check_mode(mode)
        self._fs.open(self._conv_path(path),
                      os.O_WRONLY | os.O_CREAT).close()
        return 0

    def create(self, path: str , mode: int, fi: typing.Optional[fuse_file_info] = None) -> int:
        assert self._fs is not None
        assert fi is not None
        check_mode(mode)
        fi.fh = self._save_file(self._fs.open(self._conv_path(path), fi.flags))
        return 0

    def open(self, path: str, fi: int | fuse_file_info) -> int:
        assert self._fs is not None
        assert isinstance(fi, fuse_file_info)
        fi.fh = self._save_file(self._fs.open(self._conv_path(path), fi.flags))
        return 0

    def read(self, path: typing.Optional[str], buf: bytearray | memoryview, offset: int, fhp: int | fuse_file_info) -> int:
        assert self._fs is not None
        assert isinstance(fhp, fuse_file_info)
        fh = fhp.fh
        f = self._fh_to_file[fh]
        return self._fs.preadinto(f, buf, offset)

    def write(self, path: typing.Optional[str], data: bytes, offset: int, fhp: int | fuse_file_info) -> int:
        assert self._fs is not None
        assert isinstance(fhp, fuse_file_info)
        fh = fhp.fh
        f = self._fh_to_file[fh]
        return self._fs.pwrite(f, data, offset)

    def truncate(self, path: typing.Optional[str], length: int, fh: typing.Optional[int | fuse_file_info] = None) -> int:
        assert self._fs is not None
        if fh is None:
            # TODO: add truncate() call to FS interface
            assert path is not None
            with contextlib.closing(self._fs.open(self._conv_path(path), os.O_WRONLY)) as f:
                f.truncate(length)
        else:
            assert isinstance(fh, fuse_file_info)
            f = self._fh_to_file[fh.fh]
            f.truncate(length)
        return 0

    def fsync(self, path: typing.Optional[str], datasync: int, fhp: int | fuse_file_info) -> int:
        assert self._fs is not None
        assert isinstance(fhp, fuse_file_info)
        fh = fhp.fh
        self._fs.fsync(self._fh_to_file[fh])
        return 0

    def release(self, path: typing.Optional[str], fhp: int | fuse_file_info) -> int:
        assert isinstance(fhp, fuse_file_info)
        fh = fhp.fh
        self._delete_file(fh).close()
        return 0

    def opendir(self, path: str) -> int:
        assert self._fs is not None
        return self._save_dir(self._fs.open_directory(self._conv_path(path)))

    def readdir(self, path: typing.Optional[str], fh: int) -> typing.List[str | typing.Tuple[str, typing.Dict[str, typing.Any], int]]:
        # TODO: pyfuse doesn't expose a better interface for large directories
        f = self._fh_to_dir[fh]
        return list(itertools.chain(['.', '..'], map(lambda x: (x.name, self._fs_stat_to_fuse_attrs(x.stat()), 0), f)))

    def releasedir(self, path: typing.Optional[str], fh: int) -> int:
        # NB: fusepy ignores raw_fi in this method for some reason
        self._delete_dir(fh).close()
        return 0

    def unlink(self, path: str) -> int:
        assert self._fs is not None
        self._fs.unlink(self._conv_path(path))
        return 0

    def mkdir(self, path: str, mode: int) -> int:
        assert self._fs is not None
        self._fs.mkdir(self._conv_path(path))
        return 0

    def rmdir(self, path: str) -> int:
        assert self._fs is not None
        self._fs.rmdir(self._conv_path(path))
        return 0

    def rename(self, oldpath: str, newpath: str) -> int:
        assert self._fs is not None
        oldpath_ = self._conv_path(oldpath)
        newpath_ = self._conv_path(newpath)
        self._fs.replace(oldpath_, newpath_)
        return 0

    def chmod(self, path: str, mode: int) -> int:
        return 0

    def utimens(self, path: str, times: typing.Optional[typing.Tuple[float, float]] = None) -> int:
        assert self._fs is not None

        with contextlib.closing(self._fs.open(self._conv_path(path), os.O_RDONLY)) as f:
            self._fs.futimes(f, times=times)
        return 0

    def statfs(self, _: str) -> typing.Dict[str, typing.Any]:
        assert self._fs is not None
        vfs = self._fs.statvfs()
        toret = {}
        for n in ['f_bavail', 'f_blocks', 'f_frsize']:
            toret[n] = getattr(vfs, n)

        toret['f_namemax'] = getattr(vfs, 'f_namemax', 255)
        toret['f_bfree'] = toret['f_bavail']
        toret['f_bsize'] = toret['f_frsize']

        return toret

def run_fuse_mount(create_fs: Callable[[], FileSystem],
                   mount_point: str,
                   foreground: bool = False,
                   display_name: typing.Optional[str] = None,
                   on_init: typing.Optional[Callable[[], None]] = None,
                   **kw: bool | str) -> None:
    if display_name is None:
        raise Exception("need display name argument!")
    if sys.platform == 'darwin':
        kw.setdefault('volname', display_name)
    kw.setdefault('fsname', display_name)
    FUSE(FUSEAdapter(create_fs, on_init=on_init),
         mount_point, foreground=foreground, hard_remove=True,
         debug_logging=True,
         default_permissions=True,
         raw_fi=True,
         **kw)
