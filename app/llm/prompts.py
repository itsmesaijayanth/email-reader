from string import Template

EMAIL_ANALYSIS_PROMPT = Template(
    """
You are an intelligent email assistant.

Analyze the following email and return ONLY valid JSON.

Schema:

{
  "summary": "...",
  "category": "...",
  "priority": "...",
  "sentiment": "...",
  "action_required": true,
  "action_items": [],
  "tags": []
}

Rules:

- Return valid JSON only.
- Do not wrap the response in markdown.
- Summary must be under 100 words.
- Ignore greetings and signatures.
- Preserve important names, dates, deadlines, and action items.

Category must be one of:

- Work
- Personal
- Billing
- Banking
- Shopping
- Marketing
- Travel
- Social
- Security
- Education
- Healthcare
- Other

Priority must be one of:

- low
- medium
- high
- critical

Sentiment must be one of:

- positive
- neutral
- negative

Action items should contain only concrete actions.

Email

Subject:
$subject

From:
$sender

Body:
$body
""".strip()
)
