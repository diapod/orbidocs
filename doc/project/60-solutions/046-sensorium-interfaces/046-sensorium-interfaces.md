# Sensorium Interfaces

Based on:

- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/036-room/036-room.md`
- `doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`
- `node:sensorium-interface-core`
- `node:daemon/src/sensorium_interface_runtime.rs`
- `node:daemon/src/sensorium_interface_room_projection.rs`
- `node:daemon/src/peer_runtime_host.rs`
- `node:daemon/src/host_capabilities_host.rs`
- `node:tools/conformance/sensorium_interfaces_conformance.py`

Related schemas:

- `sensorium-interface-descriptor.v1`
- `sensorium-interface-status.v1`
- `sensorium-interface-read-request.v1`
- `sensorium-interface-read-result.v1`
- `sensorium-interface-subscribe-request.v1`
- `sensorium-interface-subscription-command.v1`
- `sensorium-interface-subscription-status.v1`
- `sensorium-interface-frame.v1`
- `artifact-object-pointer.v1`
- `classification.v1`
- `capability-passport.v1`
- `vendor-media-type-registry.v1`

## Status

Implemented MVP solution.

The carrier-neutral pull-batch core, durable host runtime, open bounded source
adapter registry, Sensorium, Workbench, and Artifact Delivery source adapters,
local host-capability surface, authenticated direct-peer surface, local SSE
adapter, and WSS-backed Room `latest-state` projection are implemented.
The runtime is refusal-tested for stale or revoked authority, cursor misuse,
ordered-event Room projection, classification mismatch, and restart recovery.
Host-local bounded metrics and a four-carrier conformance runner provide the
operator evidence surface needed for post-V1 delivery decisions.

## Date

2026-07-16

## History

This solution promotes the frozen and implemented Proposal 082 contract into a
separate component. Proposal 082 remains the rationale, invariant catalog,
resolved-decision record, and implementation tracker. This solution owns the
current implementation boundary and its post-MVP extension points.

## Executive Summary

A Sensorium Interface is a host-owned, explicitly published read-only projection
of an enacted representation. It gives authorized local components or remote
peers one bounded operation family:

```text
publish source projection
  -> authorize exact interface resource
  -> read one bounded batch or open a bounded subscription
  -> pull the next batch through a carrier adapter
```

The resource is not a connector, transport, store, or capability. Sensorium,
Workbench, and Artifact Delivery own or admit source facts. Interaction Broker
owns bounded source observation.
The Sensorium Interfaces runtime owns publication, grants, subscriptions,
cursors, classification checks, lifecycle, and revocation. Direct peer, SSE, and
Room WSS are edge adapters and never become authority.

The implemented V1 delivery contract is bounded cursor-based pull-batch.
Provider push, global descriptor discovery, and automatic stream persistence are
outside this solution's MVP boundary.

## Context and Problem Statement

Sensorium observations, Workbench terminal representations, and admitted Artifact
Delivery pointers need a shared way to be deliberately exposed without giving
consumers access to connector credentials, terminals, or private provider stores.
Implementing each exposure as a separate stream API would duplicate authorization,
cursor, replay, classification, revocation, and backpressure semantics.

Sensorium Interfaces provides one contract above the producer-specific adapters
and below carrier-specific presentation. This keeps a temperature snapshot, a
Workbench terminal screen, a bounded terminal event batch, and an immutable
artifact pointer structurally comparable while preserving their distinct schemas
and delivery semantics.

## Proposed Model / Decision

The solution is stratified as:

```text
sensorium-interface-core
  schemas, lifecycle, delivery semantics, cursor binding, limits,
  classification and declassification validation

Interaction Broker source-provider adapter
  one domain source, generic private bindings, bounded adapter registry,
  source-specific validation and batch production

daemon Sensorium Interfaces runtime
  publication, grants, subscriptions, immutable management facts,
  idempotency, restart projection, revocation and inspection

carrier adapters
  local host capability, direct authenticated peer, local SSE,
  WSS Room latest-state projection
```

Only the runtime may translate current resource authority into a read or
subscription. A cursor is change/replay state, not a bearer token. A carrier
session is presentation state, not a grant. Every batch rechecks current caller,
resource, lease, classification, limit, and revocation constraints.

## Must Implement

### Contract and Pure Core

Responsibilities:

- own the eight closed Sensorium Interface schemas and typed semantic errors;
- enforce one-shot versus subscription shape, cursor binding, terminal status,
  `latest-state` no-replay, ordered-event replay bounds, and independent frame
  and batch byte caps;
- require `classification.v1` on every frame and exact payload-label equality
  when a payload embeds classification;
- accept declassification only for `Surface::Interface` with the descriptor's
  exact topic class and current fact validity;
- keep the core independent of daemon, transport, SQLite, async runtime, and
  concrete providers.

Status: `done`.

### Source Adaptation

Responsibilities:

- expose one `sensorium-interface` source kind through Interaction Broker;
- compose source authority with interface authority rather than allowing either
  to stand in for the other;
- adapt admitted Sensorium observation latest state;
- adapt Workbench terminal screen latest state separately from ordered terminal
  events;
- admit immutable Artifact Delivery object pointers through a read-only
  `artifact-snapshot` latest-state adapter;
- keep source-specific validation and production behind a bounded registry and
  revalidate persisted bindings after restart;
- require all four built-in adapters at daemon startup while treating readiness
  snapshots as advisory and each bounded source read as authoritative;
- preserve source classification and apply redaction before publication.

Status: `done`.

### Host Runtime and Authority

Responsibilities:

- implement publish, suspend, withdraw, grant, revoke, inspect, subscribe,
  renew, close, and read-next lifecycle operations;
- register `sensorium.interface.read`, `sensorium.interface.subscribe`, and the
  host-local `sensorium.interface.manage` capability;
- persist immutable management facts and rebuild disposable publication,
  grant, idempotency, and subscription projections after restart;
- bind grants and subscriptions to canonical namespaced actor refs, exact
  interface ids, capability class, expiry, lease, and current revocation
  evidence;
- serialize cursor advancement per subscription without blocking independent
  subscriptions, and admit a verified Passport in one immediate transaction;
- append canonical causal context and execution receipts without treating
  either as authority.

Status: `done`.

### Carrier Adapters

Responsibilities:

- expose local host-capability reads and management through authenticated host
  caller binding;
- admit direct-peer requests only after signed Capability Passport validation
  against `sensorium-interface@v1`, exact authenticated remote target, local
  source-node issuer, resource, operation, classification ceiling, batch caps,
  lease, and revocation freshness;
- expose local SSE only over loopback and only for an already admitted,
  caller-bound subscription;
- identify SSE and Room projection read-next operations separately in canonical
  causal context;
- project WSS Room views as a dedicated `latest-state` session whose recipient
  set is the intersection of current Room observation rights and current
  Sensorium Interface grantees, matched only by canonical Room subject key;
- omit source cursors from Room frames, refuse ordered-event interfaces, and
  close only the projection session on terminal or revoked authority;
- cap active Room projection pumps at 64 and reap terminal pump and carrier
  state together before admitting replacement work.

Status: `done`.

### Acceptance and Operator Evidence

Responsibilities:

- prove one-shot and subscription temperature flows, revocation, terminal
  status, idempotent replay, and restart rebuild;
- prove a signed direct-peer request through the standard peer message chain;
- prove exact Passport target binding, concurrent idempotent Passport admission,
  revoked-Passport replay diagnostics, and independent per-subscription read
  locks;
- prove that the Passport scope tier vocabulary remains aligned with the shared
  classification lattice and that schema-gate rejects structurally conflicting
  frame payload sources;
- prove local SSE batch delivery and terminal close after grant revocation;
- prove collaborative Workbench terminal-view projection through Room WSS,
  including recipient revocation and durable Room survival;
- expose schemas and the local SSE route through the daemon API projection;
- expose a host-local operator snapshot with bounded source/carrier/delivery-kind
  dimensions, batch occupancy, no-change, encoding-error and read
  error counts, active leases, Room pump counts, and flat local revoke transaction
  commit duration;
- degrade unavailable source-registry, active-subscription, metric-accumulator, and
  Room telemetry as isolated snapshot sections rather than failing the read-only
  operator action;
- run one conformance harness across bounded host load, signed direct-peer reads,
  SSE revocation, and Room projection revocation;
- keep external denial details generic while retaining local diagnostic traces.

Status: `done`.

## May Implement

### Measured Provider-Push Profile

A provider-push protocol may be added only if operational measurements show
that bounded read-next cannot meet a concrete latency or cost requirement. It
must be a separately acknowledged profile, not an implicit alternate meaning of
the V1 contracts.

Status: `deferred`.

### Searchable Descriptor Catalog

A federation-scoped descriptor catalog may be added only with an explicit
disclosure policy, query bounds, anti-enumeration posture, and revocation model.
V1 descriptor disclosure remains direct-grant or authorized-collaboration only.

Status: `deferred`.

### Split Management Authorities

Publication and grant administration may become separate local capabilities if
deployment evidence shows that distinct principals routinely own them. The MVP
keeps one source-local manage capability with action-specific policy.

Status: `deferred`.

## Trade-offs

- Pull-batch adapters add polling latency but preserve one semantic contract and
  one revocation point across transports.
- Exact resource grants make ambient discovery impossible, but materially reduce
  descriptor and sensor enumeration risk.
- Room projection revalidates two authority domains per emission. This costs
  more than trusting membership, but prevents the carrier from silently
  widening observation rights.
- The runtime serializes cursor advancement within each subscription to preserve
  deterministic read-next behavior, while independent subscriptions progress
  concurrently.
- The MVP Room adapter owns one OS thread per projection for its bounded
  long-poll loop. A hard 64-pump ceiling prevents thread exhaustion; a shared
  dispatcher remains a measured post-MVP optimization.
- Runtime metrics are process-local and reset on restart. This avoids creating a
  second durable telemetry store; representative evidence collection must export
  snapshots externally when persistence is required.

## Failure Modes and Mitigations

| Failure mode | Consequence | Mitigation |
|---|---|---|
| Cursor is replayed by another caller | Unauthorized observation or cursor corruption | Bind cursor and subscription to authenticated actor, exact interface, and current grant. |
| Grant or Passport is revoked during a stream | Continued observation after authority ends | Recheck revocation before source read and carrier emission; close with a typed terminal reason. |
| Room membership is treated as interface authority | Room member sees an ungranted terminal or sensor | Intersect Room `observe` rights with active interface grantees for every emission. |
| A bare grantee id collides across Room subject kinds | Authority for one principal widens to another namespace | Reject non-namespaced grantee refs at grant creation and intersect only canonical `RoomSubject::stable_key()` values. |
| Source reports `no-change` | Adapter mistakenly closes the stream | Preserve `no-change` as a non-terminal batch outcome. |
| Ordered events are projected through MVP Room WSS | Cursor leakage or false replay guarantees | Refuse attachment before starting the carrier pump. |
| Source or carrier exceeds bounds | Memory growth or oversized live frame | Enforce request, frame, batch, source-read, and Room-message caps independently. |
| Repeated Room projections exhaust host threads or retain terminal payloads | Resource exhaustion over time | Cap active pumps at 64 and reap terminal daemon and carrier entries together. |
| Resource lookup denial reveals existence | Descriptor enumeration oracle | Return one generic external denial and retain details only in local traces. |
| Daemon restarts with active subscriptions | Authority or terminal state drifts | Rebuild from durable facts and persisted subscription status before accepting work. |
| A source adapter disappears or its persisted config becomes invalid after restart | A stale publication bypasses current source policy | Revalidate the generic binding and current registered adapter before every source read. |
| Metrics acquire resource or caller identifiers | Unbounded cardinality or sensitive operational disclosure | Limit dimensions to at most 64 registered source kinds plus unresolved reads, four carriers, and two delivery kinds; expose only aggregate counters and timings. |
| Revoke transaction duration is presented as end-to-end enforcement lag | Operators receive misleadingly optimistic evidence | Expose the flat measurement as `revoke-commit-us`; enforce local and peer bounds through pull-loop and revocation-freshness budgets, and measure those boundaries separately. |
| One operator-snapshot source fails | Operator loses unrelated runtime evidence | Degrade source-registry, active-subscription, metric-accumulator, and Room sections independently to `unavailable`, log the local error, and keep core read paths independent from telemetry health. |

## Open Questions

No open question blocks the implemented MVP. Post-V1 decisions require measured
deployment evidence:

1. Does measured latency justify a separately negotiated provider-push profile?
2. Does federation use justify a searchable descriptor catalog with an explicit
   disclosure policy?
3. Do deployments need separate publication and grant-administration
   capabilities?

## Next Actions

1. Export representative snapshots from the implemented host-local `metrics`
   action and compare read-next latency, no-change rate, and batch occupancy by
   carrier, delivery kind, and source kind. Inspect flat revoke commit cost
   separately and measure enforcement at local carrier and peer freshness
   boundaries.
2. Add another producer adapter only when it can reuse the same classification,
   cursor, and authority contracts without a source-specific escape hatch.
3. Keep provider-push, descriptor search, and split management authority as
   separate post-V1 decisions backed by operational evidence.
