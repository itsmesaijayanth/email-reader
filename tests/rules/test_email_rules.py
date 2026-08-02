from app.models.email_summary import EmailSummary
from app.rules.email_rules import EmailRules


def make_summary(
    *,
    category="Other",
    priority="low",
    action_required=False,
):
    return EmailSummary(
        subject="Test Subject",
        sender="alice@example.com",
        recipient="bob@example.com",
        date="2026-08-02",
        summary="Summary",
        category=category,
        priority=priority,
        sentiment="neutral",
        action_required=action_required,
        action_items=[],
        tags=[],
    )


def test_marketing_email_is_ignored():
    summary = make_summary(category="Marketing")

    assert EmailRules.is_ignored(summary)


def test_social_email_is_ignored():
    summary = make_summary(category="Social")

    assert EmailRules.is_ignored(summary)


def test_security_email_is_critical():
    summary = make_summary(category="Security")

    assert EmailRules.is_critical(summary)


def test_critical_priority_email_is_critical():
    summary = make_summary(priority="critical")

    assert EmailRules.is_critical(summary)


def test_billing_email_is_high_priority():
    summary = make_summary(category="Billing")

    assert EmailRules.is_high_priority(summary)


def test_work_email_is_high_priority():
    summary = make_summary(category="Work")

    assert EmailRules.is_high_priority(summary)


def test_action_required_email():
    summary = make_summary(action_required=True)

    assert EmailRules.requires_action(summary)


def test_normal_email():
    summary = make_summary()

    assert not EmailRules.is_ignored(summary)
    assert not EmailRules.is_critical(summary)
    assert not EmailRules.is_high_priority(summary)
    assert not EmailRules.requires_action(summary)
