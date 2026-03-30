# Proposal 019: Supervised `http_local_json` Middleware Executor

Based on:
- `doc/project/20-memos/node-middleware-init-and-capability-reporting.md`
- `doc/project/20-memos/node-http-middleware-auth-token-header.md`
- `doc/project/30-stories/story-006.md`
- `doc/project/60-solutions/node.md`
- `node:middleware-runtime/README.md`
- `node:model-runtime/README.md`

## Status

Proposed (Draft)

## Date

2026-03-30

## Executive Summary

Orbiplex Node should add a new supervised middleware executor class for long-lived
local HTTP JSON modules:

- `http_local_json`

This executor is intentionally distinct from the current unsupervised:

- `local_http_json`

The key decision is simple:

1. `local_http_json` remains a pure adapter for an already-running local service,
2. `http_local_json` becomes the hard MVP executor for middleware modules that must
   be started, observed, and stopped together with the Node or with a dedicated
   daemon-owned component,
3. the Node host, not the module, remains the authority over lifecycle, readiness,
   restart policy, sandboxing, and exported operator state,
4. the module continues to communicate through HTTP JSON request/response rather than
   through ambient in-process privilege,
5. middleware init and capability reporting should become part of the supervised
   startup path so attached modules are no longer opaque executors.

This gives Orbiplex a practical deployment model for Dator-like and Arca-like
middleware without forcing every externally implemented module into one-shot
`command_stdio` execution or requiring a separate service manager outside the Node.

For the hard MVP baseline, `Orbiplex Dator` and `Orbiplex Arca` should be shipped
with Node as bundled Python middleware services attached through the supervised
`http_local_json` connector/executor.

## Context and Problem Statement

The current middleware runtime already has three execution surfaces:

- `nse_rhai`
- `command_stdio`
- `local_http_json`

This is enough for the functional middleware MVP, but it leaves one important gap.

`local_http_json` assumes that the target service is already running. It knows:

- endpoint,
- method,
- headers,
- timeout,
- response-size cap.

It does not know:

- how to start the service,
- how to wait for readiness,
- how to stop the service,
- how to represent the service as a daemon-owned component,
- how to surface service health in a stable operator-visible way,
- how to apply the middleware init/report contract as part of attachment.

That gap matters more now because the project is moving toward Node-attached modules
that are:

- separately implemented,
- potentially long-lived,
- richer than one-shot policy scripts,
- but still meant to be supervised by the Node host.

`story-006.md` makes this concrete. Modules such as `Orbiplex Dator` and
`Orbiplex Arca` fit poorly into `command_stdio` when they need:

- internal queueing,
- cached state,
- local HTTP APIs,
- long-lived sessions to adjacent systems,
- or a stable process lifetime aligned with the Node.

Without a supervised local-HTTP executor, the system drifts toward two bad options:

1. operators must manage attached module services manually outside the Node, which
   makes health, startup ordering, and diagnostics inconsistent,
2. modules are forced into `command_stdio`, even when their natural shape is
   a long-lived local service.

Neither option fits Orbiplex's preferred architecture of:

- explicit contracts,
- small trusted core,
- host-owned lifecycle semantics,
- and visible operational state.

## Goals

- Define a supervision-aware middleware executor for long-lived local HTTP JSON
  modules.
- Include `Orbiplex Dator` and `Orbiplex Arca` in the hard MVP as bundled
  middleware modules attached through `http_local_json`.
- Keep `local_http_json` as the unmanaged adapter and avoid overloading it with
  lifecycle semantics.
- Make module startup, readiness, shutdown, and restart policy host-owned.
- Expose supervised middleware services as explicit daemon components.
- Integrate middleware init and module reporting into the supervised attach flow.
- Reuse existing middleware request/response semantics rather than inventing a second
  invocation contract.
- Keep the hard MVP small enough to implement in the current Node without requiring
  a separate orchestration subsystem.

## Non-Goals

- This proposal does not redefine the generic middleware envelope or decision model.
- This proposal does not replace `command_stdio`.
- This proposal does not require remote network exposure for middleware modules.
- This proposal does not define full native sandbox isolation across all operating
  systems; it only requires that the host-owned sandbox/profile surface can be
  applied to supervised child processes.
- This proposal does not introduce a general-purpose service mesh or sidecar system.
- This proposal does not yet standardize a Unix-domain-socket variant.

## Decision

Orbiplex should add one new middleware executor kind:

- `http_local_json`

Its semantics are:

- the Node host owns process launch,
- the module exposes a loopback HTTP JSON invocation surface,
- the module is supervised as a daemon-owned runtime component,
- the Node waits for readiness before routing hook traffic to it,
- the Node stops it during daemon shutdown or when its owning component stops,
- the Node records lifecycle and health facts separately from ordinary middleware
  invocation traces.

The existing `local_http_json` executor remains valid and intentionally simpler:

- it is an adapter to an already-running local service,
- it is not responsible for service lifecycle.

For the hard MVP:

- `Orbiplex Dator` MUST be distributed with Node as a supervised Python middleware
  service,
- `Orbiplex Arca` MUST be distributed with Node as a supervised Python middleware
  service,
- both MUST be attached through `http_local_json`,
- both remain host-supervised extensions rather than privileged in-process
  subsystems.

## Proposed Model

### 1. Executor Taxonomy

The middleware runtime should have the following split:

- `nse_rhai`
  - in-process
  - no separate process lifecycle
- `command_stdio`
  - one-shot
  - process per invocation
- `local_http_json`
  - unmanaged long-lived local service
  - host assumes the service already exists
- `http_local_json`
  - host-supervised long-lived local service
  - host owns startup, readiness, stop, and restart behavior

This mirrors the already useful split in `node:model-runtime/README.md`:

- `http_local` separates lifecycle from invocation,
- `command_stdio` is for direct process invocation,
- and the same distinction should exist for middleware.

### 2. Hard MVP Contract

The hard MVP supervised executor should require one runtime configuration with at
least:

- stable executor id,
- stable module id,
- executable path,
- arguments,
- optional working directory,
- optional environment map,
- one loopback bind target or endpoint expectation,
- one invoke endpoint,
- one readiness endpoint,
- startup timeout,
- request timeout,
- response-size cap,
- optional sandbox-profile reference,
- bounded restart policy,
- owning daemon component id.

The hard MVP should assume at least two bundled supervised middleware component
profiles:

- `middleware.dator`
- `middleware.arca`

Recommended MVP JSON shape:

```json
{
  "id": "dator-http",
  "kind": "http_local_json",
  "module_id": "orbiplex-dator",
  "component_id": "middleware.dator",
  "launch": {
    "executable": "/opt/orbiplex/modules/dator/bin/dator-service",
    "args": ["serve", "--bind", "127.0.0.1:47951"],
    "cwd": "/opt/orbiplex/modules/dator",
    "env": {
      "ORBIPLEX_MODULE_ID": "orbiplex-dator"
    }
  },
  "http": {
    "endpoint": "http://127.0.0.1:47951",
    "invoke_path": "/v1/middleware/invoke",
    "ready_path": "/readyz",
    "health_path": "/healthz",
    "method": "POST",
    "headers": {},
    "startup_timeout_ms": 15000,
    "request_timeout_ms": 5000,
    "max_response_bytes": 65536
  },
  "sandbox_profile": "module-restricted",
  "restart_policy": {
    "mode": "on_failure",
    "max_restarts": 3,
    "window_sec": 60
  }
}
```

The exact field names may still evolve, but the MVP semantics should stay stable.

For packaging, the Node distribution should contain:

- the host-side `http_local_json` runtime,
- a bundled Python distribution for `Orbiplex Dator`,
- a bundled Python distribution for `Orbiplex Arca`,
- default component configuration wiring those modules into supervised startup.

### 3. Lifecycle Ownership

For `http_local_json`, the host owns these phases:

1. `configured`
2. `starting`
3. `ready`
4. `degraded`
5. `stopping`
6. `stopped`
7. `failed`

The module does not self-declare semantic authority over those states. It may report
health, but the host interprets that health and publishes the resulting component
state.

### 4. Startup Semantics

The MVP startup path should be:

1. daemon loads supervised middleware runtime config,
2. daemon starts the child process,
3. daemon applies the configured sandbox/profile surface before spawn,
4. daemon waits for `ready_path` to succeed within `startup_timeout_ms`,
5. daemon sends `middleware-init`,
6. module responds with module report,
7. daemon marks the component `ready` and starts routing hook calls to it.

If readiness never succeeds:

- the process is stopped,
- the component becomes `failed`,
- operator surfaces show explicit startup failure,
- ordinary hook traffic must not be routed to that executor.

### 5. Stop and Shutdown Semantics

The MVP stop path should be:

- when the daemon stops, supervised middleware services stop too,
- when the owning component is stopped or restarted, its supervised HTTP service
  follows that lifecycle,
- the host should first stop routing new hook invocations,
- then terminate the child process,
- then mark the component `stopped` or `failed` depending on the outcome.

For hard MVP, graceful termination may be simple:

1. send process termination signal,
2. wait bounded time,
3. force-kill if still alive.

The exact signal differs by platform, but the host-owned semantics should remain the
same.

### 6. Restart Policy

The hard MVP restart policy should stay small:

- `never`
- `on_failure`

For `on_failure`, the runtime should support:

- `max_restarts`
- `window_sec`

If the process exceeds that restart budget:

- the component becomes `failed`,
- the daemon does not keep flapping forever,
- operators must explicitly restart it.

This is enough for MVP. Richer backoff curves can come later.

### 7. Health Model

`http_local_json` should expose two distinct health notions:

- `ready_path`
  - whether the service can receive middleware invocations now
- `health_path`
  - optional broader health surface exposed by the service itself

The host should publish at least:

- process running or not,
- current phase,
- last readiness result,
- last healthcheck result,
- restart counters,
- last error summary.

This state should appear in the daemon component map, not only in hidden logs.

In the hard MVP, those operator-visible components should include at least:

- `middleware.dator`
- `middleware.arca`

### 8. Middleware Init and Module Reporting

The supervised attach flow should consume the existing init/report direction from
`doc/project/20-memos/node-middleware-init-and-capability-reporting.md`.

After readiness, the host sends:

- `middleware-init`

The module then returns one module report carrying at least:

- module name,
- short description,
- capability ids,
- declared output-contract references where required,
- middleware contract version,
- host API version expected by the module.

The host stores and exposes that report as module metadata rather than leaving the
executor as a bare id plus URL.

### 9. Invocation Contract

The supervised executor should reuse the same envelope/decision contract as other
middleware executors:

- input: `WorkflowEnvelope`
- output: `MiddlewareDecision`

The HTTP body should remain request/response JSON, not an ambient RPC system.

This keeps the executor transport replaceable:

- same semantic host contract,
- different lifecycle ownership model.

### 10. Sandbox and Process Policy

The supervised executor should reuse the same host-owned sandbox-profile surface now
used for `command_stdio`, as far as that surface makes sense for long-lived local
services.

Hard MVP requires only:

- portable profile application where possible,
- current OS-specific soft-hardening layer,
- no module access to host private keys or ambient settlement authority,
- explicit environment shaping owned by the host.

The module must never receive host signing keys directly as part of supervision.

### 11. Component Integration

The daemon should expose supervised middleware services as first-class components,
for example:

- `middleware.dator`
- `middleware.arca`

That component identity should support:

- status listing,
- health inspection,
- start,
- stop,
- restart,
- failure visibility.

This keeps operator tooling coherent with the rest of the daemon instead of creating
one invisible mini-supervisor inside middleware.

### 12. Trace Boundaries

The host should distinguish:

- middleware invocation trace
- middleware service lifecycle trace

Invocation trace already belongs in:

- `trace/middleware`

Lifecycle trace may be stored separately or under a distinct tag set, but it should
remain explicit. A failed readiness probe and a rejected hook invocation are not the
same class of fact.

## Hard MVP Scope

The following should be considered required for the first real rollout:

1. new executor kind `http_local_json`,
2. host-owned process launch,
3. bounded readiness wait,
4. bounded stop and kill fallback,
5. minimal restart policy (`never`, `on_failure`),
6. daemon component exposure,
7. middleware init and module report integration,
8. reuse of existing `WorkflowEnvelope` and `MiddlewareDecision`,
9. reuse of current sandbox-profile surface,
10. stable operator-visible health/state.

The following are explicitly outside the hard MVP:

- Unix domain sockets,
- hot config reload of the child service,
- zero-downtime rolling restart,
- multi-instance pools per executor,
- stream-oriented or SSE middleware responses,
- remote network exposure,
- generalized module registry federation.

## Trade-offs

### Benefits

- long-lived middleware modules become operable without external manual service
  management,
- Dator-like and Arca-like modules gain a natural runtime shape,
- Node keeps lifecycle and security authority instead of outsourcing it to module
  folklore,
- operator tooling can show real module state rather than just request failures,
- the architecture remains stratified:
  - host owns lifecycle,
  - module owns local implementation details,
  - HTTP JSON remains only the invocation surface.

### Costs

- one more executor kind and config family to maintain,
- more daemon lifecycle code,
- more health and failure-state surface to expose and test,
- some duplication with model-runtime `http_local` patterns until shared supervision
  primitives are extracted.

### Risks

- if `http_local_json` grows too many service-manager features, middleware runtime
  becomes an accidental orchestrator,
- if readiness and restart semantics are underspecified, operators will still see
  flapping and unclear states,
- if init/report is skipped, supervised modules remain opaque despite richer
  lifecycle.

## Failure Modes and Mitigations

### 1. Child process never becomes ready

Mitigation:

- bounded startup timeout,
- explicit `failed` state,
- startup error recorded in operator-visible component details.

### 2. Child process flaps repeatedly

Mitigation:

- bounded restart budget,
- terminal `failed` state after restart exhaustion,
- explicit manual restart required afterward.

### 3. Module responds but violates middleware decision contract

Mitigation:

- schema-gate and Rust-level validation still apply,
- invalid module output is treated as executor failure,
- host remains semantic authority.

### 4. Module leaks from intended trust boundary

Mitigation:

- host-owned sandbox profile,
- no private key handoff,
- no ambient settlement authority,
- loopback-only HTTP expectation.

### 5. Operator cannot tell whether failure is lifecycle or invocation

Mitigation:

- separate lifecycle state from per-hook trace,
- distinct component health and trace facts.

## Open Questions

1. Should the first MVP config allow the child to bind an ephemeral port and report
   it back, or should MVP require a fixed configured endpoint?
2. Should `middleware-init` use the same invoke endpoint with a typed envelope, or
   should it use a dedicated module-lifecycle path?
3. Should the future daemon extract one shared local-service supervisor usable by
   both model-runtime `http_local` and middleware `http_local_json`?
4. Which lifecycle facts deserve their own persisted stream instead of just component
   status snapshots?
5. Should supervised middleware services participate in daemon preflight checks when
   their executable or working directory is missing?

## Next Actions

1. Add one implementation-side memo or README note in the Node workspace aligning
   middleware supervision with the existing `http_local` model-runtime pattern.
2. Add a typed runtime contract in the Node middleware-runtime crate for
   `http_local_json`.
3. Add daemon-owned supervised component lifecycle for that executor kind.
4. Package `Orbiplex Dator` and `Orbiplex Arca` as bundled Python middleware
   modules distributed with Node.
5. Bind middleware init and module report into the supervised startup path.
6. Expose the new component state in existing control-plane component listings and
   health surfaces.
7. Add integration tests for:
   - startup success,
   - readiness timeout,
   - restart budget exhaustion,
   - clean shutdown,
   - invalid module decision responses,
   - bundled Dator and Arca startup under supervised `http_local_json`.
