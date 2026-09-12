# 00 — Verify the destination property exists and the user owns it

**Purpose:** Prove that the measurement ID already in the app resolves to a GA4 property the user can open, before any event work begins.

**Inputs:**
- `MEASUREMENT_ID` — the `G-…` value found in the app's HTML entry point, tag manager container, or framework config
- `CONTAINER_ID` — the `GTM-…` value, if the app also loads Tag Manager

**Preconditions:**
- User signed into the browser session (they sign in; never handle credentials).
- Read access to the app's source.

## Why this comes first

A measurement ID in source code is not evidence of a working destination. It may belong to a property that was deleted, one owned by a different account, or one copied from a tutorial. **Nothing fails visibly** — `gtag` accepts any well-formed ID, the requests return `2xx`, and the browser console stays clean. Skipping this step and building events on top of it is the most expensive mistake this skill exists to prevent.

## Steps

1. Find every analytics ID the app ships. Search the source for `gtag/js?id=`, `gtag('config'`, `dataLayer`, and `googletagmanager.com/gtm.js`. Record each `G-…` and `GTM-…` and the file it came from.
2. In the browser, open the GA4 property picker (Analytics home → the account/property selector in the header) and search for the site's name.
3. If nothing matches by name, enumerate: open the picker's account list and check each account's property list. Record which accounts hold zero properties — an empty account is a strong hint the property was deleted.
4. Open the candidate property's **Admin → Data streams → the web stream** and read the **Measurement ID** field. Compare it to `MEASUREMENT_ID`, character by character. Confusable pairs matter: `0`/`O`, `1`/`I`/`l`.
5. If the app also loads Tag Manager, check the container separately. Tag Manager and GA4 are different products with different permission lists — a user can own a container whose GA4 destination they cannot open. Open Tag Manager → the container → **Tags**, and read the measurement ID each tag targets.
6. Optional cross-check: in Tag Manager, the account-level **Google tags** list shows the `G-` IDs associated with that account. An ID absent from both the GA4 property list and this list is not the user's.

## Verification

Done when you can state one of:

- **Owned** — "`MEASUREMENT_ID` is the web stream of property `<PROPERTY_NAME>`, which the user can open." Proceed to `03`.
- **Not owned** — "`MEASUREMENT_ID` appears in no GA4 account and no Google tag list the user can see." Report this before doing anything else, then offer `01`.
- **Ambiguous** — the user may have a second Google account. Ask before concluding; check the account switcher for other signed-in identities.

## Undo

Read-only. Nothing to reverse.

## Failure modes / Notes

- **Deep links returning "Missing permissions."** GA4 admin URLs embed an account prefix that can change for the same property. A deep link that worked earlier in a session can start failing while access is perfectly fine. Re-select the property from the picker and use the URL the app itself produces. See [references/ga4-ui-notes.md](../references/ga4-ui-notes.md).
- **An ID that is genuinely dead.** Data sent to a deleted property is gone; it cannot be recovered or redirected. Say so plainly — the user may have assumed months of history exists.
- **Multiple IDs in one app.** A hard-coded snippet and a Tag Manager container can each carry a different ID. Record both; `02` decides which one survives.
