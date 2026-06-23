# Proposal 070: Room — Generic Subject-Addressed Room Primitive

Based on:

- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/005-operator-participation-room-policy-profiles.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/011-whisper/011-whisper.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/30-stories/story-002-federated-peer-learning.md`

## Status

`draft`

## Date

`2026-06-23`

## Executive Summary

The swarm has two divergent "room" notions today and no shared primitive:

- the **answer room** (P003, story-002) is currently a *derived read-model*
  (`answer-room-metadata.v1`) over a daemon execution record; its live
  many-participant form is deferred;
- the **association-room** (P013) is an Agora *proposal* meta-signal
  (`association-room-proposal.v1`); its membership/message/event family is documented
  but unbuilt.

They share no opening artifact, no substrate, and no generic contract. Proposal 069
(Corpus) needs a real live multi-participant room and is the forcing function to fix
this divergence rather than mint a third room family.

This proposal defines **one generic, subject-addressed `room` primitive** with two
explicit planes:

1. a **durable record skeleton** — signed `room.v1`, `room-membership.v1`,
   `room-event.v1` carrying identity, access list, and lifecycle, candidate substrate
   **Agora** (P035, the existing "shared record substrate");
2. an **ephemeral live message plane** — `room-live-message.v1` frames for synchronous,
   low-latency exchange that the protocol does **not** persist and does **not** treat
   as facts.

`answer-room` and `association-room` become projections of `room.v1`. Corpus and other
consumers ride the same primitive. A deliberately contracted transport layer (auth,
membership revocation, presence, retry, expiry, cleanup, sequence/replay, retention)
replaces the under-specified "Matrix/WSS as options" hand-wave — including the fact
that **Matrix is not ephemeral by default** and must be configured for
non-retention/redaction.

## Context and Problem Statement

`Room` is referenced by P069 as a prerequisite and implied by P003/story-002, but:

- there is no `room.v1` / `room-membership.v1` / `room-event.v1` contract;
- there is no agreed live transport, and the candidates (Matrix, WSS pub/sub) have
  very different retention, ordering, and presence semantics;
- the durable plane (if Agora-backed) has no defined topic namespace, signer
  authority, record kinds, ordering/high-water, replay, membership projection, or
  query attestation;
- without this, every room consumer (answer-room, association-room, Corpus) reinvents
  membership, access, and lifecycle.

## Goals

- One subject-addressed room identity and signed membership/lifecycle records.
- A clear two-plane split: durable signed skeleton vs ephemeral live reasoning.
- A contracted live transport with auth, revocation, presence, retry, expiry,
  cleanup, sequence/replay, and retention rules.
- An Agora-backed durable plane with explicit topic namespace and authority.
- Re-express `answer-room` (P003) and `association-room` (P013) as projections.

## Non-Goals

- This proposal does not define Corpus reasoning, procurement, or settlement (P069).
- It does not collapse rooms into one transport. MVP supports both Matrix and WSS
  pub/sub as contracted live substrates; each must satisfy the same room transport
  contract.
- It does not make the live chat durable; per-member capture stays a private option.

## Decision

### 1. Two Planes

A room has exactly two planes:

- **Durable record skeleton** (signed, append-only): who the room is, who may join,
  what rights they hold, and the ordered lifecycle. This is the source of truth for
  membership and authority.
- **Ephemeral live message plane**: synchronous frames for reasoning/coordination.
  The protocol neither stores nor replays them. Any member MAY locally capture them
  under its own classification and retention policy; capture is never a protocol
  obligation and never a shared fact.

### 2. Durable Plane over Agora

When the durable plane is Agora-backed (the recommended default; P035 is the existing
shared record substrate that already carries `association-room-proposal.v1`):

- **Topic namespace**: `orbiplex/room/v1/<authority>/<room-id>` — the single canonical
  subject-key form (also used by record-kind consumers and the Implementation
  Recommendations), derived from the opener authority and the room id.
- **Signer authority**: only the opener (or a delegated room authority) may sign
  `room.v1` open/close and grant-issuing `room-membership.v1`; members sign their own
  join/leave/acks. Authority changes (e.g. arbiter election in P069) are themselves
  signed `room-event.v1` records.
- **Record kinds**: `room.v1`, `room-membership.v1`, `room-event.v1` as Agora
  `record/kind` values.
- **Ordering / high-water**: each room carries a monotonic `seq/no`; consumers track a
  per-room high-water mark; out-of-order or gapped records are buffered or refused per
  policy, not silently merged.
- **Replay**: the durable skeleton is fully reconstructable from the Agora topic; a
  lost local projection rebuilds from replay.
- **Membership projection**: a deterministic read-model folds membership/event records
  into "current members + rights + lifecycle"; it is a projection, never authority.
- **Grant vocabulary**: MVP grants are the closed set `speak`, `vote`, `answer`,
  `observe`, `moderate`, and `delegate`. A Room implementation MUST treat any other
  grant as an extension requiring an explicit schema/policy extension; arbitrary
  strings are not accepted at the security gate.
- **Query attestation**: membership/authority queries return a signed
  `room-membership-attestation.v1` (subject, grants, lifecycle, signer, high-water
  `seq/no`, source record refs), not a bare boolean, so a relying party can audit why a
  subject is considered a member. This follows the same attested-result pattern as Seed
  Directory bindings and Agora ingest attestations rather than inventing a new trust
  model: the attestation is a projection signed by the room authority over the durable
  records, never a new source of truth.

### 3. Live Transport Contract

The live plane MUST contract the following, regardless of substrate (Matrix or WSS
pub/sub):

- **Room creation**: the opener creates the room (durable `room.v1`) first; the live
  channel is bound to the room id and is meaningless without a durable skeleton.
- **Auth / join**: a node joins only by presenting a room-scoped capability/invitation
  passport (reuse INAC invitation/capability passports, Solution 017/014). Ambient
  join is denied.
- **Membership revocation**: a signed `room-membership.v1` revoke removes a member;
  the transport MUST drop the revoked member's live access promptly (bounded lag) and
  the revoke is durable.
- **Presence**: presence (joined/ready/left/timed-out) is derived and ephemeral on the
  live plane but anchored by durable `ready`/`left` `room-event.v1` where it changes
  authority or budget accounting.
- **Retry / expiry / cleanup**: live frames are best-effort and idempotent by
  `(room/id, from, seq/no)`; the room has a durable `expires-at`; on expiry or close
  the transport channel is torn down through a bounded P055-style cleanup operation and
  any transport-side artifacts (e.g. Matrix room, WSS topic) are cleaned up. Cleanup
  timeout is degraded state, not silent success; the recommended MVP cleanup deadline is
  30 seconds unless deployment policy tightens or extends it.
- **Sequence / replay**: live frames carry a per-sender `seq/no` for local ordering and
  duplicate suppression; the protocol does not provide cross-member total order on the
  live plane (that is what the durable skeleton is for).
- **Retention**: live content is non-retained by contract. **Matrix is not ephemeral by
  default**: a Matrix-backed live plane MUST configure non-retention/redaction (server
  retention policy, message redaction on close, no public history) and MUST treat the
  Matrix room as a transient carrier, never as the durable skeleton. A WSS pub/sub
  fanout is naturally non-retained and is the simpler default for closed deliberations.

### 4. Access List and Authority

`room.v1` references a policy (`room-policy.v1`) carrying the access list and exposure:

- `access/list` — subjects (nyms/participants/nodes) permitted to join;
- `access/closed` — if true, only listed subjects may join;
- `exposure` — the room-level exposure vocabulary used by P005 and P070;
- `policy/profile` — the P005 operator-participation profile interpreted through the
  mapping table below.

#### Exposure Vocabulary Mapping

P009 remains the user-facing request exposure vocabulary. Room policy uses the more
operational room-level vocabulary because rooms need to distinguish bounded
cross-federation reach from truly global reach.

| P009 request exposure | P070 `room-policy.v1.exposure` | Rule |
|---|---|---|
| `private-to-swarm` | `private-to-swarm` | Direct mapping. |
| `federation-local` | `federation-local` | Direct mapping. |
| `public-call-for-help` | `cross-federation` or `global` | Call-site policy chooses bounded cross-federation by default; `global` requires explicit user/operator consent or a federation policy that says global publication is intended. |

This closes the P009 "split `public-call-for-help`" question for Room policy without
removing the simpler P009 user-facing label.

#### P005 Profile Mapping

The P005 profile is not a free-form label. Once a runtime interprets it, it maps to
specific room-policy fields:

| P005 profile | `human/linked-messages` | `human/live-participation` | Default use |
|---|---|---|---|
| `none` | `denied` | `denied` | Global or high-risk rooms where human live presence would create moderation or retention risk. |
| `mediated-only` | `allowed-via-node-mediation` | `denied` | Default for private, federation-local, and bounded cross-federation rooms. |
| `direct-live-allowed` | `allowed` | `allowed` | Explicit opt-in rooms with stronger membership, moderation, and retention controls. |

Future policy fields may refine those projections, but they must not silently advertise
one P005 profile and behave as another.

### 5. Projection of Existing Rooms

- **answer-room (P003)**: re-expressed as a `room.v1` opened by a `question-envelope`,
  with `answer-room-metadata.v1` becoming a projection over `room.v1` +
  `room-event.v1` instead of an execution-derived read-model.
- **association-room (P013)**: `association-room-proposal.v1` becomes a `room.v1`
  opener variant; the documented membership/message/event family maps onto
  `room-membership.v1` / `room-event.v1` / `room-live-message.v1`.

Migration is eager. There is no backward-compatibility requirement at this stage, so
new implementation work SHOULD move answer-room and association-room onto the Room
primitive instead of maintaining a compatibility projection first.

## Data Contracts

| Schema | Status | Purpose |
|---|---|---|
| `room.v1` | new | Subject-addressed room identity, opener, policy ref, lifecycle status. Signed. |
| `room-membership.v1` | new | Signed join/leave/grant/revoke with rights. Durable. |
| `room-event.v1` | new | Signed lifecycle events (`opened`, `ready`, `authority-changed`, `closed`). Durable. |
| `room-policy.v1` | new | Access list, exposure, expiry; reuses P009/P005 vocabularies. |
| `room-live-message.v1` | new (ephemeral wire) | Validated live frame: session boundary, `seq/no`, max size, replay handling. Validated but not persisted; not a fact. |
| `room-membership-attestation.v1` | new | Signed projection answering membership/authority queries (subject, grants, signer, high-water). |

## Relationship to Existing Mechanisms

- **Agora (008/P035)**: durable record substrate for the skeleton.
- **INAC (017) / Key Delegation (014)**: room-scoped invitation/capability passports
  gate join and enforce the access list.
- **Artifact Delivery (023)**: delivers room invites and the durable skeleton records;
  does not carry the live plane.
- **P003 / P013 / story-002**: consumers re-expressed as projections.
- **P069 (Corpus)**: first consumer that needs the live plane; forces this proposal.

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
|---|---|---|
| Matrix retains "ephemeral" chat | Privacy leak; chat reified as record | Contractual non-retention + redaction on close; Matrix room is a carrier only. |
| Live transport down | No deliberation | Durable skeleton survives; degrade/retry; never promote live frames to facts. |
| Revoked member keeps live access | Authority bypass | Bounded-lag transport drop on durable revoke; relying parties recheck membership projection. |
| Out-of-order durable records | Wrong membership view | Per-room `seq/no` + high-water; refuse/buffer gaps, never silent-merge. |
| Ambient join | Unauthorized presence | Join requires room-scoped passport; closed-room access list. |
| Orphaned transport rooms | Resource leak | `expires-at` + cleanup on close. |

## Resolved Decisions

1. **Live substrate support.** Matrix and WSS pub/sub are both MVP live substrates. They
   are adapter choices under the same Room transport contract, not competing protocol
   models.
2. **Migration scope.** Answer-room (P003) and association-room (P013) are eagerly
   re-expressed on `room.v1`; no compatibility projection is required at this stage.
3. **Presence semantics.** Only authority- or budget-relevant transitions are durable.
   Ordinary joined/typing/ready-ish liveness is live-plane state unless it changes
   authority, budget accounting, or lifecycle.
4. **Retention defaults.** Closed/private live content is non-retained by default; the
   durable skeleton is retained. Public rooms may define policy-specific retention, but
   live frames are never promoted to durable facts by default.
5. **Authority delegation.** The opener may delegate room authority through a signed
   delegation with explicit scope, expiry, and revocation. Delegation records are durable
   room events and must be reflected in the membership/authority projection.
6. **Grant vocabulary.** MVP room grants are a closed vocabulary:
   `speak`, `vote`, `answer`, `observe`, `moderate`, and `delegate`. Federations may
   introduce extension grants later only through an explicit schema/policy extension, not
   by silently accepting arbitrary strings at the security gate.
7. **Exposure vocabulary.** `room-policy.v1` uses the Room-level exposure vocabulary:
   `private-to-swarm`, `federation-local`, `cross-federation`, and `global`. P009
   `public-call-for-help` is a user-facing request label mapped at the P009->P070
   boundary. More specific room behavior, such as observer-only versus participatory
   public access, belongs in room policy/profile fields rather than a competing exposure
   enum.
8. **Derived answer-room projection.** A compatibility projection derived from existing
   question execution state is not a replayed Room fact stream. Its `high-water/seq-no`
   must therefore stay `0`; durable Room projections use the actual Room `seq/no`
   high-water.
9. **Live adapter ownership.** WSS pub/sub and Matrix are both concrete implementations
   behind one Room live-plane contract. Neither adapter owns a different membership,
   authority, retention, or cleanup semantics; conformance tests must run the same
   behavior suite against both.
10. **Signer-backed attestation service.** The first signer-backed
   `attest_membership` surface is a daemon query endpoint backed by the local signer.
   Middleware/live adapters may consume the attestation, but they do not receive a
   broader host capability to mint it directly in the first implementation.
11. **Room policy transport.** `room-policy.v1` may be published as an Agora record when
   a federation wants a public room-policy fact. Local-only policies remain allowed, but
   Agora-visible policies require schema-gate ingress/export coverage and must still be
   referenced from `room.v1` through `policy/ref`.
12. **Attestation transport.** `room-membership-attestation.v1` remains a direct runtime
   query response and may also be published through Agora when a durable/public proof of
   the query result is needed. It is not an Artifact Delivery payload by default.
13. **Policy profile mapping.** P005 room policy profiles map through an explicit table
   into `room-policy.v1` fields. Profiles are not free-form labels once a runtime
   interprets them.
14. **Implementation layering.** Room starts as canonical contracts plus a pure
    projection over Agora/host-owned facts, not as a separate monolithic
    `room-service` stack. Runtime surfaces may later be split into `room-core`,
    daemon host APIs, and optional transport-adapter middleware, but membership,
    authority, expiry, and retention semantics stay in the Room projection layer.
15. **Capability registration.** The reserved capability ids are `room.open`,
    `room.join`, and `room.membership-query`. They are registered in the
    Capability Registry and Node implementation ledger before runtime work so that
    passports and host grants do not invent informal room authority.
16. **Clock and expiry evaluation.** `seq/no` is the only ordering authority.
    Wall-clock fields such as `created-at`, `expires-at`, delegation expiry, and
    membership-attestation expiry are evaluated by the verifier's local trusted
    clock with an explicit policy-configured skew tolerance. Records whose
    validity window is impossible under that tolerance are refused or quarantined;
    near-boundary records may be accepted only with degraded diagnostics and a
    refresh requirement. The recommended MVP default is a 5 second skew tolerance.
    Old but otherwise valid durable records are not rejected merely for age; retention
    policy and high-water replay rules decide whether they remain usable.

## Implementation Contract

This section defines the minimum implementable shape of the Room primitive. The durable
plane and the live plane must remain separate in code: durable records form authority,
while live transports only carry ephemeral coordination frames under the authority of
the durable projection.

### Substrate and Canonicalization

Room domain records are payloads carried by the existing Agora envelope when they become
durable/federated facts:

- `room.v1`, `room-membership.v1`, and `room-event.v1` are `content/schema` values inside
  `agora-record.v1`, not replacements for the Agora envelope;
- `record/id`, `record/kind`, `topic/key`, `author/participant-id`,
  `author/nym-proof`, `record/parent`, `record/supersedes`, relay metadata, and
  envelope signatures remain Agora concerns;
- the Room content schema owns only room-domain fields such as `room/id`, `seq/no`,
  grants, lifecycle event, policy ref, and room-specific authority semantics;
- every durable Room signature, digest, idempotency key, and high-water calculation uses
  the Orbiplex canonical JSON profile implemented today by
  `agora-core::canonical::canonical_json_string`.

The first schema pass must make this carrier split explicit in examples: one example of
the domain payload and one example of the same payload embedded in `agora-record.v1`.

### Host Runtime Reuse

Room must reuse host-owned primitives instead of building a second control plane:

- **Bounded Local Server Runtime (016)** owns bounded local HTTP/WSS listener behavior.
- **Artifact Delivery (023)** delivers durable room records and room invites; it does
  not carry live frames.
- **Replay Scheduler (020)** owns cleanup/replay wakeups for expired rooms and stale
  projections.
- **Bounded Deferred Operations (029)** owns long-running cleanup and bounded-lag
  `revoke -> drop_member` / `close -> cleanup` operations.
- **Temporal Storage Convention (028)** owns local projection retention, compaction, and
  replay diagnostics.
- **Middleware (019)** may host external transport adapters, but adapter processes do not
  own membership or authority semantics.
- **TLS/WSS termination** belongs to the listener/transport layer. A Room WebSocket
  adapter may be tested as local `ws://` while still satisfying the Room live-plane
  contract; deployments that expose it off-host must place it behind the existing
  WSS/TLS listener policy rather than minting Room-specific trust roots.

### Implementation Entry Criteria

Runtime work MUST NOT begin until the first contract gate exists:

1. canonical schemas and examples for `room.v1`, `room-membership.v1`,
   `room-event.v1`, `room-policy.v1`, `room-live-message.v1`, and
   `room-membership-attestation.v1`;
2. positive and negative schema-gate/admission tests for invalid signatures, old
   canonicalization, clock skew, missing `author/nym-proof`, sequence gaps,
   duplicate `seq/no` with different digest, invalid authority, revoked membership,
   expired rooms, room-id reuse after close, projection gaps, signer-unavailable,
   oversized live frames, and missing live-message digest/nonce;
3. an Agora topic namespace fixture for `orbiplex/room/v1/<authority>/<room-id>`;
4. an explicit policy fixture for a closed private room and one public/exposed room;
5. transport conformance tests that can run against both Matrix and WSS adapters using
   the same behavior contract;
6. a positive deterministic projection golden vector proving that two nodes given the
   same accepted durable records produce byte-identical canonical membership views and
   the same projection digest.

### Durable Store and Projection Contract

The durable room plane is append-only. Implementations should separate:

1. **Fact store**: accepted `room.v1`, `room-membership.v1`, and `room-event.v1` records,
   keyed by `room/id`, `seq/no`, record digest, and signer.
2. **Projection**: deterministic read-model folded from facts into lifecycle, current
   authority, current members, grants, room policy, and high-water `seq/no`.
3. **Attestation layer**: signed answers over the projection, never direct authority.

Projection rules:

- duplicate records with the same digest are idempotent;
- duplicate `seq/no` with different digest is a conflict and must not be silently merged;
- conflicts enter a `pending-conflict` projection status until an operator/policy path
  chooses quarantine, rollback, or authoritative replay;
- gaps are buffered or refused according to local policy, never skipped;
- expired rooms cannot accept new live joins or live frames;
- revoked grants take effect in the projection before live transport authorization;
- delegated authority applies only inside its scope and before its expiry.
- every projection decision that depends on time must name the evaluation clock and
  skew tolerance used; ordering still comes from `seq/no`, never from timestamps.

Durability rules for lifecycle-like events are machine-checkable:

| Event class | Durable? | Rule |
|---|---|---|
| `opened`, `closed`, `expired` | always | They define the room lifecycle. |
| `delegated`, `delegation-revoked` | always | They change authority and must carry explicit delegation scope and expiry where applicable. |
| `member-granted`, `member-revoked` | always | They change access rights and invalidate membership attestations. |
| `ready`, `left`, `timed-out` | conditional | Durable only when the room policy marks readiness/presence as authority-, budget-, quorum-, or lifecycle-relevant. Otherwise they remain live-plane presence. |
| typing, cursor, ephemeral joined state | never by default | Live-plane state unless a future policy extension explicitly promotes it. |

Lifecycle, retention, and cleanup:

- **owner**: the local Room runtime projection store;
- **primary key**: `(room/id, seq/no, record/id)`;
- **retention**: durable facts follow the room retention policy; projections may be
  compacted after close/expiry only when replay can rebuild the same high-water state;
- **cleanup trigger**: room close, room expiry, retention window expiry, or operator
  maintenance task scheduled through Replay Scheduler;
- **indexes**: `room/id`, `seq/no`, `record/id`, lifecycle status, `expires-at`, and
  projection conflict status;
- **safety rule**: cleanup must not remove active rooms, unresolved conflicts, pending
  transport cleanup, or facts needed to verify a still-valid membership attestation.

### Authority State Machine

Room authority evolves through durable records:

| Current state | Event | Next state | Rule |
|---|---|---|---|
| none | `opened` | `opened` | Creates the room and initial authority. |
| `opened` | `delegated` | `delegated` | Allowed only by current authority and within explicit scope/expiry. |
| `delegated` | `delegation-revoked` | `opened` | Revokes scoped authority; prior delegated actions remain auditable facts. |
| `opened` or `delegated` | `member-granted` | unchanged | Adds or extends grants for one subject. |
| `opened` or `delegated` | `member-revoked` | unchanged | Removes grants for one subject and triggers live drop. |
| `opened` or `delegated` | `ready` | unchanged | Durable only when it affects authority, budget, or lifecycle. |
| `opened` or `delegated` | `expired` | `expired` | Terminal for live transport; projection remains queryable. |
| `opened` or `delegated` | `closed` | `closed` | Terminal for live transport; projection remains queryable. |
| `closed` or `expired` | any mutating event | refused | No reopen or grant mutation after terminal state. |

`opened` creates the initial authority. `delegated` grants scoped authority. `closed`
and `expired` are terminal for live transport, but the durable skeleton remains
queryable and replayable.

`closed` means explicit authority/operator closure. `expired` means the configured
validity window elapsed. Both are terminal: no mutating record may be appended after
either state. If both conditions are observed, the first terminal record in `seq/no`
order fixes the terminal reason; later terminal records are audit material only or are
refused according to local conflict policy.

Coupled state changes must be represented by one durable record or by an explicit
journaled sequence with monotonic `seq/no`. Projection trusts durable ordering only; it
must not merge concurrent state changes by "best effort" heuristics.

### Live Transport Adapter Interface

Matrix and WSS adapters must expose the same host-side behavior:

```text
open(room, policy) -> transport_binding
join(room_id, subject, passport_or_attestation) -> live_session
send(room_id, live_session, room-live-message.v1) -> accepted|rejected
drop_member(room_id, subject, reason) -> dropped|not-present
close(room_id, reason) -> closed
cleanup(room_id) -> cleaned|deferred
health(room_id) -> status
```

Each operation has mandatory bounds: timeout, maximum response bytes, retry policy,
backoff with jitter, concurrency limit per room, and failure class
(`retryable | terminal | degraded`). Defaults live in local policy and may be tightened
per deployment; unbounded adapter calls are invalid. The reference runtime uses a
5 second default clock-skew tolerance for live join attestations/passports, a 1 MiB
pre-parse frame/event ceiling for WSS and Matrix carrier inputs, a 1024 open-room
ceiling, and a 256 subscribers-per-room ceiling. Session refs are host-generated from
a canonical digest of `room/id`, not from a lossy path-safe rewrite of the room id.

Adapters must not decide membership or authority themselves. They receive an already
validated projection/attestation from the Room runtime and enforce it at the live
transport boundary.

### Retention Enforcement Contract

The default closed/private room live plane is non-retained:

- WSS pub/sub MUST avoid durable storage of live frames and MUST clear in-memory session
  buffers on close/expiry.
- Matrix MUST be configured as a transient carrier: no public history, bounded retention,
  redaction on close/expiry, and cleanup diagnostics when server-side deletion is
  delayed or partial. Redaction is a single close/expiry responsibility; cleanup must be
  idempotent and must not repeatedly redact the same carrier events.
- Any member-local capture is outside the shared protocol and must be classified under
  that member's own retention policy.
- Durable room records MAY mention live session refs and high-water lifecycle facts, but
  MUST NOT embed live message content.

### Membership Attestation API

The Room runtime should expose one query surface:

```text
attest_membership(room_id, subject, requested_grants) -> room-membership-attestation.v1
```

Failure modes are explicit: `room-not-found`, `room-expired`, `not-member`,
`grant-missing`, `projection-gap`, `authority-conflict`, `signer-unavailable`. A failed
attestation is not a live join denial reason by itself; it is the evidence the live
adapter uses to deny.

Attestations are short-lived. The default cache TTL is one minute for closed/private
rooms and MAY be shorter when revocation sensitivity is high. The MVP runtime caps
requested membership-attestation TTL at five minutes, and any membership-changing
record invalidates cached attestations for the affected room.

### Migration Plan

Because backward compatibility is not required at this stage, migration is eager:

1. `answer-room` (P003) opens a `room.v1` from the question envelope and derives answer
   metadata from the Room projection.
2. `association-room` (P013) maps proposals, membership, and lifecycle events onto the
   Room fact family.
3. Existing `answer-room-metadata.v1` and `association-room-proposal.v1` records are
   replayed into compatibility projections during the transition, but new authority is
   written only as Room facts.
4. If a node sees both legacy and Room records for the same subject, Room records win for
   authority and legacy records remain read-only provenance.
5. Legacy write paths should be deprecated for one release window and then removed once
   replay/recovery proves equivalent projections.

### Acceptance Slice

The first Room acceptance pack should prove:

1. open a closed private room and persist the durable skeleton;
2. grant two members and reject one ambient join;
3. join over WSS and Matrix using the same membership attestation contract;
4. revoke one member and observe bounded-lag live drop on both adapters;
5. close or expire the room and verify transport cleanup;
6. replay durable facts into an equivalent projection after restart;
7. verify that no live message content appears in the durable store or attestation;
8. reject a revoked passport rejoin attempt;
9. reject a join attempt after room expiry;
10. reject duplicate `seq/no` with a different digest;
11. reject room-id reuse after close;
12. replay `delegate -> revoke -> grant` and assert the same authority projection;
13. simulate WSS/Matrix divergence and assert convergence within bounded lag;
14. restart the authority node mid-deliberation and assert durable projection recovery
    without live-message recovery;
15. measure non-functional bounds: revoke latency, cleanup time, and projection rebuild
    time.

## Implementation Recommendations

`room.v1` (durable, signed):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "opener/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "authority/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "policy/ref": "room-policy:<digest>",
  "seq/no": 0,
  "created-at": "2026-06-23T10:00:00Z",
  "expires-at": "2026-06-23T10:30:00Z",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

`room-membership.v1`:

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "subject": { "kind": "nym", "id": "nym:did:key:P1" },
  "op": "join",
  "grants": ["speak", "vote"],
  "authority/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "seq/no": 3,
  "created-at": "2026-06-23T10:01:00Z",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

`room-event.v1`:

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "event": "ready",
  "authority/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "subject": { "kind": "nym", "id": "nym:did:key:P1" },
  "seq/no": 4,
  "created-at": "2026-06-23T10:01:05Z",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

`room-live-message.v1` (ephemeral wire schema: validated on the live plane, but not
signed-as-fact and not persisted by the protocol; a member may locally capture it):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "session/ref": "room-session:<id>",
  "from/subject": { "kind": "nym", "id": "nym:did:key:P1" },
  "nonce": "uYV3foRz3LeLwz5N5Jp3ew",
  "seq/no": 14,
  "size/bytes": 412,
  "content/type": "text/markdown",
  "content": "..."
}
```

The live plane validates each frame (schema, `session/ref` auth/session boundary,
`size/bytes` against a configured max, monotonic per-sender `seq/no` for ordering and
replay suppression) and then forwards it. Validation is not persistence: accepted frames
are never written to the durable skeleton.

Agora topic key: `orbiplex/room/v1/<authority>/<room-id>`; record kinds `room.v1`,
`room-membership.v1`, `room-event.v1`; consumers fold them into a membership/lifecycle
projection keyed by `room/id` with a per-room high-water `seq/no`.

`room-membership-attestation.v1` (signed query result):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "subject": { "kind": "nym", "id": "nym:did:key:P1" },
  "member": true,
  "grants": ["speak", "vote"],
  "high-water/seq-no": 17,
  "source/refs": ["room-membership.v1:...", "room-event.v1:..."],
  "attested-at": "2026-06-23T10:05:00Z",
  "expires-at": "2026-06-23T10:06:00Z",
  "signer/ref": "nym:did:key:...",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

The signature payload is the canonical JSON serialization of the full attestation
object with the top-level `signature` field removed. Verifiers therefore check the
room id, subject, granted rights, high-water sequence, source refs, signer ref, and
validity window as one signed value; the signature never signs itself.

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Phase 0 — Durable skeleton contracts

- [x] Complete the Implementation Entry Criteria: canonical schemas, examples,
  schema-gate tests, Agora topic namespace fixture, policy fixtures, and live transport
  conformance test harness. Schemas, examples, schema-gate ingress/export coverage,
  canonical topic-key fixtures, deterministic projection golden vectors, and shared
  live transport conformance are implemented across `room-core`, `schema-gate`, the
  bounded WebSocket adapter, and the Matrix adapter.
- [x] Define `room.v1`, `room-membership.v1`, `room-event.v1`, `room-policy.v1`
  (subject-addressed, signed, `seq/no`, access list). Implemented as canonical
  schemas plus `orbiplex-node-room-core` DTOs.
- [x] Define the Agora topic namespace, record kinds, signer authority, and high-water
  ordering. Topic/record-kind constants, persisted fact replay in `agora-projections`,
  and high-water projection are implemented; `room-core` validates record signer
  authority against the projected authority subject. Cryptographic verification remains
  a carrier/host boundary responsibility.
- [x] Add the positive projection golden vector: identical durable record sets on two
  nodes must produce byte-identical canonical membership views and equal projection
  digests, including expiry evaluation under an explicit skew tolerance. The golden
  vector is shared between `room-core` and `agora-projections`.
- [x] Add schema-gate ingress/export coverage for Agora-visible Room records.
  `room.v1`, `room-membership.v1`, and `room-event.v1` have Agora content ingress
  coverage, and `room-policy.v1` / `room-membership-attestation.v1` schemas are
  mirrored into node schema-gate contracts with positive/negative examples. Dedicated
  helper APIs now validate `room-policy.v1` import/export,
  `room-live-message.v1` ingress/egress, and
  `room-membership-attestation.v1` export, while Agora content ingress accepts durable
  policy and attestation publication.

### Phase 1 — Membership projection and query attestation

- [x] Deterministic membership/lifecycle projection from durable records. Implemented
  in `orbiplex-node-room-core` with duplicate, gap, conflict, close, and expiry tests;
  `orbiplex-node-agora-projections` persists `room.v1`, `room-membership.v1`, and
  `room-event.v1` facts and rebuilds the runtime Room read-model from ordered Agora
  records.
- [x] Attested membership/authority query results (signer, high-water, grants).
  `room-membership-attestation.v1` is defined, `room-core` provides a pure
  `attest_membership` factory with explicit failure modes, and `agora-service`
  exposes authenticated projection queries:
  `GET /v1/agora/projections/rooms/{room_id}` and
  `GET /v1/agora/projections/rooms/{room_id}/membership-attestation`.
  The attestation path signs canonical attestation bytes through the host signer under
  `room-membership-attestation.v1`; repeated grant parameters are intentionally not a
  query language, so callers request multiple grants with comma-separated `grants`.
  The shared `room-core` contract bounds subject identifiers, signer refs, signature
  values, durable digest inputs, local clock-skew tolerance, and attestation TTL; it
  also normalizes requested grants before membership checks and signing.

### Phase 2 — Live transport contract

- [x] Define `room-live-message.v1` and the transport contract (auth via room-scoped
  passport, revocation drop, presence, retry, expiry, cleanup, sequence). The schema
  exists and `room-core` now owns the typed live-frame DTO, room-scoped passport
  projection gate, join/send/drop/close/cleanup contract, per-sender `seq/no`
  duplicate suppression, and shared conformance tests.
- [x] Implement both MVP substrates: WSS pub/sub and Matrix with enforced
  non-retention/redaction. Both adapters satisfy the same auth, revocation, sequencing,
  expiry, cleanup, and retention contract. `room-wss` provides the bounded WebSocket
  pub/sub adapter over the shared Room live contract, including pre-parse frame limits.
  `agora-matrix-client` provides the Matrix carrier adapter over `MatrixEventSink`,
  including bounded subscriptions, oversized event refusal before JSON projection, and
  close/expiry redaction with idempotent cleanup.

### Phase 3 — Access, exposure, lifecycle

- [x] Enforce access list / closed rooms via INAC room-scoped passports. The live
  contract accepts a normalized `RoomScopedPassport` or a signed membership
  attestation, but durable Room projection membership remains decisive so stale or
  revoked passports cannot rejoin.
- [x] Wire exposure modes (P009) and room policy profiles (P005). `room-policy.v1`
  now uses the room-level P009/P070 exposure mapping and documents the explicit P005
  profile-to-policy table; schema and `room-core` runtime validation reject profile
  field drift.
- [x] Implement open/ready/close/expiry lifecycle with transport cleanup. Durable
  projection supports open/close/expiry; `room-service` owns open/join/send/drop/close
  and cleanup over live transports, and Matrix close/expiry redacts live frames while
  cleanup remains idempotent.

### Phase 4 — Consolidation

- [x] Eagerly re-express answer-room (P003) as a `room.v1` projection. Execution
  inspection exposes a `RoomProjection` rather than a bespoke room type. Historical
  selected-responder executions remain a compatibility-derived projection with
  `high-water/seq-no = 0`; future collaborative answer-room writes should use Room
  facts directly.
- [x] Re-express association-room (P013) onto the membership/event family. The
  association-room lifecycle FSM is now owned by `orbiplex-node-room-core` and reused
  by Whisper/Agora projections. Legacy association-room proposal records remain
  provenance; new live/durable implementations should use the Room family directly.
- [x] Provide the live plane needed by Corpus (P069) deliberation. The P070 live-plane
  runtime contract, bounded WebSocket pub/sub adapter, and Matrix adapter now exist;
  Corpus can build deliberation on Room without inventing a third room model.
