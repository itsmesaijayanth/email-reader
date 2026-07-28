import base64

from app.models.email import Email


class EmailParser:
    @staticmethod
    def get_header(headers: list[dict], name: str) -> str:
        """Return the value of a header by name."""
        for header in headers:
            if header["name"].lower() == name.lower():
                return header["value"]
        return ""

    @staticmethod
    def decode_body(data: str) -> str:
        """Decode Gmail's Base64URL encoded body."""
        if not data:
            return ""

        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding).decode(
            "utf-8",
            errors="replace",
        )

    @classmethod
    def parse(cls, message: dict) -> Email:
        payload = message["payload"]
        headers = payload.get("headers", [])

        body = ""

        # Multipart email
        if payload.get("parts"):
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    body = cls.decode_body(
                        part.get("body", {}).get("data", "")
                    )
                    break

        # Single-part email
        else:
            body = cls.decode_body(
                payload.get("body", {}).get("data", "")
            )

        return Email(
            id=message["id"],
            thread_id=message["threadId"],
            subject=cls.get_header(headers, "Subject"),
            sender=cls.get_header(headers, "From"),
            recipient=cls.get_header(headers, "To"),
            date=cls.get_header(headers, "Date"),
            snippet=message.get("snippet", ""),
            body=body,
        )