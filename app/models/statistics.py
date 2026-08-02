from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Statistics:
    """Statistics for a single automation run."""

    processed: int
    ignored: int
    critical: int
    high_priority: int
    action_required: int
