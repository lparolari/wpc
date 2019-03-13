# -*- coding: utf-8 -*-

from wpc.cli import cli
from boot import boot

if __name__ == "__main__":
    boot.bootstrap()
    cli.cli_commands()

    # sys.exit(main())  # pragma: no cover

