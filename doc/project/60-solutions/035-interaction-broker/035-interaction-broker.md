# Interaction Broker

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `node:interaction-broker-core`
- `node:deferred-operation`

Related schemas:

- `interaction-broker-watch.v1`
- `interaction-broker-wait.request.v1`
- `interaction-broker-wait.outcome.v1`
- `interaction-broker-probe.v1`
- `deferred-operation-status.v1`

## Status

Partial foundation

## Date

2026-06-24

## Executive Summary

Interaction Broker is the host-owned coordination primitive for bounded
waits, watches, and probes across registered observation sources. It lets a
runtime wait for something to happen without inventing private polling loops,
hidden watcher threads, or component-specific pending-state dialects.

The broker is not a domain workflow engine. It owns admission, grants,
deadlines, idempotency, cursor binding, cancellation of broker resources,
operator-visible outcomes, and audit. Domain components such as Sensorium
Workbench, Artifact Delivery, Memarium, approvals, and the deferred-operation
registry remain the owners of their own facts, effects, and state.

The current implementation state is an unwired Rust foundation in
`node:interaction-broker-core`. Cross-process broker routes, daemon
persistence, source registration, operator status, and retention-backed replay
are not implemented yet.

## Context And Problem Statement

Interactive component flows need to ask questions such as:

- did this command finish,
- did this file appear,
- did an artifact become available,
- did an approval arrive,
- did a deferred operation reach a terminal status,
- did a terminal stop making progress.

Without a shared host primitive, each component would either block a request,
spin a private watcher, scrape another component's state, or create a custom
pending status. That would couple domains that should stay independent and make
operator diagnosis hard.

Proposal 071 names Sensorium Workbench as the first concrete pressure point for
this primitive, but the broker is deliberately horizontal. Workbench is only one
observation source family.

## Proposed Model / Decision

The host owns three resource classes:

- `watch` observes one registered source from a bounded cursor and returns a
  bounded event batch;
- `wait` evaluates one declarative condition against one primary source until
  it is satisfied, terminal, or expired;
- `probe` actively asks a source provider to check a bounded fact, such as
  liveness, readiness, file existence, artifact presence, or progress.

Every broker resource has:

- a stable ref,
- caller identity and grant context at admission time,
- an idempotency key,
- a deadline or TTL,
- byte/event caps,
- classification,
- a `correlation/id`,
- a final outcome or terminal status.

Short waits may complete synchronously. A wait that can outlive one HTTP
request becomes a Bounded Deferred Operation. `deferred-operation-status.v1`
remains the lifecycle status model; `interaction-broker-wait.outcome.v1` is the
domain result carried under `result` for completed async waits.

Before a wait outcome is embedded in `deferred-operation-status.v1.result`, the
broker applies host-owned serialized byte and count caps to `observed` and
`diagnostics`. The deferred-operation status surface must not become an
unbounded provider payload channel.

## Stratification

```text
interaction-broker-core
  DTOs, validation, wait/watch/probe vocabulary, deferred status projection

daemon interaction broker service
  admission, grants, source registry, durable store, idempotency, replay window

source providers
  Workbench terminal/file events, AD artifact state, Memarium query state,
  approvals, deferred-operation registry

consumers
  Sensorium Core, JSON-e Flow, operator UI, future Inquirium loops
```

The broker must not reach into source internals. A source provider registers a
bounded observation/probe adapter; the broker decides whether the caller may use
it and how long the broker resource may live.

## Interaction With Deferred Operations

The broker consumes Bounded Deferred Operations rather than replacing them.

If a wait is longer than one request budget, the broker returns
`deferred-operation.v1` with `operation/kind = "interaction-broker.wait"`. Later
status reads return `deferred-operation-status.v1`. When the wait completes
successfully, `result` contains `interaction-broker-wait.outcome.v1`.

The broker must share the deferred-operation deterministic id validator. It must
not accept ids through a weaker private `deferred:` string-prefix check.

## Interaction With Sensorium Workbench

Sensorium Workbench produces terminal events, file metadata, environment status,
and active probe answers for resources it owns. Interaction Broker owns
cross-source wait/watch/probe admission and operator-visible wait state.

Workbench may satisfy a simple connector-local short wait directly only when it
does not span other components and does not outlive the request. Any cross-source
join belongs to the host broker.

Process termination is never broker-owned. If a wait or probe reports
`maybe_hung`, `no_progress`, `waiting_for_input`, timeout, or probe failure, the
result is diagnostic only. Killing, signaling, or closing a process remains a
Workbench connector directive or operator action.

## Storage And Recovery

The daemon runtime must follow the Temporal Storage Convention:

- explicit SQLite migrations,
- WAL-oriented pragmas,
- `busy_timeout`,
- foreign keys where applicable,
- idempotency keys,
- bounded retention,
- replay/projection diagnostics.

The broker store records active and recently completed waits, watches, probes,
cursor bindings, source refs, deadlines, final outcomes, and idempotency
decisions. It must not store raw terminal output, file content, prompt text, or
secrets unless a separate classified artifact capture explicitly authorizes it.

On startup, the daemon must run a broker recovery pass before accepting new
broker resources. Interrupted waits, watches, and probes become explicit
`failed-retryable`, `expired`, or `unknown` records according to policy; they do
not silently disappear.

## Trade-Offs

Benefits:

- one bounded coordination model instead of private polling loops,
- explicit operator visibility for pending and stuck interactions,
- reuse of Bounded Deferred Operations for long waits,
- less coupling between Sensorium, AD, Memarium, approvals, and future model
  loops.

Costs:

- one more host primitive and store,
- source providers must implement bounded observation/probe adapters,
- early schemas must be kept narrow until real cross-source use proves the
  vocabulary.

## Failure Modes And Mitigations

| Failure mode | Mitigation |
| --- | --- |
| A wait extends authority beyond the caller grant. | Clamp wait lifetime to grant expiry and reject stale or scope-mismatched waits. |
| A source-specific wait leaks into broker semantics. | Keep condition kinds small and promote only reusable conditions; source-specific detail stays in provider diagnostics. |
| A watch cursor is replayed against the wrong source. | Cursor carries its source binding and fails closed on mismatch. |
| A provider returns an oversized wait outcome. | Validate outcome schema shape and serialized byte/count caps before deferred-operation projection. |
| Quiet terminal output is treated as a hang. | Keep `quiescent`, `waiting_for_input`, `no_progress`, `maybe_hung`, and `probe_failed` separate. |
| Broker timeout kills a process. | Forbid broker-owned process termination; remediation is a connector/operator directive. |
| Broker store becomes a raw transcript store. | Store metadata by default; capture bytes only through separately classified artifacts. |

## Must Implement

### Broker Contract Core

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`

Related schemas:

- `interaction-broker-watch.v1`
- `interaction-broker-wait.request.v1`
- `interaction-broker-wait.outcome.v1`
- `interaction-broker-probe.v1`

Responsibilities:

- define source refs, watch cursors, wait scopes, wait conditions, probe
  conditions, caps, deadlines, and timeout behavior,
- reject cursor/source mismatch,
- reject path traversal in file wait/probe conditions,
- reject oversized wait outcome `observed` and `diagnostics` payloads before
  deferred-operation projection,
- require explicit `schema` and `schema/v` for top-level broker payloads,
- project completed async waits into `deferred-operation-status.v1.result`.

Status:

- `partial`: `node:interaction-broker-core` exists and is unwired.

### Host Broker Runtime

Based on:

- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`

Related schemas:

- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- own daemon admission, grant checks, idempotency keys, deadlines, and durable
  broker state,
- expose local wait/watch/probe runtime surfaces only after JSON Schemas and
  golden vectors are frozen,
- register async waits in the host deferred-operation registry,
- surface active and terminal broker resources to operator status.

Status:

- `planned`.

### Source Provider Registry

Responsibilities:

- let Workbench, Artifact Delivery, Memarium, approvals, and deferred-operation
  registry register bounded source adapters,
- keep each provider responsible for its own facts and concrete probes,
- prevent the broker from reaching into component-private storage.

Status:

- `planned`.

## May Implement

### Cross-Source Joins

Cross-source joins may be added after single-source waits and watches are backed
by durable replay windows. Until then, callers should compose smaller waits in
host-owned JSON-e Flow or another deferred-aware control-plane runtime.

Status:

- `deferred`.

## Open Questions

1. Which source provider should be the first runtime consumer after Workbench:
   Artifact Delivery artifact presence, approvals, or deferred-operation
   registry?
2. Should broker watches use polling only in the first daemon runtime, or should
   source providers be able to push events into the broker store?
3. What is the smallest operator UI shape that makes pending waits useful
   without exposing raw terminal or file content?

## Next Actions

- Publish JSON Schemas and examples for the current broker DTOs.
- Add daemon storage migrations and an unwired broker service skeleton.
- Wire the broker to the shared deferred-operation deterministic id validator.
- Add conformance tests for cursor/source mismatch, scope mismatch, deadline
  clamp, malformed deferred ids, and path traversal refusal.
