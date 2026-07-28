from dataclasses import dataclass


@dataclass(slots=True)
class Email:
    id: str
    thread_id: str
    subject: str
    sender: str
    recipient: str
    date: str
    snippet: str
    body: str
