from app.digest.formatter import DigestFormatter
from app.digest.generator import DigestGenerator
from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer
from app.pipeline.automation import AutomationPipeline


def main() -> None:
    pipeline = AutomationPipeline(
        gmail=GmailClient(),
        summarizer=EmailSummarizer(),
        generator=DigestGenerator(),
        formatter=DigestFormatter(),
    )

    pipeline.run()


if __name__ == "__main__":
    main()
