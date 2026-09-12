# 09 — Maintain custom definitions as their meaning widens

**Purpose:** Keep dimension names and descriptions honest when a parameter starts carrying values it did not originally cover.

**Inputs:**
- The dimension or metric to revise, and the new values it now carries

**Preconditions:**
- The definition exists (`05`).

## When this is needed

Reusing an existing parameter in a new place is usually the right call — it costs no slot and keeps data comparable. The cost is drift: a dimension described as "how a player left mid-game" that now also carries values from a manual and a landing page is misleading to whoever reads it in six months, including the user.

Revise the definition in the same change that widens the parameter, not later.

## Decision

- **Rename, or only re-describe?** Renaming changes the label in every report and exploration. In a young property with no saved reports the cost is near zero and an accurate name is worth it; in an established one, ask first — someone may have built reports around the old label.

## Steps

1. Admin → Data display → **Custom definitions** → the relevant tab.
2. Find the row, open its row menu (⋮) → **Edit**.
3. Update the **Description** to enumerate the values the parameter now carries, and where each comes from.
4. Update the **Dimension name** only if the decision above said so.
5. **Save.** The dialog's Save button may sit off-screen in a narrow pane; collapse the sidebar or scroll horizontally.

## Verification

- Re-open the edit dialog and read the stored value back. The list view truncates descriptions, so the row text is not sufficient evidence.
- If renamed, confirm the old name no longer appears in the definitions list.

## Undo

Edit again and restore the previous text. Names and descriptions are freely editable, so this is fully reversible.

## Failure modes / Notes

- **Scope and Event parameter are locked after creation** and appear greyed out. Changing either means archiving the definition and creating a new one, which spends a slot and splits the data at that date. This is exactly why `03` and `05` are worth doing carefully.
- **Archiving is not renaming.** Archiving removes the dimension from reports including historical rows; it is not the way to fix a label.
- A widened parameter is still one dimension. Values from different events coexist fine because reports break down by event name — that is what makes reuse cheaper than a new slot.
