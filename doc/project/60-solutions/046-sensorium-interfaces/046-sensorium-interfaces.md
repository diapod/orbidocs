# Sensorium Interfaces

Based on:

- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/40-proposals/083-sensorium-interactive-interfaces.md`
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
- `node:daemon/src/sensorium_interface_runtime/actuation_runtime.rs`
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
- `sensorium-interface-resource.v1`
- `sensorium-interface-actuation-descriptor.v1`
- `sensorium-interface-actuation-status.v1`
- `sensorium-interface-actuation-grant-scope.v1`
- `sensorium-interface-control-request.v1`
- `sensorium-interface-control-status.v1`
- `sensorium-interface-control-lease.v1`
- `sensorium-interface-invoke-request.v1`
- `sensorium-interface-invoke-receipt.v1`
- `sensorium-interface-terminal-input.v1`
- `sensorium-interface-terminal-resize.v1`
- `sensorium-interface-terminal-signal.v1`
- `sensorium-interface-led-set.v1`
- `artifact-object-pointer.v1`
- `classification.v1`
- `capability-passport.v1`
- `vendor-media-type-registry.v1`
- `room-relay-delivery.v1`

## Status

Implemented observation and actuation MVP solution.

The carrier-neutral pull-batch core, durable host runtime, open bounded source
adapter registry, Sensorium, Workbench, and Artifact Delivery source adapters,
local host-capability surface, authenticated direct-peer surface, local SSE
adapter, and WSS-backed Room `latest-state` projection are implemented.
The runtime is refusal-tested for stale or revoked authority, cursor misuse,
ordered-event Room projection, classification mismatch, and restart recovery.
Host-local bounded metrics and the extended conformance runner provide the
operator evidence surface needed for post-V1 delivery decisions.
This implementation satisfies the explicit P082 hard-MVP release blocker.
The P083 schema, capability, core, durable coordinator, LED, host/direct-peer,
Workbench PTY, operator/Room collaboration, conformance, and synchronization slices
are implemented and refusal-tested. P083-012 promotes that reviewed actuation
extension into this solution and satisfies the P083 hard-MVP release blocker.
P070 Phase 6A now also supplies the shared relay-epoch carrier used by the Room
latest-state pump and the closed P083 status/claim/control/invoke/receipt classes;
direct peer remains an optional latency path and owns no additional authority.

## Date

2026-07-17

## History

This solution promotes the frozen and implemented Proposal 082 contract into a
separate component. Proposal 082 remains the observation rationale and tracker;
Proposal 083 remains the actuation rationale, invariants, and post-MVP tracker.
P083-012 promotes its implemented hard-MVP boundary into this solution. This solution
owns the combined implementation boundary without introducing a second publication,
grant, revocation, or authority service.

## Executive Summary

A Sensorium Interface is a host-owned, explicitly published directional projection
of or input surface for an enacted representation. The promoted observation plane
gives authorized local components or remote peers one bounded pull family:

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

The promoted actuation plane adds a separate bounded effect family:

```text
publish effect adapter
  -> authorize exact interface methods
  -> read grant-gated status and claim fenced control when required
  -> invoke with current source generation and lease epoch
  -> return a metadata-only evidence-classified receipt
```

Observation authority never implies actuation authority. A collaboration carrier,
Room membership, or control lease cannot replace the exact active interface grant.

[Proposal 083: Sensorium Interactive Interfaces](../../40-proposals/083-sensorium-interactive-interfaces.md)
defines the promoted actuation rationale with separate resources, grants,
coordination, and fencing. Its implementation reuses this component's core, authority
runtime, store, admission, fact, receipt, classification, adapter, and carrier
boundaries. P083-012 records the final review and promotion into this solution.

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

### Actuation Foundation

Promoted responsibilities implemented through P083-011 and closed by P083-012:

- extend the common resource envelope with closed per-method actuation descriptors,
  control leases, invoke requests/receipts, exact grant scopes, and Workbench input
  schemas;
- register Passport-eligible `sensorium.interface.invoke` with the exact
  `sensorium-interface-actuation@v1` profile while keeping action-enumerated
  `sensorium.interface.manage` source-local;
- reuse the pure core and durable authority runtime for bounded shared ordering,
  exclusive claims, lease epochs, handoff, preemption, generation fencing,
  content-bound idempotency, restart, revocation, inspection, aggregate metrics,
  and a symmetric 16 MiB read/write cap on each serialized coordinator projection;
- keep read-source and effect-adapter traits separate while reusing bounded registry
  mechanics, including fail-closed duplicate, unavailable, unknown, and over-cap
  behavior; adapter readiness is a health hint, while effect-time provider state is
  authoritatively checked by `apply`;
- expose host-local and authenticated direct-peer actuation without deriving
  authority from observation or carrier attachment;
- route Workbench terminal input, resize, and signal through exact schemas and a
  remote-caller control authority that reaches the PTY boundary without impersonating
  the operator; provider-confirmed terminal closure withdraws the actuation source,
  changes its opaque generation, and clears transient control;
- persist metadata and digests rather than raw actuation payloads, report honest
  `unknown` outcomes for uncertain irreversible effects, and keep evidence refs
  opaque from private Workbench session bindings;
- expose strict manage actions over a bounded process-local Room collaboration
  group registry and reuse existing grant, inspection, and preemption surfaces;
- keep P070's 256-bit Room session bearer outside messages, acknowledgements, shared
  observations, collaboration-group state, and operator/member status;
- derive collaborative callers and current `actuate` membership atomically from
  one live Room transport snapshot, and intersect it with exact interface, method,
  generation, lease, epoch, sequence, and host policy authority;
- keep observation authority separate, expose bounded claim polling hints, lose
  ephemeral groups fail-closed on restart, remove explicit withdrawals immediately,
  reap closed/terminal Rooms before group access or inspection, preserve Room-scoped
  groups across one member-session disconnect, and never relay terminal bytes as Room
  messages;
- run the expanded exact-name conformance matrix across load saturation, expiry,
  renewal, handoff, stale epochs, restart, partial failure, Room dual authority,
  and two controllers writing through a real Workbench PTY.

Status: `done`.

## May Implement

### Relocatable Room Relay Carrier

P070 Phase 6A implements the authority-neutral Room relay as the default
firewall-proof carrier contract for collaborative latest-state and P083 interaction
whenever an active endpoint is projected. The P082 adapter keeps its source cursor
private: `(relay/epoch, relay/seq-no)` is only carrier resume state, and failover or
carrier cursor expiry triggers a fresh current-state read after current Room and
interface authority are rechecked.

P083 status, claim, control, invoke, and receipt use the same coordinator contracts and
fencing over the relay. Authenticated direct peer remains an optional latency upgrade,
not a lease or correctness requirement. This work is owned by P070 Phase 6A plus
P082-020/P083-013; it must not create a Sensorium-specific relay or NAT traversal
protocol.

Status: `done post-MVP` through P070 Phase 6A, P082-020, and P083-013. The relay
transports typed requests and receipts but never executes an effect or supplies
authority on behalf of the destination host.

### Measured Provider-Push Profile

The accepted baseline adds no provider-push or push-hint protocol. A future
revision may reconsider one only if operational measurements show that bounded
read-next cannot meet a concrete latency or cost requirement. It must be a
separately acknowledged profile and share one authority-neutral,
disclosure-bounded readiness-hint substrate with P083 rather than duplicate it.
Each hint audience must pass the same current grant and applicable
collaboration-policy checks as the corresponding read or claim, so notification
leaks no unauthorized resource activity.

Status: `deferred`.

### Searchable Descriptor Catalog

The accepted baseline has no searchable descriptor catalog. Caller inspection of
interfaces already disclosed by current authority is not discovery and preserves
leak-minimal lookup. A future existence-discovery catalog is a separate disclosure
oracle and requires an explicit policy, query bounds, anti-enumeration posture,
revocation model, and contract revision.

Status: `deferred`.

### Split Management Authorities

The accepted baseline keeps one source-local, non-delegable manage capability.
Current runtime dispatch and authorization policy enumerate the closed observation
and actuation action vocabulary, including `control.preempt`; preemption also
requires an active exact invoke grant before it can establish an operator lease.
Any future capability split requires distinct-principal deployment evidence and a
contract revision.

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
| Room membership is mistaken for actuation authority | A collaborator invokes an ungranted method or stale lease | Require current `actuate`, canonical session subject, exact active interface grant, grouped method, generation, and current lease fencing before dispatch. |
| A Room bearer is projected or echoed | Another member can reuse a session identity | Keep the 256-bit random ref only in the joining client's admission envelopes and bind frame subjects outside payloads. |
| Collaboration groups outlive their Room or occupy capacity after withdrawal | Process-local state becomes unusable or saturates | Remove withdrawals immediately; reap closed/terminal Room groups before access, management, and operator snapshots; clear all groups at daemon stop. |
| Terminal input is sent as an ordinary Room live message | Raw keystrokes bypass typed actuation admission or enter the wrong collaboration semantics | Carry input only as a schema-gated P083 relay delivery; retain it only in the bounded ephemeral epoch window, recheck the exact interface grant and fencing at the host, and persist only metadata/digests. |
| Relay or direct-peer upgrade is treated as control ownership | Carrier failover transfers or widens actuation authority | Keep grants and fenced leases in the host coordinator; carrier replacement changes transport only and must recheck current Room plus interface authority. |

## Open Questions

No unresolved design questions remain. Proposal 082 decisions 7-9 retain bounded
pull-batch, direct authority-scoped disclosure, and one source-local manage
capability. The deferred sections above are reconsideration boundaries, not open
implementation choices.

## Next Actions

1. Export representative snapshots from the implemented host-local `metrics`
   action and compare read-next latency, no-change rate, and batch occupancy by
   carrier, delivery kind, and source kind. Inspect flat revoke commit cost
   separately and measure enforcement at local carrier and peer freshness
   boundaries.
2. Add another producer adapter only when it can reuse the same classification,
   cursor, and authority contracts without a source-specific escape hatch.
3. Keep pull-batch, direct disclosure, and one source-local manage capability as
   the baseline. Require an explicit evidence-backed contract revision for any
   provider-push, existence-discovery, or management-authority split.
4. Collect P082-020/P083-013 relay latency, cursor-expiry, and failover evidence through
   the shared Room diagnostics rather than adding Sensorium-specific reachability or
   failover logic.
