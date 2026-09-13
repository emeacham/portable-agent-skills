# 07 — Verify events actually land

**Purpose:** Establish, with evidence, that the app's events reach the intended property — not that the code looks correct.

**Inputs:**
- `MEASUREMENT_ID`
- The list of event names expected from the paths you are about to exercise

**Preconditions:**
- The app is running somewhere you can drive (dev server or deployed site).
- A capability to read the page's network activity or run JavaScript in it.
- If any instrumented path ends in an animation, the page must be **visibly on screen** — see the `requestAnimationFrame` note under *Failure modes*.

## Why code review is not verification

Every silent failure in this skill produces correct-looking code and a correct-looking `dataLayer`. The only evidence that distinguishes working from broken is a network request leaving the browser with your event name on it.

## Steps

1. Load the app and confirm **which analytics scripts loaded**. List script `src` values containing `gtag/js` or `gtm.js`. Exactly one `gtag/js?id=MEASUREMENT_ID` is expected; two means the `02` conflict is live. A Tag Manager-injected one carries extra query parameters (`cx=`, `gtm=`).
2. Exercise an instrumented path in the UI.
3. **Read the `/g/collect` requests.** Extract each request's `en` (event name) and `tid` (measurement ID) query parameters. Requests without an `en` are batched — several events in the POST body — and are expected alongside the individual ones.
4. Confirm your event names appear and every `tid` equals `MEASUREMENT_ID`.
5. **Cross-check in GA4 Realtime** (property → Reports → Realtime): the *Event count by Event name* card should list your events within a minute or two. Pick an event name that has **never** appeared in this property before as the decisive check — it cannot be confused with earlier traffic.
6. If Realtime shows nothing while the network shows requests, check whether an internal-traffic filter is already excluding you (`08`), and whether the requests carry `tt=internal`.

## Verification

Done when you can state all three:

- the expected event names appeared as `/g/collect` requests,
- every `tid` matched `MEASUREMENT_ID`,
- Realtime counted at least one event name that is new to the property.

If any is unmet, do not report success. Name which one failed.

## Undo

Read-only, except that events sent during verification are real data in the property. Say so; `08` prevents future test traffic but does not remove what has already arrived.

## Failure modes / Notes

- **Events in `dataLayer`, no `/g/collect`.** The `02` ownership conflict. Confirm by checking for two `gtag/js` loads of the same ID. See [references/gtag-vs-gtm-ownership.md](../references/gtag-vs-gtm-ownership.md).
- **Stale Tag Manager container.** `gtm.js` caches for roughly 15 minutes, partitioned per site, so a just-published container change may not be live in your tab. Force a refetch and reload before concluding failure — technique in [references/verification-techniques.md](../references/verification-techniques.md).
- **A `beforeunload`-fired event** cannot be observed by reloading, because the page is gone. Dispatch the event manually on `window` to exercise the listener without leaving.
- **A hidden page freezes `requestAnimationFrame`, and with it every event fired at the end of an animation.** Browsers stop rAF callbacks while `document.hidden` is true — a background tab, a minimised window, or an automation/preview pane that is not on screen. Timers are *not* stopped, so clocks, countdowns and progress text keep updating and the page looks perfectly alive. The resulting event stream is the misleading part: click-handler events (`select_content`, `level_start`, `play_call`) arrive normally, while events that fire when an animation resolves (`shot_result`, `play_result`, `level_end`) never do. That reads exactly like instrumentation missing its end-of-interaction hooks.
  - **The page goes dead, not slow.** An "in flight" or "is animating" latch never clears, so every later click silently early-returns and controls stay disabled. Easy to misdiagnose as a broken button.
  - **Frozen animations resolve later, out of order.** When the page becomes visible again the stalled animation finishes and emits its event *then* — possibly after a newer interaction's event, producing an apparent orphan: a result with no matching call before it. Neither a leak nor a duplicate; just a thawed animation.
  - **Check this before diagnosing anything else.** Read `document.hidden`, and count rAF callbacks over one second: tens on a healthy page, zero on a hidden one. Give that probe a timeout — on a fully hidden page it never resolves and your tooling hangs. Then make the page genuinely visible and re-exercise the path.
- **Development framework modes double-fire mount effects.** Verify final counts against a production build.
- **Custom dimensions may not work yet.** The documented wait is 24–48 h, though they often appear sooner. Either way their absence from reports is not a failure of this operation — this operation is about delivery, not reportability.
