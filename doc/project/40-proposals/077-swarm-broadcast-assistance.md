# Proposal 077: Swarm Broadcast Assistance

Based on:
- `doc/project/20-memos/swarm-broadcast-assistance.md` (promoted memo)
- `doc/project/20-memos/whisper-corpus-composition.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/039-crisis-space-seed-v1.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`

## Status

Draft

## Date

2026-07-03

## Executive Summary

A node user may open a communication window to the swarm and broadcast an
issue that matters to them — a personal problem, a technical blockage, a
safety concern, or a request for orientation. The swarm treats the broadcast
as a **shared assistance request**, not a point-to-point message: it may
gather relevant context, route sub-questions to capable nodes, hire a Corpus
deliberation, request clarification, and converge on a helpful response or
action plan — synthesized from many partial contributions with traceable
sources, explicit uncertainty, and a clear distinction between facts,
hypotheses, and recommendations.

This proposal promotes the assistance memo into an architectural direction by
grounding it in mechanisms that now exist: the P003 question-envelope /
answer-channel transport, Corpus procurement and deliberation (P069), bounded
Agent sessions (P073), the Inquirium assistant channel with its epistemic and
mode-rigor guarantees (P066), and the crisis boundary (P039, P066
`assistant-crisis-candidate`).

Assistance is the path Whisper deliberately is not: Whisper correlates weak
signals into association; assistance is a scoped, user-initiated call for
help. The two compose (an association room may raise an assistance request or
hire expertise), but they never merge.

## Context and Problem Statement

The primitives for collective help exist, but no contract ties them into an
assistance flow: P003 can carry questions to selected responders, Corpus can
convene topic experts, Agent can run bounded unattended reasoning, and the
assistant channel can hold the human's hand — yet "I need help with X, swarm"
has no envelope, no scope control, no synthesis contract, and no explicit
crisis boundary. The memo held the vision; implementation pressure (the
Whisper→Corpus composition, the crisis-candidate path) now justifies fixing
the semantics.

## Goals

- Define the assistance request as a first-class, scoped artifact riding the
  existing question-envelope family (P003), not a new transport.
- Let the user control scope and intensity: private / federation-local /
  wider; whether follow-up questions are allowed; urgency class.
- Define the synthesis contract: multi-source response with traceable
  contributions, explicit uncertainty, and fact / hypothesis / recommendation
  separation (inheriting Inquirium's epistemic block semantics).
- Define continuity: an assistance case stays open until resolved or safely
  handed off, with facts recording each transition.
- Keep the crisis boundary hard: assistance may *nominate* a crisis
  (`crisis-candidate`), but crisis authority stays host-owned (P066), and
  data custody under crisis stays with Crisis Space (P039).
- Support both sponsored and gift-priced help (price `0` is normatively the
  gift-economy regime — see the composition memo).

## Non-Goals

- Not an emergency dispatch system: acute personal emergencies prefer the
  local help-mode path (P013 boundary); assistance is not the default first
  response to a likely cardiac arrest.
- Not a replacement for Corpus: Corpus is one hireable resolution step, not
  the assistance flow itself.
- Not a reputation or scoring system for helpers (see the anti-Goodhart guard
  in the composition memo: recognition is a trace, not a currency).
- Not swarm gossip: requests go to scoped, selected responders (P003), never
  to "everyone" implicitly.

## Proposed Model

### 1. Assistance request envelope

An `assistance-request.v1` rides the P003 question-envelope family with an
assistance profile: stable id, scope (`private` | `federation-local` |
`wider`), urgency class, follow-up policy, TTL after which the asker no
longer promises to accept late answers, and an optional coarse
`context/class: community-gift` marker (never identifying an association
room or its members — the privacy guard from the composition memo).

### 2. Decomposition and routing

The receiving side may decompose the issue and route sub-questions to capable
nodes using existing discovery (offer catalog, Corpus topic resolution) and
transport (P003 selected-responder, Artifact Delivery). Decomposition and
routing run as bounded Agent sessions (P073): human-in-the-loop gates
*effects, budgets, and acceptance* — never individual reasoning turns.

### 3. Synthesis contract

The response need not come from one node. The synthesized answer carries:
contribution references (traceable sources), explicit uncertainty, and the
fact / hypothesis / recommendation distinction. Stance is never
`authoritative`; plurality is preserved when viable alternatives exist
(Inquirium P066 epistemic semantics apply end to end).

### 4. Continuity and handoff

An assistance case is a fact-backed lifecycle: opened, decomposed, responded,
clarified, resolved, or **handed off** (to a human, a service, or the crisis
path). Every transition leaves a fact; silent closure is not a state.

### 5. Crisis boundary

If assistance processing detects crisis indicators, it emits a
`crisis-candidate` to the host crisis layer (P066) — it never declares crisis
itself. Crisis data custody follows Crisis Space (P039). Assistance may
continue alongside a crisis as its network-facing support surface, but crisis
authority and assistance choreography never merge.

### 6. Economic modes

A request may be answered under sponsorship (an asker or supporter contracts
paid steps, e.g. a Corpus procurement) or as gift work (zero-price offers).
Providers may position themselves for community work in the offer catalog;
the concrete offer-field shape lands in the owning contracts when picked up.

## Trade-offs

- Reusing the P003 question-envelope family avoids a new transport, but it
  means the assistance-specific semantics must be explicit as a profile,
  lifecycle, and synthesis contract rather than hidden in delivery mechanics.
- Calling this a "broadcast" gives users a clear mental model of asking the
  swarm for help, but the protocol must keep "broadcast" scoped: selected
  responders, signed scope, and TTL are part of the contract, not optional
  operator etiquette.
- Letting Agent sessions decompose and route work makes assistance useful
  before every step is human-driven, but effect commitment, budgets, and final
  acceptance stay behind human-in-the-loop gates.
- Sponsor-as-asker is the simplest MVP identity model for association-room
  requests. A room-scoped asker identity is more symmetric, but it belongs
  after association-room lifecycle and room membership semantics are concrete.

## Failure Modes and Mitigations

| Failure | Risk | Mitigation |
|---|---|---|
| Assistance used as emergency dispatch | Delayed real-world response | Hard non-goal; urgency class routes acute cases to the local help-mode path; crisis-candidate to host layer. |
| Scope creep of a broadcast | Sensitive issue leaks wider than intended | Scope is part of the signed envelope; responders outside scope refuse; TTL bounds late spread. |
| Community marker deanonymizes a group | Association-room existence leaks | Marker stays coarse (`community-gift`), optional, never carries room/topic/member identity. |
| Helper reputation farming via cheap tasks | Gift economy corrupted by Goodhart | No fungible score; recognition only as signed, non-aggregable acknowledgment facts. |
| Unattended agents commit effects | Autonomy exceeds budgeted trust | P073 bounded contracts; HIL gates effects/budgets/acceptance; deliberation output is a signed answer, not an action. |

## Open Questions

No unresolved questions remain for this proposal's MVP contract.

1. ~~Does `assistance-request.v1` need its own schema, or is a P003
   question-envelope profile (like `selected-responder`) sufficient for
   MVP?~~ **Resolved:** MVP uses a P003 `question-envelope` assistance profile.
   A separate `assistance-request.v1` may be introduced only after the
   lifecycle diverges enough to need its own contract family.
2. ~~What is the minimal case read-model (open assistance cases, states,
   handoffs) and where does it live — assistant channel surface or a dedicated
   host capability?~~ **Resolved:** the minimal assistance case read-model
   lives behind a dedicated host capability. Assistant Channel may consume and
   present it, but does not own the assistance state.
3. ~~How does an association room formally raise an assistance request —
   sponsor-as-asker only (MVP), or a room-scoped asker identity
   later?~~ **Resolved:** MVP uses sponsor-as-asker. Room-scoped asker identity
   is a later extension once association-room identity surfaces are stronger.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Task | Status | Notes |
|---|---|---|---|
| P077-001 | Define the assistance profile on the P003 envelope family | todo | Scope, urgency, follow-up policy, TTL, coarse `context/class` marker; MVP uses a P003 `question-envelope` profile rather than a separate `assistance-request.v1` schema. |
| P077-002 | Assistance case lifecycle facts and read-model | todo | opened/decomposed/responded/clarified/resolved/handed-off; every transition is a fact. |
| P077-003 | Crisis-candidate emission from assistance processing | todo | Rides P066 `assistant-crisis-candidate`; never declares crisis; host crisis layer owns status. |
| P077-004 | Corpus-as-resolution-step choreography | todo | Side-room first, per the composition memo; signed answer posted back into the case. |
| P077-005 | Gift/sponsored economic modes on assistance steps | todo | Price 0 = gift regime; provider community-affinity positioning in the offer catalog. |

## Next Actions

1. Define the P003 `question-envelope` assistance profile and schema-gate
   expectations.
2. Define the dedicated host-capability assistance case read-model.
3. Wire the advisory cross-references (013, 039, 069, 073) — done at
   promotion time.
4. Revisit after the Whisper association-room lifecycle slice lands, so the
   room→assistance path can grow beyond sponsor-as-asker when needed.
