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

import contextlib
import itertools
import threading
import traceback

class ConnPool(object):
    def __init__(self, create_fn):
        self._create_fn = create_fn
        self._conns = []
        self._cond = threading.Condition()
        self._total_conns = 0
        self._closed = False
        self._stack_closed_location = None

    @contextlib.contextmanager
    def get_conn(self):
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

    def close(self):
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
    def __init__(self):
        self.cond = threading.Condition()
        self.readers = 0
        self.want_write = 0
        self.writers = 0

    def _rep(self):
        if self.writers > 1 or self.writers < 0:
            return False

        if self.want_write < self.writers:
            return False

        if self.writers and self.readers:
            return False

        return True

    def acquire(self):
        with self.cond:
            assert self._rep()
            self.want_write += 1
            while self.readers or self.writers:
                self.cond.wait()
            self.writers += 1
            assert self._rep()

    def release(self):
        with self.cond:
            assert self._rep()
            self.writers -= 1
            self.want_write -= 1
            self.cond.notify_all()
            assert self._rep()

    def acquire_shared(self):
        with self.cond:
            assert self._rep()
            while self.want_write or self.writers:
                self.cond.wait()
            self.readers += 1
            assert self._rep()

    def release_shared(self):
        with self.cond:
            assert self._rep()
            self.readers -= 1
            self.cond.notify_all()
            assert self._rep()

    @contextlib.contextmanager
    def shared_context(self):
        self.acquire_shared()
        try:
            yield
        finally:
            self.release_shared()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *n):
        self.release()

@contextlib.contextmanager
def trans(conn, lock, is_exclusive=False):
    # NB: This exists because pysqlite will not start a transaction
    # until it sees a DML statement. This sucks if we start a transaction
    # with a SELECT statement.
    with (null_context()
          if lock is None else
          lock
          if is_exclusive else
          lock.shared_context()):
        begin_stmt = "BEGIN IMMEDIATE" if is_exclusive else "BEGIN DEFERRED"
        iso = conn.isolation_level
        conn.isolation_level = None
        try:
            conn.execute(begin_stmt)
            with conn:
                yield conn
        finally:
            conn.isolation_level = iso
