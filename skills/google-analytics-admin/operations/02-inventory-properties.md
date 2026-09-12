# 02 — Inventory properties in an account

**Purpose:** List every GA4 property (and app/web data streams if asked) in one account, including trashed ones, with property IDs.

**Inputs:** `ACCOUNT_ID` (from `01-inventory-accounts` or the user).

**Preconditions:** `00-sign-in` done.

## Steps

1. Open the account picker and click the account whose ID is `ACCOUNT_ID` in the "Analytics Accounts" listbox.
2. Read the accessibility tree of the listbox named **"Properties & Apps"**. Each option exposes the property **name**, the numeric **property ID**, and a link `#/a<ACCOUNT_ID>p<PROPERTY_ID>/...`.
3. Strikethrough entries are **trashed**. Record them separately — they cannot be moved.
4. An account with no properties shows a single "Open" link to `#/a<ACCOUNT_ID>p0/admin`. Record it as **empty**.
5. If measurement IDs (`G-XXXXXXX`) are needed (for code checks), open `#/a<ACCOUNT_ID>p<PROPERTY_ID>/admin/streams/table` and read each stream's measurement ID.

## Output format

| Property | ID | Status | Measurement ID(s) |
|---|---|---|---|
| `<name>` | `<id>` | live / trashed | `G-…` (optional) |

## Verification

- Every property link's account segment equals `ACCOUNT_ID`.

## Undo

Read-only; nothing to undo.

## Notes

- Repeat for every source account before starting moves; a single table with an "Account" column is easiest for the user to approve.
- Trashed properties: ask the user whether to **leave in trash** (default; they auto-purge) or **restore then move** (`Admin → Account → Trash Can → Restore`).
