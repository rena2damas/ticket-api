# Ticket Manager

A service for managing emails coming in/out from/to a O365 mailbox and integrates them with Jira.

## How does it work?

This service is suitable for anyone looking to create Jira tickets from the emails arriving to a mailbox. The motivation
behind the creation of this project is that, on one hand, Jira provides good tools to track and manage tickets, and O365
mailbox is a convenient way to receive requests in the form of an email. This solution comes to merge the best of both
worlds by allowing one to create a Jira ticket directly from a O365 email. Once a new email arrives to a mailbox, the
service picks up the message from the inbox folder, and contacts the Jira API for the creation of the ticket.

The service provides different configuration properties so that it can best fit the user's needs.

### Configuration

An ```.env``` file should contain the relevant configuration settings. As mentioned, these should be set accordingly for
a correct service usage.

A possible configuration is:

    # Database
    SQLALCHEMY_DATABASE_URI=sqlite:///example.db

    # Application context
    APPLICATION_CONTEXT=/api/tickets
    
    # verion of OpenAPI
    OPENAPI=3.0.3
    
    # The application providing info about the ticket
    TICKET_CLIENT_APP=https://example.com/
    
    # The mailbox to manage
    MAILBOX=mailbox@example.com
    
    # O365 registered tenant
    O365_TENANT_ID=...
    
    # O365 OAuth2 properties
    
    # O365 client id & secret for this application
    O365_CLIENT_ID=...
    O365_CLIENT_SECRET=...
    
    #   * 'offline_access': to be eligible to retrieve a refresh_token.
    #      Otherwise user only has access to resources for a single hour.
    #   * 'message_all': alias for 'mail.readwrite' + 'mail.send'
    #      for own user mailbox actions
    #   * 'message_all_shared': alias for 'mail.read.shared' + 'mail.readwrite.shared'
    #      for shared mailbox actions
    O365_SCOPES=offline_access,message_all,message_all_shared
    
    # Atlassian credentials
    ATLASSIAN_URL=https://atlassian.net
    ATLASSIAN_USER=me@example.com
    ATLASSIAN_API_TOKEN=...
    
    # Jira settings
    JIRA_TICKET_TYPE=Task
    JIRA_TICKET_LABELS=ticket
    JIRA_TICKET_LABEL_CATEGORIES=general,bug
    JIRA_TICKET_LABEL_DEFAULT_CATEGORY=general
    
    # Jira supported boards
    JIRA_SUPPORT_BOARD=support
    JIRA_BOARDS=JIRA_SUPPORT_BOARD
    JIRA_DEFAULT_BOARD=JIRA_SUPPORT_BOARD
    
    # Filter settings
    EMAIL_WHITELISTED_DOMAINS=example.com
    EMAIL_BLACKLIST=malicious@example.com

### O365 Authentication

Because the service relies on O365 services, one should start off by authenticating against the O365 service:

File ```o365_token.txt``` contains the authentication parameters to be exchanged with Microsoft authentication server.
The ```access_token```
is the token used in OAuth. It expires after 90 days and why it will have to be refreshed manually. Simply follow the
instructions shown in the terminal when that happens.

## Dependencies

Some dependencies require changes to the source code. To do so, get the source package from the PiPy repository. It is
usually a ```tar.gz``` file.

Then, extract the code:

```bash
tar -xvf package.tar.gz
```

Apply the code changes and create the package:

```bash
python setup.py sdist bdist_wheel
```

Add the entry to the ```requirements.txt```.

## Commands

The project provides a set of commands to be performed. To see the whole list of possible operations, run:

```bash
python main.py
```

Available options are:

* listen_for_incoming_email: start listening for incoming email.
