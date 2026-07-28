from unittest.mock import MagicMock, call, patch

import pytest

from app.models.email import Email


def test_get_unread_messages(gmail_client):
    client, messages = gmail_client

    messages.list.return_value.execute.return_value = {
        "messages": [
            {"id": "1", "threadId": "t1"},
            {"id": "2", "threadId": "t2"},
        ]
    }

    result = client._get_unread_messages()

    assert result == [
        {"id": "1", "threadId": "t1"},
        {"id": "2", "threadId": "t2"},
    ]

    messages.list.assert_called_once_with(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=10,
    )


def test_get_unread_messages_returns_empty_list(gmail_client):
    client, messages = gmail_client

    messages.list.return_value.execute.return_value = {}

    assert client._get_unread_messages() == []


def test_get_message(gmail_client):
    client, messages = gmail_client

    raw_message = {
        "id": "123",
        "threadId": "456",
        "snippet": "hello",
        "payload": {},
    }

    messages.get.return_value.execute.return_value = raw_message

    assert client._get_message("123") == raw_message

    messages.get.assert_called_once_with(
        userId="me",
        id="123",
        format="full",
    )


@patch("app.gmail.client.EmailParser.parse")
def test_iter_unread_emails(parser_mock, gmail_client):
    client, messages = gmail_client

    messages.list.return_value.execute.return_value = {
        "messages": [
            {"id": "1", "threadId": "t1"},
            {"id": "2", "threadId": "t2"},
        ]
    }

    messages.get.side_effect = [
        MagicMock(
            execute=MagicMock(
                return_value={
                    "id": "1",
                    "threadId": "t1",
                    "snippet": "",
                    "payload": {},
                }
            )
        ),
        MagicMock(
            execute=MagicMock(
                return_value={
                    "id": "2",
                    "threadId": "t2",
                    "snippet": "",
                    "payload": {},
                }
            )
        ),
    ]

    email1 = MagicMock(spec=Email)
    email2 = MagicMock(spec=Email)

    parser_mock.side_effect = [email1, email2]

    emails = list(client.iter_unread_emails())

    assert emails == [email1, email2]
    assert parser_mock.call_count == 2

    messages.get.assert_has_calls(
        [
            call(userId="me", id="1", format="full"),
            call(userId="me", id="2", format="full"),
        ]
    )


@patch("app.gmail.client.EmailParser.parse")
def test_iter_unread_emails_empty_inbox(parser_mock, gmail_client):
    client, messages = gmail_client

    messages.list.return_value.execute.return_value = {"messages": []}

    emails = list(client.iter_unread_emails())

    assert emails == []

    parser_mock.assert_not_called()
    messages.get.assert_not_called()


def test_iter_unread_emails_passes_max_results(gmail_client):
    client, messages = gmail_client

    messages.list.return_value.execute.return_value = {"messages": []}

    list(client.iter_unread_emails(max_results=25))

    messages.list.assert_called_once_with(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=25,
    )


def test_get_message_propagates_api_error(gmail_client):
    client, messages = gmail_client

    messages.get.return_value.execute.side_effect = RuntimeError("API Error")

    with pytest.raises(RuntimeError, match="API Error"):
        client._get_message("123")
