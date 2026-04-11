# Proposal 033: Workflow Fan-Out and Temporal Orchestration

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/029-workflow-template-catalog.md`

## Status

Draft

## Date

2026-04-06

## Executive Summary

The current `Arca` workflow engine supports a single vertical slice: one ordered
sequence of steps, each targeting one provider, executed synchronously within one
workflow run.  This is not enough for `story-006`, which requires a buyer-side
orchestrator to solicit multiple providers in parallel, collect their responses
within a deadline, and select the best outcome.

This proposal introduces two orthogonal but composable primitives:

1. **Fan-out** — a workflow step that dispatches one request to multiple
   discovered targets simultaneously and waits for responses according to a
   configurable aggregation policy.
2. **Temporal orchestration** — step-level timeout, retry, and deadline
   declarations that give the host deterministic control over how long any
   part of a workflow may wait before escalating or failing.

Both primitives are expressed as declarative fields in `WorkflowDefinition` step
records; neither requires `Arca` to become a protocol authority or to acquire
signing or settlement responsibilities.

## Problem Statement

`story-006` has the following buyer-side lifecycle shape:

```
Buyer submits service-order
  → discover providers from Seed Directory / offer catalog
  → solicit N providers in parallel   ← fan-out
  → collect responses within deadline  ← temporal
  → select best offer                  ← fan-in / aggregation
  → open procurement contract          ← existing substrate
```

The current Arca engine can only express the last step.  The middle three are
entirely absent from the data model.  The gap is not algorithmic complexity — it
is missing *expressibility* in the workflow definition contract.

### What is absent today

| Need | Current state |
|---|---|
| Send to N targets at once | Not expressible — targets are always singular |
| Discover targets at runtime from catalog | Not expressible — targets are hardcoded |
| Wait for first/any/all/quorum responses | Not expressible |
| Timeout a waiting step | Not expressible |
| Retry a failed step with backoff | Not expressible |
| Deadline across the whole workflow run | Not expressible |

## Goals

- Make fan-out and temporal constraints expressible in `WorkflowDefinition`
  steps without breaking the existing sequential step format.
- Keep `Arca` a hosted workflow module: the host resolves targets, enforces
  deadlines, and controls dispatch; `Arca` proposes workflow intent.
- Preserve the existing single-target sequential path as the zero-config
  default — all new fields are optional.
- Define contracts precisely enough to implement without speculative
  over-engineering.

## Non-Goals

- Full workflow DSL or process algebra.
- Sub-workflow nesting or recursive fan-out (post-MVP).
- `Arca` acquiring signing or settlement authority.
- Replacing or modifying the existing procurement substrate.
- Multi-hop fan-out chains (max chain depth = 1 in MVP).

---

## Proposed Data Model

### 1. Fan-Out Target Descriptor

A step's `target` field is extended from a single participant reference to a
`FanOutTarget` descriptor.  When absent, the existing single-target behaviour
is preserved.

```json
"target": {
  "resolve": "capability",
  "capability_id": "offer-catalog",
  "filter": {
    "service_type": "text/summarise"
  },
  "limit": 8
}
```

Alternative form — static list (for testing or known-participant flows):

```json
"target": {
  "resolve": "static",
  "participants": [
    "participant:did:key:z6Mk...",
    "participant:did:key:z6Mk..."
  ]
}
```

Fields:

| Field | Type | Description |
|---|---|---|
| `resolve` | `"capability"` \| `"static"` | How targets are discovered |
| `capability_id` | String | Required when `resolve = "capability"`; queried against Seed Directory |
| `filter` | Object | Optional additional filter passed to catalog query |
| `limit` | u32 | Maximum number of targets to solicit (default: unbounded) |
| `participants` | [String] | Required when `resolve = "static"` |

When `resolve = "capability"`, the host resolves targets by querying the local
Seed Directory cache for participants holding a current, valid capability
passport for `capability_id`.  This resolution happens at step execution time,
not at workflow definition time.

### 2. Fan-In Policy

When `target` expands to more than one participant, the step needs a rule for
deciding when to proceed.

```json
"fan_in": {
  "policy": "any_one",
  "min_responses": 1
}
```

| `policy` | Meaning |
|---|---|
| `any_one` | Proceed as soon as one response arrives.  Default. |
| `all` | Proceed only when every dispatched target has responded. |
| `quorum` | Proceed when `min_responses` responses have arrived. |
| `best_of` | Collect all responses until deadline, then select by `score_field`. |

Additional fields:

| Field | Type | Description |
|---|---|---|
| `min_responses` | u32 | Required for `quorum`; minimum acceptable response count |
| `score_field` | String | Required for `best_of`; JSON path in response to sort by |
| `score_order` | `"asc"` \| `"desc"` | Sort direction for `best_of` (default: `"desc"`) |

### 3. Temporal Constraints

Temporal constraints are declared per-step as a `timing` object.

```json
"timing": {
  "timeout":      "PT30S",
  "retry": {
    "max_attempts": 3,
    "backoff":      "PT5S",
    "backoff_multiplier": 2.0
  },
  "on_timeout":   "skip"
}
```

| Field | Type | Description |
|---|---|---|
| `timeout` | ISO 8601 duration | Maximum wall-clock time to wait for this step to complete |
| `retry.max_attempts` | u32 | How many times to retry before giving up |
| `retry.backoff` | ISO 8601 duration | Initial wait between retries |
| `retry.backoff_multiplier` | f32 | Exponential multiplier (1.0 = constant, 2.0 = doubling) |
| `on_timeout` | `"fail"` \| `"skip"` \| `"abort_workflow"` | What to do when timeout expires without a result |

A workflow-level deadline can also be declared at the root:

```json
"deadline": "PT5M"
```

This is an absolute maximum duration for the entire workflow run from first step
to completion.  When elapsed, any pending steps are cancelled and the run is
marked `deadline_exceeded`.

### 4. Extended Step Record (full shape)

A step in `WorkflowDefinition.plan.steps` with the new optional fields:

```json
{
  "step_id":      "solicit-providers",
  "service_type": "text/summarise",
  "input":        { "text": "{{input.text}}" },
  "target": {
    "resolve":        "capability",
    "capability_id":  "offer-catalog",
    "filter":         { "service_type": "text/summarise" },
    "limit":          5
  },
  "fan_in": {
    "policy":         "any_one"
  },
  "timing": {
    "timeout":        "PT30S",
    "on_timeout":     "skip"
  }
}
```

Backward compatibility: when `target`, `fan_in`, and `timing` are all absent,
the step behaves exactly as it does today.

---

## Execution Model

Fan-out and temporal constraints are enforced by the **host** (the Node daemon),
not by `Arca`.  `Arca` proposes a `WorkflowDefinition`; the host executes it.

### Fan-out dispatch (host responsibilities)

1. Resolve `target` → produce list of `participant_id` values.
2. For each target, create a child dispatch record (see below) and send the
   step's service request via the existing peer session mechanism.
3. Collect responses into a `FanInBuffer` keyed by `(step_id, participant_id)`.
4. Apply `fan_in.policy` to decide when the step is done.
5. Cancel outstanding dispatches after `timing.timeout` or when policy is
   satisfied, whichever comes first.

### Dispatch tracking

The host maintains a `WorkflowStepDispatch` record per dispatched target:

```
WorkflowStepDispatch {
    dispatch_id:    String,       // "dispatch:<uuid>"
    run_id:         String,       // parent workflow run
    step_id:        String,
    target:         String,       // participant_id
    dispatched_at:  String,       // RFC 3339
    status:         Pending | Responded | Timeout | Cancelled,
    response:       Option<JsonValue>,
    responded_at:   Option<String>,
}
```

These records are appended to the commit log under
`state/workflow-dispatch/<dispatch_id>`.

### Temporal enforcement

The daemon runs a background tick (reusing the existing workflow eviction task
or alongside it) that:

1. Checks all `Pending` dispatches against their `timing.timeout`.
2. On timeout: updates dispatch status to `Timeout`, applies `on_timeout`
   policy to the parent step, triggers retry if configured.
3. Checks all active workflow runs against the run-level `deadline`.
4. On deadline exceeded: cancels all pending dispatches for the run, marks run
   `deadline_exceeded`.

### `Arca` contract

`Arca` sees only the completed step output (the selected fan-in result) —
it does not see the raw fan-out dispatches or intermediate responses.
The host produces one canonical `step_output` from the fan-in buffer and
presents it to `Arca` as if the step had a single response.

This preserves the existing `Arca` ↔ host interface contract.

---

## Workflow Run Status Extensions

Add two new terminal statuses to `WorkflowRunStatus`:

| Status | Meaning |
|---|---|
| `deadline_exceeded` | The run-level deadline was reached before all steps completed |
| `step_timeout` | A step timed out and `on_timeout = "fail"` or `"abort_workflow"` |

---

## Interaction With Existing Proposals

| Proposal | Relation |
|---|---|
| 021 — service-offers-orders | Fan-out is the dispatch mechanism for multi-provider solicitation defined there |
| 025 — seed-directory as capability catalog | `resolve = "capability"` queries the Seed Directory; no new discovery primitive needed |
| 029 — workflow template catalog | Templates may include `target`, `fan_in`, `timing` fields; no template changes required beyond accepting new fields |
| 032 — key delegation passports | Capability passport verification used during target resolution; orthogonal |

---

## Hard MVP Scope

The following is the minimum viable scope for the first implementation sprint:

| Feature | MVP |
|---|---|
| `target.resolve = "static"` | Yes |
| `target.resolve = "capability"` | Yes |
| `fan_in.policy = "any_one"` | Yes |
| `fan_in.policy = "all"` | Yes |
| `fan_in.policy = "quorum"` | Deferred |
| `fan_in.policy = "best_of"` | Yes |
| `timing.timeout` + `on_timeout` | Yes |
| `timing.retry` | Deferred |
| Run-level `deadline` | Yes |
| `WorkflowStepDispatch` commit log records | Yes |
| Background deadline enforcement tick | Yes |
| `Arca` sees only canonical fan-in output | Yes |

Deferred items are post-MVP and MUST NOT be implemented before the MVP scope is
clean and tested.

---

## Open Questions

1. **Fan-in output shape** — when `policy = "any_one"`, the step output is the
   first response.  When `policy = "all"`, should it be an array of responses or
   should the host pick one?  Proposed: `all` returns an array under a
   `responses` key; `Arca` is responsible for selecting from it.

2. **Dispatch cancellation on peer unavailability** — if a target is unreachable
   at dispatch time, should it count against `min_responses` for `quorum`?
   Proposed: unreachable targets are excluded from the denominator.

3. **Capability resolution caching** — should `resolve = "capability"` always
   re-query Seed Directory at step execution time, or is a short TTL cache
   acceptable?  Proposed: reuse the existing `DelegationCache`/`PassportCache`
   sync interval; no additional query at dispatch time.
