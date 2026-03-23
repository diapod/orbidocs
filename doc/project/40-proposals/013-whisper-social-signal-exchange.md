# Whisper Social-Signal Exchange and Threshold Bootstrap

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/20-memos/orbiplex-anon.md`
- `doc/project/30-stories/story-005.md`

## Status

Proposed (Draft)

## Date

2026-03-23

## Executive Summary

This proposal defines the v1 shape of `Orbiplex Whisper` as a privacy-bounded
social-signal exchange layer for rumors, early pattern detection, and later
association bootstrap.

The key decisions are:

1. Whisper exchanges weak social signals rather than confirmed facts.
2. Whisper must keep rumor semantics explicit through the whole flow.
3. Whisper performs local redaction and user-approved rewriting before publication.
4. Anti-Sybil controls in v1 should be budget- and policy-based, not semantic
   duplicate detection.
5. Threshold crossing should lead to a deterministic bootstrap proposal rather than
   automatic human enrollment.
6. Onion-like or relay-based anonymity should live behind a separate outbound
   privacy capability and be requested by Whisper through routing intent rather
   than embedded into Whisper itself.

## Context and Problem Statement

Orbiplex currently has room-oriented answer exchange, procurement flows, archival
thinking, and growing support for provenance-rich artifacts. What is still missing
is a bounded way for nodes to share socially meaningful weak signals such as:

- "people in different places may be experiencing the same organizational abuse",
- "users may be hitting the same harmful moderation pattern",
- "a dignity or safety issue may be distributed rather than isolated."

Without an explicit social-signal layer, nodes either:

- keep such signals entirely local and fail to correlate them,
- or improvise ad hoc messaging that risks oversharing, weak provenance, and
  accidental rumor amplification.

The system needs a middle layer:

- weaker than evidence,
- stronger than private intuition,
- bounded enough to be privacy-aware,
- and explicit enough to support thresholding and association bootstrap.

## Goals

- Define `Whisper` as a distinct protocol family for rumor-style signal exchange.
- Keep rumor semantics explicit and never flatten them into evidence by accident.
- Make local redaction and user approval part of the publication path.
- Support interest registration and threshold detection without premature disclosure.
- Support deterministic association bootstrap after critical mass is reached.
- Keep transport-level anonymity modular through an outbound privacy capability.

## Non-Goals

- This proposal does not define full evidentiary case management.
- This proposal does not define final governance or adjudication procedures.
- This proposal does not define semantic duplicate detection for rumors in v1.
- This proposal does not require onion-style transport for every Whisper message.
- This proposal does not define the full relay/privacy provider contract beyond its
  boundary with Whisper.

## Decision

Orbiplex should treat `Whisper` as a dedicated social-signal exchange layer with the
following v1 lifecycle:

1. local rumor intake
2. local redaction and idiolect reduction
3. user approval of the sanitized result
4. `whisper-signal` publication
5. optional `whisper-interest` registration on receiving nodes
6. `whisper-threshold-reached`
7. `association-room-proposal`
8. explicit local human opt-in into the next-stage room or process

Transport anonymity remains a separate concern:

- `Whisper` expresses routing intent and privacy posture,
- Node egress resolves that posture through any installed outbound privacy or relay
  capability,
- Node decides whether the requested posture can be satisfied, degraded, or must
  fail.

## Proposed Model

### 1. Rumor semantics remain explicit

Whisper artifacts are not evidence artifacts.

The protocol must preserve a lower epistemic class such as:

- rumor,
- weak signal,
- correlated signal,
- only later, if procedurally justified, confirmed case.

This is a semantic safety boundary. The system must not let a rumor become
"confirmed" merely because many nodes repeated it.

### 2. Local redaction before publication

The raw text entered by a user or operator should remain local by default.

Before publication, Whisper should run a bounded local workflow for:

- anonymization,
- paraphrase,
- idiolect flattening,
- privacy and risk review.

The output of that workflow should be user-reviewed and user-accepted before any
network-facing artifact is emitted.

### 3. Bounded anti-Sybil controls in v1

The v1 baseline should use simpler controls instead of semantic dedup:

- rumor budgets per author scope and time window,
- forwarding budgets,
- derived-nym depth limits,
- hop TTL,
- trust- and policy-aware thresholding.

This proposal explicitly rejects hard semantic duplicate gating for v1, because:

- semantic equivalence is expensive and ambiguous,
- false positives would be operationally harmful,
- the system first needs clean contracts for rumor classification, budgets, and
  disclosure scope.

### 4. Interest without disclosure

Receiving nodes should be able to say:

- "this may matter locally"
- "I am interested in further correlation"

without revealing the underlying person, case, or internal notes.

This lets the system correlate signals before identities are exposed.

### 5. Deterministic threshold bootstrap

When critical mass is reached, the system should not:

- automatically merge people into a room,
- or choose a bootstrap authority ad hoc.

Instead, participating nodes should deterministically derive a small bootstrap set
that publishes an `association-room-proposal` with:

- initial room policy,
- disclosure assumptions,
- bootstrap expiry,
- and moderation or witness expectations.

### 6. Explicit consent gate

Threshold crossing may justify a next-stage room, but not silent enrollment.

Humans must remain opt-in at the point where:

- more information is disclosed,
- identities are correlated more directly,
- or a dedicated room is joined.

## Transport Boundary with Outbound Privacy Capabilities

`Whisper` should not own onion routing or relay topology.

Instead, a `whisper-signal` may carry routing intent such as:

- anonymity requested,
- anonymity required,
- maximum hop count,
- acceptable relay classes.

Node then resolves that intent through some outbound privacy capability if
available. `Orbiplex Anon` is one possible provider of that capability, but
Whisper should not need to know that module by name.

The v1 behavior should support at least:

- `soft-fail`: anonymous routing preferred, but non-anonymous transport may still be
  used if policy allows,
- `hard-fail`: anonymous routing required, and the rumor must not be sent if the
  requested posture cannot be satisfied.

This keeps protocol meaning separate from transport realization.

## Candidate Artifacts

The likely first contract family is:

1. `whisper-signal.v1`
2. `whisper-interest.v1`
3. `whisper-threshold-reached.v1`
4. `association-room-proposal.v1`

Later additions may include:

- `whisper-disclosure-request.v1`
- `whisper-disclosure-decision.v1`
- `whisper-forward.v1`

## Trade-offs

1. Whisper vs generic messaging:
   - Benefit: cleaner semantics and safer handling of rumors.
   - Cost: one more protocol family and lifecycle to maintain.
2. Local redaction and approval vs direct publication:
   - Benefit: stronger privacy and less idiolect leakage.
   - Cost: more friction before publication.
3. Budget-based anti-Sybil controls vs semantic dedup:
   - Benefit: implementable now, easier to reason about.
   - Cost: allows some near-duplicate rumors through.
4. Separate `Anon` module vs embedded onion routing:
   - Benefit: cleaner layering and broader reuse.
   - Cost: routing policy becomes a cross-module contract.
5. Deterministic bootstrap vs central coordinator:
   - Benefit: more federated and less monopolistic.
   - Cost: more care needed in threshold and quorum design.

## Open Questions

1. What exact threshold function should be used:
   - distinct nodes only,
   - trust-tier weighted,
   - or diversity-constrained?
2. What exact structure should a rumor nym and derived forwarding nym have?
3. Should `whisper-threshold-reached` include aggregate statistics only, or also
   bounded witness references?
4. Should some classes of rumor be forbidden from any rebroadcast without a
   suitable outbound privacy capability present?
5. Which parts of association bootstrap belong to Whisper and which should later
   move into a more specialized association module?

## Next Actions

1. Add v1 schemas for `whisper-signal`, `whisper-interest`,
   `whisper-threshold-reached`, and `association-room-proposal`.
2. Add one implementation-facing solution component for `Whisper`.
3. Add one implementation-facing solution component for an outbound privacy
   provider such as `Anon`.
4. Define the local Node service contract for model-assisted redaction and user
   approval workflows.
5. Revisit threshold policy and derived-nym rules once the first schema set exists.
