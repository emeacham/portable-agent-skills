# 08 — Clean up empty accounts (optional, destructive)

**Purpose:** After consolidation, source GA accounts (and possibly GTM accounts/containers) are empty. Trash them so the account picker stays tidy.

**Inputs:** list of account IDs the user wants removed.

**Preconditions:**
- `04-verify-move` passed for every property that used to be in the account (the account's "Properties & Apps" list shows only the `p0/admin` placeholder).
- The user has **explicitly asked** for deletion in this session. An earlier "merge everything" is not a deletion instruction — ask: "Sources are now empty; want me to move them to the trash?"

## Steps (GA account)

1. Navigate to `https://analytics.google.com/analytics/web/#/a<ACCOUNT_ID>/admin/account/settings`.
2. Click **Move to Trash Can** → confirm.
3. Repeat per account.

## Steps (GTM account)

1. Ensure every container in it has been recreated and the sites verified on the new IDs (`06`, `07`).
2. `https://tagmanager.google.com/#/admin/accounts/<GTM_ACCOUNT_NUM>/settings` → ⋮ → **Delete** → confirm.

## Verification

- The account appears with strikethrough in the picker (GA) or is absent from the GTM home table.

## Undo

- GA: Admin → Account → Trash Can → Restore (available for ~35 days).
- GTM: containers are recoverable from Trash for 30 days; accounts are not — which is why the precondition is strict.
