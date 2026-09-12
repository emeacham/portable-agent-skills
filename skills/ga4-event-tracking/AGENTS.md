# AGENTS.md — ga4-event-tracking

Instructions for any AI agent or harness (Claude Code, Codex, Copilot, Cursor, Gemini CLI, OpenCode, custom agents) that lands in this directory. This file is the harness-neutral entry point; `SKILL.md` is the same content in the Agent Skills format for harnesses that load skills natively.

## What this skill is

A runbook for adding Google Analytics 4 custom events to a web app **and proving the data arrives**. It covers the code (a safe `gtag` wrapper, page and SPA instrumentation) and the account side (property, tag ownership, custom dimensions and metrics, internal-traffic filtering) — because events that fire correctly into a destination nobody owns look identical to events that work.

It holds no credentials and is not an API client. Account work happens in a browser the user signs into.

## How to use it

1. Read `SKILL.md` (≈3 min) for the decision-shaping facts and the operations index.
2. Decide whether this is a **build** or a **diagnosis**:
   - "add event tracking to my app" → `workflows/instrument-a-web-app.md`
   - "my events aren't showing up" / "analytics isn't working" → `workflows/diagnose-missing-events.md`
   - a single named task ("register these dimensions", "rename that dimension") → the matching `operations/` file
3. Open only the file you need. Load `references/` when an operation links to one.
4. Follow **Preconditions → Steps → Verification** in order. Verification is not optional: this skill exists because the failure mode is silent.
5. Ask the user at every **Decision** marker. Never publish a container, activate a data filter, or delete a tag unasked.

## Capability mapping (translate to your harness)

| Skill needs | Claude Code / Cowork | Codex | Cursor | Copilot | Other |
|---|---|---|---|---|---|
| Edit files | `Edit` / `Write` | apply_patch | edit | edit | any editor |
| Browser with user session | in-app browser / Claude in Chrome | computer-use or Playwright MCP | built-in browser | Playwright MCP | any browser the user can log into |
| Read page structure | `read_page` / `find` (a11y tree) | DOM snapshot | DOM snapshot | DOM snapshot | prefer text/DOM over screenshots |
| Run JS in the page | `javascript_tool` | CDP `Runtime.evaluate` | console eval | CDP | devtools console, or ask the user to paste a snippet and report back |
| Run the app / tests | `Bash` | shell | terminal | terminal | any shell |
| Ask the user | `AskUserQuestion` | plain-text question | plain-text question | plain-text question | pause and ask |

Without a browser capability, operations `00`–`02` and `05`–`09` cannot run; you can still design a schema (`03`) and write code (`04`, `06`), but say clearly that none of it is verified and the destination is unconfirmed.

Without a run-JS capability, fall back to asking the user to open devtools → Network, filter on `collect`, and report the event names and `tid` they see.

## Hard rules

- Never type, store, or request passwords, 2FA codes, or API tokens. Open the sign-in URL, ask the user to sign in, wait.
- Never publish a Tag Manager container, or set a GA4 data filter to **Active**, without an explicit current instruction. Both change live behaviour; an active filter discards data that cannot be recovered.
- Never delete or archive a custom definition, tag, or trigger unasked. Archiving frees a slot but breaks existing reports.
- Never claim events are working on the strength of code review or a `dataLayer` dump. Cite a network request or a Realtime count.
- Do not silently invent a new event parameter when a registered one fits. Say which you reused and why.
- State plainly when data is unrecoverable (unregistered history, filtered traffic) rather than implying it can be recovered later.

## Files

```
ga4-event-tracking/
├── SKILL.md                 # Agent Skills entry point (frontmatter + overview + index)
├── AGENTS.md                # this file — harness-neutral entry point
├── operations/              # one file per atomic, individually-runnable operation
├── workflows/               # ordered compositions: build, and diagnose
└── references/              # naming rules, the gtag/GTM trap, SPA patterns, verification, UI notes
```
