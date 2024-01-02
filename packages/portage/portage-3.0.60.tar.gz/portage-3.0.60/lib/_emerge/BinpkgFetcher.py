# Copyright 1999-2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

from _emerge.AsynchronousLock import AsynchronousLock
from _emerge.CompositeTask import CompositeTask
from _emerge.SpawnProcess import SpawnProcess
from urllib.parse import urlparse as urllib_parse_urlparse
import stat
import sys
import portage
from portage import os
from portage.binpkg import get_binpkg_format
from portage.exception import FileNotFound
from portage.util._async.AsyncTaskFuture import AsyncTaskFuture
from portage.util._async.FileCopier import FileCopier
from portage.util._pty import _create_pty_or_pipe


class BinpkgFetcher(CompositeTask):
    __slots__ = ("pkg", "pretend", "logfile", "pkg_path", "pkg_allocated_path")

    def __init__(self, **kwargs):
        CompositeTask.__init__(self, **kwargs)

        pkg = self.pkg
        bintree = pkg.root_config.trees["bintree"]
        instance_key = bintree.dbapi._instance_key(pkg.cpv)

        binpkg_path = bintree._remotepkgs[instance_key].get("PATH")
        if not binpkg_path:
            raise FileNotFound(
                f"PATH not found in the binpkg index, the binhost's portage is probably out of date."
            )
        binpkg_format = get_binpkg_format(binpkg_path)

        self.pkg_allocated_path = pkg.root_config.trees["bintree"].getname(
            pkg.cpv, allocate_new=True, remote_binpkg_format=binpkg_format
        )
        self.pkg_path = self.pkg_allocated_path + ".partial"

    def _start(self):
        self._start_task(
            AsyncTaskFuture(future=self._main(), scheduler=self.scheduler),
            self._main_exit,
        )

    async def _main(self) -> int:
        """
        Main coroutine which saves the binary package to self.pkg_path
        and returns the exit status of the fetcher or copier.

        @rtype: int
        @return: Exit status of fetcher or copier.
        """
        pkg = self.pkg
        bintree = pkg.root_config.trees["bintree"]

        fetcher = _BinpkgFetcherProcess(
            background=self.background,
            logfile=self.logfile,
            pkg=self.pkg,
            pkg_path=self.pkg_path,
            pretend=self.pretend,
            scheduler=self.scheduler,
        )

        if not self.pretend:
            portage.util.ensure_dirs(os.path.dirname(self.pkg_path))
            if "distlocks" in self.pkg.root_config.settings.features:
                await fetcher.async_lock()

        try:
            if bintree._remote_has_index:
                remote_metadata = bintree._remotepkgs[
                    bintree.dbapi._instance_key(pkg.cpv)
                ]
                rel_uri = remote_metadata.get("PATH")
                if not rel_uri:
                    # Assume that the remote index is out of date. No path should
                    # never happen in new portage versions.
                    rel_uri = pkg.cpv + ".tbz2"
                remote_base_uri = remote_metadata["BASE_URI"]
                uri = remote_base_uri.rstrip("/") + "/" + rel_uri.lstrip("/")
            else:
                raise FileNotFound("Binary packages index not found")

            uri_parsed = urllib_parse_urlparse(uri)

            copier = None
            if not self.pretend and uri_parsed.scheme in ("", "file"):
                copier = FileCopier(
                    src_path=uri_parsed.path,
                    dest_path=self.pkg_path,
                    scheduler=self.scheduler,
                )
                copier.start()
                try:
                    await copier.async_wait()
                    copier.future.result()
                except FileNotFoundError:
                    await self.scheduler.async_output(
                        f"!!! File not found: {uri_parsed.path}\n",
                        log_file=self.logfile,
                        background=self.background,
                    )
                finally:
                    if copier.isAlive():
                        copier.cancel()

            else:
                fetcher.start()
                try:
                    await fetcher.async_wait()
                finally:
                    if fetcher.isAlive():
                        fetcher.cancel()

                if not self.pretend and fetcher.returncode == os.EX_OK:
                    fetcher.sync_timestamp()
        finally:
            if fetcher.locked:
                await fetcher.async_unlock()

        return fetcher.returncode if copier is None else copier.returncode

    def _main_exit(self, main_task):
        if not main_task.cancelled:
            # Use the fetcher or copier returncode.
            main_task.returncode = main_task.future.result()
        self._default_final_exit(main_task)


class _BinpkgFetcherProcess(SpawnProcess):
    __slots__ = ("pkg", "pretend", "locked", "pkg_path", "_lock_obj")

    def _start(self):
        pkg = self.pkg
        pretend = self.pretend
        bintree = pkg.root_config.trees["bintree"]
        settings = bintree.settings
        pkg_path = self.pkg_path

        exists = os.path.exists(pkg_path)
        resume = exists and os.path.basename(pkg_path) in bintree.invalids
        if not (pretend or resume):
            # Remove existing file or broken symlink.
            try:
                os.unlink(pkg_path)
            except OSError:
                pass

        # urljoin doesn't work correctly with
        # unrecognized protocols like sftp
        fetchcommand = None
        resumecommand = None
        if bintree._remote_has_index:
            remote_metadata = bintree._remotepkgs[bintree.dbapi._instance_key(pkg.cpv)]
            rel_uri = remote_metadata.get("PATH")
            if not rel_uri:
                # Assume that the remote index is out of date. No path should
                # never happen in new portage versions.
                rel_uri = pkg.cpv + ".tbz2"
            remote_base_uri = remote_metadata["BASE_URI"]
            uri = remote_base_uri.rstrip("/") + "/" + rel_uri.lstrip("/")
            fetchcommand = remote_metadata.get("FETCHCOMMAND")
            resumecommand = remote_metadata.get("RESUMECOMMAND")
        else:
            raise FileNotFound("Binary packages index not found")

        if pretend:
            portage.writemsg_stdout(f"\n{uri}\n", noiselevel=-1)
            self.returncode = os.EX_OK
            self._async_wait()
            return

        fcmd = None
        if resume:
            fcmd = resumecommand
        else:
            fcmd = fetchcommand
        if fcmd is None:
            protocol = urllib_parse_urlparse(uri)[0]
            fcmd_prefix = "FETCHCOMMAND"
            if resume:
                fcmd_prefix = "RESUMECOMMAND"
            fcmd = settings.get(fcmd_prefix + "_" + protocol.upper())
            if not fcmd:
                fcmd = settings.get(fcmd_prefix)

        fcmd_vars = {
            "DISTDIR": os.path.dirname(pkg_path),
            "URI": uri,
            "FILE": os.path.basename(pkg_path),
        }

        for k in ("PORTAGE_SSH_OPTS",):
            v = settings.get(k)
            if v is not None:
                fcmd_vars[k] = v

        fetch_env = dict(settings.items())
        fetch_args = [
            portage.util.varexpand(x, mydict=fcmd_vars)
            for x in portage.util.shlex_split(fcmd)
        ]

        if self.fd_pipes is None:
            self.fd_pipes = {}
        fd_pipes = self.fd_pipes

        # Redirect all output to stdout since some fetchers like
        # wget pollute stderr (if portage detects a problem then it
        # can send it's own message to stderr).
        fd_pipes.setdefault(0, portage._get_stdin().fileno())
        fd_pipes.setdefault(1, sys.__stdout__.fileno())
        fd_pipes.setdefault(2, sys.__stdout__.fileno())

        self.args = fetch_args
        self.env = fetch_env
        if settings.selinux_enabled():
            self._selinux_type = settings["PORTAGE_FETCH_T"]
        self.log_filter_file = settings.get("PORTAGE_LOG_FILTER_FILE_CMD")
        SpawnProcess._start(self)

    def _pipe(self, fd_pipes):
        """When appropriate, use a pty so that fetcher progress bars,
        like wget has, will work properly."""
        if self.background or not sys.__stdout__.isatty():
            # When the output only goes to a log file,
            # there's no point in creating a pty.
            return os.pipe()
        stdout_pipe = None
        if not self.background:
            stdout_pipe = fd_pipes.get(1)
        got_pty, master_fd, slave_fd = _create_pty_or_pipe(copy_term_size=stdout_pipe)
        return (master_fd, slave_fd)

    def sync_timestamp(self):
        # If possible, update the mtime to match the remote package if
        # the fetcher didn't already do it automatically.
        bintree = self.pkg.root_config.trees["bintree"]
        if bintree._remote_has_index:
            remote_mtime = bintree._remotepkgs[
                bintree.dbapi._instance_key(self.pkg.cpv)
            ].get("_mtime_")
            if remote_mtime is not None:
                try:
                    remote_mtime = int(remote_mtime)
                except ValueError:
                    pass
                else:
                    try:
                        local_mtime = os.stat(self.pkg_path)[stat.ST_MTIME]
                    except OSError:
                        pass
                    else:
                        if remote_mtime != local_mtime:
                            try:
                                os.utime(self.pkg_path, (remote_mtime, remote_mtime))
                            except OSError:
                                pass

    def async_lock(self):
        """
        This raises an AlreadyLocked exception if lock() is called
        while a lock is already held. In order to avoid this, call
        unlock() or check whether the "locked" attribute is True
        or False before calling lock().
        """
        if self._lock_obj is not None:
            raise self.AlreadyLocked((self._lock_obj,))

        result = self.scheduler.create_future()

        def acquired_lock(async_lock):
            if async_lock.wait() == os.EX_OK:
                self.locked = True
                result.set_result(None)
            else:
                result.set_exception(
                    AssertionError(
                        f"AsynchronousLock failed with returncode {async_lock.returncode}"
                    )
                )

        self._lock_obj = AsynchronousLock(path=self.pkg_path, scheduler=self.scheduler)
        self._lock_obj.addExitListener(acquired_lock)
        self._lock_obj.start()
        return result

    class AlreadyLocked(portage.exception.PortageException):
        pass

    def async_unlock(self):
        if self._lock_obj is None:
            raise AssertionError("already unlocked")
        result = self._lock_obj.async_unlock()
        self._lock_obj = None
        self.locked = False
        return result
