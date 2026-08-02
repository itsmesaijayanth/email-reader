from pydantic import BaseModel, Field


class EmailSummary(BaseModel):
    """Structured AI analysis of an email."""

    subject: str

    sender: str

    recipient: str

    date: str

    summary: str = Field(
        description="Concise summary under 100 words.",
    )

    category: str

    priority: str

    sentiment: str

    action_required: bool

    action_items: list[str] = Field(
        default_factory=list,
    )

    tags: list[str] = Field(
        default_factory=list,
    )
