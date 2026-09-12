# Portable skill structure (v1)

A **portable skill** is a directory that any AI harness — Claude Code, Codex, Copilot, Cursor, Gemini CLI, OpenCode, a custom agent loop, or a human — can read and act on without a platform-specific loader. It layers three conventions:

1. **Agent Skills format** (`SKILL.md` with YAML frontmatter) — the open standard already loaded natively by most harnesses.
2. **`AGENTS.md` inside the skill** — the harness-neutral entry point read by tools that don't load skills but do read `AGENTS.md` files (and by humans).
3. **Operations / workflows / references split** — so a model can run one atomic step, or the whole sequence, and only load the text it needs.

```
<skill-name>/
├── SKILL.md            # REQUIRED  frontmatter + overview + index of operations/workflows
├── AGENTS.md           # REQUIRED  harness-neutral entry point + capability mapping + hard rules
├── operations/         # REQUIRED  one file per atomic, individually runnable operation
│   └── NN-<verb-noun>.md
├── workflows/          # OPTIONAL  ordered compositions of operations with decision points
│   └── <goal>.md
├── references/         # OPTIONAL  facts, URL patterns, schemas — loaded on demand
├── scripts/            # OPTIONAL  portable executables (POSIX sh or Python stdlib preferred)
└── assets/             # OPTIONAL  templates, sample data
```

## `SKILL.md`

Frontmatter follows the Agent Skills spec:

| Field | Required | Rule |
|---|---|---|
| `name` | yes | 1–64 chars, `a-z0-9-`, no leading/trailing/double hyphen, **equals the directory name** |
| `description` | yes | ≤1024 chars; what it does **and when to trigger**; include the words users actually say |
| `license` | no | SPDX id or bundled file name |
| `compatibility` | no | ≤500 chars; only if there are environment needs (browser, network, packages) |
| `metadata` | no | string→string map; we use `author`, `version`, `structure: portable-agent-skills/v1` |
| `allowed-tools` | no | experimental; omit unless you need it |

Body (keep under ~300 lines; the spec's ceiling is 500):

1. One-paragraph purpose, including what the skill deliberately does **not** do (e.g. "never handles credentials").
2. **Required capabilities** table — abstract capability names (browser-with-user-session, file-edit, shell, ask-the-user), *not* tool names, so any harness can map them.
3. **Key facts that shape decisions** — the 3–6 things a model must know before promising anything.
4. **Operations index** — table linking every `operations/*.md` with a one-line "when".
5. **Workflows index**.
6. **Working style** — the judgment calls (what to confirm, what to verify, what to say at the end).
7. **Output** — what the user should receive when the skill finishes.

## `AGENTS.md` (inside the skill)

Written for a reader that may not know what a "skill" is. Sections, in order:

1. **What this is** (2–3 sentences).
2. **How to use it** — numbered: read SKILL.md → pick operation or workflow → open only what's needed → follow Preconditions → Steps → Verification → ask at Decision markers.
3. **Capability mapping** — table translating the abstract capabilities to concrete tools in the common harnesses, with an "Other" column.
4. **Hard rules** — the non-negotiables (credentials, destructive actions, confirmations).
5. **Files** — the tree.

## Operation files (`operations/NN-<verb-noun>.md`)

Numbered so the necessary order is visible in a directory listing, but each must be runnable **alone**. Fixed section order so a model can skim to the part it needs:

```
# NN — <Title>
**Purpose:**       one sentence
**Inputs:**        named placeholders in <ANGLE_CAPS> or `CODE_CAPS`; where each comes from
**Preconditions:** which earlier operations / permissions / user confirmations are required
## Decision        (optional) questions to ask the user, with the default
## Steps           numbered, imperative, each step observable (URL, element name, expected text)
## Verification    concrete checks; what "done" looks like
## Undo            how to reverse, or "irreversible — that's why the precondition is strict"
## Failure modes / Notes   (optional)
```

Rules:

- **No instance data.** Never bake in real account IDs, names, e-mails, paths, or org names; use placeholders and say where the value comes from ("from the user", "from operation 01").
- **Observable steps.** "Click the button named *Start move*" beats "submit the form".
- **Ask, don't assume,** at anything irreversible, terms-accepting, credential-related, or where a wrong target is costly.
- **Say what didn't change.** Users need negative confirmations ("IDs unchanged, no code changes") as much as positive ones.

## Workflow files (`workflows/<goal>.md`)

- Trigger phrases at the top (what the user might say).
- **Goal** in one sentence.
- **Inputs to establish up front** table.
- **Sequence** as an ASCII tree/list of operation numbers with `[Decision X]` markers.
- **Step detail** referencing operations by number; add only what the composition needs (ordering, batching, when to present a table).
- **Guardrails specific to this workflow.**

## `references/`

Short, single-topic files (< ~150 lines) that an operation links to. Facts, URL patterns, schemas, UI quirks. Keep links one level deep from `SKILL.md`.

## `scripts/`

Optional. Must run on macOS and Linux without installs: POSIX `sh`/`bash`, or Python 3 standard library. Print helpful errors. Never require credentials via arguments — read from the environment and document the variable name.

## Portability checklist

- [ ] `SKILL.md` frontmatter validates (`scripts/validate-skills.py` at repo root).
- [ ] `AGENTS.md` present in the skill, with a capability-mapping table.
- [ ] Every operation has Purpose / Inputs / Preconditions / Steps / Verification / Undo.
- [ ] No real IDs, names, e-mails, or org-specific paths anywhere (`scripts/validate-skills.py --strict` greps for common leak shapes).
- [ ] No harness-specific tool names outside the capability-mapping table.
- [ ] Works when read top-to-bottom by a human.
