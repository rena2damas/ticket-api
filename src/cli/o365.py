import click
from flask import current_app
from flask.cli import AppGroup
from O365 import Account, MSOffice365Protocol
from o365_notifications.base import O365Notification
from o365_notifications.streaming.mailbox import O365MailBoxStreamingNotifications

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

    if account.is_authenticated:
        current_app.logger.info('Account already authenticated.')
    else:
        current_app.logger.info('Account not yet authenticated.')
        account.authenticate(tenant_id=current_app.config['O365_TENANT_ID'],
                             scopes=current_app.config['O365_SCOPES'])
        current_app.logger.info('Authenticated successfully.')
    return account


@o365_cli.command()
@click.option('--mailbox', '-m', type=str, help='the mailbox to manage events')
@click.option('--retries', '-r', type=int, help='number of retries when request fails')
def handle_incoming_email(mailbox=None, retries=0):
    """
    Handle incoming email.
    """

    account = authenticate(mailbox=mailbox, retries=retries)
    mailbox = account.mailbox()

    mailbox_notifications = O365MailBoxStreamingNotifications(
        parent=mailbox,
        change_type=O365Notification.ChangeType.CREATED.value
    )

    # Change Id alias to the real id for the 'RecipientsFilter' object
    sent_folder = mailbox.sent_folder()
    sent_folder = sent_folder.get_folder(folder_id=sent_folder.folder_id)

    # Filling the HPDA Support object
    manager = hpdasupport.HPDASupport(mailbox=mailbox) \
        .subscriber(mailbox_notifications) \
        .jira(url=current_app.config['ATLASSIAN_URL'],
              user=current_app.config['ATLASSIAN_USER'],
              token=current_app.config['ATLASSIAN_API_TOKEN']) \
        .filters([
        hpdasupport.SenderEmailDomainWhitelistedFilter(
            whitelisted_domains=current_app.config['EMAIL_WHITELISTED_DOMAINS']),
        hpdasupport.SenderEmailBlacklistFilter(blacklist=current_app.config['EMAIL_BLACKLIST']),
        hpdasupport.RecipientsFilter(recipient_reference=current_app.config['MAILBOX'], sent_folder=sent_folder),
        hpdasupport.ValidateMetadataFilter(),
        hpdasupport.JiraCommentNotificationFilter(mailbox=mailbox)
    ])

    # Start listening for incoming notifications...
    manager.notification_manager(connection_timeout=current_app.config['CONNECTION_TIMEOUT_IN_MINUTES'],
                                 keep_alive_interval=current_app.config['KEEP_ALIVE_NOTIFICATION_INTERVAL_IN_SECONDS'],
                                 refresh_after_expire=True)
