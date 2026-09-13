# 05 — Register custom dimensions and metrics

**Purpose:** Make the schema's parameters reportable, **before** events start arriving.

**Inputs:**
- The dimension and metric table from `03`
- The target property (from `00` or `01`)

**Preconditions:**
- `03` complete and agreed with the user.
- Ideally run **before** the instrumented code reaches production. Registration is not retroactive.

## Why the ordering matters

A report shows a custom dimension only from the moment it was created. Everything collected earlier reads `(not set)` — permanently, in the GA4 UI. The raw parameter survives in a BigQuery export if one is enabled, but nothing backfills the reports. If code is already live and unregistered, say plainly that the gap is unrecoverable rather than implying a later fix.

## Decision

- **Dimension, metric, or both?** Group-by parameters are dimensions; summed or averaged numbers are metrics. Register both only when both readings answer a question.
- **Slot budget.** 50 event-scoped dimensions and 50 metrics per property. Confirm the list before creating 20 entries.

## Steps

1. Navigate to **Admin → Data display → Custom definitions** in the target property.
2. For each dimension: **Custom dimensions** tab → **Create custom dimension** → fill
   - *Dimension name* — the report label, e.g. `Play type`. No hyphens; spaces and underscores are allowed.
   - *Scope* — **Event**.
   - *Description* — say what values it carries; future-you reads this when the meaning widens.
   - *Event parameter* — the exact `snake_case` parameter name. **Type it even if the dropdown has not seen it**; the field accepts unseen names, which is what makes pre-registration possible.
   Then **Save**.
3. For each metric: **Custom metrics** tab → **Create custom metric** → name, description, event parameter, and **Unit of measurement**. The unit is **required** and has no default — Save stays disabled until it is set. Use *Standard* for counts and scores; *Seconds* (under Time) for durations.
4. After each save, confirm the new row appears with the right parameter in the *User Property/Parameter* column.

## Verification

- The dimensions and metrics tables list every planned entry with the correct parameter name and scope.
- Read at least one entry back from its edit dialog rather than the list — the list truncates descriptions.
- Count matches the schema table from `03`.
- The custom definitions exist **before** the events ship. If they do not, record the date from which data is trustworthy.

## Undo

Definitions are **archived**, not deleted. Archiving frees the slot and removes the dimension from reports, including historical rows. **Scope and event parameter cannot be changed after save** — a typo there means archive and re-create, spending a second slot. Name and description stay editable (`09`).

## Failure modes / Notes

- **Do not batch clicks without waiting.** The Save button needs a moment after a dropdown selection; a click sent immediately after choosing a unit can be dropped, and the entry silently never saves. Re-read the list after each save rather than trusting the click.
- **A narrow browser pane clips the dialog** and puts Save off-screen. Collapse the admin sidebar or scroll horizontally. See [references/ga4-ui-notes.md](../references/ga4-ui-notes.md).
- Dimensions are documented as taking **24–48 hours** to appear in standard reports, and that is the figure to quote — but they frequently show up much sooner, sometimes within hours. Check an exploration's dimension picker before telling the user to wait a day. Realtime and DebugView show the raw parameters immediately either way, so same-day verification never depends on this.
