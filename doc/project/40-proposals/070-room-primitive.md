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
- It does not mandate Matrix; it contracts the transport so Matrix or a WSS pub/sub
  fanout can satisfy it.
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
  the transport channel is torn down and any transport-side artifacts (e.g. Matrix
  room, WSS topic) are cleaned up.
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
- `exposure` — reuse P009 exposure modes and P005 room policy profiles for observer
  vs participant rights.

### 5. Projection of Existing Rooms

- **answer-room (P003)**: re-expressed as a `room.v1` opened by a `question-envelope`,
  with `answer-room-metadata.v1` becoming a projection over `room.v1` +
  `room-event.v1` instead of an execution-derived read-model.
- **association-room (P013)**: `association-room-proposal.v1` becomes a `room.v1`
  opener variant; the documented membership/message/event family maps onto
  `room-membership.v1` / `room-event.v1` / `room-live-message.v1`.

Migration may be eager or via a compatibility projection (Open Question).

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

## Open Questions

1. **Live substrate default.** Matrix (P003's choice, retention work required) vs WSS
   pub/sub fanout (simpler non-retention) as the default for closed rooms?
2. **Migration scope.** Eager re-expression of answer-room/association-room, or a
   compatibility projection first?
3. **Presence semantics.** How much presence is durable vs purely live?
4. **Retention defaults.** Default redaction/retention policy per exposure mode.
5. **Authority delegation.** May the opener delegate room authority (needed for
   arbiter election in P069), and how is that bounded?

## Implementation Recommendations

`room.v1` (durable, signed):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "opener/nym": "nym:did:key:...",
  "policy/ref": "room-policy.v1:<digest>",
  "status": "open",
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
  "subject/nym": "nym:did:key:P1",
  "op": "join",
  "grants": ["speak", "vote"],
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
  "subject/nym": "nym:did:key:P1",
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
  "from/nym": "nym:did:key:P1",
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
  "subject/nym": "nym:did:key:P1",
  "member": true,
  "grants": ["speak", "vote"],
  "high-water/seq-no": 17,
  "source/refs": ["room-membership.v1:...", "room-event.v1:..."],
  "attested-at": "2026-06-23T10:05:00Z",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Phase 0 — Durable skeleton contracts

- [ ] Define `room.v1`, `room-membership.v1`, `room-event.v1`, `room-policy.v1`
  (subject-addressed, signed, `seq/no`, access list).
- [ ] Define the Agora topic namespace, record kinds, signer authority, and high-water
  ordering.

### Phase 1 — Membership projection and query attestation

- [ ] Deterministic membership/lifecycle projection from durable records.
- [ ] Attested membership/authority query results (signer, high-water, grants).

### Phase 2 — Live transport contract

- [ ] Define `room-live-message.v1` and the transport contract (auth via room-scoped
  passport, revocation drop, presence, retry, expiry, cleanup, sequence).
- [ ] Implement one substrate (WSS pub/sub default or Matrix with enforced
  non-retention/redaction).

### Phase 3 — Access, exposure, lifecycle

- [ ] Enforce access list / closed rooms via INAC room-scoped passports.
- [ ] Wire exposure modes (P009) and room policy profiles (P005).
- [ ] Implement open/ready/close/expiry lifecycle with transport cleanup.

### Phase 4 — Consolidation

- [ ] Re-express answer-room (P003) as a `room.v1` projection (eager or compat).
- [ ] Re-express association-room (P013) onto the membership/event family.
- [ ] Provide the live plane needed by Corpus (P069) deliberation.
