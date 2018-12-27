import click
from cli import client
from cli import work
from datetime import date


@click.group()
def cli():
    """
    Command line interface for wpc.


    Luca Parolari <luca.parolari23@gmail.com>

    Work Pay Calculator @ 2018
    """


cli.add_command(client.client)
cli.add_command(work.work)
