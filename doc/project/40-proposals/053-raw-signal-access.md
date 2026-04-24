# Proposal 053: Raw Signal Access for Middleware Flows

Based on:

- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/40-proposals/044-host-owned-generic-module-store.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `node/middleware/src/envelope.rs`
- `node/middleware-runtime/src/runtime.rs`
- `node/middleware-runtime/src/json_e_executor.rs`

## Status

Draft

## Date

2026-04-24

## Executive Summary

Orbiplex middleware already passes a current envelope through an ordered chain
of components. Each component receives the data it needs, may ask the host to
apply allowed transformations, and then the next component sees the transformed
shape.

That is the normal stratified path.

This proposal adds an explicit escape hatch for a narrower technical need:
while one message is travelling through one middleware flow, selected components
may need access to the original raw signal or to the prior component inputs in
order to make a correct decision.

The decisions of this proposal are:

1. every middleware envelope SHOULD carry a host-owned `component_path[]` showing
   which components have participated in the current path,
2. the host MAY preserve a `raw_signal` from the initial trigger when at least
   one reachable component or flow declares that it needs it,
3. the host MAY preserve a `component_io_trace[]` append-list of per-component
   input snapshots, but only for paths where a downstream component requires
   that heavier visibility,
4. `raw_signal` and `component_io_trace[]` are in-memory, single-pass technical
   context in v1; they are not written to Memarium by this proposal,
5. the host, not middleware, decides whether preservation is enabled for a given
   hook/input class,
6. preservation and exposure are separate decisions: the host may carry raw
   context internally without exposing it to the current middleware,
7. middleware may read preserved context only when its own configuration and
   policy allow it,
8. raw signal access is an apophatic "hole in the abstraction": useful for edge
   cases, but not the default shape of ordinary data flow.

## Context and Problem Statement

The current middleware model is intentionally stratified:

- each component sees the current envelope,
- the host validates and applies only allowed mutations,
- the final output is the result of a bounded chain,
- trace records can later explain what happened.

This is enough for most flows. It keeps components small and prevents every
module from becoming aware of every lower-layer detail.

However, some edge cases need to pierce that abstraction during the same
execution:

- a component must compare a transformed payload with the original trigger,
- a safety check must inspect whether a previous component weakened or removed
  a relevant field,
- a classifier must know whether data was already normalized or came directly
  from an external signal,
- a connector-preparation step must know both the current operator-facing shape
  and the raw signal that started the chain.

Without a formal mechanism, components will smuggle this through ad-hoc fields,
mutable annotations, or out-of-band local storage. That makes the abstraction
leaky in the worst way: the system has a hidden dependency, but no host-owned
contract.

The goal is therefore to create a small, explicit, opt-in mechanism for raw
signal access inside one middleware passage.

## Goals

- Preserve a host-owned component path through each middleware flow.
- Allow selected execution paths to retain the initial raw signal.
- Allow selected execution paths to retain per-component input snapshots.
- Keep the mechanism in-memory and single-pass in v1.
- Make preservation a result of static configuration analysis, not a default.
- Avoid using Memarium as the first implementation of this mechanism.
- Keep the ordinary middleware path lightweight.

## Non-Goals

- This proposal does not define durable audit storage.
- This proposal does not write raw signals or traces to Memarium.
- This proposal does not define replay, export, or archival semantics.
- This proposal does not require every middleware component to receive raw input.
- This proposal does not replace existing `trace/*` records, JSON-e flow traces,
  or workflow step-completion records.
- This proposal does not give middleware permission to mutate trace fields.

## Decision

### 1. Raw Signal Access Context

The host SHOULD extend the middleware envelope with a host-owned raw signal
access context.

Conceptual shape:

```json
{
  "causality_id": "cause:01J...",
  "component_path": [
    "daemon:ingress",
    "middleware:sensorium-core",
    "middleware:story009-roles"
  ],
  "current_payload": {
    "kind": "inline",
    "value": {}
  },
  "raw_signal": {
    "kind": "inline",
    "value": {}
  },
  "component_io_trace": [
    {
      "component_id": "middleware:sensorium-core",
      "input": {}
    },
    {
      "component_id": "middleware:story009-roles",
      "input": {}
    }
  ]
}
```

The exact field placement remains implementation-specific. It may live inside
the existing `trace` object, beside the envelope as a host wrapper, or as a
transport-local context object that accompanies the envelope.

The semantic contract is more important than placement:

- `causality_id` identifies one causal passage,
- `component_path[]` is always append-only and host-owned,
- `current_payload` is the payload currently visible to the component,
- `raw_signal` is the initial signal from the first trigger,
- `component_io_trace[]` records the input each component received.

### 2. Component Path Is Always Preserved

`component_path[]` SHOULD be preserved for every middleware passage.

It is cheap and structurally useful:

- it explains how the message reached the current component,
- it supports loop detection,
- it helps debugging without exposing full payloads,
- and it gives later policy code a stable view of the path already taken.

Only the host may append to `component_path[]`. Middleware MUST NOT edit or
rewrite it.

The path entry SHOULD include a stable component identifier. A later version may
also include:

- executor kind,
- module id,
- capability id,
- local node id,
- or a step id inside a composite executor.

### 3. Raw Signal Preservation Is Opt-In Per Execution Path

The initial `raw_signal` SHOULD NOT be preserved by default.

It should be preserved only when configuration analysis determines that at least
one reachable component or flow declares a need for it.

Once enabled for a hook or flow passage, raw signal preservation MAY remain
enabled for the whole passage. The host does not need to recompute drop points
for raw signal before every executor because the raw signal is one already
existing initial value. This is different from `component_io_trace[]`, whose
cost grows with every step.

This keeps the normal flow small and limits accidental exposure. Raw signal can
contain:

- unnormalized external input,
- personal data,
- transient connector output,
- pre-redaction material,
- or operator-local context that later layers should not routinely see.

If no downstream component needs raw signal, the host SHOULD omit it entirely.

### 4. Preservation Is Not Exposure

The host may preserve more context than it exposes to the current middleware.

This is the core authority boundary:

```text
preserve_raw_signal          host keeps the initial trigger for this passage
preserve_component_io_trace  host keeps prior component inputs for this passage
expose_raw_signal            current executor/flow receives raw_signal
expose_component_io_trace    current executor/flow receives component_io_trace
```

A middleware component that does not declare raw signal access MUST receive a
sanitized envelope or wrapper that omits `raw_signal` and
`component_io_trace[]`, even if the host is preserving them for a later
component.

This prevents ambient authority. The fact that a lower layer keeps raw context
for continuity does not mean every component on the path can inspect it.

`component_path[]` is different: it is cheap, structural, and non-payload
bearing, so it remains visible as ordinary trace context unless local policy
redacts it.

### 5. JSON-e Flow Is One Operational Component

JSON-e flow middleware is treated as one operational component for raw signal
access in v1.

That means `raw_signal_access` belongs to the concrete JSON-e flow config, not
to a global JSON-e executor class. If one flow declares:

```json
{
  "id": "story009-role-draft-json-e-flow",
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": false
  }
}
```

then the host may expose raw signal to that flow invocation. Other JSON-e flows
without this declaration receive the ordinary projected context.

Inside a JSON-e flow, v1 exposes raw context only through the existing
`context_projection` mechanism. A later version may add per-step raw access
declarations, but the first boundary is per-flow because each flow is already an
operator-configured execution unit with its own id, limits, allowed calls,
template id, and trace policy.

### 6. Component Input Trace Is a Heavier Opt-In

`component_io_trace[]` is heavier than `raw_signal`.

It is an append-list of the inputs observed by components so far:

```json
[
  ["middleware:sensorium-core", {"input": "seen by sensorium-core"}],
  ["middleware:story009-roles", {"input": "seen by story009-roles"}]
]
```

The output of one component is normally the input of the next component, so v1
does not need to store both input and output at every step. The final output is
known from the final envelope or response.

If a component fails or returns early, the trace still shows the inputs leading
to that terminal point.

This trace SHOULD be enabled only for paths whose downstream components declare
that they need prior component inputs. It is not a general debugging flag.

Unlike raw signal, component I/O trace SHOULD be dropped as soon as the runtime
can prove that no remaining executor or flow can receive it. If the remaining
path cannot be proven, the host should preserve it conservatively or fail closed
according to local policy.

### 7. Preservation Table Is Derived from Configuration Analysis

The daemon SHOULD compute a preservation table before executing middleware
chains.

Inputs to the analysis include:

- middleware chain registrations,
- hook mutation policy,
- component capabilities,
- JSON-e flow definitions,
- declared component requirements,
- input channel or route metadata,
- message kind,
- service type,
- capability id,
- and known routing or dispatch rules.

The output is a table such as:

```json
{
  "before-broadcast-send": {
    "message_kind=resource-opinion": {
      "preserve_raw_signal": false,
      "preserve_component_io_trace": false,
      "expose_to": []
    }
  },
  "service-dispatch-execute": {
    "service_type=draft-author": {
      "preserve_raw_signal": true,
      "preserve_component_io_trace": false,
      "expose_to": ["story009-role-draft-json-e-flow"]
    },
    "service_type=editorial-review": {
      "preserve_raw_signal": true,
      "preserve_component_io_trace": true,
      "expose_to": ["story009-role-editorial-review-json-e-flow"]
    }
  }
}
```

The table says where the host must preserve raw signal or component input trace
because a later component may need it, and which executors or flows are allowed
to receive it.

This is deliberately a host-owned preflight result. Middleware declares needs;
the host decides when those needs are reachable.

### 8. Component Requirements Are Declarative

Middleware should declare raw-access needs in configuration or module report
data.

Conceptual shape:

```json
{
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": false,
    "reason": "compare normalized request with initial trigger",
    "max_raw_signal_bytes": 32768,
    "accepted_message_kinds": ["story009.role.execution"]
  }
}
```

For JSON-e flow, the same capability may be declared in the flow config:

```json
{
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": true
  }
}
```

The host MUST reject impossible or unsafe declarations during config validation.

### 9. Dynamic Routing Uses Conservative Preservation

Static analysis can be exact only when the host knows the possible execution
path.

When a chain contains dynamic routing, optional dispatch, or a component that
may hand off to several later components, the host SHOULD choose the smallest
conservative preservation set:

- if any reachable downstream component requires raw signal, preserve raw
  signal,
- if any reachable downstream component requires component I/O trace, preserve
  component I/O trace,
- if reachability cannot be narrowed, use the declared route class or hook-level
  policy as the boundary.

For raw signal, this conservative choice can persist for the whole passage once
enabled. For component I/O trace, the runtime SHOULD still drop the trace when a
later step proves that no possible remaining consumer exists.

If that would preserve too much sensitive input, local policy SHOULD fail closed
and require the operator to narrow the route or disable raw access.

### 10. Raw Signal Access Is Read-Only

Raw access context is read-only to middleware.

Middleware with an exposure grant may:

- read `raw_signal` if present and allowed,
- read `component_path[]`,
- read `component_io_trace[]` if present and allowed.

Middleware, with or without an exposure grant, must not:

- overwrite raw signal,
- remove path entries,
- edit prior trace entries,
- or claim that a raw signal was preserved when it was not.

The host owns all writes to this context.

### 11. No Memarium Writes in v1

This proposal intentionally does not write preserved raw signal or component I/O
trace to Memarium.

The data is a technical execution context, not necessarily a fact suitable for
durable memory.

Later proposals may define:

- opt-in archival of raw-access context,
- redacted trace storage,
- Memarium-backed replay records,
- or export bundles for operator debugging.

Those are separate decisions because persistence changes the privacy and
retention contract.

### 12. Limits and Redaction

Raw access MUST be bounded.

At minimum, configuration SHOULD support:

- maximum raw signal bytes,
- maximum component I/O trace entries,
- maximum input snapshot bytes per entry,
- allowed message kinds,
- allowed hooks,
- and redaction or deny rules for sensitive fields.

If the initial signal exceeds the configured limit, the host SHOULD either:

- omit `raw_signal` and expose a diagnostic,
- preserve a digest plus metadata,
- or fail the path if the downstream component declared raw signal as required.

The choice is local policy and should be explicit.

### 13. Relation to Existing Trace Mechanisms

This proposal complements existing trace surfaces.

Current mechanisms already include:

- `WorkflowEnvelope.trace.hop` and `trace.causality_id`,
- `MiddlewareRunResult.traces`,
- JSON-e flow step traces,
- daemon `trace/json-e-flow/...` records with step input/output digests,
- Story-009 workflow step-completion records with `memarium_record_id`
  pointers.

Raw Signal Access is different:

- it is available during the live flow,
- it may include actual raw input,
- it is selectively preserved based on reachability analysis,
- and it is not durable by default.

### 14. Why This Is an Apophatic Mechanism

Most of the time, the current abstraction should be enough. A component should
not need to know what all prior strata looked like.

Raw Signal Access exists for cases where the abstraction itself becomes part of
the risk. The system must then be able to drill a precise, host-owned hole
through the abstraction and show the lower signal without making that hole a
general data path.

The rule is:

```text
Preserve the raw signal when any declared reachable contract needs it.
Expose raw context only to the executor or flow whose own contract needs it.
Preserve component inputs only where a declared downstream contract needs them.
Always preserve the path.
```

## Minimal Data Model

### `RawSignalAccessContext`

```text
RawSignalAccessContext:
  causality_id
  component_path[]
  current_payload
  raw_signal?
  component_io_trace[]?
```

### `ComponentPathEntry`

```text
ComponentPathEntry:
  component_id
  module_id?
  executor_kind?
  capability_id?
  step_id?
```

### `ComponentInputTraceEntry`

```text
ComponentInputTraceEntry:
  component_id
  input
  input_digest
```

### `RawSignalAccessRequirement`

```text
RawSignalAccessRequirement:
  requires_raw_signal
  requires_component_io_trace
  reason
  max_raw_signal_bytes?
  max_trace_entry_bytes?
  accepted_hooks[]
  accepted_message_kinds[]
```

### `RawSignalPreservationRule`

```text
RawSignalPreservationRule:
  hook
  match
  preserve_raw_signal
  preserve_component_io_trace
  expose_to[]
  derived_from_components[]
```

## Open Questions

1. Should `current_payload` be an explicit field in the raw-access wrapper, or
   should it remain the envelope's normal `payload`?
2. Should `component_path[]` live inside `WorkflowEnvelope.trace`, or in a host
   wrapper beside the envelope?
3. Should component I/O trace store only input snapshots, or should it also
   store output snapshots for terminal and failed components?
4. How should raw signal access interact with encrypted or sealed payloads?
5. Which fields must be redacted before raw signal can be exposed to a
   downstream component?
6. Should module-report requirements, daemon config, and JSON-e flow config use
   a strict merge rule where local daemon policy may narrow but never broaden
   module-declared exposure?

## Implementation Direction

The recommended order is:

1. extend the envelope or host wrapper with `component_path[]`,
2. add raw-access requirement declarations to middleware config and JSON-e flow
   config,
3. implement the preservation-table analysis,
4. add an executor-input sanitizer that strips raw context unless the current
   executor or flow is in `expose_to[]`,
5. expose `raw_signal` only to the executor or flow whose own declaration
   requires it,
6. expose `component_io_trace[]` only to the executor or flow whose own
   declaration requires it,
7. add validation tests proving that unrelated paths do not receive raw signal,
8. add one Story-009 edge-case fixture that uses raw signal access without
   writing it to Memarium.

The implementation should start with in-memory propagation only. Durable trace
or Memarium integration belongs to a later proposal.
