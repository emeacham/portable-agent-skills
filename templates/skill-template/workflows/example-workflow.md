# Workflow — <Goal>

Use when the user says any of: "…", "…".

**Goal:** One sentence describing the end state.

## Inputs to establish up front

| Input | Source |
|---|---|
| … | user |

## Sequence

```
00 example-operation
 [Decision A: …]
 └─ NN next-operation
 └─ Final report
```

## Step detail

1. `00-example-operation` — anything the composition adds (batching, when to show a table).
2. …

## Guardrails specific to this workflow

- Never … without Decision A being an explicit yes.
