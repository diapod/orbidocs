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

## Status

Draft

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
canonical lifecycle status model; `sensorium-workbench-wait.outcome.v1` is the
domain result/projection carried directly by a short synchronous wait or under
`deferred-operation-status.v1.result` for async waits.

Candidate wait request:

```json
{
  "schema": "sensorium-workbench-wait.request.v1",
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
  "schema": "sensorium-workbench-wait.outcome.v1",
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
  "operation/id": "deferred:sensorium.workbench.wait:story009-command-ready",
  "operation/kind": "sensorium.workbench.wait",
  "updated_at": "2026-06-23T12:00:00Z",
  "result": {
    "schema": "sensorium-workbench-wait.outcome.v1",
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
| Workflow blocks on a long-running operation. | Use Bounded Deferred Operations for work that can outlive one HTTP request. |
| Client invents private polling or watcher loops. | Provide host-owned watch/wait/probe refs with deadlines, cursors, caps, and outcomes. |
| Quiet terminal is misclassified as hung. | Separate `quiescent`, `waiting_for_input`, `no_progress`, `maybe_hung`, and `probe_failed` states under policy. |
| Watch cursor is lost during component restart. | Keep bounded replay windows and explicit cursors for watch sources. |
| Event producer overwhelms a consumer. | Enforce byte/event caps, cursor windows, truncation markers, and backpressure/overload status. |
| Agent adapter bypasses Sensorium tools. | Reject adapters that own their own terminal/filesystem authority outside host grants. |
| Workbench grows into a second orchestration core. | Keep Workbench as an actuator: no policy selection, no model routing, no workflow ownership. |

## Adversarial Actuator Test Matrix

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
| `sensorium-workbench-watch.v1` | Cursor-bound subscription over a Workbench event source with caps, TTL, and classification. |
| `sensorium-workbench-wait.request.v1` | Declarative bounded condition over observations, with deadline and idempotency key. |
| `sensorium-workbench-wait.outcome.v1` | Domain result/projection for a satisfied or terminal wait condition; async lifecycle status is still `deferred-operation-status.v1`. |
| `sensorium-workbench-probe.v1` | Active bounded check for liveness, readiness, file state, artifact presence, or progress. |
| `sensorium-file-snapshot.v1` | Directory/file metadata snapshot under an allowlisted root. |
| `sensorium-file-read-result.v1` | Bounded file content or artifact ref. |
| `sensorium-workbench-patch.v1` | Patch proposal artifact and metadata. |
| `sensorium-workbench-patch-apply-result.v1` | Applied/rejected patch result with changed files and digests. |
| `sensorium-workbench-outcome.v1` | Host audit fact linking directive id, grant, caller, session/environment refs, status, timing, byte counts, and artifacts. |

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

## Open Questions

1. Should Workbench start as a separate supervised module immediately, or as an
   optional capability group inside Sensorium OS with a migration path?
   Recommendation: start as a separate supervised connector if implementation
   time allows; otherwise keep a separate Workbench contract even when reusing
   Sensorium OS internals.
2. What is the smallest terminal screen model that is useful to LLMs without
   leaking entire transcripts?
3. Should patch application use unified diff only, or admit structured edit
   operations later?
4. What default approval profile should local filesystem writes use?
5. Should terminal sessions produce Memarium facts only on explicit capture, or
   should outcome summaries always be mirrored?
6. Which sandbox backend should be first after host-local workspaces:
   container, microVM, or fixture-only virtual workspace?
7. How should Workbench expose file trees to models: direct snapshots,
   artifact-index refs, or a query-style lease?
8. Should raw PTY input be operator-only in the MVP, or may narrow built-in
   workflows use it under a stronger approval profile?
9. Which command profile fields are required before the first implementation:
   executable identity, argv schema, cwd policy, env policy, timeout, egress,
   and output capture policy?
10. Which wait conditions should be guaranteed in the MVP versus left as
    component-specific probes?
11. What bounded replay window is sufficient for watch cursors in local-only
    Workbench sessions?
12. Should `maybe_hung` be purely diagnostic, or may policy automatically
    escalate it into an operator question?
13. Should the host-owned interaction broker be promoted into its own solution
    document before Workbench implementation, or first appear as a daemon
    primitive consumed by Sensorium?
14. What are the default PTY concurrency caps for a local laptop profile:
    active sessions, reader tasks, input queue depth, and event buffer depth?
15. Are `deferred-operation-status.v1.extensions` sufficient for early async
    wait diagnostics, or should a small common wait/probe extension be promoted
    before implementation?
16. Should the existing Python Sensorium OS connector consume the shared Rust
    `sensorium-actuation-core` through a binding/RPC path, or should the shared
    core first be consumed only by the future Workbench connector while the
    Sensorium OS implementation remains a separately audited reference?
17. Which Workbench and interaction-broker DTOs need JSON Schema projections
    before the first cross-process boundary is exposed? Candidate schemas are
    watch request, wait request, wait outcome, probe request, command profile,
    command intent, relative path address, and PTY resource caps.
18. Should timeout policy ever authorize kill-on-timeout from the host
    interaction broker, or should process termination remain exclusively a
    connector/operator directive separate from wait outcome semantics?
19. Should the host interaction broker keep validating only the basic
    `deferred:<operation_kind>:<deterministic_id>` shape, or should the exact
    deterministic-id validator be shared with the deferred-operation registry
    before cross-process broker APIs are exposed?
20. Should relative path syntax validation move into a smaller shared utility
    crate consumed by both `sensorium-actuation-core` and
    `interaction-broker-core`, or should the current duplication remain
    intentional because the broker is a horizontal primitive and must not
    depend on actuation-specific code?
21. Should the Workbench foundation appear in hard-MVP implementation docs as a
    planned post-MVP seed, or only in proposal and implementation-ledger
    tracking until a connector or host runtime surface exists?

## Next Actions And Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Phase 0 - Contract Freeze

- [ ] Decide whether first implementation is a separate Workbench connector or
  an optional capability group inside Sensorium OS.
- [~] Decide whether the host-owned interaction broker is promoted to a
  separate solution before implementation or first lands as a daemon primitive.
  Initial unwired Rust foundation exists in
  `node/interaction-broker-core`; daemon ownership and public solution status
  are still undecided.
- [~] Define the shared actuation core boundary consumed by Sensorium OS and
  Workbench. Initial unwired Rust foundation exists in
  `node/sensorium-actuation-core`; Sensorium OS and Workbench do not consume it
  yet.
- [ ] Define `sensorium-workbench-environment.v1`.
- [ ] Define terminal session/command/raw-input/event/snapshot schemas.
- [~] Define watch/wait/probe schemas, status values, cursor rules, and timeout
  semantics. The initial host-owned watch/wait/probe contract lives in
  `node/interaction-broker-core`, including bounded caps, deadlines,
  correlation ids, no-progress vocabulary, and deferred-operation projection.
- [ ] Require `schema` and `schema/v` on every top-level Workbench schema while
  preserving embedded `classification.v1` as schema-only.
- [ ] Define file snapshot/read and patch apply schemas.
- [ ] Define operator-visible status fields and audit outcome shape.
- [~] Define command profile fields and normalized argv digest rules. The
  initial unwired contract lives in `node/sensorium-actuation-core`, including
  argv-as-data validation, environment policy, timeout/output caps, workspace
  root policy, and canonical JSON argv digest.
- [ ] Define `correlation/id` threading across directive, events, wait outcome,
  artifacts, and next directive.
- [~] Define async wait status as `deferred-operation-status.v1` with Workbench
  wait outcome as the result projection, not as a parallel status model.
  `node/interaction-broker-core` contains the initial conversion helper; host
  registry integration is still not wired.
- [ ] Decide MVP policy for raw PTY input.
- [ ] Decide MVP wait conditions and no-progress vocabulary.
- [ ] Define the adversarial actuator test matrix as a required acceptance
  suite.

### Phase 1 - Local Workbench Connector

- [ ] Add a supervised local Workbench connector module.
- [ ] Consume the shared actuation core instead of reimplementing path,
  command-profile, allowlist, classification, and argv rules.
- [ ] Implement host-local allowlisted workspace environment.
- [ ] Implement terminal session create/commands/events/resize/signal/close.
- [ ] Enforce PTY session, reader-task, input queue, and event buffer caps with
  explicit overload/refusal outcomes.
- [ ] Implement watch cursors for terminal events and operation outcomes.
- [ ] Implement short bounded waits for command done, terminal quiescence,
  environment ready, file exists, and artifact present.
- [ ] Implement active probes for process liveness, environment readiness, file
  existence/digest, and artifact presence.
- [ ] Keep raw PTY input disabled or operator-only until an explicit policy is
  accepted.
- [ ] Implement TTL, idle timeout, byte caps, process cleanup, and refusal
  diagnostics.
- [ ] Implement file snapshot and bounded file read.
- [ ] Implement patch apply from artifact ref with digest/provenance.
- [ ] Use Bounded Deferred Operations for environment setup or command runs that
  outlive one HTTP request.
- [ ] Run the adversarial actuator test matrix before enabling write or PTY
  features by default.

### Phase 2 - Sensorium Integration

- [ ] Add Sensorium Core capability routing for Workbench directives.
- [ ] Route cross-source waits through the host interaction broker rather than
  making Sensorium Core own AD, Memarium, approval, or deferred-operation joins.
- [ ] Add grant and policy checks for terminal command, terminal raw input,
  file snapshot, file read, and patch apply.
- [ ] Record directive outcomes and metadata-only traces.
- [ ] Add operator status/control surfaces for active sessions and sandboxes.
- [ ] Expose active waits, watches, deadlines, and suspected no-progress states
  in operator status.
- [ ] Link captured outputs through Artifact Delivery or Memarium only under
  explicit classification and retention policy.

### Phase 3 - Inquirium/JSON-e Flow Integration

- [ ] Add JSON-e Flow example: inspect terminal output through bounded snapshot.
- [ ] Add JSON-e Flow example: model proposes command, host validates, Workbench
  executes.
- [ ] Add JSON-e Flow example: wait for a Workbench condition without private
  polling in the flow step.
- [ ] Add Inquirium assistant-channel guidance for Workbench-backed tool use.
- [ ] Add negative tests proving Inquirium cannot directly invoke Workbench
  without grants.

### Phase 4 - Virtualized Backends

- [ ] Define `Sensorium Virt` backend contract for the same environment/session
  abstractions.
- [ ] Implement first disposable sandbox backend.
- [ ] Add artifact export and teardown tests.
- [ ] Add policy tests for denied egress and denied credential access.
