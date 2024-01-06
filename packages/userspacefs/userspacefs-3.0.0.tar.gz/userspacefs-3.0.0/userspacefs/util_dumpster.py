# don't abuse this file!

# for the 99.9% of you for which the preceding comment is unclear:

# keep this file small, if there is a theme of utility functions then
# put group them into a separate file

import userspacefs.abc as fsabc

import contextlib
import errno
import io
import itertools
import datetime
import os
import sqlite3
import stat
import threading
import traceback
import typing

from abc import abstractmethod
from collections.abc import Iterator, Sized, Sequence, MutableSequence, Callable

ReadableBuffer = fsabc.ReadableBuffer
WriteableBuffer = fsabc.WriteableBuffer

def datetime_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

def utctimestamp(dt: datetime.datetime) -> float:
    assert dt.tzinfo is None
    return dt.replace(tzinfo=datetime.timezone.utc).timestamp()

def datetime_from_ts(ts: float) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)

def datetime_to_ns(dt: datetime.datetime) -> int:
    return (int(dt.timestamp()) * 1000000 + dt.microsecond) * 1000

class OldStatProtocol(typing.Protocol):
    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @property
    @abstractmethod
    def type(self) -> str:
        ...

    @property
    @abstractmethod
    def mtime(self) -> datetime.datetime:
        ...

    @property
    @abstractmethod
    def ctime(self) -> datetime.datetime:
        ...

class OldDirStatProtocol(OldStatProtocol, typing.Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

class OldDirectoryProtocol(Iterator[OldDirStatProtocol], typing.Protocol):
    @abstractmethod
    def close(self) -> None:
        ...

class NewStat(fsabc.Stat):
    def __init__(self, old_st: OldStatProtocol):
        self._st = old_st

    @property
    def st_size(self) -> int:
        return self._st.size

    @property
    def st_mode(self) -> int:
        if self._st.type == 'directory':
            return stat.S_IFDIR
        else:
            return stat.S_IFREG

    @property
    def st_mtime_ns(self) -> int:
        return datetime_to_ns(self._st.mtime)

    @property
    def st_atime_ns(self) -> int:
        return datetime_to_ns(getattr(self._st, 'atime', datetime_now()))

    @property
    def st_ctime_ns(self) -> int:
        return datetime_to_ns(self._st.ctime)

    @property
    def st_birthtime_ns(self) -> int:
        dt = typing.cast(datetime.datetime, getattr(self._st, 'birthtime'))
        return datetime_to_ns(dt)

    @property
    def st_birthtime(self) -> float:
        return self.st_birthtime_ns / 10e9

    @property
    def x_id(self) -> str:
        return typing.cast(str, getattr(self._st, 'id'))

    @property
    def x_rev(self) -> str:
        return typing.cast(str, getattr(self._st, 'rev'))

    def __repr__(self) -> str:
        return 'NewStat(%r)' % (self._st,)

class NewDirEntry(fsabc.DirEntry):
    def __init__(self, old_dir_entry: OldDirStatProtocol):
        self._de = old_dir_entry

    @property
    def name(self) -> str:
        return self._de.name

    def stat(self) -> NewStat:
        return NewStat(self._de)

    def is_dir(self) -> bool:
        return self._de.type == 'directory'

    def __repr__(self) -> str:
        return 'NewDirEntry(%r)' % (self._de,)

class NewDirectory(fsabc.Directory):
    def __init__(self, old_dir: OldDirectoryProtocol):
        self._dir = old_dir

    def __iter__(self) -> typing.Self:
        return self

    def __next__(self) -> NewDirEntry:
        return NewDirEntry(next(self._dir))

    def close(self) -> None:
        self._dir.close()

class OldStat:
    def __init__(self, new_st: fsabc.Stat):
        self._st = new_st

    @property
    def size(self) -> int:
        return self._st.st_size

    @property
    def type(self) -> str:
        if stat.S_ISDIR(self._st.st_mode):
            return 'directory'
        else:
            return 'file'

    @property
    def mtime(self) -> datetime.datetime:
        return datetime_from_ts(self._st.st_mtime)

    @property
    def ctime(self) -> datetime.datetime:
        return datetime_from_ts(self._st.st_ctime)

    @property
    def atime(self) -> datetime.datetime:
        return datetime_from_ts(self._st.st_atime)

    @property
    def birthtime(self) -> datetime.datetime:
        return datetime_from_ts(getattr(self._st, 'st_birthtime'))

    @property
    def id(self) -> str:
        return typing.cast(str, getattr(self._st, 'x_id'))

    @property
    def rev(self) -> str:
        return typing.cast(str, getattr(self._st, 'x_rev'))

    def __repr__(self) -> str:
        return 'OldStat(%r)' % (self._st,)

class OldDirStat:
    def __init__(self, new_dir_entry: fsabc.DirEntry):
        self._de = new_dir_entry

    @property
    def name(self) -> str:
        return self._de.name

    @property
    def size(self) -> int:
        return OldStat(self._de.stat()).size

    @property
    def type(self) -> str:
        if self._de.is_dir():
            return 'directory'
        else:
            return 'file'

    @property
    def mtime(self) -> datetime.datetime:
        return OldStat(self._de.stat()).mtime

    @property
    def ctime(self) -> datetime.datetime:
        return OldStat(self._de.stat()).ctime

    @property
    def atime(self) -> datetime.datetime:
        return OldStat(self._de.stat()).atime

    @property
    def birthtime(self) -> datetime.datetime:
        return OldStat(self._de.stat()).birthtime

    @property
    def id(self) -> str:
        return OldStat(self._de.stat()).id

    @property
    def rev(self) -> str:
        return OldStat(self._de.stat()).rev

    def __repr__(self) -> str:
        return 'OldDirStat(%r)' % (self._de,)

class OldDirectory:
    def __init__(self, new_dir: fsabc.Directory):
        self._dir = new_dir

    def __iter__(self) -> typing.Self:
        return self

    def __next__(self) -> OldDirStat:
        return OldDirStat(next(self._dir))

    def read(self) -> typing.Optional[OldDirStat]:
        try:
            return next(self)
        except StopIteration:
            return None

    def readmany(self, size: typing.Optional[int] = None) -> typing.List[OldDirStat]:
        if size is None:
            return list(self)
        else:
            return list(itertools.islice(self, size))

    def close(self) -> None:
        self._dir.close()

class IterableDirectory(Iterator[OldDirStatProtocol]):
    def read(self) -> typing.Optional[OldDirStatProtocol]:
        try:
            return next(self)
        except StopIteration:
            return None

    def readmany(self, size: typing.Optional[int] = None) -> typing.List[OldDirStatProtocol]:
        if size is None:
            return list(self)
        else:
            return list(itertools.islice(self, size))

class PositionIO(io.RawIOBase):
    def __init__(self) -> None:
        self._offset_lock = threading.Lock()
        self._offset = 0

    def read(self, size: int = -1) -> bytes:
        ret = super(PositionIO, self).read(size)
        assert ret is not None
        return ret

    def pwrite(self, buf: ReadableBuffer, offset: int) -> int:
        raise NotImplementedError()

    def ptruncate(self, offset: int) -> int:
        raise io.UnsupportedOperation()

    def readinto(self, ibuf: WriteableBuffer) -> int:
        with self._offset_lock:
            amt = self.preadinto(ibuf, self._offset)
            self._offset += amt
            return amt

    def pread(self, size: int, offset: int) -> bytes:
        buf = bytearray(size)
        amt = self.preadinto(buf, offset)
        return bytes(memoryview(buf)[:amt])

    def preadinto(self, buf_: WriteableBuffer, offset: int) -> int:
        raise NotImplementedError()

    def write(self, buf: ReadableBuffer) -> int:
        with self._offset_lock:
            ret = self.pwrite(buf, self._offset)
            self._offset += ret
            return ret

    def seek(self, amt: int, whence: int = 0) -> int:
        if not hasattr(self, '_file_length'):
            raise io.UnsupportedOperation()

        with self._offset_lock:
            if whence == io.SEEK_SET:
                self._offset = amt
            elif whence == io.SEEK_CUR:
                self._offset += amt
            elif whence == io.SEEK_END:
                self._offset = self._file_length() + amt
            else:
                raise OSError(errno.EINVAL, os.strerror(errno.EINVAL))
            return self._offset

    def truncate(self, size: int | None = None) -> int:
        if size is not None:
            return self.ptruncate(size)
        with self._offset_lock:
            return self.ptruncate(self._offset)

    def seekable(self) -> bool:
        return hasattr(self, '_file_length')

@contextlib.contextmanager
def null_context() -> Iterator[None]:
    yield

class quick_container(object):
    def __init__(self, **kw: typing.Any):
        self._fields: Sequence[str]
        self._fields = []
        for (k, v) in kw.items():
            setattr(self, k, v)
            self._fields.append(k)
        self._fields = tuple(self._fields)

    def __repr__(self) -> str:
        return 'quick_container(' + ','.join("%s=%r" % (k, getattr(self, k)) for k in self._fields) + ')'

class Closeable(typing.Protocol):
    @abstractmethod
    def close(self) -> None:
        ...

ConnT = typing.TypeVar('ConnT', bound=Closeable, covariant=True)

class ConnPool(typing.Generic[ConnT]):
    def __init__(self, create_fn: Callable[[], ConnT]):
        self._create_fn = create_fn
        self._conns: typing.List[ConnT] = []
        self._cond = threading.Condition()
        self._total_conns = 0
        self._closed = False
        self._stack_closed_location: typing.Optional[str] = None

    @contextlib.contextmanager
    def get_conn(self) -> Iterator[ConnT]:
        conn = None
        try:
            with self._cond:
                if self._closed:
                    raise Exception("Closed! (at %s)" % (self._stack_closed_location,))

                if not self._conns:
                    conn = self._create_fn()
                    self._total_conns += 1
                else:
                    conn = self._conns.pop()
            assert conn is not None
            yield conn
        except:
            if conn is not None:
                # do this first
                with self._cond:
                    self._total_conns -= 1
                    self._cond.notify_all()
                conn.close()
            raise
        else:
            with self._cond:
                self._conns.append(conn)
                self._cond.notify_all()

    def close(self) -> None:
        with self._cond:
            if self._closed:
                return

            self._closed = True
            self._stack_closed_location = ''.join(traceback.format_stack())

            while self._total_conns != len(self._conns):
                self._cond.wait()

        for conn in self._conns:
            conn.close()

class SharedLock(object):
    def __init__(self) -> None:
        self.cond = threading.Condition()
        self.readers = 0
        self.want_write = 0
        self.writers = 0

    def _rep(self) -> bool:
        if self.writers > 1 or self.writers < 0:
            return False

        if self.want_write < self.writers:
            return False

        if self.writers and self.readers:
            return False

        return True

    def acquire(self) -> None:
        with self.cond:
            assert self._rep()
            self.want_write += 1
            while self.readers or self.writers:
                self.cond.wait()
            self.writers += 1
            assert self._rep()

    def release(self) -> None:
        with self.cond:
            assert self._rep()
            self.writers -= 1
            self.want_write -= 1
            self.cond.notify_all()
            assert self._rep()

    def acquire_shared(self) -> None:
        with self.cond:
            assert self._rep()
            while self.want_write or self.writers:
                self.cond.wait()
            self.readers += 1
            assert self._rep()

    def release_shared(self) -> None:
        with self.cond:
            assert self._rep()
            self.readers -= 1
            self.cond.notify_all()
            assert self._rep()

    @contextlib.contextmanager
    def shared_context(self) -> Iterator[None]:
        self.acquire_shared()
        try:
            yield
        finally:
            self.release_shared()

    def __enter__(self) -> None:
        self.acquire()

    def __exit__(self, *n: typing.Any) -> None:
        self.release()

@contextlib.contextmanager
def trans(conn: sqlite3.Connection, lock: typing.Optional[SharedLock], is_exclusive: bool = False) -> Iterator[sqlite3.Connection]:
    # NB: This exists because pysqlite will not start a transaction
    # until it sees a DML statement. This sucks if we start a transaction
    # with a SELECT statement.
    ctx: contextlib.AbstractContextManager[None]
    if lock is None:
        ctx = null_context()
    elif is_exclusive:
        ctx = lock
    else:
        ctx = lock.shared_context()
    with ctx:
        begin_stmt = "BEGIN IMMEDIATE" if is_exclusive else "BEGIN DEFERRED"
        iso = conn.isolation_level
        conn.isolation_level = None
        try:
            conn.execute(begin_stmt)
            with conn:
                yield conn
        finally:
            conn.isolation_level = iso
