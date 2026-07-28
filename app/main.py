from app.gmail.client import GmailClient


def main() -> None:
    gmail = GmailClient()

    for email in gmail.iter_unread_emails(max_results=5):
        print(f"Subject : {email.subject}")
        print(f"From    : {email.sender}")
        print(f"Date    : {email.date}")
        print()
        print(email.body)
        print("-" * 80)


if __name__ == "__main__":
    main()
