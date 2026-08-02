from app.digest.generator import DigestGenerator
from app.models.email_summary import EmailSummary


def make_summary(
    *,
    category="Other",
    priority="low",
    action_required=False,
):
    return EmailSummary(
        summary="summary",
        category=category,
        priority=priority,
        sentiment="neutral",
        action_required=action_required,
        action_items=[],
        tags=[],
    )


def test_generate_digest():
    generator = DigestGenerator()

    emails = [
        make_summary(category="Marketing"),
        make_summary(category="Security"),
        make_summary(category="Billing"),
        make_summary(action_required=True),
        make_summary(),
    ]

    digest = generator.generate(emails)

    assert digest.statistics.processed == 5
    assert digest.statistics.ignored == 1
    assert digest.statistics.critical == 1
    assert digest.statistics.high_priority == 1
    assert digest.statistics.action_required == 1

    assert len(digest.ignored) == 1
    assert len(digest.critical) == 1
    assert len(digest.high_priority) == 1
    assert len(digest.informational) == 2
    assert len(digest.action_required) == 1
