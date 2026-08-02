SUMMARY_PROMPT = """
You are an expert executive assistant.

Summarize the following email.

Requirements:
- Keep the summary under 100 words.
- Preserve important names, dates, deadlines, and action items.
- Ignore greetings and signatures.
- Use concise professional language.

Email:

Subject:
{subject}

From:
{sender}

Body:
{body}
""".strip()
