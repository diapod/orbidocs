# Proposal 055: Bounded Deferred Operation Contract

Based on:

- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`

Promoted to:

- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`

## Status

Implemented MVP

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
contract**. A module may quickly return `deferred` with an `operation/id`, a
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

The local-device-discovery continuation described below was added on
2026-10-13. Its versioned private progress and retention boundary are **planned**;
the implemented v1 MVP and its existing consumers keep their current semantics.

## Context and Problem Statement

Proposal 045 defines Sensorium as a local enaction stratum: actions are finite,
timeout-governed, and must linearize any internal asynchrony into one bounded
result. This prevents connector calls from becoming hidden daemons or open-ended
blocking requests.

That invariant is correct, but some useful operations are longer than one normal
request budget:

- local Inquirium/model-assisted redaction or paraphrase,
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
- Keep JSON-e and JSON-e Flow deterministic at their own boundary: a flow may
  suspend on a deferred control response, but deferred handles remain
  host-owned control-plane state rather than domain payload.

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

A call may request deferred mode through an input field:

```json
{
  "timing": {
    "mode": "sync"
  }
}
```

```json
{
  "timing": {
    "mode": "async"
  }
}
```

For v1, Sensorium keeps one capability (`sensorium.directive.invoke`) and uses
the directive timing mode. Whether that mode is allowed is declared by the
operator-signed action catalog entry, not by the caller alone.

Action catalog entries may declare:

```json
{
  "action_id": "story009.draft.compose",
  "execution_mode_support": "either",
  "deferred_profile": {
    "preferred_retry_after_seconds": 15,
    "preferred_max_ttl_seconds": 1800
  }
}
```

`execution_mode_support` is one of:

- `sync-only` — safe default. `timing.mode = "async"` is rejected before
  connector dispatch.
- `either` — caller may request either `sync` or `async`.
- `async-only` — `timing.mode = "sync"` is rejected before connector dispatch.

`deferred_profile` is a connector/action hint, not policy. The host still
computes the effective retry/expiry values through `DeferredHostPolicy`.

### 3. Deferred Initial Response

A deferred initial response should map to HTTP `202 Accepted` when carried over
HTTP. The machine-readable payload is authoritative; HTTP status codes are only
transport hints.

Canonical payload shape:

```json
{
  "schema": "deferred-operation.v1",
  "schema/v": 1,
  "status": "deferred",
  "operation/id": "deferred:sensorium.directive.invoke:...",
  "operation/kind": "sensorium.directive.invoke",
  "retry_after_seconds": 5,
  "created_at": "2026-05-05T18:00:00Z",
  "expires_at": "2026-05-05T18:05:00Z",
  "status_href": "/v1/deferred/...",
  "cancel_href": "/v1/deferred/.../cancel",
  "correlation/id": "run:...",
  "audit/outcome-ref": "outcome:...",
  "diagnostics": []
}
```

Exactly one cancellation surface MUST be present:

- `cancel_href` when the operation can still be cancelled through a host-owned
  control endpoint,
- `cancel/unavailable-reason` when the operation is explicitly not cancelable.

This keeps non-cancelable work visible without pretending that every transport
or side effect can be safely undone.

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
  "schema/v": 1,
  "operation/id": "deferred:sensorium.directive.invoke:...",
  "operation/kind": "sensorium.directive.invoke",
  "status": "pending",
  "retry_after_seconds": 10,
  "expires_at": "2026-05-05T18:05:00Z",
  "attempt_no": 2,
  "diagnostics": []
}
```

Allowed statuses:

- `pending` — not ready yet; host may retry later.
- `running` — connector has started work; host may retry later.
- `completed` — final result is available in the response or by reference.
- `failed` — final failure, not retryable unless the payload says otherwise.
- `timed-out` — connector work exceeded its configured or host-clamped timeout.
- `cancelled` — host or operator cancelled the operation.
- `expired` — host/runtime no longer accepts this operation because its
  deferred lifetime expired before a terminal result was produced.
- `unknown` — the connector no longer recognizes the operation id; host treats
  this as terminal unless policy says otherwise.

Completed response example:

```json
{
  "schema": "deferred-operation-status.v1",
  "schema/v": 1,
  "operation/id": "deferred:sensorium.directive.invoke:...",
  "operation/kind": "sensorium.directive.invoke",
  "status": "completed",
  "updated_at": "2026-05-05T18:01:12Z",
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

### 4.1 Planned Local Device Discovery Progress

The [P045 local device discovery continuation](045-sensorium-local-enaction-stratum.md#local-device-discovery-continuation)
needs incremental caller-visible candidates during one bounded operation. This
is a consumer of the shared status/poll/cancel mechanism, not a new streaming
channel or a new deferred lifecycle. The first BLE provider is owned by
[P096](096-sensorium-brainflow-connector.md); USB/serial and mDNS initially have
contract fixtures rather than qualified runtime providers.

The draft `deferred-operation-status.v2`, frozen on 2026-10-13, adds an optional, typed `progress`
field. It preserves the v1 lifecycle vocabulary and keeps a final domain result
separate from progress. The discovery progress variant must declare its type,
carry a monotonically increasing revision within the operation, and contain a
bounded snapshot validated against the frozen
`sensorium-device-discovery-candidate.v1` contract. Other domains must define
their own typed variants; `extensions` is not a stable substitute for this field.
Exact wire properties, schema bounds, and positive/negative vectors belong to
`P055-10` and the P045 profile contract.

For discovery, each revision replaces the previous snapshot. Candidate count,
encoded bytes, revision updates, operation lifetime, and candidate expiry are
bounded by the admitted profile and host policy. There is no append-only result
history. A `candidate/ref` is caller-private, bound to the operation and scope,
and conveys neither a durable binding nor acquisition consent. Providers filter
out-of-scope advertisements before sending data; the host revalidates the
remaining candidates. Neither rejected identifiers nor their counts become
progress or audit material.

Before discovery is exposed, the entire host-provider-console path must support
v2 schema validation, private progress, and the retention rules below. An
unsupported component causes admission refusal before provider I/O; the host
must not silently discard progress, reinterpret v2 as v1, or introduce a second
channel. Existing v1 consumers remain supported without changed meaning. The
initial accepted handle can remain `deferred-operation.v1`; status-version
support must be checked through admission rather than inferred from that handle.

#### Private Responses and Durable Metadata

**Pre-discovery implementation fact (2026-10-13):**
`node:daemon/src/deferred_registry.rs` passes the complete status payload from
`update_from_status_with_expected` to `append_event_locked`, which retains
`json_digest(payload)` in the status event history. Hiding candidates in an
operator response would therefore still retain a digest derived from the list.
That generic path does not establish the required discovery privacy boundary.
The 2026-10-14 isolated Node implementation adds a separate typed discovery
projection before this hash boundary; its device-free retention tests are
software evidence. Actual provider/console cancellation remains P055-11 work.

The planned host adapter must produce two explicit values before registry,
receipt, or audit handling:

| Projection | Contents and handling |
|---|---|
| Caller-private response | Current bounded candidate snapshot and revision, delivered only after exact caller identity and current action/scope authority are rechecked. Volatile operation-local storage; no retained snapshot history. |
| Durable status and audit metadata | Operation lifecycle, redacted admitted scope, times, outcome, and count of candidates actually disclosed. Registry history hashes this metadata projection only. |

Candidate bytes, references, transport identifiers, labels, and digests derived
from the private snapshot must be excluded from durable status, continuation
storage, diagnostics, status-event hashes, execution receipts, and audit records.
A deterministic hash or digest-only event is not redaction. Operation identifiers
and correlation metadata must not be derived from candidate identities either.
Retained scope metadata must also exclude private identity selectors and
transport addresses rather than copying the original request verbatim.
This planned policy narrows retention for discovery; existing v1 consumer
retention remains unchanged.

Every read, poll, cancellation request, and candidate consumption rechecks the
requesting principal and current authority for the operation and admitted scope.
Possession of an operation or candidate reference does not authorize access.
Revocation invalidates candidates immediately and triggers host-owned cleanup;
that cleanup must remain possible after the caller loses its grant. A host or
provider restart invalidates the candidate generation and erases its snapshot.
Durable operation metadata may report the interrupted lifecycle, but must not
reconstruct lists or automatically restart discovery. A new scan requires new
admission and a new bounded operation.

#### Completion and Cancellation

The P045 discovery domain result distinguishes completion of the admitted
observation window from `limit-reached` and `deadline-reached`; the latter two
are explicitly partial results. These reasons are separate from provider
failure, refusal, and a host `timed-out` lifecycle. A domain deadline can produce
a completed partial result only when the provider returns a valid result and
the host verifies discovery termination before the operation's host deadline.
An empty result only states that no matching devices were observed within that
scope and window.

Cancellation means confirmed termination of this operation's discovery session,
not disabling a shared controller. Confirmation requires a backend acknowledgement
or a qualified proof that terminating the worker releases that session. Until
then the host blocks candidate delivery and consumption and retains the transport
claim. Uncertain cleanup must not be reported as successful `cancelled`, nor
release the claim for acquisition or a new scan. Lifecycle termination and
resource-release evidence are separate facts; a terminal failure does not prove
cleanup.

An operator may select a candidate from a running snapshot. Committing a binding
waits for confirmed discovery termination and revalidates the candidate's
generation, expiry, caller, scope, and current authority. Atomic one-time
consumption and idempotent binding retry belong to P045/P096, not the shared
deferred lifecycle.

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
effective_requested_ttl =
  min_present(connector_fail_after, action_preferred_max_ttl, caller_deadline_remaining)
effective_expires_at = now + min(effective_requested_ttl, host_max_ttl)
```

A connector cannot keep work alive indefinitely by returning larger
`retry_after_seconds` or `fail_after_seconds` values. A caller-provided
`deadline_at` is also an upper bound: if both the connector/action and caller
provide lifetime hints, the effective lifetime is the smaller value before the
host maximum TTL clamp is applied.

Caller-supplied directives SHOULD NOT carry ad-hoc polling cadence fields unless
the capability profile explicitly defines them. For Sensorium directives,
`timing.timeout_ms` remains the connector execution budget, not the deferred
operation polling lifetime. Deferred operation expiry is host-policy-owned and
may be narrowed by an explicit caller `deadline_at`.

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
  "deferred_operation_id": "deferred:sensorium.directive.invoke:...",
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
    "correlation/id": "run:..."
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

Continuation context is host/runtime-private unless a specific capability
contract says otherwise. Initial `deferred-operation.v1` responses expose only
the stable operation handle, retry hint, deadlines, and optional status/cancel
links. They MUST NOT echo operator-internal allowlist entries, connector config,
or raw private payloads.

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
sensorium-core validates action execution_mode_support
  -> sync-only + async: reject
  -> async-only + sync: reject

sensorium-os action start (for async-capable actions)
  -> start Inquirium/model job / OS job / external request
  -> persist operation handle in connector-owned state
  -> return sensorium-connector-deferred.v1

host later polls
  -> sensorium.operation.status
  -> sensorium-os connector status(operation_id)
  -> pending | running | completed | failed | timed-out | cancelled | expired | unknown
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

Per-flow JSON-e Flow configuration has exactly one deferred decision:
`deferred_response_mode`.

- `surface-to-caller` (default) surfaces `deferred-operation.v1` or pending
  `deferred-operation-status.v1` as a deferred control outcome.
- `reject-as-failure` treats deferred responses as a synchronous contract
  failure (`deferred-not-accepted`).

Retry cadence, TTL, polling limits, and continuation ownership are not
per-flow settings. They remain host policy (`DeferredHostPolicy`) and the later
continuation runtime.

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

The local discovery continuation uses the draft canonical
`deferred-operation-status.v2` with optional typed progress. P055-10 now has
structural and semantic validators and positive/negative vectors, including
revision safety, final snapshot equality and cleanup uncertainty. Existing v1
wire semantics and durable digests remain unchanged. P055-11 still owns the
host/provider/console integration and measured cancellation behavior.

The 2026-10-20 Node protected-cancellation investigation adds device-free
same-image differential controls and phase/clock/worker diagnostics, not new
S029 wire semantics. An already-returned refusal and terminal session cannot be
treated as work still approaching a guard; the test observer must retain those
facts instead of reporting a generic timeout. The original missing historical
phase is not inferred from later passing runs. See
`node:docs/audits/REVIEW-SENSORIUM-CANCELLATION-TIMEOUT-2026-10-20.md`.
P055-11's real provider/console and confirmed own-session cleanup gates remain
open; neither mock acknowledgements nor a local evidence-store copy close them.

Field naming should follow existing Orbiplex JSON style. The schema should use
explicit enums for status and should leave diagnostic objects open enough for
connector-specific details.

Required initial fields:

- `schema`,
- `status`,
- `operation/id`,
- `operation/kind`,
- `retry_after_seconds`,
- `created_at`,
- `expires_at`,
- optionally `status_href` when a poll endpoint exists.

Recommended fields:

- `cancel_href`,
- `correlation/id`,
- `causal/context`,
- `audit/outcome-ref`,
- `owner_module_id`,
- `capability_id`,
- `diagnostics`.

`causal/context` is the optional P081 canonical causal context for the deferred
operation. It preserves operation lineage across continuation, polling, retry,
and recovery without making P055 itself a global trace or transaction registry.
When present, terminal `deferred-operation-status.v1` values can be projected
into P081 `execution-receipt.v1` records. The P055 `operation/id` remains the
local deferred handle, while the P081 receipt uses
`causal/context.operation/id` as the causal operation identity.

`audit/outcome-ref` links the quick `202 Accepted` control response back to
the host/runtime outcome record that made the acceptance decision. This keeps
the new response shape auditable even though it intentionally no longer returns
the full domain-specific Sensorium result envelope.

The root schema is closed by default. Experimental or deployment-local metadata
belongs under `extensions`; stable fields should be promoted to explicit schema
properties.

## Invariants

- Initial invoke returns quickly.
- Deferred operation ids are stable and idempotent for the accepted work.
- The final result is idempotent for `operation/id`.
- Host clamps retry cadence and operation lifetime.
- Connector cannot extend the operation beyond host policy.
- Sync-only capability profiles cannot return deferred status.
- Deferred operations are cancelable or explicitly non-cancelable.
- Operator diagnostics must not leak raw private payloads by default.
- Long-lived workers remain behind a supervised middleware/service boundary.
- If `causal/context` is present, the host must preserve it across continuation
  and status projection. Caller-supplied causal metadata is lineage evidence, not
  actor authority.

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

The planned discovery consumer is an explicit exception to result recovery:
restart invalidates candidates, retains only permitted operation metadata, and
requires new admission for a new scan. It never resumes discovery from a saved
candidate list or persisted continuation.

### Private Data Leakage

Diagnostics or status payloads may expose raw private material.

Mitigation: status payloads carry summaries and references by default; raw data
stays in local/private storage with separate capability gates.

For planned discovery, even a reference or digest derived from a candidate list
is private. Split the caller response from durable metadata before persistence
and hashing; validate that logs, receipts, diagnostic digests, and replay contain
neither candidate material nor a digest derived from it.

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
  -> calls whisper.redaction.prepare with timing.mode = "async"
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
  -> sensorium.operation.status(operation_id)
  <- completed(redaction draft)
```

`whisper-intake` stores the draft. The operator reviews and approves it before a
public/federated `whisper-signal.v1` candidate can be published.

## Open Questions

Resolved for MVP:

1. Host deferred operation state is durable across daemon restarts in a
   host-owned SQLite registry at `<data-dir>/storage/deferred-operations.sqlite`.
   Connector-owned state is also durable where the connector accepts deferred
   work, starting with Sensorium OS.
2. Non-cancelable operations are allowed, but they must carry
   `cancel/unavailable-reason`. A payload with neither `cancel_href` nor
   `cancel/unavailable-reason`, or with both, is invalid.
3. JSON-e Flow uses persisted continuation state. The host registry stores the
   private continuation digest and payload; operator views expose only the
   redacted read model. On `completed` status the daemon resumes the flow with
   the final result bound at the deferred step.
4. The host default max TTL is 15 minutes. Sensorium OS action profiles may ask
   for shorter retry/TTL values, but the effective values are clamped by
   `DeferredHostPolicy`.

## Next Actions

1. [done] Add JSON Schemas for `deferred-operation.v1` and
   `deferred-operation-status.v1`.
2. [done] Add a minimal host-side deferred operation classifier and policy
   clamp helper.
3. [done] Add Sensorium deferred admission support. Sensorium-core validates
   `execution_mode_support`, maps connector-owned
   `sensorium-connector-deferred.v1` acknowledgements into canonical
   `deferred-operation.v1`, and exposes `sensorium.operation.status` to poll the
   connector status path.
4. [done] Add JSON-e Flow handling for explicit deferred step outcomes without
   busy-waiting. JSON-e Flow now suspends/fails with a control-plane
   `deferred-operation` diagnostic, can resume from a completed
   `deferred-operation-status.v1`, and exposes `deferred_response_mode` as the
   per-flow contract decision.
5. [done] Add operator visibility for pending/running/timed-out/expired
   deferred operations. The daemon exposes a shared registry API and the
   operator UI exposes `/admin/deferred-operations` with list/detail, poll, and
   cancel/non-cancelable controls.
6. [done] Use `whisper.redaction.prepare` as the first practical consumer:
   Sensorium OS can accept the action as deferred, persist its connector-owned
   state, report status after restart, and support cancellation while the action
   is still pending. Model-assisted redaction quality remains Inquirium/provider
   policy, not P055 runtime semantics.
7. [done] Use Artifact Delivery as a clean non-Sensorium consumer:
   `artifact.delivery.send?mode=deferred` persists an accepted delivery and
   returns `deferred-operation.v1`; the AD runtime uses `bounded-work-runtime`
   for transport retry/backoff/deadline mechanics, exposes a canonical
   `deferred-operation-status.v1` status URL, and provides a manual recovery
   pass for recoverable delivery records.
8. [done] Adopt the first P081 causal-context bridge:
   `deferred-operation.v1` and `deferred-operation-status.v1` may carry
   `causal/context`, and the Node `deferred-operation` crate can project a
   terminal deferred status into a P081 `execution-receipt.v1` using the
   canonical causal operation id.
9. [planned] Define and validate the typed v2 progress and metadata-retention
   contract in `P055-10`, then integrate its host/provider/console behavior in
   `P055-11`. [P045](045-sensorium-local-enaction-stratum.md#local-device-discovery-continuation)
   owns discovery lifecycle, candidate/binding semantics, and the generic
   discovery acceptance tracker; [P096](096-sensorium-brainflow-connector.md)
   owns qualification of the first BLE provider.

## Tracking

| ID | Work item | Status | Notes |
|---|---|---|---|
| P055-01 | Define `deferred-operation.v1` schema | done | Initial accepted response in `doc/schemas/` and node schema-gate, including the exactly-one cancelability invariant for `cancel_href` vs `cancel/unavailable-reason`. |
| P055-02 | Define `deferred-operation-status.v1` schema | done | Status poll response in `doc/schemas/` and node schema-gate. |
| P055-03 | Host policy clamp helper | done | `deferred-operation` owns retry/TTL clamp; `bounded-work-runtime` owns retry/backoff/concurrency mechanics. |
| P055-04 | Sensorium OS reference deferred action | done | Sensorium-core validates action execution mode, maps connector deferred acknowledgements to canonical host deferred operations, polls connector status through `sensorium.operation.status`, and can call `sensorium.operation.cancel` for pending connector work. |
| P055-05 | JSON-e Flow deferred step status | done | Flow suspends pending deferred outcomes, stores a host-owned persisted continuation, resumes from completed `deferred-operation-status.v1`, and may reject deferred responses via `deferred_response_mode = "reject-as-failure"`. |
| P055-06 | Operator visibility | done | Daemon owns a shared deferred-operation registry API and Node UI exposes `/admin/deferred-operations` with list/detail, poll, cancel, non-cancelable reason, expiry, retry, source, and redacted continuation/diagnostic digests. |
| P055-07 | Whisper redaction provider integration | done | `whisper.redaction.prepare` is available through the Sensorium OS deferred path; completed responses return through `deferred-operation-status.v1` and then through existing redaction response validation. Full model policy belongs to future Inquirium/provider policy. |
| P055-08 | Artifact Delivery deferred consumer | done | AD can persist a delivery through `submit_deferred` / `artifact.delivery.send?mode=deferred`, return canonical `deferred-operation.v1` with stable operation metadata and `audit/outcome-ref`, expose canonical `deferred-operation-status.v1`, and recover accepted/running/retryable records through its ledger-backed recovery pass. |
| P055-09 | P081 causal-context bridge | done | `deferred-operation.v1` and `deferred-operation-status.v1` accept optional `causal/context`; Node `deferred-operation` serializes that context through schema-gate and can build a P081 `execution-receipt.v1` from terminal status without changing the local P055 operation handle. |
| P055-10 | Versioned typed progress and private retention contract | done | Define `deferred-operation-status.v2`, optional typed progress, bounded replaceable snapshot/revision, v1 compatibility, and separate private-response/durable-metadata inputs before registry hashing. Evidence: schema vectors for revision/size/count bounds; state fixtures for monotonic replacement; candidate bytes, ids, and derived digests absent from every retained projection. P045-DISC-001 owns the discovery-specific request/profile/candidate contract; no P045 lifecycle or integration completion is required to define this shared contract. |
| P055-11 | Host/provider/console progress and cancellation integration | planned | Depends on P055-10, P045-DISC-003, and P045-DISC-004. Gate discovery on complete v2 support; test current-authority read/poll/cancel, replacement snapshots, selection-before-stop/binding-after-stop, limit/deadline partial domain results, confirmed own-session cancellation, uncertain cleanup with claim retained, candidate invalidation and no automatic scan/list recovery after restart, and existing v1 regression. P045-DISC-005 consumes this integration alongside the shared contract; P055-11 does not depend on P045-DISC-005. |
