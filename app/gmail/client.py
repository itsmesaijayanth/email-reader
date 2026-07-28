from googleapiclient.discovery import build

from app.gmail.auth import get_credentials


class GmailClient:
    def __init__(self):
        credentials = get_credentials()
        self.service = build("gmail", "v1", credentials=credentials)

    def get_unread_messages(self, max_results: int = 10):
        """Return unread message IDs."""
        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q="is:unread",
                maxResults=max_results,
            )
            .execute()
        )

        return response.get("messages", [])
    
    def get_message(self, message_id: str):
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