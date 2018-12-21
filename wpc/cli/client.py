"""
Entry point for the command line interface.
"""

import click

from wpc.db.db import Db
from wpc.model.client import Client

db = Db()


@click.group()
def client():
    """
    Group commands for clients.
    :return: None.
    """
    return


@click.command()
@click.option('--id', type=int, help='The id of the client.')
@click.option('--name', type=str, help='The name of the client.')
def show(id, name):
    """
    Shows registered clients. If no filter is specified shows all clients.

    :param id: The id of the client.
    :param name: The name of the client.
    :return: None.
    """

    clients = []

    # Find results.
    if id is not None:
        res = db.find(Client, id)
        if res is not None:
            clients = [res]
    elif name is not None:
        clients = db.query(Client)\
                    .filter(Client.name.like("%"+name+"%"))\
                    .all()
    else:
        clients = db.getAll(Client)

    # Print results.
    if len(clients) > 0:
        click.echo("Clients: ")
        [click.echo(" {}, {}".format(x.id, x.name)) for x in clients]
    else:
        click.echo("No clients found.")

    return


@click.command()
def add():
    """
    Insert a client into the system.

    :return: None.
    """

    name = click.prompt("Name", type=str)

    if name is None:
        click.echo("Name cannot be empty")
        return

    new_client = Client(name=name)

    db.create(new_client)

    click.echo("Added %s" % name)

    return


@click.command()
@click.argument('id', type=int, required=True)
def remove(id):
    """
    Removes a client, i.e., marks it as "obsolete". This does not remove the client effectively
    from the system because the data related to it.

    :param id: The id of the client.
    :return: None.
    """

    if click.confirm("Are you sure?"):
        pass

    return


@click.command()
@click.argument('id', type=int, required=True)
def edit(id):
    """
    Edit a client.
    :param id: The id of the client.
    :return: Void.
    """

    prev_name = "test prev name"  # TODO: take this from sources.
    name = click.prompt("Name?", default=prev_name, type=str)

    return


client.add_command(show)
client.add_command(add)
client.add_command(remove)
client.add_command(edit)
