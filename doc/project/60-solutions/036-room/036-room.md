# Room

Based on:

- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/079-cross-federation-alliance.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
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

## Status

Implemented solution foundation.

This means the functional Room foundation is present: durable records,
deterministic projection, membership attestation, and live transport substrates.
It does not mean the implementation has no known hardening follow-ups. The
CR-88/CR-89 hardening stream remains the place for issues such as clock-skew
tolerance review, session-ref collision checks, subscription-count DoS limits,
pre-validation sink behavior, and stricter `room/id` validation.

## Date

2026-06-25

## Executive Summary

Room is the generic subject-addressed collaboration primitive for Orbiplex. It
replaces bespoke answer-room and association-room shapes with one durable record
family, one deterministic projection model, and one live transport contract.

The durable plane is Agora-addressed and replayable. The live plane is
non-retentive and carrier-agnostic: bounded WebSocket pub/sub and Matrix are
implementation substrates of the same Room live contract, not separate room
semantics.

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

- `done` for the functional foundation; security hardening remains tracked in
  CR-88/CR-89.

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
- keep bounded WebSocket and Matrix adapters behaviorally equivalent under
  conformance tests.

Status:

- `done` for the functional foundation; security hardening remains tracked in
  CR-88/CR-89.

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

- `in-progress`: Corpus policy, signed invitations, AD admission, and the durable
  local join/readiness control plane are implemented. Connecting admitted
  participants to a concrete bounded Room live-carrier session and propagating
  authority-visible presence remain open.

## Out of Scope

- owning Corpus reasoning or answer synthesis;
- owning procurement, settlement, contribution allocation, or payment;
- treating live messages as archival facts by default;
- bypassing durable room membership projection with live transport credentials;
- adding a third live transport semantics for a specific domain flow.

## Consumes

- Agora durable record pages;
- INAC or membership-attestation authorization material;
- room policy profiles;
- host signing for membership attestations.

## Produces

- deterministic room membership projections;
- signed membership attestations;
- metadata-only attestation audit facts;
- bounded non-retentive live room messages;
- Room projections for former answer-room and association-room flows.

## Related Capability Data

- `036-room-caps.edn`
