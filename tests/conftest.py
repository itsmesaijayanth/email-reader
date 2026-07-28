from unittest.mock import MagicMock, patch

import pytest

from app.gmail.client import GmailClient


@pytest.fixture
def gmail_client():
    """Create a GmailClient with a mocked Gmail API."""

    service = MagicMock()
    messages = service.users.return_value.messages.return_value

    with (
        patch("app.gmail.client.get_credentials"),
        patch("app.gmail.client.build", return_value=service),
    ):
        yield GmailClient(), messages
