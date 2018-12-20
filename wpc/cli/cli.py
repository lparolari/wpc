import click
from cli import client
from cli import work
from datetime import date


@click.group()
def cli():
    """Console script for wpc."""
    click.echo("Work Pay Calculator @ 2018-" + str(date.today().year))
    click.echo("lparolari <luca.parolari23@gmail.com>")

    click.echo()


cli.add_command(client.client)
cli.add_command(work.work)
