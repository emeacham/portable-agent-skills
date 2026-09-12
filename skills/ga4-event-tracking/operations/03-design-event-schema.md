# 03 — Design the event schema

**Purpose:** Decide the event names and parameters before writing code, so that registration (`05`), instrumentation (`06`), and reporting all agree.

**Inputs:**
- The app's meaningful user actions and outcomes (from reading the source and asking the user)
- Existing custom definitions in the property, if any (from `05` or the property's Custom definitions screen)

**Preconditions:**
- `00` complete — there is no point designing a schema for a destination nobody owns.

## Decision

- **What is worth an event?** Ask the user what question they want answered. "Which game do people pick" and "do readers of the manual go on to play" are answerable; "everything" is not, and produces a schema nobody queries.
- **Slot budget.** 50 event-scoped custom dimensions and 50 custom metrics per property. If the natural schema needs more, cut to the parameters that answer a stated question.

## Steps

1. **Use GA4's recommended event names wherever they genuinely fit** — `level_start`, `level_end`, `post_score`, `unlock_achievement`, `select_content`, `share`, `tutorial_begin`. These land in GA4's built-in reports; invented names only appear in explorations. Do not force a fit: a wrong recommended name is worse than an honest custom one. List in [references/ga4-event-naming.md](../references/ga4-event-naming.md).
2. **Name custom events in `snake_case`**, describing what happened, not what the code did: `shot_result`, `play_call`, `manual_open`.
3. **Decide one event per interaction, and where the outcome rides.** If the outcome is known within a few hundred milliseconds of the action and no state has changed, put both on one event. If resolving the action mutates the state you would want to report (a play that rewrites down and distance), emit the decision at the time it is made and the outcome separately — otherwise the parameters describe a world that no longer exists.
4. **Stamp a discriminator on every event** when the app has several comparable areas (`game`, `section`, `product`). One parameter makes every report splittable.
5. **Reuse parameter names across areas.** The same `result`, `source`, and `exit` used by three different pages is one registered dimension answering three questions; three near-synonyms are three slots and no cross-page comparison.
6. **Split dimensions from metrics.** Something you group *by* is a dimension (`play_type`, `down`). A number you sum or average is a metric (`yards`, `duration_sec`). A parameter can be registered as both if both readings are useful.
7. **Write the schema down** as a table of event → parameters → dimension or metric, and show it to the user before implementing. This is the cheapest moment to change it.

## Verification

- Every event name is `snake_case`, ≤40 characters, and not a reserved GA4 name.
- Every parameter appears in the table with a decided registration type, or is explicitly marked "not registered — available in BigQuery/DebugView only".
- Total new dimensions + metrics fit the remaining slot budget.
- No parameter duplicates an existing registered one under a different name.

## Undo

Paper exercise; nothing to reverse. Changing it after `05` costs a slot and a `(not set)` gap, which is exactly why this operation precedes it.

## Failure modes / Notes

- **High-volume events.** One event per shot or per play is fine for GA4's limits, but decide deliberately rather than by accident, and prefer a rolled-up summary event when the per-interaction detail answers no stated question.
- **Booleans and enumerations.** GA4 stores parameter values as strings or numbers. A small closed set of string values (`make`/`miss`) reports far better than free text.
- **Do not instrument privacy-sensitive choices** just because they are clickable. Measuring whether a policy page is read is a different act from recording which opt-out a reader reached for; decide explicitly and say so in the summary.
