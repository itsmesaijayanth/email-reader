from app.gmail.client import GmailClient
from app.llm.summarizer import EmailSummarizer


def main() -> None:
    gmail = GmailClient()
    summarizer = EmailSummarizer()

    for email in gmail.iter_unread_emails(max_results=5):
        analysis = summarizer.summarize(email)

        print("=" * 80)
        print(f"Subject  : {email.subject}")
        print(f"From     : {email.sender}")
        print(f"Category : {analysis.category}")
        print(f"Priority : {analysis.priority}")
        print(f"Sentiment: {analysis.sentiment}")
        print(f"Action   : {analysis.action_required}")

        if analysis.action_items:
            print("\nAction Items")
            for item in analysis.action_items:
                print(f"• {item}")

        if analysis.tags:
            print("\nTags")
            print(", ".join(analysis.tags))

        print("\nSummary")
        print(analysis.summary)
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()
