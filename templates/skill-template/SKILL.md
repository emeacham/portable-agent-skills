---
name: skill-template
description: One or two sentences — what this skill does AND when to use it. Include the phrases users actually say ("…", "…") so the harness triggers it even when they don't name the tool.
license: MIT
compatibility: Only if needed — e.g. "Needs a browser the user can sign into" or "Requires git and network access".
metadata:
  author: your-handle
  version: "0.1.0"
  structure: portable-agent-skills/v1
---

# <Skill title>

One paragraph: what the skill operates on, on whose behalf, and what it deliberately does **not** do (credentials, deletions, …).

## Required capabilities

| Capability | Needed for | Notes |
|---|---|---|
| ask-the-user | decision points | |
| browser-with-user-session / file-edit / shell / download | which operations | |

## Key facts that shape every decision

- Fact 1 (the thing a model must know before promising anything).
- Fact 2.

## Operations (run individually)

| # | Operation | When |
|---|---|---|
| 00 | [example-operation](operations/00-example-operation.md) | … |

## Workflows (operations in the necessary order)

- [example-workflow](workflows/example-workflow.md) — …

## Working style

- What to confirm before acting; what to verify; what to say at the end.

## Output the user should get at the end

- A short summary: what changed, what didn't, what was left alone and why.
