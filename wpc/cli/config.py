"""
Configurations command line interface.
"""

import click

from wpc.config.configurator import Configurator
from wpc.repository.customerrepo import CustomerRepo
from wpc.model.customer import Customer

configurator = Configurator()
cust_repo = CustomerRepo()


@click.command()
@click.option('-c', '--set-customer', help="Select a customer and remember it for the whole session")
def config(set_customer):
    """
    Config command.
    """

    if set_customer is not None:
        _set_customer(set_customer)
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
