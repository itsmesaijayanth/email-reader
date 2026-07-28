from app.gmail.client import GmailClient


def main():
    gmail = GmailClient()

    emails = gmail.get_unread_emails()

    for email in emails:
        print(f"Subject : {email.subject}")
        print(f"From    : {email.sender}")
        print(f"Date    : {email.date}")
        print()
        print(email.body)
        print("-" * 80)


if __name__ == "__main__":
    main()
