# Communication Exposure Modes for Swarm Requests

Based on:
- `memos/swarm-communication-exposure-modes.md`
- `proposals/003-question-envelope-and-answer-channel.md`

## Status

Proposed (Draft)

## Date

2026-03-21

## Executive Summary

This proposal defines the user-facing exposure modes that determine how widely a swarm
request may be visible and how its later traces may propagate.

The key decision is that exposure should be an explicit policy knob rather than an
accidental consequence of transport choice.

The baseline user-facing modes are:

1. `private-to-swarm`
2. `federation-local`
3. `public-call-for-help`

These are request-level exposure profiles, not identical to every lower-level room or
transport scope. A public call may still compile into different technical scopes such
as bounded cross-federation dissemination or truly global reach.

## Context and Problem Statement

`003-question-envelope-and-answer-channel.md` already defines question envelopes and
live answer rooms. What remains underspecified is the privacy and visibility intent of
the asking user or node.

Without explicit exposure modes:

- every request risks being treated as equally visible,
- retention and summarization defaults become inconsistent,
- transcript publication policy cannot reason from user intent,
- escalation from private to wider exposure becomes ad hoc.

The system therefore needs a stable, user-comprehensible exposure model that can drive
routing, retention, notification, and later archival policy.

## Goals

- Give users and nodes explicit control over exposure level.
- Separate user-facing exposure intent from low-level transport details.
- Make escalation and de-escalation of visibility possible over time.
- Bind exposure mode to routing, retention, notification, and onward sharing.
- Keep the model simple enough for interoperable client UX.

## Non-Goals

- This proposal does not define every transport-level routing scope.
- This proposal does not define the full consent taxonomy for archival export.
- This proposal does not replace room-policy profiles for human participation.

## Decision

Every user-facing swarm request should carry an explicit exposure mode or inherit one
from a visible default.

The baseline modes are:

1. `private-to-swarm`
2. `federation-local`
3. `public-call-for-help`

At baseline:

1. exposure mode MUST influence routing, retention, notification policy, and onward
   sharing defaults,
2. clients MUST make the chosen mode visible before submission,
3. exposure MAY be escalated or de-escalated over time through explicit state
   transition,
4. wider exposure MUST NOT happen silently unless a separate high-stakes constitutional
   procedure justifies it.

## Proposed Model

### 1. Mode definitions

#### `private-to-swarm`

Meaning:

- visibility is limited to the minimum set of nodes, agents, and memory components
  needed to help,
- routing should prefer least disclosure and smallest eligible set,
- later sharing and archival should default to the strictest gates.

Use when:

- the matter is personal, medical, legal, security-sensitive, or otherwise dignity
  critical.

#### `federation-local`

Meaning:

- visibility is intentionally limited to one federation or another bounded trust scope,
- routing favors local context, shared norms, and bounded disclosure,
- archival and summaries may remain eligible only inside that scope unless policy says
  otherwise.

Use when:

- local trust, language, legal context, or federation norms matter more than broad
  reach.

#### `public-call-for-help`

Meaning:

- the asker intentionally seeks broad attention, diverse input, rare expertise, or
  urgent support,
- routing may expand beyond federation boundaries,
- later publication and notification defaults may be broader than in the two stricter
  modes.

Use when:

- the problem benefits from wide reach and the asker accepts the associated exposure
  cost.

### 2. Derived policy surfaces

Exposure mode should influence at least:

- question dissemination scope,
- answer-room discovery,
- transcript export defaults,
- notification fan-out,
- summary visibility,
- vault publication eligibility.

The exact lower-level fields may differ by federation, but the semantic effect must be
predictable.

### 3. Transition rules

Exposure is a stateful property, not a one-time label.

Rules:

1. A request MAY start narrow and widen later.
2. A request MAY also narrow later, but prior disclosures and prior transcript events
   retain their historic scope.
3. Transition from narrower to wider exposure SHOULD require explicit asker consent,
   unless a separate emergency or constitutional basis exists.
4. Transition from wider to narrower exposure SHOULD update future routing,
   notifications, and publication eligibility, but must not pretend that earlier wider
   visibility never happened.

### 4. Transport mapping

Exposure modes are user-facing semantics and may map to lower-level transport scopes.

For example:

- `private-to-swarm` -> minimal eligible room membership + strict retention profile,
- `federation-local` -> federation-bounded envelope dissemination and room discovery,
- `public-call-for-help` -> cross-federation or global dissemination according to room
  and federation policy.

This keeps UX stable while preserving architectural flexibility.

### 5. Minimal contract sketch

```json
{
  "request/exposure-mode": "federation-local",
  "routing/disclosure-profile": "bounded",
  "summary/visibility-default": "federation-local",
  "transcript/export-default": "review-required",
  "notification/fanout-profile": "federation"
}
```

## Trade-offs

1. Simplicity vs fine-grained nuance:
   - Benefit: understandable user choice and interoperable clients.
   - Cost: some federations may want more than three user-facing modes.
2. Explicit escalation vs friction:
   - Benefit: less accidental overexposure.
   - Cost: more state transitions and UI prompts.
3. User intent vs federation override:
   - Benefit: stronger sovereignty and dignity protection.
   - Cost: high-stakes local policy may still need to restrict or widen behavior.

## Open Questions

1. Should `public-call-for-help` split into `cross-federation` and `global` as
   separate user-facing modes later?
2. Should exposure mode be mutable only by the asker, or also by a secretary under
   bounded policy?
3. How should exposure mode interact with transcript monitors and archivist defaults?
4. Which UI wording best conveys exposure cost without overwhelming the user?

## Next Actions

1. Bind exposure modes to question-envelope metadata and room creation policy.
2. Align transcript and archival defaults with exposure mode semantics.
3. Define visible state-transition events for exposure escalation and de-escalation.
4. Define client UX for mode selection and exposure-change confirmation.
