from app.gmail.client import GmailClient
from app.models.email import Email


class MarkAsReadAction:
    """Marks processed emails as read."""

    def __init__(self) -> None:
        self._gmail = GmailClient()

    def execute(
        self,
        email: Email,
    ) -> None:
        self._gmail.mark_as_read(email.id)
