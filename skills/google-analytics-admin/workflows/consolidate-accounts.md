# Workflow — Consolidate several GA accounts into one

Use when the user says any of: "merge my analytics accounts", "condense everything into one account", "move all properties under X", "clean up GA and Tag Manager".

**Goal:** Every live GA4 property from the source accounts ends up under the destination account with unchanged IDs; GTM is handled according to the user's explicit choice; the user receives a precise report of what changed and what did not.

## Inputs to establish up front

| Input | Source |
|---|---|
| Destination GA account (name and/or ID) | user |
| Source GA accounts (names and/or IDs) — or "everything else" | user |
| Whether GTM should be consolidated too | ask at step 5 |
| Repo paths for any site whose tag ID changes | ask only if step 6 is chosen |

## Sequence

```
00 sign-in
 └─ 01 inventory-accounts ─────────────────────────────┐
     └─ 02 inventory-properties (each source + dest)   │  read-only; present one table,
                                                        │  confirm dest/sources
 [Decision A: trashed properties?]                      │
 [Decision B: permissions mode]                         │
 └─ 03 move-property  (× every live property)          │  writes
     └─ 04 verify-move                                 │
 └─ 05 inventory-gtm                                   │  read-only
 [Decision C: GTM strategy]                             │
     ├─ leave as-is  ────────────────────────────┐     │
     └─ 06 gtm-export-import (× container)       │     │  writes + code
         └─ 07 update-site-tags                  │     │
 [Decision D: delete emptied accounts?]          │     │
 └─ 08 cleanup-empty-accounts (optional) ◄───────┘     │
 └─ Final report ◄─────────────────────────────────────┘
```

## Step detail

1. **`00-sign-in`.** Wait for the user.
2. **`01-inventory-accounts`.** If the user gave IDs, match them to names here and echo back the mapping so a typo can't send properties to the wrong account.
3. **`02-inventory-properties`** for the destination and every source. Present a single table (Account · Property · ID · Status). Also note whether the destination is currently empty.
4. **Decisions A and B** (one question, two parts, only if relevant):
   - A — trashed properties found: *leave in trash* (default) or *restore and move*.
   - B — permissions: *keep existing* (default) or *replace with destination's*.
5. **`03-move-property`** for each live property, one after another (they queue server-side; no need to wait between them). Handle the data-sharing warning as described in the operation.
6. **`04-verify-move`.** Do not report success until every property's link shows the destination account ID and the original property ID.
7. **`05-inventory-gtm`.** Present the table.
8. **Decision C** — explain in one paragraph that GTM has no move feature, so consolidation means export/import → new `GTM-` IDs → snippet edits in each site's code → old accounts deleted afterwards. Offer:
   - **Leave GTM as-is** (recommended default; containers keep working; zero code changes).
   - **Consolidate into `<existing GTM account>`** or **into a new GTM account named `<name>`** → run `06` per container, then `07` per site (ask for repo paths first).
9. **Decision D** — the source GA accounts (and any emptied GTM accounts) are now empty. Ask whether to trash them; run `08` only on a yes.
10. **Final report** (format in `SKILL.md` → "Output the user should get"). Always include the sentence about whether code changes were needed.

## Guardrails specific to this workflow

- Never start moves before the user has seen the inventory table and the destination is unambiguous.
- Never run `06`/`07` without Decision C being an explicit yes; the default is to skip.
- Never run `08` without Decision D being an explicit yes.
- If any verification fails, stop, report, and ask — do not retry moves blindly (a pending move can take minutes).
