# The gtag / Tag Manager ownership conflict

The single most expensive silent failure in GA4 instrumentation. Read before diagnosing "events fire but nothing arrives".

## The behaviour

When `gtag.js` is loaded **by Tag Manager** and that container owns a measurement ID, page-level `gtag('event', …)` calls for that ID are accepted into `dataLayer` and **never sent**.

There is no console error, no rejected promise, no failed request. The `dataLayer` entry is perfectly formed:

```
['event', 'some_event', { param: 'value', count: 3 }]
```

…and no `/g/collect` request ever carries it. The only traffic the container produces is its own enhanced-measurement events (`page_view`, `scroll`, outbound `click`), which makes the property look alive while every custom event is lost.

## The test matrix

Three configurations, measured by counting `/g/collect` requests carrying the custom event names:

| Configuration | Custom events delivered? |
|---|---|
| Container owns the ID; page has only the `dataLayer` shim | **No** |
| Container owns the ID **and** the page also calls `gtag('config', …)` for it | **No** |
| Page owns the ID; container's Google tag paused or absent | **Yes** |

Two further attempts that do **not** work when the container owns the ID:

- adding `send_to: MEASUREMENT_ID` to the event parameters,
- calling `gtag('config', MEASUREMENT_ID)` from the page afterwards to "register" the destination.

Either may appear to work once — a `config` call can flush a previously queued event, which looks like a fix and is not reproducible.

## How to recognise it in under a minute

1. List the page's script sources containing `gtag/js`. **Two loads of the same `G-` ID** is the signature. The container-injected one carries extra query parameters (`cx=`, `gtm=`); the page's own snippet does not.
2. Dump `dataLayer` and filter for entries whose first element is `'event'`. If your events are there and no `/g/collect` request carries their names, this is the cause.
3. Decisive experiment: disable the container snippet locally (comment it out, or short-circuit the loader) and re-test. If the events immediately flow, the container was the owner.

## The fix

Choose exactly one owner — see operation `02`.

- **Page owns it.** Keep the `gtag.js` loader and `gtag('config', …)` in the HTML entry point. **Pause or delete the container's Google tag** for that ID, then publish. Pausing is reversible, so prefer it on the first attempt.
- **Container owns it.** Remove the loader and `config` from the page, keep the `dataLayer` shim, and switch the app's analytics module to `dataLayer.push({ event: name, ...params })`. The container then needs a custom-event trigger and a GA4 Event tag with **every parameter mapped by hand** — the ongoing cost of this route.

## Related trap: an expired firing schedule

A container's Google tag can carry **Advanced Settings → Enable custom tag firing schedule** with a start and end date. Once the end date passes the tag stops firing entirely, and from the page this is indistinguishable from the ownership conflict: no GA script injected by the container, no events. Check the schedule before rewriting anything.

## After changing the container

`gtm.js` is served with roughly a 15-minute max-age, and browsers partition the HTTP cache per top-level site. A container published seconds ago may not be live in the tab under test, and refreshing the cache on one origin does not refresh it on another. Force a refetch before concluding the change did not work.
