from app.digest.formatter import DigestFormatter
from app.digest.generator import DigestGenerator
from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer


class AutomationPipeline:
    """Orchestrates a complete automation run."""

    def __init__(self) -> None:
        self._gmail = GmailClient()
        self._summarizer = EmailSummarizer()
        self._generator = DigestGenerator()
        self._formatter = DigestFormatter()

    def run(self) -> None:
        emails = list(
            self._gmail.iter_unread_emails(
                max_results=10,
            )
        )

        analyses = []

        for email in emails:
            analysis = self._summarizer.summarize(email)
            analyses.append(analysis)

            self._gmail.mark_as_read(email.id)

        digest = self._generator.generate(analyses)

        print(self._formatter.format(digest))
