# Automation Output Design

## Vision

The purpose of the automation framework is **not** to summarize individual emails.

Its purpose is to answer one question:

> **"What do I need to know or do right now?"**

Every source (Gmail, Slack, GitHub, Calendar, WhatsApp, etc.) should produce structured events that can be combined into a single intelligent digest.

---

# Processing Pipeline

```
Trigger
    │
    ▼
Source Connector
    │
    ▼
Normalization
    │
    ▼
LLM Analysis
    │
    ▼
Automation Rules
    │
    ▼
Digest Generator
    │
    ▼
Destination
```

---

# Processing Stages

## 1. Source Connector

Responsible for fetching raw data.

Examples:

- Gmail
- Slack
- GitHub
- Google Calendar
- WhatsApp
- Jira

Output:

```
Raw Source Data
```

---

## 2. Normalization

Every connector converts its data into a common domain model.

Example:

```
Email

Message

Issue

CalendarEvent

Notification
```

The rest of the pipeline should never know where the data came from.

---

## 3. LLM Analysis

The LLM enriches each item.

Output:

```
summary

category

priority

sentiment

action_required

action_items

tags
```

No business logic lives here.

The LLM only analyzes.

---

## 4. Automation Rules

Business rules determine what should happen.

Examples:

```
Marketing
↓

Ignore
```

```
Security
↓

Always notify
```

```
Billing
↓

Notify if payment due
```

```
GitHub PR

↓

Notify only if review requested
```

This stage should be deterministic.

No AI.

---

## 5. Digest Generator

Responsible for producing one consolidated output.

Instead of

Email 1

Email 2

Email 3

...

it generates

```
Morning Digest

Processed:
42 items

Ignored:
29

Critical:
1

High Priority:
3

Action Required:
4
```

---

# Digest Structure

```
Automation Digest

Run Time

Sources

Statistics

Critical

High Priority

Action Required

Important Updates

Informational

Ignored

Errors
```

---

# Statistics

Example

```
Processed

42

Ignored

29

Critical

1

Action Required

4
```

---

# Critical

Only items that require immediate attention.

Examples:

- Security alerts

- Payment failures

- Account suspension

- Production incidents

---

# High Priority

Important but not urgent.

Examples:

- Interview scheduled

- Invoice received

- PR review requested

---

# Action Required

Concrete actions.

Example

```
• Reply to HR

• Review PR #123

• Pay electricity bill

• Confirm travel booking
```

---

# Important Updates

Useful information that does not require action.

Examples:

```
Your package has shipped.

Flight delayed.

Meeting rescheduled.
```

---

# Informational

Interesting updates.

Examples:

```
Weekly engineering report

Monthly expense summary
```

---

# Ignored

These should not clutter the digest.

Examples:

- Marketing

- Promotions

- Newsletters

- Social media digests

Instead of listing them individually:

```
Ignored

31 Promotions

14 Social

8 Marketing
```

---

# Errors

Pipeline failures.

Example:

```
Unable to summarize

Google API timeout

Slack authentication failed
```

---

# Destinations

The digest should be independent of where it is delivered.

Examples:

Console

Slack

Telegram

Discord

WhatsApp

Email

Every destination renders the same digest.

---

# Future Sources

The digest must support multiple connectors.

Example

```
Gmail

Slack

GitHub

Calendar
```

without changing the digest format.

---

# Design Principles

- Connectors only fetch data.
- Models represent normalized data.
- LLM analyzes content.
- Rules make decisions.
- DigestGenerator creates output.
- Destinations render output.
- Each layer has a single responsibility.

---

# End Goal

A single automation run should answer:

- What is important?
- What requires action?
- What changed?
- What can be ignored?

without requiring the user to inspect every individual notification.