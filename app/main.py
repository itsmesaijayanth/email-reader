from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer


def main() -> None:
    gmail = GmailClient()
    summarizer = EmailSummarizer()

    for email in gmail.iter_unread_emails(max_results=5):
        summary = summarizer.summarize(email)

        print("=" * 80)
        print(f"Subject : {email.subject}")
        print(f"From    : {email.sender}")
        print(f"Date    : {email.date}")
        print()
        print(summary.summary)
        print("-" * 80)


if __name__ == "__main__":
    main()
