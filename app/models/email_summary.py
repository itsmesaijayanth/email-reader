from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmailSummary:
    """AI-generated summary of an email."""

    summary: str
