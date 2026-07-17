# Room

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/079-cross-federation-alliance.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `room.v1`
- `room-membership.v1`
- `room-event.v1`
- `room-policy.v1`
- `room-live-message.v1`
- `room-membership-attestation.v1`
- `room-membership-attestation-request.v1`
- `room-attestation-audit.v1`
- `room-relay-endpoint.v1`
- `room-relay-delivery.v1`

## Status

Implemented solution through the member-visible relocatable relay profile.

This means the hard-MVP Room foundation is present: durable records,
deterministic projection, membership attestation, and node-local live transport
substrates. The relocatable member-visible WSS relay defined by P070 Phase 6A is
implemented; the Phase 6B non-member federation relay and its sealed-sender-key
profile remain post-MVP work, so the solution is not yet complete for every
all-members-behind-CGNAT deployment.
The CR-88/CR-89 hardening stream remains the place for issues such as clock-skew
tolerance review, subscription-count DoS limits, pre-validation sink behavior, and
stricter `room/id` validation. Live session refs are already 256-bit CSPRNG bearer
secrets and are excluded from message payloads, acknowledgements, fan-out delivery,
member-visible status, durable Room facts, and shared Corpus observations.

## Date

2026-06-25

## Executive Summary

Room is the generic subject-addressed collaboration primitive for Orbiplex. It
replaces bespoke answer-room and association-room shapes with one durable record
family, one deterministic projection model, and one live transport contract.

The durable plane is Agora-addressed and replayable. The live plane is
non-retentive and carrier-agnostic. Bounded WebSocket pub/sub is the production
baseline once its endpoint becomes relocatable by signed relay epochs; Matrix is an
optional bridge adapter under the same Room authority contract, not a separate room,
ordering, or history semantics.

Room is not a reasoning engine, procurement system, or chat transcript archive.
It gives higher-level components a stable membership, policy, attestation,
presence, and live-message substrate.

## Context and Problem Statement

Several Orbiplex flows need bounded groups of participants around one subject:

- collaborative answers,
- association and relationship proposals,
- Corpus deliberation,
- invitation-only or closed exchanges,
- low-retention live coordination.

Without a generic Room primitive, each flow would invent its own membership
records, live transport admission, roster visibility rules, close/expiry
behavior, and attestation surface. That would duplicate authority logic and make
federated replay hard to audit.

## Proposed Model / Decision

Room has two planes.

The durable plane records signed facts:

- `room.v1` opens and describes the room subject, opener, policy, lifecycle, and
  authority root.
- `room-membership.v1` changes role and membership state.
- `room-event.v1` records durable lifecycle or domain events.
- `room-policy.v1` freezes exposure, access, TTL, and profile constraints.

The live plane carries bounded non-retentive messages:

- `room-live-message.v1` is validated by the room live contract.
- Join, send, drop, close, and cleanup are guarded by room-scoped passport or
  membership attestation.
- The host returns a random bearer session ref only to the joining client; subsequent
  carrier admission binds the payload's subject outside the frame, so no shared
  projection needs or receives the bearer.
- Durable projection membership remains decisive, so stale live credentials
  cannot override revoked or expired membership.

Membership query is an authorization surface. Runtime issuance uses
`room-membership-attestation-request.v1` over POST and returns signed
`room-membership-attestation.v1`; issue, refusal, deduplication, and rate-limit
decisions emit `room-attestation-audit.v1` facts without leaking passport bodies.
The attestation signer is represented as a canonical Room subject carrying one
base58btc Ed25519 `did:key`; consumers validate the multicodec and key length
before signature verification. Cryptographic validity proves possession only.
The consuming composition root must still join `signer/ref` to its trusted Room
authority policy before treating the attestation as admission authority.

### Federation Exposure Boundary

Room's exposure vocabulary is grounded in Proposal 076's node-level federation
selector.

- `federation-local` means the room is scoped to subjects whose relevant node,
  service, or authority material resolves under the same active `federation_id`
  selected from the local `federation-root.v1` pack.
- `cross-federation` means participants or services rooted in different
  `federation_id` values cooperate through an explicit higher-layer admission
  policy. It is not inferred merely because a carrier, Matrix homeserver, Seed
  Directory, or relay can reach both sides.
- `alliance-policy.v1` (Proposal 079) is one possible cross-federation
  admission input for Room. It does not grant membership by itself; Room still
  verifies room policy, membership projection, attestations, and live
  credentials.
- `global` remains an explicit publication/exposure decision above Room's
  durable membership projection. It is never the default fallback for an
  unknown or missing federation selector.

This keeps Room carrier-neutral: bounded WebSocket, Matrix, and future live
substrates may carry room traffic, but they do not define Orbiplex federation
authority. The active federation root defines the local authority context; Room
policy decides how, and whether, another federation is admitted.

### Relay Liveness Boundary

Production Room liveness requires exactly one reachable WSS/TLS endpoint per active
relay epoch, not one public listener per member. All participants may use outbound
WSS over TCP 443. The authority selects requester, another relay-capable member, or a
federation relay service through a signed `room-relay-endpoint.v1` fact.

One relay epoch has one monotonic ephemeral carrier order. Failover starts a new
epoch; clients refresh from durable Agora facts and domain read-models rather than
merging carrier histories. The relay validates admission evidence and bounds only.
It does not own membership, policy, grants, presence truth, Sensorium Interface
authority, or P083 leases. Room remains durably open while no relay is reachable.

## Must Implement

### Durable Room Record Family

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/60-solutions/008-agora/008-agora.md`

Related schemas:

- `room.v1`
- `room-membership.v1`
- `room-event.v1`
- `room-policy.v1`

Responsibilities:

- define subject-addressed room identity and lifecycle;
- publish durable room records into Agora-addressed topics;
- preserve signer authority, sequence ordering, high-water sequence, and expiry;
- validate room policy profiles and exposure fields;
- keep durable facts replayable into the same projection on different nodes.

Status:

- `done`

### Membership Projection and Attestation

Based on:

- `doc/project/40-proposals/070-room-primitive.md`

Related schemas:

- `room-membership.v1`
- `room-membership-attestation.v1`
- `room-membership-attestation-request.v1`
- `room-attestation-audit.v1`

Responsibilities:

- compute deterministic membership and lifecycle projections from durable
  records;
- expose bounded authenticated room projection queries;
- issue signed membership attestations for invitee first-join, member
  self-attestation, and authority roster attestation modes;
- expose one shared consumer-side verifier for canonical signature-domain,
  schema, grant uniqueness, TTL, clock-skew, and freshness checks, so higher
  layers do not reimplement Room credential admission;
- require each consumer to join that cryptographic verification with an
  explicit trusted Room authority; a valid self-signature alone is not issuer
  authorization;
- enforce TTL caps, exposure-aware disclosure rules, deduplication, and
  per-requester/per-room rate limits;
- record metadata-only audit facts for attestation issue and refusal;
- enforce the implemented TTL model: the core technical maximum is 900 seconds;
  endpoint policy caps private-to-swarm rooms at 60 seconds,
  federation-local rooms at 300 seconds, and cross-federation/global rooms at
  900 seconds unless a stricter federation policy applies.

Status:

- `done` for the functional foundation. The WSS carrier now returns explicit
  accepted/replayed acknowledgements, suppresses exact replay redelivery, and can
  restore validated subject-scoped sequence checkpoints after host restart. Its
  parser enforces a bounded wire-message limit before JSON decoding, and Corpus
  recovery consumes Room projections in fixed-high-water pages rather than an
  unbounded or silently truncated startup read.
  Security hardening remains tracked in CR-88/CR-89.

### Live Room Transport

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`

Related schemas:

- `room-live-message.v1`
- `room-membership-attestation.v1`

Responsibilities:

- define a carrier-neutral live-frame contract;
- admit live joins and sends only through room-scoped passport or membership
  attestation;
- enforce per-sender sequence duplicate suppression and bounded frame size;
- drop revoked or expired participants;
- support close/expiry cleanup and non-retention/redaction requirements;
- keep bounded WebSocket and Matrix adapter admission, revocation, bounds, and cleanup
  outcomes equivalent under conformance tests without merging carrier histories;
- let P082 attach a dedicated read-only WSS `latest-state` projection whose
  authority is the intersection of current Room `observe` rights and current
  Sensorium Interface grants, without exposing source cursors or closing the
  durable Room;
- let P083 use the explicit `actuate` grant as collaboration policy for bounded
  status/control/invoke wrappers, deriving session identity and current membership
  atomically from one live-transport snapshot, while exact Sensorium Interface
  grants and fenced leases remain independently mandatory; raw terminal bytes are
  never Room content.

Status:

- `done` for the functional foundation, the P082 latest-state projection, and the
  bounded P083 `actuate` collaboration intersection;
  security hardening remains tracked in CR-88/CR-89.

### Room Consolidation Surface

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/069-corpus.md`

Related schemas:

- `room.v1`
- `room-membership.v1`
- `room-event.v1`

Responsibilities:

- expose historical answer-room state as a Room projection instead of a bespoke
  room type;
- express association-room lifecycle on the shared membership/event family;
- provide the live plane expected by Corpus deliberation without adding a third
  room model.

Status:

- `done`

### Relocatable Federated WSS Relay

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/40-proposals/083-sensorium-interactive-interfaces.md`

Related schemas:

- `room-relay-endpoint.v1`
- `room-relay-delivery.v1`

Responsibilities:

- project the authority-signed active endpoint and monotonic relay epoch from Room
  facts;
- prefer requester, relay-capable member, then federation relay service without
  treating readiness or presence as authority;
- reuse `node-advertisement.v1` WSS relay endpoints plus optional
  `node-address-attestation.v1` and current probe evidence for node candidacy, rather
  than inventing a relay capability id;
- require exact endpoint/subject/evidence matching plus host egress and Node Transport
  trust policy before dialing, so Room authority cannot authorize an arbitrary URL;
  private, loopback, and link-local URLs remain schema-valid for local deployments but
  receive no exemption from those dial-time gates;
- expose the existing WSS runtime through host-owned TLS on TCP 443 with keepalive,
  jittered reconnect, bounded replay, and epoch-aware cursor resubscription;
- distribute endpoint failover independently of the failed relay through Agora and
  Artifact Delivery, rejecting unknown or unopened local Rooms without mailbox
  buffering;
- assign one total ephemeral order per epoch and never merge epochs;
- treat carrier sequence as bounded gap/replay state rather than proof of complete
  delivery, and reject old-epoch frames after supersession;
- support `member-visible-tls-v1` first, then the separately bounded
  `sealed-sender-key-v1` profile for a non-member relay;
- carry P082 latest-state and P083 fenced interaction through the same relay while
  keeping direct peer an optional latency upgrade.

Status:

- `implemented` through P070 Phase 6A. Canonical endpoint and delivery contracts,
  scoped relay delegation, deterministic selection and dial admission, daemon-owned
  configuration, payload-free diagnostics, host TLS termination seam, persistent WSS
  reconnect/resume with a hard per-Room connection cap and client-side epoch rollback
  refusal, receiver-side canonical payload-digest validation before checkpoint
  advancement, metadata-only checkpoints, Agora plus Artifact Delivery endpoint
  ingress, P082/P083 payload classes, exact-schema visibility splitting for observation
  versus actuation/control status, and the outbound three-node failover profile are present.
  Endpoint projection uses an explicit trusted evaluation clock and bounded skew,
  same-epoch conflict carries a typed relay-epoch discriminator and is recoverable only
  through a strictly newer valid epoch, service refresh rechecks close/monotonic state
  after transport I/O, degraded diagnostics use a closed vocabulary, and the
  signature-verifying mailbox boundary is tested without a daemon. Phase 6B non-member
  encryption remains planned post-MVP work.

## May Implement

### Corpus Deliberation Rooms

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`

Related schemas:

- `room.v1`
- `room-policy.v1`
- `room-live-message.v1`
- `corpus-reasoning-room-policy.v1`
- `corpus-reasoning-room-invite.v1`

Responsibilities:

- let Corpus define a domain-specific room policy and invitation layer on top of
  the generic Room primitive;
- preserve Corpus reasoning, chairing, and settlement semantics outside Room
  Core;
- reuse Room live transport rather than adding a Corpus-only chat substrate.

Status:

- `done` for the node-local Corpus composition: signed invitations admit narrowed
  WSS sessions, readiness and message metadata reach the authority, exact replay
  does not redeliver, and endpoint/session/sequence recovery is process-tested.
  P070 Phase 6A now supplies relocatable member-visible WSS/TLS endpoint epochs;
  Phase 6B non-member federation relay encryption remains later work. Matrix is an
  optional bridge profile, not a liveness dependency or second Corpus room semantics.

## Out of Scope

- owning Corpus reasoning or answer synthesis;
- owning procurement, settlement, contribution allocation, or payment;
- treating live messages as archival facts by default;
- bypassing durable room membership projection with live transport credentials;
- making STUN/ICE, hole punching, UDP, QUIC, or Matrix homeserver reachability a Room
  liveness requirement;
- adding a third live transport semantics for a specific domain flow.

## Consumes

- Agora durable record pages;
- Node Transport public WSS/TLS ingress and endpoint reachability;
- signed node advertisements, address attestations, and host egress policy for relay
  candidate admission;
- INAC or membership-attestation authorization material;
- room policy profiles;
- host signing for membership attestations.

## Produces

- deterministic room membership projections;
- signed membership attestations;
- metadata-only attestation audit facts;
- bounded non-retentive live room messages;
- one authority-selected WSS relay endpoint and relay epoch projection;
- Room projections for former answer-room and association-room flows.

## Related Capability Data

- `036-room-caps.edn`
