# Proposal 070: Room — Generic Subject-Addressed Room Primitive

Based on:

- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/005-operator-participation-room-policy-profiles.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/project/60-solutions/011-whisper/011-whisper.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/30-stories/story-002-federated-peer-learning.md`

## Status

`promoted`

Promoted to: `doc/project/60-solutions/036-room/036-room.md`

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
replaces the under-specified "Matrix/WSS as options" hand-wave. The firewall-proof
baseline is one relocatable WSS relay endpoint per active relay epoch, reached through
outbound TLS connections. Matrix remains an optional bridge profile and is never
imported as Room ordering, membership, or durable-history semantics.

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
- It does not make every participant publicly reachable and does not place
  STUN/ICE, NAT hole punching, UDP, or QUIC on the Room liveness path. One reachable
  WSS relay endpoint per active relay epoch is sufficient.
- It does not make Matrix a Room dependency. The implemented Matrix adapter is an
  optional bridge profile under the same authority boundary; Matrix DAG, room-state,
  and history semantics do not enter Room Core.
- It does not make the live chat durable; per-member capture stays a private option.

## Decision

### 1. Two Planes

A room has exactly two planes:

- **Durable record skeleton** (signed, append-only): who the room is, who may join,
  what rights they hold, and the ordered lifecycle. This is the source of truth for
  membership and authority.
- **Ephemeral live message plane**: synchronous frames for reasoning/coordination.
  The protocol does not durably store them. One relay epoch MAY keep a bounded
  in-memory replay window for reconnect, but it creates no cross-epoch history. Any
  member MAY locally capture frames under its own classification and retention policy;
  capture is never a protocol obligation and never a shared fact.

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
- **Record kinds**: `room.v1`, `room-membership.v1`, `room-event.v1`, and, after
  Phase 6A, `room-relay-endpoint.v1` as Agora `record/kind` values.
- **Ordering / high-water**: each room carries a monotonic `seq/no`; consumers track a
  per-room high-water mark; out-of-order or gapped records are buffered or refused per
  policy, not silently merged.
- **Replay**: the durable skeleton is fully reconstructable from the Agora topic; a
  lost local projection rebuilds from replay.
- **Membership projection**: a deterministic read-model folds membership/event records
  into "current members + rights + lifecycle"; it is a projection, never authority.
- **Grant vocabulary**: MVP grants are the closed set `speak`, `vote`, `answer`,
  `observe`, `actuate`, `moderate`, and `delegate`. A Room implementation MUST treat any other
  grant as an extension requiring an explicit schema/policy extension; arbitrary
  strings are not accepted at the security gate. P083-009 enacted `actuate` as the
  explicit collaborative Sensorium actuation extension; it never replaces exact
  Sensorium Interface authority or a current control lease.
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
  duplicate suppression. The protocol does not provide an authority-bearing
  cross-member total order on the live plane. P070 Phase 6A adds only a per-relay-epoch
  carrier order for bounded delivery and reconnect; durable and domain-specific signed
  sequences remain decisive.
- **Retention**: live content is non-retained by contract. **Matrix is not ephemeral by
  default**: a Matrix-backed live plane MUST configure non-retention/redaction (server
  retention policy, message redaction on close, no public history) and MUST treat the
  Matrix room as a transient carrier, never as the durable skeleton. A WSS pub/sub
  fanout is naturally non-retained and is the simpler default for closed deliberations.

### 3A. Relocatable WSS Relay Epochs

The production WSS topology uses a simple firewall posture: every participant opens
an outbound `wss://` connection, normally over TCP 443, to exactly one active relay
endpoint for the current relay epoch. Room does not require every node to expose a
listener. It also does not require UDP reachability, QUIC, STUN, ICE, or peer-to-peer
hole punching for liveness.

Relay placement is selected in this order unless room policy explicitly narrows it:

1. the requester/opener node, when it advertises a currently reachable endpoint;
2. another current room member with relay-capable readiness evidence;
3. a federation relay service for the all-behind-CGNAT case.

For a node candidate, `relay-capable` readiness reuses a current signed
`node-advertisement.v1` endpoint with `endpoint/transport = wss` and
`endpoint/role = relay`, optionally strengthened by `node-address-attestation.v1` and
a bounded current reachability probe. It is not a new capability id. A federation
service candidate must supply equivalent operator-admitted endpoint/readiness evidence
under the same evaluator.

Candidate readiness is evidence, not authority. The active placement is established
only by a signed, append-only `room-relay-endpoint.v1` fact issued by the current Room
authority or a delegated authority whose durable delegation includes `relay/manage`.
`relay/manage` is a closed Room authority-delegation scope carried by
`room-event.v1`; it is not a membership grant, a relay readiness flag, or a host
capability. Phase 6A provides typed delegation scopes, expiry, and revocation linkage
in the Room event contract and refuses endpoint facts outside that authority. If a
callable host relay-management surface is introduced later, its capability id and
ledger row must be registered before runtime code is added.

The endpoint fact is necessary but not sufficient to authorize a dial. Every client
still applies host-owned egress policy and Node Transport endpoint trust. The selected
URL, relay subject, and placement must match the referenced advertisement, address
attestation, or operator-admitted service evidence exactly. Room authority cannot turn
an arbitrary URL into permitted host egress. The endpoint schema deliberately permits
private, loopback, and link-local hosts because local and same-host relays are valid
deployments; the dial-time egress and transport-trust gates, not schema shape, decide
whether a concrete target is reachable from a given host.

The fact binds at least:

- `room/id` and durable Room `seq/no`;
- positive monotonic `relay/epoch`;
- `relay/subject` and
  `relay/placement = requester | room-member | federation-service`;
- canonical `endpoint/url`, restricted to `wss://` for this profile;
- `crypto/profile`, `ordering/profile`, and issue/expiry; the signed Agora envelope
  owns optional `record/supersedes` lineage;
- bounded `selection/evidence-refs` for the advertisement, address attestation, service
  readiness, or probe result used during selection; these refs explain selection but
  grant no Room authority;
- authority subject; the enclosing Agora record binds author/delegation evidence and
  the canonical-JSON signature.

At most one endpoint fact is active for an epoch. A conflicting fact for the same
`relay/epoch` is an authority conflict and fails closed. A newer valid epoch supersedes
the old carrier binding and resolves that relay-specific conflict. Generic durable
record conflicts remain pending until their existing operator/policy path acts; only a
strictly newer valid relay epoch may clear a same-epoch relay conflict. Supersession does
not reopen, replace, or fork the durable Room.

The relay assigns a positive monotonic `relay/seq-no` to every accepted ephemeral
delivery in one epoch. Client resume cursors are the tuple
`(relay/epoch, relay/seq-no)`. This is a presentation and bounded-replay order only:

- sender-owned `seq/no`, signed turn numbers, P083 source generations, lease epochs,
  and operation sequences remain the authority-bearing order;
- a relay cannot mint membership, grants, turns, leases, or effects;
- failover starts a new epoch and never merges carrier histories through a DAG, CRDT,
  or cross-epoch total order;
- after failover, clients rebuild authority from Agora facts and domain read-models,
  then resume the new live epoch from its current snapshot or bounded buffer.

Carrier sequence detects gaps and supports bounded replay, but does not prove complete
delivery. A malicious or failed relay can drop, delay, reorder before acceptance, or
observe connection metadata. Domain operations that require an effect or receipt use
their own acknowledgements, idempotency, durable facts, and retry policy. Once a newer
endpoint fact is accepted, clients refuse frames and resume cursors from every older
relay epoch.

Endpoint discovery cannot depend on the failed relay. The endpoint fact is a durable
Room/Agora record and may also be delivered through Artifact Delivery mailbox paths to
known members. The mailbox accepts endpoint facts only for an already open local Room;
unknown or unopened Rooms are rejected synchronously and are not buffered by the
acceptor. Artifact Delivery carries the control-plane fact, not live Room frames.

The relay's permitted decisions are deliberately narrow: validate the presented
membership attestation, bind the authenticated subject to the session, enforce frame,
connection, and buffer caps, assign carrier sequence, and drop sessions after current
revocation or expiry becomes visible. It does not evaluate domain policy or issue
grants. Connected presence is an ephemeral hint and never membership evidence.

Operational defaults for this profile are:

- WSS over TLS/TCP 443; QUIC may be a measured optimization but never a dependency;
- ping/keepalive approximately every 25 seconds, configurable within a bounded local
  policy so common NAT idle timers do not silently remove sessions;
- reconnect with exponential backoff and jitter;
- resubscription with the last `(relay/epoch, relay/seq-no)` cursor and a closed
  `resume/reason` of `recovery` or `reconnect`; only the latter increments reconnect
  diagnostics;
- one bounded in-memory replay window, with typed `cursor-expired` followed by current
  snapshot/read-model refresh when the requested frame is no longer retained. A client
  commits the replacement checkpoint only after that refresh succeeds; failed refresh
  leaves the prior checkpoint current and retryable.

Room liveness belongs to the relay epoch, not to the Room. A Room remains open and its
durable facts remain replayable while no relay endpoint is reachable.

### 3B. Crypto Profiles Follow Relay Placement

The endpoint fact carries an explicit crypto profile from the first implementation:

- `member-visible-tls-v1` is the baseline. The relay is a current Room member whose
  grants and Room policy permit receiving the live content; TLS protects each
  participant-to-relay hop. This profile does not claim end-to-end secrecy from the
  relay, forward secrecy, or post-compromise security. A federation relay service may
  use this profile only when it is admitted as such a content-visible member.
- `sealed-sender-key-v1` is the implemented profile for a federation relay that is not
  a Room member. Each active sender distributes sender-key material for the relay and
  membership epoch through recipient-private pairwise X25519/HKDF/XChaCha20-Poly1305
  packages signed with Ed25519 domain separation. Encrypted frames bind room, relay
  epoch, membership epoch, sender, sender sequence, ciphertext digest, and signer, so
  possession of another member's decryption material does not grant impersonation.
  Every membership fact advances a monotonic membership high-water; join, leave, grant,
  or revoke therefore fences prior ciphertext and rotates active sender-key material
  with bounded O(n) fan-out per active sender. Runtime relay transitions serialize
  projection refresh, publication, resume, and lifecycle changes so a frame cannot be
  admitted through an interleaving between membership authorization and carrier-state
  rotation. The accepted durable membership projection is the rotation trigger: its
  high-water refreshes and fences host relay state, while each active sender consumes
  the same projection to generate and pairwise-distribute fresh sender-key material.
  The host relay and federation relay never perform that redistribution because neither
  is allowed to possess the sender key. The relay sees outer connection, sender, epoch,
  sequence, timing, and size metadata, but not plaintext payload class, schema, content,
  or key material. Receivers advance sender high-water and their durable relay checkpoint
  only after the signed frame has been authenticated, its payload has been opened
  successfully, and the plaintext class/schema contract has passed admission.

MLS or another tree-based group protocol is not implicit in either profile. It may be
specified later as a new profile only if long-lived, larger rooms make O(n) fan-out per
active sender a measured problem.

Matrix is an optional bridge profile over the Room live contract. The adapter exists;
production homeserver deployment remains profile work. It may translate Room frames to
Matrix events, but Matrix DAG merge, state events, history, and homeserver membership
never become Room semantics or a fallback authority source.

### 3C. Sensorium Control Uses the Same Carrier, Not Its Authority

With Phase 6A implemented, P083 status, claim, control, invoke, and receipt messages use
the active Room relay as their default firewall-proof carrier. Their exact interface
grant, source generation, lease id, lease epoch, operation sequence, and host policy
travel in the request and remain decisive. The relay is therefore only a pipe.

An authenticated direct chair-to-Workbench connection may replace the relay path as a
latency optimization, especially for human terminal echo. It is never required for
correctness and never changes the lease. Hole punching, if ever attempted for that one
pair, belongs to the optional direct-carrier adapter rather than Room.

Initial latency budgets guide measurement rather than changing semantics:

| Path | Operational target | Consequence |
|---|---:|---|
| deliberation turns | seconds | model generation dominates; relay overhead is not a blocker |
| P082 terminal latest-state | 100-300 ms at 4-10 updates/s | bounded WSS relay is the normal path |
| human terminal input-to-echo | below roughly 150-250 ms | try direct peer when the relay path exceeds the acceptable local policy budget |

An Agent chair does not require the human terminal-echo target. Operators should
measure end-to-end latency before enabling a direct upgrade rather than infer it from
hop count alone.

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
| `room-event.v1` | new | Signed lifecycle and authority-delegation events. Phase 6A adds closed delegation scopes, bounded expiry, and explicit revocation linkage for `relay/manage`. Durable. |
| `room-policy.v1` | new | Access list, exposure, expiry; reuses P009/P005 vocabularies. |
| `room-live-message.v1` | new (ephemeral wire) | Validated live frame: carrier-authenticated session boundary outside the payload, `seq/no`, max size, replay handling. The bearer session ref is not part of the frame. Validated but not persisted; not a fact. |
| `room-membership-attestation.v1` | new | Signed projection answering membership/authority queries (subject, grants, signer, high-water). |
| `room-membership-attestation-request.v1` | new | Explicit request contract for runtime attestation issuance: request mode, requester, subject, requested grants, TTL, and room-scoped authorization. |
| `room-attestation-audit.v1` | new | Metadata-only operator-visible audit fact for issued, refused, deduplicated, and rate-limited attestation requests. |
| `room-relay-endpoint.v1` | implemented Phase 6A | Durable Room payload inside a signed Agora record, selecting one active WSS endpoint, relay epoch, placement, crypto profile, and ordering profile. Agora owns supersession lineage. |
| `room-relay-delivery.v1` | implemented Phase 6A | Ephemeral member-visible carrier header with required `delivery/kind: member-visible`, adding `relay/epoch` and `relay/seq-no` around an already validated Room live or projection payload; it is not a durable fact. |
| `room-relay-sender-key-distribution.v1` | implemented Phase 6B | Signed recipient-private sender-key package bound to Room, relay epoch, membership epoch, sender, and recipient. It is delivered through an existing pairwise sealed channel and is never relay fan-out content. |
| `room-relay-sealed-delivery.v1` | implemented Phase 6B | Ephemeral relay delivery with required `delivery/kind: sealed`, carrying an authenticated encrypted sender frame plus relay ordering metadata. Plaintext payload metadata remains inside the ciphertext. |

## Relationship to Existing Mechanisms

- **Agora (008/P035)**: durable record substrate for the skeleton.
- **INAC (017) / Key Delegation (014)**: room-scoped invitation/capability passports
  gate join and enforce the access list.
- **Artifact Delivery (023)**: delivers room invites, durable skeleton records, and
  out-of-band relay-endpoint updates when the prior relay is unreachable; it does not
  carry the live plane.
- **Node Transport (P014 / Solution 000)**: owns public WSS/TLS endpoint mechanics,
  WebPKI hostname validation, TLS trust configuration, and carrier reachability. Room
  owns relay selection and admission semantics, not a second TLS identity protocol.
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
| Relay outage is reported as Room death | Durable collaboration is treated as lost | Model liveness on `relay/epoch`; Room facts and authority survive with no active relay. |
| Relay becomes policy authority | A carrier can mint membership or effects | Relay validates evidence and caps only; durable Room projection and domain-specific fencing remain decisive. |
| Two endpoints claim one epoch | Split live view | Fail closed on same-epoch conflict; only a newer authority-signed epoch performs failover. |
| Failover tries to merge ephemeral histories | DAG/CRDT complexity enters Room Core | Start a new relay epoch and refresh from durable facts/read-models; never merge epochs. |
| Federation relay reads private content | Confidentiality breach | Require `sealed-sender-key-v1`; disclose metadata leakage and rotate active sender keys after membership change. |
| Idle NAT binding disappears | Silent live disconnect | Bounded approximately 25-second keepalive plus jittered reconnect and cursor resubscription. |
| Room authority selects an arbitrary URL | SSRF-like egress or trust bypass | Require an exact match to referenced endpoint evidence plus host egress and Node Transport trust policy before dialing. |
| Malicious relay drops or delays frames | False assumption of complete delivery | Treat relay sequence as gap detection only; domain acknowledgements, idempotency, facts, and retry remain authoritative. Fail over on bounded liveness policy. |
| Superseded relay continues sending | Split live view or rollback | Bind sessions and cursors to the accepted active epoch and refuse every lower-epoch frame after supersession. |

## Resolved Decisions

1. **Live substrate support (revised by Decision 17).** Matrix and WSS pub/sub were
   implemented under one behavior contract. The production baseline is now the
   relocatable WSS relay; Matrix remains a bridge adapter and is not required for Room
   liveness or imported into Room semantics.
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
   `speak`, `vote`, `answer`, `observe`, `actuate`, `moderate`, and `delegate`. Federations may
   introduce extension grants later only through an explicit schema/policy extension, not
   by silently accepting arbitrary strings at the security gate. P083-009 extends the
   schema, runtime vocabulary, and conformance tests with `actuate`; current Room
   membership remains collaboration policy rather than interface or lease authority.
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
9. **Live adapter ownership (revised by Decision 17).** WSS pub/sub and Matrix are
   concrete implementations behind one Room live-plane contract. Neither adapter owns
   membership or authority. Matrix conformance remains useful, but Matrix is an optional
   bridge rather than a required co-equal liveness substrate.
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
    A relay endpoint's `issued-at` must not exceed the trusted evaluation clock plus
    that tolerance. Scoped delegation authority is evaluated at the admitted fact's
    issue time, preserving deterministic replay of facts that were valid when issued.
    Old but otherwise valid durable records are not rejected merely for age; retention
    policy and high-water replay rules decide whether they remain usable.
17. **Firewall-proof relay baseline.** Room requires one reachable WSS/TLS endpoint per
    active relay epoch, not public reachability for every member. The protocol does not
    depend on hole punching, UDP, QUIC, STUN, or ICE.
18. **Relay epoch ordering.** One relay epoch has one monotonic carrier order. Failover
    creates a new epoch and clients resynchronize from durable facts and current
    read-models; no cross-epoch merge is defined.
19. **Relay placement and crypto.** Placement is authority-signed and follows requester,
    relay-capable member, then federation-service preference. A member relay uses
    `member-visible-tls-v1`; a non-member relay requires the later
    `sealed-sender-key-v1` profile. Neither profile claims MLS, forward secrecy, or PCS.
20. **Presence and relay authority.** Connected presence is an ephemeral hint. A relay
    may validate admission evidence and enforce bounds, but it cannot mint policy,
    membership, grants, or domain effects.
21. **Interactive control carrier.** The active relay is the default firewall-proof P083
    carrier. Direct peer is an optional latency upgrade and cannot create or transfer a
    lease.
22. **Relay management authority.** `relay/manage` is a closed scope of durable Room
    authority delegation. It is not a membership grant, readiness claim, or host
    capability, and it expires or is revoked through the Room authority projection.
23. **Relay fact signing.** `room-relay-endpoint.v1` is signed through its
    `agora-record.v1` envelope. It does not introduce an inner signature or a second
    content-addressing and supersession protocol.

## Implementation Contract

This section defines the minimum implementable shape of the Room primitive. The durable
plane and the live plane must remain separate in code: durable records form authority,
while live transports only carry ephemeral coordination frames under the authority of
the durable projection.

### Substrate and Canonicalization

Room domain records are payloads carried by the existing Agora envelope when they become
durable/federated facts:

- `room.v1`, `room-membership.v1`, `room-event.v1`, and
  `room-relay-endpoint.v1` are `content/schema` values inside `agora-record.v1`, not
  replacements for the Agora envelope;
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

- **Bounded Local Server Runtime (016)** owns connection bounds, overload behavior,
  deadlines, metrics, and shutdown for the synchronous listener implementation. Its
  reuse does not make loopback binding or cleartext `ws://` a production Room policy.
- **Node Transport (P014 / Solution 000)** owns public WSS/TLS ingress, WebPKI server
  authentication, and carrier reachability. Room supplies a bounded handler and
  authority contract; it does not mint Room-specific transport trust roots.
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
- **Capability Registry (P072)** is not extended merely because a node advertises relay
  readiness or appears in an endpoint fact. A new capability id is required only if
  a later slice introduces a callable host-management surface. Phase 6A does not add
  one; the data-plane relay role remains governed by Room authority facts and admission
  evidence.
- **TLS/WSS termination** belongs to the listener/transport layer. A Room WebSocket
  adapter may be tested as local `ws://` while still satisfying the Room live-plane
  contract; deployments that expose it off-host must place it behind the existing
  WSS/TLS listener policy rather than minting Room-specific trust roots.

### Implementation Entry Criteria

Runtime work MUST NOT begin until the first contract gate exists:

1. canonical schemas and examples for `room.v1`, `room-membership.v1`,
   `room-event.v1`, `room-policy.v1`, `room-live-message.v1`,
   `room-membership-attestation.v1`, `room-membership-attestation-request.v1`,
   and `room-attestation-audit.v1`;
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
- a same-epoch relay endpoint conflict is the narrow exception resolved by a strictly
  newer valid relay epoch; its conflicting fact still consumes its durable `seq/no`,
  and no unrelated next fact clears the conflict; the projection records the typed
  `relay/conflict-epoch` discriminator instead of deriving state from diagnostic text;
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
256 bits of cryptographically secure randomness and act as bearer secrets. A session
ref is returned only to the joining client and may be repeated only in that client's
join-adjacent subscription or admission requests. It MUST NOT appear in live-message
payloads, subscription acknowledgements, fan-out deliveries, member-visible status,
durable Room facts, or shared Corpus observations.

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
- Durable room records MAY mention high-water lifecycle facts, but MUST NOT mention
  live session refs or embed live message content.

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
rooms and MAY be shorter when revocation sensitivity is high. Requested TTL is capped
per exposure mode (see *Attestation Endpoint Policy*), and any membership-changing
record invalidates cached attestations for the affected room (revocation freshness
beats TTL).

### Attestation Endpoint Policy (exposure-governed)

The attestation produced by `attest_membership` is the credential a live adapter
consumes to admit a join — it is the live-join evidence, not a mere read-model. The
endpoint therefore signs, on demand, room-authority assertions that other nodes trust
for access; it is an **authorization surface**, governed default-deny by the room's
exposure mode, not an open query. This one rule resolves CR-87/CR-88 findings P1-I
(TTL inconsistency), P1-J (endpoint auth), P2-9 (rate-limit/dedup), and P2-10 (audit).

- **Authentication (default-deny), three request modes.** Unauthenticated requests are
  denied, and the endpoint never reveals whether a room or subject exists beyond what the
  requester is entitled to learn. The request MUST present a room-scoped authorization
  claim whose `kind`, subject, room id, grants, and expiry are validated by this surface;
  deployments that expose the endpoint beyond the local trusted service boundary MUST
  back that claim with the shared `capability.passport.verify` / capability-binding
  verifier. The authorization *kind* bounds what it may obtain:
  - **invitee first-join** — an invitee presenting the room-scoped **invitation** passport
    the authority already issued obtains a *self-scoped* attestation sufficient for its
    first join. This breaks the chicken-and-egg loop: you need not already be a member to
    attest the membership the invitation grants.
  - **member self-attestation** — an existing member, with its membership/capability
    passport, attests only its own membership and grants.
  - **authority roster attestation** — the room authority (or a delegated role) attests
    another subject or the roster, within the disclosure scope below.

  (Same INAC material as join, Solution 017/014; the invitation mode is what keeps the
  first legal join reachable.)
- **Wire surface.** Runtime issuance is a `POST` with an explicit request body:
  `POST /v1/agora/projections/rooms/{room_id}/membership-attestation` carrying
  `room-membership-attestation-request.v1`. The path room id and request room id must
  match. The old `GET /v1/agora/projections/rooms/{room_id}/membership-attestation`
  query surface is deprecated and may return `410 Gone`; no compatibility guarantee is
  required at this stage.
- **Disclosure scope by role.** A member MAY attest only its own membership/grants; the
  room authority (or a delegated role) MAY attest the roster. For `private-to-swarm`
  and `federation-local` rooms, other members' presence is not disclosed to a
  non-authority requester, and a closed-room roster is never enumerable by a non-member.
- **TTL cap by exposure** (replaces any flat cap; the endpoint MUST reject a requested
  TTL above the cap):

  | Exposure | Max attestation TTL |
  |---|---|
  | `private-to-swarm` | 60 s |
  | `federation-local` | 300 s |
  | `cross-federation` | 900 s |
  | `global` | per federation policy, default 900 s |

  Any membership-changing record invalidates cached attestations for the affected room
  (revocation freshness beats TTL). These are *policy* caps applied by the endpoint; the
  pure `room-core` enforces one absolute *technical* max that MUST be ≥ the largest
  per-exposure cap above. Decision: raise `ROOM_ATTESTATION_MAX_TTL_SECONDS` to `900 s`
  when implementing this phase, so the core can carry the documented
  `cross-federation` / `global` rows while endpoint policy still applies lower caps for
  private and federation-local rooms.
- **Rate-limit and dedup.** Requests are rate-limited per requester and per room, and
  identical `(room, subject, requested-grants, high-water)` requests are deduplicated,
  so the endpoint cannot be used as a signing-work amplifier.
- **Audit.** Every issued attestation and every refusal is an operator-visible audit
  fact. `room-attestation-audit.v1` carries `requester/subject`, `room/id`,
  `subject/ref`, `requested/grants`, `decision`, `reason/code`, `exposure`,
  `ttl/requested`, `ttl/granted`, `projection/high-water`, and `attestation/ref` when
  issued. It never carries payload or passport bodies. `agora-service` persists these
  facts in its local attestation audit store and exposes the recent read model through
  `GET /v1/agora/operator/room-attestation-audit` for operator inspection.

The same policy applies wherever the endpoint is hosted, **including `agora-service`**:
that surface MUST adopt the per-exposure TTL cap (resolving the room-core 60 s vs
`agora-service` 3600 s divergence), the passport auth gate, the rate-limit, and the
audit trail before it is reachable outside fixtures.

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
13. run the same WSS and Matrix adapter scenario independently and assert equal
    admission/revocation/cleanup outcomes without merging their carrier histories;
14. restart the authority node mid-deliberation and assert durable projection recovery
    without live-message recovery;
15. measure non-functional bounds: revoke latency, cleanup time, and projection rebuild
    time.

## Implementation Recommendations

The durable snippets below are Room content payloads embedded in a signed
`agora-record.v1`. The Agora envelope owns `author/participant-id`, optional nym or key
delegation proof, `record/id`, and `signature`; Room payloads do not duplicate those
fields.

`room.v1` (durable Room payload; signed by the enclosing Agora record):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "opener/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "authority/subject": { "kind": "nym", "id": "nym:did:key:..." },
  "policy/ref": "room-policy:<digest>",
  "seq/no": 0,
  "created-at": "2026-06-23T10:00:00Z",
  "expires-at": "2026-06-23T10:30:00Z"
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
  "created-at": "2026-06-23T10:01:00Z"
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
  "created-at": "2026-06-23T10:01:05Z"
}
```

`room-live-message.v1` (ephemeral wire schema: validated on the live plane, but not
signed-as-fact and not persisted by the protocol; a member may locally capture it):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "from/subject": { "kind": "nym", "id": "nym:did:key:P1" },
  "nonce": "uYV3foRz3LeLwz5N5Jp3ew",
  "seq/no": 14,
  "size/bytes": 3,
  "content/type": "text/markdown",
  "content": "..."
}
```

The live plane validates each frame (schema, `size/bytes` against a configured max,
monotonic per-sender `seq/no` for ordering and replay suppression) and binds
`from/subject` to the authenticated WSS session outside the payload. Validation is not
persistence: accepted frames are never written to the durable skeleton.

`room-relay-endpoint.v1` (durable Room payload; signed by the enclosing Agora
record):

```json
{
  "schema/v": 1,
  "room/id": "room:<authority>:<id>",
  "seq/no": 18,
  "relay/epoch": 3,
  "relay/subject": { "kind": "node", "id": "node:<id>" },
  "relay/placement": "room-member",
  "endpoint/url": "wss://relay.example.org/room-live",
  "crypto/profile": "member-visible-tls-v1",
  "ordering/profile": "relay-total-order-v1",
  "selection/evidence-refs": [
    "node-advertisement:sha256:<digest>",
    "node-address-attestation:sha256:<digest>"
  ],
  "issued-at": "2026-07-17T10:00:00Z",
  "expires-at": "2026-07-17T10:30:00Z",
  "authority/subject": { "kind": "nym", "id": "nym:did:key:..." }
}
```

`seq/no` orders the durable endpoint fact with other Room facts. `relay/epoch` selects
the carrier generation, while replacement lineage uses the enclosing Agora record's
`record/supersedes`. The WSS delivery header separately adds `relay/seq-no`; it wraps
the already validated payload and is never signed or persisted as a Room fact. The
exact `room-relay-delivery.v1` schema covers ordinary live
messages, P082 latest-state snapshots, and P083 control/receipt payloads without
turning one payload family into another. A receiver recomputes `payload/digest` from
the canonical payload and validates the exact payload schema before advancing its
relay checkpoint or exposing the delivery to a consumer.

Agora topic key: `orbiplex/room/v1/<authority>/<room-id>`; record kinds `room.v1`,
`room-membership.v1`, `room-event.v1`, and `room-relay-endpoint.v1`; consumers fold
them into a membership/lifecycle and carrier
endpoint projection keyed by `room/id` with a per-room high-water `seq/no`.

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
  coverage, and `room-policy.v1`, `room-membership-attestation.v1`,
  `room-membership-attestation-request.v1`, and `room-attestation-audit.v1` schemas are
  mirrored into node schema-gate contracts with positive/negative examples. Dedicated
  helper APIs now validate `room-policy.v1` import/export,
  `room-live-message.v1` ingress/egress, `room-membership-attestation.v1` export,
  `room-membership-attestation-request.v1` ingress, and `room-attestation-audit.v1`
  export, while Agora content ingress accepts durable policy and attestation
  publication.

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
  `POST /v1/agora/projections/rooms/{room_id}/membership-attestation`.
  The deprecated `GET` attestation surface returns a deprecation response instead of
  minting a credential. The POST path validates `room-membership-attestation-request.v1`,
  applies the three request modes, signs canonical attestation bytes through the host
  signer under `room-membership-attestation.v1`, and records
  `room-attestation-audit.v1` facts. The shared `room-core` contract bounds subject
  identifiers, signer refs, signature values, durable digest inputs, local clock-skew
  tolerance, and attestation TTL; it also normalizes requested grants before membership
  checks and signing.
- [x] Consume P081 scoped nym claims at one live admission boundary without making
  claim verification membership authority. `room-service` schema-gates and verifies a
  paired scoped request/presentation through the shared durable runtime, binds the
  evidence to `room-membership-admission`, the exact room id, the joining nym, and a
  current-certificate claim, then calls independent local policy and the existing live
  transport authorization. Tests prove a valid proof can still be denied by Room policy.

### Phase 2 — Live transport contract

- [x] Define `room-live-message.v1` and the transport contract (auth via room-scoped
  passport, revocation drop, presence, retry, expiry, cleanup, sequence). The schema
  exists and `room-core` now owns the typed live-frame DTO, room-scoped passport
  projection gate, join/send/drop/close/cleanup contract, per-sender `seq/no`
  duplicate suppression, 256-bit CSPRNG bearer sessions, bearer-free frame/fan-out
  projection, and shared conformance tests.
- [x] Implement the WSS baseline and Matrix bridge with enforced
  non-retention/redaction. Both adapters satisfy the same auth, revocation, sequencing,
  expiry, cleanup, and retention boundary without sharing carrier-history semantics.
  `room-wss` provides the bounded WebSocket pub/sub adapter over the shared Room live
  contract, including pre-parse frame limits. `agora-matrix-client` provides the
  optional Matrix bridge over `MatrixEventSink`, including bounded subscriptions,
  oversized event refusal before JSON projection, and close/expiry redaction with
  idempotent cleanup.
- [x] Expose the P082 WSS Room `latest-state` projection as a dedicated
  read-only carrier session. The adapter intersects current Room `observe`
  rights with current Sensorium Interface grantees, coalesces to one latest
  snapshot, omits source cursors, refuses ordered-event interfaces, and closes
  only the projection session on source or authority termination.
- [x] Expose P083 collaborative actuation through the explicit `actuate` grant.
  The daemon derives the canonical caller and current Room membership atomically
  from one live-transport snapshot, and then intersects them with the exact actuation
  grant, method, generation, lease, epoch, sequence, and host policy. Grouping
  remains process-local and bounded to 64 entries; terminal input never becomes a
  Room message. Withdrawal releases the active slot immediately, closed or terminal
  Rooms are reaped before group access or inspection, and a single member-session
  disconnect does not destroy the Room-scoped group.

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

### Phase 5 — Attestation Endpoint Policy enforcement

The previous service-authenticated `GET` query is deprecated. Runtime issuance now
uses `room-membership-attestation-request.v1` over POST and treats attestation minting
as an authorization surface.

- [x] Passport-shaped room authorization with the three request modes (invitee
  first-join, member self-attestation, authority roster attestation); default-deny
  otherwise. The current `agora-service` endpoint validates the room-scoped
  authorization claim at the local trusted service boundary; deployments exposing this
  outside that boundary must bind it to capability-passport verification.
- [x] Disclosure-scope enforcement by role and exposure (closed-room roster not
  enumerable by a non-authority requester).
- [x] Raise `ROOM_ATTESTATION_MAX_TTL_SECONDS` to `900 s` and enforce the per-exposure
  endpoint caps from the table above.
- [x] Per-requester / per-room rate-limit and `(room, request-mode, subject, grants,
  high-water, ttl)` dedup.
- [x] Define and emit `room-attestation-audit.v1` fact on issue, refusal,
  deduplication, and rate-limit decisions (no payload/passport bodies).
- [x] `agora-service` adopts the same auth gate, TTL caps, rate-limit, and audit before
  the endpoint is reachable outside fixtures.

### Phase 6A — Relocatable member-visible WSS relay

This phase is post-MVP carrier work. It does not reopen the completed durable Room,
membership, attestation, or node-local live-plane contracts.

- [x] Freeze `room-relay-endpoint.v1`, its positive/negative fixtures, Agora-envelope
  signing profile, monotonic epoch and supersession rules, and the ephemeral relay
  delivery header carrying `(relay/epoch, relay/seq-no)`. Reuse
  `node-advertisement.v1` relay endpoints and `node-address-attestation.v1` as bounded
  selection evidence rather than registering an ambient relay capability. Extend
  `room-event.v1` with closed authority-delegation scopes including `relay/manage`,
  bounded expiry, and explicit revocation linkage; synchronize schema-gate, Node
  mirrors, implementation ledger, and generated schema documentation. Implemented by
  the canonical endpoint/delivery schemas, closed `relay/manage` delegation fields,
  synchronized Node mirrors, and schema-gate ingress/egress checks.
- [x] Add a pure endpoint projection and selection evaluator. It must prefer requester,
  relay-capable member, then federation service; reject same-epoch conflicts; and never
  treat reachability or presence as authority. It must also reject endpoint facts from
  an ordinary relay-capable member, an expired delegation, or a revoked delegation.
  Before dialing, it must require exact endpoint/subject/evidence matching plus
  host-owned egress and Node Transport trust admission. Within one candidate class it
  uses advertisement priority, canonical subject id, and canonical endpoint URL as
  deterministic tie-breaks. `room-core` now owns this evaluator, same-epoch conflict
  refusal and strictly-newer-epoch recovery, explicit trusted-clock evaluation with the
  five-second default skew bound, canonical Room topic binding, and exact dial
  admission. Durable Agora replay proves that a same-epoch conflict remains fail-closed
  until a newer endpoint epoch restores an active projection.
- [x] Add host-owned configuration and operator diagnostics for enabled placement
  classes, advertised endpoint, active epoch, crypto profile, connected-session count,
  bounded replay occupancy, reconnects, cursor expiry, last failover, and degraded
  reason. Diagnostics contain no live payload or sealed key material. Daemon
  `room_relay` configuration materializes these bounded controls and Corpus status
  exposes per-Room metadata-only relay diagnostics. The WSS adapter enforces and
  reports a hard per-Room relay-connection cap even when one Room bearer is reused;
  degraded reasons come from a closed runtime vocabulary rather than caller strings.
- [x] Make the existing `room-wss` server deployable behind the host-owned TLS/WSS
  listener on TCP 443, with bounded approximately 25-second keepalive, jittered
  reconnect, epoch-aware cursor resubscription, replay-window caps, and current-state
  refresh after `cursor-expired`. The adapter advertises the host-owned `wss://`
  endpoint while retaining a bounded local handler behind TLS termination; its
  persistent client implements keepalive, jittered reconnect, and typed resume. Client
  admission rejects Room rebinding, cursor rollback, and every non-increasing
  `epoch-changed` checkpoint before it can replace local resume state.
- [x] Deliver newer endpoint facts independently of the old relay through Agora replay
  and Artifact Delivery mailbox fallback, then recover the selected epoch and relay
  sequence checkpoint without restoring live payload content. Agora replay and the
  dedicated Artifact Delivery `agora-record.v1` mailbox acceptor converge on one pure
  projection; the acceptor verifies exact kind/schema, signature, and canonical topic,
  rejects unknown or unopened Rooms without buffering, and has pure boundary tests.
  Checkpoint storage is metadata-only and restored gaps force refresh. Room-service
  rechecks close and monotonic projection state after transport I/O before committing
  the refreshed projection and endpoint source.
- [x] Add the P083 relay carrier for status, claim, control, invoke, and receipt messages
  without changing grant, source-generation, lease, epoch, sequence, idempotency, or
  host-policy checks. Keep authenticated direct peer as an optional latency upgrade.
  `room-relay-delivery.v1` binds each class to its exact Sensorium schema and filters
  observation versus actuation visibility from current Room grants. The shared
  `sensorium-status` carrier class additionally distinguishes observation status from
  actuation/control status by its exact schema ref, so `observe` cannot disclose P083
  control state. P082 pumps emit a validated resource-bound
  `sensorium-interface-read-result.v1` with one inline latest-state snapshot into
  an active epoch without exposing source cursors.
- [x] Add an outbound-only three-node acceptance profile proving initial relay
  placement on the requester or another content-visible member, relay failure, endpoint
  update through AD, new-epoch recovery without cross-epoch merge, membership
  revocation, and P082 latest-state plus P083 fenced invocation over the same relay. It
  must also refuse an endpoint fact authored by an ordinary relay-capable member and by
  an expired or revoked `relay/manage` delegate, a mismatched evidence ref, a disallowed
  egress target, and every old-epoch frame after failover. The `phase6a_relay`
  acceptance target covers all listed positive and refusal paths over requester,
  relay-member, and observer nodes.
- [x] Collect executable POSIX Phase 6A deployment evidence through an actual host-owned TLS
  terminator and separate relay, publisher, and observer processes. The feature-gated
  Node profile supplies its private trust root explicitly at the host boundary, carries
  P082 latest-state and P083 invoke payloads over one WSS relay, and binds the crypto
  provider per TLS config without changing process-global rustls state. The terminator
  reaps completed connection tasks and aborts outstanding tasks at shutdown. The profile
  forces bounded replay expiry followed by current-state refresh, distinguishes recovery
  from a real reconnect in diagnostics, restores metadata-only checkpoints after an
  unclean stop, separately proves graceful final-checkpoint persistence, performs
  strictly-newer-epoch failover, revokes an active member session, and refuses a payload
  whose canonical digest no longer matches. The networked publisher validates the
  host-minted 256-bit bearer shape and refuses any delivered frame containing its
  `session/ref`; the runner also rejects retained evidence containing a bearer key or
  value. Its local report contains only
  bounded timings, counters, and outcomes; fixture keys, attestations, session refs, and
  payloads are deleted or omitted. The loopback smoke uses an ephemeral TLS port, while
  the reference deployment terminates public WSS at the host listener on TCP 443.

### Phase 6B — Non-member federation relay profile

This phase enables the all-members-behind-CGNAT case without admitting the relay
service to Room content. It is intentionally sequenced after Phase 6A proves endpoint
selection and failover independently of group encryption.

- [x] Implement `sealed-sender-key-v1` only for non-member federation relays, with
  pairwise sealed sender-key distribution, sender-authenticated encrypted frames, O(n)
  membership-change fan-out per active sender, metadata-leakage disclosure, and no
  forward-secrecy or PCS claim. `room-core` now owns the pure distribution, frame,
  replay, rotation, and fencing contracts; schema-gate validates both Phase 6B wire
  families. Member-visible and sealed deliveries carry distinct required
  `delivery/kind` values, so `room-wss` dispatches the opaque union by an explicit
  discriminator rather than trial deserialization, without receiving keys. A
  between-crate test also requires every payload-class schema ref accepted by
  `room-core` to remain registered in schema-gate. A dedicated transition lock
  linearizes projection refresh, relay rotation, publication, resume, close, and
  cleanup across the membership/carrier state boundary. The common activation boundary
  rejects `sealed-sender-key-v1` with an absent or zero membership epoch, and rejects a
  membership epoch on `member-visible-tls-v1`, before it creates or mutates relay state.
  A membership projection refresh is the host-side rotation trigger; sender clients then
  own fresh key generation and recipient-private redistribution from that same projection.
- [x] Extend the outbound-only acceptance profile with an external federation relay and
  no publicly reachable Room member. Prove initial key distribution, join/leave/revoke
  rotation, refusal of old-epoch ciphertext, bounded recovery, and that the relay audit
  exposes metadata only and never plaintext or key material. The Phase 6B acceptance
  now combines the exact in-process contract scenario with a separate multiprocess
  deployment profile. Two successive non-member relay processes expose actual local
  WebSocket endpoints behind host-owned TLS, while one-shot member processes connect
  outbound. The profile proves initial distribution, join, `RoomMembershipOp::Leave`,
  revoke, refusal after every stale membership epoch, revoked-session refusal, bounded
  O(n) fan-out, sealed-client reconnect from an authenticated checkpoint, metadata-only
  checkpoint restart, and failover to a strictly newer `relay/epoch` without cross-epoch
  replay merge. It emits a 21-check redacted report plus a separate relay audit capped
  at 64 transition records. Status, audit, and report must first match closed
  metadata-only field allowlists; recursive sensitive-key and private-marker scanning
  remains defense-in-depth evidence rather than the canonical redaction mechanism.

## Open Questions

No unresolved question blocks Phase 6A or Phase 6B. MLS, QUIC, and direct-pair hole
punching are explicit evidence-gated future profiles, not implementation choices inside
the relocatable relay baseline.

## Next Actions

1. Accumulate evidence from non-loopback host-TLS deployments and compare repeated
   reconnect, cursor-expiry, revocation, and failover observations before changing any
   operational bound. The local POSIX deployment-evidence profile proves the mechanism; its
   timings are not a production SLO or a reason to tune defaults from one machine.
2. Keep direct peer an optional latency adapter; do not move membership, grants,
   leases, or source cursors into either carrier.
3. Collect non-member relay observations at realistic Room sizes before replacing the
   bounded O(n) sender-key distribution profile. MLS or another tree profile requires
   measured pressure plus a separate contract, implementation, and security review.
