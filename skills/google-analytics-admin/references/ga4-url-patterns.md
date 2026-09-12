# GA4 and GTM URL patterns (stable SPA routes)

Placeholders: `A` = GA account ID, `P` = GA property ID, `GA` = GTM internal account number, `GC` = GTM internal container number. All GA routes are hash routes under `https://analytics.google.com/analytics/web/`.

## Google Analytics 4

| Purpose | Route |
|---|---|
| Home for a property | `#/p<P>/reports/intelligenthome` |
| Account admin (account picker context) | `#/a<A>/admin/account` |
| Account settings (rename, trash) | `#/a<A>/admin/account/settings` |
| Account access management | `#/a<A>/admin/account/users` |
| Account trash can | `#/a<A>/admin/account/trash` |
| Property details | `#/a<A>p<P>/admin/property/settings` |
| **Move property** | `#/a<A>p<P>/admin/property/move` |
| Data streams (measurement IDs) | `#/a<A>p<P>/admin/streams/table` |
| Property access management | `#/a<A>p<P>/admin/property/users` |
| Product links | `#/a<A>p<P>/admin/property/links` |
| Property change history | `#/a<A>p<P>/admin/property/changehistory` |

Observed link shapes in the account picker:

- Property option: `#/a<A>p<P>/reports/intelligenthome` → parse both IDs from the `a…p…` segment.
- Empty account: single link `#/a<A>p0/admin`.

## Google Tag Manager (`https://tagmanager.google.com/`)

| Purpose | Route |
|---|---|
| All accounts/containers | `#/home` |
| Container workspace | `#/container/accounts/<GA>/containers/<GC>/workspaces/<W>` |
| Container admin overview | `#/admin/accounts/<GA>/containers/<GC>` |
| Container settings | `#/admin/accounts/<GA>/containers/<GC>/settings` |
| Export container | `#/admin/accounts/<GA>/containers/<GC>/export` |
| Import container | `#/admin/accounts/<GA>/containers/<GC>/import` |
| Account settings | `#/admin/accounts/<GA>/settings` |

## UI notes that matter for automation

- The GA header's account/property picker is exposed to accessibility tools as button **"Open the universal picker."** with two listboxes: **"Analytics Accounts"** and **"Properties & Apps"**. Read them as a tree; the picker's visual layout clips badly in narrow panes.
- Trashed accounts/properties render with strikethrough; the a11y tree shows them as ordinary options, so check the visual or the trash page if status matters.
- The Admin left sidebar overlays the content in narrow viewports. Collapse it via the chevron button at the bottom of the sidebar, then scroll the content pane left before clicking by coordinate — or click by element reference instead.
- After navigating to a new hash route, wait ~3 s before reading; the SPA renders asynchronously.
- The move dialog's success state is a modal headed **"Move request is pending"**.
- GTM's container ⋮ menu (top-right of "Edit container") contains only **Delete** — there is no move.
