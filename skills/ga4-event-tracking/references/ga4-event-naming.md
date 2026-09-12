# GA4 event and parameter naming

## Recommended events worth reaching for

GA4 gives these built-in reporting treatment. Using one that genuinely fits puts the data in a standard report instead of only in explorations.

| Event | Typical parameters | Fits when |
|---|---|---|
| `level_start` | `level_name` | a session, round, or attempt begins |
| `level_end` | `level_name`, `success` | it finishes; `success` is a boolean you define |
| `post_score` | `score`, `level`, `character` | a final score exists for **one** player |
| `unlock_achievement` | `achievement_id` | a milestone is reached |
| `select_content` | `content_type`, `item_id` | a choice is made from a set |
| `share` | `method`, `content_type`, `item_id` | content is shared outward |
| `tutorial_begin` / `tutorial_complete` | — | instructional flow |
| `search` | `search_term` | site search |
| `sign_up`, `login` | `method` | account actions |

**Do not force a fit.** `post_score` on a two-sided game where the user controls both teams reports a number that means nothing. An honest custom name beats a misapplied recommended one — say why in the summary.

## Custom names

- `snake_case`, ≤40 characters.
- Describe what happened in the product's language (`play_call`, `manual_open`), not the implementation (`button_clicked_handler`).
- Reserved prefixes you cannot use: `ga_`, `google_`, `firebase_`. Reserved names include `session_start`, `first_visit`, `user_engagement`, `app_*`, `firebase_*`.

## Parameters

- `snake_case`, name ≤40 characters, value ≤100 characters.
- Up to 25 parameters per event.
- Values are strings or numbers. A small closed set of string values reports far better than free text — `make`/`miss`, not a sentence.
- Prefer reusing one parameter across areas (`result`, `source`, `exit`) over coining near-synonyms. One registered dimension answering three questions beats three slots that cannot be compared.

## Registration limits per property

| Thing | Standard property |
|---|---|
| Event-scoped custom dimensions | 50 |
| User-scoped custom dimensions | 25 |
| Item-scoped custom dimensions | 10 |
| Custom metrics | 50 |
| Calculated metrics | 5 |
| Distinct event names | 500 |

Dimensions and metrics are separate registries with separate budgets, so a parameter can be both.

## Dimension or metric?

- **Dimension** — you group or filter *by* it: `play_type`, `down`, `team`, `result`.
- **Metric** — you sum or average it: `yards`, `score`, `duration_sec`, `accuracy`.
- Numeric values can be either. `down` as a dimension gives "what do people call on 3rd down"; as a metric it would give a meaningless average down.
- Custom metrics require a **unit of measurement**: *Standard* for counts and scores, *Seconds* / *Milliseconds* / *Minutes* / *Hours* under Time, *Currency*, or a distance unit.

## Prebuilt dimensions — check before spending a slot

Several recommended-event parameters already exist as built-in dimensions in a property: `method`, `content_type`, `item_id`, `achievement_id`, `character`, `level_name`. Search the dimension picker in any exploration before registering one of these; if it is already there, registering costs a slot for nothing.
