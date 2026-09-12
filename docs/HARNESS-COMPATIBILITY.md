# Harness compatibility

Where each harness discovers skills and instruction files, and how to point it at this repo. Paths verified September 2026; vendors change these — check their docs if something doesn't load.

## Skill discovery (`SKILL.md`)

| Harness | Project-level path | User-level path | Notes |
|---|---|---|---|
| Claude Code / Claude Cowork | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | Native Agent Skills; also `/plugin` marketplaces |
| OpenAI Codex (CLI/IDE) | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` | Native Agent Skills |
| Cursor | `.cursor/skills/<name>/` or `.agents/skills/<name>/` | `~/.cursor/skills/<name>/` | Native Agent Skills; `.cursor/rules/*.mdc` still works for always-on rules |
| GitHub Copilot (VS Code, CLI, coding agent) | `.github/skills/<name>/`, also reads `.claude/skills/` and `.agents/skills/` | — | Native Agent Skills |
| Gemini CLI | `.gemini/skills/<name>/` (extension-based) | `~/.gemini/skills/<name>/` | Falls back to `GEMINI.md` / `AGENTS.md` instructions |
| OpenCode / Pi / other | usually `.agents/skills/` or configurable | configurable | If unsupported, use the AGENTS.md route below |

**Broadest single path:** `.agents/skills/` (Codex, Cursor, Copilot read it). `scripts/install.sh` links skills into whichever of these you choose.

## Instruction files (for harnesses without skill loading)

| Harness | Reads |
|---|---|
| Codex, Cursor, Copilot, Gemini CLI, OpenCode, most agents | `AGENTS.md` in repo root and in subdirectories (nearest wins / merges) |
| Claude Code | `CLAUDE.md` (this repo's `CLAUDE.md` imports `AGENTS.md`) |
| Copilot (legacy) | `.github/copilot-instructions.md` |
| Cursor (legacy) | `.cursor/rules/*.mdc` |

Because every skill here ships its own `AGENTS.md`, a harness that only understands `AGENTS.md` still gets the full runbook when it enters the skill directory — or when you paste the skill path into the prompt.

## Three ways to use a skill from this repo

1. **Install into a harness** — `scripts/install.sh <skill> --target claude|codex|cursor|copilot|agents|all` (symlink by default, `--copy` to copy).
2. **Point the agent at the directory** — "Use the runbook in `skills/google-analytics-admin/` (start with AGENTS.md)". Works everywhere, including chat UIs where you paste the files.
3. **Vendor the skill** — copy the directory into your own project under the path your harness reads.

## Capability abstraction

Skills declare abstract capabilities (`browser-with-user-session`, `ask-the-user`, `file-edit`, `shell`, `download`). Each skill's `AGENTS.md` maps them to concrete tools per harness. When adding a harness, add a column there rather than editing operations.
