# 05 — Inventory Google Tag Manager

**Purpose:** List every GTM account and container (name, type, `GTM-` ID, internal account/container numbers) so the user can decide whether GTM needs consolidating.

**Inputs:** none.

**Preconditions:** `00-sign-in` done (same Google session as GA).

## Steps

1. Navigate to `https://tagmanager.google.com/#/home` and wait ~4 s.
2. Read the page text. The home table lists rows of `Account` and, beneath each, its containers with **Type** (Web / iOS / Android / Server / AMP) and **Container ID** (`GTM-XXXXXXX`).
3. For each container link, capture the href — it has the form `#/container/accounts/<GTM_ACCOUNT_NUM>/containers/<CONTAINER_NUM>`. These internal numbers are needed for admin URLs.

## Output format

| GTM account | Container | Type | Container ID | Internal path |
|---|---|---|---|---|
| `<name>` | `<name>` | Web | `GTM-…` | `accounts/<n>/containers/<m>` |

## Verification

- Every container ID matches `^GTM-[A-Z0-9]+$`.

## Undo

Read-only; nothing to undo.

## Notes

- GTM accounts are a separate hierarchy from GA accounts; names often differ. Do not assume a GTM account exists that matches the GA destination — ask the user which GTM account (existing or new) should be the target, or whether to leave GTM alone.
- Read [../references/gtm-limitations.md](../references/gtm-limitations.md) before proposing any GTM consolidation.
