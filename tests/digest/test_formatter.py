from app.digest.formatter import DigestFormatter
from app.models.digest import Digest
from app.models.email_summary import EmailSummary
from app.models.statistics import Statistics


def make_summary(
    *,
    subject="Subject",
    category="Other",
):
    return EmailSummary(
        subject=subject,
        sender="alice@example.com",
        recipient="bob@example.com",
        date="2026-08-02",
        summary="Summary",
        category=category,
        priority="low",
        sentiment="neutral",
        action_required=False,
        action_items=[],
        tags=[],
    )


def test_formatter():
    digest = Digest(
        statistics=Statistics(
            processed=5,
            ignored=1,
            critical=1,
            high_priority=1,
            action_required=0,
        ),
        critical=[
            make_summary(
                subject="Security Alert",
                category="Security",
            )
        ],
        high_priority=[
            make_summary(
                subject="Splitwise",
                category="Billing",
            )
        ],
        informational=[make_summary()],
        ignored=[make_summary(category="Marketing")],
    )

    output = DigestFormatter().format(digest)

    assert "Automation Digest" in output
    assert "Security Alert" in output
    assert "Splitwise" in output
    assert "Marketing" in output
