# Proposal 075: Matrix Homeserver Runtime Profile

Based on:

- `doc/project/20-memos/swarm-question-channel-transports.md`
- `doc/project/30-stories/story-011-corpus-fish.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/036-room/036-room.md`
- `node/tools/matrix-fixture/README.md`

## Status

Draft

## Date

2026-07-01

## Executive Summary

Orbiplex uses Matrix in several places, but those uses currently inherit their
operational rules from separate documents:

- Agora uses Matrix as a topic-addressed relay carrier for `agora-record.v1`.
- Artifact Delivery can use Matrix as a mailbox-style store-and-forward carrier.
- Room has an implemented Matrix bridge adapter, but its production liveness baseline
  is the relocatable WSS relay defined by P070.
- Story 011 preserves a Matrix room id as collaboration intent, while the real
  homeserver-backed live transport remains a post-MVP extension.
- The multi-node harness needs an optional Matrix fixture profile for reproducible
  smoke tests.

This proposal defines a shared **Matrix homeserver runtime profile**. It does not
ask Orbiplex to implement a Matrix homeserver. Instead, it defines the minimum
behavior, configuration surface, retention stance, security boundaries, and test
fixture expectations that an external Matrix homeserver must satisfy when used as an
Orbiplex carrier.

The central rule is:

> Matrix is a carrier and provenance signal. Orbiplex envelopes, signatures,
> passports, room membership projections, and local admission policy remain the
> source of authority.

This keeps Matrix useful without letting a transport runtime become a hidden
governance layer.

## Context and Problem Statement

Matrix appears in Orbiplex as a practical substrate for rooms, federation-agnostic
record delivery, and store-and-forward delivery. That is valuable because Matrix
already provides mature rooms, users, long polling, event delivery, and its own
homeserver-to-homeserver federation story. It is also risky because Matrix is not
ephemeral by default, carries its own identity model, its own federation protocol
is a different mechanism from Orbiplex's own federation identity (Proposal 076),
and any of this can be misread as the source of membership or message validity.

The current documentation already contains the correct local decisions, but they are
spread across multiple components:

- P035 and Solution 008 define the Matrix relay path for Agora.
- P070 and Solution 036 define the live Room transport contract.
- Solution 023 and the node implementation define Matrix mailbox behavior for
  Artifact Delivery.
- Story 011 documents that the hard-MVP Corpus acceptance pack carries a Matrix room
  id but does not start a real homeserver.
- P074 names a local Matrix fixture as an optional multi-node harness dependency.

Without a shared profile, each adapter can accidentally restate a slightly different
Matrix posture: different retention expectations, different room naming, different
payload ceilings, different error classes, or different assumptions about Matrix
membership authority.

This proposal creates one common operational contract for those consumers.

## Goals

- Define Matrix as an Orbiplex carrier profile, not as an Orbiplex authority.
- Provide one reusable profile for Room, Agora, Artifact Delivery, Corpus
  collaboration, and multi-node test harnesses.
- Make homeserver configuration explicit enough for reproducible local and CI
  fixtures.
- Preserve transport independence: WSS, Matrix, direct HTTP, and future carriers
  must not change the meaning of Orbiplex records.
- Make Matrix retention and cleanup obligations visible at the profile boundary.
- Give implementers a shared checklist before adding a new Matrix-backed adapter.

## Non-Goals

- Not an implementation of a Matrix homeserver.
- Not a replacement for Matrix Client-Server API documentation.
- Not a federation governance layer.
- Not Orbiplex's own federation identity. Matrix's homeserver-to-homeserver
  federation protocol is a separate mechanism with its own trust model.
  Proposal 076 defines Orbiplex's federation identity (`federation_id`, root
  trust, `data-dir` isolation); this proposal does not ask Orbiplex to adopt or
  depend on Matrix's federation protocol as that mechanism, and using it is
  explicitly not a goal here.
- Not a membership authority for Room.
- Not an identity authority for participants, nyms, nodes, or organizations.
- Not a requirement that every Orbiplex node run a Matrix homeserver.
- Not a hard-MVP requirement for Story 011's local Corpus acceptance pack.
- Not a second Room ordering or history model. Matrix DAG merge, room state, history,
  presence, and homeserver membership are never imported into Room Core.

## Proposed Model

### 1. Matrix Carrier Profile

A Matrix carrier profile is a deployment-local runtime binding:

```text
Orbiplex component -> Matrix adapter -> configured Matrix homeserver
```

The profile supplies:

- homeserver endpoint and server name;
- credential source;
- room alias/event namespace policy;
- payload limits;
- timeout/retry/backoff policy;
- retention and redaction behavior;
- diagnostics and health reporting;
- fixture/provisioning rules for tests.

It does not supply:

- Orbiplex signer authority;
- Room membership authority;
- capability-passport validity;
- record validity;
- settlement or procurement semantics;
- final routing policy.

### 2. Authority Boundary

Every Matrix-backed adapter MUST re-validate the embedded Orbiplex contract after
receiving a Matrix event.

For Agora:

- the embedded `agora-record.v1` envelope is verified locally;
- Matrix event signatures and sender identity are diagnostics/provenance only;
- local topic ACL, capability, revocation, delegation, schema, and idempotency gates
  decide admission.

For Room:

- durable `room.v1`, `room-membership.v1`, `room-event.v1`, and membership
  attestations decide who may join or send;
- Matrix room membership is only a transport-side consequence of an already
  authorized Room decision;
- the Matrix adapter must not invent membership from Matrix state alone.

For Artifact Delivery:

- sealed Artifact Delivery / INAC envelopes remain the authority-bearing payload;
- Matrix room/event metadata is a delivery carrier trace, not proof of sender or
  recipient authority.

### 2A. Room Uses Matrix Only as a Bridge Profile

P070 defines the Room production baseline as one relocatable WSS relay endpoint per
active relay epoch. Matrix is optional infrastructure for deployments that already
operate it or need a bridge into Matrix clients. The existing Matrix Room adapter may
translate between Room live frames and Matrix events, but it does not become a second
kind of Room.

Consequently:

- Room relay epoch and sender/domain sequences remain authoritative for their stated
  scopes; Matrix event order is carrier provenance only;
- Room failover starts a new relay epoch and never merges Matrix DAG branches into a
  Room history;
- Matrix state events do not open, close, grant, revoke, or elect Room authority;
- Room remains usable without a homeserver, and a Matrix outage does not invalidate
  durable Room facts;
- behavior-equivalence tests cover admission, bounds, revocation, and cleanup at the
  adapter boundary; they do not assert semantic equivalence between Matrix history and
  the non-retentive WSS relay buffer.

### 3. Minimal Client-Server API Surface

The MVP-compatible Matrix profile requires a homeserver that supports these
Client-Server API operations:

```text
POST /_matrix/client/v3/join/{roomIdOrAlias}
PUT  /_matrix/client/v3/rooms/{roomId}/send/{eventType}/{txnId}
GET  /_matrix/client/v3/sync
POST /_matrix/client/v3/user/{userId}/filter
PUT  /_matrix/client/v3/rooms/{roomId}/redact/{eventId}/{txnId}
```

Fixture/provisioning tooling MAY additionally require:

```text
POST /_matrix/client/v3/register
POST /_matrix/client/v3/login
POST /_matrix/client/v3/createRoom
GET  /_matrix/client/v3/directory/room/{roomAlias}
GET  /_matrix/client/versions
```

Adapters should keep the Matrix client layer thin. Matrix endpoint mechanics belong
in the Matrix client adapter; Orbiplex semantics belong in the consuming component.

### 4. Deployment Profiles

#### Local Fixture

Purpose:

- reproducible developer and CI smoke tests;
- no production federation assumptions;
- deterministic users, rooms, tokens, and cleanup.

Current reference:

- `node/tools/matrix-fixture` using Conduit;
- federation disabled;
- local server name;
- SQLite-backed ephemeral or resettable state;
- idempotent bootstrap script.

#### Single Homeserver Deployment

Purpose:

- one externally managed homeserver used by one or more Orbiplex adapters;
- suitable for early operator deployments and post-MVP live collaboration tests.

Required configuration:

- `homeserver_url`;
- `server_name`;
- access token or token-file reference;
- room alias prefix;
- event type namespace;
- retention and redaction policy;
- payload and sync limits.

#### Matrix as an Inter-Federation Carrier

Purpose:

- later use of Matrix as an optional carrier for moving federation-relevant
  Orbiplex data (Proposal 076) between two independently-operated Orbiplex
  federations, or between an Orbiplex federation and the wider public network.

This is deliberately not "running Matrix's own federation." Matrix's
homeserver-to-homeserver federation protocol is one possible way bytes move
between two Orbiplex federations; it is never what makes two Orbiplex
federations cooperate. That remains a property of signed Orbiplex records,
capability grants, and explicit promotion (see Proposal 076, *Relationship to
Existing Proposals* / Memarium), regardless of which carrier moved the bytes.

Deferred:

- multi-homeserver fallback;
- load balancing;
- cross-homeserver reliability policy;
- homeserver trust scoring;
- automatic room migration.

### 5. Retention Profile

Matrix MUST be treated as potentially durable unless configured otherwise. Any
Orbiplex use that expects ephemeral live content must explicitly select a
non-retentive profile:

- no public history for private/live rooms;
- bounded event retention where supported;
- redaction on room close/expiry;
- idempotent cleanup;
- diagnostics when redaction is delayed, partial, or unsupported;
- no durable embedding of live message content into `room.v1` or other durable
  Orbiplex records.

This does not claim that Matrix can guarantee erasure from every remote server or
member device. It defines the adapter's obligation: configure for non-retention where
possible, attempt cleanup deterministically, and report degradation when cleanup is
not complete.

### 6. Room Naming and Event Naming

Room aliases and event types MUST be derived from explicit adapter policy, not from
ad-hoc string rewriting.

Recommended defaults:

```text
room alias prefix:  orbiplex
event namespace:    ai.orbiplex.<component>.<event-kind>
txn id:             canonical Orbiplex id or digest when available
```

For Room live transport, non-secret carrier aliases and bindings should be derived
from a canonical digest of `room/id`, not from a lossy path-safe rewrite. Session refs
are different: P070 requires host-minted 256-bit CSPRNG bearer secrets that never enter
Matrix events, aliases, state, or member-visible projections.

### 7. Payload and Sync Bounds

Every Matrix adapter operation MUST have explicit local bounds:

- request timeout;
- sync long-poll timeout;
- maximum event payload bytes;
- maximum pre-parse frame bytes;
- maximum rooms or subscriptions per adapter instance;
- retry count and backoff with jitter;
- failure class (`retryable`, `terminal`, `degraded`);
- diagnostics emitted on timeout, parse failure, redaction failure, or admission
  refusal.

Unbounded Matrix adapter calls are invalid in Orbiplex runtime.

### 8. Configuration Shape

Component-specific names may differ, but the profile vocabulary should remain
consistent:

```json
{
  "matrix": {
    "enabled": true,
    "homeserver_url": "https://matrix.example.org",
    "server_name": "matrix.example.org",
    "access_token_file": "secrets/matrix-access-token",
    "room_alias_prefix": "orbiplex",
    "event_type_prefix": "ai.orbiplex",
    "max_event_payload_bytes": 1048576,
    "sync_timeout_ms": 30000,
    "request_timeout_ms": 10000,
    "retention": {
      "mode": "transient",
      "redact_on_close": true,
      "max_retention_seconds": 86400
    }
  }
}
```

Plain `access_token` MAY be accepted for local development, but production-like
profiles SHOULD prefer token files or host-owned secret storage.

## Implementation Specifics

This section is intentionally a seed. It should be expanded as node-side
implementation converges.

### Node Reference Areas

Current implementation-relevant areas:

- `node/agora-matrix-client` — thin Matrix Client-Server wrapper and event sink.
- `node/agora-matrix-client/src/sink.rs` — the `MatrixEventSink` trait: the
  already-shared, dyn-compatible carrier primitive (`ensure_room`, `send_event`,
  `live_events`, `redact_events`) reused by both the Agora relay and the Room live
  transport below. This is the closest thing today to the "one reusable profile"
  this proposal asks for, at the transport-primitive layer; the config/error
  vocabulary layered on top of it is what still needs unifying (see *Reuse: Shared
  Matrix Carrier Primitive*).
- `node/agora-matrix-client/src/room_live.rs` — `MatrixRoomLiveTransport`, an
  existing, tested implementation of `orbiplex_node_room_core::RoomLiveTransport`
  for P070/Solution 036. It wraps `InMemoryRoomLiveTransport` for all
  authorization/sequence/lifecycle decisions and uses Matrix only to publish
  frames and redact on close — the Authority Boundary rule in section 2 already
  holds in code for Room, not just in this document.
- `node/agora-matrix` — pure Matrix event-content bridge.
- `node/agora-relay-matrix` — Matrix-backed Agora relay composition.
- `node/middleware-modules/agora-service` — supervised Agora middleware service.
- `node/ad-host/src/matrix_mailbox.rs` — Artifact Delivery Matrix mailbox worker.
- `node/tools/matrix-fixture` — local Conduit fixture for integration tests.

### Adapter Contract

Each Matrix-backed adapter should expose, at minimum:

- `health()` with homeserver reachability, room readiness, sync state, and last error;
- `join_or_create()` or provisioning equivalent where the adapter owns room setup;
- `send()` with deterministic transaction id when the payload has a canonical id;
- `sync()` or worker-owned inbound loop with bounded parsing and admission handoff;
- `redact_or_cleanup()` for live/transient profiles;
- structured counters for sent, received, accepted, rejected, redacted, cleanup-failed,
  and parse-failed events.

### Error Classes

Adapters should normalize Matrix failures into Orbiplex-facing categories:

- `matrix/transport-unavailable`;
- `matrix/auth-rejected`;
- `matrix/room-unavailable`;
- `matrix/payload-too-large`;
- `matrix/sync-failed`;
- `matrix/redaction-failed`;
- `matrix/event-parse-failed`;
- `matrix/admission-rejected`.

These are adapter diagnostics. They do not replace protocol-level errors such as
invalid signature, invalid contract, expired advertisement, or capability missing.

### Reuse: Shared Matrix Carrier Primitive

Goal 2 ("one reusable profile") is already half-built, and implementers should
extend it rather than start a parallel abstraction:

- `MatrixEventSink` (`agora-matrix-client/src/sink.rs`) is the shared, dyn-safe
  carrier primitive. `http_sink.rs` and `fake_sink.rs` are its two
  implementations; `agora-relay-matrix` and `room_live.rs` are its two current
  consumers. A future Room-Matrix production wiring or an AD sink-backed carrier
  should implement or reuse this trait, not a new bespoke client.
- What is *not* yet shared is the profile layer above the sink: three separate
  config shapes exist today (`MatrixMailboxConfig` in `ad-host`, whatever
  `agora-relay-matrix` uses, and the minimal `MatrixRoomLiveConfig { relay_domain
  }` in `room_live.rs`, which has no retention/payload/timeout fields at all —
  `room_live.rs` hardcodes its payload ceiling as a `const` and has no
  configurable retention or backoff). Promote the section 8 configuration shape,
  the Error Classes enum, and a canonical txn-id/topic-alias derivation helper
  into one small module consumed by all three adapters, per DEV-GUIDELINES
  Layering 5 (`*-core` tier: pure types, no transport). This turns "each adapter
  can accidentally restate a slightly different Matrix posture" (Context and
  Problem Statement) from a documentation risk into a compile-time impossibility.
- Retry/backoff/reconnect obligations (section 7) should ride the Replay
  Scheduler (Solution 020) rather than each adapter growing its own timing loop,
  per DEV-GUIDELINES Host-Owned Runtime Primitives 2.

### Test Fixture Contract

The local fixture should provide:

- deterministic homeserver URL and server name;
- deterministic bot user;
- deterministic test room alias;
- idempotent bootstrap;
- access token export for tests;
- reset command that wipes state;
- CI-friendly startup and readiness check;
- no reliance on public Matrix federation.

The existing Conduit fixture satisfies the first slice for Agora smoke tests. Future
work should decide whether Room live transport and Artifact Delivery mailbox tests
reuse the same fixture directly or add profile-specific bootstrap helpers.

## Security and Privacy Considerations

- Matrix access tokens are secrets and must not appear in health snapshots, traces,
  generated docs, or public fixtures.
- Matrix sender ids must not be treated as Orbiplex participant, nym, node, or org
  identities.
- Pseudonymous or nym-authored Orbiplex payloads must not leak a public
  `participant:did:key` through Matrix metadata.
- Room live messages must not be copied into durable records unless a separate,
  explicit member-local capture policy applies.
- Redaction failures must be visible as degraded cleanup, not hidden behind a
  successful room close.

## Failure Modes and Mitigations

| Failure | Risk | Mitigation |
|---|---|---|
| Homeserver unavailable | Adapter stalls or drops delivery | Bounded timeout, retry/backoff, degraded health, local-first persistence where applicable |
| Access token rejected | Silent non-delivery | Fail closed, surface `matrix/auth-rejected`, do not expose token |
| Matrix room membership diverges from Orbiplex membership | Unauthorized live access | Room projection is authority for `join`/`send`: `join` is gated by membership attestation and `send` is validated against the joined session. `subscribe(room_id)` itself carries no session/subject parameter (`RoomLiveTransport::subscribe`, `room-core/src/lib.rs:1568`, and the reference `InMemoryRoomLiveTransport` impl both take only a room id) — issuing a live event stream to a caller is a host-layer responsibility: the daemon composition layer MUST call `subscribe` only after it has independently validated that caller's session/membership, and must not expose it as a directly callable operation. `drop_member` updates only local Room-core state; `MatrixEventSink` has no kick/ban operation yet, so a revoked-but-still-Matrix-joined member is not evicted from the underlying Matrix room and could keep receiving *future* live frames sent after revocation. See P075-011. |
| Homeserver retains live content | Privacy violation | Transient retention profile, redaction on close/expiry, cleanup diagnostics |
| Duplicate send after retry | Duplicate federation events | Deterministic Matrix `txnId` from Orbiplex id/digest |
| Oversized payload | Memory pressure or homeserver refusal | Pre-parse and pre-send byte ceilings |
| Matrix event accepted but Orbiplex envelope invalid | Transport becomes authority | Always re-validate embedded Orbiplex contract before local admission |
| Fixture drift | CI becomes non-reproducible | Pin fixture image/version and keep bootstrap idempotent |

## Relationship to Existing Proposals

- P035 defines Agora relay semantics. This proposal only extracts the reusable Matrix
  carrier profile from that implementation.
- P070 and Solution 036 define Room semantics, the `RoomLiveTransport` adapter
  interface, and the requirement that WebSocket and Matrix adapters stay
  behaviorally equivalent under conformance tests. This proposal supplies the
  Matrix-specific runtime profile for that interface; `room_live.rs` is the
  current implementation.
- P074 defines a broader multi-node harness. This proposal supplies the Matrix fixture
  profile that P074 can invoke.
- Story 011 remains hard-MVP through the local Corpus path. A homeserver-backed live
  collaboration fixture can be layered later using this profile without changing
  Corpus procurement semantics.

## Relationship to Agent, Inquirium, and Corpus

Matrix is a carrier several layers below these three organs. None of them should
ever see a raw Matrix event; each boundary below exists to keep that true as the
profile gets used in practice.

### Agent (Proposal 073)

An Agent that participates in a Room (for example as the Corpus chair, see
below) may end up communicating over a Matrix-backed live transport without
knowing it — that is the point of carrier independence. Two concrete
consequences follow:

- **The Agent's own budget/termination authority must not be overridden by
  Matrix transport bounds.** `AgentBudget.max_wall_time_ms` and the controller's
  `termination_condition` are the authority for how long a step may wait; Matrix
  `sync_timeout_ms` and adapter retry/backoff (section 7) are transport-layer
  bounds *beneath* that authority, not a substitute for it. A step blocked on a
  slow or degraded homeserver must still terminate on the Agent's own budget, not
  hang until Matrix gives up. Concretely: the Matrix adapter's timeout/backoff
  must always be strictly shorter than the calling Agent step's remaining
  budget, never the reverse.
- **`participant/ref` for a Room-joined Agent stays host-minted, never a Matrix
  user id.** Per Proposal 073's `agent.binding.v1` invariant, the Agent's
  accountable identity is issued by the host and asserted into Room via
  `room-membership-attestation.v1`; a Matrix `@user:server` id is carrier
  metadata only (section 2's Authority Boundary already says this for humans —
  it applies identically to an Agent-controlled participant, per DEV-GUIDELINES
  Agent and Automation Boundaries 4, no self-authorizing agents: an Agent must
  not acquire Room standing merely by being present in the underlying Matrix
  room).

### Inquirium (Proposals 063/064)

Inquirium must never consume a Matrix event directly. A Room message that
arrived over Matrix is, at the point Inquirium could see it, exactly the kind of
untrusted remote content the Communication Dialect boundary in P064 exists for:
`content` is data, never auto-interpreted as instructions. The required path is:

```text
Matrix event -> MatrixEventSink -> RoomLiveTransport (authority-gated)
  -> Room live message fact -> inquirium.context-assembly.request.v1
     (context-source grant, classification-checked)
  -> Inquirium prompt assembly (as a preamble/context block, never as an
     instruction layer)
```

Skipping the context-assembly/grant step to "just forward the Matrix payload
into the prompt" would reintroduce exactly the prompt-injection surface P064's
Output Schema/Dialect sections were designed to close, except sourced from a
federation-adjacent carrier instead of a local file. This proposal should not
define new Inquirium behavior; it only needs to hold this boundary so nobody
wires Matrix directly to a runtime candidate.

### Corpus (Proposal 069)

Two touch points, both carrier-agnostic by construction if this profile's
Authority Boundary (section 2) is respected:

- **Live deliberation** (post-MVP): Corpus's chair Agent joins a Room whose live
  plane may be Matrix-backed. Corpus reasoning/chairing/settlement semantics are
  unaffected by the carrier choice — that is the entire point of Room's
  carrier-agnostic design — but the chair Agent inherits both boundary rules
  above (its own budget authority over Matrix timeouts; host-minted
  `participant/ref` over any Matrix user id).
- **Answer classification propagation**: `corpus-reasoning-answer.v1` carries the
  small `classification.v1` lattice tier, expanded to a full `classification.v1`
  object at the AD answer-envelope boundary (Proposal 069, Resolved Decision 21).
  This expansion happens at the AD envelope boundary regardless of whether that
  envelope transits over WSS, direct HTTP, or a Matrix mailbox (section on
  Artifact Delivery in section 2). This profile must not introduce a
  Matrix-specific classification shortcut; if Matrix ever carries a
  `corpus-reasoning-answer.v1`, the same tier-to-object expansion and AD
  re-validation apply, unchanged.

## DEV-GUIDELINES Alignment

- **Layering (5) / Avoid Entanglement (4).** This proposal's central rule ("Matrix
  is a carrier and provenance signal... Orbiplex envelopes, signatures, passports,
  room membership projections, and local admission policy remain the source of
  authority") is a direct instance of "do not entangle protocol semantics with
  transport or runtime details; wire-visible meaning should survive changes in
  networking stack." The `*-core`/`*-service`/`*-http` split recommended in *Reuse:
  Shared Matrix Carrier Primitive* is how that rule stays true as more consumers
  are added, instead of becoming aspirational prose three adapters later.
- **Protocols and Interoperability (1).** "Treat the protocol as a semantic
  contract independent of operating system, CPU architecture, accelerator,
  vendor, or runtime" extends naturally to *carrier*: WSS, Matrix, and any future
  transport must be interchangeable without changing record or room semantics.
- **Host-Owned Runtime Primitives (2).** Reconnect/retry/backoff belongs to the
  Replay Scheduler (Solution 020), not a private per-adapter timing loop.
- **Security and Privacy (1).** "Privacy is a default, not a plugin" makes the
  profile's `retention.mode: "transient"` the *required* default, not merely the
  example value in section 8 — a component that wants durable Matrix history must
  opt in explicitly and justify it, not inherit durability by omission.
- **Agent and Automation Boundaries (4).** "No self-authorizing agents... may not
  ... silently widen its own operating scope" is the normative basis for the
  Agent boundary rules above: presence in a Matrix room must never itself confer
  Room standing or authority.
- **Code Reviewing Guidelines — Essence** ("authorization and revocation checks
  sometimes happen after state changes, or are skipped when host context is
  missing"). This is precisely the shape of the `drop_member` gap found while
  writing this profile (see Failure Modes and P075-011): the local authority
  check is revoked correctly, but the underlying carrier membership is not
  reconciled, leaving a window where revocation is locally true but not
  carrier-true.

## Implementation Tracker

| ID | Item | Status | Notes |
|---|---|---|---|
| P075-001 | Document shared Matrix homeserver runtime profile | proposed | This proposal is the seed artifact. |
| P075-002 | Reconcile `agora-matrix-client` config naming with profile vocabulary | partial | Agora already has `matrix_homeserver_url` and access token config. |
| P075-003 | Reconcile Artifact Delivery Matrix mailbox config with profile vocabulary | partial | Node config already requires homeserver URL, server name, token, event type, payload limit, retention, and sealing. |
| P075-004 | Define Room Matrix adapter config from the same profile | partial | `room_live.rs` already implements `RoomLiveTransport` over `MatrixEventSink` with authority-correct behavior (Room-core decides membership/sequence; Matrix only carries frames and redacts on close). Missing: `MatrixRoomLiveConfig` only has `relay_domain`; payload ceiling is a hardcoded `const`, and retention/timeout/backoff are not configurable via the shared profile shape. |
| P075-005 | Extend local Matrix fixture beyond Agora smoke, if needed | todo | Decide whether Room and AD reuse `node/tools/matrix-fixture` directly or add profile-specific bootstrap. |
| P075-006 | Add matrix-smoke harness profile in P074 implementation | todo | Should start fixture, export env, run selected multi-node Matrix smoke. |
| P075-007 | Add shared Matrix adapter diagnostic event names | todo | Align with trace/error vocabulary without making Matrix errors protocol errors. |
| P075-008 | Add operator-facing Matrix posture/readiness surface | partial | Agora status and AD UI expose some Matrix posture; Room needs equivalent when implemented. |
| P075-009 | Add retention/redaction conformance tests | partial | `room_live.rs` unit tests already cover redact-on-close, membership-projection-decisive-over-stale-passport, subscriber limits, and sink-failure-does-not-consume-sequence. Missing: the shared WSS/Matrix admission, revocation, cleanup, and bounded-delivery conformance suite implied by *Done When*, and any test for the P075-011 gap below. The suite does not require equal carrier ordering or replay histories. |
| P075-010 | Decide production deployment note for Conduit/Dendrite/Synapse | done | No production recommendation until operational evidence exists. Conduit remains the fixture/dev default only; production posture must be based on smoke, retention, reliability, and operator-maintenance data. |
| P075-011 | Evict revoked members from the underlying Matrix room, not only local Room-core state | todo | `MatrixEventSink` has no kick/ban primitive; `drop_member` in `room_live.rs` only updates in-memory Room-core state today. A revoked-but-still-Matrix-joined member is not evicted and could keep receiving live frames sent after revocation. Required fix: add a Matrix `kick`/`ban` sink operation. Until it lands, Matrix-backed Room live transport remains restricted to exposure modes where that residual risk is acceptable; it must not be used for `PrivateToSwarm` or high-privacy live rooms. |
| P075-012 | Promote Room Matrix payload/retention/backoff to configurable profile fields | todo | Replace the hardcoded `MATRIX_ROOM_LIVE_EVENT_MAX_BYTES` const and the minimal `MatrixRoomLiveConfig` with the section 8 profile shape, shared with `MatrixMailboxConfig` per *Reuse: Shared Matrix Carrier Primitive*. Keep component-local config paths, but use the shared semantic vocabulary. |
| P075-013 | Add Agent/Inquirium/Corpus boundary tests for Matrix-carried Room content | todo | Cover: an Agent step terminates on its own budget even when the Matrix adapter is degraded/slow; no Matrix event content reaches Inquirium prompt assembly except through `inquirium.context-assembly.request.v1` grants; Corpus answer classification tier-to-object expansion is identical regardless of carrier. |
| P075-014 | Freeze Matrix-backed Room as an optional bridge profile | done | P070 owns relocatable WSS relay epochs and Room liveness. Matrix carries already-authorized frames but contributes no Room DAG merge, durable history, membership, authority, or failover semantics. |

## Done When

- The shared profile is referenced by Matrix-backed consumers instead of duplicating
  carrier rules.
- The local fixture can be started reproducibly by the multi-node harness.
- Agora and Artifact Delivery Matrix adapters expose profile-compatible diagnostics.
- Room Matrix live transport uses the profile and passes shared admission,
  revocation, cleanup, and bounded-delivery conformance tests against the WSS
  adapter without importing equal ordering or replay-history semantics.
- `drop_member` evicts the underlying Matrix room membership, not only local
  Room-core authority state (P075-011).
- Story 011 can opt into a homeserver-backed live collaboration fixture without
  changing Corpus query, bid, selection, answer, or settlement semantics.

## Open Questions

None for this proposal revision.

Resolved 2026-07-01:

1. **Canonical config key.**
   Decision: keep component-local config paths, but share one semantic vocabulary
   for fields such as `homeserver_url`, `server_name`, token source, room alias
   prefix, event namespace, payload ceilings, timeouts, and retention policy.
   Rationale: this avoids migration churn while still preventing semantic drift.

2. **Production homeserver recommendation.**
   Decision: make no production recommendation until operational evidence exists.
   Conduit remains the local fixture/dev default only.
   Rationale: fixture suitability is not production suitability; production posture
   should be based on smoke, retention, reliability, and operator-maintenance data.

3. **Redaction failure semantics.**
   Decision: policy-dependent. Private or sensitive Room live profiles treat
   redaction failure as terminal or fail-closed; lower-exposure profiles may allow
   logical close to succeed while cleanup enters `degraded` with visible diagnostics.
   Rationale: this follows the classification/exposure model instead of making one
   transport cleanup outcome fit all rooms.

4. **Bot identity sharing.**
   Decision: use separate Matrix bot identities per adapter/component.
   Rationale: separate identities give clearer audit boundaries, narrower tokens,
   simpler revocation, and less accidental authority sharing.

5. **Risk before Matrix-side member eviction.**
   Decision: P075-011 must add a Matrix `kick`/`ban` sink operation so revocation
   becomes carrier-true, not only Room-core-true. Until that lands, restrict
   Matrix-backed Room live transport to exposure modes where a revoked-but-still-
   Matrix-joined member is an acceptable residual risk; do not use it for
   `PrivateToSwarm` or high-privacy live rooms.
   Rationale: this keeps the adapter usable for lower-risk profiles while
   preserving fail-closed privacy semantics for sensitive rooms.

6. **Federated Matrix deployment topology.**
   Decision: allow both one-homeserver-per-operator and shared-homeserver
   deployments, but require capability/passport evidence to declare the topology
   explicitly, e.g. `matrix.deployment/topology`.
   Rationale: this preserves deployment flexibility without hiding operational risk
   from policy and trust evaluation.

7. **Room bridge boundary.**
   Decision: P070's relocatable WSS relay is the production Room liveness baseline.
   Matrix remains an optional bridge profile and never contributes DAG merge, Room
   state, durable history, membership, authority, or failover semantics.
   Rationale: this preserves the useful Matrix adapter without coupling the small Room
   protocol to Matrix's larger distributed-state model.
