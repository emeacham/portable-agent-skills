# GA4 and Tag Manager UI notes

Quirks that cost time if you meet them without warning. Complements the sibling skill's [browser-automation-notes](../../google-analytics-admin/references/browser-automation-notes.md).

## Deep links can fail with "Missing permissions"

GA4 admin URLs embed an account prefix and a property id. **The account prefix for the same property is not stable** — a deep link that worked earlier in a session can later return *"You do not have access to the account or property"* while access is entirely fine.

When this happens, do not conclude the user lost permission or that the property was deleted:

1. Re-select the property from the picker (search it by name).
2. Read the URL the application itself produces, and use that prefix from then on.

Worth telling the user if they have bookmarked GA4 URLs, since the same error will hit them.

## The property picker is the reliable navigation

Searching the picker by property name is more robust than constructing URLs. The picker also shows the owning account and the property id next to each result, which is the quickest way to confirm you are about to act on the right one.

## Narrow panes clip dialogs

GA4's admin dialogs are wide. In a narrow browser pane the **Save** button sits off the right edge and cannot be clicked.

- Collapse the admin sidebar (chevron at its bottom).
- Or scroll the page horizontally — scroll **inside the dialog's region**, not the background, which a modal locks.
- Prefer element references over pixel coordinates; the layout shifts when the pane resizes, and stale coordinates click the wrong thing.

After any pane resize, re-read positions before clicking. A batch of coordinate clicks written against an old screenshot will land somewhere unintended.

## Locked versus editable fields

On a custom dimension or metric, after the first save:

| Field | After save |
|---|---|
| Dimension / metric name | editable |
| Description | editable |
| Scope | **locked** (greyed, disabled) |
| Event parameter | **locked** (greyed, disabled) |
| Unit of measurement (metrics) | editable |

A wrong parameter name therefore means archive and re-create, spending another slot. Read the parameter back before saving.

## Reading values back

List views truncate descriptions with an ellipsis. To confirm what was actually stored, re-open the edit dialog and read the field value, rather than trusting the row text or a screenshot.

## Custom metrics require a unit

The unit of measurement has **no default** and Save stays disabled until one is chosen. If a save appears to do nothing, check the unit first.

## Timing after a dropdown selection

Clicking Save immediately after choosing a dropdown value can be dropped — the form has not committed the selection. Allow a beat between the two, and re-read the list after each save instead of assuming a batch of clicks all landed.

## Tag Manager: workspace changes are staged

Editing, deleting, or pausing a tag changes only the **workspace**. Nothing is live until **Submit → Publish**, which creates a version. This makes edits safe to stage and review — and makes it easy to believe a change took effect when it has not.

To reverse a published change, publish a further version, or re-publish an earlier one from the **Versions** screen.

## Tag Manager: deleting a tag leaves its trigger

Triggers are independent objects. Removing a tag leaves any trigger it used in place, firing nothing. Harmless, but it accumulates — remove it in the same change if nothing else references it.
