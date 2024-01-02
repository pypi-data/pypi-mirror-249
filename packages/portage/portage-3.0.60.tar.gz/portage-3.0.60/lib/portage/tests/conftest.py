#!/usr/bin/env python
# Copyright 2006-2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

import grp
import os
import os.path as osp
import pwd
import signal
import tempfile
import shutil
import sys

import pytest

import portage
from portage.util._eventloop.global_event_loop import global_event_loop
from portage.const import PORTAGE_BIN_PATH


def debug_signal(signum, frame):
    import pdb

    pdb.set_trace()


signal.signal(signal.SIGUSR1, debug_signal)


@pytest.fixture(autouse=True, scope="session")
def prepare_environment():
    # Pretend that the current user's uid/gid are the 'portage' uid/gid,
    # so things go smoothly regardless of the current user and global
    # user/group configuration.
    os.environ["PORTAGE_USERNAME"] = pwd.getpwuid(os.getuid()).pw_name
    os.environ["PORTAGE_GRPNAME"] = grp.getgrgid(os.getgid()).gr_name

    # Insert our parent dir so we can do shiny import "tests"
    # This line courtesy of Marienz and Pkgcore ;)
    sys.path.insert(0, osp.dirname(osp.dirname(osp.dirname(osp.realpath(__file__)))))

    portage._internal_caller = True

    # Ensure that we don't instantiate portage.settings, so that tests should
    # work the same regardless of global configuration file state/existence.
    portage._disable_legacy_globals()

    if portage.util.no_color(os.environ):
        portage.output.nocolor()

    # import portage.tests as tests

    path = os.environ.get("PATH", "").split(":")
    path = [x for x in path if x]

    insert_bin_path = True
    try:
        insert_bin_path = not path or not os.path.samefile(path[0], PORTAGE_BIN_PATH)
    except OSError:
        pass

    if insert_bin_path:
        path.insert(0, PORTAGE_BIN_PATH)
        os.environ["PATH"] = ":".join(path)

    try:
        # Copy GPG test keys to temporary directory
        gpg_path = tempfile.mkdtemp(prefix="gpg_")

        shutil.copytree(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), ".gnupg"),
            gpg_path,
            dirs_exist_ok=True,
        )

        os.chmod(gpg_path, 0o700)
        os.environ["PORTAGE_GNUPGHOME"] = gpg_path

        yield

    finally:
        global_event_loop().close()
        shutil.rmtree(gpg_path, ignore_errors=True)


# if __name__ == "__main__":
#     try:
#         sys.exit(tests.main())
#     finally:
#         global_event_loop().close()
#         shutil.rmtree(gpg_path, ignore_errors=True)
