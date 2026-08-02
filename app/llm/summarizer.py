from app.llm.client import GeminiClient
from app.llm.prompts import EMAIL_ANALYSIS_PROMPT
from app.models.email import Email
from app.models.email_summary import EmailSummary


class EmailSummarizer:
    """Generate structured AI analysis for emails."""

    def __init__(self) -> None:
        self._client = GeminiClient()

    def summarize(
        self,
        email: Email,
    ) -> EmailSummary:
        prompt = EMAIL_ANALYSIS_PROMPT.substitute(
            subject=email.subject,
            sender=email.sender,
            body=email.body,
        )

        analysis = self._client.analyze_email(prompt)

        return analysis.model_copy(
            update={
                "subject": email.subject,
                "sender": email.sender,
                "recipient": email.recipient,
                "date": email.date,
            }
        )
