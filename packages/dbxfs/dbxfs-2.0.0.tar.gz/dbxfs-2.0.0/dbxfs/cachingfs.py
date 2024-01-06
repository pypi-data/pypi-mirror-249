#!/usr/bin/env python3

# This file is part of dbxfs.

# dbxfs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# dbxfs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with dbxfs.  If not, see <http://www.gnu.org/licenses/>.

import _sqlite3 # type: ignore
import base64
import collections
import contextlib
import ctypes
import datetime
import errno
import enum
import functools
import io
import itertools
import json
import logging
import os
import queue
import re
import tempfile
import threading
import traceback
import shutil
import sqlite3
import sys
import time
import typing
import weakref

from abc import abstractmethod
from collections.abc import Mapping, Callable, Sequence

import userspacefs.abc as fsabc
from userspacefs.util_dumpster import PositionIO, null_context, quick_container, IterableDirectory, NewStat, NewDirectory, OldStat, OldDirectory, OldStatProtocol, datetime_now
from userspacefs.path_common import Path

from dbxfs.util_dumpster import ConnPool, SharedLock, trans

import dropbox # type: ignore

log = logging.getLogger(__name__)

def aware_timestamp(dt):
    assert dt.tzinfo is not None
    return dt.timestamp()

if not hasattr(os, 'O_ACCMODE'):
    O_ACCMODE = 0x3
    for accmode in (os.O_RDONLY, os.O_WRONLY, os.O_RDWR):
        assert (O_ACCMODE & accmode) == accmode
else:
    O_ACCMODE = os.O_ACCMODE

# NB: dynamic 'stat' object for attr_merge
class Foo(object): pass

class attr_merge(object):
    def __init__(self, *n):
        attrs = set()
        for obj in n:
            for name in obj.attrs:
                setattr(self, name, getattr(obj, name))
                attrs.add(name)
        self.attrs = list(attrs)

    def _replace(self, **kw):
        tomerge = Foo()
        for (k, v) in kw.items():
            setattr(tomerge, k, v)
        tomerge.attrs = list(kw)
        return attr_merge(self, tomerge)

    def __repr__(self):
        return 'attr_merge(' + ', '.join('%s=%r' % (k, getattr(self, k)) for k in self.attrs) + ')'

Name = collections.namedtuple('Name', ['name', 'attrs'])
def md_plus_name(name, md):
    return attr_merge(Name(name, attrs=['name']), md)

REQUIRED_ATTRS = ["mtime", "type", "size", "id", "ctime", "rev"]
Stat = collections.namedtuple("Stat", ["mtime", "type", "size", "id", "ctime", "rev", "attrs"])

class OldStatProtocolWithExtra(OldStatProtocol, typing.Protocol):
    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @property
    @abstractmethod
    def rev(self) -> str:
        ...

def stat_to_json(obj: OldStatProtocolWithExtra) -> str:
    toret = {}
    for name in REQUIRED_ATTRS:
        elt = getattr(obj, name, None)
        if elt is None: continue
        if name in ("mtime", "ctime"):
            elt = aware_timestamp(elt)
        toret[name] = elt
    return json.dumps(toret)


def json_to_stat(str_: str) -> Stat:
    info = json.loads(str_)
    for name in REQUIRED_ATTRS:
        val: typing.Optional[typing.Any] = info.get(name)
        if val is None:
            info[name] = val
        elif name in ("mtime", "ctime"):
            val = datetime.datetime.fromtimestamp(val, tz=datetime.timezone.utc)
            info[name] = val
    info['attrs'] = REQUIRED_ATTRS
    return Stat(**info)

def attr_merge_sql(md_str_1, md_str_2):
    if md_str_1 is None:
        return md_str_2

    if md_str_2 is None:
        return md_str_1

    md1 = json_to_stat(md_str_1)
    md2 = json_to_stat(md_str_2)

    return stat_to_json(attr_merge(md1, md2))

def extract_id_sql(md_str_1):
    if md_str_1 is None:
        return None

    js = json.loads(md_str_1)

    return js['id']

def wrap_show_exc(fn):
    @functools.wraps(fn)
    def fn2(*n, **kw):
        try:
            return fn(*n, **kw)
        except:
            traceback.print_exc()
            raise
    return fn2

pysqlite_dll: typing.Optional[ctypes.PyDLL]
sqlite3_close: typing.Optional[Callable]
try:
    # NB: the sqlite3 library should already be loaded
    #     but we specify noload just in case
    if sys.platform == "darwin":
        RTLD_NOLOAD = 0x10
    elif sys.platform.startswith("linux"):
        RTLD_NOLOAD = 0x04
    else:
        RTLD_NOLOAD = 0

    pysqlite_dll = ctypes.PyDLL(_sqlite3.__file__, ctypes.RTLD_GLOBAL | RTLD_NOLOAD)

    sqlite3_close_proto = ctypes.CFUNCTYPE(
        ctypes.c_int, # return code
        ctypes.c_void_p, # db argument
    )

    try:
        sqlite3_close = sqlite3_close_proto(("sqlite3_close_v2",
                                             pysqlite_dll))
    except Exception:
        sqlite3_close = sqlite3_close_proto(("sqlite3_close",
                                             pysqlite_dll))
except Exception:
    pysqlite_dll = None
    sqlite3_close = None

class pysqlite_Connection_header(ctypes.Structure):
    _fields_ = [("a", ctypes.c_ssize_t),
                ("b", ctypes.c_void_p)]

def get_dbpp(conn):
    return ctypes.cast(id(conn) +
                       ctypes.sizeof(pysqlite_Connection_header),
                       ctypes.POINTER(ctypes.c_void_p))

_hold_ref_lock = threading.Lock()
_hold_ref: Mapping[sqlite3.Connection, Callable[[typing.Any], typing.Any]] = weakref.WeakKeyDictionary()
def register_deterministic_function(conn, name, num_params, func):
    if not isinstance(conn, sqlite3.Connection):
        raise Exception("Bad connection object: %r" % (conn,))

    if sys.version_info >= (3, 8):
        return conn.create_function(name, num_params, func, deterministic=True)

    if pysqlite_dll is None:
        raise Exception("can't create function")

    # This is a hack, oh well this is how I roll

    sqlite3_create_function_proto = ctypes.CFUNCTYPE(ctypes.c_int,
                                                     ctypes.c_void_p, # db
                                                     ctypes.c_char_p, # zFunctionName
                                                     ctypes.c_int, # nArg
                                                     ctypes.c_int, # eTextRep
                                                     ctypes.c_void_p, # pApp
                                                     ctypes.c_void_p,
                                                     ctypes.c_void_p,
                                                     ctypes.c_void_p)

    sqlite3_create_function = sqlite3_create_function_proto(("sqlite3_create_function",
                                                             pysqlite_dll))
    # get dp pointer from connection object
    dbp = get_dbpp(conn).contents

    SQLITE_DETERMINISTIC = 0x800
    SQLITE_UTF8 = 0x1
    rc = sqlite3_create_function(dbp, name.encode("utf8"), num_params,
                                 SQLITE_DETERMINISTIC | SQLITE_UTF8,
                                 id(func),
                                 pysqlite_dll._pysqlite_func_callback,
                                 None,
                                 None)
    if rc:
        raise Exception("Error while creating function: %r" % (rc,))

    # hold ref on passed function object
    with _hold_ref_lock:
        if conn not in _hold_ref:
            _hold_ref[conn] = []
        _hold_ref[conn].append(func)

class MustMutate(enum.Enum):
    token = 0
MUST_MUTATE = MustMutate.token

class Deleted(enum.Enum):
    token = 0

EMPTY_DIR_ENT = "/empty/"

class WeakrefableConnection(sqlite3.Connection):
    def __init__(self, *n, **kw):
        self.funcs = None
        sqlite3.Connection.__init__(self, *n, **kw)
        self.funcs = []

    def create_function(self, name, num_params, func, **kw):
        toret = sqlite3.Connection.create_function(self, name, num_params, func, **kw)
        # NB: since we call sqlite3_close outside of GIL, we don't want
        #     it to trigger deallocation of the function objects. instead
        #     make that happen when the connection object is deallocated
        #     by adding an extra reference to the connection object itself
        self.funcs.append(func)
        return toret

    def close(self):
        # Current versions of pysqlite call sqlite3_close() on dealloc or close()
        # without releasing the GIL. This causes a deadlock if it tries to grab lock
        # that is internal to sqlite3 that another thread already has.
        # The correct fix is to release the gil before calling sqlite3_close()
        # but since we cannot change the _sqlite module our workaround is to use a
        # special ctypes version of close.
        if sqlite3_close is None:
            return sqlite3.Connection.close(self)

        # get dp pointer from connection object
        dbpp = get_dbpp(self)

        # get db pointer
        db_ptr = dbpp.contents.value

        # we need to call call base method
        # to finalize all statements before closing database
        # but we have to set database pointer to null so it doesn't
        # call sqlite3_close() on our database without first
        dbpp[0] = ctypes.c_void_p()
        try:
            sqlite3.Connection.close(self)
        except Exception:
            dbpp[0] = db_ptr
            raise

        if db_ptr:
            rc = sqlite3_close(db_ptr)
            if rc:
                raise Exception("Error while creating function: %r" % (rc,))

    def __del__(self):
        # NB: we should be able to call sqlite3.Connection.close
        #     even if init was never called but unfortunately that does not
        #     work, so don't do it.
        if self.funcs is None:
            return
        self.close()

def connect_weakrefable(*n, **kw):
    assert 'factory' not in kw
    kw['factory'] = WeakrefableConnection
    # we call close() in __del__ which might happen on a different thread
    kw['check_same_thread'] = False
    return sqlite3.connect(*n, **kw)

def has_directory_entries(cursor, path_key):
    cursor.execute("select exists(SELECT name FROM md_cache_entries WHERE path_key = ?)",
                   (path_key,))
    row = cursor.fetchone()
    return row[0]

class _Directory(IterableDirectory):
    def _get_to_iter(self, mutate, fs, path):
        refreshed = True

        path_key = str(path.normed())
        parent_path_key = str(path.parent.normed())

        with fs._get_db_conn() as conn, \
             trans(conn, fs._db_lock, is_exclusive=mutate), contextlib.closing(conn.cursor()) as cursor:
            is_empty = False
            to_iter = []

            cursor.execute("select md from md_cache where path_key = ?", (path_key,))
            mdrow = cursor.fetchone()
            if mdrow is not None:
                (md,) = mdrow
                if md is None:
                    raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

                if json_to_stat(md).type != 'directory':
                    raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

                cursor.execute("SELECT name, (SELECT md FROM md_cache WHERE path_key = norm_join(md_cache_entries.path_key, md_cache_entries.name)) FROM md_cache_entries WHERE path_key = ?",
                               (path_key,))

                for (name, md_str) in cursor:
                    if name == EMPTY_DIR_ENT:
                        is_empty = True
                        break
                    assert md_str is not None, \
                        ("We should have metadata if we have the directory entry %r / %r" %
                         (path_key, name))
                    stat_ = json_to_stat(md_str)
                    to_iter.append(md_plus_name(name, stat_))
            else:
                # if there is no md cache entry, then there are no directory entries
                # so no need to query DB.
                assert not has_directory_entries(cursor, path_key)

            if mutate:
                stat_num = fs._get_stat_num(cursor, path_key)
                parent_stat_num = fs._get_stat_num(cursor, parent_path_key)

        # if entries was empty, then fill it
        if not to_iter and not is_empty:
            if not mutate:
                return MUST_MUTATE

            entries_names = []
            with contextlib.closing(OldDirectory(fs._fs.open_directory(path))) as dir_:
                to_iter = list(dir_)

            if not entries_names:
                entries_names.append(EMPTY_DIR_ENT)

            with fs._get_db_conn() as conn, \
                 trans(conn, fs._db_lock, is_exclusive=True), contextlib.closing(conn.cursor()) as cursor:
                new_stat_num = fs._get_stat_num(cursor, path_key)
                if (stat_num == new_stat_num and
                    parent_stat_num == fs._get_stat_num(cursor, parent_path_key)):
                    # NB: there is potentially no stat entry for this directory
                    #     and there is no way to get a stat() entry consistent with
                    #     the data returned from open_directory().
                    #     There are two options, either:
                    #     1) don't cache data if we don't have the stat entry
                    #     2) fill a dummy md entry for the directory
                    #
                    #     We choose 2) because cache entries for directories don't really
                    #     store any interesting info aside from the fact that they are a directory.

                    cursor.execute("select md from md_cache where path_key = ?", (path_key,))
                    mdrow = cursor.fetchone()
                    if mdrow is None:
                        st = Stat(mtime=datenow_now(), type='directory', size=0,
                                  id=None, ctime=datenow_now(), rev=None, attrs={})
                        fs._update_md(cursor, path, st)
                    else:
                        assert mdrow[0] is not None and json_to_stat(mdrow[0]).type == 'directory'

                    # this only inserts EMPTY_DIR_ENT, the rest is filled
                    # by _update_md()
                    cursor.executemany("INSERT INTO md_cache_entries "
                                       "(path_key, name) VALUES (?, ?)",
                                       ((path_key, name) for name in entries_names))

                    cursor.execute("update md_cache_counter "
                                   "set counter = counter + 1 "
                                   "where path_key = ?",
                                   (path_key,))

                    # Cache the metadata we've received
                    # NB: we know none of the child entries has been changed since we
                    #     check dir num (updates to children always increment parent dir num)
                    #     so we can safely update them.
                    for stat in to_iter:
                        sub_path_key = path / stat.name
                        fs._update_md(cursor, sub_path_key, stat)
                else:
                    refreshed = False

        return (to_iter, refreshed)

    def __init__(self, fs, path):
        mutate = False
        while True:
            res = self._get_to_iter(mutate, fs, path)
            if res is MUST_MUTATE:
                mutate = True
                continue
            (to_iter, _) = res
            self._it = iter(to_iter)
            return

    def close(self):
        pass

    def __next__(self):
        return next(self._it)

    def __iter__(self):
        return self


DOWNLOAD_UNIT = 2 ** 16

if sys.platform == 'win32':
    import msvcrt
    import ctypes.wintypes as wt

    ULONG_PTR = ctypes.POINTER(wt.ULONG)

    class OFFSET_STRUCT(ctypes.Structure):
        _fields_ = [
            ("Offset", wt.DWORD),
            ("OffsetHigh", wt.DWORD),
        ]

    PVOID = ctypes.c_void_p
    class OVERLAPPED_UNION(ctypes.Union):
        _fields_ = [
            ("DUMMYSTRUCTNAME", OFFSET_STRUCT),
            ("Pointer", PVOID),
        ]

    class OVERLAPPED(ctypes.Structure):
        _fields_ = [
            ("Internal", ULONG_PTR),
            ("InternalHigh", ULONG_PTR),
            ("DUMMYUNIONNAME", OVERLAPPED_UNION),
            ("hEvent", wt.HANDLE),
        ]

    ReadFile_proto = ctypes.WINFUNCTYPE(wt.BOOL, wt.HANDLE, wt.LPVOID, wt.DWORD, wt.LPDWORD, ctypes.POINTER(OVERLAPPED))
    ReadFile = ReadFile_proto(("ReadFile", ctypes.windll.kernel32))

    PyObject_AsWriteBuffer_proto = ctypes.PYFUNCTYPE(
        ctypes.c_int,
        ctypes.py_object, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_ssize_t),
    )
    PyObject_AsWriteBuffer = PyObject_AsWriteBuffer_proto(("PyObject_AsWriteBuffer", ctypes.pythonapi))
    def os_preadinto(fd: int, buf: bytearray | memoryview, offset: int) -> int:
        handle = msvcrt.get_osfhandle(fd)

        overlapped = OVERLAPPED()
        overlapped.DUMMYUNIONNAME.DUMMYSTRUCTNAME.Offset = offset & 0xffffffff
        overlapped.DUMMYUNIONNAME.DUMMYSTRUCTNAME.OffsetHigh = offset >> 32

        bytes_read = wt.DWORD()

        bufp = ctypes.c_void_p()
        bufsize = ctypes.c_ssize_t()
        err = PyObject_AsWriteBuffer(buf, ctypes.byref(bufp), ctypes.byref(bufsize))
        assert not err
        ret = ReadFile(handle, bufp.value, bufsize.value, ctypes.byref(bytes_read), ctypes.byref(overlapped))
        if not ret:
            raise ctypes.WinError(descr="Failed to call ReadFile()")

        return bytes_read.value

    WriteFile_proto = ctypes.WINFUNCTYPE(wt.BOOL, wt.HANDLE, wt.LPCVOID, wt.DWORD, wt.LPDWORD, ctypes.POINTER(OVERLAPPED))
    WriteFile = ReadFile_proto(("WriteFile", ctypes.windll.kernel32))

    PyObject_AsReadBuffer_proto = ctypes.PYFUNCTYPE(
        ctypes.c_int,
        ctypes.py_object, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_ssize_t),
    )
    PyObject_AsReadBuffer = PyObject_AsReadBuffer_proto(("PyObject_AsReadBuffer", ctypes.pythonapi))
    def os_pwrite(fd: int, buf: bytes | memoryview, offset: int) -> int:
        handle = msvcrt.get_osfhandle(fd)

        overlapped = OVERLAPPED()
        overlapped.DUMMYUNIONNAME.DUMMYSTRUCTNAME.Offset = offset & 0xffffffff
        overlapped.DUMMYUNIONNAME.DUMMYSTRUCTNAME.OffsetHigh = offset >> 32

        bytes_written = wt.DWORD()

        bufp = ctypes.c_void_p()
        bufsize = ctypes.c_ssize_t()
        err = PyObject_AsReadBuffer(buf, ctypes.byref(bufp), ctypes.byref(bufsize))
        assert not err
        ret = WriteFile(handle, bufp.value, bufsize.value, ctypes.byref(bytes_written), ctypes.byref(overlapped))
        if not ret:
            raise ctypes.WinError(descr="Failed to call WriteFile()")

        return bytes_written.value
else:
    def os_preadinto(fd: int, data: bytearray | memoryview, offset: int) -> int:
        size = len(data)
        ret = os.pread(fd, size, offset)
        data[:len(ret)] = ret
        return len(ret)

    os_pwrite = os.pwrite

class PreadMixin(object):
    def pread(self, size, offset):
        buf = bytearray(size)
        amt = self.preadinto(buf, offset)
        return memoryview(buf)[:amt]

def rev_to_fn(rev):
    # we special case dropbox revision tags
    if re.search("^rev:[0-9a-f]+$", rev) is None:
        return 'b%s.bin' % (base64.b32encode(rev.encode("utf-8")).decode("utf-8").replace("=", "z"),)

    # NB: skip rev: prefix
    return 'i%s.bin' % (rev[4:],)

class StreamingFile(PreadMixin):
    def __init__(self, fs, stat: OldStatProtocolWithExtra):
        assert stat.rev is not None, (
            "Empty stat rev for file: %r" % (stat,)
        )

        self._real_fs = fs
        self.cache_folder = fs._cache_folder
        self.fs = fs._fs
        self._stat = stat
        self.reset_lock = SharedLock()
        self.is_closed = False

        self.cached_file = None
        self.back_file = self.fs.x_open_by_rev(stat.rev)

        self._reset()

    def stat(self) -> OldStatProtocolWithExtra:
        return self._stat

    def _reset(self):
        if self.cache_folder is not None:
            try:
                os.makedirs(self.cache_folder)
            except OSError:
                pass

        if self.cache_folder is not None:
            try:
                with tempfile.NamedTemporaryFile(dir=self.cache_folder,
                                                 delete=False) as f:
                    temp_path = f.name

                old_fn = '%s.bin' % (self._stat.rev,)
                fn = rev_to_fn(self._stat.rev)

                # NB: make sure no other process uses the cached file if it exists
                try:
                    os.replace(os.path.join(self.cache_folder, old_fn), temp_path)
                except Exception as e:
                    if not isinstance(e, OSError) or e.errno not in [errno.ENOENT, errno.EINVAL]:
                        log.info("Couldn't use old fn for cache file", exc_info=True)
                    # NB: make sure no other process uses the cached file if it exists
                    try:
                        os.replace(os.path.join(self.cache_folder, fn), temp_path)
                    except FileNotFoundError:
                        pass

                self.cached_file = open(temp_path, 'r+b', buffering=0)

                amt = self.cached_file.seek(0, os.SEEK_END)

                try:
                    self._real_fs._check_space(self._stat.size - amt)
                except OSError as e:
                    assert e.errno == errno.ENOSPC
                    self.cached_file.close()
                    self.cached_file = None
                    os.rename(temp_path, os.path.join(self.cache_folder, fn))
            except Exception:
                log.warning("failed to create cache file",
                            exc_info=True)

        if self.cached_file is None:
            try:
                self.cached_file = tempfile.TemporaryFile(buffering=0)
            except Exception:
                log.warning("failed to create temporary file",
                            exc_info=True)
                return

    def preadinto(self, data, offset):
        size = len(data)
        ctx = self.reset_lock.shared_context()

        if True:
            with ctx:
                if self.is_closed:
                    raise Exception("file is closed")

                # limit size
                size = min(size + offset, self._stat.size) - offset

                if size <= 0:
                    return 0

                if self.cached_file is not None:
                    try:
                        file_size = self.cached_file.seek(0, os.SEEK_END)
                    except Exception:
                        log.warning("Failed to read cached file pointer", exc_info=True)
                        file_size = 0
                else:
                    file_size = 0

                # if we don't have all the data, then hit network
                if offset + size > file_size:
                    log.debug("Bypassing file cache %r", (offset, size))
                    amt = self.back_file.preadinto(data, offset)

                    # NB: no need to grab lock before writing to cached file
                    #     because we use pwrite()
                    try:
                        if self.cached_file is not None:
                            file_size = self.cached_file.seek(0, os.SEEK_END)
                            if offset <= file_size:
                                os_pwrite(self.cached_file.fileno(), memoryview(data)[:amt], offset)
                    except Exception as e:
                        if not (isinstance(e, (OSError, IOError)) and
                                e.errno == errno.ENOSPC):
                            log.warning("Failed to cache data", exc_info=True)

                    return amt

                if hasattr(os, 'preadv'):
                    return os.preadv(self.cached_file.fileno(), [data], offset)
                else:
                    return os_preadinto(self.cached_file.fileno(), data, offset)

    def close(self):
        th = None
        with self.reset_lock:
            if self.is_closed:
                return
            self.is_closed = True
            self.back_file.close()
            if True:
                if self.cached_file is not None:
                    # Generally close should never throw an exception
                    # but in the case of using TemporaryFile it can
                    try:
                        self.cached_file.close()
                    except FileNotFoundError:
                        pass
                    except Exception:
                        log.warning("failed to close temporary file",
                                    exc_info=True)
                    if isinstance(getattr(self.cached_file, 'name', None), str):
                        try:
                            fn = os.path.join(self.cache_folder,
                                              rev_to_fn(self._stat.rev))
                            os.rename(self.cached_file.name, fn)
                        except Exception:
                            log.exception("Unexpected failure to unlink lock file")
                    self.cached_file = None

class NullFile(PreadMixin):
    def __init__(self, id_):
        now_ = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
        self._stat = Stat(size=0, mtime=now_, ctime=now_, type='file', id=id_,
                          rev=None, attrs=REQUIRED_ATTRS)

    def stat(self):
        return self._stat

    def preadinto(self, buf, offset):
        return 0

    def close(self):
        pass

SQLITE_FILE_BLOCK_SIZE = 4096
class SQLiteFrontFile(PositionIO):
    # NB: SqliteFrontFile relies on backfile argument not mutating
    # NB: backfile becomes owned by SQLiteFrontFile after construction
    def __init__(self, backfile):
        PositionIO.__init__(self)

        self._backfile = backfile
        self._pool = ConnPool(self._create_db_conn)
        self._file_path = None

        stat = self._backfile.stat()

        try:
            (fd, self._file_path) = tempfile.mkstemp()
            os.close(fd)
            db_path = "file:%s" % (self._file_path,)
            self._setup_db(db_path, '?', stat)
        except Exception:
            log.warning("Error creating temporary file for writes, using memory only", exc_info=True)
            self._clear_db()
            self._pool = ConnPool(self._create_db_conn)
            self._file_path = None
            db_path = "file:dropboxsff-%d?mode=memory" % (id(self),)
            self._setup_db(db_path, '&', stat)

    def _setup_db(self, db_path, appender, stat: OldStatProtocolWithExtra):
        self._db_file = db_path

        use_shared_cache = True
        self._db_lock: typing.Optional[SharedLock]
        if use_shared_cache:
            self._db_file += appender + "cache=shared"
            # Application locking is only necessary in shared cache mode
            # otherwise SQLite will do locking for us
            self._db_lock = SharedLock()
        else:
            self._db_lock = None

        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), \
             contextlib.closing(conn.cursor()) as cursor:
            self._update_write_md(cursor, stat.size, stat.ctime, stat.mtime)

    def _update_write_md(self, cursor, size, ctime, mtime):
        toupdate = []
        if size is not None:
            toupdate.append(("size", size))
        if ctime is not None:
            toupdate.append(("ctime", int(aware_timestamp(ctime))))
        if mtime is not None:
            toupdate.append(("mtime", int(aware_timestamp(mtime))))
        cursor.executemany("INSERT OR REPLACE INTO md (name, value) VALUES (?, ?)",
                           toupdate)

    def replace_underlying(self, new_backfile):
        oldbackfile = self._backfile

        new_stat = new_backfile.stat()

        # basic sanity check
        assert oldbackfile.stat().size == new_stat.size

        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), \
             contextlib.closing(conn.cursor()) as cursor:
            self._update_write_md(cursor, new_stat.size, new_stat.ctime, new_stat.mtime)
            self._backfile = new_backfile

        oldbackfile.close()

    def _file_length(self) -> int:
        return self.stat().size

    def stat(self):
        stat_dict = {}
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock), contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("SELECT name, cast(value as integer) FROM md WHERE name IN ('size', 'mtime', 'ctime')")
            for (name, value) in cursor:
                if name in ["mtime", "ctime"]:
                    value = datetime.datetime.fromtimestamp(value, tz=datetime.timezone.utc)
                stat_dict[name] = value

        r = self._backfile.stat()
        return Stat(type=r.type, id=r.id, rev=None, attrs=REQUIRED_ATTRS,
                    **stat_dict)

    def _clear_db(self):
        self._pool.close()
        if self._file_path is not None:
            try:
                os.unlink(self._file_path)
            except Exception:
                log.warning("Error unlinking dirty cache file",
                            exc_info=True)

    def close(self):
        if self.closed:
            return
        self._clear_db()
        self._backfile.close()
        super().close()

    def _init_db(self, conn):
        # NB: since the database is temporary (we definitely don't
        #     need it if anything crashes) we have no need for durability.
        #     data hits disk only so it doesn't fill memory, not for persistence
        conn.execute("pragma journal_mode = memory")
        conn.execute("pragma synchronous = off")
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS blocks
        ( blkidx INTEGER PRIMARY KEY
        , data BLOB NOT NULL
        );

        CREATE TABLE IF NOT EXISTS md
        ( name TEXT PRIMARY KEY
        , value BLOB NOT NULL
        )
        """)
        conn.commit()

        return conn

    def _create_db_conn(self):
        return self._init_db(connect_weakrefable(self._db_file, uri=True))

    def _get_db_conn(self):
        return self._pool.get_conn()

    def is_dirty(self):
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock), contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("SELECT EXISTS(SELECT * FROM blocks)")
            if cursor.fetchone()[0]:
                return True
            cursor.execute("SELECT cast(value as integer) FROM md WHERE name = 'size'")
            if cursor.fetchone()[0] != self._backfile.stat().size:
                return True
            return False

    def readable(self):
        return True

    def _preadinto(self, cursor, buf, offset):
        cursor.execute("SELECT cast(value as integer) FROM md WHERE name = 'size'")
        (extent_of_file,) = cursor.fetchone()

        size = len(buf)

        if offset + size > extent_of_file:
            size = extent_of_file - offset
            if size < 0:
                return 0
            buf = memoryview(buf)[:size]

        blkidx_start = offset // SQLITE_FILE_BLOCK_SIZE
        blkidx_start_offset = offset % SQLITE_FILE_BLOCK_SIZE

        blkidx_end = (offset + size) // SQLITE_FILE_BLOCK_SIZE
        blkidx_end_offset = (offset + size) % SQLITE_FILE_BLOCK_SIZE

        if not blkidx_end_offset:
            blkidx_end -= 1
            blkidx_end_offset = SQLITE_FILE_BLOCK_SIZE

        blks = [None] * (blkidx_end - blkidx_start + 1)

        # get data from writeable sqlite overly
        cursor.execute("SELECT blkidx, data FROM blocks WHERE blkidx >= ? AND blkidx <= ?",
                       (blkidx_start, blkidx_end))
        for (blkidx, data) in cursor:
            blks[blkidx - blkidx_start] = data

        # if there were no overwritten blocks in this region,
        # just use the backfile as-is
        if all(a is None for a in blks):
            return self._backfile.preadinto(buf, offset)

        if any(a is None for a in blks):
            # get remaining blocks from backing store
            # NB: read everything at once to minimize potential latency
            data = self._backfile.pread(len(blks) * SQLITE_FILE_BLOCK_SIZE,
                                        blkidx_start * SQLITE_FILE_BLOCK_SIZE)
            for (idx, _) in enumerate(blks):
                if blks[idx] is not None:
                    continue
                read_ = data[idx * SQLITE_FILE_BLOCK_SIZE : (idx + 1) * SQLITE_FILE_BLOCK_SIZE]
                blks[idx] = b'%s%s' % (read_, b'\0' * (SQLITE_FILE_BLOCK_SIZE - len(read_)))

        assert all(len(a) == SQLITE_FILE_BLOCK_SIZE for a in blks)

        # fix up beginning and ending blocks
        if blks:
            if blkidx_start == blkidx_end:
                assert len(blks) == 1
                blks[0] = blks[0][blkidx_start_offset:blkidx_end_offset]
            else:
                blks[0] = blks[0][blkidx_start_offset:]
                blks[-1] = blks[-1][:blkidx_end_offset]

        # concatenate data and return
        toret = b''.join(blks)

        retlen = len(toret)

        buf[:retlen] = toret

        return retlen

    def _pread(self, cursor, size, offset):
        buf = bytearray(size)
        amt = self._preadinto(cursor, buf, offset)
        return memoryview(buf)[:amt]

    def preadinto(self, buf, offset):
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock), \
             contextlib.closing(conn.cursor()) as cursor:
            return self._preadinto(cursor, buf, offset)

    def writable(self):
        return True

    def _pwrite(self, cursor, data, offset):
        size = len(data)

        blkidx_start = offset // SQLITE_FILE_BLOCK_SIZE
        blkidx_start_offset = offset % SQLITE_FILE_BLOCK_SIZE

        blkidx_end = (offset + size) // SQLITE_FILE_BLOCK_SIZE
        blkidx_end_offset = (offset + size) % SQLITE_FILE_BLOCK_SIZE
        if not blkidx_end_offset:
            blkidx_end -= 1
            blkidx_end_offset = SQLITE_FILE_BLOCK_SIZE

        # write data to backfile
        desired_header_size = blkidx_start_offset
        # NB: avoid calls to pread if not necessary, this is an optimization
        if desired_header_size:
            header_block = self._pread(cursor, SQLITE_FILE_BLOCK_SIZE, blkidx_start * SQLITE_FILE_BLOCK_SIZE)
            header = header_block[:desired_header_size]
        else:
            header_block = None
            header = b''
        desired_footer_size = (blkidx_end + 1) * SQLITE_FILE_BLOCK_SIZE - (offset + size)
        if desired_footer_size:
            if (header_block is not None and
                blkidx_end == blkidx_start):
                footer_block = header_block
            else:
                footer_block = self._pread(cursor, SQLITE_FILE_BLOCK_SIZE, blkidx_end * SQLITE_FILE_BLOCK_SIZE)

            footer = footer_block[-desired_footer_size:]
        else:
            footer = b''

        if not header and not desired_header_size and not footer and not desired_footer_size:
            block_aligned_data = data
        else:
            block_aligned_data = (b'%s%s%s%s%s' %
                                  (header, b'\0' * (desired_header_size - len(header)),
                                   data,
                                   footer, b'\0' * (desired_footer_size - len(footer))))
        block_aligned_data = memoryview(block_aligned_data)
        assert not (len(block_aligned_data) % SQLITE_FILE_BLOCK_SIZE)

        hai = [(idx, block_aligned_data[(idx - blkidx_start) * SQLITE_FILE_BLOCK_SIZE:
                                        (idx - blkidx_start + 1) * SQLITE_FILE_BLOCK_SIZE])
               for idx in range(blkidx_start, blkidx_end + 1)]
        cursor.executemany("INSERT OR REPLACE INTO blocks (blkidx, data) VALUES (?, ?)",
                           hai)

        cursor.execute("SELECT cast(value as integer) FROM md WHERE name = 'size'")
        (extent_of_file,) = cursor.fetchone()

        new_extent_of_file = max(offset + size, extent_of_file)
        self._update_write_md(cursor, new_extent_of_file,
                              datetime.datetime.now(datetime.timezone.utc),
                              datetime.datetime.now(datetime.timezone.utc))

        return len(data)

    def pwrite(self, data, offset):
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), \
             contextlib.closing(conn.cursor()) as cursor:
            return self._pwrite(cursor, data, offset)

    def ptruncate(self, offset):
        blkidx_start = offset // SQLITE_FILE_BLOCK_SIZE
        blkidx_start_offset = offset % SQLITE_FILE_BLOCK_SIZE
        if not blkidx_start_offset:
            blkidx_start -= 1

        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), \
             contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("SELECT cast(value as integer) FROM md WHERE name = 'size'")
            cur_size = cursor.fetchone()[0]
            if offset < cur_size:
                # NB: technically the delete isn't necessary
                #     also this is likely a vain attempt to save space.
                #     doing things in vain is our way of life, so carry on.
                cursor.execute("DELETE FROM blocks WHERE blkidx > ?",
                               (blkidx_start,))
                self._update_write_md(cursor, offset, None, None)
            else:
                # NB: extend with zeros to block data in backfile
                self._pwrite(cursor, b'\0' * (offset - cur_size), cur_size)

class CachedDirectory(object):
    def __init__(self, fs, stat: OldStatProtocolWithExtra):
        self._fs = fs
        self._stat = stat
        assert self._stat.type == 'directory', (
            "Bad stat for CachedDirectory: %r" % (stat,)
        )
        self._file = self._fs._fs.x_open_by_id(stat.id)

        self._sync_tag = 0

    def stat(self):
        return self._stat

    def queue_sync(self):
        return None

    def sync(self):
        pass

    def pwrite(self, *n, **kw):
        raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))

    def preadinto(self, *n, **kw):
        raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))

    def ptruncate(self, *n, **kw):
        raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))

    def is_dirty(self):
        return False

    def close(self):
        self._file.close()

class BytesWrite:
    def __init__(self, obj: typing.IO[bytes]):
        self._obj = obj

    def write(self, s: bytes) -> int:
        return self._obj.write(s)

class CachedFile(object):
    def __init__(self, fs, stat: OldStatProtocolWithExtra):
        self._fs = fs
        self._id = stat.id
        self._base_stat = stat

        assert stat.type == "file", (
            "Bad stat for CachedFile: %r" % (stat,)
        )
        self._file = SQLiteFrontFile(StreamingFile(fs, stat))

        self._upload_cond = threading.Condition()
        self._upload_now: typing.Optional[SQLiteFrontFile] = None
        self._upload_next: typing.Optional[SQLiteFrontFile] = None
        self._eio = False
        self._sync_tag = 0
        self._complete_tag = 0
        self._closed = False

        self._thread = threading.Thread(target=self._upload_thread)
        self._thread.start()

    def _upload_thread(self) -> None:
        while True:
            try:
                with self._upload_cond:
                    while self._upload_now is None and self._upload_next is None:
                        if self._closed:
                            # File has been closed, abandon ship!
                            return
                        self._upload_cond.wait()
                    if self._upload_next is not None:
                        assert self._upload_next is self._file
                        self._upload_now = self._upload_next
                        self._upload_next = None
                        self._upload_cond.notify_all()
                        sync_tag = self._sync_tag
                        self._file = SQLiteFrontFile(self._file)
                    else:
                        assert self._upload_now is not None

                md = None
                self._upload_now.seek(0)
                towrite = self._fs._fs.x_write_stream()
                try:
                    shutil.copyfileobj(self._upload_now, towrite)
                    base_stat = self._base_stat
                    while True:
                        try:
                            nd = towrite.finish(self._id,
                                                mtime=self._upload_now.stat().mtime,
                                                mode=("update", base_stat.rev),
                                                strict_conflict=True)
                            md = OldStat(nd)
                        except FileExistsError: # This just means conflict
                            try:
                                e_stat = OldStat(self._fs._fs.x_stat_by_id(self._id))
                            except FileNotFoundError:
                                # file was deleted, black hole this change
                                pass
                            else:
                                # Another client edited this ID,
                                # We overwrite the file as this is
                                # what POSIX allows. Concurrency control
                                # is left to a higher level.
                                base_stat = e_stat
                                continue
                        break
                finally:
                    towrite.close()

                new_stat = None
                if md is not None:
                    assert md.id == self._id, \
                        "Bad assumption on how overwrite works :("

                    new_stat = md

                    if self._fs._cache_folder is not None:
                        try:
                            os.makedirs(self._fs._cache_folder)
                        except OSError:
                            pass

                        to_save = None
                        try:
                            to_save = tempfile.NamedTemporaryFile(dir=self._fs._cache_folder)
                            self._upload_now.seek(0)
                            # NB: we need to use BytesWrite because NamedTemporaryFile does not
                            #     infer to SupportsWrite[bytes] because of how typeshed implements
                            #     overloads
                            shutil.copyfileobj(self._upload_now, BytesWrite(to_save))
                            fn = rev_to_fn(new_stat.rev)
                            p = os.path.join(self._fs._cache_folder, fn)
                            # Unlink existing file since new one is definitely complete
                            try:
                                os.unlink(p)
                            except FileNotFoundError:
                                pass
                            except Exception:
                                log.warning("Error unlinking existing cache file",
                                            exc_info=True)
                            os.link(to_save.name, p)
                        except Exception:
                            log.warning("Error while linking cached file",
                                        exc_info=True)
                        finally:
                            if to_save is not None:
                                try:
                                    to_save.close()
                                except FileNotFoundError:
                                    pass
                                except Exception:
                                    log.warning("failed to close temporary file",
                                                exc_info=True)

                    self._base_stat = new_stat

                with self._upload_cond:
                    assert not self._closed, "File should nto be closed while we're uploading"
                    self._complete_tag = sync_tag
                    self._upload_now = None
                    self._upload_cond.notify_all()
                    if new_stat is not None:
                        try:
                            self._file.replace_underlying(StreamingFile(self._fs, new_stat))
                        except FileNotFoundError:
                            # revision no longer exists, do nothing
                            pass

                self._fs._submit_write(self._id)
            except Exception:
                log.exception("Error uploading file, sleeping...")
                with self._upload_cond:
                    self._eio = True
                    self._upload_cond.notify_all()
                    self._upload_cond.wait(100)

    def preadinto(self, buf, offset):
        return self._file.preadinto(buf, offset)

    def pwrite(self, data, offset):
        # NB: grab lock so we don't modify self._file while
        #     it's the argument of SQLiteFrontFile (from _upload_thread)
        with self._upload_cond:
            return self._file.pwrite(data, offset)

    def ptruncate(self, offset):
        with self._upload_cond:
            return self._file.ptruncate(offset)

    def stat(self):
        st = self._file.stat()
        # WriteStream.finish() has second granularity,
        # so keep mtime consistent when it comes back
        return st._replace(mtime=st.mtime.replace(microsecond=0))

    def _queue_sync(self):
        assert self._upload_next is None or self._upload_next is self._file
        if self._file.is_dirty() and self._upload_next is None:
            self._upload_next = self._file
            self._sync_tag += 1

        eio = self._eio
        self._eio = False

        if eio or self._file.is_dirty():
            self._upload_cond.notify_all()

        return (self._upload_now
                if self._upload_next is None else
                self._upload_next)

    def queue_sync(self):
        with self._upload_cond:
            return self._queue_sync()

    def sync(self):
        with self._upload_cond:
            self._queue_sync()
            sync_tag = self._sync_tag

            # wait for upload
            while not self._eio and self._complete_tag < sync_tag:
                self._upload_cond.wait()

            if self._eio:
                raise OSError(errno.EIO, os.strerror(errno.EIO))

    def _is_dirty(self):
        if True:
            return (self._file.is_dirty() or
                    self._upload_next is not None or
                    self._upload_now is not None)

    def is_dirty(self):
        with self._upload_cond:
            return self._is_dirty()

    def close(self):
        with self._upload_cond:
            if self._closed:
                return
            assert not self._is_dirty(), "close should not be called while file is syncing"
            self._file.close()
            self._closed = True
            self._upload_cond.notify_all()

LiveFileMetadata = collections.namedtuple('LiveFileMetadata',
                                          ["cached_file", "open_files"])

class InvalidFileCacheGenError(Exception): pass

class _File(PositionIO):
    def __init__(self, fs, stat: OldStatProtocolWithExtra, mode):
        PositionIO.__init__(self)

        self._fs = fs

        with self._fs._file_cache_lock:
            try:
                live_md = self._fs._open_files_by_id[stat.id]
            except KeyError:
                cached_file: CachedFile | CachedDirectory
                if stat.type == "file":
                    cached_file = CachedFile(fs, stat)
                else:
                    cached_file = CachedDirectory(fs, stat)

                live_md = self._fs._open_files_by_id[stat.id] = \
                          LiveFileMetadata(cached_file=cached_file,
                                           open_files=set())

            live_md.open_files.add(self)

        # NB: this lock lives above all file system locks
        self._lock = SharedLock()
        self._live_md = live_md
        self._id = stat.id
        self._stat = stat

        self._mode = mode

        if self._mode & os.O_TRUNC:
            self._live_md.cached_file.ptruncate(0)

    def stat(self):
        with self._lock.shared_context():
            if self._live_md is None:
                raise OSError(errno.EBADF, os.strerror(errno.EBADF))
            return self._live_md.cached_file.stat()

    def sync(self):
        with self._lock.shared_context():
            if self._live_md is None:
                raise OSError(errno.EBADF, os.strerror(errno.EBADF))

            return self._live_md.cached_file.sync()

    def preadinto(self, buf, offset):
        if not self.readable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))

        with self._lock.shared_context():
            if self._live_md is None:
                raise OSError(errno.EBADF, os.strerror(errno.EBADF))

            return self._live_md.cached_file.preadinto(buf, offset)

    def readable(self):
        return (self._mode & O_ACCMODE) in (os.O_RDONLY, os.O_RDWR)

    def pwrite(self, data, offset):
        if not self.writeable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))

        with self._lock.shared_context():
            if self._live_md is None:
                raise OSError(errno.EBADF, os.strerror(errno.EBADF))

            return self._live_md.cached_file.pwrite(data, offset)

    def writeable(self):
        return (self._mode & O_ACCMODE) in (os.O_WRONLY, os.O_RDWR)

    def _file_length(self):
        return self.stat().size

    def ptruncate(self, offset):
        if not self.writeable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))

        with self._lock.shared_context():
            return self._live_md.cached_file.ptruncate(offset)

    def close(self):
        if self.closed:
            return

        with self._lock:
            if self._live_md is None:
                return
            live_md = self._live_md
            self._live_md = None

            toclose = None
            with self._fs._file_cache_lock:
                live_md.open_files.remove(self)
                if (not self._fs._openners and
                    not live_md.open_files and
                    # keep file around as long as its syncing
                    not live_md.cached_file.queue_sync()):
                    toclose = live_md.cached_file
                    popped = self._fs._open_files_by_id.pop(self._id)
                    assert popped is live_md

                # NB: this needs to be in the file_cache_lock
                #     because CachedFile does things on open/close()
                #     that expect to be serialized for a given rev
                if toclose is not None:
                    toclose.close()

        super().close()

def check_runtime_requirements():
    if sqlite3.sqlite_version_info < (3, 9, 0):
        raise RuntimeError("Need sqlite version >= 3.9.0, you have: %r" % (sqlite3.sqlite_version,))

class FileSystem(fsabc.FileSystem):
    def __init__(self, fs, cache_folder=None):
        check_runtime_requirements()

        use_shared_cache = True

        self._cache_folder = cache_folder
        self._db_file = "file:dropboxvfs-%d?mode=memory" % (id(self),)
        self._fs = fs

        if use_shared_cache:
            self._db_file += "&cache=shared"
            # Application locking is only necessary in shared cache mode
            # otherwise SQLite will do locking for us
            self._db_lock = SharedLock()
        else:
            assert ("mode=memory" not in self._db_file and
                    ":memory:" not in self._db_file), (
                        "In-memory database connections without " +
                        "shared cache are distinct databases."
                    )

            self._db_lock = None

        self._pool = ConnPool(self._create_db_conn)

        self._file_cache_lock = threading.Lock()
        self._open_files_by_id = {}
        self._openners = 0

        # watch file system and clear cache on any changes
        # NB: we need to use a 'db style' watch because we need the
        #     ids, and create_watch() doesn't promise ids
        try:
            create_db_watch = self._fs.x_create_db_style_watch
        except AttributeError:
            self._watch_stop = None
        else:
            self._watch_stop = create_db_watch(self._handle_changes)

        # start thread that prunes cache
        self._prune_event = threading.Event()
        self._close_prune_thread = False
        threading.Thread(target=self._prune_thread, daemon=True).start()

        # start statvfs caching thread
        self._statvfs_event = threading.Event()
        self._statvfs = None
        threading.Thread(target=self._statvfs_caching_thread, daemon=True).start()

        self._refresh_thread_stop = False
        self._refresh_queue = queue.Queue(100)
        self._refresh_thread = threading.Thread(target=self._refresh_thread_start)
        self._refresh_thread.start()

    def _refresh_thread_start(self):
        while not self._refresh_thread_stop:
            to_refresh = self._refresh_queue.get()
            if to_refresh is None:
                continue

            try:
                with contextlib.closing(OldDirectory(self.open_directory(to_refresh))) as dir_:
                    for entry in dir_:
                        if self._refresh_thread_stop:
                            break
            except OSError:
                pass
            except Exception:
                log.exception("Failed to traverse directory %r", to_refresh)

    def _statvfs_caching_thread(self):
        while not self._close_prune_thread:
            try:
                self._statvfs = self._fs.statvfs()
            except Exception:
                log.warning("Error while calling statvfs", exc_info=True)
            self._statvfs_event.wait()
            self._statvfs_event.clear()

    def close(self):
        if self._close_prune_thread:
            return
        self._close_prune_thread = True
        self._prune_event.set()
        if self._watch_stop is not None:
            self._watch_stop()
        self._refresh_thread_stop = True
        self._refresh_queue.put(None)
        self._refresh_thread.join()
        self._fs.close()
        self._pool.close()

    def _check_space(self, size):
        try:
            free_space = shutil.disk_usage(self._cache_folder).free

            cache_entries = []
            for name in os.listdir(self._cache_folder):
                cache_entries.append((name, os.lstat(os.path.join(self._cache_folder, name))))
        except Exception as e:
            if not isinstance(e, OSError):
                log.exception("Error while checking space")
                return

        cache_size = sum(st.st_size for (_, st) in cache_entries)

        # % of free space that cache is allowed to take up
        N = 0.10

        if (cache_size + size) / (cache_size + free_space) > N:
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))

    def _prune_thread(self):
        if not self._cache_folder:
            return

        # prune every 30 minutes
        PRUNE_PERIOD = 30 * 60

        while not self._close_prune_thread:
            try:
                # compute total free space on disk
                free_space = shutil.disk_usage(self._cache_folder).free

                # compute total space taken by cache
                cache_entries = []
                for name in os.listdir(self._cache_folder):
                    cache_entries.append((name, os.lstat(os.path.join(self._cache_folder, name))))

                cache_size = sum(st.st_blocks * 512
                                 if hasattr(st, 'st_blocks') else
                                 st.st_size
                                 for (_, st) in cache_entries)

                # sort by ascending atime, descending size
                cache_entries.sort(key=lambda name_st_pair: -name_st_pair[1].st_size)

                # P: `cache / (cache + free_space)`
                # N: configurable value from [0, 1]

                N = 0.10

                # delete oldest accessed files, largest files until P<=N
                potential_free_space = cache_size + free_space
                for (name, st) in cache_entries:
                    try:
                        if cache_size / potential_free_space <= N:
                            break
                    except ZeroDivisionError:
                        # NB: not sure how this happens if len(cache_entries) != 0
                        #     but it does happen
                        break

                    try:
                        os.unlink(os.path.join(self._cache_folder, name))
                        cache_size -= (st.st_blocks * 512
                                       if hasattr(st, 'st_blocks') else
                                       st.st_size)
                    except Exception:
                        log.exception("Error unlinking file: %r",
                                      os.path.join(self._cache_folder, name))

                self._prune_event.wait(PRUNE_PERIOD)
                self._prune_event.clear()
            except Exception as e:
                if not isinstance(e, OSError):
                    log.exception("Error pruning cache, sleeping...")
                else:
                    log.warning("Error pruning cache, sleeping...", exc_info=True)
                self._prune_event.wait(100)

    def _init_db(self, conn):
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS md_cache
        ( path_key TEXT PRIMARY KEY
        , md TEXT
        );

        CREATE TABLE IF NOT EXISTS md_cache_entries
        ( path_key TEXT NOT NULL
        , name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS md_cache_counter
        ( path_key TEXT PRIMARY KEY
        , counter integer NOT NULL
        );

        CREATE UNIQUE INDEX IF NOT EXISTS md_cache_entries_unique
        on md_cache_entries (path_key, file_name_norm(name));
        """)
        conn.commit()

        return conn

    def _norm_join_sql(self, path_key, name):
        return str((self._fs.parse_path(path_key) / name).normed())

    def _create_db_conn(self):
        conn = connect_weakrefable(self._db_file, uri=True)
        # we do this here incase all references to the database died because of some error
        conn.create_function("attr_merge", 2, wrap_show_exc(attr_merge_sql))
        conn.create_function("norm_join", 2, wrap_show_exc(self._norm_join_sql))
        register_deterministic_function(conn, "extract_id", 1, wrap_show_exc(extract_id_sql))
        register_deterministic_function(conn, "file_name_norm", 1, wrap_show_exc(self._fs.file_name_norm))
        return self._init_db(conn)

    def _get_db_conn(self):
        return self._pool.get_conn()

    def _submit_write(self, id_):
        self._handle_changes([id_])

        # Check if file needs to be closed
        toclose = None
        with self._file_cache_lock:
            try:
                live_md = self._open_files_by_id[id_]
            except KeyError:
                # NB: file wasn't open
                return

            if (not self._openners and
                not live_md.open_files and
                # keep file around as long as its syncing
                not live_md.cached_file.queue_sync()):
                toclose = live_md.cached_file
                popped = self._open_files_by_id.pop(id_)
                assert popped is live_md

            if toclose is not None:
                assert not toclose.is_dirty()
                toclose.close()

    def _check_md_cache_entry(self, cursor, path_key):
        cursor.execute("SELECT md FROM md_cache WHERE path_key = ? limit 1",
                       (path_key,))
        row = cursor.fetchone()
        if row is not None:
            (md,) = row
            if md is not None:
                st = json_to_stat(md)
                assert st.type != "file" or st.rev is not None, (
                    "File stat missing rev: %r" % (st,)
                )

    def _update_md(self, cursor, path, stat: typing.Optional[OldStatProtocolWithExtra]):
        path_key = str(path.normed())

        do_update = True
        if stat is None:
            md_str = None
        else:
            # if the child is a directory, and we know it hasn't
            # changed (caller guarantee), then do nothing.  this
            # avoids unnecessarily recursively dropping
            # md_cache_entries
            if stat.type == 'directory':
                cursor.execute("SELECT md FROM md_cache WHERE path_key = ? limit 1",
                               (path_key,))
                row = cursor.fetchone()
                if row is not None:
                    (md,) = row
                    if (md is not None and
                        # TODO: doesn't matter for dbxfs child fs, but in the future
                        #       check mtime/size as well
                        getattr(json_to_stat(md), 'type', None) == 'directory'):
                        do_update = False
            assert stat.type != "file" or stat.rev is not None, (
                "File stat missing rev: %r" % (stat,)
            )
            md_str = stat_to_json(stat)

        if do_update:
            # This is just for debugging
            self._check_md_cache_entry(cursor, path_key)

            cursor.execute("REPLACE INTO md_cache (path_key, md) "
                           "VALUES (?, attr_merge((SELECT md FROM md_cache WHERE path_key = ?), ?))",
                           (path_key, path_key, md_str))

            self._check_md_cache_entry(cursor, path_key)

            # Delete dir entries
            cursor.execute("delete from md_cache_entries where path_key = ?",
                           (path_key,))

            cursor.execute("update md_cache_counter "
                           "set counter = counter + 1 "
                           "where path_key = ?",
                           (path_key,))

        # NB: we always update our parents cache counter if one exists
        #     so that if our parent is currently iterating, it doesn't clobber
        #     the child stat data we just set
        # NB: Ideally we'd only do this if we actually change the parent directory
        #     below but we have no other way to avoid concurrent updates to child entries
        parent_path_key = str(path.parent.normed())
        cursor.execute("update md_cache_counter "
                       "set counter = counter + 1 where "
                       "path_key = ?",
                       (parent_path_key,))

        if path_key == '/':
            return

        (parent_has_been_iterated,) = cursor.execute("""
        SELECT EXISTS(SELECT * FROM md_cache_entries WHERE path_key = ?)
        """, (parent_path_key,)).fetchone()

        if parent_has_been_iterated:
            # NB: store in parent directory if it is cached
            if stat is not None:
                cursor.execute("""
                INSERT OR REPLACE INTO md_cache_entries (path_key, name)
                SELECT ?, ? WHERE
                (SELECT EXISTS(SELECT * FROM md_cache_entries WHERE path_key = ?))
                """, (parent_path_key, path.name, parent_path_key))
                if cursor.rowcount:
                    # delete directory empty marker if it existed
                    cursor.execute("DELETE FROM md_cache_entries WHERE path_key = ? and name = ?", (parent_path_key, EMPTY_DIR_ENT))
            else:
                cursor.execute("""
                delete from md_cache_entries where path_key = ? and file_name_norm(name) = ?
                """, (parent_path_key, self._fs.file_name_norm(path.name)))
                if cursor.rowcount:
                    # insert directory empty marker if there are no more
                    # files under this directory
                    cursor.execute("""
                    INSERT INTO md_cache_entries (path_key, name)
                    SELECT ?, ? WHERE
                    (SELECT EXISTS(SELECT * FROM md_cache_entries WHERE
                    path_key = ?)) = 0
                    """,
                                 (parent_path_key, EMPTY_DIR_ENT, parent_path_key))

    def _reset_metadata_db(self, cursor):
        cursor.execute("DELETE FROM md_cache");
        cursor.execute("DELETE FROM md_cache_entries");
        cursor.execute("update md_cache_counter set counter = counter + 1");

    def _handle_changes(self, changes):
        self._statvfs_event.set()
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True):
            cursor = conn.cursor()

            if changes == "reset":
                self._reset_metadata_db(cursor)
                return

            for change in changes:
                # NB: the metadata we currently have could be newer than this change,
                #     so we invalidate cache instead of updating it with stale entry
                # TODO: we need a millisecond-precise 'server_modified' on all metadata
                #       entries from the dropbox api (including
                #       DeletedMetadata and FolderMetadata)

                # handle raw IDs in change list for now
                # TOOD: be more rigorous about change type in future
                if isinstance(change, str):
                    # NB: we currently submit changes via ID for writes to files only
                    #     i.e. not deletes or anything that modifies the path hierarchy,
                    #     so look for the md entries with the specific ID and just invalidate that
                    #     which is a relatively minimally impactful operation.
                    cursor.execute("select path_key from md_cache where md is not null and extract_id(md) = ?", (change,))
                    row = cursor.fetchone()
                    if row is None:
                        continue
                    (path_key,) = row
                else:
                    path_key = change.path_lower

                normed_path = self.create_path(*([] if path_key == "/" else path_key[1:].split("/")))
                self._invalidate_entry(cursor, normed_path)

    def _invalidate_entry(self, cursor, normed_path):
        # if True: if True: here to minimize the diff
        if True:
            if True:
                path_key = str(normed_path.normed())
                parent_path = normed_path.parent
                parent_path_key = str(parent_path)

                # Clear all directory entries,
                # also parent folder entries (since we don't know if
                # this file is currently deleted or not)
                for (path, path_key_) in [
                        (normed_path, path_key),
                        (parent_path, parent_path_key)
                ]:
                    cursor.execute("DELETE FROM md_cache_entries WHERE path_key = ?",
                                   (path_key_,))
                    # if the directory had entries, queue up refresh
                    if cursor.rowcount:
                        try:
                            self._refresh_queue.put_nowait(path)
                        except queue.Full:
                            pass

                # Remove from md cache
                cursor.execute("DELETE FROM md_cache WHERE path_key = ?",
                               (path_key,))

                # Update counters if they existed
                cursor.executemany("update md_cache_counter set counter = counter + 1 "
                                   "where path_key = ?",
                                   [(path_key,), (parent_path_key,)])

    def create_path(self, *args):
        return self._fs.create_path(*args)

    def file_name_norm(self, fn):
        return self._fs.file_name_norm(fn)

    def _invalidate_path(self, path):
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), contextlib.closing(conn.cursor()) as cursor:
            self._invalidate_entry(cursor, path)

    def open(self, path, mode=os.O_RDONLY, directory=False):
        with self._file_cache_lock:
            self._openners += 1
        try:
            try:
                st = self._stat(path)
            except FileNotFoundError:
                if not (mode & os.O_CREAT):
                    raise

                with self._fs.open(path, mode & (os.O_CREAT | os.O_EXCL)) as f:
                    st = OldStat(f.stat())

                # we need to invalidate the entry because we potentially mutated the underlying file system
                self._invalidate_path(path)
            else:
                if (mode & (os.O_EXCL | os.O_CREAT)) == (os.O_EXCL | os.O_CREAT):
                    raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))

            return _File(self, st, mode)
        finally:
            to_close = []
            with self._file_cache_lock:
                self._openners -= 1

                # close files that have no references
                if not self._openners:
                    for it in self._open_files_by_id.items():
                        (_, live_md) = it
                        if (not live_md.open_files and
                            not live_md.cached_file.queue_sync()):
                            to_close.append(it)

                    for (id_, live_md) in to_close:
                        popped = self._open_files_by_id.pop(id_)
                        assert live_md is popped

                for (_, live_md) in to_close:
                    live_md.cached_file.close()

    def open_directory(self, path):
        return NewDirectory(_Directory(self, path))

    def stat_has_attr(self, attr):
        return self._fs.stat_has_attr(attr)

    def _get_stat_num(self, cursor, path_key):
        cursor.execute("SELECT counter from md_cache_counter where path_key = ?",
                       (path_key,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("insert into md_cache_counter "
                           "(path_key, counter) values (?, -1)",
                           (path_key,))
            stat_num = -1
        else:
            (stat_num,) = row
        return stat_num

    def _stat_repeat(self, mutate: bool, path: fsabc.Path) -> OldStatProtocolWithExtra | MustMutate:
        assert isinstance(path, Path)

        DELETED = Deleted.token

        path_key = str(path.normed())
        parent_path_key = str(path.parent.normed())

        stat: None | Deleted | Stat | OldStat = None

        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=mutate), contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("SELECT md FROM md_cache WHERE path_key = ? limit 1",
                           (path_key,))
            row = cursor.fetchone()
            if row is None:
                # if it didn't exist in the md_cache, check if the
                # parent exists in md_cache_entries, if so then this
                # file doesn't exist
                (parent_has_been_iterated,) = cursor.execute("""
                SELECT EXISTS(SELECT * FROM md_cache_entries WHERE path_key = ?)
                """, (parent_path_key,)).fetchone()

                if parent_has_been_iterated:
                    assert path_key != parent_path_key, (
                        "Should not be child entries under root path if root path doesn't exist"
                    )

                    stat = DELETED
                else:
                    stat = None
            else:
                (md,) = row
                stat = DELETED if md is None else json_to_stat(md)

            if mutate:
                parent_stat_num = self._get_stat_num(cursor, parent_path_key)
                stat_num = self._get_stat_num(cursor, path_key)

        if stat is None:
            if not mutate:
                return MUST_MUTATE

            try:
                new_stat = OldStat(self._fs.stat(path))
            except FileNotFoundError:
                new_stat = None

            with self._get_db_conn() as conn, \
                 trans(conn, self._db_lock, is_exclusive=True), contextlib.closing(conn.cursor()) as cursor:
                # Only update metadata cache the path entry hasn't changed
                # and it's parent hasn't changed
                if (parent_stat_num == self._get_stat_num(cursor, parent_path_key) and
                    stat_num == self._get_stat_num(cursor, path_key)):
                    self._update_md(cursor, path, new_stat)

            stat = new_stat
        elif stat is DELETED:
            stat = None

        if stat is None:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

        return stat

    def _stat(self, path: fsabc.Path) -> OldStatProtocol:
        mutate = False

        while True:
            res = self._stat_repeat(mutate, path)
            if res is MUST_MUTATE:
                mutate = True
                continue
            return res

    def stat(self, path: fsabc.Path) -> fsabc.Stat:
        return NewStat(self._stat(path))

    def fstat(self, fobj):
        return NewStat(fobj.stat())

    def x_create_watch(self, cb, handle, *n, **kw):
        # This isinstance is arguably okay because handles are opaque objects
        # returned from open()
        assert isinstance(handle._live_md.cached_file, CachedDirectory)
        return self._fs.x_create_watch(cb, handle._live_md.cached_file._file, *n, **kw)

    def fsync(self, fobj):
        return fobj.sync()

    def unlink(self, path):
        self._fs.unlink(path)
        md = dropbox.files.DeletedMetadata(name=path.name,
                                           path_lower=str(path.normed()))
        self._handle_changes([md])

    def mkdir(self, path):
        self._fs.mkdir(path)
        self._invalidate_path(path)

    def rmdir(self, path):
        self._fs.rmdir(path)
        md = dropbox.files.DeletedMetadata(name=path.name,
                                           path_lower=str(path.normed()))
        self._handle_changes([md])

    def replace(self, oldpath: fsabc.Path, newpath: fsabc.Path) -> None:
        assert isinstance(oldpath, Path)
        assert isinstance(newpath, Path)

        self._fs.replace(oldpath, newpath)
        old_path_norm = str(oldpath.normed())
        new_path_norm = str(newpath.normed())

        # Invalidate cache entries for old path tree, and new path
        with self._get_db_conn() as conn, \
             trans(conn, self._db_lock, is_exclusive=True), contextlib.closing(conn.cursor()) as cursor:
            # TODO: send renamed directories to _refresh_thread

            # Clear new path's, new path's parent's, and old path's parent's entries
            cursor.executemany("DELETE FROM md_cache_entries WHERE path_key = ?",
                               [(new_path_norm,), (str(newpath.parent.normed()),),
                                (str(oldpath.parent.normed()),)])

            # Clear new path
            cursor.execute("DELETE FROM md_cache WHERE path_key = ?",
                           (new_path_norm,))

            cursor.executemany("update md_cache_counter set counter = counter + 1 "
                               "where path_key = ?",
                               [(new_path_norm,), (str(newpath.parent.normed()),),
                                (str(oldpath.parent.normed()),)])

            # Clear all old children's entries
            cursor.execute("DELETE FROM md_cache_entries "
                           "WHERE path_key = ? or path_key like ? || '/%'",
                           (old_path_norm, old_path_norm,))

            # Clear all old children
            cursor.execute("DELETE FROM md_cache WHERE path_key = ? or path_key like ? || '/%'",
                           (old_path_norm, old_path_norm,))
            cursor.execute("update md_cache_counter set counter = counter + 1 "
                           "where path_key = ? or path_key like ? || '/%'",
                           (old_path_norm, old_path_norm,))

    def statvfs(self):
        if self._statvfs is None:
            vfs = quick_container(f_frsize=DOWNLOAD_UNIT,
                                  f_blocks=0,
                                  f_bavail=0)
        else:
            vfs = self._statvfs
        return quick_container(f_frsize=DOWNLOAD_UNIT,
                               f_namemax=getattr(vfs, 'f_namemax', 255),
                               f_blocks=(vfs.f_blocks * vfs.f_frsize) // DOWNLOAD_UNIT,
                               f_bavail=(vfs.f_bavail * vfs.f_frsize) // DOWNLOAD_UNIT)

    def preadinto(self, handle, buf, offset):
        return handle.preadinto(buf, offset)

    def pwrite(self, handle, data, offset):
        return handle.pwrite(data, offset)

    def ftruncate(self, handle, offset):
        return handle.ptruncate(offset)

    def futimes(self, handle: fsabc.File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        # TODO: we only wrap dbxfs but if we wrapped anything else
        #       we'd need to update the times in the metadata database
        return self._fs.futimes(handle, times=times)

def main(argv: typing.Optional[Sequence[str]]) -> int:
    logging.basicConfig(level=logging.DEBUG)

    # This runtime import is okay because it happens in main()
    from userspacefs.memoryfs import FileSystem as MemoryFileSystem

    backing_fs = MemoryFileSystem([("foo", {"type": "directory",
                                            "children" : [
                                                ("baz", {"type": "file", "data": b"YOOOO"}),
                                                ("quux", {"type": "directory"}),
                                            ]
                                        }),
                                   ("bar", {"type": "file", "data": b"f"})])

    tmp_dir = tempfile.mkdtemp()
    fs = None
    try:
        fs = FileSystem(backing_fs, cache_folder=tmp_dir)

        # Test Directory listing
        def list_fs(fs: fsabc.FileSystem) -> None:
            print("Complete File Listing:")
            q = [fs.create_path()]
            while q:
                path = q.pop()

                stat = OldStat(fs.stat(path))
                print(path, stat.type, stat.id)

                with contextlib.closing(fs.open(path, os.O_RDONLY)) as f:
                    try:
                        data = f.read()
                    except IsADirectoryError:
                        assert stat.type == "directory"
                    else:
                        assert stat.type == "file"
                        print(" Contents:", data)

                try:
                    dir_handle = OldDirectory(fs.open_directory(path))
                except NotADirectoryError:
                    assert stat.type != "directory"
                else:
                    assert stat.type == "directory"
                    with contextlib.closing(dir_handle) as dir_:
                        for n in dir_:
                            q.append(path.joinpath(n.name))

        list_fs(fs)

        # Do it again to test caching
        list_fs(fs)

        # now write to a file
        with contextlib.closing(fs.open(fs.create_path("bar"), os.O_RDWR)) as f:
            f.read()
            f.write(b"hi")
            fs.fsync(f)
            f.seek(0)
            contents = f.read()
            if contents != b"fhi":
                print("Contents of bar:", contents, "(should be 'fhi')")
                return 1

        with contextlib.closing(fs.open(fs.create_path("bar"))) as f:
            contents = f.read()
            if contents != b"fhi":
                print("Contents of bar:", contents, "(should be 'fhi')")
                return 1

        # now create new file
        with contextlib.closing(fs.open(fs.create_path("newcrazy"),
                                        os.O_CREAT | os.O_WRONLY)) as f:
            f.write(b'test')

        try:
            with contextlib.closing(fs.open(fs.create_path("newcrazy"),
                                            os.O_CREAT | os.O_EXCL)) as f:
                pass
        except FileExistsError:
            # should throw
            pass
        else:
            raise Exception("Didn't throw on EXCL!")

        with contextlib.closing(fs.open(fs.create_path("newcrazy"),
                                        os.O_CREAT | os.O_RDONLY)) as f:
            print("Contents of bar:", f.read(), "(should be 'test')")

        fs.unlink(fs.create_path("newcrazy"))

        try:
            with contextlib.closing(fs.open(fs.create_path("newcrazy"))) as f:
                print("Contents of bar:", f.read(), "(should be '')")
        except FileNotFoundError:
            pass
        else:
            raise Exception("Didn't throw on file not found!!")

        fs.mkdir(fs.create_path("newdir"))

        try:
            fs.mkdir(fs.create_path("newdir"))
        except FileExistsError:
            pass
        else:
            raise Exception("Didn't throw file exists error!!")

        with fs.open(fs.create_path("newdir", "test-file"), os.O_CREAT | os.O_WRONLY) as f:
            f.write(b"TEST AGAIN")

        with fs.open(fs.create_path("newdir", "test-file")) as f:
            print("Contents of newdir/test-file: %r (should be b'TEST AGAIN')" %
                  (f.read(),))

        try:
            fs.rmdir(fs.create_path("newdir"))
        except OSError as e:
            if e.errno not in (errno.EEXIST, errno.ENOTEMPTY):
                # Not expected
                raise
        else:
            raise Exception("Expected not empty error")

        fs.unlink(fs.create_path("newdir", "test-file"))
        fs.rmdir(fs.create_path("newdir"))

        root_path = fs.create_path()
        file_path_4 = root_path.joinpath("dbfs-test-file.txt")

        with fs.open(file_path_4, os.O_CREAT) as f:
            pass

        file_path_5 = file_path_4.parent.joinpath("dbfs-test-file-2.txt")

        try:
            fs.unlink(file_path_5)
        except FileNotFoundError:
            pass

        fs.replace(file_path_4, file_path_5)

        try:
            with fs.open(file_path_4) as f:
                pass
        except FileNotFoundError:
            # expected
            pass
        else:
            raise Exception("expected file not found error!")

        fs.unlink(file_path_5)

        return 0
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if fs is not None:
            fs.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
