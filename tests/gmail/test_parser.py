import base64

from app.gmail.parser import EmailParser


def encode(text: str) -> str:
    """Encode text using Gmail's Base64URL encoding."""

    return base64.urlsafe_b64encode(text.encode()).decode().rstrip("=")


def make_message(
    *,
    subject: str = "Test Subject",
    sender: str = "alice@example.com",
    recipient: str = "bob@example.com",
    date: str = "Mon, 28 Jul 2025 10:00:00 +0000",
    snippet: str = "Hello",
    body: str = "Hello World",
    mime_type: str = "text/plain",
):
    return {
        "id": "message-id",
        "threadId": "thread-id",
        "snippet": snippet,
        "payload": {
            "mimeType": mime_type,
            "headers": [
                {"name": "Subject", "value": subject},
                {"name": "From", "value": sender},
                {"name": "To", "value": recipient},
                {"name": "Date", "value": date},
            ],
            "body": {
                "data": encode(body),
            },
        },
    }


def test_parse_plain_text_email():
    message = make_message()

    email = EmailParser.parse(message)

    assert email.id == "message-id"
    assert email.thread_id == "thread-id"
    assert email.subject == "Test Subject"
    assert email.sender == "alice@example.com"
    assert email.recipient == "bob@example.com"
    assert email.date == "Mon, 28 Jul 2025 10:00:00 +0000"
    assert email.snippet == "Hello"
    assert email.body == "Hello World"


def test_parse_with_missing_headers():
    message = make_message()
    message["payload"]["headers"] = []

    email = EmailParser.parse(message)

    assert email.subject == ""
    assert email.sender == ""
    assert email.recipient == ""
    assert email.date == ""


def test_parse_empty_body():
    message = make_message(body="")

    email = EmailParser.parse(message)

    assert email.body == ""


def test_parse_missing_body_data():
    message = make_message()
    message["payload"]["body"] = {}

    email = EmailParser.parse(message)

    assert email.body == ""


def test_parse_missing_body():
    message = make_message()
    del message["payload"]["body"]

    email = EmailParser.parse(message)

    assert email.body == ""


def test_parse_html_email():
    html = "<h1>Hello</h1>"

    message = make_message(
        body=html,
        mime_type="text/html",
    )

    email = EmailParser.parse(message)

    assert email.body == html


def test_parse_prefers_plain_text():
    message = make_message()

    message["payload"] = {
        "mimeType": "multipart/alternative",
        "headers": message["payload"]["headers"],
        "parts": [
            {
                "mimeType": "text/html",
                "body": {
                    "data": encode("<b>Hello</b>"),
                },
            },
            {
                "mimeType": "text/plain",
                "body": {
                    "data": encode("Hello Plain"),
                },
            },
        ],
    }

    email = EmailParser.parse(message)

    assert email.body == "Hello Plain"


def test_parse_falls_back_to_html():
    message = make_message()

    message["payload"] = {
        "mimeType": "multipart/alternative",
        "headers": message["payload"]["headers"],
        "parts": [
            {
                "mimeType": "text/html",
                "body": {
                    "data": encode("<b>Hello HTML</b>"),
                },
            },
        ],
    }

    email = EmailParser.parse(message)

    assert email.body == "<b>Hello HTML</b>"


def test_parse_returns_empty_when_no_parts_and_no_body():
    message = make_message()

    message["payload"] = {
        "mimeType": "multipart/mixed",
        "headers": message["payload"]["headers"],
        "parts": [],
    }

    email = EmailParser.parse(message)

    assert email.body == ""


def test_parse_missing_snippet():
    message = make_message()
    del message["snippet"]

    email = EmailParser.parse(message)

    assert email.snippet == ""
