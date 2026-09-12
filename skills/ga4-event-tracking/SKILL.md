---
name: ga4-event-tracking
description: Instrument a web app with Google Analytics 4 custom events and prove the data actually arrives — design the event schema, add a safe gtag wrapper, instrument pages and SPA routes, register custom dimensions and metrics before traffic starts, resolve who owns the measurement ID when both page code and Tag Manager configure it, verify at the network layer, and filter your own traffic out. Use whenever the user says add analytics, add event tracking, track clicks or gameplay, custom dimensions, custom metrics, GA4 events, gtag, dataLayer, measurement ID, "my events aren't showing up in GA4", "analytics isn't working", "(not set) in my report", or asks why numbers look wrong.
license: MIT
compatibility: Needs file-edit access to the web app, plus a browser the user can sign into for the GA4 admin steps and for network-level verification. No API keys; GA work runs in the user's own signed-in session.
metadata:
  author: emeacham
  version: "1.0.0"
  structure: portable-agent-skills/v1
---

# GA4 Event Tracking

Add custom GA4 events to a web app and make sure they land somewhere the user can actually read. The skill covers both halves, because only doing the first half is the usual failure: code that fires perfectly formed events into a destination nobody owns produces no error anywhere.

It does **not** handle credentials (the user signs in), does not delete GA properties or containers, and does not publish a Tag Manager container without explicit instruction.

For moving properties between accounts, consolidating accounts, or GTM export/import, use the sibling skill [`google-analytics-admin`](../google-analytics-admin/SKILL.md) instead.

## Required capabilities

| Capability | Needed for | Notes |
|---|---|---|
| File edit | `04`–`06` | The app's HTML entry point and page components. |
| Browser with user session | `00`–`02`, `07`–`09` | GA4 and GTM admin UIs, and reading the app's own network requests. |
| Run JavaScript in the page | `07` | Network-level verification. A devtools/console capability or an automation driver. |
| Ask-the-user | decisions | Destination property, tag ownership, anything irreversible. |
| Shell (optional) | `06`, `07` | Running the app's test/build/deploy commands. |

## Key facts that shape every decision

- **A measurement ID in the code proves nothing.** It may belong to a deleted property, or to someone else's. Nothing fails loudly. Run `00` before writing a single event. See [references/verification-techniques.md](references/verification-techniques.md).
- **Custom dimensions and metrics are not retroactive.** A report shows a dimension only from the moment it was registered; everything collected earlier reads `(not set)`. Register before traffic starts, not after. This is the single most expensive ordering mistake in this skill.
- **A `gtag.js` loaded *by* Tag Manager swallows page-level `gtag('event', …)` calls.** The events reach `dataLayer` perfectly formed and no network request is ever made. Exactly one owner may configure a given measurement ID. See [references/gtag-vs-gtm-ownership.md](references/gtag-vs-gtm-ownership.md).
- **Registration limits are per property:** 50 event-scoped custom dimensions, 50 custom metrics, 25 user-scoped. Scope and event-parameter are **locked after save**; name and description stay editable. Budget slots before registering.
- **Verification means the network, not the code.** `dataLayer` containing your event is not evidence it was sent. Look for a `/g/collect` request carrying the event name.
- **Reports lag; Realtime and DebugView do not.** Newly registered dimensions take 24–48 h to appear in standard reports, so same-day verification happens in Realtime/DebugView or at the network layer.

## Operations (run individually)

| # | Operation | When |
|---|---|---|
| 00 | [verify-destination-property](operations/00-verify-destination-property.md) | Always first. Does the measurement ID resolve to a property the user can open? |
| 01 | [create-property-and-stream](operations/01-create-property-and-stream.md) | When `00` finds no usable destination. |
| 02 | [resolve-tag-ownership](operations/02-resolve-tag-ownership.md) | When both page code and a GTM container configure GA4. |
| 03 | [design-event-schema](operations/03-design-event-schema.md) | Before writing code. Decide names and parameters. |
| 04 | [add-analytics-module](operations/04-add-analytics-module.md) | Create the single wrapper every call goes through. |
| 05 | [register-custom-definitions](operations/05-register-custom-definitions.md) | After `03`, **before** the events ship. |
| 06 | [instrument-pages](operations/06-instrument-pages.md) | Add events to components, including SPA route changes. |
| 07 | [verify-events-land](operations/07-verify-events-land.md) | After any change to events, tags, or IDs. |
| 08 | [filter-internal-traffic](operations/08-filter-internal-traffic.md) | Stop the user's own visits polluting the data. |
| 09 | [maintain-custom-definitions](operations/09-maintain-custom-definitions.md) | Rename or re-describe a dimension as its meaning widens. |

## Workflows (operations in the necessary order)

- [instrument-a-web-app](workflows/instrument-a-web-app.md) — the full arc for an app with no useful tracking yet.
- [diagnose-missing-events](workflows/diagnose-missing-events.md) — events fire in the browser but nothing appears in GA4. Start here for "analytics isn't working".

## Working style

- **Prove the destination before building the pipe.** `00` costs two minutes and prevents the most expensive failure in this skill.
- **Register definitions before shipping events.** If code is already live and unregistered, say plainly that the history is unrecoverable rather than implying a filter or backfill can fix it.
- **Reuse registered parameters instead of inventing new ones.** A new parameter reads `(not set)` for all prior data and costs a slot. Widening the meaning of an existing one is usually better — then update its description (`09`).
- **Verify at the network layer, and say what you observed.** "`shot_result` appeared as its own `/g/collect` request with `tid=G-XXXXXXXXXX`" is evidence. "The code looks right" is not.
- **Never claim a fix you have not watched work.** If a step is pending propagation, say so and give the user the check to run later.
- **Confirm before publishing a container or activating a data filter.** Both change live behaviour; a data filter additionally discards data irreversibly.

## Output the user should get at the end

A short summary listing: the property and measurement ID events now reach; which events and parameters were added; which custom definitions were registered and which existing ones were reused; what was verified and how (network evidence, Realtime counts); anything still propagating with the check to run later; and anything deliberately left untracked and why.
