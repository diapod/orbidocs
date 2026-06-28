# Raw Signal Access

Based on:

- `doc/project/40-proposals/053-raw-signal-access.md`
- `node/middleware/src/envelope.rs`
- `node/middleware/src/module_report.rs`
- `node/middleware-runtime/src/runtime.rs`
- `node/middleware-runtime/src/json_e_executor.rs`

## Status

Implemented

## Purpose

Raw Signal Access is a local, in-memory execution mechanism for middleware
flows that need to inspect the initial trigger or prior component inputs during
one passage through a middleware chain.

It is not durable memory, not audit storage, and not a Memarium write path.

## Runtime Contract

The runtime separates preservation from exposure.

Preservation is host-owned:

- `component_path[]` is always carried and appended by the runtime,
- `raw_signal` is preserved for the passage when at least one executor declares
  `requires_raw_signal`,
- `component_io_trace[]` is preserved only while a later executor may need it.

Exposure is executor-local:

- an executor without `raw_signal_access` receives a sanitized envelope,
- an executor with `requires_raw_signal` receives the initial payload under
  `trace.raw_signal_access.raw_signal`,
- an executor with `requires_component_io_trace` receives prior component input
  snapshots under `trace.raw_signal_access.component_io_trace`,
- the final `MiddlewareRunResult.envelope` never carries
  `trace.raw_signal_access`.

This prevents ambient authority. The host may carry raw context internally
without exposing it to middleware that did not ask for it and was not allowed by
local policy.

## Supervised HTTP Middleware

Supervised HTTP middleware declares raw access in its module report:

```json
{
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": false,
    "reason": "compare normalized payload with initial trigger"
  }
}
```

When the daemon returns a ready supervised executor from the middleware
supervisor, it wraps the executor with the latest module-report
`raw_signal_access` declaration. The underlying HTTP executor remains unaware of
module reports; the daemon layer binds module metadata to runtime exposure.

## JSON-e And JSON-e Flow

JSON-e and JSON-e-flow declare raw access in the concrete executor or flow
config:

```json
{
  "id": "story009-role-draft-json-e-flow",
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": false
  }
}
```

The declaration is per flow, not global for all JSON-e execution.

Raw context is visible to the template only if the operator projects it through
`context_projection`, for example:

```json
{
  "context_projection": {
    "raw_signal": "$.trace.raw_signal_access.raw_signal",
    "component_path": "$.trace.component_path"
  }
}
```

Without that projection, the flow may be allowed to receive raw context but the
template still does not see it as a named context value.

Current implementation status:

- JSON-e hook-chain executors are wired through `MiddlewareRuntime::run_hook`
  and can receive raw context when their `output_contract` is
  `middleware-decision.v1`.
- JSON-e-flow configs accept the same declaration per flow. Direct
  host-capability dispatch is bridged by the daemon's
  `DispatchTraceContext`, which keeps the host-owned raw context and projects
  only `trace.component_path` plus, for declaring flows only,
  `trace.raw_signal_access` into the invocation object before JSON-e
  projection.
- A JSON-e-flow executor is not treated as a generic `MiddlewareExecutor`,
  because flow output is a service response, not a middleware decision.

## Component Path

Each executor invocation appends one path entry:

```text
ComponentPathEntry:
  component_id
  executor_kind
```

The MVP uses the executor id as `component_id`. Later daemon-level integrations
may enrich entries with `module_id`, `capability_id`, or per-flow `step_id`.

## Component I/O Trace

`component_io_trace[]` stores the input payload observed by prior components.

The runtime appends a component input only when a remaining executor declares
`requires_component_io_trace`. If no remaining executor can consume it, the
runtime does not keep growing the trace.

Each receiving executor's declaration bounds the exposed trace view. If
`max_trace_entry_bytes` is set and a prior input snapshot is larger than that
limit, the host replaces the exposed `input` with a redacted metadata object
and sets `input_digest` to a `sha256:` digest of the original JSON bytes.

The MVP bounds each exposed raw value by byte size. It does not yet impose a
separate maximum number of component I/O trace entries. Deep or dynamically
expanded workflows should keep `requires_component_io_trace` narrow; a future
`max_component_io_trace_entries` policy can cap trace length if profiling shows
that entry count, not entry size, is the operational risk.

The host may still hold the original input in memory for the current passage.
That value is not written to Memarium, the daemon module store, JSON-e-flow
traces, or the final envelope.

## Size Limits And Digest-Only Projection

Raw access uses per-receiver bounds:

- `max_raw_signal_bytes` limits the exposed initial `raw_signal`,
- `max_trace_entry_bytes` limits each exposed component input trace entry.

When an exposed value exceeds its bound, the executor receives:

```json
{
  "redacted": true,
  "reason": "raw-signal-size-limit",
  "original/sha256": "sha256:...",
  "original/bytes": 49152,
  "limit/bytes": 32768
}
```

This keeps the mechanism useful for causality debugging while preventing a
component from receiving unbounded raw payloads just because another component
needed preservation.

## Boundaries

This solution intentionally does not:

- persist raw signal or component I/O trace to Memarium,
- expose raw context to every middleware in a chain,
- define replay or durable trace export,
- make raw access a debugging flag,
- or allow middleware to mutate `component_path[]` or `raw_signal_access`.

Direct dispatch paths that bypass `MiddlewareRuntime::run_hook` must implement
their own bridge explicitly. The daemon JSON-e-flow bridge is the first such
bridge; other direct sidecar paths remain out of scope until they declare the
same need.

## Tests

The MVP is covered by runtime tests that verify:

- only the declaring executor receives raw signal,
- only the declaring executor receives component I/O trace,
- oversized raw signal and component input trace values are exposed only as
  digest metadata,
- JSON-e can project exposed raw signal through `context_projection`,
- direct JSON-e-flow dispatch receives the same bounded projection semantics,
- final envelopes do not leak `trace.raw_signal_access`.
