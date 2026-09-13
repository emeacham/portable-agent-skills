# 08 — Filter the user's own traffic out

**Purpose:** Stop the user's development and testing visits from being counted, without the filter quietly lapsing the next time their IP address changes.

**Inputs:**
- `MEASUREMENT_ID` and the app's HTML entry point (for the flag, below)
- `PUBLIC_IP` — only if an IP rule is also wanted. Determine it during the session and show it to the user; do not assume.

**Preconditions:**
- `07` passed — there is no point filtering a pipeline that is not delivering.
- User explicitly asked for the filter, having been told it is **not retroactive**.

## What this does and does not do

GA4's *Internal Traffic* data filter excludes any event whose `traffic_type` parameter equals `internal`. The filter is one half; something has to **set that parameter**. There are two ways, and they are not equally good:

| Setting `traffic_type` | Survives an IP change? |
|---|---|
| An **IP rule** on the data stream | **No** — stops matching silently |
| A **flag in the page** that sets it on the gtag config | **Yes** — the address is irrelevant |

It **cannot remove data already collected**. If the user's goal is to clean up existing test events, say plainly that this does not do that.

## Decision

- **Which mechanism?** Recommend the page flag; add the IP rule only as a backstop for browsers that were never flagged. On a static residential connection an IP rule alone is tolerable; on anything dynamic it is a filter that will lapse without telling anyone.
- **Do not widen the CIDR range to cope with rotation.** A `/24` is 256 addresses and a `/16` is 65,536; every real visitor in the block is then excluded. That trades a failure that *inflates* the numbers for one that *hides real users* — harder to notice and harder to undo. Prefer `/32` plus the flag.
- **Confirm before activating the filter.** GA4 warns that filter changes are "destructive and irreversible": data excluded while it is Active is discarded, not hidden.

## Steps

### A. The page flag (the part that actually lasts)

1. In the HTML entry point, **before** the `gtag('config', …)` call, compute whether this browser is internal:
   - read a query parameter (`?internal=1` sets a `localStorage` key, `?internal=0` removes it),
   - treat `localhost` / `127.0.0.1` as always internal, so development traffic never counts,
   - wrap the whole thing in `try`/`catch` — `localStorage` **throws outright** in some privacy modes, and analytics must never break the page.
2. Pass the result into the config: `gtag('config', MEASUREMENT_ID, internal ? { traffic_type: 'internal' } : {})`. Config-level rather than per-event, so it applies to everything the page sends.
3. Tell the user the flag is **per browser**: one visit to `/?internal=1` on each device or browser they test from.

### B. The IP rule (optional backstop)

4. Admin → Data streams → the web stream → **Configure tag settings** → **Show more** → **Define internal traffic** → **Create**:
   - *Rule name* — something that will still mean something later.
   - *traffic_type value* — leave as `internal`.
   - *Match type* and *Value* — the exact address (`/32`).

### C. Activate the filter (required either way)

5. Admin → Data collection and modification → **Data filters**. GA4 ships a filter named *Internal Traffic* in **Testing** state. Open it, confirm its summary reads "Exclude events where the value of parameter `traffic_type` exactly matches `internal`", set **Filter state** to **Active**, Save, accept the confirmation.

## Verification

**If an IP rule is already matching you, `tt=internal` proves nothing** — it would appear whether or not the flag works. To isolate the flag, temporarily set it to a distinctive value the rule could never produce:

1. Change the config to send `traffic_type: 'internal_probe'`, load the page, and read a `/g/collect` request.
2. Seeing **`tt=internal_probe`** proves two things at once: the page-set parameter reaches the wire, and it **overrides** the IP-derived value — which is exactly what makes it survive a rotated address.
3. Revert to `internal` and confirm `tt=internal`.
4. Check the flag's storage behaviour directly: `?internal=1` sets the key, `?internal=0` clears it.
5. Verify on a **real hostname**, not just `localhost` — the localhost shortcut would mask a broken flag.

An IP rule on its own is not immediate: it must propagate into the cached tag config, up to about an hour. Until `tt=internal` appears, report it as *configured, propagation pending* and give the user the later check. Do not claim it is working.

## Undo

- Flag: `/?internal=0` per browser, or remove the block from the entry point.
- Filter: set its state to **Inactive**. Data discarded while it was Active does not come back.
- IP rule: delete it from the data stream independently.

## Failure modes / Notes

- **A rotated IP is silent and flattering.** With only an IP rule, the user's own visits quietly rejoin the real numbers — traffic looks better and nothing looks wrong. This is the reason the flag exists.
- **`?internal=1` is a public URL.** If it leaks and a real visitor follows it, they are excluded until they clear it. Nothing links to it and it is not in the sitemap, so the risk is small, but it is a genuine tradeoff against an IP rule, which has no URL surface.
- **Shared addresses.** On carrier-grade NAT, an office, or a campus, one address may cover real visitors. Another reason to prefer the flag.
- **Private browsing loses the flag.** `localStorage` is cleared or unavailable, so those sessions count. Say so rather than letting the user assume total coverage.
- **Your own verification traffic** is counted until the filter is live. Mention the test events already in the property rather than leaving the user to find them.
