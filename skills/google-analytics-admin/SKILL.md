---
name: google-analytics-admin
description: Administer Google Analytics 4 (GA4) and Google Tag Manager (GTM) through the web UI on the user's behalf — inventory accounts/properties/containers, move GA4 properties between accounts, consolidate several GA accounts into one, work around GTM's lack of a "move container" feature (export/import + site tag updates), and clean up empty accounts. Use whenever the user mentions Google Analytics, GA4, Tag Manager, GTM, measurement IDs (G-XXXX), container IDs (GTM-XXXX), merging/consolidating/moving analytics accounts or properties, or asks which analytics account a site reports to — even if they don't say "GA4" explicitly.
license: MIT
compatibility: Needs a browser the user can sign into (in-app browser, browser extension, Playwright/Chrome MCP, or computer use). File-edit access is needed only if site tag snippets must change. No API keys required; everything runs in the user's own signed-in session.
metadata:
  author: emeacham
  version: "1.0.0"
  structure: portable-agent-skills/v1
---

# Google Analytics Admin

Operate the GA4 and GTM admin UIs in a browser the **user** has signed into. You never handle credentials: open the sign-in page, ask the user to log in, then proceed.

Everything account-specific (account IDs, property names, container IDs, which account is the "keeper") comes from the user's request or from what you observe in the UI during the session. Nothing in this skill assumes a particular account.

## Required capabilities

| Capability | Needed for | Notes |
|---|---|---|
| Browser the user can sign into | all operations | Prefer accessibility-tree reads over screenshots; GA's UI is wide and clips in narrow panes. |
| Ask-the-user | decision points | Destination account, permission mode, GTM strategy, trashed items. |
| File edit (optional) | `07-update-site-tags` | Only when a GTM container ID or measurement ID changes. |

If the harness lacks a browser, stop and say so; do not try to use the Admin API with credentials you were not given.

## Key facts that shape every decision

Read [references/ga4-move-semantics.md](references/ga4-move-semantics.md) before promising anything. The short version:

- **GA4 accounts cannot be merged.** "Merge A into B" means *move every property from A into B*, then optionally delete A.
- **Moving a GA4 property keeps its property ID, data streams, and `G-` measurement IDs.** Historical data comes along. **No site code changes are required** for a GA property move.
- **GTM has no "move container" feature.** Consolidating containers means export → create a new container in the target account → import → the container gets a **new `GTM-` ID** → the snippet on every site that uses it must be updated. This is the only path that touches code, so always confirm it with the user before doing it.
- **Trashed properties cannot be moved.** They must be restored first or left to auto-purge.
- Moves are asynchronous ("Move request is pending"); verify after a short wait.

## Operations (run individually)

Each file in `operations/` is self-contained: purpose, inputs, preconditions, steps, verification, undo. Run one when the user asks for just that thing.

| # | Operation | When |
|---|---|---|
| 00 | [sign-in](operations/00-sign-in.md) | Always first. |
| 01 | [inventory-accounts](operations/01-inventory-accounts.md) | List every GA account the user can see. |
| 02 | [inventory-properties](operations/02-inventory-properties.md) | List properties (live + trashed) in one account. |
| 03 | [move-property](operations/03-move-property.md) | Move one GA4 property to another account. |
| 04 | [verify-move](operations/04-verify-move.md) | Confirm a property landed and IDs are unchanged. |
| 05 | [inventory-gtm](operations/05-inventory-gtm.md) | List GTM accounts and containers. |
| 06 | [gtm-export-import](operations/06-gtm-export-import.md) | Recreate a container under another GTM account. |
| 07 | [update-site-tags](operations/07-update-site-tags.md) | Patch `GTM-`/`G-` IDs in project code when they change. |
| 08 | [cleanup-empty-accounts](operations/08-cleanup-empty-accounts.md) | Delete (trash) accounts left empty after moves. |

## Workflows (operations in the necessary order)

- [consolidate-accounts](workflows/consolidate-accounts.md) — merge N source accounts into one destination account, including the GTM decision and the code-change decision. This is the workflow to use for "condense everything into one account".

## Working style

- **Confirm before anything irreversible or terms-accepting.** The move dialog includes an acknowledgement checkbox; the user's explicit instruction to move the property is the authorization to tick it, but a *destination* they did not name, a *permissions mode*, or a *delete* always gets an explicit question.
- **Inventory first, then act, then verify.** Report the inventory back in one compact table before starting moves so the user can catch a wrong target.
- **Prefer URL navigation.** GA4's SPA routes are stable; see [references/ga4-url-patterns.md](references/ga4-url-patterns.md). Jumping straight to `.../admin/property/move` avoids fragile menu clicking.
- **Read the accessibility tree, not pixels,** for lists (account picker, property list). Screenshots are for confirming dialog state.
- **Narrow browser panes clip GA.** Collapse the admin sidebar and scroll horizontally before clicking coordinates, or use element refs.
- **Say what did *not* change.** After a GA move: "IDs unchanged, no code changes." After a GTM recreation: "new container ID, snippet updated in <files>."

## Output the user should get at the end

A short summary listing: destination account; each property moved (name + ID); anything intentionally left alone (trashed items, GTM containers) and why; any code files changed; and any now-empty source accounts with an offer to delete them.
