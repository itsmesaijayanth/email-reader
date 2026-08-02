from app.config.settings import settings
from app.digest.formatter import DigestFormatter
from app.digest.generator import DigestGenerator
from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer
from app.logging.logger import logger


class AutomationPipeline:
    """Orchestrates a complete automation run."""

    def __init__(self) -> None:
        self._gmail = GmailClient()
        self._summarizer = EmailSummarizer()
        self._generator = DigestGenerator()
        self._formatter = DigestFormatter()

    def run(self) -> None:
        logger.info("Starting automation run")

        emails = list(
            self._gmail.iter_unread_emails(
                max_results=settings.gmail_max_results,
            )
        )

        analyses = []

        for email in emails:
            try:
                logger.info(
                    "Processing email: %s",
                    email.subject,
                )

                analysis = self._summarizer.summarize(email)

                analyses.append(analysis)

                self._gmail.mark_as_read(email.id)

                logger.info(
                    "Processed successfully: %s",
                    email.subject,
                )

            except Exception:
                logger.exception(
                    "Failed processing email: %s",
                    email.subject,
                )

        digest = self._generator.generate(analyses)

        print(self._formatter.format(digest))

        logger.info("Automation run completed")
