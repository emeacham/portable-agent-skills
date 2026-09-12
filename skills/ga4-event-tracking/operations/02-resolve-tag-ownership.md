# 02 — Resolve who owns the measurement ID

**Purpose:** Ensure exactly one party configures GA4 for the app — the page's own `gtag` snippet **or** a Tag Manager container — because two owners silently break page-level events.

**Inputs:**
- `MEASUREMENT_ID` (from `00` or `01`)
- `CONTAINER_ID`, if the app loads Tag Manager
- Which mechanism the app's event code uses: direct `gtag()` calls, or `dataLayer.push({event: …})`

**Preconditions:**
- `00` complete.
- User informed before any container is published — publishing changes live behaviour.

## The failure this prevents

When Tag Manager loads `gtag.js` and owns the measurement ID, page-level `gtag('event', …)` calls are **accepted into `dataLayer` and never sent**. No console error, no failed request, a perfectly formed queue entry. Neither adding `send_to` nor calling `gtag('config', …)` from the page reliably rescues them. Full evidence and the three-configuration test matrix are in [references/gtag-vs-gtm-ownership.md](../references/gtag-vs-gtm-ownership.md).

## Decision — ask the user

Present the two coherent designs and their costs. There is no third option where both configure the same ID.

- **Page owns the ID (simplest when event code calls `gtag`).** The HTML entry point loads `gtag.js` and calls `gtag('config', MEASUREMENT_ID)`. The container must **not** also configure that ID — pause or delete its Google tag. Changing the ID later needs a code deploy.
- **Container owns the ID (keeps IDs out of code).** The page sends `dataLayer.push({event: 'name', …})` instead of calling `gtag`, and the container carries a GA4 Event tag plus a custom-event trigger, with **every parameter mapped by hand** in the container UI. Each new parameter later means a container change and publish.

Say which you recommend and why. For an app that already has a typed analytics module calling `gtag`, page-owns is usually the better trade; the container route means maintaining a parameter mapping in a UI instead of in code.

## Steps

### If the page owns the ID

1. In the app's HTML entry point, ensure the snippet loads `gtag.js` for `MEASUREMENT_ID` and calls both `gtag('js', new Date())` and `gtag('config', MEASUREMENT_ID)`.
2. In Tag Manager, open the container → **Tags** and find the Google tag carrying that ID. **Pause** it (reversible) rather than deleting it on the first pass.
3. Check every other tag in the container for the same measurement ID — a GA4 Event tag can target it independently of the Google tag.
4. Submit and publish the container **only after the user confirms**. Write a version description saying what changed and why.

### If the container owns the ID

1. Remove the `gtag.js` loader and the `config` call from the page. **Keep** the two-line `dataLayer` shim so queued calls survive, if any code still calls `gtag`.
2. Rewrite the app's analytics module to `dataLayer.push({ event: name, ...params })`.
3. In the container, create a custom-event trigger matching the event names and a GA4 Event tag with the event name and every parameter mapped from data-layer variables.
4. Submit and publish after confirmation.

## Verification

Run `07`. Specifically confirm:

- Exactly **one** `gtag/js?id=…` request for `MEASUREMENT_ID` in the page's network log. A GTM-injected one carries extra query parameters (`cx=`, `gtm=`); the page's own does not. Two requests for the same ID means the conflict is still live.
- A custom event produces its own `/g/collect` request.

## Undo

- A paused tag is un-paused and re-published.
- Page-side changes revert with the code.
- **A published container version is not undone by editing** — publish a further version, or use the container's **Versions** screen to re-publish the previous one.

## Failure modes / Notes

- **Container changes are cached.** `gtm.js` is served with roughly a 15-minute max-age, and browsers partition that cache per site. A page can keep loading the pre-publish container well after publishing. Force a refetch before concluding the change failed — see [references/verification-techniques.md](../references/verification-techniques.md).
- **Both products look fine in isolation.** The container reports the tag firing; the page reports the event queued. Only the absence of a network request reveals the conflict.
- If the container's Google tag also has a **custom firing schedule**, check its end date. An expired schedule stops the tag silently, which looks identical to this conflict but has a different cause.
