# -*- coding: utf-8 -*-

from wpc.boot import boot
from wpc.cli import shell

if __name__ == "__main__":
    boot.bootstrap()
    shell.cli_commands()

    # this script can be used in IDE (PyCharm) as script path.
    # the shell entry point is defined in setup.py.
