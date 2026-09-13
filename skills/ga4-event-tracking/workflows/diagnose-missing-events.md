# Workflow — Events fire but nothing appears in GA4

**Trigger phrases:** "my events aren't showing up" · "analytics isn't working" · "GA4 shows page views but no custom events" · "the tracking code runs but there's no data" · "nothing in Realtime" · "everything says (not set)"

**Goal:** Find which of the five silent failures is in play, and fix that one rather than rewriting instrumentation that was never the problem.

## Inputs to establish up front

| Input | Source |
|---|---|
| `MEASUREMENT_ID`, `CONTAINER_ID` | the app's source |
| Which event names are expected | the app's analytics module |
| Where it is being tested | dev server or deployed site — say which |
| What the user has already checked | ask; avoid repeating their work |

## The five causes, in the order worth checking

Each is silent. None produces a console error.

```
1. Destination not owned     → 00  (the ID belongs to nobody the user can see)
2. Two owners of the ID      → 02  (a GTM-loaded gtag.js swallows page gtag() calls)
3. Tag disabled by a schedule→ inspect the container tag's Advanced Settings
4. Traffic being filtered    → 08  (an Active internal-traffic filter is excluding you)
5. Parameters unregistered   → 05  (events arrive; columns read "(not set)")
```

## Sequence

```
Establish the symptom precisely
   ├── no /g/collect requests at all ──────► causes 1–3
   ├── requests exist, Realtime empty ─────► cause 4
   └── events in Realtime, reports empty ──► cause 5 (or the reporting lag)
07 verify-events-land      ← run first; it separates the three symptoms above
   │
   ├─ dataLayer has events, no network request
   │     └─► 02 resolve-tag-ownership  [Decision: which owner]
   │
   ├─ two gtag/js loads of the same ID
   │     └─► 02 resolve-tag-ownership
   │
   ├─ no requests and the container tag looks fine
   │     └─► check the tag's custom firing schedule end date
   │
   ├─ requests carry tt=internal, Realtime empty
   │     └─► 08 (working as configured — say so, it is not a bug)
   │
   └─ events in Realtime, dimensions blank
         └─► 05 register-custom-definitions + explain non-retroactivity
```

## Step detail

**Separate the symptoms before theorising.** Run `07` and classify: (a) nothing on the network, (b) network yes / Realtime no, (c) Realtime yes / reports no. Each points at a different cause, and (c) is usually not a fault at all.

**Cause 1 is the cheapest to rule out** and the most embarrassing to miss. Run `00` even when the user is confident the property exists — "we've had analytics for years" is compatible with the ID pointing at a property that was deleted.

**Cause 2 has a distinctive signature:** `dataLayer` contains perfectly formed event entries and no `/g/collect` request carries their names. Confirm by counting `gtag/js?id=` loads for the same measurement ID — two means the conflict. The decisive experiment is to disable the container locally and re-test; if the events flow, the container was the owner. Full matrix in [references/gtag-vs-gtm-ownership.md](../references/gtag-vs-gtm-ownership.md).

**Cause 3 hides in Advanced Settings.** A container tag can carry a custom firing schedule with an end date in the past, which stops it firing entirely and looks exactly like cause 2 from the page. Check it before rewriting anything.

**Cause 4 is often success, misread.** If requests carry `tt=internal` and an Active data filter excludes that value, the pipeline is working and the user is filtered out of their own reports. Verify from a different network before calling it broken.

**Cause 5 is not a delivery problem.** Events are arriving; the parameters are simply not reportable. Registering fixes it going forward only — say plainly that the earlier data reads `(not set)` permanently.

**Before concluding any fix worked,** account for caching: `gtm.js` caches for roughly 15 minutes and browsers partition that cache per site, so a just-published container change may not be live in the tab you are testing.

## Guardrails specific to this workflow

- **Do not rewrite the instrumentation first.** In four of the five causes the event code is already correct, and replacing it destroys the evidence that would have identified the real cause.
- **Do not claim a fix without re-running `07`.** Every cause here is silent; only a network request or a new-to-the-property Realtime event name is evidence.
- **Distinguish "configured" from "working"** when propagation is pending, and give the user the check to run later.
- If the root cause is an unrecoverable one — a dead property, an unregistered history — lead with that fact rather than with the remediation. The user may have been making decisions on numbers that never existed.
