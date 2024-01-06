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

import argparse
import contextlib
import errno
import functools
import getpass
import io
import importlib.metadata
import json
import logging
import os
import subprocess
import sys
import time
import traceback
import types
import typing
import urllib.request
import urllib.error
import uuid
import webbrowser

from abc import abstractmethod
from collections.abc import Callable, Sequence

syslog: typing.Optional[types.ModuleType]
try:
    import syslog
except Exception:
    syslog = None

import platformdirs as appdirs

import dropbox # type: ignore

import privy # type: ignore

import userspacefs
from userspacefs.abc import FileSystem

import sentry_sdk

from block_tracing import block_tracing

dbxfs_gui: typing.Optional[types.ModuleType]
try:
    import dbxfs.gui as dbxfs_gui
except ModuleNotFoundError:
    dbxfs_gui = None

from dbxfs.dbxfs import FileSystem as DropboxFileSystem
from dbxfs.cachingfs import FileSystem as CachingFileSystem, check_runtime_requirements
from dbxfs.disable_quick_look import FileSystem as DisableQuickLookFileSystem
from dbxfs.translate_ignored_files import FileSystem as TranslateIgnoredFilesFileSystem

safefs_wrap_create_fs: typing.Optional[Callable]
safefs_add_fs_args: typing.Optional[Callable]
try:
    from dbxfs.safefs_glue import safefs_wrap_create_fs, safefs_add_fs_args
except ImportError:
    safefs_wrap_create_fs = None
    safefs_add_fs_args = None

log = logging.getLogger(__name__)

APP_NAME = "dbxfs"

# This exposure is intentional
APP_KEY = "iftkeq2y4qj0nbt"

DEFAULT_INSTANCE_GUID = "edbd8aa5-aca2-4d7b-bea0-791ed83f429c"

HOLD_MUTEX = None

def acquire_hold(instance_guid):
    # this is only implemented for windows currently
    if sys.platform != 'win32':
        return True

    import win32api
    import win32event
    import winerror

    global HOLD_MUTEX
    HOLD_MUTEX = win32event.CreateMutex(None, True, instance_guid)
    le = win32api.GetLastError()
    log.debug("Last error: %r, instance: %r", le, instance_guid)
    return le != winerror.ERROR_ALREADY_EXISTS

def allow_multiple(instance_guid, use_gui):
    # if we're not running frozen, the user presumably knows what they
    # are doing, so we permit multiple instances
    if not getattr(sys, 'frozen', False):
        return True

    # this is only implemented for windows currently
    if sys.platform != 'win32':
        return True

    import win32gui
    import win32com.client

    def get_disks():
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer, "root\\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
        return colItems

    # create mutex with guid
    if not acquire_hold(instance_guid):
        if use_gui:
            win = win32gui.FindWindow(None, "dbxfs")
            if win:
                win32gui.SetForegroundWindow(win)
            else:
                for disk in get_disks():
                    if disk.ProviderName is not None and disk.ProviderName.endswith("\\dbxfs"):
                        subprocess.run(["start", disk.name], shell=True)
        else:
            print("Another instance already running")
        return False

    return True

def yes_no_input(message: typing.Optional[str] = None,
                 default_yes: bool = False) -> bool:
    if default_yes:
        extra = "[Y/n]"
    else:
        extra = "[y/N]"
    answer = input("%s%s " % (message + ' ' if message is not None else '', extra))
    while answer.lower().strip() not in ("y", "n", "yes", "no", ""):
        print("Please answer yes or no!")
        answer = input("%s%s " % (message + ' ' if message is not None else '', extra))
    if not answer.lower().strip():
        return default_yes
    return answer.lower().startswith('y')

class UIProtocol(typing.Protocol):
    @abstractmethod
    def can_interact(self) -> bool:
        ...

    @abstractmethod
    def yes_no_input(self, message: typing.Optional[str] = None,
                     default_yes: bool = False) -> bool:
        ...

    @abstractmethod
    def link_dbxfs(self, authorize_url: str) -> str:
        ...

    @abstractmethod
    def getpass(self, label: str) -> str:
        ...

    @abstractmethod
    def create_pass(self, header: str) -> str:
        ...

class ConsoleUI(UIProtocol):
    def can_interact(self) -> bool:
        return (sys.stdout is not None and sys.stdout.isatty())

    def warning(self, message: str) -> None:
        if sys.platform != "win32":
            print("\033[0;31m\033[1m", end='')
        print("Warning: %s" % (message,), end='')
        if sys.platform != "win32":
            print("\033[0;0m")
        else:
            print()

    def error(self, message: str) -> None:
        if sys.platform != "win32":
            print("\033[0;31m\033[1m", end='')
        print("Error: %s" % (message,), end='')
        if sys.platform != "win32":
            print("\033[0;0m")
        else:
            print()

    def yes_no_input(self, message: typing.Optional[str] = None,
                     default_yes: bool = False) -> bool:
        if not self.can_interact():
            print("Error: need an interactive shell")
            raise Exception()

        return yes_no_input(message, default_yes=default_yes)

    def link_dbxfs(self, authorize_url: str) -> str:
        if not self.can_interact():
            print("Error: run in an interactive shell to obtain a new refresh token")
            raise Exception()

        print("We need a refresh token. Perform the following steps:")
        print("1. Go to " + authorize_url)
        print("2. Click \"Allow\" (you may have to log in first)")
        print("3. Copy the authorization code.")

        while True:
            auth_code = input("Enter authorization code (Ctrl-C to quit): ")
            if not auth_code:
                print("Authorization code cannot be empty")
                continue
            break

        return auth_code

    def getpass(self, label: str) -> str:
        if not self.can_interact():
            print("Error: need to run in interactive mode to get passphrase")
            raise Exception()

        return getpass.getpass("%s (Ctrl-C to quit): " % (label,))

    def create_pass(self, header: str) -> str:
        if not self.can_interact():
            print("Error: need to run in interactive mode to create passphase")
            raise Exception()

        if header is not None:
            print(header)
        print("Warning: Your passphrase must contain enough randomness to be resistent to hacking. You can read this for more info: https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/")
        while True:
            pass_ = getpass.getpass("Enter new passphrase (Ctrl-C to quit):")
            pass2_ = getpass.getpass("Enter new passphrase (again) (Ctrl-C to quit): ")
            if pass_ != pass2_:
                print("Passphrases didn't match, please re-enter")
            else:
                del pass2_
                break

        return pass_

def base_create_fs(client_kw_args: typing.Dict[str, typing.Any], cache_folder: typing.Optional[str]) -> FileSystem:
    fs: FileSystem
    fs = CachingFileSystem(DropboxFileSystem(client_kw_args), cache_folder=cache_folder)

    # From a purity standpoint the following layer ideally would
    # go between the caching fs and dropbox fs, but because the
    # contract between those two is highly specialized, just put
    # it on top
    fs = TranslateIgnoredFilesFileSystem(fs)

    if sys.platform == 'darwin':
        fs = DisableQuickLookFileSystem(fs)

    return fs

class RealSysLogHandler(logging.Handler):
    def __init__(self, *n, **kw):
        super().__init__()
        assert syslog is not None
        syslog.openlog(*n, **kw)

    def _map_priority(self, levelname: int) -> int:
        assert syslog is not None
        return {
            logging.DEBUG:    syslog.LOG_DEBUG,
            logging.INFO:     syslog.LOG_INFO,
            logging.ERROR:    syslog.LOG_ERR,
            logging.WARNING:  syslog.LOG_WARNING,
            logging.CRITICAL: syslog.LOG_CRIT,
            }[levelname]

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        priority = self._map_priority(record.levelno)
        assert syslog is not None
        syslog.syslog(priority, msg)

def headless_stream_handler(app_name: str) -> typing.Optional[logging.Handler]:
    if syslog is not None:
        return RealSysLogHandler(app_name, syslog.LOG_PID)

    return None

def my_block_tracing():
    try:
        block_tracing()
    except Exception:
        log.warning("Block tracing failed, memory is readable by external processes",
                    exc_info=True)

def initialize_sentry(sentry_user, version):
    BOOTTIME = time.monotonic()

    def before_send(event, hint):
        event.setdefault("contexts", {}).update({"uptime": time.monotonic() - BOOTTIME})

        try:
            with urllib.request.urlopen("https://sentry.dbxfs.org/info") as f:
                options = json.load(f)

            c = sentry_sdk.Hub.current.client
            c.options.update(options)
            c.__setstate__(c.__getstate__())
        except (urllib.error.URLError, urllib.error.HTTPError):
            pass
        except Exception:
            # NB: we can't use log.exception() here because that would cause
            #     infinite recursion in Sentry
            traceback.print_exc()

        return event

    try:
        sentry_sdk.init("https://b4b13ebd300849bd92260507a594e618@sentry.io/1293235",
                        release='%s@%s' % (APP_NAME, version),
                        before_send=before_send,
                        include_local_variables=False)
        sentry_sdk.set_user(dict(id=sentry_user))
    except Exception:
        log.warning("Failed to initialize sentry", exc_info=True)

def on_new_process(proc_args: typing.Dict[str, typing.Any]) -> None:
    # Protect access token and potentially encryption keys
    my_block_tracing()

    display_name = proc_args['display_name']
    verbose = int(proc_args['verbose'])

    acquire_hold(proc_args['instance_guid'])

    format_ = '%(levelname)s:%(name)s:%(message)s'

    handlers = []

    result = headless_stream_handler(display_name)
    if result is not None:
        handlers.append(result)

    level = [logging.WARNING, logging.INFO, logging.DEBUG][min(2, verbose)]
    logging.basicConfig(level=level, handlers=handlers, format=format_)

    if int(proc_args.get('send_error_reports', '0')):
        version = proc_args['version']
        initialize_sentry(proc_args['sentry_user'], version)

def create_fs(fs_args: typing.Dict[str, typing.Any]) -> FileSystem:
    refresh_token = fs_args.get('refresh_token')
    access_token = fs_args.get('access_token')
    cache_folder = fs_args['cache_folder']

    dbx_client_args = dict(
        oauth2_refresh_token=refresh_token,
        oauth2_access_token=access_token,
        app_key=APP_KEY,
    )

    sub_create_fs = functools.partial(base_create_fs, dbx_client_args, cache_folder)

    if safefs_wrap_create_fs is not None:
        sub_create_fs = safefs_wrap_create_fs(sub_create_fs, fs_args)

    return sub_create_fs()

def on_mount(args: typing.Dict[str, typing.Any]):
    if sys.platform == 'win32' and args.get('gui') is not None:
        try:
            subprocess.run(["start", args['mount_point']], shell=True)
        except Exception:
            log.warning("Failed to open directory in file explorer", exc_info=True)

def warn_old_version(ui, config, version):
    save_config = False
    try:
        if not version:
            return (save_config, False)

        with urllib.request.urlopen("https://pypi.org/pypi/dbxfs/json") as f:
            rversion = json.load(io.TextIOWrapper(f))['info']['version']

        if rversion != version and (config.get("upgrade_asked") is None or
                                    config.get("upgrade_asked") != rversion):
            if getattr(sys, 'frozen', False):
                if ui.yes_no_input(("dbxfs is out of date. Your version is %s "
                                    "while the new version is %s. Would you like "
                                    "to download the new version?") %
                                   (version, rversion)):
                    webbrowser.open(("https://www.dbxfs.org/new_version?%s" %
                                     (urllib.parse.urlencode([
                                         ("old_version", version),
                                         ("new_version", rversion),
                                     ]),)),
                                    new=2)
                    return (save_config, True)

                save_config = True
                config['upgrade_asked'] = rversion
            else:
                ui.warning("dbxfs is out of date (%s vs %s), upgrade with 'pip3 install --upgrade dbxfs'" %
                           (rversion, version))
    except Exception:
        log.warning("Failed to get most recent version", exc_info=True)

    return (save_config, False)

class FUSEOption(argparse.Action):
    def __init__(self, **kw):
        super(FUSEOption, self).__init__(**kw)

    def __call__(self,
                 parser: argparse.ArgumentParser,
                 ns: argparse.Namespace,
                 values: str | Sequence[typing.Any] | None,
                 option_string: str | None = None) -> None:
        if ns.o is None:
            ns.o = {}
        assert isinstance(values, str)
        for kv in values.split(","):
            ret = kv.split("=", 1)
            if len(ret) == 2:
                ns.o[ret[0]] = ret[1]
            else:
                ns.o[ret[0]] = True

def add_cli_arguments(parser: argparse.ArgumentParser) -> None:
    def ensure_listen_address(string: str) -> typing.Tuple[str, int]:
        try:
            (host, ports) = string.split(":", 1)
        except ValueError:
            host = string
            port = 0
        else:
            port = int(ports)
            if not (0 <= port < 65536):
                raise argparse.ArgumentTypeError("%r is not a valid TCP port" % (port,))

        if not host:
            host = "127.0.0.1"

        return (host, port)

    parser.add_argument("-f", "--foreground", action="store_true",
                        help="keep filesystem server in foreground")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="show log messages, use twice for maximum verbosity")
    _group = parser.add_mutually_exclusive_group()
    _group.add_argument("-s", "--smb", action="store_true",
                        help="force mounting via SMB")
    _group.add_argument("-w", "--webdav", action="store_true",
                        help="force mounting via WebDAV")
    parser.add_argument("-n", "--no-mount", action="store_true",
                        dest="smb_no_mount",
                        help="export filesystem via network server but don't mount it")
    parser.add_argument("-l", "--listen-address",
                        dest="smb_listen_address",
                        type=ensure_listen_address,
                        help="address that the filesystem server should listen on, append colon to specify port")
    parser.add_argument("-o", metavar='opt,[opt...]', action=FUSEOption,
                        help="FUSE options, e.g. -o uid=1000,allow_other")

def _main(argv: typing.Optional[typing.List[str]] = None):
    try:
        import pyi_splash

        # Close the splash screen. It does not matter when the call
        # to this function is made, the splash screen remains open until
        # this function is called or the Python program is terminated.
        pyi_splash.close()
    except ModuleNotFoundError:
        pass
    except Exception:
        log.exception("pyi_splash failed")

    if sys.version_info < (3, 11):
        print("Error: Your version of Python is too old, 3.11+ is required: %d.%d.%d" % sys.version_info[:3])
        return -1

    try:
        check_runtime_requirements()
    except RuntimeError as e:
        print("Error: %s" % (e,))
        return -1

    # Protect access token and potentially encryption keys
    my_block_tracing()

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    add_cli_arguments(parser)
    parser.add_argument("-c", "--config-file",
                        help="config file path")
    parser.add_argument("--print-default-config-file", action='store_true',
                        help="print default config file path to standard out and quit")
    parser.add_argument("--get-refresh-token", action='store_true',
                        help="authorize new refresh token and print to standard out")
    parser.add_argument("--gui", action='store_true',
                        help="Use GUI for interactive configuration")
    parser.add_argument("--userspacefs-main", action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument("mount_point", nargs='?')
    args = parser.parse_args(argv[1:])

    if args.smb_no_mount and not args.smb and not args.webdav:
        print("error: either --smb or --webdav must be specified when --no-mount is specified",
              file=sys.stderr)
        return -1

    if args.userspacefs_main:
        return userspacefs.main(argv)

    if sys.stderr is None:
        logging_stream = headless_stream_handler(APP_NAME)
    else:
        logging_stream = logging.StreamHandler()

    handlers = []
    if logging_stream is not None:
        handlers.append(logging_stream)

    format_ = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    level = [logging.WARNING, logging.INFO, logging.DEBUG][min(2, args.verbose)]
    logging.basicConfig(level=level, handlers=handlers, format=format_)

    try:
        version = importlib.metadata.version("dbxfs")
    except Exception:
        log.warning("Failed to get version", exc_info=True)
        version = ''

    config_dir = appdirs.user_config_dir(APP_NAME)

    if args.config_file is not None:
        config_file = args.config_file
    else:
        config_file = os.path.join(config_dir, "config.json")

    if args.print_default_config_file:
        print(config_file)
        return 0

    config = {}

    refresh_token = None
    access_token = None
    save_refresh_token = False
    save_config = False
    came_from_command = False

    use_gui = args.gui or sys.stdout is None

    ui: UIProtocol
    if use_gui:
        if dbxfs_gui is None:
            print("No GUI available")
            return 1
        ui = dbxfs_gui
    else:
        ui = ConsoleUI()

    if not args.get_refresh_token:
        try:
            os.makedirs(config_dir, exist_ok=True)
        except OSError as e:
            ui.error("Unable to create configuration directory: %s" % (e,))
            return -1

        try:
            f = open(config_file)
        except IOError as e:
            if e.errno != errno.ENOENT: raise
        else:
            try:
                with f:
                    config = json.load(f)
            except ValueError as e:
                ui.error("Config file %r is not valid json: %s" % (config_file, e))
                return -1

        instance_guid = config.get("instance_guid", DEFAULT_INSTANCE_GUID)
        if not allow_multiple(instance_guid, use_gui):
            return -1

        # NB: this must happen after allow_multiple, otherwise it may
        #     cause a redundant dialog
        (new_save_config, should_quit) = warn_old_version(ui, config, version)
        if should_quit:
            return 0

        if new_save_config:
            save_config = True

        cache_folder = config.get("cache_dir")

        mount_point = args.mount_point
        if mount_point is None:
            mount_point = config.get("mount_point")

        # NB: mount point is always optional for windows because we can auto-generate one
        if not args.smb_no_mount and mount_point is None and sys.platform != 'win32':
            parser.print_usage()
            print("%s: error: please provide the mount_point argument" % (os.path.basename(argv[0]),))
            return 1

        encrypted_folders = config.get("encrypted_folders", [])

        if refresh_token is None and access_token is None:
            refresh_token_command = config.get("refresh_token_command", None)
            if refresh_token_command is not None:
                print("Running %r for refresh token" % (' '.join(refresh_token_command),))
                try:
                    refresh_token = subprocess.check_output(refresh_token_command).decode("utf-8")
                except UnicodeDecodeError:
                    print("Refresh token command output is not utf-8 encoded")
                    return -1
                except TypeError:
                    print("Bad refresh token command: %r, " % (refresh_token_command,))
                    return -1
                # NB: refresh tokens never contain white-space and the refresh token
                #     command often accidentally appends a newline character.
                refresh_token = refresh_token.strip()
                came_from_command = True

        access_token_command = config.get("access_token_command", None)
        if refresh_token is None and access_token is None and access_token_command is not None:
            print("Running %r for access token" % (' '.join(access_token_command),))
            try:
                access_token = subprocess.check_output(access_token_command).decode("utf-8")
            except UnicodeDecodeError:
                print("Access token command output is not utf-8 encoded")
                return -1
            except TypeError:
                print("Bad access token command: %r, " % (access_token_command,))
                return -1
            # NB: access tokens never contain white-space and the access token
            #     command often accidentally appends a newline character.
            access_token = access_token.strip()
            came_from_command = True

        if refresh_token is None and access_token is None:
            refresh_token_privy = config.get("refresh_token_privy", None)
            if refresh_token_privy is not None:
                passwd = None
                while True:
                    passwd = ui.getpass("Enter refresh token passphrase (not your Dropbox password)")
                    try:
                        refresh_token = privy.peek(refresh_token_privy, passwd).decode('utf-8')
                    except ValueError:
                        if not ui.yes_no_input("Incorrect password, create new refresh token?"):
                            continue
                    break
                del passwd

        if refresh_token is None and access_token is None:
            access_token_privy = config.get("access_token_privy", None)
            if access_token_privy is not None:
                passwd = None
                while True:
                    passwd = ui.getpass("Enter access token passphrase (not your Dropbox password)")
                    try:
                        access_token = privy.peek(access_token_privy, passwd).decode('utf-8')
                    except ValueError:
                        if not ui.yes_no_input("Incorrect password, create new access token?"):
                            continue
                    break
                del passwd

    while True:
        if access_token is None and refresh_token is None:
            save_refresh_token = True

            auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')
            authorize_url = auth_flow.start()

            auth_code = ui.link_dbxfs(authorize_url)

            try:
                oauth_result = auth_flow.finish(auth_code)
            except Exception as e:
                print("Authorization code was invalid!")
                continue

            refresh_token = oauth_result.refresh_token

        # test out access token
        try:
            assert (refresh_token is None) != (access_token is None)
            dropbox.Dropbox(
                oauth2_access_token=access_token,
                oauth2_refresh_token=refresh_token,
                app_key=APP_KEY,
            ).users_get_current_account()
        except (dropbox.exceptions.BadInputError,
                dropbox.exceptions.AuthError,
                ValueError) as e:
            if came_from_command:
                if access_token is not None:
                    print("""\
The access token retrieved by executing the command specified in the
'access_token_command' configuration key is no longer valid, please
obtain a new one.\
""")
                else:
                    print("""\
The refresh token retrieved by executing the command specified in the
'refresh_token_command' configuration key is no longer valid, please
obtain a new one.\
""")
                return 1
            print("Token was invalid: %s" % (e,))
            refresh_token = None
            access_token = None
        else:
            break

    if args.get_refresh_token:
        print("Refresh token:", refresh_token)
        return 0

    if save_refresh_token and ui.yes_no_input("We're now connected to your Dropbox account. Do you want to save the credentials we just obtained for the next time you run dbxfs?", default_yes=True):
        assert refresh_token is not None

        # clear all token commands
        for key in ['access_token_privy', "keyring_user",
                    'refresh_token_privy']:
            config.pop(key, None)

        pass_ = ui.create_pass("Before we can save your credentials, we need a passphrase to encrypt them.\n\nThis passphrase can be anything, it doesn't have to be your Dropbox password. Please make sure it's sufficiently random and not easily guessable.")
        config['refresh_token_privy'] = privy.hide(refresh_token.encode('utf-8'), pass_, server=False)
        del pass_
        save_config = True

    if ui.can_interact() and not config.get("asked_send_error_reports", False):
        if ui.yes_no_input("Would you like to help us improve %s by providing anonymous error reports?" % (APP_NAME,), default_yes=True):
            config['send_error_reports'] = True
        config['asked_send_error_reports'] = True
        save_config = True

    if config.get("send_error_reports", False) and not isinstance(config.get("sentry_user", None), str):
        config['sentry_user'] = uuid.uuid4().hex
        save_config = True

    if save_refresh_token and mount_point is not None and ui.yes_no_input("Do you want \"%s\" to be the default mount point?" % (mount_point,), default_yes=True):
        config['mount_point'] = mount_point
        save_config = True

    if save_config:
        with open(config_file, "w") as f:
            json.dump(config, f)

    if mount_point is None:
        assert sys.platform == 'win32'
        for i in reversed(range(65, 91)):
            mount_point = '%s:\\' % (chr(i),)
            if not os.path.isdir(mount_point):
                break
        else:
            raise Exception("Couldn't determine a mount point")

    log.info("Starting %s...", APP_NAME)

    if config.get('send_error_reports', False):
        initialize_sentry(config['sentry_user'], version)

    if cache_folder is None:
        cache_folder = os.path.join(appdirs.user_cache_dir(APP_NAME), "file_cache")
        try:
            os.makedirs(cache_folder, exist_ok=True)
        except OSError:
            log.warning("Failed to create cache folder, running without file cache")
            cache_folder = None
        log.debug("Using default cache path %s", cache_folder)
    else:
        if not os.path.isdir(cache_folder):
            print("User-provided \"cache_dir\" setting doesn't refer to a directory: \"%s\"" % (cache_folder,))
            return 1
        log.debug("Using custom cache path %s", cache_folder)

    assert (refresh_token is None) != (access_token is None)

    fs_args: typing.Dict[str, typing.Any]
    fs_args = {}

    if access_token is not None:
        fs_args['access_token'] = access_token
    if refresh_token is not None:
        fs_args['refresh_token'] = refresh_token
    fs_args['cache_folder'] = cache_folder

    if safefs_add_fs_args is not None:
        dbx_client_args = dict(
            oauth2_refresh_token=refresh_token,
            oauth2_access_token=access_token,
            app_key=APP_KEY,
        )

        with contextlib.closing(base_create_fs(dbx_client_args, cache_folder)) as fs:
            safefs_add_fs_args(fs, encrypted_folders, fs_args)
    elif encrypted_folders:
        print("safefs not installed, can't transparently decrypt encrypted folders")
        return 1

    if mount_point is not None and not os.path.exists(mount_point) and os.path.dirname(mount_point) != mount_point:
        if ui.can_interact() and ui.yes_no_input("Mount point \"%s\" doesn't exist, do you want to create it?" % (mount_point,), default_yes=True):
            try:
                os.makedirs(mount_point, exist_ok=True)
            except OSError as e:
                print("Unable to create mount point: %s" % (e,))
                return -1

    display_name = APP_NAME

    proc_args = {}
    proc_args['instance_guid'] = instance_guid
    proc_args['display_name'] = display_name
    proc_args['verbose'] = str(args.verbose)
    proc_args['version'] = version
    proc_args['send_error_reports'] = str(int(config.get('send_error_reports', False)))
    if config.get('send_error_reports', False):
        proc_args['sentry_user'] = config['sentry_user']

    on_mount_args = {'mount_point': mount_point}
    if use_gui:
        on_mount_args['gui'] = '1'

    if getattr(sys, 'frozen', False):
        main_executable = [sys.executable, "--userspacefs-main"]
    else:
        main_executable = None

    # we don't want the installer to display the splash when
    # launching the file system server process. This is our custom
    # extension
    os.environ['PYINSTALLER_NOSPLASH'] = '1'

    return userspacefs.simple_main(mount_point, display_name,
                                   ('dbxfs.main.create_fs', fs_args),
                                   on_new_process=('dbxfs.main.on_new_process', proc_args),
                                   on_mount=('dbxfs.main.on_mount', on_mount_args),
                                   foreground=args.foreground,
                                   smb_only=args.smb,
                                   webdav_only=args.webdav,
                                   no_mount=args.smb_no_mount,
                                   listen_address=args.smb_listen_address,
                                   fuse_options=args.o,
                                   main_executable=main_executable)

def main(argv: typing.Optional[typing.List[str]] = None):
    try:
        return _main(argv)
    except KeyboardInterrupt:
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
