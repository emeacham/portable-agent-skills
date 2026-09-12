# AGENTS.md — <skill-name>

Instructions for any AI agent or harness that lands in this directory. `SKILL.md` carries the same content in the Agent Skills format.

## What this skill is

2–3 sentences.

## How to use it

1. Read `SKILL.md`.
2. Decide: one operation (`operations/NN-*.md`) or the workflow (`workflows/*.md`).
3. Open only what you need; follow **Preconditions → Steps → Verification**.
4. Ask the user at every **Decision** marker.

## Capability mapping (translate to your harness)

| Skill needs | Claude Code / Cowork | Codex | Cursor | Copilot | Other |
|---|---|---|---|---|---|
| ask-the-user | `AskUserQuestion` | plain-text question | plain-text question | plain-text question | pause and ask |
| file-edit | `Edit` | apply_patch | edit | edit | any editor |
| (add rows for browser / shell / download as needed) | | | | | |

## Hard rules

- Never handle credentials.
- Never delete / accept terms / spend without an explicit instruction in the current session.
- Report what was left untouched and why.

## Files

```
<skill-name>/
├── SKILL.md
├── AGENTS.md
├── operations/
├── workflows/
└── references/
```
