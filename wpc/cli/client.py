"""
Entry point for the command line interface.
"""

import click

import wpc

# from wpc.model.customer import Customer
# from wpc.repository.repo import Repo

cli_repo = wpc.repository.Repo(wpc.model.Customer)

@click.group()
def client():
    """
    Client's commands group.
    """
    return


@click.command()
@click.option('--id', 'id_', type=int, help='The id of the client.')
@click.option('--name', type=str, help='The name of the client.')
def show(id_, name):
    """
    Shows registered clients. If no filter is specified shows all clients.

    :param id_: The id of the client.
    :param name: The name of the client.
    """

    clients = []

    # Find results.
    if id_ is not None:
        res = cli_repo.find(id_)
        if res is not None:
            clients = [res]
    elif name is not None:
        clients = cli_repo.query()\
                    .filter(wpc.model.Customer.name.like("%"+name+"%"))\
                    .all()
    else:
        clients = cli_repo.query().all()

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
    """

    name = click.prompt("Name", type=str)

    if name is None:
        click.echo("Name cannot be empty")
        return

    new_client = wpc.model.Customer(name=name)

    cli_repo.create(new_client)

    click.echo("Added %s" % name)

    return


@click.command()
@click.argument('id_', type=int, required=True)
def remove(id_):
    """
    Removes a client, i.e., marks it as "obsolete". This does not remove the client effectively
    from the system because the data related to it.

    :param id_: The id of the client.
    """
    # TODO: implement obsolete client.

    c = cli_repo.find(id_)
    if c is None:
        click.echo("Client with id %s not found." % id_)
        return

    if click.confirm("Are you sure?"):
        cli_repo.remove(c)
        click.echo("Success.")
    else:
        click.echo("OK.")

    return


@click.command()
@click.argument('id_', type=int, required=True)
def edit(id_):
    """
    Edit a client.
    :param id_: The id of the client.
    """

    c = cli_repo.find(id_)
    if c is None:
        click.echo("Client with id %s not found." % id_)
        return

    name = click.prompt("Name?", default=c.name, type=str)

    c.name = name
    cli_repo.update(c)

    click.echo("Success.")

    return


client.add_command(show)
client.add_command(add)
client.add_command(remove)
client.add_command(edit)
