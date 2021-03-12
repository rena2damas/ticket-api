import click
from flask import current_app
from flask.cli import AppGroup
from O365 import Account, MSOffice365Protocol

o365_cli = AppGroup(
    'o365',
    short_help='Handle O365 operations, mostly to handle Outlook events'
)


@o365_cli.command()
@click.option('--mailbox', '-m', type=str, help='the mailbox to manage events')
@click.option('--retries', '-r', type=int, help='number of retries when request fails')
def authenticate(mailbox=None, retries=0):
    """
    Set authorization code used for OAuth2 authentication.
    """

    credentials = (current_app.config['O365_CLIENT_ID'], None)
    protocol = MSOffice365Protocol(api_version='beta')
    account = Account(credentials,
                      protocol=protocol,
                      tenant_id=current_app.config['O365_TENANT_ID'],
                      main_resource=mailbox or current_app.config['MAILBOX'],
                      request_retries=retries)

    if not account.is_authenticated:
        account.authenticate(tenant_id=current_app.config['O365_TENANT_ID'],
                             scopes=current_app.config['O365_SCOPES'])
    current_app.logger.info('Authenticated successfully.')
