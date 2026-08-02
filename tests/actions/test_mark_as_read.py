from unittest.mock import patch

from app.actions.mark_as_read import MarkAsReadAction
from app.models.email import Email


@patch("app.actions.mark_as_read.GmailClient")
def test_mark_as_read(mock_client):
    email = Email(
        id="123",
        thread_id="456",
        subject="Subject",
        sender="alice@example.com",
        recipient="bob@example.com",
        date="today",
        snippet="",
        body="hello",
    )

    action = MarkAsReadAction()

    action.execute(email)

    mock_client.return_value.mark_as_read.assert_called_once_with("123")
