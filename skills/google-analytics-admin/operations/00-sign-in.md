# 00 — Sign in (user-driven)

**Purpose:** Get a browser tab that is signed into the user's Google account, without the agent ever touching credentials.

**Inputs:** none.

**Preconditions:** A browser capability the user can interact with (see `AGENTS.md` capability mapping).

## Steps

1. Open `https://analytics.google.com/analytics/web/` in the browser.
2. If the tab lands on `accounts.google.com`, tell the user: "Google's sign-in page is open in the browser — please sign in there, then tell me when you're in." Then **stop and wait**.
3. When the user says they're in, reload the GA URL and read the page text. Success looks like a page titled "Analytics | Home" (or "Analytics") with an account picker in the header.
4. If Google shows a 2-step verification or CAPTCHA, leave it to the user; never attempt it.

## Verification

- Page title contains "Analytics".
- The account picker button ("Open the universal picker" in the accessibility tree) is present.

## Undo

Nothing to undo. If the user wants to switch Google identities, ask them to do it in the browser's account menu.

## Notes

- Sessions persist in most in-app browsers; if the user was already signed in, step 2 is skipped.
- GTM (`https://tagmanager.google.com/`) shares the same Google session — no second login needed.
