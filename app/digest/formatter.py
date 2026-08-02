from collections import Counter

from app.models.digest import Digest
from app.models.email_summary import EmailSummary


class DigestFormatter:
    """Formats a digest into a human-readable report."""

    def format(
        self,
        digest: Digest,
    ) -> str:
        lines: list[str] = []

        lines.extend(self._header())

        lines.extend(self._statistics(digest))

        if digest.critical:
            lines.extend(
                self._section(
                    "🚨 Critical",
                    digest.critical,
                )
            )

        if digest.high_priority:
            lines.extend(
                self._section(
                    "⚠️ High Priority",
                    digest.high_priority,
                )
            )

        if digest.action_required:
            lines.extend(
                self._action_section(
                    digest.action_required,
                )
            )

        if digest.informational:
            lines.extend(
                self._section(
                    "ℹ️ Informational",
                    digest.informational,
                )
            )

        if digest.ignored:
            lines.extend(
                self._ignored_section(
                    digest.ignored,
                )
            )

        return "\n".join(lines)

    @staticmethod
    def _header() -> list[str]:
        return [
            "=" * 80,
            "📬 Automation Digest",
            "=" * 80,
            "",
        ]

    @staticmethod
    def _statistics(
        digest: Digest,
    ) -> list[str]:
        stats = digest.statistics

        return [
            f"Processed       : {stats.processed}",
            f"Ignored         : {stats.ignored}",
            f"Critical        : {stats.critical}",
            f"High Priority   : {stats.high_priority}",
            f"Action Required : {stats.action_required}",
            "",
        ]

    @staticmethod
    def _section(
        title: str,
        emails: list[EmailSummary],
    ) -> list[str]:
        lines = [
            "=" * 80,
            title,
            "=" * 80,
            "",
        ]

        for email in emails:
            lines.append(email.subject)
            lines.append(f"From: {email.sender}")
            lines.append(email.summary)

            if email.tags:
                lines.append(f"Tags: {', '.join(email.tags)}")

            lines.append("")

        return lines

    @staticmethod
    def _action_section(
        emails: list[EmailSummary],
    ) -> list[str]:
        lines = [
            "=" * 80,
            "✅ Action Required",
            "=" * 80,
            "",
        ]

        for email in emails:
            for item in email.action_items:
                lines.append(f"• {item}")

        lines.append("")

        return lines

    @staticmethod
    def _ignored_section(
        emails: list[EmailSummary],
    ) -> list[str]:
        counts = Counter(email.category for email in emails)

        lines = [
            "=" * 80,
            "🗑 Ignored",
            "=" * 80,
            "",
        ]

        for category, count in sorted(counts.items()):
            lines.append(f"{category:<15} {count}")

        lines.append("")

        return lines
