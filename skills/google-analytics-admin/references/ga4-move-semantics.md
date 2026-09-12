# GA4 property moves — what changes and what doesn't

| Thing | After "Move property" |
|---|---|
| Property ID (numeric) | **unchanged** |
| Data streams and `G-` measurement IDs | **unchanged** |
| Historical reporting data | moves with the property |
| Explorations, audiences, key events, custom definitions | move with the property |
| Product links (Google Ads, Search Console, BigQuery, Merchant Center) | move with the property; re-verify afterwards |
| Property-level user permissions | copied (if "keep") or replaced by destination's (if "replace") |
| Account-level users of the *source* | become property-level users on the moved property only when "keep" is chosen |
| Data-sharing settings | property inherits the **destination account's** settings (GA warns when they differ) |
| Terms of Service / DPA | destination account's terms apply (the confirm checkbox) |
| Site/app code (`gtag.js`, GTM tags referencing `G-`) | **no change required** |

Other facts:

- Moves are asynchronous. The UI says "Move request is pending"; most complete within a minute.
- A property in the **trash** cannot be moved. Restore it first (Admin → Account → Trash Can) or leave it to auto-purge.
- You need **Edit** on the source property and **Edit** (or Admin) on the destination account. If the destination is missing from the dropdown, that's why.
- There is no "merge accounts" action; an account is just a container of properties plus users and settings.
- Universal Analytics properties are gone; only GA4 properties exist in the UI.
- Moving a property does not move GTM containers — they are a different product with their own account hierarchy (see `gtm-limitations.md`).
