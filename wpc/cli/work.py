import datetime
import click


@click.group()
def work():
    """
    Group commands for works.
    :return: None.
    """
    return


@click.command()
@click.option('--start', type=str, help='Filter work from date.')
def show(start):
    """
    Shows registered works.

    :return: None.
    """

    # from_dt = datetime.date.fromtimestamp()

    click.echo(start)

    return


@click.command()
def add():
    """
    Insert a client into the system.

    :return: None.
    """

    name = click.prompt("Name", type=str)

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
    :return: None.
    """

    prev_name = "test prev name" # TODO: take this from sources.
    name = click.prompt("Name?", default=prev_name, type=str)

    return


work.add_command(show)
work.add_command(add)
work.add_command(remove)
work.add_command(edit)
