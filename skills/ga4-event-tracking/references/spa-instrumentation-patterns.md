# SPA instrumentation patterns

Single-page apps break several assumptions that page-load analytics relies on. These are the patterns that survive contact with a router.

## Open / close pairs with dwell time

To measure how long a route or overlay was looked at, and where the visitor went next: emit `<thing>_open` on mount and `<thing>_close` on unmount, carrying `duration_sec` and an `exit` naming the destination.

Shape, framework-neutral:

```
on mount:
    openedAt = now
    closed   = false           # scoped to THIS mount, not a long-lived ref
    emit "<thing>_open"
    register beforeunload -> close("unload")

close(exit):
    if closed: return
    closed = true
    emit "<thing>_close" { duration_sec: round((now - openedAt)/1000), exit, source }

on unmount:
    unregister beforeunload
    close(exitRef)             # exitRef default "navigation"
```

## The two exits are disjoint — you need both

| Exit | Fires | Does **not** fire |
|---|---|---|
| Component unmount | in-app navigation, browser back | tab close, reload |
| `beforeunload` | tab close, reload, external navigation | in-app navigation |

Registering only one loses half the departures. Guard so the first to run wins.

**Do not call `preventDefault()`** in the `beforeunload` handler unless the page has genuinely unsaved state — it raises the browser's "Leave site?" prompt. Appropriate for a game in progress; gratuitous on a policy page that a search result drops people onto.

## The StrictMode latch trap

React StrictMode double-invokes mount effects in development: mount → cleanup → mount. If the "already closed" flag is a **ref**, it stays `true` through the simulated unmount and the real close never fires again — in development you see one spurious close and then silence forever.

Make the flag a plain local variable **inside** the effect so each run gets a fresh one. Refs are correct for values that must survive across the component's life (the pending `exit`); wrong for per-mount state.

Production builds do not double-invoke, so verify final counts against a production build rather than the dev server.

## Recording where the visitor went

Give each link an `onClick` that writes its destination into a ref before the router navigates; the unmount cleanup reads it. Default the ref to a generic `navigation` so browser-back and typed URLs still report something.

When several blocks of a page link to the same few routes, record **both** the destination and the block (`card` / `about` / `footer`). The pairing is what answers "which of these three link groups is doing the work" — the destination alone cannot.

## Events that can resolve twice

Where an outcome is reachable from two code paths — a timeout and a bounds check, an animation callback and a state watcher — the event can fire twice for one interaction while the app's own counter increments once. Set an "already reported" flag when the interaction *starts* and clear it on the next one, so the event count matches the counter.

## Clean up timers on unmount

An interval left running after navigation keeps mutating state and can emit a completion event for a route nobody is on. This is an analytics correctness problem, not only a leak: it manufactures sessions that never happened.

## Capturing state before it mutates

If resolving an action rewrites the state you want to report, capture the values first. Emitting a decision event at decision time and an outcome event at resolution time is usually cleaner than threading a snapshot through — and the decision event is the one that answers "what did people choose", which is generally the interesting question.

## Page views on route change

GA4's enhanced measurement fires `page_view` on History API changes, so SPA route changes are usually covered without code. If the app also updates `document.title` in an effect, the title recorded may be the previous route's — worth checking before adding manual `page_view` calls, which risks double-counting.
