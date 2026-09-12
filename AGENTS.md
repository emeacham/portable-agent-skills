# AGENTS.md — portable-agent-skills

You are an AI agent reading a repository of **portable skills**: runbooks that work in any harness (Claude Code, Codex, Copilot, Cursor, Gemini CLI, OpenCode, custom loops) and for humans.

## If you were sent here to *use* a skill

1. `ls skills/` and pick the skill whose name matches the task, or read the `description` line in each `skills/*/SKILL.md`.
2. Enter that directory and read its `AGENTS.md` (or `SKILL.md` — same content, different framing).
3. Follow the operation or workflow it points you to. Load `references/` files only when an operation links to them.
4. Ask the user at every **Decision** marker. Never perform a destructive or terms-accepting action the user has not explicitly requested in this session.
5. Never handle credentials: open sign-in pages and wait for the user.

## If you were sent here to *add or change* a skill

1. Read `docs/SKILL-STRUCTURE.md` — it is the contract every skill must meet.
2. Scaffold from `templates/skill-template/` (`cp -r templates/skill-template skills/<name>`), then fill in every section; delete nothing from the required section order.
3. Keep instance data out: no real account IDs, names, e-mails, hostnames, or org paths. Use placeholders and say where the value comes from.
4. Run `python3 scripts/validate-skills.py --strict` and fix everything it reports.
5. Add the skill to the table in `README.md`.

## Repository map

```
.
├── README.md                     human-facing: intent, usage, how AI should use it
├── AGENTS.md                     this file (harness-neutral)
├── CLAUDE.md                     Claude Code shim → imports AGENTS.md
├── LICENSE                       MIT
├── docs/
│   ├── SKILL-STRUCTURE.md        the portable skill contract (v1)
│   ├── HARNESS-COMPATIBILITY.md  where each harness looks for skills/instructions
│   └── CONTRIBUTING.md
├── templates/skill-template/     scaffold matching the contract
├── scripts/
│   ├── validate-skills.py        frontmatter + structure + leak checks (stdlib only)
│   └── install.sh                symlink/copy skills into harness directories
└── skills/
    └── google-analytics-admin/   GA4 + GTM administration via the user's browser session
```

## Conventions that apply repo-wide

- Operations are numbered and individually runnable; workflows compose them in the necessary order.
- Abstract capabilities (browser-with-user-session, ask-the-user, file-edit, shell, download) are mapped to concrete tools only inside each skill's `AGENTS.md` capability table.
- Markdown only; scripts are POSIX sh or Python 3 stdlib.
