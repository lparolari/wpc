import click


@click.group()
def client():
    pass


@click.command()
@click.option('--id',   type=int, help='The id of the client.')
@click.option('--name', type=str, help='The name of the client.')
def show(id, name):
    """
    Shows registered clients. If no filter is specified shows all clients.
    """
    click.echo("Registered clients:")
    for x in [1, 10]:
        click.echo(x)

    pass


@click.command()
@click.argument('name', type=str, required=True)
def add(name):
    click.echo("Added %s" % name)
    pass


@click.command()
def remove():
    pass


@click.command()
def edit():
    pass


client.add_command(show)
client.add_command(add)
client.add_command(remove)
client.add_command(edit)
