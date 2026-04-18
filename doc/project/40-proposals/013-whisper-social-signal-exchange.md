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
  collective response or protective action. The signal grade expresses protective
  risk and urgency. Emergency assistance
  paths may be triggered.
- **`inspiration`** — the signal describes a convergent idea, creative discovery, or
  emerging approach that multiple people or groups appear to have independently
  reached. The lifecycle goal is to propose co-creation or collaboration between
  parties who have not yet found one another. The signal grade expresses convergence
  strength, co-creation potential, or urgency of matching interested participants. Emergency
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

## Distribution and Local Storage

A whisper is a content artifact; *how* it reaches receivers is a separate
question. This proposal freezes two coequal distribution mechanisms and
one local storage rule.

### Agora as one distribution surface

A whisper MAY be published as a first-class Agora record (proposal 035)
with:

- `record/kind = "whisper"`,
- `content/schema = "whisper-signal.v1"`,
- `author/participant-id` carrying the `rumor/nym` as a
  `nym:did:key:...` identity (proposal 035 §2 invariant 9),
- `author/nym-certificate-ref` resolving to a currently valid
  `nym-certificate.v1` (proposal 015),
- envelope `signature` produced by the nym's private key,
- ingest admitted by the attestation gate (proposal 041) with the nym
  certificate accepted as the attestation artifact under the topic's
  configured ingest mode.

When a whisper travels on Agora, identity, authorship, timing, the
canonical record identifier, and the signature live in the **envelope**,
not in the `whisper-signal.v1` content body. This mirrors the
envelope-vs-content reconciliation applied to `resource-opinion.v1` in
proposal 026 §2.

| Concern | Where it lives |
|---|---|
| pseudonymous author identity | envelope `author/participant-id` = `nym:did:key:...` |
| nym authorization binding | envelope `author/nym-certificate-ref` |
| authoring timestamp | envelope `authored/at` |
| canonical signal identifier | envelope `record/id` |
| signature over canonical bytes | envelope `signature` (Ed25519 by the nym key) |
| topic routing | envelope `topic/key` (conventionally `ai.orbiplex.whispers/<topic-class>` for public/federated whispers; `private/<name>` for direct-only INAC artefacts that must never be carried by Agora) |
| whisper semantics | content body validated by `whisper-signal.v1` |

Agora distribution is appropriate when:

- the whisper's `disclosure/scope` is `federation-scoped`,
  `cross-federation`, or `public-aggregate-only`,
- the author wants addressable subject-index presence under a public
  topic,
- the relay operators' ingest policies (proposal 041 §4–§5) match the
  whisper's risk and routing posture.

Agora distribution is NOT appropriate for whispers whose
`disclosure/scope` is `private-correlation`; those SHOULD travel via
direct node-to-node exchange.

This is a **SHOULD, not a MUST**, by design. On public Agora
deployments the semantics of `private-correlation` are incompatible
with Agora's publication properties (public topic enumeration,
subject-index presence, per-topic digest), and any such deployment
SHOULD refuse these whispers at ingest. A closed / intra-organization
federation (e.g. a corporate deployment whose Agora relay is
authenticated, non-public, and governed by its own ingest policy) MAY
choose to carry `private-correlation` whispers internally, because the
exposure surface of such a relay is already narrowed to the
organization. The rule is therefore scoped to disclosure semantics,
not mechanically to the `agora-record.v1` envelope — operators of
non-public federations are trusted to decide.

### Direct node-to-node exchange as the second distribution surface

A whisper MAY travel directly between participating nodes without
touching an Agora relay. The **wire format remains the same
`agora-record.v1` envelope**, so canonicalization, signature rules, and
self-verification are identical; only the transport and the addressable
scope differ:

- transport: node-to-node authenticated channel realized through the
  outbound privacy capability (see "Transport Boundary" below),
- scope: the receiving set is determined by direct node selection or
  by interest registration (`whisper-interest.v1`), not by public
  topic subscription,
- retention: governed by each receiver's local Memarium policy; there
  is no shared substrate to enforce uniform retention across
  receivers.

Direct exchange is appropriate when:

- `disclosure/scope = "private-correlation"`,
- routing requires `hard-fail` anonymity and no Agora relay can
  guarantee it,
- the whisper is an early pattern probe that has not yet crossed any
  threshold that would justify durable public presence.

### Interest discovery and bounded private dissemination

For `private-correlation` whispers, Agora-discovered topic interest is
**eligibility, not delivery entitlement**.

An Agora topic interest record may say that a node is willing and able to
receive private whispers for a topic class via INAC or another acceptable
private exchange path. It MUST NOT imply that every matching private
whisper must be delivered to that node. The origin node is responsible
only for **bounded initial dissemination** under local egress policy.

A node selecting recipients for a private whisper SHOULD choose a small,
policy-bounded set using criteria such as:

- topic-class compatibility,
- accepted `disclosure/scope`,
- private transport support,
- local egress budget,
- declared intake capacity,
- node or operator assurance,
- diversity across federation, jurisdiction, operator class, or
  reputation band,
- deterministic epoch sampling, so popular topics do not always route
  to the same receivers.

Wider awareness SHOULD be achieved by thresholded aggregate artifacts
and consent-gated follow-up, not by raw private-signal fan-out. A million
nodes expressing general interest in a popular topic therefore does not
create a million-message delivery obligation.

### Holder-assisted redistribution

A node that receives and stores a private whisper MAY later act as an
additional holder and redistributor, but only when all of the following
are true:

- the signed whisper and local Memarium policy allow forwarding or
  custodial redelivery,
- the receiving operator explicitly enables holder availability for the
  relevant class of whisper,
- the node publishes only a bounded availability signal to Agora, not
  the private whisper itself,
- the node enforces the same disclosure, routing, budget, consent, and
  audit constraints that applied to the origin node.

The holder availability signal is a discovery hint, not a public shadow
copy of the whisper. It SHOULD avoid raw `signal/text`, raw keywords,
case-specific timestamps, and other reconstructive metadata. A safe v1
shape should be closer to:

- topic class or coarse topic family,
- accepted private transport profile,
- disclosure scope accepted by the holder,
- capacity and rate limits,
- assurance / relay / witness class,
- optional opaque availability token for correlation with direct
  follow-up.

Publishing holder availability for a private whisper is itself a
disclosure act. Public Agora deployments SHOULD treat per-signal holder
availability as sensitive and may refuse it unless it is sufficiently
coarse, delayed, thresholded, or explicitly authorized by the whisper's
policy. Closed / intra-organization federations MAY use more specific
holder availability beacons when their ingress and visibility policies
make that exposure acceptable.

Holder-assisted redistribution does not require an Agora availability
record. A trusted node MAY contact a peer directly over INAC and offer a
private whisper transfer using a bounded topic hint such as "I hold a
private whisper for topic class X under disclosure scope Y". The peer
MAY then request the artefact, ignore the offer, or ask for operator
review before requesting it.

This offer/request/transfer path is independent of the whisper's origin:
the held whisper may have been authored locally, received directly,
received through a trusted relay, restored from Memarium custody, or
obtained from a later holder. What matters is the signed artefact, its
forwarding policy, local holder policy, and the receiver's intake policy.

Receiver decision policy MAY be:

- **default policy** — deterministic local rules request or refuse the
  offered whisper automatically,
- **operator approval** — the node notifies the operator and requests
  only after explicit approval,
- **advisory automation** — a local advisory model or LLM evaluates the
  offer against policy and recommends or triggers a request, subject to
  configured autonomy limits and audit logging.

The offer itself MUST NOT contain raw `signal/text`, raw keywords, or
other reconstructive metadata. It should be no more specific than the
minimum needed for the peer to decide whether to request the artefact.

The same whisper MAY move between distribution surfaces over time:
what starts as direct node-to-node exchange and later crosses a
threshold (§5) MAY be republished to Agora as `whisper-durable`
(record kind registered in proposal 035 §3), with the transition
gated by the explicit consent step (§6).

### Memarium as local storage

Regardless of distribution surface, the **local storage of a whisper**
— both authored and received — is the node's Memarium (proposal 036).
Memarium carries:

- the signed `agora-record.v1` envelope byte-identically (requirements-014
  NFR-004), so the whisper remains verifiable and reshippable whether
  it first traveled via Agora or directly,
- the action trace for the whisper's lifecycle (draft, redaction,
  approval, publication, forwarding, interest counting, threshold
  detection),
- the privacy policies that determine whether the whisper can be
  replayed, forwarded, or exposed outside the node.

Memarium is the authoritative local archive; Agora (where used) is a
replicated publication surface. A whisper never stored in Memarium
never existed from the local node's perspective. A whisper stored in
Memarium remains replayable for the custodial redelivery flow
(proposal 040) subject to the node's current retention and disclosure
policy; the author's consent and the receiving relay's current
ingest policy both remain authoritative at each reship.

### Operator-mediated rumor curation

A node that subscribes to public whispers (Agora) or accepts private
whispers (direct node-to-node) accumulates received rumors in Memarium
as part of the normal ingest path. Memarium is append-only from the
envelope's perspective — a received whisper envelope is never
retroactively mutated or deleted — but the node's local curation state
for that envelope **is** a mutable projection, stored as separate
Memarium facts keyed by the received record's id.

The node surfaces accumulated rumors to the operator through a local
inbox-style view (e.g. "you have 5 new whispers"). For each rumor the
operator can apply one of the curation verdicts:

- **credibility rating** on a 1..5 scale,
- **mark as spam**,
- **mark as policy-violating** (e.g. abusive, illegal, off-topic for
  this node's federation posture).

Each verdict is expressed as a `resource-opinion.v1` (proposal 026)
whose envelope `record/about` references the rumor's `record/id` —
the same identity under which the whisper is addressable in Agora
and in Memarium. This keeps rumor curation inside the same opinion
mechanism that the substrate already uses for resources, proposals,
and identities; no separate "rumor review" schema is introduced.

The concrete mapping (per `rumor-opinion.overlay.v1` defined in
proposal 026 §2.4) is:

- **credibility rating** → `opinion/subject-kind: "rumor"` plus
  `rumor/credibility` integer in `1..5`. The core `opinion/rating`
  field is left unused for rumor curation; credibility is a
  kind-specific dimension orthogonal to the substrate-wide rating
  scale.
- **mark as spam** → `opinion/subject-kind: "rumor"` plus
  `rumor/rejection-reason: "spam"`.
- **mark as policy-violating** → `opinion/subject-kind: "rumor"`
  plus `rumor/rejection-reason: "policy-violation"` (or one of the
  more specific enum values `abusive`, `off-topic`, `duplicate`,
  `fabricated` when the operator chooses a narrower reason).

A single curation opinion MAY combine a credibility score and a
rejection reason, and MAY additionally carry `opinion/text` when the
operator wants to justify the verdict.

Default propagation effect of a verdict, applied by the node's own
outbound policy (not by the protocol):

- **rated**: does not alter propagation; rating is a first-class
  opinion that other nodes may or may not consume through the Agora
  opinion topic for that record,
- **spam**: the envelope is retained locally for audit but is **not**
  rebroadcast, not forwarded via holder-assisted redistribution
  (§Holder-assisted redistribution), and is excluded from threshold
  counting on this node,
- **policy-violating**: same outbound suppression as spam, and
  additionally the node's curation opinion is published so that
  peers relying on this node's judgement can discount the rumor.

The curation opinion itself is an ordinary Agora record and follows
the disclosure and signing rules of proposal 026; it does **not**
inherit the original whisper's `disclosure/scope`. An operator
reviewing a `private-correlation` whisper can still publish a public
"this is spam" opinion about its record id without leaking the
whisper body, because the opinion targets the id, not the content.

No protocol-level deletion of the original whisper is required.
Suppression is a local propagation decision; the verifiable envelope
and its curation verdicts coexist in Memarium as separate facts on
the same timeline.

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

`whisper-signal.v1` is a **content-body schema** for the Agora record
envelope (proposal 035) and for the same envelope used in direct
node-to-node exchange (see "Distribution and Local Storage"). The
content body carries whisper-level semantics only:

- `signal_polarity` (`problem` | `inspiration`),
- `epistemic/class`, `signal/text`, `topic/class`, `context/facets`,
- `confidence`, `disclosure/scope`, `signal/grade`, source attribution,
- routing intent (`routing/profile`, `routing/failure-mode`,
  `forwarding/max-hops`, ...).

Identity and authorization that the pre-reconciliation sketch carried
inside the content body move to the enclosing envelope:

- `rumor/nym` → envelope `author/participant-id` as
  `nym:did:key:...`,
- attached `nym-certificate` → envelope `author/nym-certificate-ref`,
- nym signature over the body → envelope `signature` over the full
  canonical envelope bytes (Ed25519 by the nym key).

This keeps `whisper-signal.v1` a small portable shape independent of
whether the whisper travels on Agora or directly between nodes, and
prevents the signing domain from being split across two artifacts.

`whisper-interest.v1` should not mirror that pattern. It remains a node-scoped
local-interest declaration:

- counted and evaluated per participating node,
- carrying `interested/node-id` rather than a participant or nym author,
- and suitable for threshold coordination without turning local readiness into a
  pseudonymous transport-facing identity.

Later additions may include:

- `whisper-topic-interest.v1`
- `whisper-holder-availability.v1`
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
6. **Resolved** — resolved in proposal 026 §2.4: curation verdicts
   are expressed as `resource-opinion.v1` with
   `opinion/subject-kind: "rumor"` plus the `rumor-opinion.overlay.v1`
   fields (`rumor/credibility` in `1..5`; `rumor/rejection-reason`
   as a closed enum). No new opinion subtype is introduced. Still
   open: should the substrate define a minimum aggregation rule
   (e.g. K independent `rumor/rejection-reason = spam` verdicts from
   trusted peers) that a receiving node's default policy treats as
   an automatic propagation suppressor, and how is "trusted peer"
   scoped for that purpose?

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
7. Rewrite `whisper-signal.v1.schema.json` as a content-body-only schema
   (dropping `signal/id`, `created-at`, `rumor/nym`, `auth/nym-signature`,
   and `auth/nym-certificate` — all of which move to the enclosing
   `agora-record.v1` envelope per the Distribution section), mirroring
   the content-body-only shape already applied to
   `resource-opinion.v1.schema.json` for proposal 026.
8. Register `whisper` as a recognized `record/kind` and
   `whisper-signal.v1` as a recognized `content/schema` in the Agora
   relay reference implementation; register
   `ai.orbiplex.whispers/<topic-class>` as the conventional
   public/federated topic-key prefix, and reserve `private/<name>`
   for direct-only INAC artefacts outside Agora.
9. Define the direct node-to-node exchange contract as a thin binding
   over the same `agora-record.v1` envelope, consuming the outbound
   privacy capability for transport and the attestation gate for
   peer admission, with Memarium as the sole persistent store on both
   ends.
10. Wire operator-mediated rumor curation
    (§Operator-mediated rumor curation) into the Node UI whisper
    inbox: per-rumor actions for `rumor/credibility` (1..5),
    `rumor/rejection-reason: spam`, and
    `rumor/rejection-reason: policy-violation`; each action emits a
    `resource-opinion.v1` with `opinion/subject-kind: "rumor"`
    targeting the rumor's `record/id`, persisted as a Memarium fact
    and routed through the node's normal opinion publication path.
    Outbound propagation policy consumes the local verdicts as
    suppression inputs (any `rumor/rejection-reason` present → no
    rebroadcast, no holder-assisted redistribution, excluded from
    threshold counting).
11. Publish `rumor-opinion.overlay.v1.schema.json` as a standalone
    overlay artifact validating the `rumor/*` namespace
    (`rumor/credibility`, `rumor/rejection-reason`), and add a
    worked example pair under
    `doc/schemas/examples/`: one pure-credibility verdict (no
    text, `rumor/credibility: 2`) and one spam verdict
    (`rumor/rejection-reason: "spam"` plus short justification in
    `opinion/text`).
