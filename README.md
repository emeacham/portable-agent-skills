# portable-agent-skills

Runbooks ("skills") that any AI coding agent — **Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI, OpenCode**, or a human — can pick up and execute the same way, on any platform, without a vendor-specific loader.

## Why this exists

Every harness now has its own way to load reusable instructions, and most have converged on the open [Agent Skills](https://agentskills.io) `SKILL.md` format. But a `SKILL.md` alone still leaves two gaps:

- Harnesses (and people) that don't load skills still need an entry point → every skill here also ships an **`AGENTS.md`**.
- A skill that is one long prose file can't be run *one step at a time* or *in a guaranteed order* → every skill here is split into numbered **operations** (atomic, individually runnable) and **workflows** (operations in the necessary order, with explicit decision points).

The result is a directory you can drop into `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or simply point an agent at with "use the runbook in this folder".

## Skills

| Skill | What it does | Needs |
|---|---|---|
| [`google-analytics-admin`](skills/google-analytics-admin/) | Administer GA4 and Google Tag Manager through the **user's own signed-in browser session**: inventory accounts/properties/containers, move GA4 properties between accounts, consolidate many accounts into one, handle GTM's lack of a move feature (export/import + site tag updates), clean up empty accounts. No credentials, no API keys. | a browser the user can sign into |

## Using a skill

**With a harness that loads Agent Skills** (Claude Code, Codex, Cursor, Copilot, …):

```sh
git clone https://github.com/emeacham/portable-agent-skills
cd portable-agent-skills
./scripts/install.sh google-analytics-admin --target all      # symlinks into every known skills dir
# or: --target claude | codex | cursor | copilot | agents      # one harness
# add --copy to copy instead of symlink, --project to install into ./ instead of ~/
```

Then ask in plain language: *"merge my analytics accounts into one"* — the skill's `description` is written to trigger on that.

**With anything else** (chat UI, custom agent, a harness without skill support):

> Use the runbook in `skills/google-analytics-admin/` — start with its `AGENTS.md`.

Or paste `AGENTS.md` + the one operation you need into the prompt. Each operation is self-contained.

**As a human:** read the skill's `AGENTS.md`, then the operation. They are written to be followed by hand.

## How an AI / harness should use this repo

Short version (the full text is in [`AGENTS.md`](AGENTS.md), which every major harness reads automatically):

1. Pick the skill by its `description` (in `SKILL.md` frontmatter).
2. Read the skill's `AGENTS.md`; map its **required capabilities** (browser, ask-the-user, file-edit, …) to your own tools using the table there.
3. Run **one operation** if the user asked for one thing, or the **workflow** if they asked for the end-to-end outcome. Load `references/` only when linked.
4. Follow each operation's *Preconditions → Steps → Verification*; stop and ask at every *Decision*.
5. Never handle credentials; never delete or accept terms without an explicit instruction in the current session; always report what did **not** change.

## Adding a skill

1. Read [`docs/SKILL-STRUCTURE.md`](docs/SKILL-STRUCTURE.md) — the contract (Agent Skills frontmatter + `AGENTS.md` + operations/workflows/references).
2. `cp -r templates/skill-template skills/<your-skill-name>` and fill it in. No real IDs, names, e-mails, or org paths — placeholders only.
3. `python3 scripts/validate-skills.py --strict`
4. Add a row to the table above and open a PR. See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Layout

```
skills/<name>/
├── SKILL.md        Agent Skills entry (frontmatter + overview + operation index)
├── AGENTS.md       harness-neutral entry + capability mapping + hard rules
├── operations/     NN-verb-noun.md — atomic, individually runnable
├── workflows/      goal.md — operations in necessary order with decision points
├── references/     facts, URL patterns, UI quirks (loaded on demand)
├── scripts/        optional, POSIX sh / Python stdlib only
└── assets/         optional templates and samples
```

Where each harness looks for skills and instruction files: [`docs/HARNESS-COMPATIBILITY.md`](docs/HARNESS-COMPATIBILITY.md).

## Principles

- **Portable over clever.** Markdown, placeholders, abstract capabilities. Tool names appear only in a per-skill mapping table.
- **Atomic and ordered.** Anything you can ask for on its own is an operation; the necessary sequence is a workflow.
- **Verify, then report.** Every operation ends with observable checks and a statement of what changed *and what didn't*.
- **The user owns the risk.** Credentials, deletions, terms acceptance, and code changes always go through the user.

## License

[MIT](LICENSE)
