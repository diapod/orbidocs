# Corpus

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/067-shared-offer-catalog-over-agora.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/036-room/036-room.md`

Related schemas:

- `topic-taxonomy.v1`
- `topic-resolution.v1`
- `corpus-reasoning-query.v1`
- `corpus-reasoning-bid.v1`
- `corpus-reasoning-bid-state.v1`
- `corpus-reasoning-answer.v1`
- `service-offer.v1`
- `procurement-offer.v1`
- `procurement-contract.v1`
- `room.v1`
- `room-policy.v1`
- `room-membership-attestation.v1`
- `agent.binding.v1`
- `agent.outcome.v1`
- `corpus-chair-admission.v1`
- `corpus-agent-answer-draft.accept.request.v1`
- `corpus-agent-answer-draft.v1`
- `classification.v1`

## Status

Implemented solution foundation.

The hard-MVP procurement slice is implemented and accepted as the solution-level
contract for topic-routed collaborative reasoning. Live deliberation on Room and
its policy/invitation layer remain post-MVP. The bounded Agent-backed chair join
and inert Corpus answer-draft acceptance are implemented foundations; they do not
yet authorize final answer signing or publication.

## Date

2026-07-15

## Executive Summary

Corpus is the topic-routed collaborative reasoning component. It lets a node
resolve a question into a governed topic, discover providers advertising
Corpus competence on that topic, broadcast a bounded reasoning query, collect
signed bids, and bridge the selected offer into the ordinary procurement path.

Corpus does not replace the offer catalog, Artifact Delivery, Room, Inquirium,
or Agent. It composes them:

- topic taxonomy and resolution name the problem space;
- Shared Offer Catalog indexes Corpus-capable `service-offer.v1` records;
- Artifact Delivery carries query/bid/answer envelopes;
- procurement contracts settle selected work;
- Room and Agent provide the later live deliberation surface.

The durable output of Corpus reasoning is the signed answer and its traceable
provenance. Live room chatter is not a protocol fact unless another component
explicitly stores it under its own policy.

## Context and Problem Statement

Orbiplex already had marketplace procurement, offer catalog projection, Artifact
Delivery, Room, Inquirium, and Agent building blocks. What was missing was the
thin coordination protocol that turns "I need an answer about this topic" into:

1. deterministic topic resolution;
2. provider discovery by topic;
3. bounded query broadcast;
4. signed bid collection;
5. selected procurement;
6. optional live deliberation and final answer acceptance.

Without Corpus, each story would have to glue these strata ad hoc, creating
parallel query, topic, room, pricing, and answer semantics.

## Proposed Model / Decision

Corpus is a role plus protocol layer. It is not a separate marketplace
authority and it is not a model runtime.

The hard-MVP path is procurement-oriented:

```text
question keywords
  -> topic-resolution.v1
  -> Shared Offer Catalog topic index
  -> corpus-reasoning-query.v1 over Artifact Delivery
  -> corpus-reasoning-bid.v1 responses
  -> corpus-reasoning-bid-state.v1 requester projection
  -> selected procurement-offer.v1
  -> procurement-contract.v1 / receipt path
```

The post-MVP path adds live deliberation:

```text
selected participants
  -> room.v1 + corpus-reasoning-room-policy.v1
  -> live Room transport
  -> Agent/Inquirium-backed participant reasoning
  -> corpus-reasoning-answer.v1
```

Corpus wire contracts reuse existing money, procurement, classification,
canonical JSON, and Room conventions. It does not introduce a Corpus-specific
canonicalization profile or a new settlement rail.

## Must Implement

### Topic Taxonomy and Resolution

Based on:

- `doc/project/40-proposals/069-corpus.md`

Related schemas:

- `topic-taxonomy.v1`
- `topic-resolution.v1`

Responsibilities:

- define a signed, versioned, federation-scoped taxonomy artifact;
- resolve keywords to a canonical topic term or explicit ambiguity;
- keep resolution deterministic and auditable;
- reject arbitrary topic strings that do not belong to the pinned taxonomy.

Status:

- `done`

### Corpus-Capable Offer Indexing

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md`

Related schemas:

- `service-offer.v1`
- `topic-taxonomy.v1`

Responsibilities:

- treat Corpus provider offers as normal `service-offer.v1` records with a
  Corpus extension;
- index active offers by canonical topic term and taxonomy digest;
- apply supersession, full withdrawal, expiry, and partial-topic removal as
  offer-catalog read-model rules;
- expose topic-index query surfaces without making Corpus a second catalog.

Status:

- `done`

### Query, Bid, and Bid-State Flow

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `corpus-reasoning-query.v1`
- `corpus-reasoning-bid.v1`
- `corpus-reasoning-bid-state.v1`
- `question-envelope.v1`
- `procurement-offer.v1`

Responsibilities:

- send Corpus queries as bounded Artifact Delivery fan-out;
- keep `corpus-reasoning-query.v1` as a decorator over `question-envelope.v1`;
- represent bids as signed envelopes around `procurement-offer.v1`;
- keep requester bid state as a local read model so silence, refusal, policy
  denial, timeout, and delivery failure are not conflated.

Status:

- `done`

### Procurement Bridge

Based on:

- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/069-corpus.md`

Related schemas:

- `procurement-offer.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:

- convert a selected Corpus bid into the ordinary procurement contract path;
- keep price, currency, unit, contract, and receipt semantics owned by
  procurement;
- reject counter prices outside the query bracket unless explicitly selected
  by the requester;
- preserve query and correlation identifiers through the settlement path.

Status:

- `done`

## May Implement

### Live Deliberation on Room

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/036-room/036-room.md`

Related schemas:

- `room.v1`
- `room-policy.v1`
- `corpus-reasoning-room-policy.v1`
- `corpus-reasoning-room-invite.v1`
- `corpus-reasoning-answer.v1`

Responsibilities:

- open a Room for selected Corpus participants;
- bind deliberation policy, access list, role assignments, and answer
  acceptance to Room records;
- keep live chat ephemeral by default;
- emit a signed, content-addressed answer as the durable reasoning artifact.

Status:

- `post-MVP`

### Agent-Assisted Chairing

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`

Related schemas:

- `agent.binding.v1`
- `agent.outcome.v1`
- `room-membership-attestation.v1`
- `corpus-chair-admission.v1`
- `corpus-agent-answer-draft.accept.request.v1`
- `corpus-agent-answer-draft.v1`
- `corpus-reasoning-role-assignment.v1`
- `corpus-reasoning-instruction-overlay.v1`
- `corpus-reasoning-answer.v1`

Responsibilities:

- allow the requester to appoint its own bounded Agent as chair delegate;
- require a pre-existing local Corpus round and signed, fresh Room evidence from
  that round's node-local authority, with a canonical Ed25519 `did:key` signer;
- keep the accountable chair subject explicit in Room policy;
- let Agent/Inquirium assist reasoning without becoming the authority root;
- admit the terminal Agent product only as an inert, content-addressed Corpus
  answer draft through local-control authority, strict embedded-evidence schema
  validation, and actor-bound idempotent replay, with publication authority fixed
  false;
- route sensitive effects through host-owned human-in-loop gates.

Status:

- `done` for the bounded chair binding and answer-draft acceptance foundation;
  Room policy, invitations, remote authority trust, and final-answer
  signing/publication remain post-MVP.

## Out of Scope

- owning the curated/training `corpus-entry.v1` corpus;
- replacing Room membership, presence, live transport, or attestation;
- replacing Inquirium or Agent runtime semantics;
- defining N-way contribution settlement;
- persisting live deliberation chatter as a protocol fact by default.

## Consumes

- topic taxonomy artifacts;
- Corpus-capable offer catalog projections;
- Artifact Delivery delivery results;
- procurement offer/contract/receipt records;
- Room membership and policy records for post-MVP deliberation.

## Produces

- topic resolution records;
- Corpus query and bid records;
- requester bid-state projections;
- selected procurement bridges;
- Corpus answer records in the live-deliberation layer.

## Related Capability Data

- `038-corpus-caps.edn`
