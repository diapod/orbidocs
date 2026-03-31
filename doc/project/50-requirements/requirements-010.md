# Requirements 010: Supervised `http_local_json` Middleware Executor

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/20-memos/node-middleware-init-and-capability-reporting.md`
- `doc/project/30-stories/story-006.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-30`
Status: Draft (hard MVP slice)

## Executive Summary

This document defines the first implementation-facing requirements for a
supervision-aware local HTTP middleware executor in Orbiplex Node.

The hard MVP goal is narrow:

- keep `local_http_json` as the unmanaged adapter,
- add a distinct supervised executor kind `http_local_json`,
- include `Orbiplex Dator` and `Orbiplex Arca` as bundled Python middleware modules
  attached through that supervised executor,
- make the Node host own process lifecycle, readiness, restart, and shutdown,
- bind middleware init and module reporting into startup,
- and expose supervised middleware services as first-class daemon components.

## Context and Problem Statement

The current middleware runtime already supports:

- `nse_rhai`,
- `command_stdio`,
- `local_http_json`.

That is enough for the existing middleware MVP, but not for long-lived local
modules that naturally want to behave like attached services rather than one-shot
scripts.

Modules such as `Orbiplex Dator`, `Orbiplex Arca`, or later `Orbiplex Monus` may
need:

- queue state,
- long-lived HTTP handlers,
- local caches,
- stable readiness semantics,
- and lifecycle aligned with the Node.

`local_http_json` does not provide that. It only talks to an already-running
service and has no contract for:

- startup,
- readiness,
- shutdown,
- restart budget,
- or daemon-visible health.

Without a supervised executor, the system forces operators into one of two weak
patterns:

- managing attached module services completely outside the Node,
- or overusing `command_stdio` for modules that are operationally long-lived.

Both patterns weaken diagnostics, lifecycle visibility, and host authority.

## Proposed Model / Decision

### Executor Split

Orbiplex MUST keep two separate local HTTP middleware executor families:

- `local_http_json`
  - unmanaged,
  - assumes service already exists,
- `http_local_json`
  - supervised by the Node host,
  - owns launch, readiness, stop, and restart policy.

### Host-Owned Lifecycle

The host, not the module, MUST own the lifecycle of `http_local_json`.

At minimum, the host must be able to represent:

- `configured`
- `starting`
- `ready`
- `degraded`
- `stopping`
- `stopped`
- `failed`

### Hard MVP Runtime Surface

The hard MVP supervised executor configuration MUST admit at least:

- stable executor id,
- stable module id,
- daemon component id,
- executable path,
- arguments,
- optional working directory,
- optional environment variables,
- loopback HTTP endpoint,
- invoke path,
- readiness path,
- optional health path,
- startup timeout,
- request timeout,
- maximum response bytes,
- optional sandbox profile reference,
- bounded restart policy.

### Startup Contract

The hard MVP startup sequence MUST be:

1. launch child process,
2. apply host-owned sandbox/profile shaping before spawn,
3. wait for readiness within a bounded timeout,
4. emit `middleware-init`,
5. receive module report,
6. only then mark the component ready for hook traffic.

### Shutdown Contract

The host MUST stop supervised middleware services:

- during daemon shutdown,
- and when the owning daemon component is stopped or restarted.

### Invocation Contract

The supervised executor MUST continue to use the generic middleware host
contracts:

- input: `WorkflowEnvelope`
- output: `MiddlewareDecision`

The addition of supervision MUST NOT create a second semantic invocation
protocol.

### Bundled Hard-MVP Modules

The hard MVP MUST include at least two bundled middleware modules:

- `Orbiplex Dator`
- `Orbiplex Arca`

Both modules MUST:

- be distributed together with the Node release,
- be implemented in Python,
- be attached through `http_local_json`,
- remain host-supervised modules rather than privileged in-process components.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST support a distinct middleware executor kind `http_local_json` for host-supervised local HTTP JSON modules. | Fact | Proposal 019 |
| FR-002 | The system MUST preserve `local_http_json` as a separate unmanaged executor kind and MUST NOT silently overload it with supervision semantics. | Fact | Proposal 019 |
| FR-003 | `http_local_json` configuration MUST include stable `executor/id`, `module/id`, and `component/id` fields or their semantically equivalent canonical names. | Fact | Proposal 019 |
| FR-004 | `http_local_json` configuration MUST include launch information sufficient for host-owned process startup: executable path, arguments, optional working directory, and optional environment map. | Fact | Proposal 019 |
| FR-005 | `http_local_json` configuration MUST include one loopback HTTP endpoint plus an invoke path and readiness path. | Fact | Proposal 019 |
| FR-006 | The host MUST reject non-loopback endpoint targets for `http_local_json` in the hard MVP baseline. | Fact | Proposal 019 |
| FR-007 | The host MUST wait for module readiness before routing ordinary middleware hook traffic to a supervised `http_local_json` executor. | Fact | Proposal 019 |
| FR-008 | The host MUST bound readiness waiting by a configured startup timeout and mark the component `failed` if readiness is not reached in time. | Fact | Proposal 019 |
| FR-009 | The host MUST stop routing new invocations to a supervised middleware component before beginning its shutdown path. | Fact | Proposal 019 |
| FR-010 | The host MUST stop supervised `http_local_json` services when the daemon stops. | Fact | Proposal 019 |
| FR-011 | The host MUST also stop or restart a supervised `http_local_json` service when its owning component is stopped or restarted. | Fact | Proposal 019 |
| FR-012 | The first hard MVP restart policy for `http_local_json` MUST support at least `never` and `on_failure`. | Fact | Proposal 019 |
| FR-013 | For `on_failure`, the runtime MUST support bounded restart budget through at least `max_restarts` and `window_sec` or semantically equivalent fields. | Fact | Proposal 019 |
| FR-014 | When the restart budget is exhausted, the host MUST stop automatic restart attempts and surface the component as `failed`. | Fact | Proposal 019 |
| FR-015 | Supervised middleware startup MUST include the host-owned `middleware-init` handshake after readiness and before the component is considered available for ordinary hook execution. | Fact | Proposal 019 + middleware init memo |
| FR-016 | The supervised module MUST be able to return one module report carrying at least module name, short description, capability ids, and contract-version information. | Fact | Proposal 019 + middleware init memo |
| FR-017 | The daemon MUST expose supervised `http_local_json` services as first-class components in the operator-visible component map. | Fact | Proposal 019 |
| FR-018 | Operator inspection of those components MUST include at least current phase, last readiness outcome, restart counters, and last error summary. | Fact | Proposal 019 |
| FR-019 | The supervised executor MUST continue to consume `WorkflowEnvelope` and emit `MiddlewareDecision`, rather than defining a second middleware semantic protocol. | Fact | Proposal 019 |
| FR-020 | The host SHOULD distinguish middleware invocation trace from middleware service lifecycle facts so startup failures are not conflated with ordinary hook rejections. | Inference | Proposal 019 + project values |
| FR-021 | `http_local_json` MUST admit an optional sandbox-profile reference reusing the Node's host-owned sandbox policy surface for child process launch. | Fact | Proposal 019 |
| FR-021a | The supervised `http_local_json` surface MAY later expose explicit host-granted capability contracts for attached modules such as `Orbiplex Monus`, instead of ambient unrestricted access to memory, model, or publication surfaces. | Fact | Proposal 019 + Proposal 022 |
| FR-022 | The supervised executor MUST NOT receive host private signing keys or ambient settlement authority as part of its launch contract. | Fact | Proposal 019 + project values |
| FR-023 | The hard MVP Node distribution MUST bundle `Orbiplex Dator` as a Python middleware module attached through `http_local_json`. | Fact | Proposal 019 |
| FR-024 | The hard MVP Node distribution MUST bundle `Orbiplex Arca` as a Python middleware module attached through `http_local_json`. | Fact | Proposal 019 |
| FR-025 | The daemon MUST expose bundled `middleware.dator` and `middleware.arca` as first-class supervised components rather than opaque side effects of startup. | Fact | Proposal 019 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Lifecycle, readiness, and restart semantics for supervised middleware MUST remain host-owned rather than delegated to module folklore. | Fact | Proposal 019 |
| NFR-002 | The hard MVP supervised executor SHOULD remain small and SHOULD NOT grow into a general-purpose service mesh or external orchestrator. | Fact | Proposal 019 |
| NFR-003 | The same module implementation SHOULD remain replaceable behind another transport or executor kind as long as it preserves `WorkflowEnvelope` and `MiddlewareDecision` compatibility. | Inference | Contract-first architecture |
| NFR-004 | Supervised middleware services MUST remain diagnosable through stable operator-visible state rather than only through child-process logs. | Fact | Proposal 019 + project values |
| NFR-005 | The supervised local-HTTP contract SHOULD stay close enough to the model-runtime `http_local` pattern that later extraction of shared supervision primitives remains possible. | Inference | Proposal 019 + existing Node design |
| NFR-006 | Bundling `Dator` and `Arca` with Node MUST NOT collapse their authority into the host process; they remain replaceable modules behind the same host-owned contract. | Fact | Proposal 019 + project values |
| NFR-006a | Future attached modules such as `Monus` SHOULD receive only explicit host-granted capabilities, so the middleware runtime does not become a hidden ambient authority surface. | Fact | Proposal 022 + project values |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Module never becomes ready | Hook traffic would target an unusable service | Require bounded readiness wait and explicit `failed` component state. |
| Module keeps crashing and restarting | Endless flapping and unclear availability | Require bounded restart budget and terminal `failed` state after exhaustion. |
| Operator cannot tell whether the problem is startup or one bad request | Diagnostics collapse into opaque failure noise | Keep lifecycle state separate from ordinary middleware invocation trace. |
| Supervised module reaches beyond intended trust boundary | Host loses authority over secrets or policy | Reuse host-owned sandbox/profile controls and forbid key handoff. |
| Unmanaged and supervised HTTP executors drift into one blurred config family | Operators and implementors lose semantic clarity | Keep `local_http_json` and `http_local_json` as explicit separate executor kinds. |

## Open Questions

1. Should the hard MVP require a fixed configured endpoint, or may the child bind an ephemeral port and report it back after readiness?
2. Should `middleware-init` be routed through the normal invoke path or through a dedicated lifecycle path?
3. Which lifecycle facts should become their own persisted stream rather than only component-state snapshots?
4. When shared supervision primitives emerge, should middleware and model-runtime local HTTP services converge on one daemon-side supervisor module?

## Next Actions

1. Add typed `http_local_json` runtime contracts to the Node middleware-runtime crate.
2. Add daemon-owned supervision for that executor kind.
3. Package `Orbiplex Dator` and `Orbiplex Arca` as bundled Python middleware modules distributed with Node.
4. Wire middleware init and module reporting into the supervised startup path.
5. Expose supervised middleware component state through existing control-plane inspection.
6. Add integration tests for startup success, readiness timeout, restart exhaustion, and shutdown behavior of the bundled modules.
