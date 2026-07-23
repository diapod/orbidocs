# Proposal 071: Sensorium Workbench

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/039-notifications/039-notifications.md`
- `doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`

## Status

Accepted / implemented.

The settled solution surface is promoted to
`doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`.
This proposal remains the rationale, design history, resolved-decision log, and
implementation tracker for Workbench. The promoted solution component owns the
current solution-level responsibility boundary. The host-owned operator
consent spine is implemented for exact and bounded-prefix Workbench terminal
commands: a pure
`operator-consent-core` contract crate, daemon-owned consent registry and
operator APIs, P066 notification/answer reuse, `operator-consent.request.v1`,
`operator-consent-decision.v1`, `sensorium-workbench.consent-descriptor.v1`,
and Workbench exact-argv/prefix runtime admission with shared append-only sidecar
merge, bounded refresh, active `node-operator-binding.v1` enforcement for
answers and revocation, durable-grant grantability checks, inactive-binding
diagnostics, and dedicated operator UI. Native broker providers, explicit
artifact handoff, the Rust actuation bridge, a managed fixture-copy virtual
executor, and Agent/Corpus/Room tool-request lineage are also implemented.
The property-attested process-isolated backend architecture is frozen, and the
first `vfkit-system.v1` host-lifecycle slice is implemented for
`macos-vz-arm64.v1`. The daemon-owned broker now covers allocation, closed-argv
launch, inspection, cooperative drain, teardown, recovery, exact process/socket/
resource identity, boot nonces, reconciliation, and quarantine without exposing
VMM administration sockets to Python. Process-level fake-vfkit evidence covers
replay, dirty exit, PID reuse, socket and binary substitution, missing storage,
and orphan cleanup. The packaged guest agent and host channel now cover exact
generation/plan/image/nonce binding, bounded process/PTY/file/lifecycle mechanics,
one total process-output budget, ioctl-backed PTY resize, atomically durable
content-bound patch staging, endpoint-identity revalidation, chunked transfer,
and local-transport conformance. A pinned full-system GNU/Linux arm64 image
builder and real-vfkit harness now prove EFI boot, the virtio-vsock guest channel,
systemd/PID 1, bounded PTY/file mechanics, offline package use, constrained guest
resources, dirty-restart recovery, and deterministic teardown on Apple Silicon.
The virtualized Workbench adapter routes that PTY/file channel through daemon-owned
`sensorium.virt.host`; terminal output enters P082 and P083 remains the sole remote
control authority. The additive Story 012 profile now runs the digest-pinned repair
fixture inside that same full-system guest and proves the complete three-node
collaboration, revoke, dirty restart, repair, passing observation, export, and
unpublished Corpus draft under a schema-gated `single-runtime-vertical` report.
The freeze also requires closed capability vocabularies,
plan-bound operational context and policy floors, evidence-based logical image
equivalence, and sanitized classified serial diagnostics. The existing Workbench
environment/export contracts remain landed.

The `cloud-hypervisor-system.v1` implementation slice is also landed behind the
same daemon-owned host contract. It includes operator-only profile admission,
binary/firmware/raw-image pinning, a closed REST and device builder, durable
lifecycle and recovery identities, an output-only continuously bounded serial
tail, cgroup v2 and non-root process identity, Cloud Hypervisor's default seccomp
posture, explicit Landlock rules, the common guest protocol, SMBIOS bootstrap,
authoritative cgroup cleanup during quarantine/orphan reconciliation, and Workbench
executor routing. The image resolver admits a multi-backend logical manifest but
requires exactly one matching Cloud Hypervisor x86_64/EFI/raw variant. macOS
fake-process conformance proves the command,
API, replay, substitution-refusal, serial-bound, and lifecycle mechanics without
claiming KVM. A Linux x86_64 CI compile/conformance gate and a separate real-KVM
deployment runner with a closed schema-gated evidence report are checked in. This
item remains **in progress** until that
runner produces passing evidence on Linux x86_64 with `/dev/kvm`; QEMU/TCG and
the fake VMM cannot satisfy the deployment gate.

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
  "command/ref": "command:story009-test",
  "event.seq/no": 42,
  "event/kind": "output",
  "bytes/base64": "Y2FyZ28gdGVzdCAuLi4K",
  "bytes/sha256": "sha256:aa6Fud_IA0XPRXzUS1xggKYcwW52ndR6bTRdHNHOrwA",
  "bytes/count": 15,
  "observed_at": "2026-07-22T10:00:00Z",
  "classification": {
    "schema": "classification.v1",
    "source_tier": "Personal",
    "effective_tier": "Personal",
    "provenance": { "kind": "local-space", "space": "Personal" },
    "bound_subjects": {
      "personal_or_community": [
        { "kind": "person", "id": "participant:did:key:z6MkTerminalViewer" }
      ]
    },
    "declassify_trail": []
  }
}
```

`output` events preserve exact PTY bytes as base64 plus a digest and count;
UTF-8 text is a presentation concern, not the wire truth. Lifecycle, resize,
accepted-input, and rejected-input events use closed kind-specific shapes. Input
events may retain only a byte count and reason code, never raw input content.

Terminal events are session-local observations. Their connector-local replay log
has explicit event, byte, and age caps. A cursor older than the retained floor
produces an explicit gap before newer events; a closed terminal produces an
explicit terminal end rather than an empty non-terminal batch. The authoritative directive
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

#### 7.1 Backend Capability Admission

A backend id selects an implementation; it is not evidence of isolation. Before a
process-isolated environment is allocated, the host must compare a normalized
environment requirement with a host-attested backend capability descriptor. The
minimum descriptor vocabulary is:

```text
backend/id
backend/provider
backend/version
backend/binary-digest
platform/ref
locality
host/architecture
guest/architecture
isolation/class
system/fidelity
control/transport
control/guest-endpoint
control/host-endpoint
control/channel-binding
boot/mode
storage/formats
device/classes
console/mode
network/profiles
host-filesystem-sharing/mode
credential-injection/mode
resource-enforcement/classes
lifecycle/operations
```

`sensorium-virt-backend-capabilities.v1` is a closed contract, not an open map of
backend claims. `additionalProperties` is false; supported-value collections are
bounded sets with unique items; and every semantic value is selected from a
versioned enum. The initial V1 vocabulary is:

| Dimension | Closed V1 values |
| --- | --- |
| `locality` | `local-only`, `remote-sandbox` |
| `host/architecture`, `guest/architecture` | `x86_64`, `arm64` |
| `isolation/class` | `none`, `process-sandbox`, `shared-kernel-container`, `hardware-vm` |
| `system/fidelity` | `filesystem-view`, `process-runtime`, `shared-kernel-linux`, `full-system-linux` |
| `control/transport` | `none`, `local-process`, `virtio-vsock` |
| `control/guest-endpoint` | `none`, `af-vsock` |
| `control/host-endpoint` | `none`, `af-vsock`, `unix-domain-socket` |
| `control/channel-binding` | `none`, `environment-generation-boot-nonce` |
| `boot/mode` | `none`, `efi`, `direct-kernel` |
| `storage/formats` | `directory-copy`, `raw`, `kernel-initrd-rootfs` |
| `device/classes` | `virtio-block`, `virtio-vsock`, `virtio-rng`, `diagnostic-serial`, `virtio-net` |
| `console/mode` | `none`, `diagnostic-output-only` |
| `network/profiles` | `none`, `isolated`, `egress-allowlisted` |
| `host-filesystem-sharing/mode` | `denied`, `read-only`, `read-write` |
| `credential-injection/mode` | `denied`, `explicit-scoped` |
| `resource-enforcement/classes` | `host-cpu`, `host-memory`, `host-process`, `host-storage`, `host-io`, `guest-vcpu`, `guest-memory`, `guest-pids`, `guest-storage`, `channel-bounds` |
| `lifecycle/operations` | `allocate`, `start`, `inspect`, `drain`, `teardown`, `recover` |

`backend/id`, `backend/provider`, and `platform/ref` resolve through bounded host
registries rather than semantic enums; an unknown identity is denied before
matching. Adding a new semantic value requires a schema/registry revision and
conformance evidence. Host
policy may select or equate only values already admitted by that version, so policy
configuration cannot turn an arbitrary string into evidence.
Plural descriptor fields such as `network/profiles` and `device/classes` contain
supported sets; the normalized plan records one selected scalar such as
`network/profile` and an exact selected device set. Locality remains a separate
requirement and never masquerades as an isolation class.

The host, not the backend adapter, owns this attestation. A backend may report raw
facts, but a Rust validator maps the pinned binary, platform, enabled device set,
and host controls to the effective descriptor. Unknown, missing, or unverified
properties do not match a requirement.

Matching is conjunctive and property-based. `hardware-vm` is not a magic synonym
for every stronger-looking backend name, and the property dimensions do not form
one universal scalar ordering. A full-system proof can require, for example:

```text
isolation/class = hardware-vm
system/fidelity = full-system-linux
control/transport = virtio-vsock
control/channel-binding = environment-generation-boot-nonce
host-filesystem-sharing/mode = denied
network/profile = none
```

Host policy may admit an explicit set of equivalent values on one dimension, but
it must not infer equivalence from marketing labels such as container, sandbox,
or microVM. The selected descriptor, normalized environment plan, policy ref,
image manifest, and their digests become one immutable allocation input. Replay
with the same idempotency key and plan digest returns the same environment; the
same key with a different digest is a conflict.

The normalized plan also requires the exact effective
`sensorium-operational-context.v1` value. The host derives it before allocation
from the environment candidate, the selected resource context, and a policy floor;
the backend adapter may neither default nor rewrite it after normalization. The
plan digest binds the source candidate digest, effective context, and policy ref.
The initial policy floor is `test` when `network/profile != none` or
`host-filesystem-sharing/mode != denied`. Any reachable network target or shared
host resource contributes its own context, and the effective class is the maximum
of the candidate, the floor, and those attached-resource classes. Missing target
context fails admission closed. A stricter deployment may raise this floor, but
none may lower a production or critical target to `test`. Raising the class does
not authorize the host to rewrite the candidate's untrusted `context/summary`;
the policy ref and candidate digest explain the raise. The reference full-system
configuration proof uses `test`. A disposable offline VM may use `experimental`,
while `hardware-vm` by itself never chooses an impact class.

The current `sensorium-workbench-environment.v1` `backend` and `executor.kind`
fields remain useful projections, but they are too coarse to serve as isolation
evidence. Phase 4 must add a companion capability descriptor and normalized-plan
contract before enabling a process-isolated PTY.

#### 7.2 Reference Full-System Profiles

The first implementation target is split by host platform rather than pretending
that one VMM is portable across macOS and Linux:

| Profile | Role | Required substrate | Initial posture |
| --- | --- | --- | --- |
| `vfkit-system.v1` on `macos-vz-arm64.v1` | first developer reference backend and first implementation slice | Apple Silicon, Apple Virtualization Framework, pinned vfkit binary | full GNU/Linux arm64 system; EFI boot; raw working disk and per-environment EFI variable store; `virtio-blk`, `virtio-vsock`, `virtio-rng`; no NIC or serial device in the first deployment profile |
| `cloud-hypervisor-system.v1` on `linux-kvm-x86_64.v1` | first Linux full-system deployment backend | Linux/KVM, cgroup v2, pinned Cloud Hypervisor binary, host filesystem confinement | full GNU/Linux x86_64 system; firmware boot from an explicit raw image; block, vsock, entropy, bounded diagnostic serial; no NIC by default |
| `firecracker-system.v1` on a compatible `linux-kvm-*.v1` platform | second Linux backend and hardened minimal-device profile | Linux/KVM and a jailer-equivalent launch boundary | introduced after the guest protocol and image manifest are stable; only the common block, vsock, entropy, console, resource, and teardown substrate is portable |

`vfkit-system.v1` is selected first because the primary developer platform is
macOS on Apple Silicon and vfkit can boot a normal EFI disk image while exposing
bounded lifecycle inspection and control. Its host endpoint for a guest
virtio-vsock port is a dedicated Unix-domain socket. The domain contract still
names `virtio-vsock`; the UDS translation is private backend mechanics:

```text
control/transport:       virtio-vsock
control/guest-endpoint:  af-vsock
control/host-endpoint:   unix-domain-socket
```

The allowed vfkit device profile is closed. `virtio-fs`, Rosetta shares, host
directory mounts, host block-device passthrough, credentials, arbitrary host
sockets, graphics/input devices, and network devices are denied. The only host
socket exceptions are the exact broker-allocated VMM-administration and guest-
control sockets; the administration socket remains broker-private. For every
backend, diagnostic serial is output-only and bounded, never an interactive console or second input
path. Its bytes are untrusted guest data: ordinary status and logs retain only
metadata, while an explicitly admitted diagnostic capture inherits the environment
classification and operational context, has byte/time caps plus a digest and
truncation marker, and is subject to configured redaction. Operator presentation
uses a sanitized rendering that escapes control bytes and strips terminal-control
sequences, including ANSI CSI, OSC, and DCS; raw bytes are never written directly
to an operator terminal. Allocation creates an APFS copy-on-write clone of the
pinned raw base disk and a private EFI variable store; the base image remains
immutable. The process
is launched headlessly with an operator-pinned version and binary digest. An Intel
Mac profile may be registered later as `macos-vz-x86_64.v1`, but only after
separate image and conformance evidence; architecture substitution is not implicit.

`cloud-hypervisor-system.v1` is the first Linux profile because its local REST
API maps cleanly to full-system lifecycle mechanics and it supports firmware boot
of ordinary raw Linux images. Orbiplex uses only a closed subset of the VMM:
`virtio-block`, `virtio-vsock`, `virtio-rng`, optional future isolated
`virtio-net`, and bounded serial diagnostics. `virtio-fs`, VFIO, vhost-user
devices, host directory mounts, arbitrary hotplug, live migration, and durable
memory snapshots are denied. Serial diagnostics follow the same bounded, classified,
sanitized output-only policy. Disk format is
explicit; format autodetection and backing-file chains are not admitted.
The Linux host broker runs the VMM under a dedicated unprivileged identity,
cgroup v2 limits, seccomp, and a file allowlist enforced by Landlock. The
`cloud-hypervisor-system.v1` production configuration queries the host Landlock
ABI before it can publish capabilities or accept allocation and requires ABI v3
or newer, matching the pinned VMM's hard-requirement mode. The normalized plan
requires the closed `host-filesystem-allowlist` resource-enforcement class; an
unsupported kernel therefore cannot advertise or allocate this profile. A future
backend may use an equally explicit host wrapper, but must publish a distinct
closed enforcement class and pass separate conformance.
The closed launcher does not expose Cloud Hypervisor's `--seccomp` option, so the
VMM's built-in seccomp remains enabled with its default trapping action. The host
cgroup's fixed `pids.max = 64` bounds VMM-side tasks and is deliberately distinct
from the plan's `processes/max`, which is projected into guest-agent admission.
The image-specific deployment evidence separately proves the pinned guest service
`TasksMax`; a host cgroup limit never substitutes for that guest-side proof. REST
I/O budgets are operation-classed and closed in code: `2 s` for ping, create, and
info, `15 s` for boot, `10 s` for guest shutdown, and `5 s` for VMM shutdown.
Socket publication is followed by a bounded API ping retry for transient local
connect refusal; malformed API responses and exhaustion remain terminal failures.
If the selected profile requires one of these controls and the host cannot prove
it, allocation fails closed.

Firecracker follows as a separate backend because its smaller device model and
jailer are valuable hardening, while its kernel/rootfs preparation and full-system
shutdown mechanics should not define the first Workbench contract. This is a
sequencing decision for the full GNU/Linux configuration proof, not a universal
security ranking of VMMs.

OCI may distribute a signed and digest-pinned logical image artifact containing
backend variants, the guest-agent binary, SBOM, provenance, and minimum guest
protocol. An OCI runtime does not own Workbench allocation, lifecycle, recovery,
or authority.

Implementation-source basis, verified on 2026-07-20: the official
[vfkit usage contract](https://github.com/crc-org/vfkit/blob/main/doc/usage.md)
documents EFI boot, raw/APFS clone-backed disks, optional devices, Unix-socket
REST control, and guest-vsock-to-host-UDS mapping; the official
[Cloud Hypervisor README](https://github.com/cloud-hypervisor/cloud-hypervisor)
and [API contract](https://github.com/cloud-hypervisor/cloud-hypervisor/blob/main/docs/api.md)
document firmware boot and Unix-socket lifecycle control; the official
[Firecracker design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md),
[jailer](https://github.com/firecracker-microvm/firecracker/blob/main/docs/jailer.md),
and [vsock](https://github.com/firecracker-microvm/firecracker/blob/main/docs/vsock.md)
documents define the later minimal-device profile. Version numbers remain
operator-pinned deployment data rather than proposal constants.

#### 7.3 Two Ports And Three Ownership Layers

VMM lifecycle and guest Workbench mechanics are separate ports:

```text
EnvironmentBackend
  allocate start inspect drain teardown recover

GuestWorkbenchChannel
  handshake spawn_process open_pty
  terminal_input terminal_resize terminal_signal
  file_snapshot file_read patch_stage artifact_export
  inspect quiesce shutdown
```

The ports are logical contracts; they need not be one Rust trait across a process
boundary. Cloud Hypervisor, vfkit, and Firecracker differ behind
`EnvironmentBackend`. The same bounded guest protocol implements
`GuestWorkbenchChannel`, so SSH, a network interface, or a host-shared filesystem
never becomes public Workbench semantics.

Ownership is stratified:

- `sensorium-virt-core` is a pure Rust contract layer for backend capabilities,
  requirement matching, normalized plans, limits, lifecycle transitions,
  image compatibility, plan digests, recovery identity, and network/device/host-
  path refusal. A bounded companion process may expose these decisions to Python;
  absence, timeout, or malformed output fails closed.
- the daemon-owned `virt-host-broker` is the host authority for working disks,
  process identities, VMM launch, exact API/control sockets, platform resource
  controls, optional Linux cgroups and network namespaces, resource enumeration,
  quarantine, and teardown. A concrete implementation may use a different module
  name without changing this ownership boundary.
- the Python Workbench adapter owns connector mechanics: mapping an already
  normalized plan to bounded backend request data, readiness waits, bounded guest
  RPC, SQLite projections, Interaction Broker observations, and typed diagnostics.
  It receives broker-allocated identities and the exact guest-channel handle; the
  host broker retains the VMM administrative socket and mediates its narrow
  lifecycle operations. The adapter must not gain ambient authority to launch
  arbitrary VMM processes, open arbitrary host paths, create host network devices,
  or widen the normalized plan.

This preserves the current rule: Python runs connector mechanics; Rust owns
semantic validation and host authority.

#### 7.4 Guest Agent Contract

The reference image contains a small Rust process named
`orbiplex-workbench-guest`. It communicates only over virtio-vsock, without IP or
SSH. The initial handshake binds at least:

```text
environment/ref
source/generation-ref
normalized-plan/digest
image/digest
guest-agent/protocol-version
guest/cid
boot/nonce
```

`boot/nonce` is generated for every start and must match the host recovery record.
A backend supplies it through a dedicated ephemeral read-only boot/config input or
an equivalently bound channel established by the host broker. It is a freshness
and channel-binding control, not cryptographic attestation that the guest is honest.
A stale agent, restored guest, old control socket, or previous source generation
is refused before any command is dispatched. Operation frames additionally bind
the environment, generation, operation id, sequence, deadline, payload length,
chunk count, and digest. Queues and reassembly buffers have hard byte, frame,
chunk, and time caps.

The implemented V1 wire vocabulary is closed to `handshake`, `request`, `chunk`,
`result`, and `error`. `sensorium-virt-core` owns the shared bindings, typed
operation set, honest `succeeded`/`refused`/`unknown` evidence rules, and hard
frame/chunk/transfer limits. The host derives the expected handshake exclusively
from the current vfkit recovery record and releases its broker lock before channel
I/O. It rechecks endpoint device/inode identity across connect; endpoint replacement
or listener loss refuses before the handshake, while the full handshake binding
remains the channel authority. The packaged Rust guest uses the same engine over Linux AF_VSOCK and a
feature-gated local Unix transport used only for conformance. That harness runs the
real guest binary and proves process, PTY, file, patch, export, lifecycle inspect,
quiesce, shutdown, admission refusal, deadline non-extension, exact wire bounds,
partial-transfer refusal, and content-bound replay after a lost patch-stage receipt,
in addition to stale-nonce, replay, overflow, and disconnect behavior; it is not VM, image,
systemd, kernel, cgroup, network, or vfkit deployment evidence.
`quiesce` first reaps completed PTY children, so its active-session count describes
live authority rather than retained process bookkeeping.

`output/bytes-max` is one decoded-byte budget for a process result, shared by
stdout and stderr rather than multiplied per stream. PTY resize uses the terminal
ioctl directly and does not require an image-specific `stty` executable.
`patch-stage` is staging, not application: it atomically stores exact content
under a path/content/length-bound stage ref, returns that same ref for an exact
retry, never mutates the target, exposes count and bytes through `inspect`, and
retains at most 64 stages and 64 MiB in environment state until teardown. A
disconnect before complete transfer publishes no stage; a lost response after
commit is resolved by exact replay. Request parsing and pre-dispatch admission
failures are `refused` with admission evidence. `unknown` is reserved for an
admitted effect whose outcome cannot be proved.

The guest agent owns no authorization policy. It executes only normalized,
already-admitted mechanics and returns untrusted observations. Root inside the
guest can compromise the agent and falsify guest state; it must not thereby gain
host paths, credentials, sockets, or ambient network access. Guest cgroups,
including per-command PID limits, are useful defense in depth and conformance
controls, but they are not a host security boundary against compromised guest
root. Host-side CPU, memory, storage, process, and I/O limits remain mandatory.

#### 7.5 Images, Resources, And Network

The logical image manifest pins the full-system image, architecture, boot
variant, guest protocol, guest-agent digest, SBOM, provenance, and backend-
specific artifacts. The initial vfkit variant contains an arm64 raw disk plus an
EFI variable-store template. The initial Cloud Hypervisor variant contains an
x86_64 raw disk plus pinned firmware. A later Firecracker variant may contain a
kernel, initrd, and rootfs while preserving the same logical image ref where its
userspace and protocol provenance are equivalent. Equivalence is manifest evidence,
not a publisher assertion: variants under one logical image ref must share the
canonical userspace/rootfs content digest, SBOM digest, build-provenance ref and
digest, exact guest-agent binary digest, and guest-protocol/schema-set digest.
Variant-specific kernel, initrd, firmware, disk-layout, and boot-artifact refs and
digests remain separate. A mismatch or missing equivalence field requires a distinct
logical image ref. Sharing the logical ref states common userspace and control-
protocol lineage; it does not claim byte-identical boot artifacts or replace
per-variant conformance. A consumer that requires an exact kernel or firmware pins
the variant ref and digest as well as the logical image ref.

The reference guest is intentionally ordinary: a full GNU/Linux distribution,
`systemd` as PID 1, distribution kernel and initramfs, required `virtio_*`
drivers, harmless test modules such as `dummy` or `loop`, the Workbench guest
agent, no `sshd`, no user keys, no cloud credentials, no host mounts, and no
default NIC. Package tests use a pinned read-only repository artifact or disk;
they do not require Internet egress.

Limits are enforced at both strata where meaningful:

- vCPU and guest RAM are fixed by the normalized VMM plan and bounded again by
  host policy;
- working-disk virtual size and a node-wide physical-storage reservation prevent
  sparse images or many concurrent clones from exhausting the host; a native
  quota is used where the platform provides one;
- guest per-command CPU, PID, timeout, output, and filesystem limits are enforced
  by the guest supervisor as defense in depth;
- platform-available host process, memory, CPU, I/O, control-socket, console, and
  storage budgets contain a faulty or hostile guest independently of guest
  cooperation; unavailable controls remain explicit non-capabilities rather than
  implied guarantees;
- serial and vsock channels use bounded ring buffers and backpressure.

The initial reference network profile is `none`: no virtual network device is
attached. A later `isolated` profile may attach a NIC to an explicitly isolated
backend-specific network with no uplink, NAT, or default route. A future
`egress-allowlisted` profile requires its own grant and bounded DNS/proxy/firewall
contract. Linux `netns`/TAP/nftables and macOS user-mode networking are different
mechanisms and must produce separate platform evidence rather than share an
implementation-shaped promise.

#### 7.6 Recovery And Conformance

Process-isolated recovery extends the existing Workbench startup sweep. The
host-private recovery record binds the pinned backend and binary digest,
environment and plan digests, image digest, process identity plus a reuse-safe
start marker, API/control socket identity, boot nonce, working disk identity,
resource-control identities, source generation, and any network resources.
Linux-specific fields such as cgroup, netns, TAP, UID/GID, and `/proc` start time
are present only for Linux profiles; macOS records equivalent process, socket,
disk, and launch identities without pretending that Linux primitives exist.
For Cloud Hypervisor, the reuse-safe process marker binds `/proc/<pid>/stat`,
`comm`, `cmdline`, and `/proc/<pid>/exe` identity while the recovery record and
current host configuration independently bind the pinned binary digest.

Before accepting new environment requests, the broker compares durable records
with live processes, sockets, disks, and platform resource controls; inspects the
VMM; performs the guest handshake; and recovers only an exact plan, image, nonce,
and generation match. Unknown, partial, or contradictory resources are
quarantined and then torn down. A previous-process `running` value is never
authoritative.

`drain` is monotonic and stops new sessions. `teardown` becomes terminal only
after the VMM is gone, control sockets and host resources are removed, retained
storage follows policy, and any requested export is durable. Memory snapshots
and live migration are outside v1 recovery; v1 either recovers the exact live VM
or safely tears it down and recreates from pinned image/storage policy.
An exact live-boot recovery preserves its source generation. Any recreated or new
guest boot advances the generation even when policy preserves the working disk.

The first backend is complete only when deployment evidence covers:

- full boot to `systemd` and a generation/nonce-bound guest-agent handshake;
- harmless kernel module, mount namespace, tmpfs/loop mount, and local package
  repository operations without host effects;
- absence of NIC, host paths, host environment, SSH agent, keychain, host
  credentials, and unallocated sockets;
- file, patch, explicit export, immutable-base-image, and deterministic teardown
  behavior;
- the P083 two-controller fenced PTY conformance suite against the real guest;
- CPU/RAM, guest PID, disk, serial, vsock, queue, timeout, and output exhaustion;
- crash/restart at every allocate/start/drain/teardown boundary, stale boot nonce,
  stale generation, and idempotent replay conflicts;
- bounded `allocate -> agent ready`, PTY round-trip, file/patch/export, physical
  disk amplification, teardown, and reconciliation measurements.

The implemented full-system Story 012 profile reuses the existing three-node Room,
Corpus, Agent, and shared-terminal topology to prove collaborative GNU/Linux
service configuration. It is additive post-MVP acceptance evidence and does not
reinterpret the completed baseline Story 012 gate.

The additive PowerDNS/Bielik specialization uses the same Workbench runtime and
P083 authority boundary. Its image builder may attach vfkit NAT only to the
disposable build VM while installing exact package versions; the final runtime
profile remains no-NIC. Agent/model output stays inert, and node A executes only
the checked-in deterministic configuration sequence after HIL and exclusive
lease admission.

An environment also declares its operational impact through the P082-owned
`sensorium-operational-context.v1` value. A connector or backend may supply an
operator-configured candidate default, but the exact normalized plan pins the
host-effective value before allocation and the resulting
`sensorium-workbench-environment.v1` repeats it. One Workbench deployment may
operate both disposable test workspaces and live production systems. Host policy
may raise the candidate and records the effective value in every derived terminal-
screen, terminal-event, or actuation-interface publication; it may never lower it.
A read-only terminal over a production system remains `production` even though the
published access mode is observation-only. The selected network and host-share
profiles participate only as conservative policy floors; they do not replace the
actual context of a reachable or shared resource.

The environment also exposes a host-owned source generation reference. Replacement,
recreation, or an operational-context change advances that generation or otherwise
invalidates the old publication under P082's current-publication predicate. A change
such as `test -> production` must serialize creation of a new interface publication
and withdrawal of the old one as superseded. An operator may correct an erroneous
overclassification such as `critical -> test` through the same audited replacement
path with an explicit reason; consumer-side local policy still may only raise the
current source declaration.

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
| raw terminal input / signal / resize | `sensorium.workbench.terminal` | Local operator authority remains the default outside collaborative publication. The implemented P083-008 bridge accepts separately granted and fenced remote Sensorium Interface control without representing the caller as the operator. P083-009 adds Room collaboration through a separate current `actuate` grant, an exact interface grant, and the existing lease/generation fencing; Room observation remains separately authorized. |
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

#### Operator Consent Prompting

Workbench and Sensorium OS may later offer an interactive "ask the operator and
remember the answer" path for effects that are **not yet allowed, but are
eligible for operator approval**. This path must reuse the existing host-owned
operator-question and notification primitives instead of creating a
Workbench-specific notification handler.

The consent state machine belongs to the host:

1. A Sensorium adapter or host workflow submits a typed
   `inquirium.operator-question.request.v1` with `recipient/class = operator`,
   a fail-closed `default/on-timeout`, a concrete `operation/ref`, and a
   host-shaped `widget/kind`.
2. The daemon projects the pending question to `notification-create.v1` and
   renders schema-defined notification actions for the operator UI.
3. A node operator answers through the registered notification action target.
   The submitting runtime-auth session must be bound to an active
   `node-operator-binding.v1` whose capability profile is
   `node-primary-operator` (Proposal 034). Ordinary participant
   acknowledgement is not enough to mutate execution policy or persistent
   allowlists.
4. The host records the answer as an auditable operator-question outcome and,
   when granted, emits a domain-specific `operator-consent-decision.v1` record
   that the relevant adapter binding can project into its own allowlist
   sidecar.

The notification is only the presentation and wake-up layer. It does not become
domain authority, and an adapter must not grant itself new authority merely
because it produced the question. The host validates both the runtime-auth
session and its active node-operator binding, records the decision, owns
revocation/list visibility, and controls whether a decision is one-shot or
durable.

The consent lifecycle is layered over the P066 operator-question lifecycle. The
operator question remains `pending -> answered | timed_out | cancelled |
superseded`. The consent decision derived from it is `pending -> granted |
denied | expired`, and a previously granted consent may later become `revoked`
through the host-owned consent registry. `revoked` is therefore a consent-layer
state, not a synonym for P066 `cancelled`.

The minimal decision shape is:

```json
{
  "schema": "operator-consent-decision.v1",
  "schema/v": 1,
  "approval/ref": "approval:consent:sha256:<base64url>",
  "operation/ref": "operator-question:<id>",
  "operator/ref": "node-operator-binding:<id>",
  "consent/decision": "granted",
  "consent/scope": "remember-exact-argv",
  "issued/at": "2026-07-06T00:00:00Z",
  "expires/at": "2026-07-07T00:00:00Z",
  "revocation/ref": null,
  "delta/digest": "sha256:<base64url>",
  "provenance": {
    "source/component": "sensorium-workbench",
    "requested/by": "component:sensorium-workbench",
    "reason/code": "command-profile-missing"
  }
}
```

`delta/digest` covers the concrete intent, not mutable audit metadata:
capability id, operation digest, workspace/root refs when present, proposed
scope, argv/action shape, and safety caps such as timeout, output bytes,
egress, credential policy, and result pointer constraints. This prevents the
same command or action shape from colliding across different workspaces,
capabilities, or safety envelopes.
`approval/ref` is derived deterministically by prefixing the exact
`delta/digest` with `approval:consent:`, so a digest
`sha256:<base64url>` becomes `approval:consent:sha256:<base64url>`.

For Workbench terminal commands, host-shaped choices should be ordered from
narrow to broad:

- `deny` - fail closed and optionally suppress repeated identical prompts for a
  bounded cooldown;
- `allow-once` - allow this exact command intent once without changing durable
  policy;
- `remember-exact-argv` - admit the exact argv, cwd/workspace, capability, and
  profile context as a durable sidecar delta;
- `remember-argv-prefix` - admit a bounded argv prefix plus explicitly declared
  variable-argument prefixes, both capped by host policy;
- `remember-executable-any-args` - a high-risk option that is disabled by
  default and available only under an explicit host policy/capability gate
  registered before implementation. Without that gate the consent layer must
  not render this option even when the widget kind permits it.

For Sensorium OS, the same consent state machine may approve a concrete action
catalog delta, but the binding remains connector-specific: Sensorium OS action
entries use action class, executable, result contract, and
`result_pointer_fields`; Workbench command profiles use argv prefixes, cwd,
environment, egress, timeout, and PTY/output caps. A single generic allowlist
format would hide these differences and should not be introduced.

The recommended persistence shape is hybrid:

- the host keeps a capability-scoped approval ledger/index for list, revoke,
  audit, deduplication, and policy reasoning;
- each adapter receives or materializes an adapter-specific sidecar projection
  that stores only the delta required by that adapter;
- the effective configuration is `main config + sidecar projection`, validated
  after merge before execution;
- sidecars may append admissible entries, but must not silently override safety
  caps such as egress denial, credential policy, maximum timeout, maximum bytes,
  or workspace-root boundaries unless a separate explicit policy says so.

Audit export for this flow is redacted by default. Full argv, parameter
schemas, and action descriptors may be retained only under their classification
policy; exported audit should prefer digest, capability id, source component,
operator binding ref, selected scope, and redacted summaries. Secrets, tokens,
passwords, and raw environment values are never audit payload.

Revoking or expiring a `node-operator-binding.v1` does not rewrite historical
consent facts. The effective sidecar projection must, however, treat any
durable consent whose `operator/ref` points to a revoked or expired binding as
inactive and surface `consent-operator-binding-inactive` in diagnostics.
Likewise, an expired durable consent fact remains auditable history but is not
effective authority; Workbench projections omit it and surface
`consent-expired`. If host authorization policy later removes durable
grantability for the consent capability, the fact likewise remains audit
history, but the effective projection omits it and surfaces
`consent-capability-not-grantable`.

Implementation status 2026-07-07:

- `node:operator-consent-core` defines the host-owned request/decision data
  model, fail-closed timeout requirement, deterministic `delta/digest`, and
  `approval:consent:<delta/digest>` derivation.
- The daemon persists pending/answered/expired/revoked consent records under
  `<data-dir>/storage/operator-consents.sqlite`, exposes submit/list/detail/
  revoke APIs, projects pending requests into P066 operator questions and
  durable notifications, and translates answered operator-question actions into
  `operator-consent-decision.v1`. Operator-consent read and Workbench/Sensorium
  OS sidecar projection endpoints are operator surfaces; module callers are
  rejected fail-closed. Revocation also requires an active local
  `node-operator-binding.v1` and records the active binding ref as the
  revoking operator.
- The P066 notification action dispatcher rejects non-operator callers for
  `inquirium.operator-question.respond`. Consent answers additionally require
  the answering operator participant to own an active local
  `node-operator-binding.v1` with the `node-primary-operator` capability
  profile, and durable answers fail closed unless the target capability is
  grantable under host capability authorization policy. If that host policy
  later removes durable grantability for a capability, existing durable consent
  facts are not deleted, but future effective projections omit them with
  `consent-capability-not-grantable`.
- Workbench emits `sensorium-workbench.consent-descriptor.v1` for
  `command-profile-missing`, accepts `allow-once` and
  `remember-exact-argv` decisions whose descriptor matches the current command
  exactly, and can load a host-projected exact-argv command-profile sidecar
  without loosening egress, credential, timeout, or output-byte caps. The
  connector refreshes the sidecar through a bounded TTL, validates sidecar entry
  schemas, and validates inline consent descriptor schemas before admission.
  The daemon omits expired durable decisions, decisions signed by inactive
  operator bindings, and decisions whose capability is no longer grantable for
  durable consent from the effective sidecar projection, emits
  `consent-expired`, `consent-operator-binding-inactive`, or
  `consent-capability-not-grantable` diagnostics for those skipped entries, and
  the Workbench connector imports sidecar diagnostics into its operator-visible
  config diagnostics.
- Sensorium OS uses the same host-owned consent registry for
  `remember-action-catalog-entry` durable decisions. The daemon projects
  granted Sensorium OS decisions into `sensorium-os.action-catalog-sidecar.v1`
  deltas, writes that sidecar to the Sensorium OS middleware config tree,
  applies the same expired/inactive-binding/no-longer-grantable filters, and
  the connector appends valid non-overriding deltas into its effective action
  catalog while importing projection diagnostics.

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
| Property-attested backend admission | Lets one requirement select different substrates without treating names as security claims. | Adds descriptor, normalization, policy, digest, and per-platform evidence contracts. |
| vfkit first on macOS; Cloud Hypervisor first on Linux | Makes the first full-system proof executable on the primary developer host while retaining a direct KVM deployment path. | Requires two lifecycle adapters and separate host-containment evidence instead of one nominally portable VMM. |
| One bounded guest agent instead of SSH or host shares | Keeps PTY, file, patch, and export semantics common across VMMs and removes credential-shaped control. | The image must carry and update the agent, and all guest-returned state remains untrusted. |
| No memory snapshots in recovery v1 | Keeps boot freshness, source generation, and grant expiry reasoned from live facts. | Recovery may require a slower full boot or teardown/recreate path. |
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
| One adapter-level default labels test and production environments alike. | Pin operational context on the exact environment/resource; treat the adapter value only as an operator-configured candidate default. |
| A read-only viewport is labeled less cautiously than the environment it observes. | Require every derived P082/P083 resource to inherit the environment class; host policy may raise but never lower it. |
| An environment changes impact class while an old interface remains readable. | Advance or invalidate the source generation, publish an immutable replacement, withdraw the old interface as superseded, and let P082 refuse old-generation or superseded reads. |
| A backend name is accepted as proof of isolation or system fidelity. | Match exact host-attested capability properties against a normalized requirement; unknown or unverified properties fail closed. |
| Policy treats an unknown capability string as a new equivalent property. | Use closed, versioned enums for every semantic descriptor dimension and registry-bound backend/platform refs; require schema and conformance changes before a new value can match. |
| A network or host-share profile is added without raising operational caution or inheriting the target context. | Resolve the effective operational context in the normalized plan, apply at least the `test` floor, inherit higher attached-resource classes, and deny unknown target context. |
| Backend-specific image variants share one logical ref without comparable provenance. | Require common userspace, SBOM, build provenance, guest-agent, and protocol/schema-set digests; otherwise issue distinct logical refs and retain exact variant digests. |
| Python gains an administrative VMM socket or arbitrary host process-launch authority. | Keep VMM launch, resource allocation, exact sockets, and teardown in the daemon-owned host broker; provide the adapter only normalized plans and broker-allocated handles. |
| A previous guest boot or restored VM reconnects under current authority. | Bind every handshake and operation to environment, source generation, image/plan digests, and a per-boot nonce; reject stale or contradictory recovery state. |
| Guest root disables guest-agent or guest-cgroup controls. | Treat all guest output as untrusted and retain independent host CPU, memory, storage, process, I/O, socket, and network containment. |
| Guest serial output injects terminal controls or sensitive content into operator diagnostics. | Keep ordinary logs metadata-only; bound and classify explicit captures; sanitize ANSI/control sequences at presentation; apply configured redaction without treating it as complete secret detection. |
| Sparse disks or many APFS clones exhaust host storage. | Combine a fixed virtual-disk maximum with node-wide physical-storage reservation/accounting and a native quota where available. |
| A memory snapshot silently revives expired grants, nonces, or source generations. | Exclude memory snapshots and live migration from v1 recovery; recover only the exact live VM or recreate from pinned image/storage policy. |
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
| `sensorium-virt-backend-capabilities.v1` | Closed host-attested backend/platform refs and versioned enum sets for locality, architecture, isolation, fidelity, transport, device, network, lifecycle, and resource enforcement. |
| `sensorium-virt-environment-plan.v1` | Canonical requirement, selected profile, exact P082 operational context and policy floor, attached-resource context, policy ref, resource plan, image ref, and allocation-idempotency digests. |
| `sensorium-virt-image-manifest.v1` | Logical full-system image whose shared userspace/SBOM/provenance/agent/protocol digests prove variant equivalence while exact boot artifacts remain variant-specific. |
| `sensorium-virt-recovery-record.v1` | Host-private identity for VMM process, sockets, working storage, boot nonce, source generation, platform resources, and reconciliation status. |
| `sensorium-virt-guest-frame.v1` | Bounded handshake and operation envelope for the guest channel, including environment/generation binding, sequence, deadline, chunk caps, and payload digest. |
| `sensorium-virt.host.request.v1` | Closed internal ingress envelope for fixture, vfkit, and Cloud Hypervisor allocation, exact environment start/inspect/drain/teardown/recover bindings, and authoritative host reconciliation. Caller payloads never select host paths, VMM binaries, sockets, or argv. |
| `sensorium-virt-vfkit-deployment-report.v1` | Closed metadata-only evidence report with the exact vfkit check set, VMM/image/firmware/guest digests, operational context, functional timing budgets, and bounded measurements. |
| `sensorium-virt-cloud-hypervisor-deployment-report.v1` | Closed metadata-only Linux/KVM evidence report with the exact Cloud Hypervisor check set, VMM/image/firmware/guest digests, operational context, continuously bounded serial evidence, and measurements constrained by explicit functional budgets. |
| `sensorium-terminal-session.v1` | Session descriptor: command profile, workspace, classification, limits, status. |
| `sensorium-terminal-command.v1` | Structured command intent with command profile, argv data, idempotency key, and normalized argv digest. |
| `sensorium-terminal-input.v1` | Bounded raw input event to an existing session. |
| `sensorium-terminal-event.v1` | Append-only output/status event. |
| `sensorium-terminal-screen-snapshot.v1` | Bounded model/UI view over recent terminal state. |
| `sensorium-workbench-error-codes.v1` | Shared runtime diagnostic code vocabulary for Workbench refusal, recovery, patch, artifact, file, terminal, wait, and configuration failures. |
| `interaction-broker-watch.v1` | Cursor-bound subscription over a registered source provider with caps, TTL, and classification. |
| `interaction-broker-wait.request.v1` | Declarative bounded condition over observations, with deadline and idempotency key. |
| `interaction-broker-wait.outcome.v1` | Domain result/projection for a satisfied or terminal wait condition; async lifecycle status is still `deferred-operation-status.v1`. |
| `interaction-broker-probe.v1` | Active bounded check for liveness, readiness, file state, artifact presence, or progress. |
| `sensorium-file-snapshot.v1` | Directory/file metadata snapshot under an allowlisted root. |
| `sensorium-file-read-result.v1` | Bounded file content or artifact ref. |
| `sensorium-workbench-patch.v1` | Patch proposal artifact and metadata. |
| `sensorium-workbench-patch-apply-result.v1` | Applied/rejected patch result with changed files and digests. |
| `sensorium-workbench-outcome.v1` | Host audit fact linking directive id, grant, caller, session/environment refs, status, timing, byte counts, and artifacts. |
| `sensorium-actuation.bridge.request.v1` | Bounded request from the Python connector to the Rust actuation validator. |
| `sensorium-actuation.bridge.response.v1` | Fail-closed Rust validation result with typed diagnostics. |
| `sensorium-virt-workspace-export.v1` | Bounded content bundle exported from a managed virtual workspace. |
| `sensorium-virt-export-result.v1` | Artifact descriptor and counts produced by explicit virtual workspace export. |
| `sensorium-virt-teardown-result.v1` | Terminal lifecycle and cleanup result for managed environment teardown. |
| `sensorium-workbench-tool-request.v1` | Host-verified Agent, Corpus, or Room lineage around a Sensorium Workbench directive. |
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
- A backend id is never accepted as isolation evidence without a matching
  host-attested capability descriptor and normalized plan digest.
- The reference full-system profile has no NIC, SSH service, host share,
  credential injection, or arbitrary host socket.
- VMM lifecycle authority, working-storage allocation, platform resource controls,
  and recovery remain daemon-owned; the Python adapter receives only exact
  broker-allocated handles.
- Every guest boot has a fresh nonce bound to environment, image, plan, source
  generation, and the dedicated control endpoint.
- Guest-agent output is untrusted; guest-side cgroups and supervisors do not
  replace independent host resource containment.
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

No unresolved questions remain for the current local Workbench foundation,
Phase 3A operator-consent slices, or the frozen Phase 4 full-system backend
architecture. Backend-specific implementation findings may reopen only a
bounded property or profile decision; they must not be hidden as adapter-local
behavior.

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
8. **Raw PTY input.** Raw PTY input remains operator-only outside an explicitly
   published actuation interface. Model-driven workflows normally use structured
   command/file intents, while the implemented P083-008 bridge permits separately
   granted remote terminal bytes only under the exact exclusive lease, generation,
   epoch, sequence, method, deadline, and Workbench session checks defined by
   [Proposal 083](083-sensorium-interactive-interfaces.md). P083-009 now derives the
   canonical remote caller from a current Room `actuate` session and still requires
   the exact interface grant and fenced lease. Observation never turns into command
   authority, and the remote caller is never represented as operator.
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
21. **Shared actuation core adoption.** Python Sensorium OS remains a separately
   audited reference connector, while Workbench consumes
   `sensorium-actuation-core` through a bounded required companion process with
   no Python validation fallback. The shared core is the contract plus golden
   vectors from day zero, not merely the Rust crate. Canonical rules for path
   canonicalization, symlink escape refusal, allowlists, command profiles, and
   classification must be expressed as data/reference rules with golden vectors. The
   Rust `sensorium-actuation-core` carries those vectors as the reference
   implementation; Python Sensorium OS must run the same conformance vectors.
   Workbench uses `sensorium-actuation.bridge.{request,response}.v1` over a
   64-KiB fail-closed process boundary rather than embedding Rust through FFI.
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
30. **Command profile validation source.** The Python Workbench connector calls
    the required `orbiplex-sensorium-actuation-contract` companion process for
    command-profile and relative-path decisions. Missing, malformed, timed-out,
    or refused responses fail readiness or the affected request closed. Shared
    golden vectors remain the cross-language conformance layer.
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
34. **Operator consent prompting.** Interactive approval for new Sensorium OS or
    Workbench operations reuses host-owned `inquirium.operator-question.request.v1`
    projected through durable notifications. The host owns the state machine,
    runtime-auth session validation against an active
    `node-operator-binding.v1`, audit, revocation/list visibility, and durable
    approval ledger. Adapters own only the binding from a granted decision into
    their adapter-specific sidecar projection; they may request consent but must
    not mutate their own authority outside the host approval path.
    Durable grants amplify authority and therefore require an explicit
    affirmative operator action from an active runtime-auth session bound to an
    active `node-operator-binding.v1`, plus a host grantability
    policy/capability gate for the requested consent scope. A detached operator
    signature may be added later for high-risk or long-lived consent classes,
    but it is not required for the MVP path.
    If one runtime-auth session can present more than one active operator
    binding, one applicable `node-primary-operator` binding is sufficient; the
    selected binding must be deterministic or explicitly selected by the host
    and recorded as `operator/ref`.
35. **Consent revocation authority.** Revoking a durable consent in the MVP
    requires an authenticated active node-operator runtime session bound to an
    active `node-operator-binding.v1`; it does not require a fresh detached
    operator signature. This is acceptable because revocation reduces authority.
    The audit record must still capture the runtime session ref, operator
    binding ref, timestamp, target consent, and reason.
    Revocation uses a dedicated operator surface,
    `POST /v1/operator-consents/{approval_ref}/revoke`, with `approval_ref`
    URL-encoded. It is not represented as another
    `inquirium.operator-question.respond` answer, because it acts on an already
    materialized durable consent rather than on a pending question.
36. **Effective sidecar merge timing.** Effective sidecar projections are cached
    with deterministic invalidation on consent grant, revocation, expiry,
    main-config changes, and node restart/warm-recovery when the shared sidecar
    merge primitive owns the projection. The current Workbench connector
    implementation uses a bounded sidecar refresh TTL, validates the refreshed
    sidecar before use, and consumes the validated projection rather than
    treating a startup snapshot as final.
37. **Bounded argv-prefix consent.** `remember-argv-prefix` is limited by host
    caps for fixed prefix length and variable-prefix count. The effective
    profile is bound to the exact workspace/root/path context reviewed by the
    operator and may not widen egress, credential environment, timeout, or
    output-byte policy. Arbitrary executable plus arbitrary argv remains denied.
38. **First Sensorium Virt executor.** `fixture-copy.v1` is a managed-copy
    executor, not a process sandbox. It copies a bounded symlink-free source
    root under the Workbench data directory, permits approved writes only to the
    managed copy, supports explicit bounded artifact export, and deletes only
    the managed copy on operator-confirmed teardown. PTY stays unavailable until
    a backend provides process isolation.
39. **Product tool-request lineage.** Agent, Corpus, and Room use
    `sensorium-workbench-tool-request.v1` as an optional request profile of
    `sensorium.directive.invoke`, not as a direct connector route. The host
    verifies the admitted effect proposal, active Corpus round, or current
    execution-derived answer-room membership before stamping lineage and passing the ordinary directive to
    Sensorium Core. One Agent effect proposal binds to one `directive/id` with
    replay of that same directive allowed.
40. **Operational impact belongs to the exact environment.** An adapter may define
    a default `sensorium-operational-context.v1`, but each Workbench environment
    pins its candidate class. Host policy may raise it, never lower it, and every
    derived P082/P083 publication inherits the resulting value and source generation.
    Read-only access does not reduce the class of a production or critical source.
    Source-side correction uses a reasoned immutable replacement; it is not blocked
    by the consumer-side monotonicity rule.
41. **Backend properties, not backend names, prove suitability.** Process-isolated
    allocation requires a host-attested backend capability descriptor matched
    conjunctively against a normalized environment requirement. Missing or
    unverified isolation, fidelity, transport, device, network, host-share, or
    resource-enforcement properties fail closed. The selected plan and image are
    digest-bound to idempotency and recovery. Operator configuration pins the
    required properties and registries, not fixture-generated image or capability
    refs whose values are content-derived. Workbench verifies that the returned
    `backend/id` equals the selected executor; exact capability, variant, and image
    refs/digests remain host-derived evidence bound by the normalized plan.
42. **Reference full-system backend sequence.** `vfkit-system.v1` on
    `macos-vz-arm64.v1` is the first developer reference and first implementation
    slice. `cloud-hypervisor-system.v1` on `linux-kvm-x86_64.v1` is the first Linux
    deployment profile. `firecracker-system.v1` follows after the guest protocol
    and image manifest stabilize as the smaller-device hardened Linux profile.
    This ordering serves the GNU/Linux configuration proof and is not a universal
    VMM security ranking.
43. **VMM lifecycle and guest mechanics are separate ports.**
    `EnvironmentBackend` owns allocate/start/inspect/drain/teardown/recover
    mechanics. `GuestWorkbenchChannel` owns bounded process, PTY, file, patch,
    export, quiesce, and shutdown mechanics over one shared guest protocol. SSH,
    a network interface, and host filesystem sharing are not Workbench semantics.
    Each backend advertises the exact supported lifecycle subset. The processless
    `fixture-copy.v1` allocation reaches `ready` atomically and therefore does not
    advertise a separate `start`; its `recover` support is the host-owned
    reconciliation sweep, not caller-selected resurrection of one environment.
44. **Rust owns validation and host authority; Python owns connector mechanics.**
    A pure `sensorium-virt-core` validates capabilities and plans. A daemon-owned
    host broker allocates storage and platform resources, launches and reconciles
    VMMs, and issues exact control handles. The Python Workbench adapter maps
    normalized plans to bounded broker requests and guest-channel RPC without a
    validation fallback, VMM administrative socket, or ambient host authority.
45. **Guest control uses a bounded virtio-vsock agent.** The reference image runs
    `orbiplex-workbench-guest` without IP or SSH. Every boot uses a fresh nonce;
    handshake and operations bind environment, source generation, plan/image
    digests, sequence, deadlines, byte/chunk caps, and payload digests. The guest
    owns no policy and all returned state remains untrusted.
46. **Default VM posture is no-device network and no host sharing.** The initial
    vfkit deployment profile attaches only block, vsock, and entropy; diagnostic
    serial remains disabled until its retained output has a continuously enforced
    bound. A later Cloud Hypervisor profile may add the separately evidenced,
    output-only bounded diagnostic serial device. vfkit maps guest AF_VSOCK to one broker-
    allocated host Unix socket. OCI may distribute pinned image artifacts but
    does not own lifecycle. Isolated networking is a later, separately evidenced
    platform profile.
47. **Recovery v1 does not use memory snapshots.** Startup reconciliation binds
    exact process/socket/storage identities, boot nonce, plan/image digests, and
    source generation. It recovers only an exact live match; partial or unknown
    resources are quarantined and torn down. Memory snapshots and live migration
    remain excluded until freshness and authority semantics receive a separate
    contract. A `hardware-vm` record in `ready` or `draining` must carry process,
    control-socket, and boot-nonce identity; a processless fixture record omits
    those fields. `recorded-at` is validated evidence, not an ordering authority:
    lifecycle transitions and exact generation/resource identities establish
    freshness even when a host wall clock moves backwards.
48. **Operational context is part of the normalized VM plan.** The host resolves
    the exact P082 context before allocation and binds the candidate digest,
    effective value, and policy ref into the plan digest. Non-`none` networking or
    non-denied host sharing has a minimum `test` floor, then inherits any higher
    reachable/shared-resource class. Missing target context denies allocation. Every
    guest observation and actuation interface inherits the resulting context and
    source generation without backend or carrier reinterpretation. The reference
    full-system configuration proof is `test`; a contained offline disposable VM may
    remain `experimental`, because isolation class and operational impact are
    orthogonal. The candidate digest binds the pre-policy candidate and therefore
    intentionally need not equal the digest of the effective context after a floor
    or attached-resource raise. The current Workbench default remains `test`;
    selecting `research` or `experimental` for a contained offline environment is
    an explicit operator decision, not an inferred downgrade.
49. **Logical image equivalence requires comparable provenance.** Backend variants
    share one logical image ref only when the manifest proves identical canonical
    userspace/rootfs, SBOM, build provenance, guest-agent binary, and guest-protocol/
    schema-set digests. Kernel, initrd, firmware, disk layout, and boot artifact
    identities remain variant-specific and independently conformance-tested.
50. **Backend capability semantics use closed versioned vocabularies.** Semantic
    dimensions in `sensorium-virt-backend-capabilities.v1` are enums and bounded
    enum sets with no additional properties. Backend and platform identities resolve
    through host registries. New values require a schema/registry revision and
    evidence; policy cannot bless an unknown string as equivalent.
51. **Diagnostic serial is an untrusted output artifact.** It is output-only and
    bounded, absent from ordinary content logs, and never rendered raw. Explicit
    captures inherit environment classification and operational context, carry
    digest/truncation metadata, pass configured redaction, and are sanitized against
    ANSI and other control-sequence injection at the operator presentation boundary.
52. **The standalone Sensorium Virt companion is an explicit development path.**
    `virt_host.standalone_companion_enabled` is a literal boolean, defaults to false,
    and may be enabled only together with the closed
    `virt_host.standalone_companion_purpose = development|conformance` value. A
    missing, ill-typed, or production-purpose value cannot enable it. Supervised
    production/channel mode never falls back to
    the companion when the daemon runtime or `sensorium.virt.host` capability is
    absent; the environment refuses admission instead. Both the daemon and companion
    boundaries expose only a bounded typed code plus a stable public message. Raw host
    paths, subprocess stderr, internal exception text, and capability failure details
    remain host-local diagnostics.
53. **Disabling a VMM profile preserves only terminal cleanup authority.** A
    literal `vfkit.enabled = false` denies allocate, start, recover, inspect, and
    drain. When the complete operator-pinned profile remains available, the daemon
    may load it only for `environment.teardown` and `host.reconcile`; this permits
    bounded resource removal without silently retaining the ordinary lifecycle.
    A missing `enabled` field is reported as not configured, not as an explicit
    operator disable.
54. **Guest operations are serialized per environment in V1.** The production
    guest agent owns one `GuestRuntime` and synchronously accepts one connection,
    executes at most one operation, and closes that exchange before accepting the
    next connection. The host lifecycle lock protects authoritative record and
    endpoint selection but is not held across guest I/O. Multiple pending host
    connections therefore do not imply parallel guest effects. Any future
    parallelism requires a separate partitioned-concurrency contract with explicit
    ordering and conflict semantics.

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
  Workbench. `node/sensorium-actuation-core` owns the Rust reference rules and
  golden vectors. Workbench invokes its bounded companion-process contract for
  path and command-profile admission; Python Sensorium OS remains conformance-
  bound without sharing Workbench process lifecycle.
- [x] Define `sensorium-workbench-environment.v1`.
- [x] Define terminal session/command/raw-input/event/snapshot schemas. The accepted
  terminal observation model separates a bounded viewport snapshot from an
  append-only exact-byte event feed. The event schema uses closed per-kind shapes,
  digest-bound base64 output, content-free input acknowledgements, and explicit
  lifecycle events.
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
  serialized byte/count caps before projection. The daemon broker registers
  long waits in the host deferred-operation registry and projects their terminal
  outcomes through the canonical status contract.
- [x] Decide MVP policy for raw PTY input. Decision: operator-only in MVP.
- [x] Decide MVP wait conditions and no-progress vocabulary. MVP waits cover process
  exit, stdout/stderr pattern, file exists/changes, and timeout; `maybe_hung` is
  diagnostic only.
- [x] Define the adversarial actuator test matrix as a required acceptance
  suite. The matrix is now specified as a refusal-first release gate and must be
  encoded as `sensorium-actuation-core` golden vectors plus Python connector
  conformance tests before write/PTY runtime surfaces are enabled. Published
  relative-path and command-profile golden vectors are published and consumed by
  Rust and the Python Workbench connector tests; they reject traversal, embedded
  current-directory components, trailing slash forms, backslash separators,
  missing fixed argv prefixes, disallowed executables, and variable argv atoms
  outside explicit allowlisted prefixes.
- [x] Enforce the Phase Release Gates before Phase 1+ runtime work: frozen schemas for
  exposed surfaces, registered capabilities, documented storage/recovery contract, and
  executable refusal-first golden vectors for the relevant effect classes.
- [x] Bind Python Workbench decisions to `sensorium-actuation-core` through a
  stable process boundary. The required bounded companion-process bridge owns
  relative-path and command-profile decisions, and the connector fails closed
  when the bridge is absent, unavailable, times out, or returns a malformed
  response. Development and test profiles do not enable a Python fallback.

### Phase 1 - Local Workbench Connector

- [x] Add a supervised local Workbench connector module. Node now ships the
  opt-in `middleware-modules/sensorium-workbench` Python connector with
  `/healthz`, `/readyz`, `/shutdownz`, `/v1/middleware/init`, status/config,
  factory config, and daemon factory/inventory coverage. It uses
  `seed_config: false` and remains disabled until an operator configures it.
- [x] Consume the shared actuation core instead of reimplementing path,
  command-profile, allowlist, classification, and argv rules. The connector
  calls the required Rust companion process for relative-path and command-
  profile decisions and is tested against shared golden vectors plus
  traversal, root-self, symlink-traversal refusal, oversized reads, dangerous env
  stripping, command-profile denial, bridge timeout/unavailability, and malformed
  response refusal.
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
  SQLite with full-record event/byte/age retention caps, exposes event cursors and
  explicit retained-floor gaps, and supports resize/signal/close under explicit
  terminal grants. Output events preserve exact PTY bytes; accepted or rejected
  input records never retain input content. Factory config keeps the runtime disabled until an operator
  sets `terminal_enabled: true` and provides command profiles.
- [x] Enforce PTY session, reader-task, input queue, and event buffer caps with
  explicit overload/refusal outcomes. Laptop defaults remain `2` sessions,
  `4` reader tasks, queue depth `256`, and event buffer `1000`; the connector
  also caps command timeout and output bytes.
- [x] Implement watch cursors for terminal and generalized source events. The
  connector exposes bounded synthetic/local event cursors for environment/read/probe
  events and per-session terminal event cursors; the host broker adds stable
  snapshot cursors for file-tree, Artifact Delivery, approval/consent,
  Memarium-query, and dynamically registered sources. Operation outcomes remain
  in the canonical deferred-operation status/wait path instead of introducing a
  second cursor-bearing lifecycle model.
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
- [x] Implement TTL, idle timeout, byte caps, process cleanup, and refusal
  diagnostics. Request body caps, file read byte caps, terminal command timeout,
  command output byte caps, session caps, process termination on close/timeout,
  startup orphan process signaling, event payload caps, SQLite retention cleanup,
  typed refusal diagnostics, and opt-in `terminal_idle_timeout_ms` idle cleanup
  for open non-running sessions on terminal admission paths exist. `/v1/status`
  remains a read-only projection and does not close sessions. By policy,
  running commands are governed by `command_timeout_ms`, explicit close, or
  operator signal rather than an idle sweep.
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
- [x] Use Bounded Deferred Operations for environment setup or command runs that
  outlive one HTTP request. The current terminal command endpoint returns
  `202 accepted` and exposes event/wait polling. Async waits now return the
  canonical `deferred-operation.v1` / `deferred-operation-status.v1` shapes,
  require an explicit wait grant for status reads, de-duplicate by
  `idempotency/key`, mark interrupted pending/running wait operations as failed
  with retry diagnostics on startup, and mark previously starting/running
  terminal commands plus failed terminal-command spawn attempts as failed for
  bounded post-restart/idempotent replay. Terminal command runs invoked through
  the daemon host capability surface now register daemon-owned
  `sensorium-workbench.terminal-command` Bounded Deferred Operations and poll
  command state through the host Interaction Broker terminal provider. Daemon
  cancel for those command BDOs now calls the Workbench
  `sensorium.workbench.terminal.command.cancel` action with a host-owned
  operator-confirmed grant, maps the connector transition through
  `cancel_requested` / `signaled` / `terminated` / `cancel_failed`, and projects
  terminated commands as canonical BDO `cancelled` status. Terminal
  `command.done` events now carry `signal_origin` so timeout-driven `SIGTERM`,
  operator cancel, and ordinary process exit remain distinguishable in the event
  stream.
- [x] Run the adversarial actuator test matrix before enabling write or PTY
  features by default. The executable conformance and acceptance suites cover traversal, root self,
  symlink traversal, oversized files, grant-required mediated read, command
  profile denial including variable argv beyond a fixed prefix, dangerous env
  override stripping, credential-like env override refusal before command start,
  request/profile egress refusal, operator-only raw input denial, retired
  session refs, residual-child startup recovery status diagnostics, and a PTY
  happy path. It now also covers artifact digest mismatch, terminal capture
  to artifact, terminal-capture artifact-write grant refusal, delete-forbidden
  patch apply, successful structured patch apply, structured patch rollback on
  partial write failure, connector-local deferred wait projection, operation
  status grant refusal, connector idempotency-key refusal/conflict, interrupted
  operation recovery, interrupted terminal-command recovery, failed-spawn
  terminal-command replay, TTL cleanup for replay records, idempotent replay for
  terminal command/cancel/capture/artifact/patch effects, an executable PTY story
  smoke, a Python Workbench actuation conformance runner against shared golden
  vectors, and the daemon rule that Inquirium cannot directly invoke Sensorium
  connectors. It now also covers the `fixture-virtual-workspace` managed-copy
  executor: source-copy caps and symlink refusal, approved patching only in the
  copy, bounded export, source immutability, persisted lifecycle, idempotent
  teardown, and PTY refusal without process isolation.

### Phase 2 - Sensorium Integration

- [x] Add Sensorium Core capability routing for Workbench directives. The
  connector exposes `/v1/sensorium/connector/invoke` and Workbench action ids
  for Sensorium Core mediated routing; Sensorium Core already dispatches
  allowlisted connector directives with directive metadata and idempotency.
- [x] Route cross-source waits through the host interaction broker rather than
  making Sensorium Core own AD, Memarium, approval, or deferred-operation joins.
  The daemon broker now owns grant-context admission for JSON-e/module
  wait/watch/probe calls through daemon-issued host-local HMAC grant material
  requested by `bindings.host_grant_requests`, keeps deferred-operation
  `OperationDone` waits host-owned, and wires live Workbench file-tree plus
  terminal providers for file probes, file waits, file-tree watch batches,
  terminal liveness/progress probes, terminal waits, and terminal watch batches.
  Dynamic non-Workbench provider registration/status APIs now exist with
  bounded observed-state joins for artifact, environment, approval, and
  Memarium-query providers, including `approval-state` and
  `memarium-query-state` wait conditions. Domain-native Artifact Delivery,
  approval/consent, and Memarium-query providers now expose bounded snapshots
  and stable watch cursors; other domains join through dynamic registration.
- [x] Add grant and policy checks for terminal command, terminal raw input,
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
- [x] Record directive outcomes and metadata-only traces. Terminal runtime now
  records sessions, commands, events, terminal captures, local artifacts,
  connector-local deferred waits, patch applications, idempotency replay
  records with bounded replay TTLs, startup recovery diagnostics, lifecycle
  diagnostics, and metadata-only outcomes durably in connector SQLite or bounded
  in-process operator status. Host broker audit and explicit artifact handoff
  audit are implemented. Session refs are retired after first use to keep the
  audit trail unambiguous.
- [x] Add operator status/control surfaces for active sessions and sandboxes.
  `/v1/status` reports terminal enablement, PTY caps, active session count,
  session summaries, startup recovery diagnostics, lifecycle diagnostics, and
  idle-closed session diagnostics when admission paths sweep sessions under
  configured `terminal_idle_timeout_ms`; the status endpoint itself stays
  read-only. Session close and managed virtual-environment teardown are explicit
  control surfaces.
- [x] Expose active waits, watches, deadlines, and suspected no-progress states
  in operator status. Event cursors, command status, connector-local active wait
  count/status, no-progress probe diagnostics, host-broker status/providers/
  resource read APIs, provider health, ownership, recent resources, and
  remediation paths are exposed in node-ui.
- [x] Link captured outputs through Artifact Delivery or Memarium only under
  explicit classification and retention policy. Terminal capture now writes a
  bounded local artifact descriptor with classification and provenance. The
  daemon verifies bytes and descriptor digest/size before explicit idempotent
  Artifact Delivery resolver and/or metadata-only Memarium handoff.
  Handoff replay binds `idempotency/key` to both the normalized request and
  `correlation/id`, preventing retries from being attributed to another trace.

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
- [x] Add story-level Workbench PTY acceptance smoke. Implemented as
  `node:tools/acceptance/workbench-pty-story.py`; it creates a terminal
  session, runs allowlisted argv through the PTY, waits for command completion,
  reads bounded terminal events, captures them to an artifact, replays
  idempotent command/capture calls, and checks fail-closed command-profile and
  raw-input refusal paths.
- [x] Add shared Workbench actuation conformance runner. Implemented as
  `node:tools/conformance/workbench_actuation_conformance.py`; it validates the
  Python connector against shared relative-path and command-profile golden
  vectors plus runtime refusal invariants for command profile, no-egress, and
  credential-env denial. P083-010 extends it with a real interactive shell PTY,
  two fenced Sensorium controller authority shapes, resize/input markers, signal,
  and bounded process completion.
- [x] Add the shared Agent/Corpus/Room Workbench tool-request boundary.
  `sensorium-workbench-tool-request.v1` wraps an ordinary
  `sensorium.directive.invoke` request. The daemon verifies Agent proposal and
  parameter digest, active Corpus round ownership, or current execution-derived
  answer-room membership,
  stamps host-owned lineage, and then uses Sensorium Core. It never exposes a
  direct Workbench connector route to those products.

### Phase 3A - Host-Owned Operator Consent For Allowlist Deltas

- [x] Define `operator-consent-core` as a pure host-owned contract layer. It
  should model consent requests, operation descriptors, selectable scope
  options, deduplication keys, TTLs, fail-closed timeout defaults, decision
  statuses (`pending`, `granted`, `denied`, `expired`, `revoked`), and the
  distinction between `operator_confirmed` authority and ordinary
  `user_acknowledged` visibility. It should also define the
  `operator-consent-decision.v1` payload shape and the mapping from P066
  operator-question lifecycle states to consent decision states. It must define
  `approval/ref` as `approval:consent:<delta/digest>`, e.g.
  `approval:consent:sha256:<base64url>`.
- [x] Add a daemon-owned consent registry and audit ledger under the node
  data-dir. The natural key should include capability id, source component,
  operation digest, workspace/root ref when present, proposed scope, and
  requester. The registry must support idempotent request replay, list, detail,
  revoke, expiry sweep, duplicate suppression, and redacted audit export.
  Revocation is authorized by an authenticated active node-operator runtime
  session bound to an active `node-operator-binding.v1`; it does not require a
  fresh detached operator signature in the MVP.
  Redacted export must omit secret material and raw environment values, and
  should prefer digests plus redacted summaries for argv, parameters, and
  action descriptors.
- [x] Reuse `inquirium.operator-question.request.v1` and durable notifications
  for the prompt/answer surface. The consent layer should build a typed
  operator question with `recipient/class = operator`, registered widget kind
  `single-choice`, a fail-closed `default/on-timeout`, and a response target
  owned by the daemon. No Sensorium adapter should create its own notification
  action handler.
- [x] Reuse the P066 notification projection and answer routing
  (`assistant-interaction-notification-projection` and action target
  `inquirium.operator-question.respond`) instead of adding another notification
  handler. The consent answer handler should validate that the submitting
  runtime-auth session is bound to an active `node-operator-binding.v1` with
  `node-primary-operator` and that the requested durable grant passes the host
  grantability policy/capability gate, then translate the selected option into
  an `operator-consent-decision` record without letting the adapter mutate
  policy directly. The implemented exact-argv path performs active binding
  validation at answer time and fails closed for durable scopes whose
  capability is not grantable by host capability authorization policy.
- [x] Define Workbench consent scope choices. The supported options are
  `deny`, `allow-once`, `remember-exact-argv`, and
  `remember-argv-prefix`. `remember-executable-any-args` is a high-risk
  optional policy extension and must remain disabled unless an explicit
  host policy/capability gate enables it; the gate must be registered before
  runtime implementation and the option must be hidden when the gate is absent.
  `remember-argv-prefix` has host-policy caps for maximum fixed prefix length
  and maximum variable-prefix entries. The runtime admits deny, allow-once,
  exact argv, and workspace-bound bounded prefixes. It does not expose
  arbitrary-executable consent.
- [x] Implement the Workbench sidecar projection. A granted durable decision
  should append a command-profile delta scoped by workspace/root, cwd policy,
  argv exact/prefix data, allowed variable prefixes, environment policy,
  egress policy, timeout/output caps, approval ref, operator ref, expiry, and
  revocation ref. The projection must not raise safety caps or loosen egress,
  credential, workspace, timeout, or byte limits beyond the main policy.
  Its approval digest must cover capability id, operation digest,
  workspace/root refs, proposed argv scope, and safety caps, not just argv text.
  The reviewed Workbench consent descriptor is published as
  `sensorium-workbench.consent-descriptor.v1`. The implemented projection
  supports exact argv and bounded workspace/root/path-bound argv prefixes,
  validates command-profile sidecar entry schema
  ids, rejects inline decisions whose descriptor schema is not
  `sensorium-workbench.consent-descriptor.v1`, and refreshes the sidecar
  through a bounded TTL. The effective daemon projection filters entries whose
  `operator/ref` no longer points to an active local
  `node-operator-binding.v1` and reports
  `consent-operator-binding-inactive`, filters expired durable consent and
  reports `consent-expired`, filters capabilities no longer grantable for
  durable consent and reports `consent-capability-not-grantable`, and leaves
  those diagnostics visible to the Workbench connector.
- [x] Define the Sensorium OS action-catalog sidecar projection. A granted
  Sensorium OS decision should materialize a catalog delta shaped like P048
  action declarations: action class, executable or script root, argv shape,
  parameter schema, limits, result contract, `result_pointer_fields`,
  sensitivity, approval ref, operator ref, expiry, and revocation ref. The
  consent descriptor should be promoted to its own schema rather than an
  untyped inline blob inside the operator-question request. The descriptor
  schema is published. The implemented daemon projection emits
  `sensorium-os.action-catalog-sidecar.v1`, publishes the binding/delta/sidecar
  schemas, writes the sidecar to the Sensorium OS middleware config tree,
  reuses the same effective durable filters as Workbench, and the connector
  loads append-only non-overriding deltas before running its existing
  action-catalog validator.
- [x] Add a shared sidecar merge primitive for adapter config deltas. It
  lives beside the existing path/config utility strata, supports append-only
  allowlist deltas first, reports merge provenance, and requires schema
  validation after `main config + sidecar` is composed. Avoid generic
  deep-override semantics for security-sensitive caps. Sidecar entries whose
  `operator/ref` points to a revoked or expired node-operator binding must be
  inactive in the effective projection. `node:config-sidecar-core` now owns the
  append-only provenance-preserving merge and conflict semantics used by the
  Workbench and Sensorium OS projections; both still validate the composed
  adapter-specific schema before activation.
- [x] Add operator UI/API surfaces for consent visibility and revocation:
  pending requests, answered decisions, durable sidecar entries, expiry,
  selected scope, operation digest, source component, operator ref, issued/at,
  expires/at, revocation/ref, delta/digest, and revoke/deny actions. Revocation
  uses `POST /v1/operator-consents/{approval_ref}/revoke`, not the
  operator-question answer endpoint. The UI should make it clear which entries
  are one-shot, durable, expired, or revoked. The daemon API and dedicated
  node-ui consent screen expose this state and revoke action.
- [x] Add integration tests and fixtures. P066-owned primitives cover request
  deduplication, timeout fail-closed, widget contract validation, and duplicate
  answer replay metadata. P071-owned tests should cover deny, allow-once
  without sidecar mutation, remember-exact argv, remember-prefix, active
  node-operator-binding enforcement, participant-only denial of consent,
  sidecar merge validation, stale/inactive operator binding diagnostics,
  revocation removal from the effective projection, and refusal of attempts to
  loosen safety caps. Current coverage includes core digest/timeout validation,
  registry request/answer/replay/projection behavior, semantic duplicate
  request replay after deny/grant/revoke, Workbench consent denial,
  exact-decision admission, consent-disabled denial, operator-read endpoint
  module-caller denial, active-binding revoke authority, expired durable
  projection filtering, sidecar schema validation, dynamic sidecar refresh,
  imported sidecar diagnostics, prefix workspace/root/path binding, shared merge
  conflicts/provenance, and sidecar cap-refusal tests.

### Phase 4 - Virtualized Backends

- [x] Define the first `Sensorium Virt` backend contract for the same
  environment, file, patch, artifact export, lifecycle, and teardown
  abstractions. The synchronized environment/export/result schemas preserve the
  boundary for later process-isolated executors.
- [x] Implement the first managed virtual executor. `fixture-copy.v1` copies a
  bounded symlink-free source tree under the Workbench data directory and
  permits approved patching only against that copy. It is disposable but is not
  described as a process sandbox; PTY stays unavailable.
- [x] Freeze process-isolated backend admission as a conjunction of host-attested
  properties rather than a backend-name allowlist. The selected reference sequence
  is `vfkit-system.v1` on `macos-vz-arm64.v1`, then
  `cloud-hypervisor-system.v1` on `linux-kvm-x86_64.v1`, followed by a separately
  hardened Firecracker profile.
- [x] Publish `sensorium-virt-backend-capabilities.v1`,
  `sensorium-virt-environment-plan.v1`, `sensorium-virt-image-manifest.v1`,
  `sensorium-virt-recovery-record.v1`, `sensorium-virt-guest-frame.v1`, and the
  closed internal `sensorium-virt.host.request.v1` envelope plus
  `sensorium-virt-vfkit-deployment-report.v1` with
  positive and refusal fixtures. Capability dimensions must use the closed V1
  vocabularies above and refuse unknown enum values and unregistered backend or
  platform refs. The normalized plan must bind the exact P082 operational context,
  its candidate digest, policy ref, selected network/host-share floor, and attached-
  resource context. The image manifest must prove logical-variant equivalence from
  common userspace, SBOM, provenance, guest-agent, and protocol/schema-set digests.
  The canonical schemas, positive examples, refusal fixtures, Node protocol mirrors,
  and schema-gate mappings are present.
- [x] Evolve the environment projection to carry only exact refs/digests from those
  host-owned contracts rather than backend claims. The fixture projection now
  carries the host-returned plan, capabilities, image-variant, generation, and
  recovery refs/digests; the same metadata is persisted in the Workbench store.
- [x] Implement `sensorium-virt-core` capability/plan/image/lifecycle/recovery and
  guest-frame validation plus a bounded fail-closed companion surface for the
  Python adapter. The pure Rust crate covers all P082 impact classes including
  `research`, rejects duplicate set entries, unregistered
  backend/platform refs, mismatched canonical digests, property or image-variant
  mismatches, digest-valid but semantically unbounded plans, illegal lifecycle
  transitions, stale recovery and guest bindings, malformed recovery process/
  control-socket identity or timestamps, and dishonest payload length/digest
  declarations.
- [x] Implement the first daemon-owned host-broker slice for exact fixture working-
  storage allocation, authoritative startup enumeration, contradictory/orphaned
  state quarantine, content-bound idempotency, generation supersession, inspect,
  drain, and deterministic teardown. In supervised operation `fixture-copy.v1`
  reaches this authority through the internal, non-passportable
  `sensorium.virt.host` channel capability, restricted to the
  `sensorium-workbench` module. The daemon selects the state root and admits
  `fixture.prepare` only when source path, workspace/root refs, operational
  context, policy ref, and copy limits match layered operator configuration.
  The bounded `sensorium-virt.host.request.v1` companion remains only for local
  development and conformance, requires explicit
  literal-boolean `virt_host.standalone_companion_enabled = true` plus a closed
  `virt_host.standalone_companion_purpose = development|conformance`, and defaults
  to disabled; missing, ill-typed, or production-purpose values are configuration
  errors and remain disabled.
  Supervised channel mode never falls back to it when daemon admission is
  unavailable. Mutations are serialized by a broker lock shared across daemon and
  companion processes; tree, state, and configuration directory enumeration is
  capped before materialization. Python no longer creates or removes managed
  environment trees and receives no arbitrary process, host-path, network-device,
  or VMM-admin operation.
  Both the daemon admission path and the standalone companion validate the closed
  host request through Node schema-gate. Reconciliation returns full aggregate
  counts plus at most 64 structured diagnostics with opaque record/resource refs
  and an explicit truncation marker; host refusal envelopes and Workbench errors use
  allowlisted public messages, so raw host paths, subprocess diagnostics, capability
  failure details, and unbounded error strings do not cross into Workbench. The
  connector also refuses a host plan whose `backend/id` differs from the configured
  executor kind. It validates required refs and digests in the plan and recovery
  record independently before comparing their bindings, so two missing values
  cannot agree. Python guest-root normalization is early configuration feedback,
  while Rust guest `resolve_contained` remains the authoritative per-operation
  containment boundary. Schema-gate regression coverage removes one required
  capability dimension and proves that missing properties are refusal, not a
  wildcard.
- [x] Extend the host broker with VMM process launch, API/control socket allocation,
  bounded VMM resource-plan projection, boot identity, and platform-specific
  recovery for
  `vfkit-system.v1`; keep that authority out of the Python connector. The daemon
  loads an operator-authored, digest-pinned vfkit profile and admits only the
  closed `vfkit.allocate` and lifecycle operations. The broker owns private
  state, fsync-backed APFS-cloned raw disk and EFI variable store allocation,
  short private Unix socket paths, CSPRNG boot nonces, exact PID/start-marker and
  socket-inode identities, with a durable launch intent committed before process
  creation and process identity persisted before waiting for socket readiness.
  Startup recovery finds and terminates an exact matching launch that escaped the
  PID commit, while content-bound replay, generation supersession, cooperative
  stop, deterministic teardown, orphan detection, and quarantine remain enforced.
  The vfkit API client exposes a closed typed lifecycle operation set rather than
  accepting free-form method, endpoint, or body strings. A disabled profile keeps
  only teardown/reconcile authority as resolved decision 53. The socket root is
  opened with no-follow directory semantics, permissioned through its descriptor,
  pinned by device/inode identity, and rechecked before lifecycle use. The
  feature-gated 18-case process harness includes refusal of the fake VMM without
  conformance authority, dead-listener, interrupted-launch, boot-nonce freshness,
  socket-root substitution, and generation-supersession evidence in addition to
  the original lifecycle cases.
  The fake VMM binary and non-macOS conformance constructor are absent from normal
  builds, and the fake binary refuses without the marker emitted only by that
  constructor. An operator-authored binary digest remains an explicit host trust
  decision; vendor-only provenance requires package policy or an allowlist rather
  than heuristic recognition of executable bytes.
  Host paths and VMM arguments never enter the caller request or response.
- [x] Implement and package `orbiplex-workbench-guest` with generation/plan/image/
  nonce-bound virtio-vsock handshake, bounded process and PTY control, chunked
  file/patch/export frames, defense-in-depth guest resource limits, lifecycle
  inspect, quiesce, and shutdown. `sensorium-virt-host::GuestWorkbenchChannel`
  validates exact bindings,
  monotonic sequence, deadlines, outcomes, and transfer metadata. The vfkit broker
  derives the channel binding from its authoritative live recovery record. A
  feature-gated local-transport suite runs the actual guest binary and covers the
  happy path plus stale nonce, replayed sequence, malformed request and transfer
  admission, exact output and wire bounds, deadline non-extension, partial
  transfer, and durable exact patch-stage replay after a lost
  receipt, quiesce refusal, and deterministic shutdown without claiming full-system
  deployment evidence. A production-exchange test pins one operation per
  connection; together with the synchronous single-runtime accept loop this
  establishes per-environment operation serialization without holding the host
  lifecycle lock across provider I/O. Host-channel tests separately cover endpoint replacement,
  dead listeners, exact maximum response transfer, and oversized response metadata.
  Readiness is tracked as three distinct facts: guest
  `protocol implemented`; real-binary local `conformance proven`; full-system
  vfkit `deployment evidence proven`.
- [x] Add an independent bounded guest `terminal-read` operation. The guest retains
  exact PTY output chunks behind a monotonically increasing cursor, reports an
  explicit dropped-through gap after bounded eviction, rejects future cursors,
  and keeps terminal output readable after process exit until ordinary bounded
  pressure reclaims it. Real-binary conformance keeps two PTYs open together,
  proves that their retained bytes and cursors do not cross, refuses
  `high-water + 1`, and distinguishes that refusal from a successful read with
  explicit eviction-gap evidence. Input, resize, and signal remain separate
  effect operations.
- [x] Implement the host-lifecycle adapter for `vfkit-system.v1` as the first
  process-isolated backend slice on
  `macos-vz-arm64.v1`: pinned binary, EFI full-system GNU/Linux arm64 image, APFS
  working-disk clone, private EFI variable store, dedicated vsock-to-UDS control
  socket, closed block/vsock/rng device set, and no NIC, serial channel, host share,
  Rosetta, SSH, credential injection, or memory snapshots. The target profile's
  output-only diagnostic serial remains disabled until retained output has a
  continuously enforced byte bound; periodic truncation is not such evidence. A
  separate fake-vfkit process
  harness exercises the exact command surface and lifecycle without claiming
  full-system or Apple Virtualization Framework evidence. Real-vfkit boot and
  guest-channel evidence remain owned by the next item.
- [x] Build the pinned full-system GNU/Linux arm64 image and run real-vfkit
  deployment evidence for verified guest readiness, systemd/PID 1, harmless
  kernel and mount operations, offline package installation, no-NIC/no-SSH/no-
  share/no-credential posture, real PTY, file/read/patch-stage/export behavior,
  bounded process output, observed CPU/RAM/disk/TasksMax plan, guest PID exhaustion, generation/plan/image/nonce
  handshake, stale-generation refusal, dirty-restart recovery, content-bound
  idempotency conflict/refusal, cooperative drain, deterministic teardown, and
  bounded measurements under explicit functional deadlines. The image builder
  pins source and builder digests, serializes concurrent builds, writes metadata
  atomically, and emits manifest, SBOM, provenance, firmware, guest-agent, and a
  final digest-bound completion record. The exact ignored deployment test and its
  runner schema-gate a closed redacted report with VMM/image/firmware/guest pins
  and without host paths, guest output, credentials, or serial bytes. An external
  marker may signal that the runner finished, but is never accepted as evidence.
- [x] Route the guest PTY and file channel through the virtualized Workbench
  adapter and existing P083 two-controller fencing. `microvm` roots select the
  exact `vfkit-system.v1` executor through daemon-owned `sensorium.virt.host`;
  file snapshot/read, artifact export, PTY open/read/input/resize/signal/cancel,
  and content-bound `patch.stage` reuse the existing Workbench contracts. Guest
  PTY output enters the same durable terminal-event log consumed by P082, while
  P083 remains the sole remote control authority above the backend boundary.
  Restart may rebind the live VM, but retires prior process-local PTY authority.
  Reuse of that session or its command idempotency key returns the typed
  `workbench-restart-required-relink` outcome and requires a new session under
  the current generation. Terminal close commits a local `closing` transition
  before guest I/O, refuses concurrent effects, and permits environment teardown
  to complete the same authority retirement without holding the terminal lock
  across provider I/O. Dedicated acceptance checks prove both restart
  supersession and the close/teardown race.
  Workbench patch-stage replay binds the key to address, source generation,
  content digest, and content length; conflicting reuse is refused. An `unknown`
  guest PTY outcome is terminal for waiters without claiming success or failure.
  The live-feed harness resolves each exact Rust test through bounded
  `libtest --list --format=terse` output before execution rather than parsing
  human progress text.
- [x] Add `story-012-vfkit-full-system` as an additive profile rather than
  reinterpreting the completed Story 012 baseline. Its v2 runner installs the
  deterministic repair fixture in the digest-pinned guest image and uses one
  Workbench runtime for the real vfkit guest, P082 observation, P083 repair
  lease, and three-node collaboration. The closed schema-gated report claims
  `single-runtime-vertical` only after proving failing and passing PTY evidence,
  B/C deliberation, exclusive repair, observer revocation, dirty recipient
  restart, stale-generation refusal, artifact export, and an unpublished Corpus
  draft.
- [x] **Additive post-MVP and non-blocking for the completed baseline gate:**
  retain the Story 012 PowerDNS/Bielik
  `single-host-full-system` report. The closed profile, schema-gated report,
  exact package/fixture
  image builder, P083 deterministic apply path, localhost-only listener check,
  authoritative DNS assertions, and structural tests are implemented. The
  retained 2026-07-23 run supplies the required real model and guest evidence;
  this result is not inferred from the manifest-repair vertical.
- [x] Keep the role-aware Story 012 correction loop on the existing P082/P083
  boundaries: the shared PTY remains read-only for participants, one bounded
  deliberately wrong host-owned experiment is admitted through its own short
  P083 lease, its verifier failure advances the latest-state projection, and the
  deterministic fallback obtains a fresh lease after bounded deliberation.
  No lease spans model inference and no model text becomes PTY input.
- [ ] Run and retain the expensive role-aware PowerDNS profile. The earlier
  retained report predates the multi-cycle terminal-feedback path and remains
  narrower evidence rather than an implicit pass for this extension.
- [ ] Add a delegated adaptive-executor acceptance profile only after Corpus and
  Agent can carry an attributed inert `inquirium.candidate-plan.v1`. Requester
  policy may designate a remote Chair or participant Agent, but Room authority
  must not widen Workbench authority: node A still requires a separate
  resource-scoped Sensorium grant, current generation, review decision, bounded
  lease, and revocation check before any terminal effect. Remote control MUST
  reuse P083 / Solution 046 claim/control/invoke and MUST NOT add a Workbench-
  local relay or prose-to-command bridge.
- [ ] **In progress:** complete deployment evidence for
  `cloud-hypervisor-system.v1` as the first Linux deployment profile after the
  backend-neutral vfkit slice proves the contracts.
  The backend, daemon admission, Workbench routing, binary/firmware/raw-image
  pinning, closed REST/device builder, durable lifecycle/recovery, continuously
  bounded output-only serial, Linux cgroup v2/non-root identity, default seccomp,
  fail-closed Landlock ABI v3 preflight plus the attested
  `host-filesystem-allowlist` enforcement class, explicit Landlock rules, SMBIOS
  guest bootstrap, macOS fake-process conformance, exact-process dirty-restart
  reconciliation, bounded API readiness, authoritative cgroup cleanup, exact Cloud Hypervisor manifest-variant selection,
  operation-classed REST I/O budgets and an explicit host-task/guest-process limit
  separation,
  Linux x86_64 host/guest/schema/daemon/Workbench compile and conformance CI gate,
  and schema-gated real deployment runner are landed.
  Completion still requires that runner to pass on a physical or remote Linux
  x86_64 KVM host with the pinned full-system image. QEMU/TCG and fake-process
  evidence are explicitly non-substitutable for this final gate.
- [ ] Implement `firecracker-system.v1` only after the guest protocol and image
  manifest stabilize; require the same backend-neutral conformance plus a
  jailer-equivalent host profile. Keep Incus, crosvm, OCI-to-VM runtimes, Kata,
  containers, gVisor, and Wasm as separately classified optional backends rather
  than substitutes for the full-system hardware-VM proof.
- [x] Add artifact export and teardown tests, including source immutability,
  idempotent replay, managed-root containment, and persisted lifecycle state.
- [x] Add local-runtime policy tests for denied egress and denied credential
  env override access. Broader virtualized-backend policy tests remain tied to
  the future Sensorium Virt backend contract.

### Phase 5 - Sensorium Interface Source Projection

- [x] Expose Workbench terminal screen snapshots as a P082 `latest-state`
  source without granting terminal control.
- [x] Expose Workbench terminal events as a separate P082 `ordered-events`
  source with exact-byte schema validation, bounded replay, explicit gap and end
  semantics, and generation-bound cursors.
- [x] Expose an owner-bound local live event feed for both local and direct-peer
  subscriptions. Loopback SSE projects already admitted local subscriptions; the
  direct-peer feed uses the ordinary Passport-bound P082 pull path, validates each
  returned result and inline payload, and presents it through a local SSE endpoint
  without turning the cursor or feed ref into authority.
- [x] Prove the collaborative read-only terminal view through the WSS Room
  adapter, including current Room-plus-interface authority intersection,
  cursor omission, grant-revocation close, and durable Room survival.
- [x] Keep publication, grants, subscriptions, direct-peer admission, SSE, and
  Room carrier semantics owned by Proposal 082 / Solution 046 rather than the
  Workbench connector.
- [x] Add operational-impact defaults and exact environment pinning. Extend the
  environment contract and connector configuration with
  `sensorium-operational-context.v1`, require an effective value before publishing
  Workbench-backed collaborative or remotely invokable interfaces, expose a
  host-owned `source/generation-ref`, and inherit both into every derived P082/P083
  resource. Serialize immutable replacement and old-publication withdrawal on impact
  change; enforce P082's 512-byte UTF-8 summary cap; and test mixed test/production
  resources under one adapter, host-only raising, reasoned `critical -> test`
  correction, `test -> production` replacement, old-generation and superseded-id
  refusal, and missing/oversized-value refusal. The environment schema and bundled
  connector now require exact root- and environment-level context, derive a
  process-epoch-bound generation from the complete environment projection, pin
  actuation grants to both environment ref and current generation, and refuse stale
  authority. Runtime replacement/race tests plus Workbench mixed-context and
  summary-provenance tests provide the Phase 5 evidence.
