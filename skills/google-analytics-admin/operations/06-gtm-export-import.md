# 06 — Recreate a GTM container under another account (export → import)

**Purpose:** Because GTM cannot move a container between accounts, reproduce a container's tags/triggers/variables in a **new** container under the target GTM account. The new container has a **new `GTM-` ID**, so this operation is always paired with `07-update-site-tags`.

**Inputs:**
- Source container: `SRC_GTM_ACCOUNT_NUM`, `SRC_CONTAINER_NUM`, `SRC_CONTAINER_ID`, name, type
- Target GTM account (existing name/number, or "create new named `<name>`")
- Explicit user confirmation that a container-ID change (and code change) is acceptable

**Preconditions:**
- `05-inventory-gtm` done.
- User has **confirmed** this path after being told the ID will change. If they prefer, the default alternative is *leave GTM as-is* — containers keep working regardless of which account they sit in.
- The workspace to export has no unpublished changes the user wants to keep (export the latest **version**, not a dirty workspace, unless told otherwise).

## Steps

1. **Export the source container**
   `https://tagmanager.google.com/#/admin/accounts/<SRC_GTM_ACCOUNT_NUM>/containers/<SRC_CONTAINER_NUM>/export`
   Choose the latest published version (or the workspace if the user wants unpublished work) → **Export**. The browser downloads a JSON file. Downloading requires the user's permission in most harnesses; ask, and note the filename.
2. **Create the destination container**
   In the target GTM account: Admin → Container → **+** (Create container) → same name and same **target platform** (Web/iOS/…) as the source → Create. Accept the GTM terms only if the user has told you to create the container (the dialog is part of creation).
   Record the new `GTM-` ID.
3. **Import**
   `…/admin/accounts/<DEST_GTM_ACCOUNT_NUM>/containers/<DEST_CONTAINER_NUM>/import` → choose the exported JSON → workspace: *Existing (Default Workspace)* → **Overwrite** (the new container is empty, so overwrite is safe) → Confirm.
4. **Review** the import preview: tag/trigger/variable counts should match the source's latest version.
5. **Publish** the new container (Submit → Publish) so the new `GTM-` ID serves the same configuration.
6. Hand off to `07-update-site-tags` with `OLD_ID = SRC_CONTAINER_ID`, `NEW_ID = <new GTM id>`.
7. Only after the sites are deployed and verified (`07`, step Verification): optionally trash the old container / old GTM account (`08-cleanup-empty-accounts`).

## Verification

- Destination container's Versions page shows version 1 published with the imported items.
- Container ID recorded and different from the source.

## Undo

Keep the old container untouched until the new one is verified in production; rollback is simply reverting the snippet to `OLD_ID`.

## Notes

- GA4 configuration tags inside the container reference `G-` measurement IDs, which did **not** change if the GA property was merely moved. Nothing inside the container needs editing for a GA property move.
- Server-side containers have additional URL/transport settings that must be re-entered manually.
