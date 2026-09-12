# Contributing

1. Scaffold: `cp -r templates/skill-template skills/<name>`; `<name>` must match the frontmatter `name` (lowercase, hyphens).
2. Write `SKILL.md` first (description = what + when; be specific about trigger phrases), then `AGENTS.md`, then operations, then any workflow, then references.
3. Keep instance data out. If you developed the skill against a real account, replace every ID/name/e-mail with a placeholder and a note on where the value comes from.
4. Every operation needs Purpose, Inputs, Preconditions, Steps, Verification, Undo. Steps must be observable (URL, element name, expected text).
5. Validate: `python3 scripts/validate-skills.py --strict`. CI runs the same command.
6. Add the skill to the README table. One skill per PR.

Style: imperative voice; explain *why* a rule exists instead of shouting MUST; prefer tables for inventories and decisions; keep `SKILL.md` under 300 lines and references under 150.
