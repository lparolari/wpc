import click
from datetime import date
from .client import client
from .work import work
from .invoice import invoice
from .config import config


@click.group()
def cli():
    """
    Command line interface for wpc.


    Luca Parolari <luca.parolari23@gmail.com>

    Work Pay Calculator @ 2018
    """


cli.add_command(client.client)
cli.add_command(work.work)
cli.add_command(invoice.invoice)
cli.add_command(config.config)
