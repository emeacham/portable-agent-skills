# Google Tag Manager — consolidation limitations

**GTM has no "move container to another account" feature.** The container settings ⋮ menu offers only *Delete*. The supported way to get a container's configuration under a different account is:

1. **Export** the container (Admin → Export Container) as JSON.
2. **Create** a new container in the target account (same type: Web / iOS / Android / AMP / Server).
3. **Import** the JSON into the new container (Admin → Import Container → Overwrite into Default Workspace).
4. **Publish** the new container.
5. **Replace the container ID** in every site/app that loads it — the new container has a new `GTM-XXXXXXX` ID.
6. Once verified in production, delete the old container/account.

Consequences the user must accept before choosing this path:

- **Code changes** in every property that embeds the container (head `<script>` and body `<noscript>` snippets, or wherever the ID is configured).
- **Version history is not carried over**; the new container starts at version 1.
- **Container-level user permissions, environments, and custom domains (server containers)** must be recreated manually.
- **Consent-mode defaults / Google tag gateway settings** are container-level and must be re-checked.
- During the switch-over, a site may briefly run the old container ID (cached HTML). Keep the old container published until the new ID is confirmed live.

What does **not** require any of this:

- Moving GA4 **properties** between GA accounts (GTM tags reference `G-` measurement IDs, which don't change).
- Renaming a GTM account.
- Leaving containers where they are: a container in "Account A" serves a site just as well as one in "Account B". The only cost of not consolidating is an untidy account list.

Because of this asymmetry, the recommended default in a consolidation is **leave GTM as-is** unless the user specifically wants one GTM account and accepts the code change.
