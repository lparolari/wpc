from datetime import date

import click
from tabulate import tabulate

from wpc.model.work import Work
from wpc.repository.workrepo import WorkRepo

work_repo = WorkRepo(Work)


@click.group()
def work():
    """
    Work's commands group.
    """
    return


@click.command()
@click.argument('begin', type=str) # help='Filter work from date.')
@click.argument('end', type=str) # help='Filter work to date.')
def between(begin, end):
    # parse begin date, parse end date
    # filter
    return


@click.command()
@click.option('--day', type=click.IntRange(1, 31), help='Filter work by day (month is assumed as current).')
@click.option('--month', type=click.IntRange(1, 12), help='Filter work by month (year is assumed the current).')
@click.option('--year', type=int, help='Filter work by year.')
@click.option('--all', 'all_', is_flag=True, help='Show all.')
def show(day, month, year, all_):
    """
    Shows registered works.

    By default, shows works from this month. You can use the ``--all`` option to show all registered works.
    You can combine other options in this way:
     - day
     - month
     - year
     - day & month
     - month & year
     - day & month & year
    """

    works = []
    try:
        if year is not None or month is not None or day is not None:

            do = day is not None
            mo = month is not None
            yo = year is not None

            # only year is provided.
            if yo and not mo and not do:
                works = work_repo.getByYear(year)
            # only month is provided.
            if mo and not yo and not do:
                works = work_repo.getByMonth(month)
            # only day is provided.
            if do and not yo and not mo:
                works = work_repo.getByDay(day)

            # year and month, not day provided.
            if yo and mo and not do:
                works = work_repo.getByMonth(month, year)
            # month and day, not year provided.
            if mo and do and not yo:
                works = work_repo.getByDay(day, month)
            # year and day is not a useful case.
            if yo and do and not mo:
                raise ValueError("year and day cannot be combined together")

            # both year, month and day provided.
            if yo and mo and do:
                works = work_repo.getByDay(day, month, year)
        elif all_:
            works = work_repo.getAll()
        else:
            # default get by month
            works = work_repo.getByMonth(date.today().month)
    except ValueError as e:
        click.echo("ValueError: " + str(e), err=True)
        return

    headers = ['Customer', 'Date', 'Begin', 'End', 'Hours', 'Registry']
    rows = [[w.customer.name, w.datestr, w.beginstr, w.endstr, w.hours, w.registry] for w in works]

    click.echo(tabulate(rows, headers))

    return


@click.command()
def add():
    """
    Insert a client into the system.
    """

    # name = click.prompt("Name", type=str)

    return


@click.command()
@click.argument('id', 'id_', type=int, required=True)
def remove(id_):
    """
    Removes a client, i.e., marks it as "obsolete". This does not remove the client effectively
    from the system because the data related to it.

    :param id_: The id of the client.
    """

    if click.confirm("Are you sure?"):
        pass

    return


@click.command()
@click.argument('id', 'id_', type=int, required=True)
def edit(id_):
    """
    Edit a client.
    :param id_: The id of the client.
    """

    prev_name = "test prev name"  # TODO: take this from sources.
    name = click.prompt("Name?", default=prev_name, type=str)

    return


work.add_command(between)
work.add_command(show)
work.add_command(add)
work.add_command(remove)
work.add_command(edit)
