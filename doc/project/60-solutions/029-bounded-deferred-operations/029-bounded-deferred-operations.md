# Bounded Deferred Operations

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md`
- `node:deferred-operation`
- `node:bounded-work-runtime`
- `node:daemon/src/deferred_registry.rs`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

## Status

Implemented MVP

## Date

2026-05-18

## Executive Summary

Bounded Deferred Operations define the shared Orbiplex control-plane contract
for host capabilities and middleware calls that cannot return a final domain
value inside one normal request budget.

The mechanism separates four concerns:

- `bounded-work-runtime` owns local bounded execution mechanics,
- `deferred-operation` owns the portable wire contracts and host policy clamps,
- the daemon owns the durable host registry, operator visibility, polling, and
  cancellation bridge,
- each domain runtime still owns the meaning and safety of its own work.

This solution promotes Proposal 055 from a proposal-level design into the
solution architecture. It is intentionally horizontal: Artifact Delivery,
Sensorium, JSON-e Flow, Whisper, and future middleware may consume the same
deferred-operation contract without turning the scheduler or daemon into a
domain workflow engine.

## Context and Problem Statement

Several Orbiplex paths need bounded long work:

- Artifact Delivery may accept a delivery and complete transport later.
- Sensorium OS actions may need time to run external local actions.
- JSON-e Flow may call a host capability that returns a pending control result.
- Whisper redaction preparation may need a provider step that is slower than a
  normal request-response call.

Without a shared contract, every component would invent its own pending status,
retry cadence, cancellation semantics, restart behavior, and operator UI. That
would create hidden coupling and make it hard to answer basic operational
questions such as:

- what is still running,
- what can be cancelled,
- when should the host poll again,
- what expired,
- what result should resume a suspended flow.

## Proposed Model / Decision

A long operation returns `deferred-operation.v1` instead of a final domain
payload. The payload is host-owned control-plane state:

```text
caller -> host capability / middleware
  -> accepted deferred operation
  -> host registry records the handle
  -> poller/operator checks status
  -> terminal status appears
  -> owning runtime consumes result or terminal failure
```

The status endpoint returns `deferred-operation-status.v1`. Terminal statuses
are:

- `completed`
- `failed`
- `timed-out`
- `cancelled`
- `expired`
- `unknown`

Non-terminal statuses are:

- `pending`
- `running`

The invariant for cancellation is strict:

```text
exactly one of:
  cancel_href
  cancel/unavailable-reason
```

This prevents two bad states: pretending every operation is cancelable, and
silently hiding that an operation cannot be cancelled.

## Stratification

```text
bounded-work-runtime
  bounded threads
  stop tokens
  retry/backoff
  deadlines

deferred-operation
  deferred-operation.v1
  deferred-operation-status.v1
  deterministic operation ids
  retry/TTL clamp policy

daemon deferred registry
  durable host read model
  status history digests
  poll/cancel API
  operator UI
  private continuation storage

domain runtimes
  Artifact Delivery ledger/recovery
  Sensorium OS action state
  JSON-e Flow continuation owner
  Whisper provider semantics
```

The daemon registry is an operator-visible join point, not the source of domain
truth. Domain ledgers still own their own facts, effects, and safety rules.

## Must Implement

### Deferred Operation Wire Contract

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- return `202 Accepted` with `deferred-operation.v1` when work is accepted but
  not complete,
- expose `status_href` and bounded retry/expiry hints,
- enforce exactly one cancellation surface,
- keep `continuation` and status polling in the control plane, not in the
  domain payload,
- validate contracts at host/runtime boundaries.

Status:

- `done`

### Host Policy and Bounded Runtime Boundary

Based on:

- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`

Responsibilities:

- clamp requested retry and TTL values through host policy,
- keep the host default maximum TTL at 15 minutes unless a deployment policy
  explicitly changes it,
- allow providers such as Sensorium OS to request shorter TTLs, but not longer
  than host policy,
- keep concurrency, retry/backoff, deadline, and stop-token mechanics in
  `bounded-work-runtime`.

Status:

- `done`

### Durable Host Registry

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- persist accepted operations under
  `<data-dir>/storage/deferred-operations.sqlite`,
- expose list/detail/status/poll/cancel APIs,
- store operator-visible fields such as kind, owner, status, retry, expiry,
  cancelability, correlation id, continuation digest, diagnostics digest, and
  last error,
- store status history as digest-only audit events,
- avoid exposing raw continuation or payload material in operator views.

Status:

- `done`

### Poll, Expiry, and Cancellation Runtime

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`

Related schemas:

- `deferred-operation-status.v1`

Responsibilities:

- poll registered operations through their owning runtime,
- respect `retry_after_seconds` and `expires_at`,
- mark expired operations as `expired`,
- bridge cancellation only when `cancel_href` exists,
- return the configured `cancel/unavailable-reason` for non-cancelable work,
- treat `unknown` as terminal rather than creating an infinite retry loop.

Status:

- `done`

### JSON-e Flow Persisted Continuation

Based on:

- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- suspend a JSON-e Flow when a host capability returns a deferred operation,
- persist continuation data as host-owned control-plane state,
- resume the flow after a `completed` status with the final result bound at the
  deferred step,
- fail the flow with a clear `deferred-operation` diagnostic for terminal
  failure states,
- preserve `deferred_response_mode = reject-as-failure` for flows that require
  synchronous semantics.

Status:

- `done`

### Sensorium OS Deferred Action State

Based on:

- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`

Responsibilities:

- map connector deferred acknowledgements to canonical host deferred operations,
- persist connector-owned deferred action state under the module data directory,
- expose `sensorium.operation.status`,
- expose `sensorium.operation.cancel` for work that is still pending,
- return explicit non-cancelable reasons for work already in irreversible
  phases.

Status:

- `done`

### Operator Visibility

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/001-node-ui/001-node-ui.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- expose `/admin/deferred-operations`,
- list pending/running/timed-out/expired/cancelled/failed/completed operations,
- show operation detail, retry state, expiry, source component, continuation
  owner, status history, and redacted digests,
- provide poll-now and cancel controls,
- never show raw continuation state or raw payloads in the operator UI.

Status:

- `done`

### Artifact Delivery Deferred Consumer

Based on:

- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `artifact-delivery-status.v1`
- `artifact-delivery-recovery.v1`
- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- accept `artifact.delivery.send?mode=deferred`,
- persist accepted delivery state in the AD ledger,
- return a canonical deferred operation handle,
- expose operation status through the shared deferred status contract,
- recover accepted/running/retryable records through AD recovery.

Status:

- `done`

## May Implement

### Automatic Poller Wakeups

Based on:

- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- run a lightweight daemon poller for due operations,
- optionally use the replay scheduler as a wake-up source,
- keep deferred-operation semantics in the P055 runtime rather than inside the
  scheduler,
- expose poller counters to operators.

Status:

- `planned`

### Cross-Node Deferred Operation Aggregation

Based on:

- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- aggregate deferred state across nodes only when an explicit federated
  operator view exists,
- avoid treating remote deferred handles as local authority,
- preserve per-node ownership and audit semantics.

Status:

- `deferred`

## Out of Scope

- replacing domain ledgers such as Artifact Delivery delivery history,
  Sensorium connector action state, or workflow-specific ledgers,
- capturing runtime stacks, closures, file handles, sockets, locks, or thread
  handles as continuations,
- turning the daemon into a generic workflow engine,
- treating deferred operations as ordinary domain payload,
- making every operation cancelable,
- exposing raw continuation state through operator UI,
- defining provider-specific quality policy for Whisper redaction.

## Consumes

- `deferred-operation.v1`
- `deferred-operation-status.v1`
- domain runtime status surfaces such as Artifact Delivery delivery status and
  Sensorium connector operation status,
- host policy for retry, TTL, and cancellation behavior.

## Produces

- durable deferred operation read model,
- digest-only status event history,
- operator list/detail/poll/cancel surfaces,
- resumed runtime continuations for owners such as JSON-e Flow,
- terminal diagnostics for failed, timed-out, cancelled, expired, and unknown
  operations.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Deferred handle has no cancellation semantics | Schema requires exactly one of `cancel_href` or `cancel/unavailable-reason`. |
| Provider restart loses accepted work | Critical providers persist connector-owned state; host registry persists the shared read model. |
| Polling loops forever on unknown operation | `unknown` is terminal and written to registry history. |
| Deferred handle leaks into domain payload | Runtimes treat it as control-plane state and either suspend, resume, or fail the flow. |
| Operator UI exposes sensitive continuation state | UI shows only digest and redacted read-model fields. |
| Scheduler becomes workflow engine | Scheduler may wake polling, but deferred-operation runtime owns status semantics and continuation ownership. |

## Tests and Evidence

Current MVP evidence includes:

- schema validation for positive and negative `deferred-operation.v1` examples,
- `deferred-operation` unit tests for TTL/retry clamp and cancellation
  invariant,
- middleware-runtime tests for JSON-e Flow suspend/resume/reject behavior,
- Sensorium Core tests for deferred connector delegation,
- Sensorium OS service tests for deferred action state and cancellation,
- daemon tests for registry persistence and AD deferred recovery,
- Node UI and daemon compile checks,
- Story-005 AD smoke using deferred/recovery-capable Artifact Delivery paths.

## Related Capability Data

- `029-bounded-deferred-operations-caps.edn`

## Notes

This solution deliberately names a horizontal control-plane mechanism rather
than a domain component. That is why it is not folded into Artifact Delivery,
Sensorium, Scheduler, or Middleware: each of those consumes the contract, but
none should own the shared vocabulary for bounded deferred work.
