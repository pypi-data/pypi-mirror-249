import typing_extensions

import datetime
import itertools
import typing

from collections.abc import Iterator, Sequence, Callable
from abc import ABC, abstractmethod
from io import RawIOBase

Buffer = typing_extensions.Buffer

if typing.TYPE_CHECKING:
    import _typeshed
    WriteableBuffer = _typeshed.WriteableBuffer
    ReadableBuffer = _typeshed.ReadableBuffer
else:
    WriteableBuffer = Buffer
    ReadableBuffer = Buffer

class Change(typing.Protocol):
    @property
    def action(self) -> str:
        raise NotImplementedError()

    @property
    def path(self) -> typing.Sequence[str]:
        raise NotImplementedError()

ChangeList = str | typing.Sequence[Change]

# Stat mimics os.stat_result
class Stat(typing.Protocol):
    @property
    @abstractmethod
    def st_size(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def st_mode(self) -> int:
        raise NotImplementedError()

    @property
    def st_mtime(self) -> float:
        return self.st_mtime_ns / 1e9

    @property
    def st_atime(self) -> float:
        return self.st_atime_ns / 1e9

    @property
    def st_ctime(self) -> float:
        return self.st_ctime_ns / 1e9

    @property
    @abstractmethod
    def st_mtime_ns(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def st_atime_ns(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def st_ctime_ns(self) -> int:
        raise NotImplementedError()

# DirEntry mimics os.DirEntry
class DirEntry(typing.Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def stat(self) -> Stat:
        raise NotImplementedError()

    @abstractmethod
    def is_dir(self) -> bool:
        raise NotImplementedError()

# File mimics io.FileIO
# It's similar to RawIOBase except we never return None for readinto/write/read
class File(typing.Protocol):
    @abstractmethod
    def readinto(self, ibuf: WriteableBuffer) -> int:
        raise NotImplementedError()

    @abstractmethod
    def write(self, buf: ReadableBuffer) -> int:
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def truncate(self, size: typing.Optional[int] = None) -> int:
        raise NotImplementedError()

    def __enter__(self) -> typing.Self:
        return self

    def __exit__(self, *n: typing.Any) -> None:
        return self.close()

    @abstractmethod
    def read(self, size: int = -1) -> bytes | bytearray:
        raise NotImplementedError()

# Path mimics pathlib.Path
class Path(typing.Protocol):
    @abstractmethod
    def joinpath(self, *args: str) -> typing.Self:
        raise NotImplementedError()

    # NB: This is probably an evil abuse of the '/' operator
    def __truediv__(self, elt: str) -> typing.Self:
        return self.joinpath(elt)

    @property
    @abstractmethod
    def parts(self) -> Sequence[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def parents(self) -> Sequence[typing.Self]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def parent(self) -> typing.Self:
        raise NotImplementedError()

# mimics os.statvfs() result
class StatVFS(typing.Protocol):
    @property
    @abstractmethod
    def f_bavail(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def f_blocks(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def f_frsize(self) -> int:
        raise NotImplementedError()

# mimics os.scandir() result
class Directory(Iterator[DirEntry], typing.Protocol):
    def __enter__(self) -> typing.Self:
        return self

    def __exit__(self, *n: typing.Any) -> None:
        return self.close()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

PathT = typing.TypeVar('PathT', bound=Path)
FileT = typing.TypeVar('FileT', bound=File)

class FileSystemG(typing.Protocol[PathT, FileT]):
    @abstractmethod
    def create_path(self, *parts: str) -> PathT:
        raise NotImplementedError()

    @abstractmethod
    def fstat(self, file: FileT) -> Stat:
        raise NotImplementedError()

    @abstractmethod
    def stat(self, path: PathT) -> Stat:
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def open(self, path: PathT, flags: int) -> FileT:
        raise NotImplementedError()

    @abstractmethod
    def preadinto(self, file: FileT, buf: Buffer, offset: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def pwrite(self, file: FileT, data: Buffer, offset: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def fsync(self, file: FileT) -> None:
        raise NotImplementedError()

    @abstractmethod
    def open_directory(self, path: PathT) -> Directory:
        raise NotImplementedError()

    @abstractmethod
    def unlink(self, path: PathT) -> None:
        raise NotImplementedError()

    @abstractmethod
    def mkdir(self, path: PathT) -> None:
        raise NotImplementedError()

    @abstractmethod
    def rmdir(self, path: PathT) -> None:
        raise NotImplementedError()

    @abstractmethod
    def replace(self, oldpath: PathT, newpath: PathT) -> None:
        raise NotImplementedError()

    @abstractmethod
    def statvfs(self) -> StatVFS:
        raise NotImplementedError()

    @abstractmethod
    def futimes(self, file: FileT,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        raise NotImplementedError()

FileSystem = FileSystemG[Path, File]

def safe_cast_file_system(fs: FileSystemG[PathT, FileT]) -> FileSystem:
    return typing.cast(FileSystem, fs)

PathTCov = typing.TypeVar('PathTCov', bound=Path, covariant=True)
FileTCov = typing.TypeVar('FileTCov', bound=File, covariant=True)

@typing.runtime_checkable
class CreateWatchExtG(typing.Protocol[PathTCov, FileTCov]):
    @abstractmethod
    def x_create_watch(self, cb: Callable[[ChangeList], None],
                       dir_handle: FileT, completion_filter: int, watch_tree: bool) -> Callable[[], None]:
        raise NotImplementedError()

CreateWatchExt = CreateWatchExtG[Path, File]
