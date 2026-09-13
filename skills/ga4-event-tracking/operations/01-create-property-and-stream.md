# 01 — Create a GA4 property and web data stream

**Purpose:** Produce a destination the user owns, yielding a fresh `MEASUREMENT_ID` for the app to send to.

**Inputs:**
- `PROPERTY_NAME` — from the user
- `ACCOUNT_NAME` — which existing GA account holds it (from the user)
- `SITE_URL` — the site's canonical origin
- `REPORTING_TIMEZONE`, `CURRENCY` — see Decision

**Preconditions:**
- `00` concluded there is no usable destination, **and** the user explicitly asked for a new property.
- User has Editor or Administrator on the destination account.

## Decision

- **Which account?** Never guess. Offer the accounts found in `00`, and mention that mirroring the Tag Manager account naming keeps the two products legible side by side.
- **Reporting time zone.** This sets day boundaries for every report and is awkward to reason about later. If the user does not say, infer from evidence and state the inference — a repository's commit timestamps carry a UTC offset, which beats defaulting to whatever GA pre-selects. Confirm the inference in your summary.
- **Property name.** Reuse the name the user already uses elsewhere for the site rather than inventing one.

## Steps

1. Admin → **Create** → **Property**.
2. Enter `PROPERTY_NAME`. Set the reporting time zone and currency. Continue.
3. Business details: pick the closest industry category and size. These only affect benchmarking suggestions; do not over-think them.
4. Business objectives: choose the one or two that match (for a content or game site, "Understand web and/or app traffic" and "View user engagement & retention"). Changeable later.
5. Click **Create**. Accept the terms only if the user asked for a property — their instruction is the authorization.
6. On the data-collection step choose **Web**. Enter `SITE_URL` as a **bare host with no port** — `example.com`, not `localhost:5173`; the field rejects a port with *"Valid website URL is required"*. It is metadata only: GA never verifies it and accepts events from whatever origin actually sends them, so a development-only app can use its eventual production host. Add a stream name. Leave **Enhanced measurement** on unless the user objects; it supplies `page_view`, `scroll`, and outbound `click` without code.
7. Read the **Measurement ID** from the resulting panel — then confirm it on **Admin → Data streams → the stream**, where it is displayed as a labelled field rather than embedded in a code snippet.

## Verification

- The stream detail page shows the stream name, `SITE_URL`, and a `G-…` measurement ID.
- Re-read that ID from the labelled field, not from a screenshot of the snippet. A single wrong character produces a silent failure identical to the one `00` exists to catch.
- Record the property ID from the URL; later operations need it.

## Undo

Admin → Property details → **Move to trash**. Trashed properties purge after roughly 35 days and can be restored until then. A new property cannot inherit the old one's history.

## Failure modes / Notes

- **"Valid website URL is required"** means the URL carries a port, a path, or a scheme the field will not take. Strip it back to the bare host.
- **"No data received in past 48 hours"** on the stream page is expected until `07` succeeds, and lingers briefly afterwards. It is not a verification signal.
- **Enhanced measurement counts outbound link clicks automatically.** Worth telling the user if the site links anywhere sensitive — turning it off is a data-stream setting, not a code change.
- A new property starts empty. If the user believed they had history at the old ID, say explicitly that it is not recoverable.
