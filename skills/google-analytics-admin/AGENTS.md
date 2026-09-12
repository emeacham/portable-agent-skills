# AGENTS.md — google-analytics-admin

Instructions for any AI agent or harness (Claude Code, Codex, Copilot, Cursor, Gemini CLI, OpenCode, custom agents) that lands in this directory. This file is the harness-neutral entry point; `SKILL.md` is the same content in the Agent Skills format for harnesses that load skills natively.

## What this skill is

A runbook for administering Google Analytics 4 and Google Tag Manager through the web UI, in a browser session the user signs into. It is **not** an API client and holds no credentials.

## How to use it

1. Read `SKILL.md` (≈2 min). It contains the decision-shaping facts and the index of operations.
2. Decide whether the user wants **one operation** or the **consolidation workflow**:
   - "move property X to account Y" → `operations/03-move-property.md` (+ `04-verify-move.md`)
   - "what analytics accounts do I have" → `operations/01-inventory-accounts.md`
   - "merge/condense/consolidate my accounts" → `workflows/consolidate-accounts.md`
3. Open only the operation/workflow file you need; open `references/` files when an operation points to them.
4. Follow the operation's **Preconditions → Steps → Verification** in order. Do not skip Verification; GA moves are asynchronous.
5. Ask the user at every **Decision** marker. Never guess a destination account or delete anything unasked.

## Capability mapping (translate to your harness)

| Skill needs | Claude Code / Cowork | Codex | Cursor | Copilot | Other |
|---|---|---|---|---|---|
| Browser with user session | in-app browser / Claude in Chrome | computer-use or Playwright MCP | built-in browser | Playwright MCP | any browser automation the user can log into |
| Read page structure | `read_page` / `find` (a11y tree) | DOM snapshot | DOM snapshot | DOM snapshot | prefer text/DOM over screenshots |
| Ask the user | `AskUserQuestion` | plain-text question | plain-text question | plain-text question | pause and ask |
| Edit files (optional) | `Edit` | apply_patch | edit | edit | any editor |

If the browser capability is absent, stop and tell the user this skill needs a browser they can sign into.

## Hard rules

- Never type, store, or request passwords, 2FA codes, or API tokens. Open the sign-in URL, ask the user to log in, wait.
- Never delete a GA account, property, or GTM container without an explicit, current instruction from the user.
- Before a GTM export/import (which changes the container ID and therefore site code), confirm with the user; offer "leave GTM as-is" as the default.
- Report what was left untouched and why.

## Files

```
google-analytics-admin/
├── SKILL.md                 # Agent Skills entry point (frontmatter + overview + index)
├── AGENTS.md                # this file — harness-neutral entry point
├── operations/              # one file per atomic, individually-runnable operation
├── workflows/               # ordered compositions of operations with decision points
└── references/              # facts, URL patterns, and UI notes loaded on demand
```
