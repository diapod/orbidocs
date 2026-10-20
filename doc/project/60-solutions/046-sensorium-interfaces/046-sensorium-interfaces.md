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
- `node:daemon/src/sensorium_interface_remote_feed.rs`
- `node:daemon/src/sensorium_interface_runtime/actuation_runtime.rs`
- `node:daemon/src/sensorium_interface_room_projection.rs`
- `node:daemon/src/peer_runtime_host.rs`
- `node:daemon/src/host_capabilities_host.rs`
- `node:tools/conformance/sensorium_interfaces_conformance.py`
- `node:tools/acceptance/sensorium-terminal-live-feed/run.py`

Related schemas:

- `sensorium-operational-context.v1`
- `sensorium-interface-descriptor.v1`
- `sensorium-interface-status.v1`
- `sensorium-interface-read-request.v1`
- `sensorium-interface-read-result.v1`
- `sensorium-interface-subscribe-request.v1`
- `sensorium-interface-subscription-command.v1`
- `sensorium-interface-subscription-status.v1`
- `sensorium-interface-frame.v1`
- `sensorium-terminal-event.v1`
- `sensorium-interface-remote-feed-request.v1`
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
P082-022 additionally completes a canonical exact-byte terminal event contract,
bounded Workbench replay with explicit gaps and terminal end, an owner-bound
recipient-side direct-peer feed, and local SSE presentation for both local and
remote admitted subscriptions. Recipient-side peer egress requires the separate
host-local `sensorium.interface.remote-feed` grant; source reads continue to require
an exact signed `sensorium.interface.subscribe` Passport.

## Date

2026-07-22

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

The implemented V1 delivery contract is bounded cursor-based pull-batch. Local
and direct-peer live terminal views are projections over that same contract: the
recipient host advances the admitted subscription and presents batches through
loopback SSE rather than introducing provider push or carrier authority. A
Workbench retention gap is projected before retained events, while recipient
reconnect forwards its stale cursor and preserves the source-reported gap. The
real guest proof keeps two PTYs live together and demonstrates that their bytes
and cursors remain isolated.
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
Ordinary Corpus deliberation requires neither plane. An admitted Sensorium Interface
is an optional context or effect channel for a consumer that needs an enacted
representation; it does not define the problem domain or confer authority through
participation alone.

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

### Planned Local Device Discovery Boundary

[P045 local device discovery continuation](../../40-proposals/045-sensorium-local-enaction-stratum.md#local-device-discovery-continuation)
owns the planned shared discovery contract and the sole `P045-DISC-001`–`007`
tracker. [P082](../../40-proposals/082-sensorium-interfaces.md#20-planned-local-device-discovery-is-not-interface-discovery)
preserves the publication/read boundary. The planned local candidates are
short-lived, caller-private scan results, not published Interface descriptors,
source observations, artifact pointers, or catalogue entries. They must not
enter Interface read/subscribe adapters, Room/Agora projections, or federated
descriptor discovery.

Discovery, operator-confirmed binding, source acquisition, explicit Interface
publication, and an exact consumer read/subscription each retain separate
authority. A successful scan or binding does not create a source or publication;
Interface access does not authorize scanning, pairing, or acquisition. Subsequent
publication of an admitted source reuses this solution's existing source-policy,
classification, management and grant checks.

Status: `planned` under P045. This continuation adds no implemented source
adapter or Interface operation and does not alter this solution's implemented
MVP. The searchable descriptor catalogue below remains deferred and concerns
disclosure of published interfaces, independently of local device candidates.

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

### Optional Sensorium Web latest-state adapter

P084 adds `sensorium-web-latest-state` through the existing open bounded source
registry. It is registered only when the `sensorium-web` middleware module is
configured and is deliberately not a fifth required built-in. The adapter reads
only an already admitted latest snapshot, rechecks source/generation and the
canonical snapshot digest, coalesces an unchanged cursor to `no-change`, and has
no refresh method. Existing local SSE, direct-peer, and Room carriers therefore
remain transport projections rather than acquisition authority. Dedicated real
TLS peer read/subscription and local Room WebSocket acceptance now closes
P084-008 with exact Passport scopes, dual Room/interface authority, revocation,
generation fencing, explicit supersession and remote-refresh refusal. The Room
fixture supplies admitted membership facts; this does not claim federated relay
or remote membership issuance. Evidence is retained in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-REMOTE-INTERFACE-EVIDENCE.md`. The strengthened 1.2.0
profile run also proves secret-canary absence in operator/carrier data and real
retained artifacts; link query values are removed before digest binding. Its
explicit profile migration requires a new generation and fresh publication
authority. Full capacity, controlled failures and the combined review close
P084-009 in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-STATIC-ACCEPTANCE-EVIDENCE.md`; P082 hard-MVP
readiness is unchanged. The real macOS local read/SSE slice is retained in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-LOCAL-INTERFACE-EVIDENCE.md`: admitted payload/digest
binding, no-change, changed snapshots, revocation, generation fencing, and
explicit supersession requiring fresh grants, with zero consumer-triggered fetches.

P084-012a also composes this adapter with local Harvester intake. An operator
session configures an immutable source binding, but each selected-snapshot import
still requires an independent current interface read grant. The bridge verifies
the retained document-block artifact and repeats admission after artifact I/O;
findings preserve source classification and exact provenance. It adds no refresh,
remote handoff or publication path. Evidence:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-EVIDENCE.md`.

### P084-012a review hardening

Review H-1 through H-10 distinguishes pre-claim `not-started` refusal from
settling an already claimed operation, using the same refresh-status contract
and failure semantics. A bounded refusal projection isolates the rejected
source generation and makes its reason visible without consuming operation
slots or starving healthy sources. The 1.2.1 extraction revision computes link
truncation after deduplication. Harvester configuration equality is semantic;
no-op registration returns HTTP 200. Safe host trace categories preserve refusal
causes, and the post-artifact read uses its own causal child operation without
extending the original deadline. Evidence:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-REVIEW-EVIDENCE.md`.

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
- revalidate current publication and source bindings after successful or failed
  provider I/O so terminal generation and supersession failures retain their
  interface type across the consumer-neutral broker boundary;
- require the four settled adapters and the P096 synthetic-only biosignal
  adapter at daemon startup while treating readiness snapshots as advisory and
  each bounded source read as authoritative; the biosignal adapter resolves
  existing acquisitions only and retains its separate qualification gates;
- preserve source classification and apply redaction before publication.
- validate Workbench terminal output as exact bytes with matching digest/count,
  preserve explicit retained-floor gaps, and map terminal source closure to one
  terminal batch without advancing past unconsumed capped events.

Status: `done`.

The P096 synthetic adapter now has retained four-case same-process host-API
acceptance (P096-010a). Its native and remote carriers remain gated separately;
registration/readiness does not activate a source or qualify another carrier.

### Host Runtime and Authority

Responsibilities:

- implement publish, suspend, withdraw, grant, revoke, inspect, subscribe,
  renew, close, and read-next lifecycle operations;
- register `sensorium.interface.read`, `sensorium.interface.subscribe`, and the
  host-local `sensorium.interface.remote-feed` and `sensorium.interface.manage`
  capabilities;
- persist immutable management facts and rebuild disposable publication,
  grant, idempotency, and subscription projections after restart;
- bind grants and subscriptions to canonical namespaced actor refs, exact
  interface ids, capability class, expiry, lease, and current revocation
  evidence;
- serialize cursor advancement per subscription without blocking independent
  subscriptions, and admit a verified Passport in one immediate transaction;
- freeze the exact grant selected before provider I/O and recheck it with fresh
  subscription state in the delivery transaction serialized with local
  revocation; a new grant cannot admit an old read, a closed subscription cannot
  be restored by late output, and valid lease renewal remains preserved;
- append canonical causal context and execution receipts without treating
  either as authority.

Status: `done`.

### Carrier Adapters

Responsibilities:

- expose local host-capability reads and management through authenticated host
  caller binding; derive `module:<module-id>` from that binding consistently for
  capability admission, causal-context validation, feed ownership, and local SSE,
  rather than accepting the request body's actor as authority;
- admit direct-peer requests only after signed Capability Passport validation
  against `sensorium-interface@v1`, exact authenticated remote target, local
  source-node issuer, resource, operation, classification ceiling, batch caps,
  lease, and revocation freshness;
- expose local SSE only over loopback and only for an already admitted,
  caller-bound subscription;
- allow a recipient-side direct-peer feed only with local remote-feed authority,
  then select an active signed subscribe Passport for the authenticated source
  node, pin the returned resource, subscription, delivery kind, and caps, and expose
  it only to its creating local caller through loopback SSE;
- bound every peer wait to five seconds, reject WSS messages above 1 MiB before
  application decoding, and measure the result against requested `batch.bytes_max`
  before typed deserialization; retry only transport unavailability;
- register a consumer-side integrity validator for every inline schema that carries
  byte-evidence and re-compute its count and digest before presentation;
- identify SSE and Room projection read-next operations separately in canonical
  causal context;
- project WSS Room views as a dedicated `latest-state` session whose recipient
  set is the intersection of current Room observation rights and current
  Sensorium Interface grantees, matched only by canonical Room subject key;
- omit source cursors from Room frames, refuse ordered-event interfaces, and
  close only the projection session on terminal or revoked authority;
- cap active Room projection pumps at 64 and reap terminal pump and carrier
  state together before admitting replacement work;
- keep pump intent process-local: source-host restart requires an explicit local
  projection restart, while recipient restart can refresh the relay's bounded
  current latest-state delivery without durable Sensorium pump state.

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
- prove exact non-UTF-8 terminal bytes, bounded Workbench retention gaps, terminal
  end, owner-bound direct-peer cursor advancement, and remote pull-batch projection
  through local SSE;
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

P082 latest-state relay publication uses the closed
`sensorium-interface-read-result.v1` resource envelope with one inline
cursor-free snapshot, not a bare frame. The destination host may expose that
resource through Interaction Broker only under an exact host-component context.
The Story 012 daemon resolver maps a statically bound opaque Agent observation
source to this adapter, then rechecks Room membership generation, relay epoch,
exact interface authority, schema, classification, freshness, and byte bounds
around the broker read. These Room/Sensorium axes remain private to the daemon;
`agent-core` contains only the generic need/binding/evidence contract and reuses
the horizontal P081 causal context without importing Sensorium semantics.
Observation content remains process-local and passage-bounded; durable broker and
Agent records retain no raw payload.

Story 012 receives the delivery through an authenticated Room subscription and
compares its epoch with the relay acknowledgement rather than deriving both sides
from the local inbox. After the broker read it opens a fresh bounded subscription
to recheck the current relay epoch and current Room invitation before admitting
the Agent passage.

### Operational Impact Context

P082-021 and P083-014 implement a post-MVP extension of this same component. It
publishes the ordered `sensorium-operational-context.v1` value on an exact enacted
resource, binds it to the current source generation, propagates both through P082
results and P083 status/receipts, and lets a consuming host raise but never lower the
current source class. P082 defines stale solely as a generation mismatch or a
superseded effective publication; impact changes and corrections use audited
immutable replacement. Workbench-backed, collaborative-live, and remotely invokable
profiles are not special cases: the V1 resource envelope requires the value for every
publication. The earlier wire-optional rollout path was deliberately not used. Every
profile therefore fails closed when the value is absent, malformed, oversized beyond
the 512-byte UTF-8 summary cap, inconsistent, or stale.

Room remains an opaque carrier. Agent Core retains only bounded generic qualifier refs
and strict digests, while the daemon and P064 prompt-assembly boundary render a versioned,
non-droppable caution layer before feed-dependent inference. Host-owned request metadata
and the durable Inquirium trace pair each source class with its context digest and record
the local policy ref, floor, and selected class. The trace consumes that composition-root
projection directly, so local elevation remains auditable without entering Agent Core. The
extension creates no capability, access grant, or effect authority and does not reopen
the completed hard-MVP boundary.

The normalized publication slot is indexed by source kind/ref, projection profile,
and direction. Replacement is serialized with read and effect admission, closes old
subscriptions, requires a non-empty trimmed NUL-free reason capped at 512 UTF-8
bytes, emits bounded metadata-only correction facts, and makes stale generations
and superseded ids typed refusals. Workbench environment generation and authority
are exact; Story 012 exercises the collaborative replacement path. A Room
pump that encounters generation or context drift publishes a recipient-filtered,
transient `suspended` / `degraded` status before close without rewriting the durable
publication. Revoking the last observer clears the transport audience before close,
preventing bounded replay of the prior latest-state result.

Status: `done post-MVP`.

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
leak-minimal lookup. A future existence-discovery catalog of published interfaces
is a separate disclosure oracle and requires an explicit policy, query bounds,
anti-enumeration posture, revocation model, and contract revision.

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
| Workbench evicts terminal events before a subscriber catches up | Silent loss or a cursor that falsely claims continuity | Persist a bounded retained floor and emit an explicit gap before the next available event. |
| A remote host returns malformed or mismatched terminal evidence | Recipient renders corrupted bytes or accepts another subscription's data | Schema-gate the complete read result and each inline payload, pin resource/subscription/delivery/caps, and verify output count and digest before SSE projection. |
| A local subscription grant is reused to initiate peer egress | Observation authority silently widens into network authority | Require separate host-local `sensorium.interface.remote-feed` authority, then independently require an exact source-issued subscribe Passport. |
| A peer stalls or returns an oversized or malformed result | A feed blocks indefinitely, allocates beyond its contract, or retries a terminal integrity failure | Bound peer wait and carrier bytes, enforce requested result bytes before typed decode, and retry only transport-unavailable failures. |
| A remote feed ref or cursor is reused by another local caller | Local authority is confused with possession of presentation state | Bind every feed to the authenticated creating module and recheck ownership on read and close. |
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
5. Add a multiprocess two-deployed-node direct-peer terminal-feed run only as
   stronger deployment evidence; retain the implemented peer-runtime transport test
   as the component-level proof and do not fork the live-feed contract.

### P084-012b local review boundary

After P084-012a admission, the operator can supply an explicit redacted summary,
topic, optional polarity and draft intent through the local Harvester web review
API. `weak-signal-web-review.v1` binds this immutable decision to the original
finding digest; classification and snapshot provenance survive into an optional
unpublished local Whisper draft. This consumes already admitted local evidence
and grants no new P082 read, acquisition, remote delivery or publication authority.
The bounded v3 review store records facts and projections atomically and rebuilds
divergent review projections on reopen while validating retained facts. Explicit
FK enforcement preserves parent bindings; safe HTTP classes distinguish invalid
input, conflicting decisions, retained capacity and host failures. See P084 section "P084-012b: explicit web review and
local draft" and `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEWED-DRAFT-EVIDENCE.md` for the
contract, compatibility limits and measured acceptance. P084-012b is done for
this bounded local slice. Broader P084-012 remains
partial; the new slice does not close P078-007.


### P084-012c operator review projection

The node-ui review surface consumes already imported findings and sends explicit
operator decisions through the P084-012b API. Classification, provenance and the
finding digest remain visible; draft creation requires an affirmative choice.
Authentication and CSRF remain at the operator UI boundary and the daemon retains
review authority, immutable facts and the unpublished local draft. The UI grants
no fetch, P082 read or Whisper publication authority. Broader P084/P078 integration
remains partial. P084-012c is done for measured local operator UI acceptance; see
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEW-UI-EVIDENCE.md`.

### Synthetic delivery clarification (2026-10-16)

P096's delivery review decisions scope measured latency to the host path
(SDK drain to local receipt) and the 100 ms read-revoke bound to local grant
revocation. Global revocations retain the separate freshness/propagation budget
of the revocation view; stale views refuse. Content `host/digest` is unkeyed
SHA-256 consistency, without cryptographic host authentication. The normal
source adapter preserves existing `interface/overloaded` across Interaction
Broker for retryable concurrent-reader exhaustion (host capability HTTP 429),
without closing the publication or restarting acquisition. Native, remote and
SSE biosignal qualification remain separate. See the decisions in
[Proposal 096](../../40-proposals/096-sensorium-brainflow-connector.md#delivery-review-decisions-2026-10-16).


### Synthetic requalification checkpoint (2026-10-19)

The optional P096 local synthetic path passed a new pinned release (`45454121`,
source `ecbaf810`, image `532d20ed`) with a predeclared fifteen-second profile.
Identical baseline/loaded p95/p99/max gates (250/500/1000 ms) now accompany a
measured integer zero healthy-reader gap count. Measured triples were
138/167/197 ms and 120/157/164 ms; local read-grant revoke was 61 ms. Every preset
exceeded 100 block observations. Refused earlier runs remain unqualified and
preserved. This confirms only P096-010a's same-process synthetic host-API scope;
P096-005, physical/TCC, native overflow, remote/HTTP/SSE and release qualification
remain separate. Exact artifacts and review are in
`node:docs/evidence/sensorium-synthetic-local-20261019/`.


### Protected acquisition ownership checkpoint (2026-10-19)

The private acquisition owner records bounded pre-effect and terminal lifecycle
facts alongside its existing consent confirmations. It fences before storage,
verifies supervisor disposal before terminal audit I/O, and requires the current
intent revision to be durable at release authorization before exact claim release.
Late terminal withdrawal has separate audit status and cannot reopen collection or reuse consent. Neither a publication
nor a reader gains acquisition authority from those facts; the generic pending
operation seed keeps its existing role. Historical custody remains unchanged.

The final pinned `753911aa` software checkpoint passes 462 standard cases and
four explicitly selected owned-synthetic control cases. An explicit-unlock writer
guard prevents duplicated descriptors from retaining completed ownership; success
and error-return regressions preserve exclusion of an independent successor.
This is separate from the exact `578abe5d` P096-010a performance report.

This is a device-free implementation/conformance checkpoint on the separate
Sensorium branch. P096-005 remains partial under its existing six physical-native,
two controlled-native-fault and two exact-candidate host-software prerequisites.
No native/TCC adoption, recovery, headband test or broader carrier promotion follows.
See `node:daemon/docs/SENSORIUM-ACQUISITION-CONTROL.md` and the dated Node review.


### Native safety candidate preparation (2026-10-19)

Clean `af692fed` production source `4fc1405e` and release image `56fa8251` are
frozen on turbo.local. The create-only ad-hoc GUI capsule has distinct signed
image `e8989103` and handoff `8c00d7d4`; exact closure/signature checks and actual
rootless LaunchServices `launchd` preflight pass. All 51 frozen-client tests pass
on target Python 3.13.15, including closed optional audit diagnostics that never
supply cleanup or authority. Preparation preserves 238 prior protected files
(non-key hashes and metadata; signing-key files metadata only),
journal revision 81/twelve Cases, controller namespace and zero claims; only
eight files of one new capsule were added. Owner authority was expired at that
preparation checkpoint and Bluetooth permission remained unobserved. No manager,
permission probe, scan, acquisition, recovery, Case or grant renewal ran. P096-005 remains partial under the unchanged
six physical-native/two controlled-native-fault/two exact-candidate host-software
matrix; the older synthetic performance report retains its own exact candidate.
See `node:docs/evidence/sensorium-host-control-20261019/` and the dated candidate
preparation review.


### Delegated metadata authority checkpoint (2026-10-19)

The private acceptance owner supports explicit review-bound delegated SSH control
for metadata renewal, retaining default local-TTY behavior. Disabled same-owner
registered siblings require matching plans/declarations and remain unchanged;
occupied p21 renewal matches the complete retirement-history head while fresh
Case keeps its separate occupancy guard. The control declaration is no SSH
authentication or OS/TCC attestation. Current custody, exact source/image/boot,
worker absence, idle resources and partial-publication fencing remain mandatory.

Pinned admin `ba73dc1d`/source `b7553f0f`/image `171b658b` and its exact manager-free
process observer completed review `4cdd860b` on turbo.local. Same-scope controller/
discovery expiry is **2026-10-20 00:59:45 CEST**. Independent before/after checks
preserve twelve protected sources, journal 81/twelve Cases, expired registered
p21 revision 5, zero claims and no pending transition. Two pure and three normal-
owner/fault cases pass. Separately approved SIGTERM of twelve identity-checked
orphaned host helpers permitted a fresh ordinary absence check; it is no native
stop or recovery evidence. No manager, permission probe, scan, acquisition, Case,
recovery or native qualification ran. The older frozen GUI remains exact and TCC
unobserved. P096-005 and its native-origin matrix remain partial. See
`node:docs/evidence/sensorium-host-control-20261019/authority-renewal-runtime.json`
and the dated authority renewal review.


### Bounded private consent history and delegated control (2026-10-19)

Native enrollment reserves maximum confirmation and terminal audit room before
its transport claim and wearer-control publication, including never-WEAR. Typed
capacity/busy refusals precede acquisition effects; lock contention alone may
wait 250 ms within the original cleanup deadline after disposal. Durable closed
entries with verified released-claim eligibility may move to create-only 64-KiB
digest-linked segments (128 files maximum), with an atomic active-head pointer,
verified history and additive late withdrawal. Unknown/quarantined history stays
active; no old consent is reissued or silently pruned. Post-release eligibility
bookkeeping cannot downgrade confirmed cleanup or recreate its claim.

New persisted fields form a one-way strict-reader boundary. Preserve frozen
images as history and require actual format compatibility before use; existing
source `4fc1405e` knows base lifecycle but not the new fields. No target migration,
image replacement or hardware work is performed by this source checkpoint.

Delegated metadata renewal is limited to four hours per review; the default
nearby-terminal route retains its TTY and 24-hour bound. Explicit idle-root status
reports verified completed-review metadata with `authority/granted:false`, not
current permission or human presence. Public `operator/control` spelling is
separate from the retained private/historical bytes. Node checkpoints `c6a24619` and `55dc91eb` pass 475 standard/52 console checks,
three normal-owner/fault cases and one real-owned-synthetic disposal case. This
software conformance keeps P096-005 partial and the native origin matrix open.
See the dated Node review.
Acceptance source commits are kept reachable in both repositories under
`refs/acceptance/sensorium-p096-20261019/`; a later merge commit will preserve
master's current-source fixture and regenerate the combined ledger. The branches
remain separate in this checkpoint.


### Corrected nearby preparation (2026-10-19)

Node clean `3775bf56` freezes the reviewed source `cbb85050` as production release
`dfcf60f5` and a separate signed GUI `d153b457`/handoff `5205c163` on turbo.local.
Exact closure/signature checks, 52 frozen-client tests and rootless actual
`launchd` preflight pass. All 248 previous root files, controller namespace,
journal 81/twelve Cases and zero claims are preserved; only the new capsule's
eight files are added. No new consent fields or root migration, grant renewal,
manager, hardware or recovery runs. New ad-hoc TCC remains unobserved. Preparation
does not reuse earlier native evidence or close P096-005's origin matrix. Both
branches remain separate. See
`node:docs/audits/REVIEW-SENSORIUM-CORRECTED-CANDIDATE-2026-10-19.md` and
`node:docs/evidence/sensorium-host-control-20261019/corrected-candidate-preparation.json`.


### Merged-source preparation (2026-10-20)

Node clean merged `a176fdd2` freezes source `7a500816` as final signed deployment
`92f7ba9b` and GUI `0baa4846`/handoff `83f75e0d` on turbo.local. The oversized
compiler image was refused; explicit signing-container normalization preserves
the original and independently verifies payload equivalence within the unchanged
128-MiB deployment bound. All 52 frozen-client checks, signatures and rootless
actual GUI `launchd` preflight pass. All 256 previous root files, directory and
controller state, journal 81/twelve Cases and zero claims remain exact; eight new
capsule files are added. Expired authority and unobserved TCC are preserved.
No manager, hardware, root migration, renewal or further merge occurs. This
preparation leaves P096-005 and its native-origin matrix partial. Both temporary
branches continue separately after the earlier merge. See
`node:docs/audits/REVIEW-SENSORIUM-MERGED-CANDIDATE-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/merged-candidate-preparation.json`.


### Merged-source authority renewal (2026-10-20)

Exact delegated review `60ea3f0d` completed on turbo.local using merged commit
`a176fdd2`, source `7a500816` and deployment image `92f7ba9b`. The declared
`operator/control` is `delegated-ssh`; its 14400-second TTL was fixed at prepare,
with absolute controller/discovery expiry **2026-10-20 05:27:23 CEST**
(`1792466843000` Unix ms). The authority projection changes only the same-scope
discovery expiry fields and controller expiry/generation. Twelve protected sources, journal revision
81/twelve Cases and expired registered p21 revision 5 remain exact, with zero
claims and no pending transition.

Of 264 previous root files, two reviewed policies change content; the remaining
262 file observations preserve non-key content hashes and signing-key metadata.
`read-store.sqlite` changes only ctime through a `0600` permission refresh, with
unchanged content, inode, mode and mtime. Two create-only review/consumption files
are added. The explicit status projection records this completed review with
`authority/granted:false`; historical completion does not authorize a new action.
No Bluetooth manager, hardware, root migration, recovery, new consent, consent
reuse or merge ran. P096-005 stays **partial** under the unchanged six `physical-native`, two
`controlled-native-fault` and two exact-candidate `host-software` prerequisites.
See `node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-RENEWAL-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/authority-renewal-20261020-runtime.json`.

### Native qualification preflight and package identity (2026-10-20)

A freshly authorized SSH attempt with Muse 2 reaches only preflight. Exact GUI
`0baa4846`/source `7a500816` observes Bluetooth allowed and confirmed no-scan
cleanup; TCC attribution remains unverified. Released retirement `02af8be7`
completes 5-to-6 while preserving history, consent, sibling and journal 81/twelve
Cases. Revision 6 remains unregistered, claims remain zero, and the intended Case
refuses before SCAN or any stage approval.

Offline comparison proves that immutable acquisition worker `616fd76e` differs
from the compiled `1fa413b5`; this correctly blocks exact-asset admission without
identifying the original first failing guard. A distinct revision-1 package
`sensorium.acceptance.muse-2-p21.sdk-health` requires fresh normal Author/Sign,
preserving old identities. Sixteen closed preflight stages and bounded closed
stderr relay diagnostics preserve the guards. Four focused Rust tests and one
normal-key coexistence test pass; no corrected candidate is frozen yet. Neither
new consent/lifecycle format nor a completed native prerequisite follows.
P096-005 remains partial under its unchanged six/two/two origin matrix. A private
`PRIMARY_EVIDENCE_STORE` durability mirror is separate from public retention
policy. See
`node:docs/audits/REVIEW-SENSORIUM-NATIVE-PREFLIGHT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/native-preflight-20261020-runtime.json`.

### Corrected native package preparation (2026-10-20)

Node `88542281`/source `280b188c` freezes admin image `51deff86` and signed GUI
`2b19ea81`/handoff `eeec3bc9`. The exact seven-file closure, code signatures,
rootless actual `launchd` metadata and 58 frozen-client checks pass. Normal
Author/Sign produces the distinct sdk-health package `47dccc41`, review
`ba9db538` and sidecar `d37dfb8d`; independent OpenSSL verification passes and
refuses a modified payload, preserving legacy packages.

Signing preserves hashes and metadata for 274 previous non-key files except the
ordinary read-store ctime refresh; two signing-key files are checked by metadata
only, without reading their contents. Exactly thirteen files are added, while the
controller, zero claims and journal 81/twelve Cases stay unchanged. A separate
no-SCAN diagnostic reaches one SCAN prompt and sends only STOP, without stage approvals. Case
`67c78496` records released client withdrawal with no target; only journal content
changes to 84/thirteen Cases. Consent, control and grants are preserved and
revision 6 remains unregistered. No scan, acquisition, recovery or merge occurs.
New-GUI TCC is unobserved, independent of the older image's allowed observation;
fresh physical readiness remains required. P096-005 stays partial under its
unchanged six/two/two matrix, without a qualifier decision or adoption. Private
`PRIMARY_EVIDENCE_STORE` copies remain separate from public retention policy. See
`node:docs/audits/REVIEW-SENSORIUM-NATIVE-PREFLIGHT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/native-corrected-20261020-runtime.json`.

**Later fresh native observation (2026-10-20).** The same `88542281`/source
`280b188c`, GUI `2b19ea81` and package `47dccc41` complete one freshly approved
SCAN/BIND/REGISTER revision 6/WEAR p21 sequence. A separate new-GUI permission
probe observes allowed with confirmed state-only manager cleanup; TCC attribution
remains unverified. The source observation reports `observed-released`,
`run-completed`, cooperative native cleanup, executor exit, durable audit revision
2 and controller release. Host snapshots show journal 93/fourteen Cases, zero
claims and unchanged controller namespace. Revision 6 stays stopped and
registered with its fresh binding and original five-minute p21 grant. Persisted
lifecycle fields make the root incompatible with older strict readers. This
retains `qualification:false` and `adoption:false`, without closing a formal
six/two/two prerequisite case or freshly observing firmware. No additional
hardware trial, reset, retry or merge follows. See
`node:docs/evidence/sensorium-host-control-20261019/native-p21-r6-20261020-runtime.json`
and the existing native-preflight review.

### Device-free protected-control observations (2026-10-20)

P096's private acquisition owner records bounded monotonic facts and explicit
counters without authorizing work or blocking protected stop. Authenticated HTTP
ingress includes session-lock waiting; shared provider removal refuses unfinished
siblings. Missing exact-launch/native-call observations remain missing. This is
implementation/conformance evidence only, with no new qualification, adoption,
remote migration, hardware run or change to historical observations. P096-005
remains partial.

### Finite private campaign runner (2026-10-20)

The private Node runner prepares four operational episodes over the same owners:
baseline, authenticated wearer HTTP stop, Case deadline and actual provider loss.
It reuses only an exact still-current released registration and requires fresh
current admission, enrollment and consent per acquisition. A fixed campaign
budget, independent control lane and create-only partial reporting do not renew
authority, retry or recover. Seven missing scenario hooks remain explicit blocked
rows. The offline collector validates original v1 case records and groups entire
qualification tuples; registration reuse never merges changed launch-chain facts.
No new native qualification, target migration, hardware trial or branch integration
is claimed. P096-005 remains partial.


### Private campaign owner integrations (2026-10-20)

A subsequent device-free checkpoint connects the seven previously blocked
operational hooks. Six common episodes cover baseline, protected HTTP stop, Case
deadline, provider loss, private application operator-session logout and that
application's ordinary-control pool saturation. These last two scopes are not
Node UI/OS logout or whole-Node management saturation. Current admission, fresh
enrollment, WEAR, consent and permits remain required for every acquisition.

One terminal branch explicitly reduces only the current acquisition grant's
expiry, waits for actual monitor refusal and, after confirmed disposal, checks
ordinary enrollment against the same retained expired grant. It restores no
authority. The alternative branch injects a fixed signed nonreturning C call,
observes native-body entry, requests protected stop and retains uncertain claims;
a real conflicting enrollment probe and create-only restart checkpoint preserve
that uncertainty. The five-second fault-cleanup cap is an implementation bound,
not measured shutdown qualification or an SDK-deadlock observation. A separately
approved external restart can later be observed read-only against exact
source/image, OS/launch, changed boot and unchanged protected state. The observer
performs no reset, recovery, grant change or middleware start.

The two terminal branches cannot run consecutively by silently renewing a grant
or releasing quarantine. Derived observations share the exact parent episode;
missing evidence remains missing. The distinct immutable campaign package needs
normal Author/Sign, a new pinned build and a newly frozen signed client before
target use. This checkpoint performs no SSH, hardware trial, root migration or
merge and rewrites no historical evidence. P096-005 remains **partial** under the
unchanged qualifier, origin matrix and full-tuple rules; fresh process ancestry
can still split qualification groups despite exact registration reuse. See
[P096's owner checkpoint](../../40-proposals/096-sensorium-brainflow-connector.md#campaign-owner-integration-checkpoint-2026-10-20)
and `node:daemon/docs/SENSORIUM-P096-CAMPAIGN.md`.


### Private campaign target preparation (2026-10-20)

Merged workstream Node `64e92854` prepares source pin `2694f0aa`, admin image
`cce00f57` and ad-hoc GUI `e8ce6d5f`/handoff `6821f1d4` on the nearby host.
Normal Author/Sign publishes distinct campaign package `98dda828`, review
`6bd78dd6` and sidecar `ffea479f`, with thirteen exact package files and nine
frozen GUI closure files. A separately reviewed local-symbol removal preserves
all eighteen loaded sections, globals, imports and fixups within the existing
image cap; debug symbolization differs. This adds no native qualification.

The target passes 156 program checks after validation-kit input omissions are
corrected; the original failed attempt remains retained and product code is
unchanged. Inert C-library loading observes no native-body entry or SDK import.
Root preservation covers 299 old non-key hashes, two signing-key metadata records,
103 directory identities, both parents and the controller namespace. All metadata
is exact for 300 of 301 old files; only read-store SQLite ctime changes, consistent
with the normal mode-0600 permission refresh. The strict refusal and separate
closed exception review are preserved. Exactly 26 files/eight directories are
added; journal 93/fourteen Cases, zero claims, expired ownership and stopped
registered p21 revision 6 remain unchanged.

No Case, permission probe, Bluetooth manager, renewal, root migration, recovery or
hardware trial runs. This preparation does not claim final primary-branch
integration. Fresh authority handling and any revision-6 retirement remain
separate; new-image TCC and physical evidence are unobserved. P096-005 remains
**partial** under the unchanged qualifier and origin matrix. See
[P096's preparation checkpoint](../../40-proposals/096-sensorium-brainflow-connector.md#campaign-target-preparation-checkpoint-2026-10-20),
`node:docs/audits/REVIEW-SENSORIUM-CAMPAIGN-PREPARATION-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/campaign-preparation-20261020-runtime.json`.


### Revision-6 controller/discovery renewal (2026-10-20)

The paired temporary branches fast-forward to Node `82f9c535` / Orbidocs
`7044cbe2`, leaving the primary branches unchanged. Metadata administration uses
the retained signed candidate `64e92854` / source `2694f0aa` / image `cce00f57`;
no newly synchronized source or startup qualification is assigned to that image.

Separately reviewed delegated SSH renewal `5e89ee68` fixes a 14400-second lifetime
at prepare, expiring **2026-10-21 00:19:27 CEST** (`1792534767000` Unix ms).
Only controller-policy expiry/generation and the existing stopped discovery
revision 3's exact host/caller grant expiries change. Twelve protected digests,
journal 93/fourteen Cases and zero claims remain exact. Immutable SDK-health and
campaign packages, stopped p21 revision 6, its expired grant, binding, consent and
history remain preserved.

No manager, permission probe, SCAN, measurement, recovery, root migration or new
wearer consent occurs. P096-005 remains **partial**. Retirement **6 → 7 remains
next and separately reviewed**, not completed by renewal. See
[P096's renewal checkpoint](../../40-proposals/096-sensorium-brainflow-connector.md#revision-6-authority-renewal-checkpoint-2026-10-20),
`node:docs/audits/REVIEW-SENSORIUM-R6-AUTHORITY-RETIREMENT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/authority-r6-20261020-runtime.json`.


### Released revision-6 retirement (2026-10-20)

Separate review `fe930943` on retained administrator `64e92854` / source
`2694f0aa` completes metadata retirement **6 → 7**, using Case `487b1e94` and
its exact `confirmed-case-release` basis. Four reviewed metadata sources remove
only the expired revision-6 host grant/plan, acquisition grant, discovered
binding and active candidate receipt. Revision 7 is reserved by completed
history; it is neither registered nor granted authority.

Journal 93/fourteen Cases, consent and logical resource state remain unchanged, the controller
is free, and both immutable SDK-health and campaign packages remain exact. The
campaign package stays unregistered. Controller/discovery authority keeps its
**2026-10-21 00:19:27 CEST** expiry (`1792534767000` Unix ms). The local comparison
accounts for serde's omitted empty `discovery/receipts`; no product fix is claimed.

No recovery, hardware, manager, permission probe, new consent or registration
occurs. Fresh SCAN/BIND/REGISTER revision 7/WEAR p21 remain separate future
steps. The synchronized workspace is not a rebuild of the retained target, and
no primary integration or native qualification follows. P096-005 remains
**partial**. See
[P096's completed retirement](../../40-proposals/096-sensorium-brainflow-connector.md#released-revision-6-retirement-checkpoint-2026-10-20),
`node:docs/evidence/sensorium-host-control-20261019/retirement-r6-r7-20261020-runtime.json`
and `node:docs/audits/REVIEW-SENSORIUM-R6-AUTHORITY-RETIREMENT-2026-10-20.md`.


### Revision-7 campaign interruption (2026-10-20)

The separately authorized SSH campaign uses exact signed GUI `e8ce6d5f`, source
`2694f0aa` and verified nine-file handoff `6821f1d4`. The actual GUI launchd
preflight and same-image Bluetooth permission-only observation pass; cleanup and
observer exit are confirmed, while responsible-process attribution remains
unverified. Controller/discovery authority is current until
**2026-10-21 00:19:27 CEST** (`1792534767000` Unix ms), and revision 7 begins as
reserved, with a free controller and zero resource claims.

Only CAMPAIGN and SCAN are approved. Baseline Case `7aef6c89` stops during scan
with `incomplete-released`, `case-authority-fenced` and `client-withdrawal`.
The backend reports cancelled with confirmed no-scan cleanup and worker exit;
controller release is confirmed and acquisition is absent. The endpoint records
no STOP decision and `withdrawn: false`. Internal client transport/nonce/timeout
paths can send the same withdrawal frame, so its actual origin remains
unresolved. Deliberate wearer withdrawal, absent hardware, denied Bluetooth or
expired grants are not inferred.

The automatic report is partial with `campaign-episode-not-released`; its
baseline-completion condition does not negate confirmed actual release. Later
selected rows are blocked and the alternative fault branch remains unselected.
Fresh reads show journal 98/fifteen Cases, released Case state, zero claims, no
pending fence and only discovery revision 3 in inventory. Revision 7 remains
reserved/unregistered; no BIND, REGISTER, WEAR, new p21 grant or consent occurs.
No automatic retry, reset, recovery, renewal or integration follows. Diagnose
the first closed client-control termination reason before a fresh approved
attempt; P096-005 remains **partial** without formal prerequisite closure. See
[P096's campaign interruption](../../40-proposals/096-sensorium-brainflow-connector.md#revision-7-campaign-interruption-checkpoint-2026-10-20),
`node:docs/evidence/sensorium-host-control-20261019/campaign-r7-20261020-runtime.json`
and `node:docs/audits/REVIEW-SENSORIUM-CAMPAIGN-R7-2026-10-20.md`.


### Client-control diagnosis and software repair (2026-10-20)

Device-free reproduction of the frozen client exposes two defects: blocked
ordinary SSH output can stall its shared heartbeat relay, and internal remote
EOF/challenge/echo failures can send the explicit `S` withdrawal frame. A
blocked real-pipe output control times out near 605 ms while endpoint input
remains open. This proves a reachable software failure path, not the unique
cause of revision-7 Case `7aef6c89`. Its signed image, report and unresolved
historical attribution remain preserved.

The source repair sends `S` only for explicit STOP/Ctrl-C and closes the socket
for internal loss, preserving the host monitor's `ControlLost` classification.
The first closed client reason and monotonic timestamp use a lock independent
of socket writes. A bounded ordinary-output queue and nonblocking pipe/TTY
writes keep heartbeat echoes independent, with bounded drain/final publication
and a first closed relay reason. Review identifies another fairness gap: many
individually bounded decision writes can monopolize one turn and delay EOF.
Queued decisions are bounded, and each turn prioritizes input EOF/STOP before
another decision write. Existing echo/socket/host-control/campaign
bounds remain 600 ms/250 ms/one second/900 seconds. The closed confirmation-error
allowlist also covers LOGOUT/SATURATE/REVOKE/FAULT; that correction is not a cause
claim for the earlier SCAN.

Create-only `client-control-<scenario>.json` is a strict client diagnostic in the
protected campaign namespace, separate from host observations. It confers no
authority, native cleanup attestation, claim-release proof or prerequisite
closure. This device-free checkpoint performs no SSH action, target build or
signing, root migration, native attempt or integration. Another physical attempt
requires a new exact pinned build and signed client plus fresh operator
approval. P096-005 remains **partial**. See
[P096's client-control diagnosis](../../40-proposals/096-sensorium-brainflow-connector.md#client-control-diagnosis-and-software-repair-checkpoint-2026-10-20),
`node:docs/evidence/sensorium-host-control-20261019/client-control-diagnosis-20261020.json`
and `node:docs/audits/REVIEW-SENSORIUM-CLIENT-CONTROL-2026-10-20.md`.


### Client-release follow-up source checkpoint (2026-10-20)

The source follow-up moves potentially blocking output into a disposable owned
copier, with a lifetime EOF watcher and cancellable teardown. It preserves the
caller's stdout/stderr OFD flags. Nonce echoes have priority over ordinary
decisions; a shared lock covers only an immediate write attempt and its wait
consumes the existing 250-ms write budget. The 600-ms remote echo window stays
unchanged and supplies no guarantee about SSH network delay. Finite queues,
EOF/STOP priority, first closed diagnostics and the existing reason-set equality
regression remain separate from authority or native cleanup proof.

Ordinary acquisition now refuses the fault-capable package before enrollment
effects. Only the closed campaign factory opts into that package family, for
both fresh and reused targets; request fields cannot select it. Inert structural
verification/registration still grants no execution authority, and fault arming
retains its separate session, phase, permit and current-authority checks. Existing
campaign expectations already distinguish provider loss (`ControlLost`) from
explicit protected stop (`ClientWithdrawal`). Historical reports and the unknown
revision-7 SCAN origin remain unchanged.

This source checkpoint claims no target preparation, measured runtime pass,
permission observation, hardware, migration or integration. P096-005 stays
**partial**; a future physical attempt requires a fresh interactive readiness
question and an explicit operator answer. See
[P096's source follow-up](../../40-proposals/096-sensorium-brainflow-connector.md#client-release-follow-up-source-checkpoint-2026-10-20),
`node:docs/audits/REVIEW-SENSORIUM-CLIENT-RELEASE-FOLLOWUPS-2026-10-20.md`
and
`node:docs/evidence/sensorium-host-control-20261019/client-release-followups-20261020.json`.
