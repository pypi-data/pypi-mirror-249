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

import itertools
import typing

from collections.abc import Sequence, Callable, Iterable

import userspacefs.abc as fsabc

def is_parent(path_a: fsabc.Path, path_b: fsabc.Path) -> bool:
    return path_a in path_b.parents

# NB: this acts like a pathlib PurePath object
class Path(object):
    def __init__(self, compsi: Iterable[str], fn_norm: typing.Optional[Callable[[str], str]] = None):
        comps = tuple(compsi)
        assert all(type(comp) is str for comp in comps)
        self._comps = comps
        if fn_norm is None:
            fn_norm = lambda x: x
        self._fn_norm = fn_norm

    @classmethod
    def root_path(cls: typing.Type[typing.Self], fn_norm: typing.Optional[Callable[[str], str]] = None) -> typing.Self:
        return cls([], fn_norm=fn_norm)

    @classmethod
    def parse_path(cls: typing.Type[typing.Self], p: str, fn_norm: typing.Optional[Callable[[str], str]] = None) -> typing.Self:
        root = cls.root_path(fn_norm=fn_norm)
        if p == "/":
            return root
        return root.joinpath(*p[1:].split("/"))

    def joinpath(self, *comps: str) -> typing.Self:
        assert all(a for a in comps), "empty path components are  not allowed!"
        return self.__class__(itertools.chain(self._comps, comps),
                              fn_norm=self._fn_norm)

    @property
    def parts(self) -> tuple[str]:
        return typing.cast(typing.Tuple[str], tuple(itertools.chain(('/',), self._comps)))

    # NB: This is probably an evil abuse of the '/' operator
    def __truediv__(self, elt: str) -> typing.Self:
        return self.joinpath(elt)

    def __repr__(self) -> str:
        return 'Path' + str(self)

    def _norm(self) -> typing.Sequence[str]:
        return tuple(map(self._fn_norm, self._comps))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Path):
            return False
        return self._norm() == other._norm()

    def __hash__(self) -> int:
        return hash(self._norm())

    def __str__(self) -> str:
        return '/' + '/'.join(self._comps)

    @property
    def name(self) -> str:
        if not self._comps: return ''
        return self._comps[-1]

    @property
    def parent(self) -> typing.Self:
        if not self._comps: return self
        return type(self)(self._comps[:-1], fn_norm=self._fn_norm)

    @property
    def parents(self) -> typing.List[typing.Self]:
        ret = []
        p = self
        while True:
            n = p.parent
            if p == n:
                break
            ret.append(n)
            p = n
        return ret

    def normed(self) -> typing.Self:
        return type(self)(self._norm(), fn_norm=self._fn_norm)

    def with_name(self, new_name: str) -> typing.Self:
        return self.parent / new_name
