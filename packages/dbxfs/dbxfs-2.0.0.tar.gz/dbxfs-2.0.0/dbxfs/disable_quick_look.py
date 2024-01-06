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

import errno
import itertools
import logging
import os
import typing

import userspacefs.abc as fsabc
from userspacefs.memoryfs import FileSystem as MemoryFileSystem
from userspacefs.util_dumpster import OldDirectory, NewDirectory

log = logging.getLogger(__name__)

class QLDir(object):
    def __init__(self, *dirs):
        self._dirs = dirs
        self._curiter = self._myiter()

    def read(self):
        try:
            return next(self)
        except StopIteration:
            return None

    def readmany(self, size=None):
        if size is None:
            return list(self)
        else:
            return list(itertools.islice(self, size))

    def _myiter(self):
        for dir_ in self._dirs:
            yield from dir_

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._curiter)

    def close(self):
        for dir_ in self._dirs:
            dir_.close()
        self._dirs = ()

class QLFile(object):
    def __init__(self, f):
        self._f = f

    def __getattr__(self, name):
        return getattr(self._f, name)

class FileSystem(fsabc.FileSystem):
    def __init__(self, backing_fs):
        self._overlay  = MemoryFileSystem([(".ql_disablethumbnails", {"type": "file", "data": b""}),
                                           (".metadata_never_index", {"type": "file", "data": b""}),
                                           (".ql_disablecache", {"type": "file", "data": b""})])

        self._fs = backing_fs

    def close(self):
        if self._fs is None:
            return
        self._fs.close()
        self._fs = None

    def _filter(self, path):
        if (path.name.lower() == ".ds_store" or
            path == self.create_path(".TemporaryItems") or
            path == self.create_path(".Trashes")):
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))
        return path in [self.create_path(".ql_disablethumbnails"),
                        self.create_path(".metadata_never_index"),
                        self.create_path(".ql_disablecache")]

    def open(self, path, mode=os.O_RDONLY):
        if self._filter(path):
            return QLFile(self._overlay.open(self._overlay.create_path(*path.parts[1:])))
        return self._fs.open(path, mode=mode)

    def open_directory(self, path):
        dir_ = self._fs.open_directory(path)
        if path == self.create_path():
            dir_ = NewDirectory(QLDir(OldDirectory(self._overlay.open_directory(path)), OldDirectory(dir_)))
        return dir_

    def stat(self, path):
        if self._filter(path):
            return self._overlay.stat(self._overlay.create_path(*path.parts[1:]))
        return self._fs.stat(path)

    def fstat(self, fobj):
        if isinstance(fobj, QLFile):
            return self._overlay.fstat(fobj._f)
        return self._fs.fstat(fobj)

    def create_path(self, *parts: str) -> fsabc.Path:
        return self._fs.create_path(*parts)

    def fsync(self, file_: fsabc.File) -> None:
        self._fs.fsync(file_)

    def futimes(self, file_: fsabc.File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        self._fs.futimes(file_, times=times)

    def mkdir(self, path: fsabc.Path) -> None:
        self._fs.mkdir(path)

    def preadinto(self, file_: fsabc.File, buf: fsabc.Buffer, offset: int) -> int:
        return self._fs.preadinto(file_, buf, offset)

    def pwrite(self, file_: fsabc.File, data: fsabc.Buffer, offset: int) -> int:
        return self._fs.pwrite(file_, data, offset)

    def replace(self, oldpath: fsabc.Path, newpath: fsabc.Path) -> None:
        self._fs.replace(oldpath, newpath)

    def rmdir(self, path: fsabc.Path) -> None:
        return self._fs.rmdir(path)

    def statvfs(self) -> fsabc.StatVFS:
        return self._fs.statvfs()

    def unlink(self, path: fsabc.Path) -> None:
        return self._fs.unlink(path)

    def __getattr__(self, name):
        return getattr(self._fs, name)
