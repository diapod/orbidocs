# Federated Answer Procurement Lifecycle Artifacts

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`
- `doc/project/40-proposals/005-operator-participation-room-policy-profiles.md`
- `doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`

## Status

Proposed (Draft)

## Date

2026-03-22

## Executive Summary

This proposal defines the missing machine-readable lifecycle artifacts for federated
answer procurement.

The key decision is simple:

1. the same procurement lifecycle should work for `full-node`, `hybrid`, and
   `pod-client` participation,
2. the lifecycle should be expressed as a small set of explicit artifacts rather than
   implicit chat history,
3. collaborative answer rooms and paid single-responder execution should remain
   linkable through shared identifiers instead of becoming separate universes,
4. provenance, settlement, and publication policy should remain visible at the data
   boundary.
5. payment settlement must remain rail-neutral at the protocol core so the project
   does not need to start as a crypto-asset operator.

## Context and Problem Statement

The current corpus already covers most of the conceptual pieces:

- question envelopes and answer rooms,
- exposure modes,
- room policy profiles,
- human-origin semantics,
- transcript monitoring,
- `pod`-backed participation.

What remains underspecified is the concrete lifecycle that moves a request through:

- publication,
- offer collection,
- selection,
- contract formation,
- answer delivery,
- receipt and audit.

Without explicit artifacts:

- different node profiles will improvise incompatible payloads,
- deterministic validation becomes difficult,
- settlement and provenance become chat-convention rather than contract,
- later transcript, archival, and reputation layers inherit ambiguity.

## Goals

- Define a minimal interoperable lifecycle for federated answer procurement.
- Reuse the same artifact set across `full-node`, `hybrid`, and `pod-client`.
- Keep collaborative room mode and price-bound procurement mode linkable.
- Make settlement and receipts explicit.
- Preserve provenance and human-origin semantics at the response boundary.
- Keep the trusted core small enough to be implementable on multiple runtimes.

## Non-Goals

- This proposal does not freeze the exact offer-scoring algorithm.
- This proposal does not define the full reputation backend.
- This proposal does not define the full dispute or appeal workflow.
- This proposal does not define final cryptographic signature container formats.
- This proposal does not mandate on-chain or crypto-native settlement.

## Decision

Orbiplex should adopt five explicit lifecycle artifacts as the v1 procurement core:

1. `question-envelope`
2. `procurement-offer`
3. `procurement-contract`
4. `procurement-receipt`
5. `response-envelope`

These artifacts are sufficient to represent the happy path for:

- collaborative answer discovery,
- narrowing to a selected responder,
- optional paid settlement,
- provenance-rich answer return.

The same `question/id` remains the common thread between room discussion,
procurement, transcript material, and final response.

## Proposed Lifecycle

### 1. `question-envelope`

Purpose:
- publish a signed request on the event layer,
- declare exposure mode and response channel,
- express responder filters and procurement intent,
- open the room-level context for later discussion.

This artifact belongs to the asking side and is the canonical opening move.

### 2. `procurement-offer`

Purpose:
- let an eligible remote responder advertise terms,
- keep price, deadline, answer bounds, and specialization fit explicit,
- attach bounded reputation evidence without requiring the full answer yet.

This artifact lets the asking side compare offers deterministically.

### 3. `procurement-contract`

Purpose:
- record the selected responder and acceptance criteria,
- freeze payment terms and confirmation mode,
- bind the narrower execution path back to the original question and room.

This artifact is the line between offer comparison and accountable execution.

### 4. `procurement-receipt`

Purpose:
- record the outcome of the contract,
- preserve signatures or signature references of relevant actors,
- provide auditable closure for settlement, rejection, cancellation, or expiry.

This artifact is the settlement and audit anchor.

### 5. `response-envelope`

Purpose:
- deliver the accepted answer back to the local node or thin client,
- preserve responder, room, contract, and receipt references,
- surface confidence and human-origin semantics without requiring transcript parsing.

This artifact is the user-facing machine-readable result boundary.

## Identity and Participation Compatibility

The lifecycle must work across participation profiles.

### `full-node`

The asking node is both the user-facing actor and the swarm-facing actor.

### `hybrid`

The asking side may mix local execution with delegated execution, but the lifecycle
artifacts remain the same.

### `pod-client`

The serving node may publish and route on behalf of a hosted user, but the artifacts
must preserve the distinction between:

- serving infrastructure actor,
- hosted participant,
- optional public-facing `nym`.

The artifact model therefore must tolerate delegated gateways without losing identity
semantics.

## Contract Boundaries

### Shared identifiers

At minimum, the lifecycle should keep explicit links among:

- `question/id`
- `room/id`
- `offer/id`
- `contract/id`
- `receipt/id`
- `response/id`

### Policy surfaces

The artifacts should carry enough information to derive or validate:

- exposure mode,
- room policy profile,
- procurement intent,
- confirmation mode,
- human-origin relevance,
- transcript eligibility decisions.

### Settlement neutrality

The lifecycle must keep settlement semantics explicit without requiring one payment
rail.

The v1 rule should be:

- contracts define amount, unit, and confirmation semantics,
- receipts record outcome and settlement reference,
- the protocol core stays neutral between:
  - external invoicing,
  - host-local ledger settlement,
  - manual transfer,
  - future specialized rails.

This keeps Orbiplex from binding early product scope to crypto-native operator duties.

### Deliberate omissions from v1

The following remain intentionally outside the trusted core for now:

- full dispute and appeal state machine,
- full reputation aggregation model,
- transport-specific wrappers,
- final signature packaging standard,
- local sufficiency-check algorithm.

## Minimal v1 Schema Set

The recommended v1 schema filenames are:

- `question-envelope.v1.schema.json`
- `procurement-offer.v1.schema.json`
- `procurement-contract.v1.schema.json`
- `procurement-receipt.v1.schema.json`
- `response-envelope.v1.schema.json`

These should become the canonical machine boundary for the procurement lifecycle.

## Trade-offs

1. Explicit artifacts vs simpler chat-only flow:
   - Benefit: interoperability, validation, auditability.
   - Cost: more schema and versioning surface.
2. Small core vs richer semantics:
   - Benefit: easier multi-runtime implementation.
   - Cost: retry, dispute, and reputation details still live outside the core.
3. Unified lifecycle across node profiles vs profile-specific shortcuts:
   - Benefit: lower coupling and easier migration between participation modes.
   - Cost: delegated `pod` flows still need some extra identity fields or wrappers.

## Open Questions

1. What exact deterministic tie-break order should be used when offers score equally?
2. Should `response-envelope` carry composite confidence only, or also decomposed
   factors such as retrieval coverage and arbiter outcome?
3. Should a future `dispute-case` artifact be attached to `procurement-receipt`, or
   should it live as a separate lifecycle family?
4. Which fields should remain mandatory for `pod-client` delegated publication versus
   transport-specific wrappers outside the core artifact?

## Next Actions

1. Add v1 JSON Schemas for the five lifecycle artifacts.
2. Add positive and negative examples for each artifact.
3. Bind future offer-scoring and dispute proposals to these identifiers instead of
   inventing parallel payload families.
4. Update requirements and tests to validate this lifecycle as the preferred machine
   boundary for answer procurement.
