# 07 — Update site tag snippets in project code

**Purpose:** When (and only when) a GTM container ID or a GA measurement ID has changed, find every occurrence in the affected project(s) and update it.

**Inputs:**
- `OLD_ID` → `NEW_ID` pairs (e.g. `GTM-<old> → GTM-<new>`, or `G-<old> → G-<new>`)
- Path(s) to the project repositories (ask the user; never guess a filesystem location)

**Preconditions:**
- A file-edit capability on the machine/container that holds the repo.
- The user has confirmed the code change (this is the only code-touching operation in the skill).

## When this operation is NOT needed

- A GA4 **property move** (`03`) — property ID and `G-` IDs are unchanged.
- Leaving GTM containers in their current accounts — `GTM-` IDs are unchanged.

State this explicitly to the user instead of searching the code for nothing.

## Steps

1. Search the repo for each `OLD_ID` (case-sensitive) across all text files. Typical locations: `index.html`, `_document.*`, `app.component.html`, `layout.*`, `angular.json`/`environment*.ts`, `.env*`, `gtag`/`dataLayer` setup, `nuxt.config`, `next.config`, tag-manager helper modules, README/docs.
2. Replace `OLD_ID` with `NEW_ID` in each hit. Keep both `<script>` (head) and `<noscript>` (body) GTM snippets in sync.
3. Search for the ID **without** its prefix as well (some code builds `"GTM-" + id`).
4. Run the project's formatter/lint if one exists; do not otherwise refactor.
5. Show the user the diff (file list + before/after lines) and let them commit/deploy, or commit if they asked you to.

## Verification

- Zero remaining occurrences of `OLD_ID` in tracked files (`git grep OLD_ID` returns nothing).
- After deploy: GTM **Preview** or the browser network log on the live site shows a request to `gtm.js?id=NEW_ID` (or `gtag/js?id=NEW_G_ID`).

## Undo

Revert the commit / re-run the replacement in reverse.
