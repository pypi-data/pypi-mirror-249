#!/usr/bin/env python3

# This file is part of userspacefs.

# userspacefs is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# userspacefs is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with userspacefs.  If not, see <http://www.gnu.org/licenses/>.

from userspacefs.abc import FileSystem

import argparse
import errno
import functools
import importlib
import logging
import os
import os.path
import pathlib
import queue
import random
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import typing
import urllib.parse

from collections.abc import Callable, Mapping, Sequence

have_fuse_mount = True
try:
    from userspacefs.fuse_adapter import run_fuse_mount
except EnvironmentError:
    have_fuse_mount = False

from userspacefs.macos_path_conversion import FileSystem as MacOSPathConversionFileSystem
from userspacefs.smbserver import SMBServer, SimpleSMBBackend
from userspacefs.webdavserver import WebDAVServer

log = logging.getLogger(__name__)

class MountError(Exception): pass

def get_func(fully_qualified_fn_name: str) -> Callable[..., typing.Any]:
    (create_fs_module, fn_name) = fully_qualified_fn_name.rsplit('.', 1)
    return typing.cast(Callable[..., typing.Any], getattr(importlib.import_module(create_fs_module), fn_name))

def create_create_fs(create_fs_params: typing.Tuple[str, typing.Mapping[str, str]]) -> Callable[[], FileSystem]:
    (create_fs_module, fs_args) = create_fs_params

    create_fs_ = get_func(create_fs_module)

    create_fs: Callable[[], FileSystem] = functools.partial(create_fs_, fs_args)

    if sys.platform == "darwin":
        orig_create_fs = create_fs
        def create_fs_() -> FileSystem:
            return MacOSPathConversionFileSystem(orig_create_fs())

        create_fs = create_fs_

    return create_fs

def get_root(path: str) -> str:
    while os.path.dirname(path) != path:
        path = os.path.dirname(path)
    return path

def _run_fs_server(create_fs_params: typing.Tuple[str, typing.Mapping[str, str]],
                   create_server_fn: Callable[[socket.socket, FileSystem], typing.Any],
                   mount_fn: Callable[[typing.Tuple[str, int], str], None],
                   unmount_fn: Callable[[str], None],
                   mount_signal: typing.Optional[Callable[[typing.Tuple[str, int]], None]] = None,
                   smb_no_mount: bool = False,
                   smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None,
                   mount_point: typing.Optional[str] = None,
                   foreground: bool = False,
                   ) -> None:
    create_fs = create_create_fs(create_fs_params)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if smb_listen_address is None:
        smb_listen_address = ("127.0.0.1", 0)

    for prop in ('SO_REUSEADDR', 'SO_REUSEPORT'):
        if hasattr(socket, prop):
            sock.setsockopt(socket.SOL_SOCKET, getattr(socket, prop), True)

    sock.bind(smb_listen_address)

    (host, port) = sock.getsockname()

    server = None

    mm_q: queue.Queue[bool] = queue.Queue()
    def check_mount() -> None:
        assert server is not None

        is_mounted = False

        if not smb_no_mount:
            assert mount_point is not None
            try:
                mount_fn((host, port), mount_point)
            except Exception:
                log.debug("Mount failed, killing server", exc_info=True)
                server.stop()
                return

            is_mounted = True

        # give mount signal
        if mount_signal is not None:
            mount_signal((host, port))

        while True:
            try:
                r = mm_q.get(timeout=(None
                                      if not is_mounted else
                                      1 if foreground else 30))
            except queue.Empty:
                pass
            else:
                log.debug("Got kill flag!")
                break

            if (is_mounted and
                not (os.path.ismount(mount_point) and
                     os.path.isdir(mount_point))):
                log.debug("Drive has gone unmounted")
                is_mounted = False
                break

        if is_mounted:
            assert mount_point is not None
            unmount_fn(mount_point)

        log.debug("CALLING SERVER CLOSE")
        server.stop()

    def kill_signal(*_: typing.Any) -> None:
        log.debug("Got kill signal!")
        mm_q.put(False)

    fs = create_fs()
    try:
        server = create_server_fn(sock, fs)

        # enable signals now that server is set
        signal.signal(signal.SIGTERM, kill_signal)
        signal.signal(signal.SIGINT, kill_signal)

        threading.Thread(target=check_mount, daemon=True).start()

        server.run()
    finally:
        if server is not None:
            server.close()
        fs.close()

def run_smb_server(create_fs_params: typing.Tuple[str, typing.Mapping[str, str]],
                   mount_signal: typing.Optional[Callable[[str], None]] = None,
                   display_name: typing.Optional[str] = None,
                   smb_no_mount: bool = False,
                   smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None,
                   mount_point: typing.Optional[str] = None,
                   foreground: bool = False) -> None:
    if display_name is None:
        raise Exception("need display name argument!")
    def create_server(sock: socket.socket, fs: FileSystem) -> typing.Any:
        return SMBServer(SimpleSMBBackend("\\\\127.0.0.1\\%s" % (display_name,),
                                          fs),
                         sock=sock)
    def create_url(address: typing.Tuple[str, int]) -> str:
        (host, port) = address
        return ("cifs://guest:@%s:%d/%s" %
                (host, port, display_name))
    def mount(address: typing.Tuple[str, int], mount_point: str) -> None:
        # NB: this only works for macOS
        ret = subprocess.call(["mount", "-t", "smbfs",
                               create_url(address),
                               mount_point])
        if ret:
            raise Exception("failed mount! %d" % (ret,))
    def unmount(mount_point: str) -> None:
        # NB: this only works for macOS
        subprocess.call(["umount", "-f", mount_point])
    def my_mount_signal(address: typing.Tuple[str, int]) -> None:
        if mount_signal is not None:
            mount_signal(create_url(address))
    return _run_fs_server(
        create_fs_params,
        create_server, mount, unmount,
        my_mount_signal,
        smb_no_mount,
        smb_listen_address,
        mount_point,
        foreground,
    )

def run_webdav_server(create_fs_params: typing.Tuple[str, typing.Mapping[str, str]],
                      mount_signal: typing.Optional[Callable[[str], None]] = None,
                      display_name: typing.Optional[str] = None,
                      smb_no_mount: bool = False,
                      smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None,
                      mount_point: typing.Optional[str] = None,
                      foreground: bool = False) -> None:
    if display_name is None:
        raise Exception("need display name argument!")
    path_root = "/%s" % (urllib.parse.quote(display_name),)
    def create_server(sock: socket.socket, fs: FileSystem) -> typing.Any:
        return WebDAVServer(fs, path_root=path_root, sock=sock)
    def create_url(address: typing.Tuple[str, int]) -> str:
        (host, port) = address
        webdav_url = "http://%s" % (host,)
        if port != 80:
            webdav_url += ":%d" % (port,)
        webdav_url += path_root
        return webdav_url
    def mount(address: typing.Tuple[str, int], mount_point: str) -> None:
        # NB: this only works for Windows
        if sys.platform != 'win32':
            raise Exception("this platform not supported")

        drive_letter = mount_point[0]

        webdav_url = create_url(address)

        log.debug("Mounting: %r", webdav_url)

        tried = False
        while True:
            ret = subprocess.call(["net", "use", '%s:' % (drive_letter,),
                                   "%s" % (webdav_url,),
                                   "/persistent:no"],
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            if not ret:
                break
            if not tried:
                import win32com.shell.shell as shell
                res = shell.ShellExecuteEx(
                    lpVerb='runas',
                    lpFile="%s\\System32\\sc" % (os.environ['SystemRoot'],),
                    lpParameters="config WebClient start=auto",
                )
                if res:
                    tried = True
                    time.sleep(1)
                    continue
            raise Exception("failed mount! %d" % (ret,))
    def unmount(mount_point: str) -> None:
        # NB: this only works for Windows
        if sys.platform != 'win32':
            raise Exception("this platform not supported")

        drive_letter = mount_point[0]

        subprocess.call(["net", "use", '%s:' % (drive_letter,),
                         "/delete"],
                        creationflags=subprocess.CREATE_NO_WINDOW)
    def my_mount_signal(address: typing.Tuple[str, int]) -> None:
        if mount_signal is not None:
            mount_signal(create_url(address))
    return _run_fs_server(
        create_fs_params,
        create_server, mount, unmount,
        my_mount_signal,
        smb_no_mount,
        smb_listen_address,
        mount_point,
        foreground,
    )

def run_mount(create_fs_params: typing.Tuple[str, typing.Mapping[str, str]],
              mount_point: typing.Optional[str],
              foreground: bool = False,
              display_name: typing.Optional[str] = None,
              fuse_options: typing.Optional[Mapping[str, bool | str]] = None,
              smb_no_mount: bool = False,
              smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None,
              smb_only: bool = False,
              webdav_only: bool = False,
              mount_signal: typing.Optional[Callable[[typing.Optional[str]], None]] = None) -> int:
    assert smb_no_mount or mount_point is not None, "must specify a mount point unless smb_no_mount is set"
    assert (smb_only or webdav_only) or mount_point is not None

    if not (smb_only or webdav_only) and have_fuse_mount:
        log.debug("Attempting fuse mount")
        try:
            if fuse_options is None:
                fuse_options = {}

            # NB: redundant assert but mypy isn't smart enough to derive this fact
            assert mount_point is not None

            def on_init() -> None:
                if mount_signal is not None:
                    mount_signal(None)

            # foreground=True here is not a error, run_mount() always runs in
            # foreground, the kwarg is for run_smb_server()
            run_fuse_mount(create_create_fs(create_fs_params), mount_point, foreground=True,
                           display_name=display_name, on_init=on_init,
                           **fuse_options)
            return 0
        except RuntimeError as e:
            # Fuse is broken, fall back to SMB
            pass

    if webdav_only or (not smb_only and sys.platform == 'win32'):
        run_webdav_server(
            create_fs_params,
            mount_signal=mount_signal,
            smb_no_mount=smb_no_mount,
            smb_listen_address=smb_listen_address,
            mount_point=mount_point,
            display_name=display_name,
            foreground=foreground
        )
        return 0

    run_smb_server(create_fs_params, mount_signal=mount_signal,
                   smb_no_mount=smb_no_mount, smb_listen_address=smb_listen_address,
                   mount_point=mount_point, display_name=display_name, foreground=foreground)

    return 0

def main_(argv: typing.Optional[typing.List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv

    # to avoid accidental SIGPIPE
    # redirect stdout to devnull
    # we have to do it this way because pass_fds is not
    # supported on windows, but dup() is
    new_stdout = os.fdopen(os.dup(1), "w")
    os.close(1)
    fd = os.open(os.devnull, os.O_WRONLY)
    if fd != 1:
        os.dup2(fd, 1)
        os.close(fd)

    create_fs_module = None
    fs_args = {}
    smb_no_mount = False
    smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None
    mount_point = None
    display_name = None
    on_new_process = None
    proc_args = {}
    smb_only = False
    fuse_options = {}
    webdav_only = False

    # get fs_args from env
    for (key, value) in os.environ.items():
        # NB: python forces windows environment variables to upper case for some reason
        #     so we have to access them that way
        if sys.platform == 'win32':
            key = key.lower()
        if  key.startswith("__userspacefs_fs_arg_"):
            fs_args[key[len("__userspacefs_fs_arg_"):]] = value
        elif key.startswith("__userspacefs_proc_arg_"):
            proc_args[key[len("__userspacefs_proc_arg_"):]] = value
        elif key == "__userspacefs_onp_module":
            on_new_process = value
        elif key == "__userspacefs_create_fs_module":
            create_fs_module = value
        elif key == "__userspacefs_smb_no_mount":
            smb_no_mount = True
        elif key == "__userspacefs_smb_listen_address":
            smb_listen_address_a = value.split(":", 1)
            smb_listen_address = (smb_listen_address_a[0], int(smb_listen_address_a[1]))
        elif key == "__userspacefs_mount_point":
            mount_point = value
        elif key == "__userspacefs_display_name":
            display_name = value
        elif key == "__userspacefs_smb_only":
            smb_only = True
        elif key == "__userspacefs_webdav_only":
            webdav_only = True
        elif key.startswith("__userspacefs_fuse_opt_"):
            opt_value: bool | str = value
            if value == ",":
                opt_value = True
            fuse_options[key[len("__userspacefs_fuse_opt_"):]] = opt_value

    if create_fs_module is None:
        raise Exception("Parent did not pass create_fs_module argument!")

    if on_new_process is not None:
        get_func(on_new_process)(proc_args)

    create_fs_params = (create_fs_module, fs_args)

    def mount_signal(url: typing.Optional[str] = None) -> None:
        if url is not None:
            print("mounted %s" % (url,), file=new_stdout, flush=True)
        else:
            print("mounted", file=new_stdout, flush=True)
        # new_stdout will not be used anymore
        new_stdout.close()

    run_mount(create_fs_params, mount_point,
              foreground=False,
              mount_signal=mount_signal,
              display_name=display_name,
              smb_no_mount=smb_no_mount,
              smb_listen_address=smb_listen_address,
              smb_only=smb_only,
              webdav_only=webdav_only,
              fuse_options=fuse_options)

    return 0

def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    try:
        return main_(argv=argv)
    except Exception:
        logging.exception("unexpected exception")
        return -1

def mount_and_run_fs(display_name: str,
                     create_fs_params: typing.Tuple[str, typing.Mapping[str, str]],
                     mount_point: typing.Optional[str],
                     on_new_process: typing.Optional[typing.Tuple[str, typing.Mapping[str, str]]] = None,
                     on_mount: typing.Optional[typing.Tuple[str, typing.Mapping[str, str]]] = None,
                     foreground: bool = False,
                     smb_only: bool = False,
                     webdav_only: bool = False,
                     smb_no_mount: bool = False,
                     smb_listen_address: typing.Optional[typing.Tuple[str, int]] = None,
                     fuse_options: typing.Optional[Mapping[str, bool | str]] = None,
                     main_executable: typing.Optional[typing.List[str]] = None) -> int:

    if not smb_no_mount:
        assert mount_point is not None
        mount_point = os.path.abspath(mount_point)

    assert not smb_no_mount or (smb_only or webdav_only)

    can_mount_automatically = (
        (smb_only and sys.platform == "darwin") or
        (webdav_only and sys.platform == "win32") or
        ((not smb_only and not webdav_only) and (sys.platform in ["win32", "darwin"] or have_fuse_mount))
    )
    if not smb_no_mount and not can_mount_automatically:
        if smb_only:
            raise MountError("Don't know how to automatically mount SMB on this platform.")
        if webdav_only:
            raise MountError("Don't know how to automatically mount WebDAV on this platform.")
        raise MountError("Don't know how to automatically mount the file system on this platform.")

    def no_auto_mount_message(url: typing.Optional[str] = None) -> None:
        if smb_no_mount:
            assert url is not None
            print("You can access the file server at %s" % (url,))
        if on_mount is not None:
            get_func(on_mount[0])(on_mount[1])

    if not foreground:
        if sys.executable is None:
            raise Exception("need a path to the executable!")

        for (key, value) in create_fs_params[1].items():
            os.environ['__userspacefs_fs_arg_' + key] = value

        os.environ['__userspacefs_create_fs_module'] = create_fs_params[0]

        if on_new_process is not None:
            for (key, value) in on_new_process[1].items():
                assert key == key.lower(), "all proc arg keys must be lowercase: %r" % (key,)
                os.environ['__userspacefs_proc_arg_' + key] = value

            os.environ['__userspacefs_onp_module'] = on_new_process[0]
        if smb_no_mount:
            os.environ['__userspacefs_smb_no_mount'] = '1'
        if smb_listen_address is not None:
            ser = smb_listen_address[0]
            ser += ":%d" % (smb_listen_address[1],)
            os.environ['__userspacefs_smb_listen_address'] = ser
        if mount_point is not None:
            os.environ["__userspacefs_mount_point"] = mount_point
        os.environ["__userspacefs_display_name"] = display_name
        if fuse_options is not None:
            for (key, value_o) in fuse_options.items():
                if isinstance(value_o, bool):
                    if value_o is not True:
                        continue
                    # comma cannot be used as a fuse option value
                    value_o = ','
                os.environ['__userspacefs_fuse_opt_' + key] = value_o
        if smb_only:
            os.environ['__userspacefs_smb_only'] = '1'
        if webdav_only:
            os.environ['__userspacefs_webdav_only'] = '1'

        if main_executable is None:
            assert not getattr(sys, 'frozen', False), (
                "Application is frozen, must use main_executable argument"
            )
            main_executable = [sys.executable, "-c", "import sys; from userspacefs import main; sys.exit(main())"]

        proc = subprocess.Popen(main_executable,
                                universal_newlines=True,
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL,
                                start_new_session=True,
                                cwd=get_root(sys.executable))

        # NB: necessary for type checker
        assert proc.stdout is not None

        # wait for proc to get mounted\n (signaled by writing mounted stdout)
        # or for proc to die
        ret = 1
        while True:
            buf = proc.stdout.readline()
            if not buf:
                ret = proc.wait()
                break

            mo = re.search(r"^mounted(\s+(\S+))?\s*$", buf)
            if mo is not None:
                if mo.group(1) is not None:
                    url = mo.group(2)
                else:
                    url = None
                no_auto_mount_message(url)
                ret = 0
                break

        return ret

    run_mount(create_fs_params, mount_point,
              foreground=True,
              mount_signal=no_auto_mount_message,
              display_name=display_name,
              fuse_options=fuse_options,
              smb_no_mount=smb_no_mount,
              smb_listen_address=smb_listen_address,
              smb_only=smb_only,
              webdav_only=webdav_only,
    )

    return 0

def simple_main(mount_point: typing.Optional[str], display_name: str,
                create_fs_params: typing.Tuple[str, typing.Mapping[str, typing.Any]],
                on_new_process: typing.Optional[typing.Tuple[str, typing.Mapping[str, str]]] = None,
                on_mount: typing.Optional[typing.Tuple[str, typing.Mapping[str, str]]] = None,
                foreground: bool = False,
                smb_only: bool = False,
                webdav_only: bool = False,
                no_mount: bool = False,
                listen_address: typing.Optional[typing.Tuple[str, int]] = None,
                fuse_options: typing.Optional[Mapping[str, bool | str]] = None,
                main_executable: typing.Optional[typing.List[str]] = None) -> int:
    try:
        return mount_and_run_fs(display_name, create_fs_params,
                                mount_point,
                                on_new_process=on_new_process,
                                on_mount=on_mount,
                                foreground=foreground,
                                smb_only=smb_only,
                                webdav_only=webdav_only,
                                smb_no_mount=no_mount,
                                smb_listen_address=listen_address,
                                fuse_options=fuse_options,
                                main_executable=main_executable)
    except MountError as e:
        print(e)
        return -1

class _FUSEOption(argparse.Action):
    def __init__(self, **kw: typing.Any):
        super(_FUSEOption, self).__init__(**kw)

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

def _add_simple_cli_arguments(parser: argparse.ArgumentParser) -> None:
    def ensure_listen_address(string: str) -> typing.Tuple[str, int]:
        try:
            (host, port_s) = string.split(":", 1)
        except ValueError:
            host = string
            port = 0
        else:
            port = int(port_s)
            if not (0 <= port < 65536):
                raise argparse.ArgumentTypeError("%r is not a valid TCP port" % (port,))

        if not host:
            host = "127.0.0.1"

        return (host, port)

    parser.add_argument("-f", "--foreground", action="store_true",
                        help="keep filesystem server in foreground")
    _group = parser.add_mutually_exclusive_group()
    _group.add_argument("-s", "--smb", action="store_true",
                        help="force mounting via SMB")
    _group.add_argument("-w", "--webdav", action="store_true",
                        help="force mounting via WebDAV")
    parser.add_argument("-l", "--listen-address",
                        type=ensure_listen_address,
                        help="address that the filesystem server should listen on, append colon to specify port")
    parser.add_argument("-o", metavar='opt,[opt...]', action=_FUSEOption,
                        help="FUSE options, e.g. -o uid=1000,allow_other")
    parser.add_argument("-n", "--no-mount", action="store_true",
                        help="export filesystem via network server but don't mount it")
    parser.add_argument("mount_point", nargs='?')

def simple_main_from_argv(display_name: str,
                          create_fs_params: typing.Tuple[str, typing.Mapping[str, typing.Any]],
                          argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    _add_simple_cli_arguments(parser)
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="show log messages, use twice for maximum verbosity")
    args = parser.parse_args(argv[1:])

    level = [logging.WARNING, logging.INFO, logging.DEBUG][min(2, args.verbose)]
    logging.basicConfig(level=level)

    if args.mount_point is None and not args.no_mount:
        print("error: the 'mount_point' argument is required unless --no-mount is specified",
              file=sys.stderr)
        return -1

    if args.no_mount and not args.smb and not args.webdav:
        print("error: either --smb or --webdav must be specified when --no-mount is specified",
              file=sys.stderr)
        return -1

    return simple_main(args.mount_point, display_name, create_fs_params,
                       foreground=args.foreground,
                       smb_only=args.smb,
                       webdav_only=args.webdav,
                       no_mount=args.no_mount,
                       listen_address=args.listen_address,
                       fuse_options=args.o)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
