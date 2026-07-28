from app.gmail.client import GmailClient


def main():
    gmail = GmailClient()

    messages = gmail.get_unread_messages()

    print(f"Found {len(messages)} unread emails")

    for message in messages:
        print(message["id"])


if __name__ == "__main__":
    main()