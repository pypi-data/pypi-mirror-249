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

from userspacefs import simple_main_from_argv

import datetime
import io
import os
import sys
import time
import typing

from collections.abc import Callable, Sequence
from pathlib import PurePath as Path

# NB: need to correct readinto signature of io.FileIO
class File(io.FileIO):
    def readinto(self, __buffer: fsabc.WriteableBuffer) -> int:
        a = super(File, self).readinto(__buffer)
        assert a is not None
        return a

class FileSystem(fsabc.FileSystemG[Path, File]):
    def __init__(self, root: str):
        self._root = Path(root)

    def create_path(self, *parts: str) -> Path:
        return self._root.joinpath(*parts)

    def fstat(self, file: File) -> os.stat_result:
        return os.fstat(file.fileno())

    def close(self) -> None:
        pass

    def fsync(self, file: File) -> None:
        return os.fsync(file.fileno())

    def mkdir(self, path: Path) -> None:
        return os.mkdir(path)

    def open(self, path: Path, mode: int) -> File:
        return typing.cast(
            File,
            os.fdopen(os.open(path, mode), "r+b", buffering=0),
        )

    def open_directory(self, path: Path) -> fsabc.Directory:
        return os.scandir(path)

    def preadinto(self, file: File, buf: fsabc.Buffer, offset: int) -> int:
        if hasattr(os, 'preadv'):
            return os.preadv(file.fileno(), [buf], offset)
        else:
            with memoryview(buf) as mbuf:
                # TODO: Windows support
                data = os.pread(file.fileno(), len(mbuf), offset)
                mbuf[:len(data)] = data
                return len(data)

    def pwrite(self, file: File, data: fsabc.Buffer, offset: int) -> int:
        return os.pwrite(file.fileno(), data, offset)

    def replace(self, source: Path, dest: Path) -> None:
        os.replace(source, dest)

    def rmdir(self, path: Path) -> None:
        os.rmdir(path)

    def stat(self, path: Path) -> os.stat_result:
        return os.stat(path)

    def statvfs(self) -> fsabc.StatVFS:
        # TODO: Windows support
        return os.statvfs(self._root)

    def unlink(self, path: Path) -> None:
        os.unlink(path)

    def futimes(self, file: File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        # TODO: Windows support
        os.utime(file.fileno(), times=times)

def _make_fs(args: typing.Dict[str, typing.Any]) -> FileSystem:
    return FileSystem(os.getcwd())

def main(argv: typing.Optional[Sequence[str]] = None) -> int:
    return simple_main_from_argv("stdlibfs", ("userspacefs.stdlibfs._make_fs", {}), argv=argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
