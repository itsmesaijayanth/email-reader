from dataclasses import dataclass, field

from app.models.email_summary import EmailSummary
from app.models.statistics import Statistics


@dataclass(slots=True, frozen=True)
class Digest:
    """Final digest produced by the automation pipeline."""

    statistics: Statistics

    critical: list[EmailSummary] = field(default_factory=list)

    high_priority: list[EmailSummary] = field(default_factory=list)

    action_required: list[EmailSummary] = field(default_factory=list)

    informational: list[EmailSummary] = field(default_factory=list)

    ignored: list[EmailSummary] = field(default_factory=list)
