from googleapiclient.discovery import build

from app.contracts.gmail import GmailMessage
from app.gmail.auth import get_credentials
from app.gmail.parser import EmailParser
from app.models.email import Email


class GmailClient:
    def __init__(self):
        credentials = get_credentials()
        self.service = build("gmail", "v1", credentials=credentials)

    def get_unread_emails(self) -> list[Email]:
        """Fetch all unread emails."""

        messages = self.get_unread_messages()

        emails: list[Email] = []

        for message in messages:
            raw_message = self.get_message(message["id"])
            emails.append(EmailParser.parse(raw_message))

        return emails

    def get_message(
        self,
        message_id: str,
    ) -> GmailMessage:
        """Fetch a full Gmail message by ID."""
        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )
