from typing import NotRequired, TypedDict


class GmailMessageReference(TypedDict):
    id: str
    threadId: str


class GmailHeader(TypedDict):
    name: str
    value: str


class GmailBody(TypedDict, total=False):
    data: str
    size: int
    attachmentId: str


class GmailPart(TypedDict, total=False):
    partId: str
    mimeType: str
    filename: str
    headers: list[GmailHeader]
    body: GmailBody
    parts: list["GmailPart"]


class GmailMessage(TypedDict):
    id: str
    threadId: str
    snippet: str
    payload: GmailPart

    labelIds: NotRequired[list[str]]
    historyId: NotRequired[str]
    internalDate: NotRequired[str]
    sizeEstimate: NotRequired[int]
