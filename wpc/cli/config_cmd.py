"""
Configurations command line interface.
"""

import click

from wpc.config.configurator import Configurator
from wpc.repository.customerrepo import CustomerRepo
from wpc.model.customer import Customer

# import wpc

configurator = Configurator()
cust_repo = CustomerRepo()


@click.command()
@click.option('-c', '--customer', help="The name or id of customer to set")
@click.option('--debug/--no-debug', help="Print debug stuff", default=None)
def config(customer, debug):
    """
    Configure and setup the application.
    """

    if customer is not None:
        _set_customer(customer)
    elif debug is not None:
        _set_debug(debug)
    else:
        click.echo("No operations performed.")

    return


def _set_customer(c_name_or_id):

    if c_name_or_id.isdigit():
        customer = cust_repo.find(c_name_or_id)
    else:
        customer = cust_repo.getAll(Customer.name == '%' + c_name_or_id + '%')

    if customer is None:
        click.echo("No customer with id or name %s found." % c_name_or_id)
    else:
        configurator.customer = str(customer.id)
        click.echo("Customer %s set." % customer.name)


def _set_debug(is_debug):

    configurator.debug = is_debug
    click.echo("Debug set to %s." % is_debug)
