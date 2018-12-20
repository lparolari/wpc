import click
from db.db import Db
from wpc.models.client import Client


@click.group()
def client():
    """
    Group commands for clients.
    :return: None.
    """
    return


@click.command()
@click.option('--id',   type=int, help='The id of the client.')
@click.option('--name', type=str, help='The name of the client.')
def show(id, name):
    """
    Shows registered clients. If no filter is specified shows all clients.

    :param id: The id of the client.
    :param name: The name of the client.
    :return: Void.
    """

    for x in [1, 2, 3]:
        click.echo(x)

    return


@click.command()
def add():
    """
    Insert a client into the system.

    :return: Void.
    """

    name = click.prompt("Name", type=str)

    # TODO: change this with the proper logic.

    # Only for testing purposes.
    db = Db()

    new_client = Client(name=name)

    db.session.add(new_client)
    db.session.commit()

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

    prev_name = "test prev name" # TODO: take this from sources.
    name = click.prompt("Name?", default=prev_name, type=str)

    return


client.add_command(show)
client.add_command(add)
client.add_command(remove)
client.add_command(edit)