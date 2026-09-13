# Verification techniques

How to get evidence, rather than an impression, that events are arriving.

## What counts as evidence

| Observation | Proves |
|---|---|
| Event object present in `dataLayer` | the app called the wrapper. **Nothing about delivery.** |
| `/g/collect` request carrying `en=<event>` and `tid=<id>` | it left the browser, addressed correctly |
| Event name visible in GA4 Realtime | GA4 accepted and processed it |
| An event name **new to the property** in Realtime | unambiguously *this* test, not earlier traffic |

The last row is the strongest check available same-day. Pick a name the property has never seen and look for exactly that.

## Reading the requests

GA4 sends to `…/g/collect`. Useful query parameters:

- `en` — event name. **Absent on batched requests**, where several events travel in the POST body. A request with no `en` is normal, not a failure.
- `tid` — the measurement ID it is addressed to. Every request should carry the intended one.
- `tt` — traffic type. `internal` means an internal-traffic rule matched this client (see operation `08`).

Collecting them without devtools, when a run-JS capability is available: read `performance.getEntriesByType('resource')`, filter names containing `/g/collect`, and extract `en` and `tid` from each URL. This survives page interaction and needs no network panel.

Instrumenting `navigator.sendBeacon` or `fetch` to capture payloads also works, but GA4 chooses its transport per call — an empty capture proves nothing on its own. Resource timing is the more reliable read.

## Which scripts loaded

List script `src` values containing `gtag/js` or `gtm.js`. Two loads of the **same** `G-` ID is the ownership conflict. The Tag Manager-injected one carries extra query parameters (`cx=`, `gtm=`); a page's own snippet does not.

## Caching that will mislead you

**Tag Manager containers** are served with roughly a 15-minute max-age, and modern browsers partition the HTTP cache by top-level site. Consequences:

- a container published seconds ago may not be live in the tab under test,
- refreshing the cached copy while on one origin does **not** refresh it for another — a local dev server and the production domain hold separate copies.

Force a refetch of the container URL with cache bypass, then reload, before concluding a container change did not take effect. Checking whether the freshly fetched container even mentions the measurement ID is a fast way to confirm a publish landed.

## Exercising a `beforeunload` handler

Reloading destroys the page before you can read the result. Dispatch the event manually on `window` instead — the listener runs, the page stays, and the captured event is readable.

## Realtime vs DebugView vs reports

- **Realtime** — event counts for the last 30 minutes, no setup. The everyday check. Its window rolls, so a baseline taken 30 minutes ago is not comparable.
- **DebugView** — full parameter detail for a client in debug mode. Use when you need to see parameter *values*, not just names.
- **Standard reports** — lag, and newly registered custom dimensions are documented as taking **24–48 hours** to appear. In practice they are often much quicker — within a single evening — so it costs nothing to look early. Treat the window as the promise you make, not the earliest you check: absence before 24 h is not evidence of a fault, but presence before 24 h is perfectly normal.

## Local versus deployed

Verify in both places; they fail differently.

- **Local** proves the instrumentation and the parameter shapes.
- **Deployed** proves the shipped HTML carries the intended ID and the container agrees with it.

A build that passes locally can still deploy the wrong measurement ID. Grepping the deployed HTML for the old ID — expecting zero matches — is a cheap, decisive check.

## Your verification traffic is real data

Events sent while testing are recorded in the property like any others. Say so. An internal-traffic filter (operation `08`) prevents future test traffic; it does not remove what already arrived.
