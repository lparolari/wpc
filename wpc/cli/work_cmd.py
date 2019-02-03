# import wpc
import datetime
import time
from datetime import date
from pprint import pprint

import click
from dateutil import parser
from tabulate import tabulate

from wpc.model.work import Work
from wpc.model.customer import Customer
from wpc.repository.workrepo import WorkRepo
from wpc.repository.customerrepo import CustomerRepo
import csv

work_repo = WorkRepo(Work)
customer_repo = CustomerRepo(Customer)


class WorkCli:
    pass


@click.group()
def work():
    """
    Work's commands group.
    """
    return


@click.command()
@click.argument('begin', type=str)  # help='Filter work from date.')
@click.argument('end', type=str)  # help='Filter work to date.')
def between(begin, end):
    # parse begin date, parse end date
    # filter

    raise NotImplementedError

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

    headers = ['Client', 'Date', 'Begin', 'End', 'Hours', 'Registry']
    rows = [[w.client.name if w.client_id is not None else '', w.datestr, w.beginstr, w.endstr, w.hours, w.registry] for w in works]

    click.echo(tabulate(rows, headers))

    return


@click.command()
def add(import_file):
    """
    Insert a client into the system.
    """

    raise NotImplementedError


@click.command()
@click.argument('id_', type=int, required=True)
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
@click.argument('id_', type=int, required=True)
def edit(id_):
    """
    Edit a client.
    :param id_: The id of the client.
    """

    raise NotImplementedError

    prev_name = "test prev name"  # TODO: take this from sources.
    name = click.prompt("Name?", default=prev_name, type=str)

    return


@click.command()
@click.option('--export', 'operation', flag_value='export', default=True)
@click.option('--import', 'operation', flag_value='import')
@click.option('--file-type', type=click.Choice(['csv']), default='csv')
@click.option('--file', type=click.Path())
@click.argument('customer_id', type=int, required=True)
def data(operation, file_type, file, customer_id):
    """
    Import or export w data.
    """

    # TODO: this operations should be encapsulated out cli package.
    if operation == 'import':
        if file_type == 'csv':
            if file is not None:
                with open(file, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if row[0] is not '':
                            if line_count >= 2:

                                #parserinfo = parser.parserinfo(dayfirst=True)

                                w = Work()
                                w.customer = customer_repo.find(customer_id)
                                w.date = parser.parse(row[0], parser.parserinfo(dayfirst=True))
                                w.begin = datetime.datetime.strptime(row[1], "%H:%M") if row[1] is not '' else None
                                w.begin = w.begin.replace(year=w.date.year, month=w.date.month, day=w.date.day)
                                w.end = datetime.datetime.strptime(row[2], "%H:%M") if row[2] is not '' else None
                                w.end = w.end.replace(year=w.date.year, month=w.date.month, day=w.date.day)
                                # minutes automatically calculated from wpc.
                                # w.minutes = sum(map(lambda x, y: x * y, map(int, row[3].split(".")), [60, 1, 0])) if row[3] is not '' else None
                                w.km = row[4] if row[4] is not '' else 0
                                w.prod = False if row[5] == 'FALSE' else True
                                w.add = row[6] if row[6] is not '' else None
                                w.note = row[7] if row[7] is not '' else None
                                w.registry = row[8] if row[8] is not '' else None
                                w.price = 12

                                work_repo.create(w)

                            line_count += 1

                    print(f'Processed {line_count} lines.')

    return


# disable between, not so useful. To be removed.
# work.add_command(between)
work.add_command(show)
work.add_command(add)
work.add_command(remove)
work.add_command(edit)
work.add_command(data)
