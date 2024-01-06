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

import codecs
import collections
import contextlib
import datetime
import errno
import http.client
import io
import json
import logging
import os
import random
import threading
import time
import typing
import sqlite3
import ssl
import stat
import sys
import urllib
import urllib.parse
import urllib.request

import email.utils as eut

from collections.abc import Iterator

import dropbox # type: ignore

import userspacefs.abc as fsabc
from userspacefs.path_common import Path
from userspacefs.util_dumpster import PositionIO, quick_container, IterableDirectory, datetime_now, NewStat, NewDirectory

log = logging.getLogger(__name__)

if not hasattr(os, 'O_ACCMODE'):
    O_ACCMODE = 0x3
    for accmode in (os.O_RDONLY, os.O_WRONLY, os.O_RDWR):
        assert (O_ACCMODE & accmode) == accmode
else:
    O_ACCMODE = os.O_ACCMODE

STAT_ATTRS = ["name", "type", "size", "mtime", "id", "ctime", "rev"]
Stat = collections.namedtuple("Stat", ["name", "type", "size", "mtime", "id", "ctime", "rev", 'attrs'])
_StatObject = Stat

def db_datetime_to_aware_datetime(dt):
    if dt.tzinfo is None:
        # dropbox used to use or still uses UTC datetimes without tzinfo, just add tzinfo
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt

def aware_datetime_to_db_datetime(dt):
    assert dt.tzinfo is not None
    # dropbox accepts tz aware datetimes, but they need to be in utc
    return dt.astimezone(datetime.timezone.utc)

def _md_to_stat(fs, md):
    name = md.name
    type = 'directory' if isinstance(md, dropbox.files.FolderMetadata) else 'file'
    size = 0 if isinstance(md, dropbox.files.FolderMetadata) else md.size
    mtime = (db_datetime_to_aware_datetime(md.client_modified)
             if not isinstance(md, dropbox.files.FolderMetadata) else
             datetime_now())
    ctime = (db_datetime_to_aware_datetime(md.server_modified)
             if hasattr(md, 'server_modified') else
             datetime_now())
    rev = ('rev:' + md.rev
           if type == "file" else
           None)
    return _StatObject(name, type, size, mtime, md.id, ctime=ctime, rev=rev,
                       attrs=STAT_ATTRS)

def md_to_stat(fs, md):
    return NewStat(_md_to_stat(fs, md))

class _Directory(IterableDirectory):
    def __init__(self, fs, path):
        self._fs = fs
        self._path = path

        self._md = self.__it()
        # Provoke initial list_folder() call
        ret = next(self._md)
        assert ret is None

    def __it(self) -> Iterator[Stat | None]:
        start = None
        self._cursor = None
        stop = False
        while not stop:
            if self._cursor is None:
                path_ = "" if self._path == "/" else self._path
                try:
                    res = self._fs._clientv2.files_list_folder(path_)
                    # XXX: Hack: we "snapshot" this directory by not returning entries
                    #      newer than the moment this iterator was started
                    start = self._fs._get_response_datetime()
                except dropbox.exceptions.ApiError as e:
                    if e.error.is_path():
                        if e.error.get_path().is_not_found():
                            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT)) from e
                        elif e.error.get_path().is_not_folder():
                            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR)) from e
                    raise
                yield None
            else:
                res = self._fs._clientv2.files_list_folder_continue(self._cursor)

            for f in res.entries:
                if isinstance(f, dropbox.files.DeletedMetadata):
                    continue
                if (isinstance(f, dropbox.files.FileMetadata) and
                    db_datetime_to_aware_datetime(f.server_modified) > start):
                    stop = True
                    break
                yield _md_to_stat(self._fs, f)

            self._cursor = res.cursor

            if not res.has_more:
                stop = True

    def close(self) -> None:
        pass

    def __iter__(self) -> typing.Self:
        return self

    def __next__(self) -> Stat:
        ret = next(self._md)
        assert ret is not None
        return ret

class DropboxAPIError(Exception):
    def __init__(self, json_):
        super().__init__(json_)

class HTTPError(Exception):
    pass

HTTP_TIMEOUT=30

def make_https_connection(target_host_port):
    ssl_context = ssl.create_default_context()
    ca_bundle = os.getenv("REQUESTS_CA_BUNDLE")
    if ca_bundle is not None:
        ssl_context.load_verify_locations(ca_bundle)

    proxy = os.getenv("HTTPS_PROXY")
    if proxy is not None:
        o = urllib.parse.urlparse(proxy)
        conn = http.client.HTTPSConnection(o.hostname, o.port, timeout=HTTP_TIMEOUT, context=ssl_context)
        conn.set_tunnel(*target_host_port)
    else:
        conn = http.client.HTTPSConnection(*target_host_port, timeout=HTTP_TIMEOUT, context=ssl_context)

    return conn

def download_connection(access_token, path, start=None, length=None):
    target_host_port = ("content.dropboxapi.com", 443)

    finished = False

    conn = make_https_connection(target_host_port)
    try:
        args = {"path" : path}

        path = "/2/files/download?" + urllib.parse.urlencode({'arg' : json.dumps(args)})

        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(access_token)

        if start is not None:
            if length is not None:
              headers['Range'] = 'bytes=%s-%s' % (start, start + length - 1)
            else:
              headers['Range'] = 'bytes=%s-' % start
        elif length is not None:
            headers['Range'] = 'bytes=-%s' % length

        log.info("Request to %s", path)
        conn.request("GET", path, None, headers)
        resp = conn.getresponse()
        try:
            if resp.status == 409:
                reader = codecs.getreader("utf-8")
                error = json.load(reader(resp))
                raise DropboxAPIError(error)
            elif resp.status not in (200, 206):
                data = resp.read()
                raise HTTPError(resp.status)

            log.info('https://%s:%d "GET %s HTTP/1.1" %d', target_host_port[0], target_host_port[1], path, resp.status)

            md = json.loads(resp.getheader("dropbox-api-result"))

            finished = True

            return (md, resp, conn)
        finally:
            if not finished:
                resp.close()
    finally:
        if not finished:
            conn.close()

class _File(PositionIO):
    readbehind: typing.ClassVar = 0
    readbehind_lock: typing.ClassVar = threading.Lock()

    def __init__(self, fs, path):
        super().__init__()
        self._fs = fs
        self._path = path
        self.requests_lock = threading.Lock()
        self.download_lock = threading.Condition()
        self.http_request = None
        self.requests = []

    def close(self):
        with self.download_lock:
            if self.http_request is not None:
                self.http_request['stream'].close()
                self.http_request = None

    def _try_request(self, wait_dict):
        with self.download_lock:
            offset = wait_dict['offset']
            size = wait_dict['size']

            # check if our request was fulfilled
            if wait_dict['amt_read'] is not None:
                log.debug("We already had data! %r", (offset, size))
                toret = wait_dict['amt_read']
                with self.requests_lock:
                    self.requests.remove(wait_dict)
                wait_dict = None
                return toret

            # wait on condition here
            if self.http_request is not None:
                # check if we have a request at the current http request,
                # if so and we are not that request, then wait
                with self.requests_lock:
                    local_requests = list(self.requests)
                found = False
                for r in local_requests:
                    if r['offset'] == self.http_request['offset']:
                        found = True
                        break
                # if there was a request at the current http request
                # then release lock and let another thread try
                if found and r is not wait_dict:
                    return None

            cls = type(self)

            if (self.http_request is not None and
                0 <= offset - self.http_request['offset'] <= cls.readbehind):
                http_request = self.http_request
            else:
                # make new http request
                http_request = {}
                http_request['offset'] = max(0, offset - self.readbehind)
                http_request['stream'] = _ReadStream(self._fs, self._path,
                                                     offset=http_request['offset'])

                if self.http_request is not None:
                    self.http_request['stream'].close()
                self.http_request = http_request

            request_size = offset - self.http_request['offset']
            request_offset = self.http_request['offset']

            log.debug("Request at %r", (request_offset, request_size + size))

            # download requests

            # first download all readbehind data before our specific request

            toread = request_size + size
            buf = bytearray(request_size)
            data = memoryview(buf)
            while toread > size:
                amt = http_request['stream'].readinto(data[size + request_size - toread:])
                if not amt:
                    # eof
                    break
                toread -= amt

            data = data[:size + request_size - toread]
            http_request['offset'] += len(data)

            if toread == size:
                # now download our request. we do it in two sections
                # so that we don't copy our request twice
                our_buf = memoryview(wait_dict['buf'])
                while toread > 0:
                    amt = http_request['stream'].readinto(our_buf[size - toread:])
                    if not amt:
                        # eof
                        break
                    toread -= amt

                wait_dict['amt_read'] = size - toread
                http_request['offset'] += size - toread
            else:
                # EOF
                wait_dict['amt_read'] = 0

            with self.requests_lock:
                local_requests = list(self.requests)

            # find earliest adjacent request, this dictates what our "readbehind"
            # will be in proceding downloads
            local_requests.sort(key=lambda x: x['offset'])
            ridx = local_requests.index(wait_dict)
            assert ridx >= 0
            idx = ridx
            while idx >= 1:
                if (local_requests[idx - 1]['offset'] + local_requests[idx - 1]['size'] ==
                    local_requests[idx]['offset']):
                    idx -= 1
                else:
                    break
            adj_back_offset = local_requests[idx]['offset']
            idx = ridx
            while idx < len(local_requests) - 1:
                if (local_requests[idx + 1]['offset'] ==
                    local_requests[idx]['offset'] + local_requests[idx]['size']):
                    idx += 1
                else:
                    break
            adj_front_offset = local_requests[idx]['offset']

            new_readbehind = adj_front_offset - adj_back_offset
            assert new_readbehind >= 0

            with cls.readbehind_lock:
                if new_readbehind > cls.readbehind:
                    log.debug("New readbehind %r (was %r)", new_readbehind, cls.readbehind)
                    cls.readbehind = new_readbehind

            # fulfill all requests
            for req in local_requests:
                if (req['offset'] >= request_offset and
                    req['offset'] + req['size'] <= request_offset + request_size):
                    read_buf = data[req['offset'] - request_offset :
                                    req['offset'] - request_offset + req['size']]
                    req['buf'][:len(read_buf)] = read_buf
                    req['amt_read'] = len(read_buf)

            # return
            toret = wait_dict['amt_read']
            assert wait_dict['amt_read'] is not None
            with self.requests_lock:
                self.requests.remove(wait_dict)
            wait_dict = None
            return toret

    def preadinto(self, buf, offset):
        wait_dict = dict(offset=offset, size=len(buf), buf=buf, amt_read=None)

        # put request in request list
        with self.requests_lock:
            self.requests.append(wait_dict)

        try:
            # wait to do download requests:
            while True:
                res = self._try_request(wait_dict)
                if res is not None:
                    wait_dict = None
                    return res
        finally:
            if wait_dict is not None:
                with self.requests_lock:
                    self.requests.remove(wait_dict)

    def readable(self):
        return True

    def stat(self):
        return self._fs._get_md(self._path)

# NB: now only used as a connection management helper for _File
class _ReadStream(io.RawIOBase):
    def __init__(self, fs, path, offset=None):
        self._fs = fs
        self._path = path
        self._offset = 0
        self._lock = threading.Lock()
        self._read_conn = None
        self._real_conn = None
        if offset is None:
            offset = 0
        assert offset >= 0
        self._start_offset = offset

    def readinto(self, buf):
        with self._lock:
            if self._path is None:
                raise ValueError("closed!")
            while True:
                if self._read_conn is None:
                    assert self._real_conn is None
                    try:
                        (_, self._read_conn, self._real_conn) = download_connection(self._fs._get_access_token(),
                                                                                    self._path,
                                                                                    start=self._start_offset)
                    except DropboxAPIError as e:
                        log.warning("API ERROR!")
                        if (e.args[0]['error']['.tag'] == "path" and
                            e.args[0]['error']['path']['.tag'] == "not_file"):
                            raise OSError(errno.EISDIR, os.strerror(errno.EISDIR)) from None
                        else: raise
                    except HTTPError as e:
                        if e.args[0] != 416:
                            raise
                        # range not satifiable, just return EOF stream
                        self._read_conn = io.BytesIO()
                    else:
                        range_was_honored = self._read_conn.getheader("content-range")
                        if not range_was_honored:
                            # handle case where range isn't honored because
                            # offset is past the EOF
                            content_length = self._read_conn.getheader('content-length')
                            if (content_length is not None and
                                self._start_offset >= int(content_length)):
                                # turn read_conn into EOF stream
                                self._read_conn.close()
                                self._read_conn = io.BytesIO()
                            else:
                                log.warning("Range wasn't honored: %r", (offset, size))

                                # read until start offset
                                toread = self._start_offset
                                while toread:
                                    toread = min(2 ** 16, toread)
                                    c = self._read_conn.read(toread)
                                    if not c: break
                                    toread -= len(c)

                try:
                    toret = self._read_conn.readinto(buf)
                except Exception:
                    log.info("Download connection failure", exc_info=True)
                    # if we have a failure while reading from the http response
                    # then kill connection and try to make it again. if at that point
                    # we fail to re-establish the connection, then fail the entire routine.
                    self._read_conn.close()
                    self._read_conn = None
                    self._real_conn.close()
                    self._real_conn = None
                    continue
                self._start_offset += toret
                return toret

    def readable(self):
        return True

    def close(self):
        if self.closed:
            return
        with self._lock:
            if self._read_conn is not None:
                self._read_conn.close()
            self._read_conn = None
            if self._real_conn is not None:
                self._real_conn.close()
            self._real_conn = None
            # Set path to none to signal closed
            self._path = None
        super().close()

ApiError = dropbox.exceptions.ApiError

def new_files_upload(client, f, path,
                     mode=dropbox.files.WriteMode.add,
                     autorename=False,
                     strict_conflict=False,
                     client_modified=None):
    return client.files_upload(f, path,
                               mode=mode, autorename=autorename,
                               strict_conflict=strict_conflict,
                               client_modified=client_modified)

def new_files_upload_session_finish(client,
                                    buf, cursor,
                                    ci):
    commit = dict(
        path=ci['path'],
        mode=ci.get('mode', dropbox.files.WriteMode.add),
        autorename=ci.get('autorename', False),
        strict_conflict=ci.get('strict_conflict', False),
    )
    if 'client_modified' in ci:
        commit['client_modified'] = ci['client_modified']
    return client.files_upload_session_finish(
        buf, cursor, dropbox.files.CommitInfo(**commit),
    )

BUF_SIZE = 4 * 1024 * 1024
class _WriteStream(object):
    def __init__(self, fs):
        self._fs = fs
        self._session_id = None
        self._buf = io.BytesIO()
        self._lock = threading.Lock()
        self._offset = 0

    def _flush(self):
        to_up = bytes(self._buf.getbuffer()[:BUF_SIZE])

        if self._session_id is None:
            # start session
            session_result = self._fs._clientv2.files_upload_session_start(to_up)
            self._session_id = session_result.session_id
        else:
            self._fs._clientv2.files_upload_session_append(to_up, self._session_id, self._offset)

        self._offset += len(to_up)

        self._buf = io.BytesIO(self._buf.getbuffer()[BUF_SIZE:])

    def write(self, buf):
        with self._lock:
            self._buf.write(buf)

            while len(self._buf.getbuffer()) >= BUF_SIZE:
                self._flush()

    def finish(self, path, mode='add', strict_conflict=False,
               mtime=None):
        if mode == 'add':
            mode = dropbox.files.WriteMode.add
        elif mode == 'overwrite':
            mode = dropbox.files.WriteMode.overwrite
        else:
            assert (isinstance(mode, tuple) and
                    mode[0] == 'update' and
                    mode[1][:4] == 'rev:')
            mode = dropbox.files.WriteMode.update(mode[1][4:])

        if isinstance(path, Path):
            path = str(path)

        if mtime is not None:
            mtime = aware_datetime_to_db_datetime(mtime)

        with self._lock:
            # Only flush to upload session if we've flushed before
            # otherwise we'll cut straight to upload()
            if self._session_id is not None:
                while len(self._buf.getbuffer()) >= BUF_SIZE:
                    self._flush()

                cursor = dropbox.files.UploadSessionCursor(self._session_id,
                                                           self._offset)
                try:
                    arg = dict(
                        path=path,
                        mode=mode,
                        strict_conflict=strict_conflict
                    )
                    if mtime is not None:
                        arg['client_modified'] = mtime
                    md = new_files_upload_session_finish(
                        self._fs._clientv2,
                        bytes(self._buf.getbuffer()), cursor,
                        arg,
                    )
                except ApiError as e:
                    if (e.error.is_path() and
                        e.error.get_path().is_conflict()):
                        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST)) from e
                    raise
            else:
                assert len(self._buf.getbuffer()) < BUF_SIZE
                try:
                    md = new_files_upload(self._fs._clientv2,
                                            bytes(self._buf.getbuffer()), path,
                                            mode=mode,
                                            strict_conflict=strict_conflict,
                                            client_modified=mtime)
                except ApiError as e:
                    if (e.error.is_path() and
                        e.error.get_path().reason.is_conflict()):
                        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST)) from e
                    raise

            return md_to_stat(self._fs, md)

    def close(self):
        # Ideally we would eagerly clean up the session_id, but API
        # doesn't provide that
        pass

Change = collections.namedtuple('Change', ['action', 'path'])

(FILE_NOTIFY_CHANGE_FILE_NAME,
 FILE_NOTIFY_CHANGE_DIR_NAME,
 FILE_NOTIFY_CHANGE_ATRIBUTES,
 FILE_NOTIFY_CHANGE_SIZE,
 FILE_NOTIFY_CHANGE_LAST_WRITE,
 FILE_NOTIFY_CHANGE_LAST_ACCESS,
 FILE_NOTIFY_CHANGE_CREATION,
 FILE_NOTIFY_CHANGE_EA,
 FILE_NOTIFY_CHANGE_SECURITY,
 FILE_NOTIFY_CHANGE_STREAM_NAME,
 FILE_NOTIFY_CHANGE_STREAM_SIZE,
 FILE_NOTIFY_CHANGE_STREAM_WRITE) = map(lambda x: 1 << x, range(12))

def delta_thread(dbfs):
    cursor = None
    needs_reset = True
    while not dbfs._closed:
        try:
            if cursor is None:
                cursor = dbfs._clientv2.files_list_folder_get_latest_cursor('', True).cursor
            res = dbfs._clientv2.files_list_folder_continue(cursor)
        except Exception as e:
            if isinstance(e, dropbox.files.ListFolderContinueError):
                cursor = None
                needs_reset = True
            elif not isinstance(e, OSError):
                log.exception("failure while doing list folder, sleeping for 60 seconds")
            else:
                # TODO: this should be exponential backoff
                log.info("List error, sleeping for 60 seconds")

            time.sleep(60)
            continue

        with dbfs._watches_lock:
            watches = list(dbfs._watches)

        for watch in watches:
            if needs_reset:
                watch('reset')
            if res.entries:
                watch(res.entries)

        needs_reset = False

        cursor = res.cursor
        if not res.has_more:
            try:
                while True:
                    res = dbfs._clientv2.files_list_folder_longpoll(cursor)
                    if dbfs._closed or res.changes:
                        break
                    if res.backoff is not None:
                        log.info("List backoff, sleeping for %r seconds", res.backoff)
                        time.sleep(res.backoff)
            except OSError:
                pass
            except Exception:
                log.exception("failure during longpoll")

class FileSystem(fsabc.FileSystemG[Path, _File]):
    def __init__(self, client_kwargs):
        self._access_token = client_kwargs.get('oauth2_access_token')
        self._access_token_expire = None
        self._client_kwargs = client_kwargs
        self._local = threading.local()
        self._watches = []
        self._watches_lock = threading.Lock()
        self._closed = False
        self._access_token_lock = threading.Lock()

        # share this session (i.e. connection pool) across threads
        if 'session' in self._client_kwargs:
            raise Exception("Can't override 'session' argument")
        self._client_kwargs['session'] = self._create_session()

        # kick off delta thread
        threading.Thread(target=delta_thread, args=(self,), daemon=True).start()

    def _get_access_token(self):
        with self._access_token_lock:
            return self._get_access_token_unlocked()

    def _get_access_token_unlocked(self):
        if (self._access_token is not None and
            (self._access_token_expire is None or time.monotonic() < self._access_token_expire)):
            return self._access_token

        assert self._client_kwargs['oauth2_refresh_token'] is not None
        assert self._client_kwargs['app_key'] is not None

        target_host_port = ("api.dropboxapi.com", 443)

        conn = make_https_connection(target_host_port)

        args = {
            "grant_type" : "refresh_token",
            "refresh_token": self._client_kwargs['oauth2_refresh_token'],
            'client_id': self._client_kwargs['app_key'],
        }

        path = "/oauth2/token"

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }

        log.info('Request to %s', path)
        conn.request("POST", path, urllib.parse.urlencode(args), headers)
        resp = conn.getresponse()
        log.info('https://%s:%d "POST %s HTTP/1.1" %d', target_host_port[0], target_host_port[1], path, resp.status)

        if resp.status != 200:
            data = resp.read()
            raise HTTPError(resp.status)

        md = json.load(resp)

        self._access_token_expire = time.monotonic() + int(md['expires_in'])
        self._access_token = md['access_token']

        return self._access_token

    def _create_session(self):
        session = dropbox.create_session()

        old_session_post = session.post
        def new_session_post(*n, **kw):
            r = old_session_post(*n, **kw)
            self._local.r = r
            return r
        session.post = new_session_post

        return session

    def _get_response_datetime(self):
        return eut.parsedate_to_datetime(self._local.r.headers['Date'])

    def _add_watch(self, watch_fn):
        with self._watches_lock:
            self._watches.append(watch_fn)

    def _remove_watch(self, watch_fn):
        with self._watches_lock:
            self._watches.remove(watch_fn)

    def close(self):
        if self._closed:
            return
        self._closed = True

    def create_path(self, *args):
        return Path([], fn_norm=self.file_name_norm).joinpath(*args)

    def parse_path(self, p):
        return Path.parse_path(p, fn_norm=self.file_name_norm)

    def file_name_norm(self, n):
        # XXX: not all upper<->lower characters are equivalent in Dropbox
        return n.lower()

    # NB: This is probably evil opaque magic
    @property
    def _clientv2(self) -> dropbox.Dropbox:
        toret = getattr(self._local, '_clientv2', None)
        if toret is None:
            self._local._clientv2 = toret = dropbox.Dropbox(**self._client_kwargs)
        return toret

    def _get_md_inner(self, path):
        log.debug("GET %r", path)
        try:
            # NB: allow for raw paths/id strings
            p = str(path)
            if p == '/':
                return dropbox.files.FolderMetadata(name="/", path_lower="/", id="/")
            md = self._clientv2.files_get_metadata(p)
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path():
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT)) from e
            else: raise
        return md

    def _get_md(self, path):
        md = self._get_md_inner(path)
        log.debug("md: %r", md)
        return md_to_stat(self, md)

    def _stat_create(self, path, mode=0, directory=False):
        if (mode & os.O_CREAT) and (mode & os.O_EXCL):
            if directory:
                try:
                    md = self._clientv2.files_create_folder(str(path))
                except dropbox.exceptions.ApiError as e:
                    if e.error.get_path().is_conflict():
                        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST)) from e
                    else:
                        raise
            else:
                try:
                    md = new_files_upload(self._clientv2, b'', str(path),
                                          strict_conflict=True)
                except dropbox.exceptions.ApiError as e:
                    if e.error.get_path().reason.is_conflict():
                        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST)) from e
                    else:
                        raise
        elif (mode & os.O_CREAT) and (mode & os.O_TRUNC) and not directory:
            md = self._clientv2.files_upload(b'', str(path),
                                             mode=dropbox.files.WriteMode.overwrite)
        else:
            while True:
                # NB: would be nice if dropbox API had an API for
                #     "create/get metadata" which is basically what stat_create() is
                try:
                    md = self._get_md_inner(path)
                except FileNotFoundError:
                    if not (mode & os.O_CREAT):
                        raise
                    md = None

                if md is None:
                    if directory:
                        try:
                            md = self._clientv2.files_create_folder(str(path))
                        except dropbox.exceptions.ApiError as e:
                            if e.error.get_path().is_conflict():
                                continue
                            else:
                                raise
                    else:
                        try:
                            md = self._clientv2.files_upload(b'', str(path))
                        except dropbox.exceptions.ApiError as e:
                            if e.error.is_path():
                                if e.error.get_path().reason.is_conflict():
                                    continue
                                if (e.error.get_path().reason.is_disallowed_name() or
                                    e.error.get_path().reason.is_malformed_path()):
                                    raise OSError(errno.EINVAL, os.strerror(errno.EINVAL)) from e
                                if e.error.get_path().reason.is_no_write_permission():
                                    raise OSError(errno.EACCES, os.strerror(errno.EACCES)) from e
                                if e.error.get_path().reason.is_insufficient_space():
                                    raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC)) from e
                            raise
                else:
                    if (not isinstance(md, dropbox.files.FolderMetadata) and
                        (mode & os.O_TRUNC)):
                        md = self._clientv2.files_upload(b'', str(path),
                                                         mode=dropbox.files.WriteMode.update(md.rev))
                break
        return md

    def x_stat_create(self, path, mode=0, directory=False):
        # x_stat_create() doesn't honor O_TRUNC (but open() does)
        return md_to_stat(self, self._stat_create(path, mode & ~os.O_TRUNC, directory))

    def _open_by_dbid(self, id_, mode):
        # NB: In general write mode is broken since writes don't propagate across
        #     file objects. Until Dropbox API provides Range-PUT there is no
        #     great way to implement it.
        if (O_ACCMODE & mode) != os.O_RDONLY:
            raise OSError(errno.EINVAL, os.strerror(errno.EINVAL))

        return _File(self, id_)

    def open(self, path, mode=os.O_RDONLY, directory=False):
        md = self._stat_create(path, mode, directory)

        # NB: we don't use x_open_by_id because that would require us
        #     to allocate an entry in the ID table.
        return self._open_by_dbid(md.id, mode)

    def x_stat_by_id(self, id_):
        return self._get_md(id_)

    def x_open_by_id(self, id_, mode=os.O_RDONLY):
        return self._open_by_dbid(id_, mode)

    def x_open_by_rev(self, rev):
        return _File(self, rev)

    def x_write_stream(self):
        return _WriteStream(self)

    def open_directory(self, path):
        return NewDirectory(_Directory(self, str(path)))

    def stat_has_attr(self, attr):
        return attr in STAT_ATTRS

    def stat(self, path):
        return self._get_md(path)

    def fstat(self, fobj):
        return fobj.stat()

    def x_create_watch(self, cb, dir_handle, completion_filter, watch_tree):
        # TODO: we don't support added, moved_from, or moved_to events

        # NB: _File just means it was opened with open()
        # (this includes directories)
        # This assert is okay because dir_handle is arguably okay because
        # handles are opaque objects returned from open()
        assert isinstance(dir_handle, _File)

        assert (str(dir_handle._path) == "/" or
                str(dir_handle._path).startswith("id:"))

        id_ = dir_handle._path
        dirpath = [None]
        done = [False]

        def watch_fn(entries):
            if entries == "reset":
                return cb("reset")

            process_delete = True
            if dirpath[0] is None:
                process_delete = False
                if id_ == "/":
                    dirpath[0] = id_
                else:
                    md = self._get_md_inner(id_)
                    dirpath[0] = md.path_lower

            to_sub = []
            ndirpath = dirpath[0]
            prefix_ndirpath = ndirpath + ("" if ndirpath == "/" else "/")

            for entry in entries:
                # XXX: this check is racy since this could be a stale
                #      delete from before we event retrieved the ID
                #      for this file. We minimize damage using
                #      `process_delete` but there is still chance of
                #      us getting stale data the next time we are
                #      called (though this should rarely occur in
                #      practice).
                if (process_delete and
                    isinstance(entry, dropbox.files.DeletedMetadata) and
                    entry.path_lower == ndirpath):
                    done[0] = True
                    continue

                if (not isinstance(entry, dropbox.files.DeletedMetadata) and
                    entry.id == id_):
                    dirpath[0] = md.path_lower
                    ndirpath = dirpath[0]
                    prefix_ndirpath = ndirpath + ("" if ndirpath == "/" else "/")
                    done[0] = False

                if done[0]:
                    continue

                # TODO: filter based on completion filter
                if not entry.path_lower.startswith(prefix_ndirpath):
                    continue
                if (not watch_tree and
                    entry.path_lower[len(prefix_ndirpath):].find("/") != -1):
                    continue
                path = self.create_path(*(([] if ndirpath == "/" else ndirpath[1:].split("/")) +
                                          [entry.name]))

                # TODO: pull initial directory entries to tell the difference
                #       "added" and "modified"
                action = ("removed"
                          if isinstance(entry, dropbox.files.DeletedMetadata) else
                          "modified")
                to_sub.append(Change(action, path.parts[1:]))

            if to_sub:
                try:
                    cb(to_sub)
                except:
                    log.exception("failure during watch callback")

        self._add_watch(watch_fn)

        def stop():
            self._remove_watch(watch_fn)

        return stop

    def x_create_db_style_watch(self, cb):
        self._add_watch(cb)

        def stop():
            self._remove_watch(cb)

        return stop

    def unlink(self, path):
        if path.parent == path:
            # Short-circuit on failing on root
            raise OSError(errno.EPERM, os.strerror(errno.EPERM))

        # NB: dropbox api provides no single-file delete call
        #     if a directory exists at this location, it will recursively
        #     delete everything
        try:
            md = self._clientv2.files_delete(str(path))
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path_lookup():
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT)) from e
            else:
                raise
        else:
            if isinstance(md, dropbox.files.FolderMetadata):
                log.warn("Called unlink() on directory and it succeeded: %r", path)

    def mkdir(self, path):
        st = self.x_stat_create(path, os.O_CREAT | os.O_EXCL, True)
        assert stat.S_ISDIR(st.st_mode)

    def rmdir(self, path):
        # NB: dropbox api provides no empty-directory delete call
        #     if there are files under this directory, this will delete them
        try:
            md = self._clientv2.files_delete(str(path))
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path_lookup():
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT)) from e
            else:
                raise
        else:
            if not isinstance(md, dropbox.files.FolderMetadata):
                log.warn("Called rmdir() on non-directory and it succeeded: %r", path)

    def _slow_rename(self, old_path: Path, new_path: Path) -> None:
        # only allow:
        # anything -> nothing
        # directory -> empty directory
        # file -> file

        while True:
            try:
                md = self._get_md_inner(new_path)
            except FileNotFoundError:
                md = None

            omd = self._get_md_inner(old_path)

            if md is None:
                pass
            elif isinstance(md, dropbox.files.FolderMetadata):
                if not isinstance(omd, dropbox.files.FolderMetadata):
                    raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))

                with self.open_directory(new_path) as d:
                    try:
                        next(iter(d))
                    except StopIteration:
                        children = False
                    else:
                        children = True

                if children:
                    raise OSError(errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY))
            else:
                if isinstance(omd, dropbox.files.FolderMetadata):
                    raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

            if md is not None:
                try:
                    self._clientv2.files_delete(str(new_path))
                except dropbox.exceptions.ApiError as e:
                    if not e.error.is_path_lookup():
                        raise

            try:
                return self._clientv2.files_move(str(old_path), str(new_path))
            except dropbox.exceptions.ApiError as e:
                if not (e.error.is_to() and
                        e.error.get_to().is_conflict()):
                    raise

    def x_rename_stat(self, old_path, new_path):
        try:
            md = self._clientv2.files_move(str(old_path), str(new_path))
        except dropbox.exceptions.ApiError as e:
            if (e.error.is_to() and
                e.error.get_to().is_conflict()):
                return self._slow_rename(old_path, new_path)
            raise
        return md_to_stat(self, md)

    def replace(self, old_path: Path, new_path: Path) -> None:
        self.x_rename_stat(old_path, new_path)

    def statvfs(self):
        ALLOCATION_UNIT_SIZE = 4 * 1024 * 1024
        space_usage = self._clientv2.users_get_space_usage()
        allocation = (space_usage.allocation.get_individual()
                      if space_usage.allocation.is_individual() else
                      space_usage.allocation.get_team()).allocated
        return quick_container(f_frsize=ALLOCATION_UNIT_SIZE,
                               f_blocks=allocation // ALLOCATION_UNIT_SIZE,
                               f_bavail=max(0, (allocation - space_usage.used) // ALLOCATION_UNIT_SIZE))

    def preadinto(self, handle, buf, offset):
        return handle.preadinto(buf, offset)

    def pwrite(self, handle, data, offset):
        raise OSError(errno.ENOSYS, os.strerror(errno.ENOSYS))

    def fsync(self, handle):
        pass

    def ftruncate(self, handle, offset):
        raise OSError(errno.ENOSYS, os.strerror(errno.ENOSYS))

    def futimes(self, file: _File,
                times: typing.Optional[typing.Tuple[float, float]] = None) -> None:
        raise OSError(errno.ENOSYS, os.strerror(errno.ENOSYS))

def main(argv):
    # run some basic tests on this class

    if sys.stdin.isatty():
        token = getpass.getpass("Access Token: ")
    else:
        token = sys.stdin.read()

    fs = FileSystem(dict(oauth2_access_token=token))

    root_path = fs.create_path()

    root_md = fs.stat(root_path)
    print("Root MD:", root_md)

    print("Root directory listting:")
    with contextlib.closing(fs.open_directory(root_path)) as f:
        for entry in f:
            if entry.type == "file":
                to_open = entry
            print("", entry)

    file_path = root_path.joinpath(to_open.name)
    file_md = fs.stat(file_path)
    print("File MD:", file_md)

    with contextlib.closing(fs.open(file_path)) as f:
        print("File Data: %r" % (f.read(4),))
        print("File Data 2: %r" % (f.read(4),))

    file_path_2 = root_path.joinpath("dbfs-test.txt")
    with contextlib.closing(fs.x_write_stream()) as f:
        f.write(b"test")
        f.finish(file_path_2, "overwrite")

    try:
        with contextlib.closing(fs.open(file_path_2, os.O_CREAT | os.O_EXCL)) as f:
            pass
    except FileExistsError:
        # Expected
        pass
    else:
        raise Exception("This should raise")

    event = threading.Event()
    def cb(changes):
        print(changes)
        event.set()

    root_file = fs.open(root_path)
    stop = fs.x_create_watch(cb, root_file, ~0, False)

    file_path_3 = root_path.joinpath("dbfs-test-dir")

    try:
        fs.mkdir(file_path_3)
    except FileExistsError:
        print("Directory already existed", file_path_3)

    try:
        fs.mkdir(file_path_3)
    except FileExistsError:
        # expected
        pass
    else:
        raise Exception("This should raise")

    fs.rmdir(file_path_3)

    file_path_4 = root_path.joinpath("dbfs-test-file.txt")

    with fs.open(file_path_4, os.O_CREAT) as f:
        pass

    file_path_5 = file_path_4.parent.joinpath("dbfs-test-file-2.txt")

    try:
        fs.unlink(file_path_5)
    except FileNotFoundError:
        pass

    fs.rename_noreplace(file_path_4, file_path_5)

    fs.unlink(file_path_5)

    print("Waiting for FS event for 10 seconds")
    if not event.wait(5 * 60):
        raise Exception("Event never came!")
    stop()

if __name__ == "__main__":
    import getpass
    sys.exit(main(sys.argv))
