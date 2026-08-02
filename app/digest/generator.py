from app.models.digest import Digest
from app.models.email_summary import EmailSummary
from app.models.statistics import Statistics
from app.rules.email_rules import EmailRules


class DigestGenerator:
    """Generate a digest from analyzed emails."""

    def generate(
        self,
        emails: list[EmailSummary],
    ) -> Digest:
        critical: list[EmailSummary] = []
        high_priority: list[EmailSummary] = []
        action_required: list[EmailSummary] = []
        informational: list[EmailSummary] = []
        ignored: list[EmailSummary] = []

        for email in emails:
            if EmailRules.is_ignored(email):
                ignored.append(email)
                continue

            if EmailRules.is_critical(email):
                critical.append(email)

            elif EmailRules.is_high_priority(email):
                high_priority.append(email)

            else:
                informational.append(email)

            if EmailRules.requires_action(email):
                action_required.append(email)

        statistics = Statistics(
            processed=len(emails),
            ignored=len(ignored),
            critical=len(critical),
            high_priority=len(high_priority),
            action_required=len(action_required),
        )

        return Digest(
            statistics=statistics,
            critical=critical,
            high_priority=high_priority,
            action_required=action_required,
            informational=informational,
            ignored=ignored,
        )
