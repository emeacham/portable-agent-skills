#!/usr/bin/env python3
"""Validate every skill under skills/ against docs/SKILL-STRUCTURE.md.

Standard library only. Exit code 1 on any error.

Checks
  * SKILL.md exists with YAML frontmatter; name/description constraints per the
    Agent Skills spec; name == directory name; metadata is a str->str map.
  * AGENTS.md exists and has a capability-mapping table + "Hard rules".
  * operations/ has >=1 file named NN-verb-noun.md, each with the required
    sections in order.
  * workflows/*.md (if any) reference operations that exist.
  * Relative markdown links resolve.
  * --strict: grep for instance-data leaks (e-mails, 7-10 digit bare IDs,
    G-/GTM- IDs that are not placeholders, literal filesystem home paths).

Usage: python3 scripts/validate-skills.py [--strict] [SKILL_DIR ...]
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OP_FILE_RE = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
OP_SECTIONS = ["**Purpose:**", "**Inputs:**", "**Preconditions:**", "## Steps", "## Verification", "## Undo"]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

LEAK_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "e-mail address"),
    (re.compile(r"(?<![\w/#<>`-])\d{7,10}(?![\w>-])"), "bare 7-10 digit ID"),
    (re.compile(r"\bG-[A-Z0-9]{6,}\b"), "real-looking G- measurement ID"),
    (re.compile(r"\bGTM-[A-Z0-9]{5,}\b"), "real-looking GTM- container ID"),
    (re.compile(r"/(?:Users|home)/[a-z][\w-]*"), "literal home directory path"),
]
LEAK_ALLOW = re.compile(r"XXXX|<[A-Z_]+>|`[A-Z_]+`|example|placeholder", re.I)

errors: list[str] = []
warnings: list[str] = []


def err(path: str, msg: str) -> None:
    errors.append(f"{os.path.relpath(path, ROOT)}: {msg}")


def warn(path: str, msg: str) -> None:
    warnings.append(f"{os.path.relpath(path, ROOT)}: {msg}")


def parse_frontmatter(text: str) -> dict[str, object] | None:
    """Minimal YAML subset: scalars and one-level maps. Enough for the spec fields."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end].splitlines()
    data: dict[str, object] = {}
    current_map: str | None = None
    for line in block:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_map:
            k, _, v = line.strip().partition(":")
            data[current_map][k.strip()] = v.strip().strip('"').strip("'")  # type: ignore[index]
            continue
        current_map = None
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v == "":
            data[k] = {}
            current_map = k
        else:
            data[k] = v.strip('"').strip("'")
    return data


def check_links(path: str, text: str) -> None:
    base = os.path.dirname(path)
    for m in LINK_RE.finditer(text):
        target = m.group(1)
        if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, target))):
            err(path, f"broken relative link: {target}")


def check_leaks(path: str, text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), 1):
        for pat, label in LEAK_PATTERNS:
            for m in pat.finditer(line):
                window = line[max(0, m.start() - 15): m.end() + 15]
                if LEAK_ALLOW.search(window):
                    continue
                err(path, f"line {lineno}: possible instance data ({label}): {m.group(0)!r}")


def validate_skill(skill_dir: str, strict: bool) -> None:
    name = os.path.basename(skill_dir.rstrip("/"))
    skill_md = os.path.join(skill_dir, "SKILL.md")
    agents_md = os.path.join(skill_dir, "AGENTS.md")
    ops_dir = os.path.join(skill_dir, "operations")
    wf_dir = os.path.join(skill_dir, "workflows")

    if not os.path.isfile(skill_md):
        err(skill_dir, "missing SKILL.md")
        return
    text = open(skill_md, encoding="utf-8").read()
    fm = parse_frontmatter(text)
    if fm is None:
        err(skill_md, "missing or malformed YAML frontmatter")
    else:
        n = fm.get("name")
        d = fm.get("description")
        if not isinstance(n, str) or not (1 <= len(n) <= 64) or not NAME_RE.match(n):
            err(skill_md, f"invalid name {n!r} (1-64 chars, a-z0-9 and single hyphens)")
        elif n != name:
            err(skill_md, f"name {n!r} != directory name {name!r}")
        if not isinstance(d, str) or not (1 <= len(d) <= 1024):
            err(skill_md, "description missing or not 1-1024 chars")
        c = fm.get("compatibility")
        if c is not None and (not isinstance(c, str) or len(c) > 500):
            err(skill_md, "compatibility must be a string of <=500 chars")
        md = fm.get("metadata")
        if md is not None and not (isinstance(md, dict) and all(isinstance(v, str) for v in md.values())):
            err(skill_md, "metadata must be a map of string -> string")
        for key in fm:
            if key not in {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}:
                warn(skill_md, f"non-standard frontmatter key {key!r}")
    body_lines = text.count("\n")
    if body_lines > 500:
        err(skill_md, f"{body_lines} lines; spec ceiling is 500")
    elif body_lines > 300:
        warn(skill_md, f"{body_lines} lines; contract recommends <=300")
    for section in ("## Required capabilities", "## Operations"):
        if section not in text:
            err(skill_md, f"missing section {section!r}")
    check_links(skill_md, text)

    if not os.path.isfile(agents_md):
        err(skill_dir, "missing AGENTS.md")
    else:
        a = open(agents_md, encoding="utf-8").read()
        if "## Capability mapping" not in a:
            err(agents_md, "missing '## Capability mapping' table")
        if "## Hard rules" not in a:
            err(agents_md, "missing '## Hard rules'")
        check_links(agents_md, a)

    op_names: set[str] = set()
    if not os.path.isdir(ops_dir) or not os.listdir(ops_dir):
        err(skill_dir, "operations/ missing or empty")
    else:
        for f in sorted(os.listdir(ops_dir)):
            p = os.path.join(ops_dir, f)
            if not OP_FILE_RE.match(f):
                err(p, "operation file must be named NN-verb-noun.md")
                continue
            op_names.add(f[:-3])
            t = open(p, encoding="utf-8").read()
            pos = -1
            for s in OP_SECTIONS:
                i = t.find(s)
                if i == -1:
                    err(p, f"missing section {s!r}")
                elif i < pos:
                    err(p, f"section {s!r} out of order")
                else:
                    pos = i
            check_links(p, t)

    if os.path.isdir(wf_dir):
        for f in sorted(os.listdir(wf_dir)):
            if not f.endswith(".md"):
                continue
            p = os.path.join(wf_dir, f)
            t = open(p, encoding="utf-8").read()
            for s in ("**Goal:**", "## Sequence", "## Guardrails"):
                if s not in t:
                    err(p, f"missing section {s!r}")
            for ref in re.findall(r"`(\d{2}-[a-z0-9-]+)`", t):
                if ref not in op_names:
                    err(p, f"references unknown operation {ref!r}")
            check_links(p, t)

    if strict:
        for dirpath, _, files in os.walk(skill_dir):
            for f in files:
                if f.endswith(".md"):
                    p = os.path.join(dirpath, f)
                    check_leaks(p, open(p, encoding="utf-8").read())


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        if not os.path.isdir(SKILLS_DIR):
            print("no skills/ directory", file=sys.stderr)
            return 1
        targets = [os.path.join(SKILLS_DIR, d) for d in sorted(os.listdir(SKILLS_DIR))
                   if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    for t in targets:
        validate_skill(os.path.abspath(t), strict)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(targets)} skill(s) checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
