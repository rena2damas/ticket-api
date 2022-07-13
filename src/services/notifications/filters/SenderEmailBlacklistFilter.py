from flask import current_app

from src.services.notifications.filters.OutlookMessageFilter import OutlookMessageFilter


class SenderEmailBlacklistFilter(OutlookMessageFilter):
    """Filter for message whose sender email is not blacklisted"""

    def __init__(self, blacklist):
        self.blacklist = blacklist

    def apply(self, message):
        if not message:
            return None

        sender_email = message.sender.address
        if sender_email in self.blacklist:
            current_app.logger.info(
                f"Message skipped as the sender's email '{sender_email}' is blacklisted."
            )
            return None
        return message
