# Workflow — Instrument a web app with GA4 events

**Trigger phrases:** "add analytics to my app" · "add event tracking" · "I want to track what people do on the site" · "add GA4 events to the game" · "set up custom dimensions" · "measure engagement on these pages"

**Goal:** Go from no useful tracking to events arriving in a property the user owns, with the parameters reportable and the user's own traffic excluded.

## Inputs to establish up front

| Input | Source |
|---|---|
| `MEASUREMENT_ID`, `CONTAINER_ID` | the app's source (`00` step 1) |
| What question the tracking should answer | the user — ask if they have not said |
| Which pages or interactions matter | reading the source + the user |
| Destination property | `00`, or `01` if none exists |

## Sequence

```
00 verify-destination-property
   ├── owned ──────────────► 03
   └── not owned ─► [Decision A: create a property?] ─► 01 ─► 03
03 design-event-schema  ─► [Decision B: confirm the schema table]
02 resolve-tag-ownership ─► [Decision C: page owns or container owns]
05 register-custom-definitions        ← before any events ship
04 add-analytics-module
06 instrument-pages
07 verify-events-land   ─► if it fails, go to workflows/diagnose-missing-events.md
   └── ship (commit / deploy) ─► 07 again, against production
08 filter-internal-traffic ─► [Decision D: confirm, not retroactive]
09 maintain-custom-definitions (only if a parameter's meaning widened)
```

## Step detail

**Start with `00`, always.** Two minutes here prevents building an entire event schema on a destination nobody owns. If it comes back "not owned", stop and report before proposing `01` — the user may know which account it belongs to.

**Decision A — create a property?** Only on an explicit yes. Say that a new property starts empty and any history at the old ID is unrecoverable.

**`03` before `02`,** because the schema determines whether the page or the container is the better owner: an app that already calls `gtag` from a typed module wants page-ownership; one willing to push to `dataLayer` can let the container own it, at the cost of mapping every parameter by hand.

**Decision B — show the schema table** (event → parameters → dimension/metric) before implementing. This is the cheapest moment to cut scope, and the moment to check the slot budget.

**`05` before `04`/`06` is deliberate.** Registration is not retroactive. Registering while the code is still local means no `(not set)` gap at all. If the user would rather see it working first, that is a legitimate choice — state the cost and record the date from which data is trustworthy.

**`04` then `06`.** One module, then call sites. Keep `gtag` out of components.

**`07` twice:** once locally, once against the deployed site. The local run proves the instrumentation; the production run proves the deployed HTML carries the right ID and the container agrees. They fail differently.

**Decision D — the internal-traffic filter** is opt-in and the user must know it does not remove existing test events.

## Guardrails specific to this workflow

- Do not commit or deploy before `07` passes locally. Shipping an unverified pipeline means the first evidence arrives from real users, and by then the `(not set)` gap is real.
- Do not register definitions for parameters the schema has not settled — scope and parameter are locked after save.
- Do not publish a Tag Manager container or activate a data filter without an explicit current instruction.
- If the user already has live traffic on an unregistered schema, lead with that: the history to date cannot be recovered into reports, and the honest fix is to register now and note the cutover date.
- Report which pages were deliberately left untracked. Silence about a route reads as an oversight.
