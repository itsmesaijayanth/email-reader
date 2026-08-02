from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class EmailSummary:
    """Structured AI analysis of an email."""

    summary: str
    category: str
    priority: str
    sentiment: str
    action_required: bool
    action_items: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
