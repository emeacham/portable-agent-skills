# 08 — Filter the user's own traffic out

**Purpose:** Stop the user's development and testing visits from being counted, using GA4's two-part internal-traffic mechanism.

**Inputs:**
- `PUBLIC_IP` — the public IP of the machine to exclude. Determine it during the session and show it to the user; do not assume.

**Preconditions:**
- `07` passed — there is no point filtering a pipeline that is not delivering.
- User explicitly asked for the filter, having been told it is **not retroactive**.

## What this does and does not do

Two separate pieces, and it only works with both:

1. a **rule** on the data stream that stamps `traffic_type=internal` on matching requests, and
2. a **data filter** on the property that excludes events carrying that value.

It **cannot remove data already collected**. If the user's goal is to clean up existing test events, say plainly that this does not do that — a filter only affects future traffic.

## Decision

- **Confirm before activating.** GA4 itself warns that filter changes are "destructive and irreversible" — data excluded while the filter is Active is discarded, not hidden.
- **Match type.** Prefer an exact single address (`/32` in CIDR terms) over a wider range. A wider range risks excluding genuine visitors on neighbouring addresses; an exact match that goes stale merely stops filtering, which fails safe.

## Steps

1. Determine `PUBLIC_IP` for the machine to exclude, and check whether an IPv6 address is also in play. Tell the user the value you are about to use.
2. **Create the rule.** Admin → Data streams → the web stream → **Configure tag settings** → **Show more** → **Define internal traffic** → **Create**:
   - *Rule name* — something that will still mean something later, e.g. `Developer machine`.
   - *traffic_type value* — leave as `internal`.
   - *Match type* and *Value* — the exact address.
   Save.
3. **Activate the filter.** Admin → Data collection and modification → **Data filters**. GA4 ships a filter named *Internal Traffic* in **Testing** state. Open it, confirm its summary reads "Exclude events where the value of parameter traffic_type exactly matches internal", set **Filter state** to **Active**, Save, and accept the confirmation dialog.

## Verification

Not immediate — the rule must propagate into the cached tag config, which can take up to about an hour.

1. Load the site and read a `/g/collect` request. When the rule is live, requests carry **`tt=internal`**.
2. Then confirm exclusion: exercise an event name **not already present** in the property and check Realtime. It should not appear.
3. Until `tt=internal` shows up, report the filter as *configured, propagation pending*, and give the user the check to run later. Do not claim it is working.

## Undo

Set the filter's state back to **Inactive** to stop further exclusion. Data discarded while it was Active does not come back. The rule itself can be deleted from the data stream independently.

## Failure modes / Notes

- **Dynamic IP addresses.** Most residential connections rotate. When the address changes the filter silently stops matching and the user's visits are counted again — it fails safe, but tell them to re-check if the numbers ever look flatteringly good.
- **Shared addresses.** On carrier-grade NAT, an office, or a campus, the address may be shared with real visitors who would then be excluded. Ask if the connection type is not obviously a single household.
- **Your own verification traffic** is counted until the filter is live. Mention the handful of test events already in the property rather than leaving the user to find them.
