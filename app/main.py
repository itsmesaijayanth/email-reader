from app.digest.formatter import DigestFormatter
from app.digest.generator import DigestGenerator
from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer


def main() -> None:
    gmail = GmailClient()
    summarizer = EmailSummarizer()
    generator = DigestGenerator()
    formatter = DigestFormatter()

    emails = list(gmail.iter_unread_emails(max_results=10))

    analyses = []

    for email in emails:
        analysis = summarizer.summarize(email)
        analyses.append(analysis)

        gmail.mark_as_read(email.id)

    digest = generator.generate(analyses)

    print(formatter.format(digest))


if __name__ == "__main__":
    main()
