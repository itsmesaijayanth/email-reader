from app.llm.client import GeminiClient
from app.llm.prompts import SUMMARY_PROMPT
from app.models.email import Email
from app.models.email_summary import EmailSummary


class EmailSummarizer:
    """Generate AI summaries for emails."""

    def __init__(self) -> None:
        self._client = GeminiClient()

    def summarize(
        self,
        email: Email,
    ) -> EmailSummary:
        prompt = SUMMARY_PROMPT.format(
            subject=email.subject,
            sender=email.sender,
            body=email.body,
        )

        summary = self._client.generate(prompt)

        return EmailSummary(summary=summary)
