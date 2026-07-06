# Sensorium Workbench

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `node:sensorium-actuation-core`
- `node:interaction-broker-core`
- `node:middleware-modules/sensorium-workbench`

Related schemas:

- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`
- `sensorium-terminal-command.v1`
- `sensorium-terminal-input.v1`
- `sensorium-terminal-event.v1`
- `sensorium-terminal-screen-snapshot.v1`
- `sensorium-file-snapshot.v1`
- `sensorium-file-read-result.v1`
- `sensorium-workbench-patch.v1`
- `sensorium-workbench-patch-apply-result.v1`
- `sensorium-workbench-outcome.v1`
- `sensorium-relative-path-address.v1`
- `sensorium-command-profile.v1`
- `sensorium-command-intent.v1`
- `sensorium-pty-resource-caps.v1`
- `interaction-broker-watch.v1`
- `interaction-broker-wait.request.v1`
- `interaction-broker-wait.outcome.v1`
- `interaction-broker-probe.v1`
- `deferred-operation.v1`
- `deferred-operation-status.v1`
- `capability-authorization-policy.v1`

## Status

Partial implementation foundation.

The contract, schema, conformance-vector, capability-registration, opt-in local
connector foundation, and daemon-owned Interaction Broker runtime slice exist.
The daemon now admits broker wait/watch/probe calls from JSON-e/module callers
through daemon-issued host-local HMAC grant material requested by
`bindings.host_grant_requests`, and the Workbench file-tree and terminal
providers are live through the broker for file probes, file waits, file-tree
watch event batches, terminal liveness/progress probes, terminal waits, and
terminal watch event batches. The daemon also projects admitted broker
wait/watch/probe submissions into metadata-only audit events. The remaining
solution work is broader adversarial actuator coverage, future virtualized
backends, richer recovery/retention semantics, and non-Workbench source-provider
joins.

## Date

2026-07-04

## History

This solution promotes the accepted Proposal 071 Workbench foundation from
2026-06-23 into a separate solution component. Proposal 071 remains the
rationale, design history, resolved-decision log, and implementation tracker;
this solution owns the current solution-level boundary.

## Executive Summary

Sensorium Workbench is the high-impact local actuation component for model-
assisted software and system work. It lets a node inspect bounded local
workspaces, manage supervised terminal sessions, apply approved patches, expose
short waits and probes, and hand artifacts across the host boundary without
giving models ambient shell or filesystem authority.

Workbench is a Sensorium connector/runtime class, not a new organ and not an
Inquirium adapter. The invariant remains:

```text
Inquirium thinks.
Host authorizes.
Sensorium acts.
Workbench brokers terminal, filesystem, patch, and workspace effects.
```

The solution promotes the settled P071 foundation into a separate component
because Workbench carries a materially higher risk profile than Sensorium OS
one-shot actions. It has distinct capability ids, runtime limits, state stores,
operator status, and recovery duties.

## Context and Problem Statement

Model-assisted development needs a loop:

```text
observe environment
propose next step
authorize bounded effect
execute through host policy
observe result
repeat
```

If that loop is implemented as direct model-to-terminal control, the model
silently becomes the commander of the node. If it is hidden inside workflow
scripts, terminal state, filesystem access, waits, artifacts, and cleanup
become private side effects. Both shapes collapse reasoning, authorization, and
actuation into one unsafe surface.

Workbench gives the system one explicit local workbench boundary. It keeps
terminal sessions, file snapshots, patch application, environment lifecycle,
wait/watch/probe coordination, audit metadata, and cleanup visible to the host
and operator.

## Proposed Model / Decision

Workbench is a node-local Sensorium connector/runtime component. Its first
implementation is a separate supervised middleware connector, disabled by
factory config and enabled only by explicit operator configuration.

The solution is stratified as:

```text
sensorium-actuation-core
  path rules, command profiles, argv-as-data, env policy, PTY caps

sensorium-workbench connector/runtime
  host-local workspaces, PTY sessions, file snapshot/read, patch apply,
  connector-local short waits/probes, metadata stores, cleanup

Sensorium Core
  directive admission, capability routing, audit linkage, connector dispatch

Interaction Broker
  host-owned waits, watches, probes, source registry, deferred wait projection

Inquirium / JSON-e Flow / UI
  plans, proposed intents, approval flows, bounded read views
```

Workbench consumes the same lower actuation rules as Sensorium OS so that path
traversal, symlink escape, command profile, environment, timeout, output cap,
classification, and idempotency behavior do not drift between local actuators.

The first stable runtime scope is host-local only. Containers, microVMs, remote
machines, credential grants, desktop automation, browser profile access, and
network egress are future backend or capability contracts, not part of the
foundation.

## Must Implement

### Workbench Capability Boundary

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`

Related schemas:

- `capability-authorization-policy.v1`
- `sensorium-workbench-outcome.v1`

Responsibilities:

- register `sensorium.workbench.terminal`, `sensorium.workbench.file`,
  `sensorium.workbench.patch`, and `sensorium.workbench.env`;
- keep Workbench authority separate from Sensorium OS grants;
- expose Workbench actions only through Sensorium-mediated connector routing;
- preserve the rule that Inquirium may propose intents but cannot invoke
  connectors directly;
- bind effect classes to required grants, caller posture, approval mode,
  autonomy floor, and conflict-of-interest policy.

Status:

- `partial`: capability ids and policy sidecars exist; JSON-e/module broker
  calls request host grants through `bindings.host_grant_requests`, and the
  daemon mints host-local HMAC grant material before dispatch.

### Shared Actuation Core

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`

Related schemas:

- `sensorium-relative-path-address.v1`
- `sensorium-command-profile.v1`
- `sensorium-command-intent.v1`
- `sensorium-pty-resource-caps.v1`

Responsibilities:

- provide reusable path syntax and containment rules;
- reject traversal, NUL bytes, symlink escape, root self-access where a file is
  required, and path-space/root mismatch;
- validate command profiles as argv data, not shell strings;
- enforce default-deny workspace roots and variable argv prefix behavior;
- define PTY resource caps and timeout/output cap validation;
- publish golden vectors consumed by Rust and Python Workbench conformance
  tests.

Status:

- `partial`: `node:sensorium-actuation-core`, `node:relative-path-core`,
  schemas, examples, and initial golden vectors exist. Direct Python
  consumption through FFI/RPC remains deferred; the current Python connector
  mirrors the rules against shared vectors.

### Local Workbench Connector Runtime

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`

Related schemas:

- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`
- `sensorium-terminal-command.v1`
- `sensorium-terminal-event.v1`
- `sensorium-terminal-screen-snapshot.v1`
- `sensorium-file-snapshot.v1`
- `sensorium-file-read-result.v1`
- `sensorium-workbench-outcome.v1`

Responsibilities:

- run as an opt-in supervised middleware connector with readiness, lifecycle,
  status, and config surfaces;
- admit only explicitly configured host-local workspace roots;
- expose bounded file snapshot/read without ambient filesystem access;
- create bounded PTY sessions only when terminal runtime is explicitly enabled;
- execute structured command intents without shell interpolation;
- bound terminal events, output bytes, input queues, reader tasks, active
  sessions, idle/TTL policy, and close semantics;
- keep raw terminal input, resize, and signal operator-only in the foundation
  slice.

Status:

- `partial`: the opt-in Python connector exists with host-local workspace,
  file, probe, wait, watch, PTY, capture, and status surfaces. Idle timeout,
  daemon-owned status integration, and broader adversarial runtime coverage
  remain incomplete.

### Patch and Artifact-Mediated Writes

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `sensorium-workbench-patch.v1`
- `sensorium-workbench-patch-apply-result.v1`
- `sensorium-file-read-result.v1`

Responsibilities:

- require patch apply to consume artifact refs rather than raw model output;
- verify artifact digest and size before application;
- support structured edits and narrow unified-diff application;
- reject deletes by default;
- enforce the same workspace containment and symlink rules as reads;
- record metadata-only outcomes and rollback partial structured writes when
  possible.

Status:

- `partial`: artifact-backed patch apply exists in the opt-in connector behind
  explicit grants and operator confirmation. Host Artifact Delivery or Memarium
  admission remains a separate future handoff.

### Interaction and Deferred Coordination

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`

Related schemas:

- `interaction-broker-watch.v1`
- `interaction-broker-wait.request.v1`
- `interaction-broker-wait.outcome.v1`
- `interaction-broker-probe.v1`
- `deferred-operation.v1`
- `deferred-operation-status.v1`

Responsibilities:

- expose short waits and probes for command completion, terminal quiescence,
  environment readiness, file state, artifact presence, and no-progress
  diagnostics;
- implement the Workbench-owned terminal/file source-provider adapter that
  registers with the broker-owned source-provider registry;
- keep cross-source waits, watches, and probes host-owned through Interaction
  Broker;
- project long waits through `deferred-operation-status.v1` instead of a
  parallel lifecycle dialect;
- require explicit status-read grants; possession of an operation id is not
  authority;
- prevent broker timeout or `maybe_hung` diagnostics from authorizing process
  termination.

Status:

- `partial`: connector-local waits/probes/watches and deferred status
  projection exist. The daemon-owned Interaction Broker runtime now provides
  host capability dispatch, durable broker resource storage, seeded provider
  registry rows, operator read APIs, host Bounded Deferred Operation
  registration/polling for broker-owned waits, JSON-e/module grant-context
  admission through daemon-issued host-local HMAC grant material requested by
  `bindings.host_grant_requests`, metadata-only broker audit projection, and
  live Workbench file-tree plus terminal provider adapters. File probes, file
  waits, file-tree watch batches, terminal liveness/progress probes, terminal
  waits, and terminal watch batches can now flow through the broker. Dynamic
  non-Workbench provider registration and deeper recovery/retention behavior
  remain future work.

### Storage, Recovery, and Operator Visibility

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`

Related schemas:

- `sensorium-terminal-event.v1`
- `sensorium-workbench-outcome.v1`
- `interaction-broker-wait.outcome.v1`

Responsibilities:

- keep Workbench and broker stores metadata-first;
- avoid storing raw terminal transcripts, file contents, prompts, source blobs,
  or credentials by default;
- use explicit migrations, WAL-oriented SQLite pragmas, `busy_timeout`, foreign
  keys where relationships exist, idempotency keys, retention windows, and
  replay/projection diagnostics;
- run startup recovery before accepting new PTY, file, patch, wait, or
  environment requests;
- surface residual children, failed cleanup, interrupted waits, and degraded
  recovery facts to operator status.

Status:

- `partial`: the connector has a metadata SQLite store, retention cleanup,
  orphan signaling, session retirement, and interrupted operation marking.
  Host/operator projection of recovery telemetry remains future work.

### Adversarial Actuator Conformance

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`

Related schemas:

- `sensorium-relative-path-address.v1`
- `sensorium-command-profile.v1`
- `sensorium-terminal-command.v1`
- `sensorium-workbench-patch-apply-result.v1`

Responsibilities:

- maintain refusal-first golden vectors for path, command, PTY lifecycle,
  network/credential denial, cleanup, idempotency, replay, broker scope, patch,
  and artifact cases;
- run those vectors against shared Rust cores and Python connector tests;
- refuse enabling write or PTY features by default until the relevant negative
  vectors pass;
- keep the conformance suite as the cross-language contract, not an
  implementation detail.

Status:

- `partial`: initial path, command-profile, patch, artifact, grant, raw-input,
  idempotency, and connector-local deferred wait vectors exist. Residual-child,
  egress, credential, replay, and virtualized-backend vectors remain broader
  runtime work.

## May Implement

### Sensorium Virt Backends

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`

Related schemas:

- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`

Responsibilities:

- interpret the same environment, terminal, file, artifact, and teardown
  contracts over fixture-only virtual workspaces, containers, microVMs,
  emulators, or remote disposable machines;
- declare locality, network policy, filesystem roots, credential policy,
  teardown policy, artifact export policy, and resource limits;
- preserve Workbench contracts across backend changes.

Status:

- `deferred`.

### Agent and Corpus Tool Use

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/60-solutions/038-corpus/038-corpus.md`

Related schemas:

- `sensorium-command-intent.v1`
- `sensorium-workbench-outcome.v1`

Responsibilities:

- let Agent, Corpus, or Room workflows request bounded Workbench tool use
  through host policy;
- keep all effects mediated by Sensorium and Workbench grants;
- reject any adapter that owns terminal or filesystem authority outside the
  Workbench boundary.

Status:

- `deferred`.

## Out of Scope

- direct model-to-terminal or model-to-filesystem authority;
- treating Workbench as a new constitutional organ;
- replacing Sensorium Core, Sensorium OS, Interaction Broker, Artifact
  Delivery, Inquirium, or Agent;
- public or federated Workbench execution;
- network egress, credential access, clipboard access, keychain access, SSH
  agent access, browser profile access, desktop automation, or GUI event
  injection by default;
- making raw terminal transcripts or file contents durable facts by default;
- using broker waits or probes to kill processes.

## Consumes

- Sensorium directive requests;
- Workbench capability grants and authorization-policy data;
- command profiles and command intents;
- workspace root configuration;
- artifact refs for patch apply and capture;
- Interaction Broker wait/watch/probe requests;
- deferred-operation policy for long waits.

## Produces

- Workbench environment, terminal session, terminal event, file snapshot, file
  read, patch apply, and outcome records;
- metadata-only Workbench audit facts;
- terminal screen snapshots and bounded event cursors;
- connector-local deferred wait projections until host broker runtime owns
  them;
- recovery and cleanup diagnostics for operator status.

## Related Capability Data

- `042-sensorium-workbench-caps.edn`

## Notes

Workbench should be read as a high-impact actuator boundary below Sensorium
Core and above low-level host-local mechanics. It is intentionally boring:
structured command intents before raw terminal input, relative addresses before
ambient filesystem paths, artifacts before inline bytes, metadata traces before
raw transcripts, and explicit cleanup before trusting a restarted process
generation.
