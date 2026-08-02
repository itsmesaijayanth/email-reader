from collections.abc import Iterator

from googleapiclient.discovery import build

from app.contracts.gmail import GmailMessage, GmailMessageReference
from app.gmail.auth import get_credentials
from app.gmail.parser import EmailParser
from app.models.email import Email


class GmailClient:
    def __init__(self):
        credentials = get_credentials()
        self.service = build("gmail", "v1", credentials=credentials)

    def iter_unread_emails(
        self,
        max_results: int = 10,
    ) -> Iterator[Email]:
        """Yield unread emails one at a time."""

        messages = self._get_unread_messages(max_results)

        for message in messages:
            raw_message = self._get_message(message["id"])
            yield EmailParser.parse(raw_message)

    def _get_unread_messages(
        self,
        max_results: int = 10,
    ) -> list[GmailMessageReference]:
        """Fetch metadata for unread Gmail messages."""

        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["UNREAD"],
                maxResults=max_results,
            )
            .execute()
        )

        return response.get("messages", [])

    def _get_message(
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

    def mark_as_read(
        self,
        message_id: str,
    ) -> None:
        """Mark a Gmail message as read."""

        (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={
                    "removeLabelIds": ["UNREAD"],
                },
            )
            .execute()
        )
