# 04 — Verify a property move

**Purpose:** Confirm each moved property now lives under `DEST_ACCOUNT_ID`, with the same property ID (and therefore the same measurement IDs), and that the source no longer lists it.

**Inputs:** `DEST_ACCOUNT_ID`, list of `(PROPERTY_NAME, PROPERTY_ID)` expected.

**Preconditions:** `03-move-property` started for each property; wait ≥10 s (up to a few minutes for large properties).

## Steps

1. Navigate to `https://analytics.google.com/analytics/web/#/a<DEST_ACCOUNT_ID>/admin/account` and reload.
2. Open the account picker, select the destination account, read the **"Properties & Apps"** listbox.
3. For each expected property, check an option exists whose link is `#/a<DEST_ACCOUNT_ID>p<PROPERTY_ID>/…` — the account segment must be the destination and the property segment must be the **original** ID.
4. Optionally select each source account and confirm its "Properties & Apps" list no longer contains the property (an emptied account shows one `p0/admin` link).
5. If a property is missing, wait 60 s and re-check once more before reporting a problem.

## Verification

This operation *is* the verification. It passes when every expected property appears under the destination with its original ID and none remain in the sources.

## Output format

| Property | ID | Now under | Measurement IDs changed? |
|---|---|---|---|
| `<name>` | `<id>` | `<dest name> (<dest id>)` | No |

State explicitly: **"Property and measurement IDs are unchanged — no site code changes are needed."**

## Undo

Read-only; nothing to undo. If a move is wrong, run `03-move-property` in reverse.

## Notes

- If the user also wants proof at the stream level, open `#/a<DEST_ACCOUNT_ID>p<PROPERTY_ID>/admin/streams/table` and quote the `G-` IDs.
