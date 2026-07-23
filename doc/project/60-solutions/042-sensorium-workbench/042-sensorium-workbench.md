# Sensorium Workbench

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/40-proposals/083-sensorium-interactive-interfaces.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `node:sensorium-actuation-core`
- `node:sensorium-virt-core`
- `node:sensorium-virt-host`
- `node:sensorium-virt-host/tests/vfkit_deployment.rs`
- `node:tools/acceptance/sensorium-virt-vfkit`
- `node:tools/acceptance/story-012-shared-chair-terminal`
- `node:tools/acceptance/sensorium-terminal-live-feed`
- `node:daemon/src/sensorium_virt_integration.rs`
- `node:interaction-broker-core`
- `node:middleware-modules/sensorium-workbench`

Related schemas:

- `sensorium-operational-context.v1`
- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`
- `sensorium-terminal-command.v1`
- `sensorium-terminal-input.v1`
- `sensorium-interface-terminal-input.v1`
- `sensorium-interface-terminal-resize.v1`
- `sensorium-interface-terminal-signal.v1`
- `sensorium-terminal-event.v1`
- `sensorium-terminal-screen-snapshot.v1`
- `sensorium-file-snapshot.v1`
- `sensorium-file-read-result.v1`
- `sensorium-workbench-patch.v1`
- `sensorium-workbench-patch-apply-result.v1`
- `sensorium-workbench-patch-stage-result.v1`
- `sensorium-workbench-outcome.v1`
- `sensorium-workbench-error-codes.v1`
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
- `operator-consent.request.v1`
- `operator-consent-decision.v1`
- `sensorium-workbench.consent-descriptor.v1`
- `sensorium-os.consent-descriptor.v1`
- `sensorium-actuation.bridge.request.v1`
- `sensorium-actuation.bridge.response.v1`
- `sensorium-virt-workspace-export.v1`
- `sensorium-virt-export-result.v1`
- `sensorium-virt-teardown-result.v1`
- `sensorium-virt-backend-capabilities.v1`
- `sensorium-virt-environment-plan.v1`
- `sensorium-virt-image-manifest.v1`
- `sensorium-virt-recovery-record.v1`
- `sensorium-virt-guest-frame.v1`
- `sensorium-virt.host.request.v1`
- `sensorium-virt-vfkit-deployment-report.v1`
- `story-012-vfkit-full-system-report.v1`
- `sensorium-workbench-tool-request.v1`
- `sensorium-interface-descriptor.v1`
- `sensorium-interface-frame.v1`
- `sensorium-interface-read-result.v1`

## Status

Implemented; additional Linux backends remain optional follow-up profiles.

The contract, schema, conformance-vector, capability-registration, opt-in local
connector foundation, and daemon-owned Interaction Broker runtime slice exist.
The daemon now admits broker wait/watch/probe calls from JSON-e/module callers
through daemon-issued host-local HMAC grant material requested by
`bindings.host_grant_requests`, and the Workbench file-tree and terminal
providers are live through the broker for file probes, file waits, file-tree
watch event batches, terminal liveness/progress probes, terminal waits, and
terminal watch event batches. The daemon also projects admitted broker
wait/watch/probe submissions into metadata-only audit events. The current
implementation also covers a managed fixture-copy virtualized executor with
host-owned allocation/reconcile/quarantine/teardown, exact normalized-plan,
capability, image-variant, generation, and recovery evidence, explicit export/
teardown, closed schema-gated host ingress, bounded structured reconciliation
diagnostics, daemon BDO registration/polling for long-running Workbench terminal
commands, broker projection of Workbench provider operator status, and dynamic
observed-state joins for artifact, environment, approval, and Memarium-query
providers. The first host-owned operator consent spine is also implemented for
exact Workbench terminal commands: the daemon owns consent requests, P066
operator-question/notification projection, answer-to-decision translation,
list/detail/revoke APIs, and a Workbench exact-argv command-profile sidecar
projection. Operator-consent read/projection APIs reject module callers
fail-closed, duplicate requests replay by semantic request equality, and the
Workbench connector refreshes sidecar profiles through a bounded TTL instead of
freezing the startup snapshot. The same spine now enforces active
`node-operator-binding.v1` authority for consent answers and revoke calls,
fails durable answers closed unless the target capability is grantable by host
authorization policy, and omits expired exact-argv sidecar entries or entries
whose `operator/ref` points to an inactive binding, or whose capability is no
longer durable-grantable, while surfacing `consent-expired`,
`consent-operator-binding-inactive`, or `consent-capability-not-grantable`
diagnostics. The Workbench connector imports those host sidecar diagnostics into
its operator-visible config diagnostics. The same host-owned spine now also
projects granted Sensorium OS `remember-action-catalog-entry` decisions into
`sensorium-os.action-catalog-sidecar.v1`, writes that sidecar to the Sensorium
OS middleware config tree, and the Sensorium OS connector loads valid
non-overriding deltas into its effective action catalog. The daemon now also
owns native Artifact Delivery, approval/consent, and Memarium-query broker
providers, explicit Workbench artifact handoff, bounded argv-prefix consent,
shared append-only sidecar merge, dedicated node-ui consent/broker screens, a
required Rust actuation companion-process boundary without a Python validation
fallback, and Agent/Corpus/Room tool request lineage admission through Sensorium
Core. Workbench screen snapshots and terminal events are now implemented as
separate read-only Sensorium Interface source projections, including a
collaborative WSS Room latest-state acceptance path. The first
property-attested process-isolated host-lifecycle runtime is now implemented:
the daemon-owned `vfkit-system.v1` broker validates a pinned Apple Silicon
profile, allocates private raw-disk/EFI/socket resources, launches a closed
device set, records exact process/socket/resource and boot-nonce identity, and
owns inspect, drain, teardown, recovery, reconciliation, and quarantine. A
process-level fake-vfkit suite proves replay and principal crash/substitution
refusals without exposing VMM administration sockets to Python. The packaged
Rust guest and host channel now add exact generation/plan/image/nonce binding,
bounded process/PTY/file/lifecycle operations, chunked transfer, and real-binary
local conformance. The guest now also supports an independent bounded terminal-read
cursor with exact bytes, explicit eviction gaps, post-exit replay, and future-cursor
refusal. A pinned full-system GNU/Linux arm64 image and real-vfkit
deployment harness now additionally prove the guest channel, systemd, kernel/
mount/package operations, no-NIC/no-share posture, bounded guest resources,
recovery, and teardown. The virtualized Workbench adapter now selects
`vfkit-system.v1` for `microvm` roots through the daemon-owned host capability,
maps guest file, export, patch-stage, and PTY operations onto existing Workbench
contracts, writes guest output into the P082 terminal event source, and leaves
P083 as the only remote actuation authority. Patch-stage replay is content- and
generation-bound, completed PTYs are reaped before guest quiescence is reported,
and an unprovable guest PTY outcome terminates waits as `unknown`. Its additive
Story 012 v2 profile delivers the repair fixture inside the digest-pinned guest
image and runs real vfkit, Workbench, P082/P083, Room, Agent, and Corpus through
one Workbench runtime. The closed report names the evidence boundary
`single-runtime-vertical` and proves failing/passing PTY observation, exclusive
repair, revoke, dirty restart, stale-generation refusal, export, and an
unpublished draft. Later Linux backends and
optional daemon command-BDO signal policy beyond the implemented `TERM` cancel
path also remain post-baseline work.

Proposal 083 defines the hard-MVP release-blocking path for separately granted
terminal input, resize, and signal actuation. Its P083-002 through P083-011 runtime
and synchronization slices are now implemented: a remote caller reaches the existing
Workbench PTY checks as a remote Sensorium Interface control authority carrying exact
grant, generation, lease, epoch, sequence, method, deadline, and causal lineage.
Workbench never relabels that caller as the operator, raw bytes are not retained by
the generic interface runtime, and provider-confirmed terminal closure fences the
source.
The bounded Room grouping/status/control/invoke surface derives caller identity
from a current `actuate` session and intersects it with exact interface authority.
The conformance matrix proves two controllers against a real PTY while Rust proves
queue, handoff, stale-epoch refusal, restart, saturation, and partial failure.
P083-012 now promotes that reviewed actuation boundary into Solution 046; only the
P083-013 relay carrier remains deferred until P070 Phase 6A.

## Date

2026-07-21

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
- `sensorium-workbench-error-codes.v1`

Responsibilities:

- register `sensorium.workbench.terminal`, `sensorium.workbench.file`,
  `sensorium.workbench.patch`, and `sensorium.workbench.env`;
- keep Workbench authority separate from Sensorium OS grants;
- expose Workbench actions only through Sensorium-mediated connector routing;
- preserve the rule that Inquirium may propose intents but cannot invoke
  connectors directly;
- bind effect classes to required grants, caller posture, approval mode,
  autonomy floor, and conflict-of-interest policy.
- keep interactive operator consent host-owned: Workbench may request
  approval for an eligible command/profile delta, but the daemon must use
  `inquirium.operator-question.request.v1` projected through durable
  notifications for the prompt/answer state machine before any adapter-specific
  sidecar projection is materialized;
- project exact-argv and bounded `remember-argv-prefix` decisions into a Workbench
  command-profile sidecar without loosening workspace, egress, credential,
  timeout, or output-byte caps.

Status:

- `implemented`: capability ids and policy sidecars exist; JSON-e/module broker
  calls request host grants through `bindings.host_grant_requests`, and the
  daemon mints host-local HMAC grant material before dispatch. Exact-argv
  "ask and remember" command consent now reuses host-owned operator questions
  and notifications, persists host-owned consent decisions, and projects a
  bounded exact-argv sidecar that the connector refreshes with a bounded TTL.
  The implemented exact-argv path enforces active node-operator-binding
  authority, durable-grant grantability policy, expired-consent filtering,
  host-policy revalidation for effective durable sidecars, workspace-bound
  argv-prefix profiles that cannot widen egress/credential/time/output caps,
  inactive-binding sidecar diagnostics, connector import of host sidecar
  diagnostics, and dedicated operator consent inspection/revocation UI.
  Arbitrary-executable consent remains intentionally unsupported. Sensorium OS
  action-catalog consent deltas also use this spine: granted durable decisions
  are projected into a host-authored sidecar, filtered by the same authority and
  grantability rules, and loaded by the Sensorium OS connector as append-only
  non-overriding action declarations.

### Shared Actuation Core

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`

Related schemas:

- `sensorium-relative-path-address.v1`
- `sensorium-command-profile.v1`
- `sensorium-command-intent.v1`
- `sensorium-pty-resource-caps.v1`
- `sensorium-actuation.bridge.request.v1`
- `sensorium-actuation.bridge.response.v1`

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

- `implemented`: `node:sensorium-actuation-core`, `node:relative-path-core`,
  schemas, examples, and golden vectors exist. The Python connector invokes the
  required bounded `orbiplex-sensorium-actuation-contract` companion process
  for relative-path and command-profile decisions and fails readiness or the
  affected request closed when that bridge is absent, unavailable, or malformed;
  no development profile enables a Python validation fallback.

### Local Workbench Connector Runtime

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`

Related schemas:

- `sensorium-operational-context.v1`
- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`
- `sensorium-terminal-command.v1`
- `sensorium-terminal-event.v1`
- `sensorium-terminal-screen-snapshot.v1`
- `sensorium-file-snapshot.v1`
- `sensorium-file-read-result.v1`
- `sensorium-workbench-outcome.v1`
- `sensorium-workbench-error-codes.v1`

Responsibilities:

- run as an opt-in supervised middleware connector with readiness, lifecycle,
  status, and config surfaces;
- admit only explicitly configured host-local workspace roots;
- expose bounded file snapshot/read without ambient filesystem access;
- create bounded PTY sessions only when terminal runtime is explicitly enabled;
- execute structured command intents without shell interpolation;
- bound terminal events, output bytes, input queues, reader tasks, active
  sessions, idle/TTL policy, and close semantics;
- replay terminal command, terminal capture, artifact-write, and patch-apply
  effects by `idempotency/key` without repeating local side effects;
- keep raw terminal input, resize, and signal operator-only in the foundation
  slice.

Status:

- `implemented` for the local and managed fixture-copy scope: the opt-in Python connector exists with host-local workspace,
  file, probe, wait, watch, PTY, capture, idempotency replay with bounded TTLs,
  idle-timeout, read-only status surfaces, and a `fixture-virtual-workspace`
  backend. `fixture-copy.v1` copies a bounded symlink-free source tree into a
  managed root, permits approved patching only there, supports explicit bounded
  artifact export and teardown, and leaves the source untouched. PTY stays
  fail-closed because the fixture executor does not provide process isolation.

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

- `implemented`: artifact-backed patch apply exists behind explicit grants and
  operator confirmation. The daemon can hand verified Workbench artifacts to
  the host object resolver and record explicit Artifact Delivery and/or
  metadata-only Memarium destinations with idempotent audit. Handoff replay
  binds its idempotency key to the normalized request and `correlation/id`.

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

- `implemented` for current provider classes: connector-local waits/probes/watches and deferred status
  projection exist. The daemon-owned Interaction Broker runtime now provides
  host capability dispatch, durable broker resource storage, seeded provider
  registry rows, operator read APIs, host Bounded Deferred Operation
  registration/polling for broker-owned waits, JSON-e/module grant-context
  admission through daemon-issued host-local HMAC grant material requested by
  `bindings.host_grant_requests`, metadata-only broker audit projection, and
  live Workbench file-tree plus terminal provider adapters. File probes, file
  waits, file-tree watch batches, terminal liveness/progress probes, terminal
  waits, and terminal watch batches can now flow through the broker. Dynamic
  non-Workbench provider registration/status APIs, dynamic observed-state joins
  for artifact, environment, approval, and Memarium-query providers, broker
  startup recovery, bounded broker retention, Workbench provider operator-status
  projection, and daemon BDO polling/cancel for Workbench terminal commands are
  now implemented. Domain-native Artifact Delivery, approval/consent, and
  Memarium-query providers expose bounded snapshots and stable watch cursors;
  additional domains can join through the dynamic provider contract.

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
- mark previously starting/running terminal commands failed so post-restart
  idempotency replay returns terminal command state rather than an unbounded
  running record;
- mark failed terminal-command spawn attempts as failed so idempotent replay
  cannot return an accepted command that never started;
- expose a host-owned cancel path for daemon-registered Workbench terminal
  command BDOs, mapping cancel to the connector's operator-confirmed
  `sensorium.workbench.terminal.command.cancel` action and projecting
  terminated commands as canonical BDO `cancelled` status while terminal
  `command.done` payloads carry `signal_origin` to distinguish timeout,
  operator cancel, and ordinary process exit;
- surface residual children, failed cleanup, interrupted waits, interrupted
  terminal commands, idle-closed sessions, and degraded recovery facts to
  operator status.

Status:

- `implemented` for the current local runtime: the connector has a metadata SQLite store, retention cleanup,
  orphan signaling, session retirement, interrupted operation/command marking,
  failed-spawn command marking, idempotency replay records with bounded TTLs,
  idle-session cleanup on terminal admission paths, and connector-local
  recovery/lifecycle status diagnostics. The daemon broker status now projects
  Workbench provider operator status from connector `/v1/status`; node-ui
  presents provider health, ownership, recent resources, and remediation paths.

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
- keep an executable PTY story smoke and Python-side Workbench actuation
  conformance runner in the Node workspace;
- refuse enabling write or PTY features by default until the relevant negative
  vectors pass;
- keep the conformance suite as the cross-language contract, not an
  implementation detail.

Status:

- `implemented` for exposed local/fixture-copy effects: path, command-profile, patch, artifact, grant, raw-input,
  idempotency, connector-local deferred wait, residual-child recovery,
  interrupted-command recovery, failed-spawn command replay, no-egress,
  operator-consent disabled-denial, dynamic sidecar-refresh, host sidecar
  diagnostics import, full workspace/root/path prefix-consent binding,
  credential-env refusal, local replay, replay TTL cleanup,
  PTY story, Rust bridge, managed-copy export/teardown, broker wait, replay, and
  Python conformance vectors exist. The extended Sensorium Interfaces runner also
  proves two independently fenced controllers writing through one real
  interactive Workbench shell PTY, including stale-holder refusal and bounded
  terminal shutdown. The same suite must run against the future vfkit, Cloud
  Hypervisor, and Firecracker profiles together with each profile's separate
  recovery, resource, and host-containment evidence.

### Read-Only Sensorium Interface Sources

Based on:

- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`

Related schemas:

- `sensorium-terminal-screen-snapshot.v1`
- `sensorium-terminal-event.v1`
- `sensorium-interface-descriptor.v1`
- `sensorium-interface-frame.v1`
- `sensorium-interface-remote-feed-request.v1`

Responsibilities:

- expose terminal screen snapshots as one `latest-state` source;
- expose terminal events as a separate exact-byte `ordered-events` source with
  bounded event/byte/age retention plus explicit gap and terminal end;
- preserve Workbench classification, workspace/session binding, and bounded
  source semantics without granting terminal control;
- let Solution 046 own publication, interface grants, subscriptions, direct-peer
  admission, SSE, and Room carrier behavior.
- expose local or direct-peer admitted subscriptions as owner-bound loopback SSE
  without treating a feed ref or cursor as authority.

Status:

- `implemented`: the daemon adapts both Workbench source classes through the
  Interaction Broker. Local SSE presents already admitted local subscriptions;
  the recipient-side direct-peer feed selects a current signed Passport, pins and
  validates each returned batch and inline terminal payload, and exposes it only to
  the creating local caller. The WSS Room acceptance path projects a cursor-free latest
  screen snapshot to the intersection of current Room observers and current
  interface grantees, closes on interface-grant revocation, and leaves the
  durable Room open. Ordered terminal events are refused by the MVP Room carrier.

## May Implement

### Sensorium Virt Backends

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`

Related schemas:

- `sensorium-operational-context.v1`
- `sensorium-workbench-environment.v1`
- `sensorium-terminal-session.v1`
- `sensorium-virt-workspace-export.v1`
- `sensorium-virt-export-result.v1`
- `sensorium-virt-teardown-result.v1`
- `sensorium-virt-backend-capabilities.v1`
- `sensorium-virt-environment-plan.v1`
- `sensorium-virt-image-manifest.v1`
- `sensorium-virt-recovery-record.v1`
- `sensorium-virt-guest-frame.v1`
- `sensorium-virt.host.request.v1`
- `sensorium-virt-vfkit-deployment-report.v1`

Responsibilities:

- interpret the same environment, terminal, file, artifact, and teardown
  contracts over fixture-only virtual workspaces, containers, microVMs,
  emulators, or remote disposable machines;
- match normalized environment requirements against host-attested backend,
  platform, locality, architecture, isolation, system-fidelity, transport, device,
  network, host-share, lifecycle, and resource-enforcement properties;
- keep every semantic capability dimension on a closed versioned vocabulary and
  deny unknown backend/platform refs before property matching;
- pin the effective P082 operational context in the normalized plan, including
  policy floors and higher contexts inherited from reachable or shared resources;
- prove logical image-variant equivalence from common userspace, SBOM, build-
  provenance, guest-agent, and protocol/schema-set digests while retaining exact
  variant boot-artifact identities;
- separate `EnvironmentBackend` lifecycle mechanics from the bounded
  `GuestWorkbenchChannel` process, PTY, file, patch, export, quiesce, and
  shutdown protocol;
- keep terminal reads independent from PTY input/effect calls, cursor-bound,
  exact-byte, and explicitly gapped after bounded guest-side eviction;
- keep backend/plan/image validation and VMM launch/recovery authority in Rust
  and the daemon-owned host broker while the Python connector owns bounded
  adapter and guest-RPC mechanics;
- preserve Workbench contracts across backend changes.

Status:

- `implemented fixture admission spine`: the five backend-neutral contracts,
  closed host request contract,
  positive/refusal fixtures, pure `sensorium-virt-core`, bounded companion, and
  first daemon host-broker slice are live. Supervised Workbench reaches it through
  the internal non-passportable `sensorium.virt.host` channel capability; the
  daemon fixes its state root and revalidates fixture source, refs, operational
  context, policy, and limits against layered operator configuration. The
  standalone companion is a local-development/conformance path only, defaults to
  disabled, and requires explicit literal-boolean
  `virt_host.standalone_companion_enabled = true` plus the closed
  `virt_host.standalone_companion_purpose = development|conformance`; missing,
  ill-typed, or production-purpose values refuse. Supervised production/channel
  mode never falls back to it when daemon admission is absent.
  `fixture-copy.v1` uses bounded allocation, startup enumeration, quarantine,
  cross-process mutation serialization, content-bound replay, generation
  supersession, inspect/drain/teardown, exact evidence projection, and SQLite
  metadata persistence. Both host entry paths use Node schema-gate, Workbench
  rejects backend substitution and missing plan/recovery bindings before comparing
  their values, and reconciliation exposes capped structured diagnostics without
  raw host paths or internal failure text. Python guest-root normalization is early
  feedback only; Rust guest containment remains authoritative. Host and Workbench
  boundaries emit only allowlisted public refusal messages. Contract verification
  covers `research`,
  rejects digest-valid but semantically invalid plans, and requires process,
  control-socket, and boot-nonce identity for a live hardware VM while permitting
  processless fixture records. The vertical smoke proves dirty-restart recovery,
  managed-copy patch/export, teardown, and source immutability. It intentionally
  refuses PTY;
- `process-isolated guest runtime and first deployment profile proven`:
  backend names are not isolation
  evidence. The daemon-owned `vfkit-system.v1` host adapter now provides the
  closed VMM lifecycle, a durable pre-spawn launch intent, fsync-backed boot
  artifacts, typed fixed API operations, and exact recovery identity persisted
  before socket readiness. Its feature-gated 18-case process conformance covers
  fake-VMM refusal without conformance authority, interrupted launch recovery,
  dead listeners, replay, dirty exit, PID reuse, binary/socket and socket-root
  substitution, missing storage, fresh boot nonces, generation supersession, and
  orphan cleanup. The fake VMM and non-macOS conformance constructor are absent
  from normal builds, and the fake binary requires the marker emitted only by that
  constructor. The production socket root is opened without following symlinks
  and pinned by descriptor identity. A disabled profile retains only teardown/
  reconcile authority.
  Its current closed device set is block, vsock, and entropy; diagnostic serial
  remains disabled until retained output has a continuously enforced byte bound.
  The packaged Rust guest and host channel now implement the nonce/generation/
  plan/image-bound handshake, closed request/result/error vocabulary, monotonic
  sequencing, one total process-output budget, ioctl-backed PTY resize, atomically
  durable content-bound patch staging, chunked file/patch/export, lifecycle
  inspect, quiesce, and shutdown. The vfkit broker derives the expected channel binding
  from its current recovery record and rechecks endpoint identity across connect.
  This is `protocol implemented`. A feature-gated local transport runs the real
  guest binary and covers admission refusal, outcome/evidence combinations,
  deadline non-extension, exact wire bounds, partial transfers, lost patch-stage
  receipts, stale nonce, replay, overflow, disconnect, and the full mechanics path;
  one production connection carries at most one operation, and the synchronous
  single-runtime guest loop serializes effects per environment without extending
  the host lifecycle lock across guest I/O. This is `conformance proven`. The pinned-image builder and exact real-vfkit
  deployment harness now add the separate `deployment evidence proven` state for
  the host/guest substrate: EFI full-system boot, verified AF_VSOCK handshake,
  systemd/PID 1, harmless kernel and mount operations, offline package install,
  no-NIC/no-SSH/no-share/no-credential posture, real PTY, file/patch/export,
  bounded output, observed CPU/RAM/disk/TasksMax plan and PID exhaustion, dirty recovery, replay/conflict refusal,
  stale-generation refusal, cooperative drain, deterministic teardown, and a
  schema-gated redacted timing report under explicit functional budgets. The
  builder completion record and report bind the executed VMM, image, firmware,
  and guest-agent digests; an external readiness marker is not evidence. P083 two-controller routing remains required
  before virtualized PTY is enabled.

Frozen reference sequence:

| Profile | Role | Boundary |
| --- | --- | --- |
| `vfkit-system.v1` / `macos-vz-arm64.v1` | first developer reference and first process-isolated implementation slice | pinned vfkit over Apple Virtualization Framework; EFI full GNU/Linux arm64 image; APFS raw-disk clone; dedicated virtio-vsock-to-UDS control channel; block/vsock/rng only; no serial device, NIC, SSH, host share, Rosetta, credentials, or snapshots |
| `cloud-hypervisor-system.v1` / `linux-kvm-x86_64.v1` | first Linux deployment profile | pinned Cloud Hypervisor and firmware; explicit raw image; unprivileged identity, cgroup v2, host filesystem confinement, closed devices, no NIC by default, and the same guest protocol |
| `firecracker-system.v1` / compatible Linux KVM profile | subsequent minimal-device hardening backend | introduced after the image manifest and guest protocol stabilize; must pass the same backend-neutral conformance suite under a jailer-equivalent host boundary |

VMM administration sockets remain private to the host broker. Diagnostic serial
is output-only; it is not a second interactive control path. Serial bytes are
untrusted guest data: ordinary logs remain metadata-only, explicit captures are
bounded and inherit environment classification plus operational context, and
operator rendering strips terminal-control sequences and escapes control bytes
rather than writing raw data to a terminal.

The reference guest runs `orbiplex-workbench-guest` over virtio-vsock without IP
or SSH. Every boot advances source generation unless an exact live boot is being
recovered, and binds environment, plan/image digests, a fresh boot nonce, bounded
operation frames, and the dedicated control endpoint. Guest output remains
untrusted; host resource containment does not depend on guest cooperation.

OCI may distribute signed, digest-pinned image variants, SBOM, provenance, and
guest-agent artifacts, but an OCI runtime does not own Workbench lifecycle or
authority. Variants share one logical image ref only when their canonical
userspace/rootfs, SBOM, build provenance, guest-agent binary, and guest-protocol/
schema-set digests match; kernel, initrd, firmware, disk layout, and boot artifacts
remain variant-specific and require independent conformance. Memory snapshots and
live migration are outside the v1 recovery contract.

### Operational Impact Publication

The implemented P082-021/P083-014 extension requires each exact Workbench
environment to pin a `sensorium-operational-context.v1` candidate. An adapter may
provide an operator-configured default, but environments sharing that adapter may
still be `test`, `production`, or `critical`. Host policy may raise but never lower
the current source class. A process-isolated normalized plan pins the effective
context before allocation; non-`none` networking or non-denied host sharing has at
least a `test` floor, and a higher reachable/shared-resource class is inherited.
Unknown target context fails closed. The reference full-system configuration proof
uses `test`; a contained offline disposable VM may remain `experimental`, because
`hardware-vm` is not an impact class. Every derived observation or actuation
interface inherits the result with a host-owned source generation. Impact changes
and operator corrections use audited immutable P082 replacement, making old
generations and superseded publications unusable. The bundled connector derives a
process-epoch-bound generation from the complete environment projection, preserves source summary only
when all highest-impact roots agree on the exact context, and requires actuation
authority to match both environment ref and current generation. P071 Phase 5 and the
P082/P083 trackers contain the runtime and refusal evidence.

Status: `done post-MVP` for operational-impact publication, the fixture admission
spine, backend-neutral guest runtime, real-vfkit host/guest deployment, P083-backed
virtualized Workbench integration, and the additive one-runtime Story 012 vfkit
vertical. Restarted guest PTY sessions and command replays now
return a typed relink result, and terminal close uses a local `closing`
transition to serialize concurrent effects without retaining a lock across guest
I/O; dedicated acceptance checks cover restart supersession and concurrent
environment teardown. Exact Rust checks are resolved by `libtest --list` before
execution instead of parsing progress text. Cloud Hypervisor and Firecracker
remain separately evidenced future Linux profiles, not completion blockers for
the implemented vfkit reference profile.

### Agent, Corpus, and Room Tool Use

Based on:

- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/60-solutions/047-agent/047-agent.md`
- `doc/project/60-solutions/038-corpus/038-corpus.md`

Related schemas:

- `sensorium-command-intent.v1`
- `sensorium-workbench-outcome.v1`
- `sensorium-workbench-tool-request.v1`

Responsibilities:

- let Agent, Corpus, or Room workflows request bounded Workbench tool use
  through host policy;
- keep all effects mediated by Sensorium and Workbench grants;
- reject any adapter that owns terminal or filesystem authority outside the
  Workbench boundary.

Status:

- `implemented` as the shared admission boundary: Agent, Corpus, and Room
  requests wrap an ordinary Workbench directive in
  `sensorium-workbench-tool-request.v1`; the daemon verifies an admitted Agent
  proposal, active Corpus round, or current execution-derived answer-room
  projection, stamps host-owned source metadata, and then invokes
  Sensorium Core. Agent proposals bind to one `directive/id` with idempotent
  replay. Product-specific workflow producers remain owned by Agent, Corpus,
  and Room rather than Workbench.

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
