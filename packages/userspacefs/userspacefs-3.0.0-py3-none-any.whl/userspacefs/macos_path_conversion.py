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

# macOS SMB client converts illegal Windows characters like so:
#   0x01-0x1F       0xF001-0xF01F
#  "               0xF020
#  *               0xF021
#  /               0xF022
#  <               0xF023
#  >               0xF024
#  ?               0xF025
#  \               0xF026
#  |               0xF027

import userspacefs.abc as fsabc

from typing_extensions import Buffer

import datetime
import typing

from collections.abc import Callable

REPLACE_MAP = {
    0xf020: ord('"'),
    0xf021: ord('*'),
    0xf022: ord('/'),
    0xf023: ord('<'),
    0xf024: ord('>'),
    0xf025: ord('?'),
    0xf026: ord('\\'),
    0xf027: ord('|'),
}

for i in range(0x1, 0x20):
    REPLACE_MAP[0xF000 | i] = i

class FileSystem(fsabc.FileSystem):
    def __init__(self, backing_fs: fsabc.FileSystem):
        self._sub = backing_fs

        if hasattr(self._sub, 'x_create_watch'):
            self.x_create_watch = self._x_create_watch

    def _convert_path(self, path: fsabc.Path) -> fsabc.Path:
        return self._sub.create_path(*[p.translate(REPLACE_MAP) for p in path.parts[1:]])

    def open(self, path: fsabc.Path, mode: int) -> fsabc.File:
        return self._sub.open(self._convert_path(path), mode)

    def open_directory(self, path: fsabc.Path) -> fsabc.Directory:
        return self._sub.open_directory(self._convert_path(path))

    def stat(self, path: fsabc.Path) -> fsabc.Stat:
        return self._sub.stat(self._convert_path(path))

    def unlink(self, path: fsabc.Path) -> None:
        return self._sub.unlink(self._convert_path(path))

    def mkdir(self, path: fsabc.Path) -> None:
        return self._sub.mkdir(self._convert_path(path))

    def rmdir(self, path: fsabc.Path) -> None:
        return self._sub.rmdir(self._convert_path(path))

    def replace(self, old_path: fsabc.Path, new_path: fsabc.Path) -> None:
        return self._sub.replace(self._convert_path(old_path),
                                 self._convert_path(new_path))

    def close(self) -> None:
        return self._sub.close()

    def create_path(self, *parts: str) -> fsabc.Path:
        return self._sub.create_path(*parts)

    def _x_create_watch(self, cb: Callable[[fsabc.ChangeList], None],
                        dir_handle: fsabc.File, completion_filter: int, watch_tree: bool) -> Callable[[], None]:
        sub = typing.cast(fsabc.CreateWatchExt, self._sub)
        return sub.x_create_watch(cb, dir_handle, completion_filter, watch_tree)

    def fstat(self, file: fsabc.File) -> fsabc.Stat:
        return self._sub.fstat(file)

    def fsync(self, file: fsabc.File) -> None:
        return self._sub.fsync(file)

    def preadinto(self, file: fsabc.File, buf: Buffer, offset: int) -> int:
        return self._sub.preadinto(file, buf, offset)

    def pwrite(self, file: fsabc.File, data: Buffer, offset: int) -> int:
        return self._sub.pwrite(file, data, offset)

    def statvfs(self) -> fsabc.StatVFS:
        return self._sub.statvfs()

    def futimes(self, file: fsabc.File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        return self._sub.futimes(file, times=times)
