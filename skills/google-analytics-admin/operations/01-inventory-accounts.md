# 01 — Inventory GA accounts

**Purpose:** Produce a list of every Google Analytics account visible to the signed-in user, with IDs, so the user can name the destination and sources unambiguously.

**Inputs:** none.

**Preconditions:** `00-sign-in` done.

## Steps

1. From any GA page, open the account picker (header button "Open the universal picker").
2. Read the accessibility tree of the listbox named **"Analytics Accounts"**. Each option exposes the account **name** and numeric **account ID**.
3. Note accounts rendered with strikethrough — those are in the trash (deleted, pending purge). Mark them `trashed`.
4. Close the picker (Escape).

## Output format

Present one compact table:

| Account | ID | Status |
|---|---|---|
| `<name>` | `<id>` | live / trashed |

Then ask (if not already stated) which account is the **destination** and which are **sources**.

## Verification

- The list count matches what the picker shows; re-read if the tree was truncated (scroll the listbox).

## Undo

Read-only; nothing to undo.

## Notes

- Account IDs are stable and appear in URLs as `#/a<ACCOUNT_ID>...`; capture them — they are what later operations use.
- If the picker is clipped by a narrow browser pane, rely on the accessibility tree rather than a screenshot.
