# 03 — Move a GA4 property to another account

**Purpose:** Relocate one property (with its data, streams, and IDs) from `SOURCE_ACCOUNT_ID` to `DEST_ACCOUNT_ID`.

**Inputs:**
- `SOURCE_ACCOUNT_ID`, `PROPERTY_ID` (from `02-inventory-properties`)
- `DEST_ACCOUNT_ID` / destination account **name** (from the user)
- `PERMISSIONS_MODE`: `keep` (default) or `replace` — see Decision below

**Preconditions:**
- `00-sign-in` done; user has Edit (or Admin) on both accounts.
- Property is **not** in the trash.
- User has explicitly named the destination account.

## Decision (ask once per consolidation, not per property)

- **Permissions:** "Keep existing property permissions" copies the property's current users along; "Replace with destination account permissions" makes it inherit the destination's users. When the same person owns everything, either is fine — default to *keep* unless the user wants a clean permission set.

## Steps

1. Navigate directly to the move page:
   `https://analytics.google.com/analytics/web/#/a<SOURCE_ACCOUNT_ID>p<PROPERTY_ID>/admin/property/move`
   (Equivalent UI path: Admin → Property → Property details → **Move property**.)
2. Wait ~3 s; confirm the heading **"Move Property"** and the sentence "Your changes will affect **<property name>**". If the sidebar overlaps the form, collapse it (chevron at the sidebar's bottom) and scroll left.
3. Click the **"Select a destination account"** dropdown and choose the option whose text is the destination account's name. Verify the dropdown now shows that name.
4. Select the permissions radio per `PERMISSIONS_MODE`.
5. Tick the **Confirm changes** checkbox (Terms-of-Service acknowledgement for the destination account). The user's instruction to move is the authorization; do not re-ask.
6. Click **Start move**.
7. If a **Warning** dialog appears saying data-sharing settings differ and the property will inherit the destination's, click **Confirm** — inheriting the destination's settings is the expected outcome of consolidation. (Mention it in the final report.)
8. Expect a dialog **"Move request is pending"**. Dismiss it (Go to Admin / Escape).

## Verification

Run `04-verify-move` after all moves are queued (they complete in seconds to minutes).

## Undo

Run this same operation with source and destination swapped. IDs are unchanged either way.

## Failure modes

- **"Start move" disabled:** destination not selected or checkbox unticked.
- **No destination in dropdown:** the user lacks Edit on that account, or the destination is the same account.
- **Property in trash:** restore first (`02` Notes).
- **Property has an active Google Ads / Search Console / BigQuery link:** links move with the property, but re-check them afterwards (Admin → Product links).
