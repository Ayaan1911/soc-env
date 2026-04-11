---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: false
---

# Email Triage Environment

A real-world **email triage** OpenEnv environment where AI agents learn to classify and action emails (SPAM, HAM, PHISHING).

## Action Space (MCP Tools)
- `triage_email(classification, action, reasoning)`: Classify an email and recommend an action.

## Observation Space
- `email_id`: Unique identifier
- `subject`: Email subject
- `sender`: Email sender
- `body`: Email content
- `step`: Current email index
- `total_steps`: emails in task
- `progress`: Task completion score

## Tasks
- `task1`: Obvious Spam Detection (Easy)
- `task2`: Phishing Detection (Medium)
- `task3`: Spear Phishing Detection (Hard)

## License
MIT
