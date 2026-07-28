import base64

from app.constants.gmail import (
    TEXT_HTML,
    TEXT_PLAIN,
)
from app.contracts.gmail import (
    GmailHeader,
    GmailMessage,
    GmailPart,
)
from app.models.email import Email


class EmailParser:
    @classmethod
    def parse(cls, message: GmailMessage) -> Email:
        """Convert a Gmail API message into an Email domain model."""

        payload = message["payload"]

        header_map = cls._build_header_map(payload.get("headers", []))

        return Email(
            id=message["id"],
            thread_id=message["threadId"],
            subject=header_map.get("subject", ""),
            sender=header_map.get("from", ""),
            recipient=header_map.get("to", ""),
            date=header_map.get("date", ""),
            snippet=message.get("snippet", ""),
            body=cls._extract_body(payload),
        )

    @staticmethod
    def _build_header_map(
        headers: list[GmailHeader],
    ) -> dict[str, str]:
        """Convert Gmail headers into a case-insensitive dictionary."""

        return {header["name"].lower(): header["value"] for header in headers}

    @classmethod
    def _extract_body(
        cls,
        payload: GmailPart,
    ) -> str:
        """Extract and decode the preferred email body."""

        part = cls._find_best_body_part(payload)

        if part is None:
            return ""

        encoded = part.get("body", {}).get("data", "")

        return cls._decode_body(encoded)

    @classmethod
    def _find_best_body_part(
        cls,
        payload: GmailPart,
    ) -> GmailPart | None:
        """
        Return the preferred body part.

        Preference:
            1. text/plain
            2. text/html
            3. payload.body (single-part emails)
        """

        parts = payload.get("parts", [])

        for mime_type in (TEXT_PLAIN, TEXT_HTML):
            for part in parts:
                if part.get("mimeType") == mime_type:
                    return part

        return payload

    @staticmethod
    def _decode_body(data: str) -> str:
        """Decode Gmail Base64URL encoded content."""

        if not data:
            return ""

        padding = "=" * (-len(data) % 4)

        return base64.urlsafe_b64decode(data + padding).decode(
            "utf-8",
            errors="replace",
        )
