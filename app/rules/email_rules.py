from app.models.email_summary import EmailSummary


class EmailRules:
    """Business rules for email automation."""

    IGNORED_CATEGORIES = {
        "Marketing",
        "Social",
    }

    CRITICAL_CATEGORIES = {
        "Security",
    }

    HIGH_PRIORITY_CATEGORIES = {
        "Billing",
        "Banking",
        "Work",
        "Healthcare",
    }

    @classmethod
    def is_ignored(
        cls,
        email: EmailSummary,
    ) -> bool:
        return email.category in cls.IGNORED_CATEGORIES

    @classmethod
    def is_critical(
        cls,
        email: EmailSummary,
    ) -> bool:
        return email.priority == "critical" or email.category in cls.CRITICAL_CATEGORIES

    @classmethod
    def is_high_priority(
        cls,
        email: EmailSummary,
    ) -> bool:
        return (
            email.priority == "high" or email.category in cls.HIGH_PRIORITY_CATEGORIES
        )

    @staticmethod
    def requires_action(
        email: EmailSummary,
    ) -> bool:
        return email.action_required
