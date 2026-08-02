from string import Template

EMAIL_ANALYSIS_PROMPT = Template(
    """
You are an intelligent email assistant.

Analyze the following email.

Requirements:

- Write a concise summary under 100 words.
- Ignore greetings and signatures.
- Preserve important names, dates, deadlines and action items.
- Infer the appropriate category.
- Infer the priority.
- Infer the sentiment.
- Set action_required appropriately.
- Populate action_items when necessary.
- Generate useful tags.

Email

Subject:
$subject

From:
$sender

Body:
$body
""".strip()
)
