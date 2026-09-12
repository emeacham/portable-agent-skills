# 06 — Instrument pages and components

**Purpose:** Emit the designed events from the app, including the single-page-app cases that are easy to get silently wrong.

**Inputs:**
- The schema from `03`
- The module from `04`

**Preconditions:**
- `04` done; `05` done or explicitly deferred with the user informed of the `(not set)` cost.

## Steps

1. **Fire user-decision events where the decision happens** — in the click handler, before any state mutation, so the parameters describe the situation the user acted on.
2. **Fire outcome events where the outcome resolves**, carrying values captured *before* the mutation if the resolution rewrites them (previous score, previous possession, whichever the report needs).
3. **For a page or overlay worth measuring dwell time on**, emit an `_open` on mount and a `_close` on unmount carrying `duration_sec`, plus an `exit` naming where the user went. Record the destination in a ref set by each link's click handler, defaulting to a generic `navigation`.
4. **Cover both exits, because they are disjoint.** Closing or reloading a tab never unmounts the component; in-app navigation never fires `beforeunload`. Register a `beforeunload` listener *and* fire from the unmount cleanup, guarded so only the first one wins.
5. **Do not call `preventDefault()` in that `beforeunload` listener** unless the page genuinely has unsaved state. It raises the browser's "Leave site?" prompt — appropriate for a game in progress, gratuitous on a manual or policy page.
6. **Guard the close with a flag scoped to the effect, not a ref.** React StrictMode double-invokes mount effects in development; a ref-based flag stays set through the simulated unmount and suppresses the real close forever. A plain local variable inside the effect gets a fresh value per run. Details and code shape in [references/spa-instrumentation-patterns.md](../references/spa-instrumentation-patterns.md).
7. **Guard events that can resolve twice.** Where an outcome path is reachable from two code paths (a timeout and a bounds check, say), set a "already reported" flag when the interaction starts and clear it on the next interaction, so the event count matches the app's own counter.
8. **Clean up timers on unmount.** A countdown left running after navigation keeps firing and can emit a completion event for a page nobody is on. This is an analytics correctness issue, not just a leak.
9. **Leave pages untracked deliberately, not accidentally.** Note in the summary which routes send nothing and why.

## Verification

- Unit tests, type-check, and build pass.
- Run the app and exercise each instrumented path, then inspect the captured events — see `07`. Check specifically that:
  - each interaction produces exactly one event,
  - `duration_sec` is non-zero after a real pause,
  - each link sets its own `exit` value,
  - the unload path fires without raising a "Leave site?" prompt.
- Development double-firing from StrictMode is expected; confirm the production build emits once.

## Undo

Revert the component changes. No account-side effects.

## Failure modes / Notes

- **Events queued but never sent** is the signature of the ownership conflict in `02`, not a bug in this operation. Check the network before rewriting instrumentation.
- **A parameter that is `undefined`** should be dropped by the module (`04`), so an exit with no link-set source simply omits the key.
- Batched `/g/collect` requests hide event names in the POST body; absence from the query string is not absence from the payload.
