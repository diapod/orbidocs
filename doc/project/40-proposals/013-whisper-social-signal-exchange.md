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
- "a dignity or safety issue may be distributed rather than isolated",
- "ambulance refusal followed by severe complications may be repeating as a systemic emergency-care failure rather than as isolated bad luck",
- "independent inventors in different countries appear to be converging on the same technical approach without prior contact",
- "several communities have independently bootstrapped structurally similar solutions to an unmet need".

The second class of signal — inspiration convergence — is as important as the first.
Where problem signals serve early detection and collective response, inspiration signals
serve co-creation: connecting people who have independently arrived at a similar idea
before their paths diverge irrecoverably. Both polarities deserve first-class support.

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

### 0. Signal polarity

A `whisper-signal` carries one of two fundamental polarities:

- **`problem`** — the signal describes a distributed harm, failure, or dignity risk.
  The lifecycle goal is early correlation and, where critical mass is reached,
  collective response or protective action. Risk grade applies. Emergency assistance
  paths may be triggered.
- **`inspiration`** — the signal describes a convergent idea, creative discovery, or
  emerging approach that multiple people or groups appear to have independently
  reached. The lifecycle goal is to propose co-creation or collaboration between
  parties who have not yet found one another. Risk grade does not apply. Emergency
  protocols are never triggered.

`signal_polarity` is a mandatory field on `whisper-signal.v1`. The two polarities
share the same lifecycle but differ in urgency, redaction posture, and the nature of
the resulting association room:

- problem → support, coordination, or protective response room,
- inspiration → co-creation or collaboration room.

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

Protective anonymization in this workflow is aimed at people and protected local contexts. It should not blindly erase names of companies, hospitals, ambulance operators, or other institutions when those entities are plausibly part of the harmful pattern and do not require protection.

When a local helper such as `Monus` prepared the draft, downstream policy should
still be able to distinguish user-authored, operator-observed, Monus-derived, and
Monus-plus-Sensorium-derived signals.

For role semantics, the outgoing `whisper-signal` should preserve both:

- `sender/node-id` for the infrastructure actor carrying the publication, and
- a pseudonymous authored role through `rumor/nym`, attached `nym-certificate`,
  and `nym` signature over the outgoing artifact body.

When Whisper uses the nym path, the backing `participant-id` should remain on the
local or issuing side of the boundary rather than being disclosed in the
wire-level `whisper-signal` artifact itself.

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

Acute personal emergencies detected through local Sensorium should still prefer a
local help-mode or emergency-assistance path. Whisper is for correlation-worthy
distributed patterns, not as the default first response to a likely cardiac arrest
or comparable collapse.

## Candidate Artifacts

The likely first contract family is:

1. `whisper-signal.v1`
2. `whisper-interest.v1`
3. `whisper-threshold-reached.v1`
4. `association-room-proposal.v1`

`whisper-signal.v1` should be the first concrete artifact that embeds:

- `signal_polarity` (`problem` | `inspiration`),
- `rumor/nym`,
- attached `nym-certificate`,
- and a `nym` signature over the artifact body.

`whisper-interest.v1` should not mirror that pattern. It remains a node-scoped
local-interest declaration:

- counted and evaluated per participating node,
- carrying `interested/node-id` rather than a participant or nym author,
- and suitable for threshold coordination without turning local readiness into a
  pseudonymous transport-facing identity.

Later additions may include:

- `whisper-disclosure-request.v1`
- `whisper-disclosure-decision.v1`
- `whisper-forward.v1`

At least one of those early contracts should also preserve whether the signal was
directly user-authored, operator-observed, or prepared by a local helper such as
`Monus`, so that downstream policy can distinguish user-authored rumors from
monitor-derived ones. If Sensorium materially informed the draft through `Monus`,
that should remain visible as well.

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

1. Should `inspiration` signals use a different threshold function than `problem`
   signals (e.g. lower count, broader geographic diversity requirement)?
2. What exact threshold function should be used:
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
6. Decide whether a future local module such as `Orbiplex Monus` should be allowed
   to prepare semi-automatic or automatic Whisper drafts from wellbeing-weighted
   local signals.
