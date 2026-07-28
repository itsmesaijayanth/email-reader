from app.gmail.client import GmailClient
from app.gmail.parser import EmailParser


def main():
    gmail = GmailClient()

    messages = gmail.get_unread_messages(max_results=1)

    raw_email = gmail.get_message(messages[0]["id"])

    email = EmailParser.parse(raw_email)

    print("=" * 80)
    print(f"Subject : {email.subject}")
    print(f"From    : {email.sender}")
    print(f"Date    : {email.date}")
    print("-" * 80)
    print(email.body)


if __name__ == "__main__":
    main()