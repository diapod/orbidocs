# Proposal 071: Sensorium Workbench

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`

## Status

Accepted / partial implementation foundation.

The settled solution surface is promoted to
`doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`.
This proposal remains the rationale, design history, resolved-decision log, and
implementation tracker for Workbench. The promoted solution component owns the
current solution-level responsibility boundary.

## Date

2026-06-23

## Executive Summary

Orbiplex will eventually need model-assisted workflows that can inspect and
shape local software environments: run commands, observe terminal output, read
bounded file snapshots, propose patches, apply approved changes, and operate
inside disposable sandboxes. This is the capability class usually associated
with LLM-managed agents.

In Orbiplex, the model must not become the commander of the node. Inquirium is
the model inquiry organ. It may produce plans, command proposals, patch
proposals, interpretations, and next-step candidates. The actual actuation
surface belongs to Sensorium and remains host-authorized.

This proposal defines **Sensorium Workbench** as a specialized Sensorium
connector/runtime for high-impact local workbench actuation:

```text
Inquirium thinks.
Host authorizes.
Sensorium acts.
Workbench brokers terminal, filesystem, and sandbox effects.
```

Sensorium Workbench is not a new organ and not an Inquirium adapter. It is a
Sensorium connector class, supervised like other middleware, with explicit
capability groups for terminal sessions, workspace file snapshots, patch
application, artifact exchange, and sandbox environments.

The first implementation should be narrow and local-only. It should be a
supervised Workbench connector with its own readiness, lifecycle, operator
status, and grants, even if it reuses lower-level Sensorium OS libraries. It
should expose host-brokered terminal and filesystem capabilities over HTTP/JSON
contracts, not direct terminal access to a model. It should be suitable for
JSON-e Flow orchestration and future Inquirium assistant/agent loops, while
preserving grants, leases, classification, audit, idempotency, and operator
control.

Interactivity is part of the contract. Workbench should not force clients to
invent private polling loops, sleep intervals, prompt scraping, or hidden
watcher threads. Waiting for a prompt, checking that a file appeared, detecting
that a command stopped making progress, and observing that an environment is
ready should be expressed as host-brokered waits, watches, probes, and outcomes.
The broker that joins observations across Workbench, Artifact Delivery,
Memarium, approvals, and deferred operations should be a host-owned primitive,
not a private feature of Sensorium Core.

## Context And Problem Statement

Model-assisted development or system investigation needs a loop:

```text
observe environment
ask model for next step
validate proposed action
execute bounded action
observe result
repeat
```

Without a proper local workbench boundary, the system tends toward one of two
bad shapes:

- direct model-to-terminal control, where an LLM or agent runtime owns a shell,
  filesystem, and credential context;
- one-off OS actions hidden inside workflow scripts, where each workflow invents
  its own terminal, file, and sandbox mechanics.

Both shapes complect reasoning, authorization, and actuation. They also obscure
the difference between a model proposing a command and the node actually
running that command.

The existing Sensorium OS connector action classes are deliberately
program-agnostic and mostly one-shot. They are good for bounded actions such as
running an allowlisted script. They are not enough for interactive terminal
sessions, screen snapshots, incremental command loops, workspace file exchange,
or disposable virtual environments.

Interactive work also needs temporal coordination across component boundaries.
A caller often needs to wait until something exists, wait until output becomes
quiet, verify that a child process still lives, detect lack of progress, or
race an expected observation against a deadline. If each component implements
that on its own, the system drifts toward hidden polling, inconsistent timeout
semantics, and unobservable background work.

## Goals

- Define Sensorium Workbench as a specialized Sensorium connector/runtime.
- Keep Inquirium out of direct terminal/filesystem ownership.
- Provide a host-brokered PTY/session contract over HTTP/JSON.
- Provide bounded filesystem snapshot, read, patch, and artifact contracts.
- Support local workspaces and future virtualized sandboxes.
- Make all terminal and filesystem effects grant-bound, lease-bound,
  classified, audited, and operator-visible.
- Provide brokered wait/watch/probe contracts for interactive workflows.
- Support JSON-e Flow and built-in orchestration loops.
- Keep terminal bytes and file contents out of ordinary model traces unless
  explicitly admitted by policy.

## Non-Goals

- This proposal does not define a general-purpose autonomous agent.
- It does not let Inquirium bypass host policy or Sensorium grants.
- It does not replace Sensorium OS one-shot action classes.
- It does not require remote execution, SSH, containers, or VMs in the first
  slice.
- It does not define a public/federated workbench protocol.
- It does not grant network egress, credential access, or arbitrary filesystem
  access by default.
- It does not make PTY transcripts durable facts by default.
- It does not require WebSockets or any specific streaming transport in the
  first slice.
- It does not allow unbounded blocking waits or component-private background
  polling as the normal interaction mechanism.

## Decision

### 1. Workbench Is A Sensorium Connector Class

Sensorium Workbench is a Sensorium connector/runtime role:

```text
Sensorium Core
  owns capability admission, policy, grants, audit, and dispatch

Sensorium Workbench
  owns PTY/session mechanics, workspace filesystem views, patch application,
  local sandbox lifecycle, and artifact handoff
```

It may share low-level libraries with Sensorium OS, but it must have its own
declared capability group, readiness report, operator status, lifecycle
controls, grant surface, and refusal diagnostics. PTY sessions and filesystem
writes have a materially higher risk profile than ordinary read-only
observations or one-shot script invocations, so they must not inherit Sensorium
OS authority by implication.

Implementation MAY begin as an optional capability group inside the existing
Sensorium OS module if that reduces bootstrapping cost, but the public contract
must still name the Workbench boundary separately. Once PTY sessions or writes
are enabled, a separate supervised middleware connector is the preferred
implementation shape.

When the boundary is stable enough to implement, the recommended split is:

- `sensorium-workbench-core`: portable data contracts, state machines,
  validation, path rules, command profiles, and failure classes;
- `sensorium-workbench-service`: PTY/session management, workspace roots,
  patch application, sandbox lifecycle, persistence, and policy evaluation;
- `sensorium-workbench-http`: loopback HTTP mapping, bounded local server
  runtime integration, middleware init/report, and shutdown behavior.

A Python prototype is acceptable only if it follows the same bounded local
server invariants: no unbounded per-request threads, explicit overload
behavior, cooperative shutdown, no hidden residual child processes, and
operator-visible cleanup failures.

Workbench and Sensorium OS must share the lower safety primitives that define
local actuation semantics. The shared lower module may be named
`sensorium-actuation-core` or, if bootstrapped from the existing OS connector
implementation, `sensorium-os-core`, but it must be consumed by both connector
classes. It owns path canonicalization, symlink-escape rejection, command
profile validation, allowlist interpretation, environment policy validation,
classification/sensitivity propagation, argv normalization, and content-digest
helpers. Reimplementing these rules separately in Workbench and Sensorium OS
would create a second vulnerability surface for traversal, argv injection, and
policy drift.

### 2. Inquirium Produces Intent, Not Effects

Inquirium may produce:

- a plan;
- a command proposal;
- a patch proposal;
- a file-inspection request;
- an interpretation of terminal output;
- a next-step candidate.

It must not directly own:

- a PTY;
- a shell process;
- a filesystem root;
- a VM or container;
- credentials;
- network egress.

The normal loop is:

```text
UI / JSON-e Flow / built-in workflow
  -> Inquirium generate/plan operation
  -> host validates model proposal
  -> Sensorium directive to Workbench
  -> Workbench executes bounded local effect
  -> Sensorium records outcome/observation/artifact refs
  -> loop continues
```

An "agent adapter" for a full external agent runtime MAY exist later, including
an MCP-like tool protocol or another tool-calling protocol. That protocol is an
implementation detail below the host grant boundary. The adapter is still just
a supervised runtime that requests host-granted tools. It does not become a
commander and does not bypass Workbench or Sensorium.

### 3. Workbench Uses Declarative Tool Intents

Workbench should distinguish three levels of intent:

- raw terminal input, such as bytes sent to an interactive PTY;
- structured command intent, such as a command profile plus `argv` data;
- structured edit intent, such as a patch artifact or file operation plan.

Model-driven workflows should prefer structured command and edit intents.
Raw terminal input is a high-risk compatibility escape hatch for genuinely
interactive programs, not the normal interface for model-generated actions.

The first contract should therefore expose separate operation classes:

- `terminal.input.command` for host-validated command intent;
- `terminal.input.raw` for bounded raw input to an existing PTY session;
- `files.patch.apply` for approved patch application from an artifact ref.

`terminal.input.command` must avoid shell interpolation. A command request names
an allowlisted command profile and passes arguments as data. The host records a
normalized argv digest before execution, so traces can identify the effect
without storing prompt or terminal content.

Candidate command intent shape:

```json
{
  "schema": "sensorium-terminal-command.v1",
  "schema/v": 1,
  "directive/id": "directive:workbench-20260623-001",
  "correlation/id": "workbench-loop:story009-001",
  "idempotency/key": "idem:workbench-20260623-001",
  "terminal.session/ref": "terminal-session:story009-abc",
  "command.profile/ref": "command-profile:cargo-test",
  "argv": ["cargo", "test", "-p", "orbiplex-node-nse"],
  "cwd": {
    "workspace/ref": "workspace:story009-local",
    "root/ref": "root:repo",
    "relative/path": "node"
  },
  "env": {
    "mode": "profile-defaults-only"
  },
  "limits": {
    "timeout_ms": 120000,
    "stdout_bytes": 65536,
    "stderr_bytes": 65536
  },
  "argv/normalized-sha256": "sha256:..."
}
```

### 4. Terminal Sessions Are Host-Brokered Resources

Workbench exposes terminal sessions as bounded resources, not as raw sockets to
models. A terminal session has:

- `terminal.session/ref`;
- owning component/caller;
- sandbox/workspace binding;
- command profile;
- classification;
- max duration;
- idle timeout;
- max active sessions per connector and per workspace;
- bounded reader task permits;
- input/output queue depth caps;
- input/output byte caps;
- optional approval policy;
- audit/outcome records;
- explicit close semantics.

Terminal lifecycle is explicit:

```text
requested -> starting -> running -> idle -> closing -> closed
                            \-> failed
                            \-> expired
                            \-> killed
```

Session creation, input, resize, signal, and close directives should carry
idempotency keys. Closing a session is idempotent. A cleanup failure is not
hidden behind `closed`; it is an operator-visible degraded state until the host
can confirm that child processes and temporary resources are gone.

PTY sessions must have their own bounded resource contract, separate from the
HTTP server request permits. A Workbench connector declares `sessions/max`,
`sessions/per-workspace-max`, `reader-tasks/max`, `input-queue/max-depth`, and
`event-buffer/max-depth`. When those limits are reached, session creation or
input admission fails fast with an overload/refusal outcome instead of queuing
unbounded reader loops or process handles.

The terminal event stream is append-only:

```json
{
  "schema": "sensorium-terminal-event.v1",
  "schema/v": 1,
  "terminal.session/ref": "terminal-session:story009-abc",
  "correlation/id": "workbench-loop:story009-001",
  "seq/no": 42,
  "event/type": "output",
  "stream": "pty",
  "bytes/encoding": "utf-8",
  "text": "cargo test ...",
  "truncated": false,
  "classification": {
    "schema": "classification.v1",
    "source_tier": "Personal",
    "effective_tier": "Personal",
    "provenance": {
      "kind": "local-space",
      "space": "Personal"
    },
    "bound_subjects": {
      "personal_or_community": [
        {
          "kind": "role",
          "id": "node-operator"
        }
      ]
    },
    "declassify_trail": []
  }
}
```

Terminal events are session-local observations. The authoritative directive
outcome is a separate host audit fact that links caller, grant, directive id,
session ref, status, byte counts, timing, and artifact refs. Raw output becomes
durable only when capture policy stores it as an artifact or classified fact.

The model-facing view should usually be a bounded screen or event snapshot, not
the unbounded raw transcript:

```json
{
  "schema": "sensorium-terminal-screen-snapshot.v1",
  "schema/v": 1,
  "terminal.session/ref": "terminal-session:story009-abc",
  "correlation/id": "workbench-loop:story009-001",
  "seq/from": 30,
  "seq/to": 42,
  "rows": ["$ cargo test", "test result: ok"],
  "cursor": {"row": 2, "col": 16},
  "truncated": false
}
```

### 5. Interactivity Is Brokered As Waits, Watches, And Probes

Interactive workflows need a brokered temporal layer. A component should not
hold a raw socket, sleep for an arbitrary number of seconds, scrape a prompt,
or spawn a private watcher thread just to know whether the world changed.
Workbench should expose interaction primitives as data:

- a `watch` observes an event source from a cursor and returns bounded event
  batches or a stream-compatible cursor;
- a `wait` evaluates a declarative condition against observations until it is
  satisfied, cancelled, expired, or timed out;
- a `probe` actively asks Workbench to check a bounded fact about a resource,
  such as process liveness, environment readiness, file existence, digest
  change, artifact presence, or terminal quiescence.

The useful event sources are:

- terminal session events and screen snapshots;
- terminal command outcomes;
- file snapshot and digest observations;
- artifact admission and export outcomes;
- environment lifecycle changes;
- deferred operation status changes;
- operator approval or revocation events.

The natural long-term owner of inter-component interaction brokerage is a
host-owned interaction-broker primitive: admission, grant checks, wait
registry, cross-source joins, cancellation, operator visibility, and audit.
Sensorium Core may consume this primitive for Workbench-backed flows, but it
must not become the owner of AD, Memarium, approval, or deferred-operation
joins. The Workbench connector owns connector-local observation production and
active probes for resources it controls. A connector may complete a simple
local wait directly, but a wait that spans Workbench, Artifact Delivery,
Memarium, approvals, or deferred operations belongs to the host broker, with
each domain component acting only as an observation source.

Waits and probes must be host-owned resources with refs, deadlines,
classification, idempotency keys, caller identity, grant context, byte caps, and
explicit outcomes. A wait that can outlive one HTTP request must become a
Bounded Deferred Operation. `deferred-operation-status.v1` remains the
canonical lifecycle status model; `interaction-broker-wait.outcome.v1` is the
domain result/projection carried directly by a short synchronous wait or under
`deferred-operation-status.v1.result` for async waits.

Candidate wait request:

```json
{
  "schema": "interaction-broker-wait.request.v1",
  "schema/v": 1,
  "wait/ref": "wait:story009-command-ready",
  "correlation/id": "workbench-loop:story009-001",
  "idempotency/key": "idem:wait-story009-command-ready",
  "scope": {
    "terminal.session/ref": "terminal-session:story009-abc"
  },
  "condition": {
    "kind": "terminal.quiescent",
    "after.seq/no": 42,
    "quiet_ms": 750,
    "require_process_alive": true
  },
  "deadline_ms": 10000,
  "on_timeout": "return-not-kill"
}
```

Candidate wait outcome:

```json
{
  "schema": "interaction-broker-wait.outcome.v1",
  "schema/v": 1,
  "wait/ref": "wait:story009-command-ready",
  "correlation/id": "workbench-loop:story009-001",
  "condition/status": "satisfied",
  "observed": {
    "terminal.session/ref": "terminal-session:story009-abc",
    "seq/from": 42,
    "seq/to": 48
  },
  "duration_ms": 1180,
  "classification": {
    "schema": "classification.v1",
    "source_tier": "Personal",
    "effective_tier": "Personal",
    "provenance": {
      "kind": "local-space",
      "space": "Personal"
    },
    "bound_subjects": {
      "personal_or_community": [
        {
          "kind": "role",
          "id": "node-operator"
        }
      ]
    },
    "declassify_trail": []
  }
}
```

For an async wait, the host returns and polls the canonical deferred status
shape:

```json
{
  "schema": "deferred-operation-status.v1",
  "schema/v": 1,
  "status": "completed",
  "operation/id": "deferred:interaction-broker.wait:story009-command-ready",
  "operation/kind": "interaction-broker.wait",
  "updated_at": "2026-06-23T12:00:00Z",
  "result": {
    "schema": "interaction-broker-wait.outcome.v1",
    "schema/v": 1,
    "wait/ref": "wait:story009-command-ready",
    "correlation/id": "workbench-loop:story009-001",
    "condition/status": "satisfied"
  }
}
```

Conditions should be declarative and bounded. The first set should cover:

- `terminal.output.since`: new output exists after a sequence number;
- `terminal.quiescent`: no new output for a stable window;
- `terminal.command.done`: a command outcome exists;
- `terminal.process.alive`: the session process is still alive;
- `terminal.no_progress`: no output, progress marker, or state change for a
  policy-defined interval;
- `file.exists`: a relative path exists under a root;
- `file.digest.changed`: a path digest differs from an observed digest;
- `artifact.present`: an artifact ref has been admitted;
- `environment.ready`: an environment reached `ready`;
- `operation.done`: a deferred operation reached a terminal status.

The MVP should keep each wait scoped to one primary resource. Multi-resource
conditions should be expressed as host-side composition of smaller waits until
there is a clear need for a dedicated join contract.

Silence is not automatically a hang. Hang detection needs a policy-defined
progress model: expected event cadence, quiet window, max idle interval, process
liveness, and optional probes. A terminal session may be alive and quiet
because the command is computing, waiting for input, or blocked. Workbench can
report `maybe_hung`, `waiting_for_input`, `no_progress`, or `probe_failed`, but
the host policy decides whether to continue, ask the operator, send input,
cancel, or kill.

Watch cursors and wait refs should be replayable for a bounded retention
window. This lets a JSON-e Flow, UI, or Inquirium loop resume after a transient
component restart without losing the causal edge between "I asked for this
effect" and "this observation satisfied the next step".

### 6. Filesystem Access Is Lease And Snapshot Based

Workbench must not expose "the disk" as an ambient filesystem. It exposes:

- allowlisted workspace roots;
- canonical path validation;
- file and directory snapshots;
- bounded reads;
- patch proposals;
- approved patch application;
- artifact reads/writes through host object-store or artifact refs;
- provenance linking each write to operation, caller, policy, and session.

The filesystem address model should be host-owned and relative:

```text
workspace/ref
path-space/ref
root/ref
relative/path
```

The connector canonicalizes `root/ref + relative/path` before every access,
rejects traversal, rejects NUL bytes, rejects empty paths where a file is
required, and rejects symlink escape outside the allowlisted root. A direct
`file://...` value received from a model or external agent is not authority.
If a direct data-plane lease is needed, the host translates it into a scoped
lease only after canonical validation, classification, expiry, and runtime or
operation binding.

Snapshots are metadata observations. They may reveal names, sizes, digests, and
classifications, but they do not grant byte reads by themselves. Bounded file
reads are separate directives, and writes should normally flow through patch
application or artifact admission rather than ad hoc overwrite calls.

The model should receive file snapshots or selected excerpts. It should return
patch proposals or edit intentions. Applying a patch is a Workbench directive
under host policy.

Example patch request:

```json
{
  "schema": "sensorium-workbench.patch-apply.request.v1",
  "schema/v": 1,
  "workspace/ref": "workspace:story009-local",
  "correlation/id": "workbench-loop:story009-001",
  "patch/ref": "artifact:sha256:...",
  "target/root": "root:repo",
  "policy": {
    "require_clean_apply": true,
    "allow_create": true,
    "allow_delete": false,
    "max_changed_files": 12
  }
}
```

### 7. Sandboxes Are Workbench Environments

Workbench can start with host-local workspaces. Future `Sensorium Virt` can
implement the same environment contract using containers, microVMs, emulators,
or remote disposable machines.

The stable abstraction is the environment:

```text
workspace/ref
sandbox/ref
terminal.session/ref
artifact/ref
data-lease/ref
```

Environment lifecycle is explicit:

```text
allocating -> ready -> draining -> closed
                    \-> failed
                    \-> expired
```

The first implementation should support only host-local allowlisted workspaces.
Future virtualized backends must not change the Workbench contracts. They only
provide different interpreters for the same environment, terminal, file,
artifact, and teardown abstractions.

Backends are implementation choices:

- host-local directory;
- temporary copied workspace;
- container;
- VM;
- remote disposable environment;
- simulated fixture environment.

The backend must declare:

- locality;
- network policy;
- filesystem roots;
- credential policy;
- teardown policy;
- artifact export policy;
- resource limits.

### 8. HTTP Is The Middleware Transport, Not The Domain

Components communicate through the existing host/middleware style. Workbench may
expose local HTTP endpoints to Sensorium Core, but the domain contract is
Sensorium capability data, not ad hoc HTTP semantics.

These endpoints are connector-private loopback surfaces. Ordinary components,
JSON-e flows, Inquirium adapters, and UI clients should consume Sensorium host
capabilities or `sensorium.directive.invoke` actions instead of dialing the
Workbench connector directly.

Candidate local endpoints:

```text
POST /v1/sensorium/workbench/terminal-sessions
GET  /v1/sensorium/workbench/terminal-sessions/{session_ref}
POST /v1/sensorium/workbench/terminal-sessions/{session_ref}/commands
POST /v1/sensorium/workbench/terminal-sessions/{session_ref}/raw-input
POST /v1/sensorium/workbench/terminal-sessions/{session_ref}/resize
POST /v1/sensorium/workbench/terminal-sessions/{session_ref}/signal
GET  /v1/sensorium/workbench/terminal-sessions/{session_ref}/events
POST /v1/sensorium/workbench/terminal-sessions/{session_ref}/close

POST /v1/sensorium/workbench/files/snapshot
POST /v1/sensorium/workbench/files/read
POST /v1/sensorium/workbench/patches/apply

POST /v1/sensorium/workbench/watches
GET  /v1/sensorium/workbench/watches/{watch_ref}/events
POST /v1/sensorium/workbench/watches/{watch_ref}/close
POST /v1/sensorium/workbench/waits
GET  /v1/sensorium/workbench/waits/{wait_ref}
POST /v1/sensorium/workbench/probes

POST /v1/sensorium/workbench/environments
GET  /v1/sensorium/workbench/environments/{sandbox_ref}
POST /v1/sensorium/workbench/environments/{sandbox_ref}/close
```

The first Python connector slice intentionally exposes narrower loopback-private
paths such as `/v1/workbench/file/read` and a mediated
`/v1/sensorium/connector/invoke` entrypoint. The `/v1/sensorium/workbench/...`
shape above is the host/Sensorium-facing projection to keep stable as daemon
grant routing matures; it is not permission to bypass Sensorium Core by dialing
connector-local HTTP from flows, UI clients, or Inquirium adapters.

Those paths are loopback-private connector surfaces. They are not public node APIs and
MUST bind through the bounded local server runtime only. Host/module authentication is
still required because loopback is not authority.

| Endpoint family | Capability id | Required grant / caller posture |
|---|---|---|
| terminal session create/read/close | `sensorium.workbench.terminal` | Explicit Workbench terminal grant; operator-approved by default. |
| structured terminal command | `sensorium.workbench.terminal` | Directive grant plus command profile admission; generated commands use argv data, not shell interpolation. |
| raw terminal input / signal / resize | `sensorium.workbench.terminal` | Operator-only in MVP. |
| terminal events / screen snapshots | `sensorium.workbench.terminal` | Read grant scoped to session ref and classification. |
| terminal capture to artifact | `sensorium.workbench.terminal` + `sensorium.workbench.patch` | Terminal grant scoped to the session plus artifact-write grant; capture persists state and is not a read-only terminal action. |
| file snapshot/read | `sensorium.workbench.file` | Bounded read grant scoped to workspace/root/path lease. |
| patch apply | `sensorium.workbench.patch` | Write/patch grant plus digest/provenance checks; operator approval unless an explicit lease allows auto-apply. |
| watches | `interaction-broker.watch` | Host broker grant scoped to observation source, cursor window, TTL, and classification. |
| waits | `interaction-broker.wait` | Host broker grant scoped to observation source, deadline, and idempotency key. |
| operation status | `interaction-broker.wait` | Status reads require an explicit wait grant; possession of an operation id is not authority. |
| probes | `interaction-broker.probe` | Host broker grant scoped to target source and diagnostic purpose. |
| environment create/read/close | `sensorium.workbench.env` | Environment grant scoped to backend, roots, teardown policy, and resource caps. |

Sensorium Core may wrap these as `sensorium.directive.invoke` actions so
ordinary consumers do not need to speak directly to the connector.

Streaming is an optimization, not the semantic contract. The same watch/wait
contract should work through polling, bounded long-polling, server-sent events,
or a future bidirectional local channel. The stable semantics are refs, cursors,
deadlines, backpressure, caps, and terminal outcomes.

### 9. Approval And Autonomy Levels

Workbench is a high-impact actuator. Default posture:

- read-only snapshots may be allowed under a bounded read grant;
- terminal creation requires explicit workbench grant;
- terminal input that runs a command is a directive;
- filesystem writes require explicit write grant;
- patch application requires write grant and may require operator approval;
- network egress is denied unless the environment policy explicitly allows it;
- credential access is denied unless a separate sealed secret grant exists;
- destructive operations require a stronger approval profile.

Authority should be separated by effect class:

| Layer | May produce | May approve | May execute |
| --- | --- | --- | --- |
| Inquirium model | Plans, command intents, patch intents, explanations | no | no |
| JSON-e Flow / built-in workflow | Structured directives and policy context | only when granted by host policy | no |
| Host / Sensorium Core | Final directive, grant decision, idempotency key | yes | dispatch only |
| Workbench connector | Bounded local effect outcome | no | yes, within directive |
| Operator | Manual approval, revocation, emergency stop | yes | through host controls |

Autonomy levels should be expressed by policy, not by model identity. The same
model output may be:

- advice-only;
- proposed command requiring approval;
- automatically executable in a disposable sandbox;
- automatically executable in a local workspace under narrow allowlists.

P072 continuation note: this section seeded the first implemented
authorization-policy-as-data slice. `capability-authorization-policy.v1` now
projects the Workbench and Interaction Broker grant/posture/approval/autonomy
rows into registry-consumable policy sidecar data, while `capability-registry.v1`
remains the source for capability identity and eligibility.

### 10. Trace And Memory

Workbench traces must be useful without leaking unnecessary content.

Trace records should include:

- caller;
- `correlation/id` threading directive, events, wait outcome, artifacts, and
  next directive;
- session ref;
- workspace/sandbox refs;
- operation class;
- command digest and argv metadata;
- file refs and digests;
- result status;
- duration;
- byte counts;
- policy decisions;
- artifact refs;
- approval refs;
- watch/wait/probe refs;
- condition kind and normalized condition digest;
- deadline, timeout, cancellation, and progress status.

Raw terminal output and file contents should not be written into generic traces
by default. If captured, they should be artifacts or Memarium facts under an
explicit classification and retention policy.

This follows the broader Orbiplex pattern: an ephemeral observation is not a
durable fact. A live terminal transcript, like a live room chat or an
intermediate reasoning exchange, is operational context until a host policy
explicitly captures, classifies, and admits it as an artifact or fact.

Workbench should reuse existing host-owned runtime primitives instead of
creating private equivalents:

- Bounded Deferred Operations for long-running environment creation, test runs,
  indexing, batch edits, and other operations that outlive one HTTP request;
- Replay Scheduler for bounded periodic probes, maintenance watches, and
  policy-owned rechecks that must survive one immediate interaction loop;
- Artifact Delivery for moving patch artifacts, captured logs, build outputs,
  screenshots, and export bundles between components;
- Memarium for classified summaries or operator-approved durable observations;
- Host-Owned Module Store for installing and activating Workbench connector
  packages, tool profiles, and future backend modules.

Process termination is never broker-owned. When a wait or probe reports `maybe_hung`,
timeout, or no progress, the Interaction Broker emits the diagnostic outcome only; the
Workbench connector or operator decides whether to cancel, signal, kill, ask the user,
or keep observing.

### 11. Relationship To Existing Sensorium OS

Sensorium OS remains the generic OS action connector for allowlisted one-shot
actions. Sensorium Workbench is for interactive or workspace-shaped action:

| Capability | Sensorium OS | Sensorium Workbench |
| --- | --- | --- |
| One-shot read-only process | primary | possible |
| Allowlisted script | primary | possible |
| Interactive PTY | no | primary |
| Screen/event snapshots | no | primary |
| Workspace file snapshot | limited | primary |
| Patch apply | no or narrow | primary |
| Disposable sandbox | no | primary/future |
| Agent loop support | indirect | primary actuator |

Workbench does not replace Sensorium OS. It provides a stricter, more
observable boundary for effects that are too stateful for the one-shot action
catalog.

The first Workbench implementation should be independently shippable before any
Inquirium agent loop exists. JSON-e Flow, operator UI, and direct Sensorium
directives are sufficient to validate the actuator boundary, resource caps,
wait/watch/probe semantics, and audit behavior.

### 12. Relationship To Agent Adapters

A future Inquirium adapter may wrap a whole agent runtime, including an MCP-like
tool protocol. That adapter may be useful, but it must still call host-granted
tools. Tool execution remains outside the adapter:

```text
agent runtime
  -> requests terminal/file/sandbox tool
  -> host policy gate
  -> Sensorium Workbench directive
  -> audited effect
```

If an agent runtime has its own terminal/filesystem access that bypasses
Workbench, it is not an acceptable Inquirium adapter for Orbiplex Node.

Corpus or room-deliberation experts may later use Workbench as an actuation
surface for grounded reasoning, such as running a test or inspecting a local
artifact during deliberation. That use remains mediated by host policy:
deliberation proposes the act, Workbench executes only after Sensorium grants,
and the resulting observation is not a durable fact unless admitted.

## Storage And Recovery Contract

Workbench and the host Interaction Broker are stateful enough to require the
same store discipline as other daemon-owned ledgers. Any session, wait, watch,
probe, sandbox, approval, idempotency, or cleanup store must follow the Temporal
Storage Convention / Storage and Database Schema Design contract: explicit
`user_version` migrations, WAL-oriented pragmas where SQLite is used,
`busy_timeout`, foreign keys where relationships exist, stable idempotency keys,
bounded retention, and replay or projection diagnostics. Short-lived caches may
remain disposable, but the decision to make a store disposable must be explicit.

The first daemon implementation should use two separate stores so that local
actuation lifecycle and horizontal coordination do not become one accidental
database:

- `<data-dir>/storage/sensorium-workbench.sqlite` for Workbench-owned sessions,
  command intents, terminal events metadata, workspace roots, patch attempts,
  cleanup records, and idempotency decisions;
- `<data-dir>/storage/interaction-broker.sqlite` for host-owned waits, watches,
  probes, cursor bindings, source refs, deadlines, final outcomes, and
  idempotency decisions.

Both stores are metadata-first. They must not store raw terminal transcripts,
file contents, prompts, credentials, or source blobs by default. Large or
sensitive bytes move through classified artifact/object-store handles or through
explicit capture facts with retention policy.

Minimum Workbench tables or equivalent records:

- `environments`: `environment/ref`, workspace refs, root refs, backend,
  status, classification digest, limits digest, cleanup status;
- `terminal_sessions`: `terminal.session/ref`, environment ref, command profile
  ref, state, caps digest, last event sequence, opened/closed timestamps;
- `terminal_events`: session ref, sequence number, event kind, byte count,
  optional byte digest/ref, status, classification digest, retention class;
- `command_intents`: command id, session ref, idempotency key, normalized argv
  digest, cwd address, timeout, outcome ref;
- `file_snapshots` and `patch_attempts`: metadata, digests, artifact refs, and
  refusal/apply diagnostics;
- `cleanup_records`: previous process generation, discovered resource, action
  taken, terminal cleanup status.

Minimum Interaction Broker tables or equivalent records:

- `broker_sources`: source kind, source ref, provider component, classification
  digest, retention window;
- `watches`: watch ref, source ref, cursor, TTL, caps, idempotency key, status;
- `waits`: wait ref, source ref, condition digest, deadline, idempotency key,
  deferred operation id, condition status, final outcome digest/ref;
- `probes`: probe ref, source ref, condition digest, timeout, idempotency key,
  outcome digest/ref;
- `cursor_replay`: source ref, sequence/cursor, event digest/ref, retained until;
- `recovery_records`: previous generation resources and explicit recovery
  outcomes.

Daemon restart recovery is part of the safety contract, not an operator
afterthought. On startup the Workbench runtime must run one authoritative
recovery sweep before accepting new PTY, file, patch, or environment requests:

1. enumerate runtime-owned child processes, PTY sessions, reader tasks,
   temporary workspace/sandbox roots, active waits, and watch cursors from the
   previous process generation;
2. terminate or quarantine residual child processes and PTY resources using the
   connector's cleanup policy;
3. remove or quarantine temporary roots that are not explicitly retained by
   policy;
4. mark interrupted sessions, waits, watches, and probes as `failed-retryable`,
   `failed`, or `degraded` according to the persisted state and cleanup outcome;
5. append metadata-only recovery facts and expose cleanup failures in operator
   status.

This mirrors the Artifact Delivery recovery rule: a previous-process `running`
state is not silently trusted after restart. There is one source of truth for
recovery state, and no hidden background shell is allowed to survive merely
because the daemon crashed. Recovery status values should be boring and
operator-readable: `recovered`, `terminated`, `quarantined`,
`failed-retryable`, `failed-permanent`, `expired`, and `unknown`.

## Trade-offs

| Choice | Benefit | Cost / constraint |
| --- | --- | --- |
| Workbench as Sensorium connector, not Inquirium adapter | Preserves the organ boundary: models propose, Sensorium acts. | Requires one more host-routed step in agent-like loops. |
| Structured command intents before raw PTY input | Easier policy checks, idempotency, traces, replay, and tests. | Some interactive programs need a raw-input escape hatch later. |
| Snapshot/lease-based filesystem model | Avoids ambient disk authority and keeps path validation host-owned. | More explicit plumbing for file reads and patch workflows. |
| Host-owned brokered waits, watches, and probes | Makes interactive coordination visible, bounded, replayable, and testable across components without coupling Sensorium to every domain source. | Adds a small temporal contract layer before richer agent loops feel natural. |
| Shared actuation core for OS and Workbench | Reduces traversal, argv injection, allowlist, and classification drift. | Requires extracting safety primitives instead of copying code into the new connector. |
| Host-local first slice | Delivers useful developer workflows quickly. | Does not yet isolate arbitrary code as strongly as containers or VMs. |
| Metadata traces by default | Reduces prompt, terminal, secret, and source-code leakage. | Debugging deep agent failures may require explicit capture artifacts. |
| Reuse host-owned primitives | Keeps lifecycle, artifacts, and deferred work consistent across components. | Workbench implementation must integrate with existing registries instead of inventing local shortcuts. |

## Failure Modes And Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Model output is treated as authority. | Require host validation and Sensorium grants before every Workbench directive. |
| Command text is executed through shell interpolation. | Use command profiles and `argv` data for model-driven commands; reserve raw input for approved interactive sessions. |
| Path traversal or symlink escape reaches outside the workspace. | Canonicalize every path under `root/ref + relative/path`; reject traversal, NUL bytes, empty invalid paths, and symlink escape. |
| PTY output leaks secrets into generic traces. | Store only metadata by default; capture raw bytes only as classified artifacts or facts. |
| Long-running process survives session close. | Make cleanup part of the state machine; report degraded cleanup failures to operator status. |
| Daemon restarts while PTY sessions or sandboxes are active. | Run a startup recovery sweep that terminates or quarantines residual child processes, reader tasks, PTY resources, and temporary roots before accepting new Workbench requests. |
| Workflow blocks on a long-running operation. | Use Bounded Deferred Operations for work that can outlive one HTTP request. |
| Client invents private polling or watcher loops. | Provide host-owned watch/wait/probe refs with deadlines, cursors, caps, and outcomes. |
| Quiet terminal is misclassified as hung. | Separate `quiescent`, `waiting_for_input`, `no_progress`, `maybe_hung`, and `probe_failed` states under policy. |
| Watch cursor is lost during component restart. | Keep bounded replay windows and explicit cursors for watch sources. |
| Event producer overwhelms a consumer. | Enforce byte/event caps, cursor windows, truncation markers, and backpressure/overload status. |
| Wait outcome overwhelms deferred-operation consumers. | Bound `observed` and `diagnostics` by schema shape and by host-owned serialized byte/count caps before projection into `deferred-operation-status.v1`. |
| Agent adapter bypasses Sensorium tools. | Reject adapters that own their own terminal/filesystem authority outside host grants. |
| Workbench grows into a second orchestration core. | Keep Workbench as an actuator: no policy selection, no model routing, no workflow ownership. |

## Adversarial Actuator Test Matrix

This matrix is a release gate for any Workbench runtime that can write files,
spawn PTYs, apply patches, create sandboxes, or expose brokered waits across a
process boundary. The cases must be encoded as golden vectors in
`sensorium-actuation-core` and run by both the Rust Workbench implementation and
Python Sensorium OS conformance tests. The required posture is refusal-first:
every negative vector must fail before the corresponding runtime surface can be
enabled by default.

| Class | Required negative or stress cases |
| --- | --- |
| Path validation | Reject `..`, absolute paths, empty paths where a file is required, NUL bytes, symlink escape, root self-access when a file is required, and path-space/root mismatch. |
| Command intent | Reject shell strings, argv injection through profile escape, unknown command profile, cwd outside root, env override outside policy, timeout above max, and output cap overflow. |
| PTY lifecycle | Enforce `sessions/max`, per-workspace session caps, reader task caps, input queue caps, idle timeout, TTL expiry, close idempotency, and overload refusal. |
| Network and credentials | Deny egress, keychain, SSH agent, browser profile, clipboard, desktop automation, and sealed secret access without explicit future grants. |
| Cleanup | Surface residual child processes, failed process kill, leaked temporary roots, and sandbox teardown failure as operator-visible degraded states. |
| Idempotency and replay | Replaying session create, command intent, wait, probe, close, and patch apply with the same idempotency key must not duplicate effects. |
| Interaction broker | Reject waits without scope, waits extending beyond grant expiry, unbounded deadlines, lost cursor replay outside retention, and cross-source waits not owned by the host broker. |
| Artifact and patch | Reject digest mismatch, size mismatch, patch outside root, dirty apply when clean apply is required, unexpected delete, and artifact admission without provenance. |

## Candidate Data Contracts

Every top-level Workbench artifact should carry both `schema` and `schema/v`.
Embedded `classification.v1` labels keep the existing classification-family
shape: `schema`, `source_tier`, `effective_tier`, `provenance`,
`bound_subjects`, and `declassify_trail`, without `schema/v`.

| Schema | Purpose |
| --- | --- |
| `sensorium-workbench-environment.v1` | Declares workspace/sandbox backend, roots, locality, egress, credentials, teardown. |
| `sensorium-terminal-session.v1` | Session descriptor: command profile, workspace, classification, limits, status. |
| `sensorium-terminal-command.v1` | Structured command intent with command profile, argv data, idempotency key, and normalized argv digest. |
| `sensorium-terminal-input.v1` | Bounded raw input event to an existing session. |
| `sensorium-terminal-event.v1` | Append-only output/status event. |
| `sensorium-terminal-screen-snapshot.v1` | Bounded model/UI view over recent terminal state. |
| `interaction-broker-watch.v1` | Cursor-bound subscription over a registered source provider with caps, TTL, and classification. |
| `interaction-broker-wait.request.v1` | Declarative bounded condition over observations, with deadline and idempotency key. |
| `interaction-broker-wait.outcome.v1` | Domain result/projection for a satisfied or terminal wait condition; async lifecycle status is still `deferred-operation-status.v1`. |
| `interaction-broker-probe.v1` | Active bounded check for liveness, readiness, file state, artifact presence, or progress. |
| `sensorium-file-snapshot.v1` | Directory/file metadata snapshot under an allowlisted root. |
| `sensorium-file-read-result.v1` | Bounded file content or artifact ref. |
| `sensorium-workbench-patch.v1` | Patch proposal artifact and metadata. |
| `sensorium-workbench-patch-apply-result.v1` | Applied/rejected patch result with changed files and digests. |
| `sensorium-workbench-outcome.v1` | Host audit fact linking directive id, grant, caller, session/environment refs, status, timing, byte counts, and artifacts. |
| `capability-authorization-policy.v1` | P072 Phase 4 sidecar for per-capability required grants, caller posture, approval mode, autonomy floor, and COI policy for Workbench and Interaction Broker capability ids. |

Phase 0 schema ownership belongs to the Workbench implementation owner. The owner must
publish JSON Schema files and positive/negative examples before any corresponding
cross-process connector route is exposed. Rust DTOs may precede schemas only while they
remain in-process and unwired.

## Security Invariants

- Default deny.
- No ambient terminal.
- No ambient filesystem.
- No shell interpolation for generated commands.
- Workbench and Sensorium OS must use the same lower actuation primitives for
  path canonicalization, command profiles, allowlists, argv normalization, and
  classification/sensitivity propagation.
- Canonical path validation before every file access.
- Writes only under allowlisted workspace roots.
- Network egress denied by default.
- Credentials denied by default.
- Clipboard access, keychain access, SSH agent access, browser profile access,
  desktop automation, and GUI event injection are denied by default and require
  separate future capability contracts.
- Every accepted directive has exactly one outcome record.
- Every wait/watch/probe has explicit scope, deadline or TTL, caps, and final
  lifecycle status.
- A wait must not extend authority beyond the grant that created it.
- PTY sessions, reader tasks, input queues, and event buffers are bounded by
  connector-declared caps.
- Terminal output and file bytes are bounded and classified.
- Long-running sessions have TTL and idle timeout.
- Closing a sandbox tears down processes and temporary storage unless retention
  policy explicitly preserves artifacts.
- Inquirium cannot bypass Workbench by choosing a different model or adapter.

## First Implementation Slice

The first slice should be deliberately small:

1. Add Workbench capability declarations to Sensorium Core.
2. Extract or identify the shared actuation core used by Sensorium OS and
   Workbench for path, command, allowlist, classification, and argv rules.
3. Implement a local-only supervised Workbench connector.
4. Support one environment type: allowlisted host-local workspace.
5. Support terminal session create, structured command intent, events, resize,
   signal, and close with strict limits.
6. Support explicit PTY session, reader-task, queue, and event-buffer caps.
7. Support short synchronous waits for terminal command done, terminal
   quiescence, environment ready, file exists, and artifact present.
8. Support watch cursors for terminal events and deferred operation outcomes.
9. Support file snapshot and bounded read.
10. Support patch apply from artifact ref, with no deletes by default.
11. Add JSON-e Flow examples for observe -> ask Inquirium -> propose command ->
   approve -> execute -> observe.
12. Add operator status showing active sessions, workspaces, waits, watches,
    limits, last outcomes, and suspected no-progress states.
13. Add the adversarial actuator test matrix before enabling write or PTY
    features by default.

The first slice does not need containers, VMs, remote execution, credential
grants, raw terminal input for model-driven commands, or autonomous multi-step
agent loops. It also does not need WebSockets; polling or bounded long-polling
is enough if cursor and outcome semantics are stable.

### Phase Release Gates

Phase 1 may begin only when Phase 0 has frozen schemas/examples for the specific
surfaces being exposed, capability ids are registered, the storage/recovery contract is
documented, and the adversarial matrix has executable golden vectors for path and
command-intent refusal. PTY creation may not be enabled by default until PTY lifecycle,
cleanup, oversized-output, orphan-after-crash, and credential-egress vectors pass.

Phase 2 may begin only when the local connector produces metadata-only outcomes,
operator-visible status, and bounded recovery facts for Phase 1 effects. Sensorium Core
must consume Workbench through grants/directives, not by reaching into connector-local
HTTP details.

Phase 3/4 integration with room, Corpus, or agent loops may begin only after Workbench
has a stable refusal-first conformance suite shared with Python Sensorium OS and after
watch/wait/probe replay semantics are backed by bounded retention.

## Open Questions

No open questions remain for the current local Workbench foundation slice.

## Resolved Decisions

1. **Workbench packaging.** Workbench starts as a separate supervised connector. It may
   reuse Sensorium OS internals, but its operational identity, capability declarations,
   limits, traces, and lifecycle are distinct.
2. **Terminal screen model.** The default LLM-facing terminal observation is a bounded
   viewport snapshot with cursor position and a digest/ref for omitted backlog. It does
   not expose full transcripts unless explicitly captured under a separate policy.
3. **Patch model.** Patch application supports both unified diff and structured edit
   operations. Unified diff remains the human-readable lowest common denominator;
   structured edits exist for machine-authored, schema-checked transformations.
4. **Filesystem writes.** Local filesystem writes require explicit approval by default.
   Writes inside an already granted leased workspace may be auto-allowed only when the
   lease and policy say so; outside that lease, approval remains required.
5. **Terminal-to-Memarium capture.** Terminal sessions create Memarium facts only on
   explicit capture. Outcome summaries are not mirrored automatically.
6. **First sandbox backend.** After host-local workspaces, the first sandbox backend is
   a fixture-only virtual workspace. Containers and microVMs are later substrate
   implementations.
7. **File tree exposure.** Workbench exposes file trees to models through query-style
   leases. A lease is narrower and easier to revoke than a full direct snapshot.
8. **Raw PTY input.** Raw PTY input is operator-only in MVP. Model-driven workflows use
   structured command/file intents, not arbitrary terminal keystrokes.
9. **Command profile completeness.** The first implementation requires executable
   identity, argv schema, cwd policy, env policy, timeout, egress, and output capture
   policy before a command profile can be accepted.
10. **MVP wait conditions.** MVP waits cover process exit, stdout/stderr pattern, file
   exists/changes, and timeout. Component-specific probes can be added later.
11. **Watch replay window.** Local Workbench watch cursors keep a bounded replay window
   by both count and time, with the laptop profile defaulting to 1,000 events or 10
   minutes unless policy overrides it. The eventual watch request schema must carry both
   event/byte caps and a time-window or TTL axis; the broker enforces the narrowest
   applicable bound.
12. **`maybe_hung`.** `maybe_hung` is diagnostic only. It does not automatically create
   operator questions or kill processes.
13. **Interaction Broker status.** The host-owned interaction broker should be promoted
   into its own solution document before Workbench implementation exposes a cross-process
   runtime surface.
14. **Laptop PTY caps.** The default local laptop profile is conservative: 2 active PTY
   sessions, 4 reader tasks, input queue depth 256, and event buffer depth 1,000. These
   caps are policy-configurable.
15. **Async wait diagnostics.** Early async wait diagnostics use
   `deferred-operation-status.v1.extensions`; no separate common wait/probe extension is
   promoted before implementation.
16. **Workbench DTO schema gate.** All candidate Workbench and interaction-broker DTOs
   need JSON Schema projections before the first cross-process boundary is exposed:
   watch request, wait request, wait outcome, probe request, command profile, command
   intent, relative path address, and PTY resource caps.
17. **Timeout termination.** Timeout policy does not authorize kill-on-timeout from the
   host interaction broker. Process termination remains a connector/operator directive
   separate from wait outcome semantics.
18. **Deferred id validation.** The host interaction broker must share the exact
   deterministic-id validator with the deferred-operation registry before cross-process
   broker APIs are exposed. Broker acceptance of an operation-done condition must call
   the deferred-operation validator, not merely check the `deferred:` prefix.
19. **Relative path validation.** Relative path syntax validation moves into a small
   shared utility crate consumed by both `sensorium-actuation-core` and
   `interaction-broker-core`.
20. **Hard-MVP documentation visibility.** Workbench foundation appears in hard-MVP
   implementation docs as a planned post-MVP seed. This keeps the runtime boundary
   visible to implementers without claiming that Workbench itself is part of hard-MVP.
21. **Shared actuation core adoption.** The first implementation keeps Python Sensorium
   OS as a separately audited reference connector and lets Workbench consume
   `sensorium-actuation-core` natively. The shared core is the contract plus golden
   vectors from day zero, not merely the Rust crate. Canonical rules for path
   canonicalization, symlink escape refusal, allowlists, command profiles, and
   classification must be expressed as data/reference rules with golden vectors. The
   Rust `sensorium-actuation-core` carries those vectors as the reference
   implementation; Python Sensorium OS must run the same conformance vectors now,
   without FFI. Direct Python consumption of the Rust core is a tracked later phase,
   adopted only when the FFI/IPC cost is justified.
22. **Capability registration.** The reserved capability ids are
    `sensorium.workbench.terminal`, `sensorium.workbench.file`,
    `sensorium.workbench.patch`, `sensorium.workbench.env`,
    `interaction-broker.wait`, `interaction-broker.watch`, and
    `interaction-broker.probe`. They are registered before runtime work so that
    Workbench and broker authority does not appear as untracked informal module power.
23. **State-store discipline.** Workbench and Interaction Broker stores must follow
    the Temporal Storage Convention / Storage and Database Schema Design contract:
    explicit migrations, WAL-oriented SQLite pragmas, `busy_timeout`, foreign keys,
    idempotency keys, bounded retention, and replay/projection diagnostics.
24. **Restart recovery sweep.** A Workbench runtime must enumerate and terminate or
    quarantine residual child processes, PTY resources, reader tasks, and temporary
    sandbox roots on daemon restart before accepting new requests. Interrupted
    sessions and waits must become explicit failed/degraded records, never invisible
    live residue.
25. **Command profile default-deny.** `allowed_workspace_roots` must be non-empty.
    Empty filesystem authority is a profile error, not a wildcard. Empty
    `allowed_arg_prefixes` means no variable argv atoms are allowed beyond
    executable plus `fixed_args`; it never means allow arbitrary argv.
26. **Command identity admission.** `command/id` may be omitted on incoming
    command intent. The host assigns it when missing, preserves it when present
    and valid, and records the resulting value on `sensorium-terminal-command.v1`
    for correlation and audit.
27. **Empty environment defaults.** Empty strings in
    `EnvPolicy::Allowlisted.defaults` are explicit environment values, not
    unset/clear operations. If Workbench later needs unset semantics, it must
    model them as a separate explicit operation.
28. **Terminal command scope binding.** A broker source provider must validate
    that `TerminalCommandDone.command/id` belongs to the persisted
    `terminal.session/ref -> command/id` relation before accepting the wait
    condition. The host broker validates the generic shape and scope; the source
    provider owns the Workbench-specific binding check.
29. **Host-local workspace root admission.** The first Workbench connector slice
    admits only explicitly configured, absolute, existing directory roots and
    refuses empty paths, relative paths, duplicate `(workspace/ref, root/ref)`
    pairs, and the filesystem root itself. This does not make the connector a
    general filesystem broker; workspace roots remain operator-scoped grants.
30. **Command profile validation source.** The Python Workbench connector keeps
    a deliberately mirrored fail-closed validator in this slice, tightly coupled
    to shared command-profile golden vectors also consumed by
    `sensorium-actuation-core`. A Rust CLI/RPC/FFI validator remains a later
    implementation option, adopted only when the runtime cost and packaging
    surface are justified by evidence.
31. **Terminal capture authorization.** Terminal capture is a terminal read plus
    an artifact write. The session event read requires a
    `sensorium.workbench.terminal` grant scoped to the session, while the
    persisted capture artifact requires a separate `sensorium.workbench.patch`
    artifact-write grant. Capability reports may use the patch capability as
    the primary persisted-effect capability, but handlers must enforce both
    sides.
32. **Connector idempotency admission.** Connector-mediated probes, watches,
    waits, terminal mutations, terminal capture, artifact writes, and patch
    apply must carry a valid `idempotency/key`. The first local implementation
    enforces presence at the connector boundary and de-duplicates async waits by
    this key; broader host-issued replay tokens remain a later host-broker
    layer.
33. **Operation status authorization.** Deferred operation status is not public
    by operation id. Status reads require an explicit capability grant for the
    relevant operation family, with the local Workbench wait pilot using
    `interaction-broker.wait`.

## Next Actions And Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Phase 0 - Contract Freeze

- [x] Decide whether first implementation is a separate Workbench connector or
  an optional capability group inside Sensorium OS. Decision: separate supervised
  Workbench connector.
- [x] Promote the host-owned interaction broker into a separate solution before
  implementation exposes a cross-process runtime surface. Solution 035 now
  defines Interaction Broker as a horizontal host primitive; the initial unwired
  Rust foundation exists in `node/interaction-broker-core`.
- [x] Define the shared actuation core boundary consumed by Sensorium OS and
  Workbench. Initial unwired Rust foundation exists in
  `node/sensorium-actuation-core`. Decision for this slice: keep Python as a
  deliberately mirrored validator, but bind it tightly to shared golden vectors.
  Rust and the Python Workbench connector now both consume the relative-path and
  command-profile golden vectors; direct FFI/RPC consumption remains a later
  tracked stability step rather than the first boundary.
- [x] Define `sensorium-workbench-environment.v1`.
- [x] Define terminal session/command/raw-input/event/snapshot schemas. The accepted
  terminal observation model is a bounded viewport snapshot with cursor and backlog
  digest/ref.
- [x] Define watch/wait/probe schemas, status values, cursor rules, and timeout
  semantics. The initial host-owned watch/wait/probe contract lives in
  `node/interaction-broker-core`, including bounded caps, deadlines,
  correlation ids, no-progress vocabulary, deferred-operation projection, and
  source-provider validation for persisted `terminal.session/ref -> command/id`
  bindings, plus published JSON Schemas/examples.
- [x] Require `schema` and `schema/v` on every top-level Workbench schema while
  preserving embedded `classification.v1` as schema-only.
- [x] Assign Phase 0 schema ownership and publish JSON Schema files plus
  positive/negative examples before exposing any corresponding cross-process connector
  route.
- [x] Define file snapshot/read and patch apply schemas. Patch apply supports both
  unified diff and structured edit operations.
- [x] Define operator-visible status fields and audit outcome shape.
- [x] Define the Workbench/Interaction Broker storage contract and startup recovery
  sweep. Stores must use explicit migrations, WAL-oriented SQLite pragmas,
  `busy_timeout`, foreign keys where applicable, idempotency keys, and
  metadata-only recovery facts; restart recovery must kill or quarantine orphan
  PTY/child processes and temp roots before new requests are admitted.
- [x] Define command profile fields and normalized argv digest rules. The
  initial unwired contract lives in `node/sensorium-actuation-core`, including
  argv-as-data validation, environment policy, timeout/output caps, workspace
  root policy, default-deny workspace roots, empty-prefix-as-no-variable-argv,
  host assignment or preservation of valid `command/id`, explicit empty
  environment defaults, canonical JSON argv digest, and published
  schema/examples.
- [x] Define `correlation/id` threading across directive, events, wait outcome,
  artifacts, and next directive.
- [x] Define async wait status as `deferred-operation-status.v1` with Workbench
  wait outcome as the result projection, not as a parallel status model.
  `node/interaction-broker-core` contains the conversion helper and consumes the
  shared deferred-operation id validator. Wait outcomes are bounded by host
  serialized byte/count caps before projection; host registry integration is
  still not wired.
- [x] Decide MVP policy for raw PTY input. Decision: operator-only in MVP.
- [x] Decide MVP wait conditions and no-progress vocabulary. MVP waits cover process
  exit, stdout/stderr pattern, file exists/changes, and timeout; `maybe_hung` is
  diagnostic only.
- [~] Define the adversarial actuator test matrix as a required acceptance
  suite. The matrix is now specified as a refusal-first release gate and must be
  encoded as `sensorium-actuation-core` golden vectors plus Python Sensorium OS
  conformance tests before write/PTY runtime surfaces are enabled. Initial
  relative-path and command-profile golden vectors are published and consumed by
  Rust and the Python Workbench connector tests; they reject traversal, embedded
  current-directory components, trailing slash forms, backslash separators,
  missing fixed argv prefixes, disallowed executables, and variable argv atoms
  outside explicit allowlisted prefixes.
- [~] Enforce the Phase Release Gates before Phase 1+ runtime work: frozen schemas for
  exposed surfaces, registered capabilities, documented storage/recovery contract, and
  executable refusal-first golden vectors for the relevant effect classes.
- [ ] Track later direct Python Sensorium OS consumption of `sensorium-actuation-core`
  through binding/RPC only after the Rust core and conformance vectors prove stable.

### Phase 1 - Local Workbench Connector

- [x] Add a supervised local Workbench connector module. Node now ships the
  opt-in `middleware-modules/sensorium-workbench` Python connector with
  `/healthz`, `/readyz`, `/shutdownz`, `/v1/middleware/init`, status/config,
  factory config, and daemon factory/inventory coverage. It uses
  `seed_config: false` and remains disabled until an operator configures it.
- [x] Consume the shared actuation core instead of reimplementing path,
  command-profile, allowlist, classification, and argv rules. The current
  connector follows the same conservative path/refusal semantics in Python and
  is tested against shared relative-path and command-profile golden vectors plus
  traversal, root-self, symlink-traversal refusal, oversized reads, dangerous env
  stripping, and command-profile denial. This is the accepted first implementation
  shape: a mirrored Python validator tightly coupled to golden vectors; direct
  binding/RPC to the Rust core remains a later stability step.
- [x] Implement host-local allowlisted workspace environment. The connector
  exposes configured `workspace_roots` as
  `sensorium-workbench-environment.v1`; missing, unavailable, relative,
  duplicate, empty, or filesystem-root workspace roots make `/readyz` fail
  closed with typed diagnostics.
- [x] Implement terminal session create/commands/events/resize/signal/close.
  The opt-in Python Workbench connector now creates bounded terminal sessions,
  spawns structured argv commands through a PTY without shell interpolation,
  admits variable arguments only through explicit `allowed_argv_prefixes`,
  hard-denies dangerous environment override keys, records terminal events in
  SQLite, exposes event cursors, and supports resize/signal/close under explicit
  terminal grants. Factory config keeps the runtime disabled until an operator
  sets `terminal_enabled: true` and provides command profiles.
- [x] Enforce PTY session, reader-task, input queue, and event buffer caps with
  explicit overload/refusal outcomes. Laptop defaults remain `2` sessions,
  `4` reader tasks, queue depth `256`, and event buffer `1000`; the connector
  also caps command timeout and output bytes.
- [~] Implement watch cursors for terminal events and operation outcomes. The
  connector exposes bounded synthetic/local event cursors for environment/read/probe
  events and per-session terminal event cursors; local deferred wait status is
  visible through `/v1/workbench/operation/status`, while generalized operation
  outcome watches remain tied to later host-broker runtime work.
- [x] Implement short bounded waits for command done, terminal quiescence,
  environment ready, file exists, and artifact present. The connector now has a
  bounded wait path over probe conditions for each MVP condition. Short waits run
  synchronously up to `sync_wait_max_ms`; explicit async waits return
  `deferred-operation.v1` and project through `deferred-operation-status.v1`.
- [x] Implement active probes for process liveness, environment readiness, file
  existence/digest, and artifact presence. Environment readiness, file
  existence/digest, process-alive, terminal-command-done, terminal-quiescent,
  terminal-no-progress, and artifact-present probes are implemented.
- [x] Keep raw PTY input disabled or operator-only until an explicit policy is
  accepted. Raw PTY input is implemented only as an operator-confirmed grant
  path; model-driven raw input remains denied.
- [~] Implement TTL, idle timeout, byte caps, process cleanup, and refusal
  diagnostics. Request body caps, file read byte caps, terminal command timeout,
  command output byte caps, session caps, process termination on close/timeout,
  startup orphan process signaling, event payload caps, SQLite retention cleanup,
  and typed refusal diagnostics exist; idle-timeout policy remains future work.
- [x] Implement file snapshot and bounded file read. Snapshot lists symlinks as
  metadata without following them; reads refuse symlink traversal and files over
  the host read cap.
- [x] Implement patch apply from artifact ref with digest/provenance. Patch
  apply is now an opt-in artifact-backed path behind
  `sensorium.workbench.patch` plus operator confirmation. It verifies artifact
  digest and size, supports structured create/replace/append plus a narrow
  single-file unified-diff path, refuses deletes by default, plans structured
  edits before applying them, rolls back previously applied structured writes
  on later write failure, records metadata-only outcomes, and uses the same
  workspace containment and symlink checks as reads.
- [~] Use Bounded Deferred Operations for environment setup or command runs that
  outlive one HTTP request. The current terminal command endpoint returns
  `202 accepted` and exposes event/wait polling. Async waits now return the
  canonical `deferred-operation.v1` / `deferred-operation-status.v1` shapes,
  require an explicit wait grant for status reads, de-duplicate by
  `idempotency/key`, and mark interrupted pending/running wait operations as
  failed with retry diagnostics on startup, but they are still connector-local
  rather than registered in the daemon host Bounded Deferred Operation registry.
- [~] Run the adversarial actuator test matrix before enabling write or PTY
  features by default. The current test slice covers traversal, root self,
  symlink traversal, oversized files, grant-required mediated read, command
  profile denial including variable argv beyond a fixed prefix, dangerous env
  override stripping, operator-only raw input denial, retired session refs, and a
  PTY happy path. It now also covers artifact digest mismatch, terminal capture
  to artifact, terminal-capture artifact-write grant refusal, delete-forbidden
  patch apply, successful structured patch apply, structured patch rollback on
  partial write failure, connector-local deferred wait projection, operation
  status grant refusal, connector idempotency-key refusal, interrupted operation
  recovery, and the daemon rule that Inquirium cannot directly invoke Sensorium
  connectors. Broader residual-child, egress, credential, replay, and
  virtualized-backend vectors remain.

### Phase 2 - Sensorium Integration

- [x] Add Sensorium Core capability routing for Workbench directives. The
  connector exposes `/v1/sensorium/connector/invoke` and Workbench action ids
  for Sensorium Core mediated routing; Sensorium Core already dispatches
  allowlisted connector directives with directive metadata and idempotency.
- [~] Route cross-source waits through the host interaction broker rather than
  making Sensorium Core own AD, Memarium, approval, or deferred-operation joins.
  The daemon broker now owns grant-context admission for JSON-e/module
  wait/watch/probe calls through daemon-issued host-local HMAC grant material
  requested by `bindings.host_grant_requests`, keeps deferred-operation
  `OperationDone` waits host-owned, and wires live Workbench file-tree plus
  terminal providers for file probes, file waits, file-tree watch batches,
  terminal liveness/progress probes, terminal waits, and terminal watch batches.
  AD, Memarium, approval, and dynamic non-Workbench provider joins remain open.
- [~] Add grant and policy checks for terminal command, terminal raw input,
  file snapshot, file read, and patch apply. The connector enforces explicit
  grant envelopes for mediated file/probe/watch/wait actions and terminal
  actions; raw input, resize, and signal additionally require operator
  confirmation; terminal capture requires both terminal-session and
  artifact-write grants; operation status reads require an explicit wait grant;
  and daemon broker dispatch now requires JSON-e/module callers to request the
  relevant broker grant in `bindings.host_grant_requests`, then admits the call
  only after daemon-issued host-local HMAC grant material is minted and verified.
- [x] Extract Workbench grant/autonomy policy into the
  authorization-policy-as-data sidecar. `capability-authorization-policy.v1`
  now carries required grants, caller posture, approval mode, autonomy floor, and
  COI policy for the P071 Workbench and Interaction Broker capability ids; P072
  Phase 4 is marked landed against this contract.
- [~] Record directive outcomes and metadata-only traces. Terminal runtime now
  records sessions, commands, events, terminal captures, local artifacts,
  connector-local deferred waits, patch applications, and metadata-only outcomes
  durably in connector SQLite. Host audit projection of those facts remains
  future. Session refs are retired after first use to keep the audit trail
  unambiguous.
- [x] Add operator status/control surfaces for active sessions and sandboxes.
  `/v1/status` reports terminal enablement, PTY caps, active session count, and
  session summaries; session close is an explicit control surface. Sandboxes
  remain future virtualized backend work.
- [~] Expose active waits, watches, deadlines, and suspected no-progress states
  in operator status. Event cursors, command status, connector-local active wait
  count/status, no-progress probe diagnostics, and host-broker status/providers/
  resource read APIs are exposed. Rich operator UX over host-broker state
  remains future.
- [~] Link captured outputs through Artifact Delivery or Memarium only under
  explicit classification and retention policy. Terminal capture now writes a
  bounded local artifact descriptor with classification and provenance; AD or
  Memarium admission remains a separate explicit future handoff.

### Phase 3 - Inquirium/JSON-e Flow Integration

- [x] Add JSON-e Flow example: inspect terminal output through bounded snapshot.
  Implemented under
  `node/middleware-runtime/fixtures/json-e-flow/sensorium-workbench/`.
- [x] Add JSON-e Flow example: model proposes command, host validates, Workbench
  executes.
- [x] Add JSON-e Flow example: wait for a Workbench condition without private
  polling in the flow step.
- [x] Add Inquirium assistant-channel guidance for Workbench-backed tool use.
  The Workbench README and JSON-e Flow examples document the non-authoritative
  Inquirium proposal path: model output becomes intent, while Sensorium grants
  and Workbench execute.
- [x] Add negative tests proving Inquirium cannot directly invoke Workbench
  without grants. The daemon dispatch regression now explicitly asserts that
  `inquirium-core` cannot dispatch `sensorium.connector.invoke`; only
  `sensorium-core` may reach connector-local invoke.

### Phase 4 - Virtualized Backends

- [ ] Define `Sensorium Virt` backend contract for the same environment/session
  abstractions.
- [ ] Implement first disposable sandbox backend.
- [ ] Add artifact export and teardown tests.
- [ ] Add policy tests for denied egress and denied credential access.
