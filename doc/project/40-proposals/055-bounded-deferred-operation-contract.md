# Proposal 055: Bounded Deferred Operation Contract

Based on:

- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`

## Status

Draft

## Date

2026-05-05

## Executive Summary

Orbiplex has several bounded invocation surfaces where the callee is expected to
return a result quickly: Sensorium directives, Sensorium OS actions, JSON-e
transforms, JSON-e Flow host-capability dispatch, and similar host-to-module
calls.

That default should remain intact. A synchronous host call MUST NOT silently
become a long-running process, watcher, stream, or unbounded model job.

This proposal adds a separate extension: a **bounded deferred operation
contract**. A module may quickly return `deferred` with an `operation_id`, a
`retry_after_seconds` hint, and an expiry/deadline. The host then polls a status
capability or status endpoint under host-owned retry, deadline, and cancellation
policy.

The core invariant is:

```text
The initial invocation remains bounded.
Long work is represented by a bounded deferred operation handle.
The host owns retry cadence, expiry, cancellation, and final timeout policy.
```

This gives Orbiplex a microservice-style "try again later" path without
breaking the existing sync contract.

## Context and Problem Statement

Proposal 045 defines Sensorium as a local enaction stratum: actions are finite,
timeout-governed, and must linearize any internal asynchrony into one bounded
result. This prevents connector calls from becoming hidden daemons or open-ended
blocking requests.

That invariant is correct, but some useful operations are longer than one normal
request budget:

- local model-assisted redaction or paraphrase,
- slow hardware or OS sampling,
- expensive validation over a large local dataset,
- connector calls that need to enqueue work into a separately supervised worker,
- remote calls where the caller should not block a host thread while waiting.

The wrong fix would be to let normal Sensorium or JSON-e calls block longer. That
would blur the boundary between request/response invocation and process
orchestration.

The better fix is a distinct deferred mode. The callee quickly acknowledges that
work has been accepted and returns a durable or semi-durable handle. The host
then polls, cancels, or expires the operation through explicit policy.

The key design constraint is that `deferred` must not become a domain value that
flows through every downstream component. It is a runtime control outcome. The
owning runtime captures a continuation context, pauses the branch, polls or waits
under host policy, and resumes the flow with a completed value or terminal
failure.

## Goals

- Preserve fast bounded sync invocation as the default.
- Add an explicit, bounded way to represent longer work.
- Make retry cadence, max lifetime, and cancellation host-owned.
- Allow Sensorium OS and other connectors to return `202 Accepted`-like
  semantics without keeping host requests open.
- Allow schedulers or lighter pollers to drive status checks.
- Keep deferred work observable by operators.
- Keep JSON-e and JSON-e Flow deterministic at their own boundary: they may
  receive a deferred result and pass it upward, but they should not hide an
  unbounded wait inside a pure-looking transform.

## Non-Goals

- This proposal does not make every action asynchronous.
- This proposal does not change the default Sensorium directive invariant.
- This proposal does not require the general replay scheduler for every deferred
  check.
- This proposal does not define a distributed job queue.
- This proposal does not allow connectors to defer forever.
- This proposal does not make Sensorium OS a long-lived worker supervisor.
  Long-lived workers remain separately supervised middleware or external
  services.

## Proposed Model / Decision

### 1. Default Sync Contract Remains the Default

Every existing bounded call remains synchronous unless the caller explicitly opts
into deferred mode or the capability profile declares that deferred outcomes are
allowed.

The default rule is:

```text
sync invoke -> completed | failed
```

A connector MUST NOT return a deferred handle from a capability whose profile is
sync-only.

### 2. Deferred Mode Is Explicit

A call may request or allow deferred mode through either a capability/profile
split or an input field.

Two acceptable shapes:

```text
sensorium.directive.invoke@sync
sensorium.directive.invoke@deferred
```

or:

```json
{
  "execution_mode": "sync"
}
```

```json
{
  "execution_mode": "deferred"
}
```

For v1, the simpler wire shape is to keep one capability and include an explicit
`execution_mode`, while capability/readiness policy states whether the caller may
use deferred mode.

### 3. Deferred Initial Response

A deferred initial response should map to HTTP `202 Accepted` when carried over
HTTP. The machine-readable payload is authoritative; HTTP status codes are only
transport hints.

Canonical payload shape:

```json
{
  "schema": "deferred-operation.v1",
  "status": "deferred",
  "operation_id": "operation:sensorium:sha256:...",
  "retry_after_seconds": 5,
  "created_at": "2026-05-05T18:00:00Z",
  "expires_at": "2026-05-05T18:05:00Z",
  "status_capability": "sensorium.directive.status",
  "cancel_capability": "sensorium.directive.cancel",
  "correlation_id": "run:...",
  "diagnostics": []
}
```

HTTP mapping:

- `202 Accepted` for accepted deferred work.
- `Retry-After` MAY mirror `retry_after_seconds`.
- `Location` MAY point to a host-local status URL when one exists.
- `429 Too Many Requests` with `Retry-After` remains rate limiting.
- `503 Service Unavailable` with `Retry-After` remains service overload or
  temporary unavailability, not a normal accepted job.

### 4. Status Poll Contract

The host checks status through a status capability or endpoint.

```text
host -> status(operation_id)
```

Canonical status response:

```json
{
  "schema": "deferred-operation-status.v1",
  "operation_id": "operation:sensorium:sha256:...",
  "status": "pending",
  "retry_after_seconds": 10,
  "expires_at": "2026-05-05T18:05:00Z",
  "attempt_no": 2,
  "diagnostics": []
}
```

Allowed statuses:

- `pending` — not ready yet; host may retry later.
- `completed` — final result is available in the response or by reference.
- `failed` — final failure, not retryable unless the payload says otherwise.
- `expired` — operation exceeded its own lifetime.
- `canceled` — host or operator canceled the operation.
- `unknown` — the connector no longer recognizes the operation id; host treats
  this as terminal unless policy says otherwise.

Completed response example:

```json
{
  "schema": "deferred-operation-status.v1",
  "operation_id": "operation:sensorium:sha256:...",
  "status": "completed",
  "completed_at": "2026-05-05T18:01:12Z",
  "result": {
    "schema": "sensorium-directive-result.v1",
    "status": "completed",
    "result": {
      "json": {
        "redacted_text": "..."
      }
    }
  },
  "diagnostics": []
}
```

### 5. Host-Owned Polling Policy

The host MUST clamp every connector-provided hint.

Host policy owns:

- minimum retry interval,
- maximum retry interval,
- maximum total operation lifetime,
- maximum attempts,
- maximum response bytes,
- cancellation policy,
- operator-visible diagnostics,
- persistence or volatility of operation state.

Connector hints are advisory:

```text
effective_retry_after = clamp(connector_retry_after, host_min, host_max)
effective_expires_at = min(connector_expires_at, host_deadline)
```

A connector cannot keep work alive indefinitely by returning larger
`retry_after_seconds` values.

### 6. Poller vs Scheduler

The general scheduler MAY drive deferred polls, but the contract should not
require it.

A host may implement a lightweight `DeferredOperationPoller` with the same
policy semantics when the general scheduler is too heavy for a short operation.

Layer boundary:

```text
deferred operation contract = semantic state machine
scheduler / poller          = execution mechanism
workflow / JSON-e Flow      = consumer of final outcome
connector                   = owner of the concrete long work
```

### 6.1 Deferred Is a Control Outcome, Not Domain Data

Downstream components MUST NOT receive `deferred` as ordinary input unless they
explicitly declare a deferred-aware control-plane role.

Preferred control flow:

```text
component A calls deferred-capable capability
  <- deferred(operation_id)
runtime captures continuation context
runtime stops this branch
runtime polls/status-checks later
runtime resumes from the recorded point with completed(result)
component B receives completed(result), not deferred(...)
```

This keeps the data plane clean. Domain components process domain values. The
runtime plane owns waiting, polling, retry, expiry, cancellation, and resume.

### 6.2 Continuation Context Is a Serializable Value

The continuation is not a captured language stack. It is explicit data.

Candidate shape:

```json
{
  "schema": "orbiplex-continuation.v1",
  "continuation_id": "continuation:...",
  "workflow_run_id": "run:...",
  "step_id": "call_sensorium_directive",
  "deferred_operation_id": "operation:sensorium:sha256:...",
  "resume_kind": "json_e_flow_step",
  "resume_point": {
    "executor_id": "json_e_flow",
    "template_id": "template:...",
    "step_index": 3,
    "step_id": "call_sensorium_directive",
    "output_binding": "sensorium_result"
  },
  "caller": {
    "module_id": "story009.json-e-flow.roles"
  },
  "capability_id": "sensorium.directive.invoke",
  "context": {},
  "envelope": null,
  "trace": {
    "correlation_id": "run:..."
  },
  "idempotency_key": "idem:...",
  "deadline_at": "2026-05-05T18:05:00Z",
  "attempts": 1
}
```

The exact schema may evolve, but the invariant is stable:

```text
Continuation context is a value, not a captured stack.
Only the runtime that owns the interpreter may consume the continuation.
```

Allowed contents:

- schema and version,
- continuation id,
- workflow/run/step ids,
- owning component/module id,
- deferred operation id,
- resume kind and resume point,
- caller/capability snapshot,
- current context or input JSON,
- optional envelope snapshot,
- trace/correlation ids,
- idempotency key,
- deadline/retry policy snapshot,
- attempt counters and last diagnostic.

Forbidden contents:

- stack frames,
- closures/functions,
- thread handles,
- sockets,
- locks,
- open files,
- process handles,
- borrowed memory references.

### 6.3 Resume Strategy

The target architecture is continuation-resume, not broad abort-and-retry.

For JSON-e Flow:

```text
step call_sensorium_directive
  -> deferred(operation_id)

persist continuation:
  template_id
  step_index
  current_context_json
  output_binding = "sensorium_result"
  operation_id
  trace_id
  deadline
  idempotency_key

resume:
  poll operation_id
  completed(result)
  bind context["sensorium_result"] = result
  continue from step_index + 1
```

Abort-and-reschedule-step is acceptable only as a fallback for strictly
idempotent steps. It retries more work than necessary and is harder to reason
about when side effects exist.

### 7. Sensorium OS Application

Sensorium OS actions remain finite, timeout-governed command invocations.

Deferred mode means the initial Sensorium OS action quickly starts or checks a
separately managed operation and returns a handle. It does not mean Sensorium OS
keeps the host request open.

Valid pattern:

```text
sensorium-os action start
  -> start local model job / OS job / external request
  -> persist operation handle in connector-owned state
  -> return deferred operation_id

host later polls
  -> sensorium-os action status(operation_id)
  -> pending | completed | failed | expired
```

Invalid pattern:

```text
sensorium-os action invoke
  -> block for minutes while model or watcher runs
  -> hold host request/thread open
```

### 8. JSON-e and JSON-e Flow Application

JSON-e transforms should stay pure and bounded. They may shape a deferred
operation request or response, but they should not hide polling inside a
transform.

JSON-e Flow may call a deferred-capable host capability and receive `deferred` as
an explicit control outcome. A workflow engine should then persist a
continuation, suspend that branch, schedule or poll later, and resume the step
with the completed value.

It should not busy-wait inside one JSON-e Flow execution.

### 9. Operator Visibility

Deferred operations should be visible to operators when they outlive one normal
request.

Minimal operator view:

- operation id,
- owning module/capability,
- created at,
- expires at,
- next retry at,
- attempts,
- current status,
- last diagnostic,
- cancel/retry action when allowed.

This may live in a generic host view and/or in a domain-specific middleware UI.

## Data Contracts

This proposal introduces two candidate schemas:

- `deferred-operation.v1` — initial accepted deferred response,
- `deferred-operation-status.v1` — status poll response.

Field naming should follow existing Orbiplex JSON style. The schema should use
explicit enums for status and should leave diagnostic objects open enough for
connector-specific details.

Required initial fields:

- `schema`,
- `status`,
- `operation_id`,
- `retry_after_seconds`,
- `created_at`,
- `expires_at`,
- `status_capability` or `status_href`.

Recommended fields:

- `cancel_capability` or `cancel_href`,
- `correlation_id`,
- `owner_module_id`,
- `capability_id`,
- `diagnostics`.

## Invariants

- Initial invoke returns quickly.
- Deferred operation ids are stable and idempotent for the accepted work.
- The final result is idempotent for `operation_id`.
- Host clamps retry cadence and operation lifetime.
- Connector cannot extend the operation beyond host policy.
- Sync-only capability profiles cannot return deferred status.
- Deferred operations are cancelable or explicitly non-cancelable.
- Operator diagnostics must not leak raw private payloads by default.
- Long-lived workers remain behind a supervised middleware/service boundary.

## Trade-offs

### Benefits

- Preserves the simple sync contract for normal actions.
- Supports longer local model or OS work without blocking host requests.
- Gives operators explicit visibility into pending work.
- Allows JSON-e Flow and Sensorium OS to compose with longer work without
  becoming hidden schedulers.
- Keeps retry/backoff policy local and auditable.

### Costs

- Adds one more state machine to host/runtime code.
- Requires persistence or careful volatile-state semantics for operation handles.
- Requires UI/diagnostics work to avoid opaque pending jobs.
- Requires clear capability profiles so sync-only callers do not accidentally get
  deferred outcomes.

## Failure Modes and Mitigations

### Infinite Deferral

A connector may keep returning `pending`.

Mitigation: host-owned `expires_at`, max attempts, and max lifetime are terminal.

### Retry Storm

Many pending operations may all request short retry intervals.

Mitigation: host clamps minimum interval, applies per-module concurrency limits,
and may jitter retry times.

### Lost Operation State

A connector restart may lose the operation id.

Mitigation: `unknown` is terminal by default unless the caller explicitly allows
restart recovery. Critical deferred operations should persist connector-owned
state.

### Private Data Leakage

Diagnostics or status payloads may expose raw private material.

Mitigation: status payloads carry summaries and references by default; raw data
stays in local/private storage with separate capability gates.

### Hidden Long-Running Work in JSON-e

A JSON-e helper could block inside a heavy function.

Mitigation: JSON-e execution budgets remain in force. Deferred work must cross an
explicit host capability boundary.

### Scheduler Coupling

A lightweight deferred action could be forced through the full scheduler.

Mitigation: define the state machine independently from the execution mechanism;
use the scheduler only when useful.

## Concrete Scenario: Whisper Redaction

A user submits raw private text to `whisper-intake`.

```text
whisper-intake
  -> stores raw/private material locally
  -> seals raw/private material to personal Memarium
  -> calls whisper.redaction.prepare with execution_mode = deferred
```

The provider is JSON-e Flow backed by a Sensorium OS action.

```text
JSON-e Flow
  -> sensorium.directive.invoke
  <- deferred(operation_id, retry_after_seconds = 5)
```

The host records the deferred operation and polls later.

```text
host poller
  -> sensorium.directive.status(operation_id)
  <- completed(redaction draft)
```

`whisper-intake` stores the draft. The operator reviews and approves it before a
public/federated `whisper-signal.v1` candidate can be published.

## Open Questions

1. Should the v1 status path be capability-shaped (`sensorium.directive.status`)
   or URL-shaped (`status_href`) by default?
2. Should host deferred operation state be durable across daemon restarts in v1,
   or may v1 treat restart as terminal `unknown` for connector-owned operations?
3. Should `cancel_capability` be required for every deferred operation, or should
   non-cancelable operations be allowed with an explicit reason?
4. Should JSON-e Flow gain first-class `awaiting_deferred_operation` step status,
   or should it return a generic awaiting outcome to its caller?
5. What is the default maximum deferred operation lifetime for Sensorium OS
   actions: seconds, minutes, or profile-specific only?

## Next Actions

1. Add JSON Schemas for `deferred-operation.v1` and
   `deferred-operation-status.v1`.
2. Add a minimal host-side deferred operation classifier and policy clamp helper.
3. Add Sensorium OS reference support for one deferred action pair:
   `start` + `status`.
4. Add JSON-e Flow handling for explicit deferred step outcomes without
   busy-waiting.
5. Add operator visibility for pending/expired deferred operations.
6. Use `whisper.redaction.prepare` as the first practical consumer once its
   provider contract is implemented.

## Tracking

| ID | Work item | Status | Notes |
|---|---|---|---|
| P055-01 | Define `deferred-operation.v1` schema | todo | Initial accepted response. |
| P055-02 | Define `deferred-operation-status.v1` schema | todo | Status poll response. |
| P055-03 | Host policy clamp helper | todo | Min/max retry, max lifetime, max attempts. |
| P055-04 | Sensorium OS reference deferred action | todo | Start/status pair, no open host request. |
| P055-05 | JSON-e Flow deferred step status | todo | No busy-wait inside one execution. |
| P055-06 | Operator visibility | todo | Pending/expired/cancel/retry state. |
| P055-07 | Whisper redaction provider integration | todo | First practical consumer through `whisper.redaction.prepare`. |
