# import wpc
import datetime
import time
from datetime import date
from pprint import pprint
import csv
import click
from dateutil import parser
from tabulate import tabulate

from wpc.model.work import Work
from wpc.model.customer import Customer
from wpc.repository.workrepo import WorkRepo
from wpc.repository.customerrepo import CustomerRepo
from wpc.config.configurator import Configurator

work_repo = WorkRepo(Work)
customer_repo = CustomerRepo(Customer)
configurator = Configurator()


class WorkCli:
    pass


@click.group()
def work():
    """
    Work's commands group.
    """
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
    Inserts work.
    """

    raise NotImplementedError


@click.command()
@click.argument('id_', type=int, required=True)
def remove(id_):
    """
    Remove work.
    :param id_: A work id.
    """
    raise NotImplementedError


@click.command()
@click.argument('id_', type=int, required=True)
def edit(id_):
    """
    Edit work details.
    :param id_: A work id.
    """
    raise NotImplementedError


@click.command()
@click.option('--export', 'operation', flag_value='export', default=True)
@click.option('--import', 'operation', flag_value='import')
@click.option('--file-type', type=click.Choice(['csv']), default='csv')
@click.option('--file', type=click.Path())
@click.option('--ignore-empty-fields/--no-ignore-empty-fields', default=False)
def data(operation, file_type, file, ignore_empty_fields):
    """
    Import or export works.
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
                                w.customer = customer_repo.find(configurator.customer)
                                w.date = parser.parse(row[0], parser.parserinfo(dayfirst=True))
                                # minutes automatically calculated from wpc.
                                # minutes = sum(map(lambda x, y: x * y, map(int, row[3].split(".")), [60, 1, 0])) if row[3] is not '' else None
                                try:
                                    minutes = datetime.datetime.strptime(row[3], "%H.%M.%S")
                                except ValueError:
                                    minutes = datetime.datetime.strptime(row[3], "%H:%M")
                                w.begin = datetime.datetime.strptime(row[1], "%H:%M") if row[1] is not '' else w.date.replace(hour=0, minute=0, second=0)
                                w.begin = w.begin.replace(year=w.date.year, month=w.date.month, day=w.date.day)
                                w.end = datetime.datetime.strptime(row[2], "%H:%M") if row[2] is not '' else w.date.replace(hour=minutes.hour, minute=minutes.minute, second=0)
                                w.end = w.end.replace(year=w.date.year, month=w.date.month, day=w.date.day)
                                w.km = row[4] if row[4] is not '' else 0
                                w.prod = False if row[5] == 'FALSE' else True
                                w.add = row[6] if row[6] is not '' else None
                                w.note = row[7] if row[7] is not '' else None
                                w.registry = row[8] if row[8] is not '' else None if ignore_empty_fields is False else ''
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
