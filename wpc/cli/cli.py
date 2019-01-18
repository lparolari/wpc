# import wpc

import click

from datetime import date
# from .client import client
# from .work import work
# from .invoice import invoice
# from .config import config
from wpc.cli import client, work, invoice, config


@click.group()
def cli():
    """
    Command line interface for wpc.


    Luca Parolari <luca.parolari23@gmail.com>

    Work Pay Calculator @ 2018
    """
    pass


cli.add_command(client)
cli.add_command(work)
cli.add_command(invoice)
cli.add_command(config)



