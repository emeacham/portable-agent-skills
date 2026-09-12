# 04 — Add the analytics module

**Purpose:** Create the single module every analytics call goes through, so the tag is touched in exactly one place and a missing tag can never break the app.

**Inputs:**
- `MEASUREMENT_ID` (only if the page owns the ID — see `02`)
- The schema from `03`

**Preconditions:**
- `02` decided who owns the measurement ID.

## Steps

1. **Create one module** (for example `analytics.ts`) exporting a `track(name, params)` function. Nothing else in the app should call `gtag` or touch `dataLayer` directly; that is what makes the ownership question answerable later.
2. **Make every call best-effort.** Read the tag from the global scope, return early when it is absent, and wrap the whole body in `try`/`catch`. The tag is legitimately missing in unit tests, during a static build, and for anyone running a content blocker — none of which should throw out of a click handler.
3. **Read the global as `globalThis`, not `window`.** Identical in a browser, but it keeps the module importable where there is no DOM, so it can be unit-tested without a DOM environment.
4. **Strip `undefined` parameters** before sending, so an optional parameter is omitted rather than transmitted as the string `"undefined"`.
5. **Offer a bound helper** for a discriminator used on most events — a factory returning a `track` that merges a fixed parameter such as `{ game }`. Call sites stay short and the discriminator cannot be forgotten. Keep plain `track` exported too, for pages the discriminator does not describe.
6. **Add unit tests** for the contract that matters: a no-op when the tag is absent; the event and parameters forwarded when it is present; `undefined` parameters dropped; no throw when the tag itself throws.
7. **If the page owns the ID**, add the loader and `config` call to the HTML entry point, with a comment saying why the ID lives there rather than in the container. If the container owns it, keep only the `dataLayer` shim so calls queue.

## Verification

- Test suite passes, including a case asserting silence when the tag is missing.
- Type-check and build pass.
- Grep the codebase: `gtag(` and `dataLayer` appear only in the module and the HTML entry point.

## Undo

Delete the module and its tests; revert the entry-point snippet. No account-side effects.

## Failure modes / Notes

- **Do not make `track` throw or log loudly on a missing tag.** It will fire on every blocked pageview and train everyone to ignore the console.
- **Resist a queue-and-replay wrapper** that buffers events until the tag appears. It sounds robust and hides the ownership conflict in `02` — the events accumulate and are never sent, which is precisely the bug that is hardest to see.
- Keep the module free of route or component knowledge; it takes a name and a bag of parameters and nothing else.
