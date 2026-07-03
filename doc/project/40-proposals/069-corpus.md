# Proposal 069: Corpus — Topic-Routed Collaborative Reasoning

Based on:

- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/067-shared-offer-catalog-over-agora.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/60-solutions/003-arca/003-arca.md`
- `doc/project/60-solutions/004-dator/004-dator.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/30-stories/story-002-federated-peer-learning.md`
- `doc/project/30-stories/story-006-voluntary-swarm-exchange.md`

## Status

`draft`

## Date

`2026-06-23`

## Executive Summary

`Corpus` lets a node find, hire, and convene a small set of *topic-expert* nodes —
nodes that run an LLM and declare competence on a taxonomically named subject — and
have those nodes collaboratively reason toward a single best answer.

The flow has two phases of different nature and **different readiness**:

1. **Procurement (the MVP).** Keywords resolve to one canonical topic term (e.g.
   `IT:programming:C++`). The offer catalog is queried for nodes advertising a
   `corpus.provider` competence on that topic. A query carrying a price bracket is
   broadcast; each responder bids or stays silent; the asker selects a subset. This
   rides **Artifact Delivery** (Solution 023), reusing the proven Arca/Dator
   request→result pattern generalized to fan-out. **Buildable on existing
   infrastructure; this is the MVP slice.**
2. **Live deliberation (post-MVP).** The asker opens a **room** (Proposal 070), invites
   the selected nodes under an access list, and the participants — each backed by its
   model through **Inquirium** — hold a live synchronous discussion. Latency matters and
   chatter is expected, so the deliberation is a **live chat**. A requester-appointed
   chair resolves conflicts (full arbiter election is later). Convergence produces one
   signed final answer.

Corpus is a thin role plus a small protocol that **composes** existing strata and adds
a topic-taxonomy resolver, a topic field on offers, and a deliberation policy. It
explicitly depends on two prerequisites not yet complete: the generic **Room** primitive
(P070) and the **Agent organ** (P073) that provides the bounded reasoning session. The MVP needs
neither.

The live in-room chat is *reasoning*, not protocol facts: the protocol does not persist
it; only the room skeleton and the final signed answer are durable. Any member MAY
locally capture and audit the chat under its own classification and retention policy.

## Terminology Boundary

`corpus-entry.v1` already exists as a **curated/training corpus** artifact
(requirements 002–005). That "corpus" means *a body of curated knowledge for training
and retrieval*. It is unrelated to the Corpus *component* defined here (*live
collaborative reasoning over a topic*). To prevent drift:

- the component keeps the human-facing name **Corpus**;
- its wire contracts use the **`corpus-reasoning-*`** namespace, never bare `corpus-*`,
  so they never collide with `corpus-entry.v1`;
- topic contracts use **`topic-*`**; room contracts live in P070 (`room.v1`, …).

## Context and Problem Statement

The machinery exists but is spread across components: marketplace procurement (P021/P011,
Arca/Dator), Artifact Delivery (023), the answer-room/Whisper room lineage (P003/P013,
consolidated by P070), and Inquirium (P063/P064/P066). What is missing is the glue: a
deterministic way to name a subject from keywords, a way to discover topic-expert
offers, and a live reasoning session whose only durable output is the answer. Semantic
Index (Solution 022) is vector similarity over *local memory*, not a topic taxonomy.

## Goals

- Resolve a keyword set to one canonical topic term, or to an explicit ambiguous
  candidate set, deterministically and auditably.
- Let providers advertise topic-scoped `corpus.provider` competence in the existing
  offer catalog, with defined indexing, validation, and withdrawal semantics.
- Reuse Artifact Delivery for discovery, broadcast query, bidding, and selection (MVP),
  with an explicit, timestamped bid-state read-model.
- Layer a live synchronous deliberation room (on P070) with access list, a
  requester-appointed chair, and bounded time/step/token budgets.
- Keep the live chat ephemeral; the final answer is the only durable reasoning artifact
  and is a concrete, content-addressed, signed payload.
- Bridge to P011 settlement (single contracting provider for MVP; N-way later).

## Non-Goals

- Not the curated/training corpus (`corpus-entry.v1`).
- Not the Room primitive (P070) nor the Inquirium runtime (P063/P066).
- Not a new settlement rail; it bridges to P011/P016.
- Not a frozen scoring algorithm, seed taxonomy, or reputation backend.
- The MVP excludes the live room, arbiter election, and N-way settlement.

## Prerequisites and Dependencies

| Prerequisite | Needed for | Status |
|---|---|---|
| AD deferred + fan-out + single-owner acceptors (023) | MVP procurement | partial, usable |
| Offer catalog + Dator offers (003/004/067) | MVP discovery | partial, usable |
| P011 procurement artifacts + P016 escrow | MVP settlement (single provider) | partial |
| **Room primitive (P070)** | live deliberation (post-MVP) | **partial: durable contracts, projection core, and Agora runtime projection adapter exist; live plane not built** |
| **Agent organ (P073)** — bounded reasoning session | live multi-turn reasoning (post-MVP) | **partial: `agent-core`/`agent-host` exist and the daemon has a node-local `spawn/status/stop` runtime; fork, persistence, Room chair binding, and effect proposals are not built** |

The MVP depends only on the first three rows. The live-deliberation layer is
**blocked-by** P070's live plane/runtime integrations and the Agent organ (P073)
runtime, stated explicitly rather than assuming a live room exists.

Room is a generic swarm primitive, not a Corpus-owned subsystem. Corpus depends
on Room; Room must not depend on Corpus or import Corpus reasoning semantics.
`Corpus-on-Room` is therefore a domain protocol layered over a neutral room:
Corpus may decorate room policy, invite, role, and answer facts, but membership,
presence, live transport, lifecycle, attestations, and room projections remain
owned by the Room layer.

### Bounded reasoning session (Agent organ, P073)

Full Corpus needs a multi-turn reasoning session bound to a room, with bounded
steps/deadline/tokens, context ingestion, and explicit draft boundaries. That is
exactly the **Agent organ (P073)**: a host-owned, bounded, stateful controller
with a budget (`steps` / `deadline` / `tokens`), Memarium-backed session context,
and no self-authorization. Corpus should consume the Agent organ as its
deliberation session — its deliberation `budget` maps directly onto the Agent
budget/controller contract — rather than define a smaller Corpus-only LLM surface
or a parallel "Inquirium thread/session runtime". The current Agent slice is
enough to create, inspect, and stop a bounded node-local agent, but it is not yet
the Corpus deliberation runtime: durable Memarium-backed state, fork/suspend/resume,
Room chair binding, and effect-proposal routing remain post-MVP work. Until those
parts land, only the MVP procurement slice is implementable.

## Proposed Model / Decision

### 1. Component Boundary

`Corpus` is a **role plus protocol**, not a parallel marketplace authority. The
demand-side (asker) path extends the Arca demand surface; the supply-side (provider)
path extends the Dator supply surface; both consume host capabilities for every signed
act. Corpus contributes only the topic resolver, the offer topic field, the deliberation
policy, the chair/arbiter logic, and the answer contract.

### 2. Topic Resolution: Signed Versioned Data + Deterministic Matcher

- `topic-taxonomy.v1` is an **open, signed, versioned governance artifact**, not an
  enum. It carries `taxonomy/id`, `federation/id`, `version` + `versioning/scheme`,
  `digest`, `issuer/nym`, `issuer/public-key-ref`, `valid/from`, `valid/until`,
  `supersedes` + `supersession/proof`, an `extension/policy` sub-schema, and a
  `signature`. Terms and per-term labels are unique (validated). Federations may extend
  subtrees; nodes pin `taxonomy/digest`.
- Resolution is a **pure deterministic weighted matcher** returning a canonical
  `topic/term` or an explicit `ambiguous` candidate set. `topic-resolution.v1` records
  the `epsilon`, `matched/labels[]`, `resolver/version`, and is itself signed, so a
  result is reproducible and auditable.

### 3. Topic-Scoped Offers, Indexing, Validation, Withdrawal

`service-offer.v1` (`service/type = "corpus.provider"`) gains a `corpus` extension. It
remains a **full** `service-offer.v1` (all base required fields apply); the extension
adds, not replaces. Decisions:

- **One offer, multiple topic scopes.** One offer carries a `corpus/topics` set, plus
  `corpus/model-class` (enum: `local-llm | remote-llm | human-curated |
  hybrid-llm-curated`), `corpus/taxonomy-digest`, and `corpus/taxonomy-issuer` (so a
  consumer can fetch the issuer key and verify the taxonomy signature — the digest
  alone does not enable verification).
- **`corpus/topics ⊆ terms(taxonomy/digest)`.** Arbitrary strings must not enter the
  topic index. JSON Schema cannot express set-membership against an external artifact,
  so the offer/catalog admission layer enforces it after resolving the pinned taxonomy:
  given `corpus/taxonomy-digest`, every `corpus/topics[*]` must be a term of that
  taxonomy. Missing or untrusted taxonomy material fails closed.
- **Indexing.** The shared catalog (P067) builds a topic index keyed by canonical
  `topic/term` (and parent terms for fallback): `{ offer/id, sequence/no,
  taxonomy/digest, provider/node-id }`.
- **Withdrawal (incl. partial).** Reuse the offer `sequence/no` + withdrawal marker
  (P067). **There is no per-topic withdrawal:** removing a single topic is a
  supersession — publish a new offer revision with a higher `sequence/no` and the
  reduced `corpus/topics`; the index replaces the prior revision. A full withdrawal
  marker removes all of the offer's topic-index entries. `record/supersedes` is not the
  offer-catalog revision authority for this flow; it remains available on Agora
  envelopes, while the catalog read-model reconciles offers by `offer/id`, monotonic
  `sequence/no`, status, and expiry.

### 4. Procurement over Artifact Delivery (the MVP)

1. The asker broadcasts `corpus-reasoning-query.v1` to candidate nodes through one AD
   delivery plan (`?mode=deferred`, a single parallel stage). The query is a Corpus
   decorator over `question-envelope.v1` (P003), not a sibling question primitive. It
   adds the topic, `corpus/taxonomy-digest`, original `query/keywords` (for audit
   reproducibility), requester ids, price bracket, `max/candidates` (fan-out cap), and
   `deadline-at`.
2. Each provider's single `corpus-reasoning-query.v1` acceptor replies with a signed
   `corpus-reasoning-bid.v1` (§4.1) to `reply/target`, correlated by `correlation/id` +
   `query/id`. The bid signature must be checked before a bid can affect selection; the
   daemon MVP verifies its `local-runtime-assertion` against `key/public` and binds that
   key to `bidder/node-id`.
3. The asker maintains a timestamped `corpus-reasoning-bid-state.v1` read-model so
   silence is not conflated with refusal (§4.2), then selects a subset.

**Identifier relationships.** Three ids live in one flow and MUST be mapped explicitly:
`query/id` is minted by the asker and is the spine of the bid round; `correlation/id`
ties one query↔bid pair across AD; when a bid embeds a `procurement-offer.v1`, that
offer's `question/id` is set equal to the Corpus `query/id` so the later
`procurement-contract.v1` chains back to the original query.

#### 4.1 Bid is an envelope around `procurement-offer.v1`

`corpus-reasoning-bid.v1` is **not** a parallel pricing type. It is a thin envelope:
`decision` (enum `accept | decline | counter`) + `bid/valid-until` (TTL) + `policy/digest`
+ an **embedded** `procurement-offer.v1`. The embedded offer carries the
procurement-required fields (`responder/participant-id`, `price/*`, `answer/min-length`,
`answer/max-length`, `execution/mode`, `specialization/tags`, `reputation/evidence`) so
the later contract has everything it needs. `decline` carries no offer; `counter`
carries an offer with a price outside the original bracket.

#### 4.2 Bid-state read-model (no silence/refusal conflation)

Per candidate, `corpus-reasoning-bid-state.v1` carries `state` (`bid-received | declined
| timed-out | delivery-failed | policy-denied | unreachable`), `received-at`,
`updated-at`, a `reason`/`diagnostic-code`, and `delivery/attempt-id` correlating to the
AD delivery. Each candidate's delivery is itself a `deferred-operation-status.v1`; the
bid-state is the **multi-candidate aggregation** over those, not a replacement for them.
Default selection treats only `bid-received` as eligible.

### 5. Live Deliberation (post-MVP, on the Room primitive)

The deliberation runs entirely on **Room** (P070): the asker opens a `room.v1`, attaches
a `corpus-reasoning-room-policy.v1`, and invites selected nodes under the room access
list (`corpus-reasoning-room-invite.v1`). Participants join the room's ephemeral live
plane and reason synchronously through the Agent organ (P073) bounded reasoning session. The chat
is ephemeral reasoning, never a protocol fact (P070 §1).

This is a use of the generic Room primitive, not a special Corpus room family.
Room provides the neutral substrate for many workflows; Corpus supplies only the
topic-expert deliberation protocol layered on top of that substrate.

`corpus-reasoning-room-policy.v1`: `exposure` (enum bound to P009 exposure modes, not a
new namespace), `answer/acceptance` (enum `chair-signed | n-of-m | unanimous`),
`chair/mode` (`requester-appointed` for MVP-of-this-layer, `elected` later),
`chair/nym` + `chair/credentials` (a capability-passport ref proving the chair is
authorized — not a bare nym), `quorum/required`, `tie-break`, `revocation-policy`, and
budgets `budget/time-ms` + `budget/steps` + `budget/tokens` (tokens matter because the
LLM cost is per-token, not only per-step).

**Chair before election.** For the first live layer the requester appoints a chair (or
acts as chair); a fallback/revocation policy is required even for that case. Full arbiter
**election** (eligibility, COI, quorum, deadline, tie-break, revocation, fallback) is a
later layer.

**Agent as chair delegate.** The requester MAY appoint its own host-owned Agent
(P073) as the chair delegate for the room, but this does not make the Agent a new
authority root. The room policy still names the accountable chair subject
(`chair/nym` + `chair/credentials`) and may additionally reference
`chair/agent-ref`; the host remains responsible for the Agent's budget,
lifecycle, grants, and stop/resume controls. An Agent-chair may coordinate the
discussion, propose turns, detect conflicts, request summaries, and propose the
final answer, but it cannot self-authorize publication, settlement, membership
changes, or effects outside the grants accepted by the host and the room policy.

**Room participants are subjects or Agents, not raw model adapters.** A Corpus
deliberation room may contain human participants, participant-controlled Agents,
or node/service roles represented by Agents. A raw Inquirium adapter or model
runtime MUST NOT appear as a room member. Inquirium is invoked by an Agent or by
another host-owned flow as bounded inference; it does not own room identity,
memory, lifecycle, budget, stop/resume semantics, or accountability. A
single-turn model response MAY be represented as a degenerate Agent profile with
one step, no fork, no durable autonomous memory, and an explicit budget.

**Participant roles and instruction overlays.** The chair MAY assign
deliberation roles to participants (for example `cxx-implementer`,
`code-reviewer`, `adversarial-critic`, `domain-summarizer`) through explicit
room/Corpus policy facts. These roles are not ambient authority and do not
override local node policy. They are task-shaping metadata consumed by each
participant's local Inquirium prompt-assembly policy. The chair MAY also propose
per-role or per-turn instruction overlays, but remote nodes treat them as
suggestions or bounded instruction profiles that must be locally accepted,
validated, classified, and budgeted before they enter the participant's prompt.
This prevents coordinator-controlled prompt injection while still allowing the
room to organize expert perspectives.

### 6. Answer Contract (concrete, content-addressed, signed)

Convergence yields one `corpus-reasoning-answer.v1`: `answer/id`, `query/id`, `room/id`,
`topic/term`, `corpus/taxonomy-digest`, `content/ref` **or** inline `content` **plus
`content/digest`** (so a verifier can confirm the inline content matches what was
signed), `answer/format` (`plain-text | markdown | json | edn`), `classification`
(the small `classification.v1` lattice tier `Public | Community | Personal`, expanded to a full `classification.v1` object at the AD answer-envelope boundary; see Resolved Decision 21), `policy/digest` (required),
`provenance/refs`, `contribution/refs`, `contributor/weights[]` (present even though
N-way settlement is post-MVP, so a later settlement can use the same answer),
`attestation/evidence` (e.g. the deliberation `room-event.v1` high-water mark, proving
the answer came from the room and not a single responder), and `signatures[]` per
`answer/acceptance`.

The first implemented single-provider slice uses a narrower but stricter contract:
`corpus-reasoning-answer.v1` is accepted only after schema validation, content digest
verification, signature verification, and round binding. The signer key must derive the
same `node:did:key` as `responder/node-id`; `responder/node-id` must match the provider
of the selected bid; `selected/bid-id`, when present, must match the round's selected
bid; and `policy/digest` must equal the round's `corpus/taxonomy-digest`. This makes
the answer a provider-originated fact attached to a selected round, not a requester-local
JSON note.

### 7. Settlement Bridge (single contracting provider for MVP)

For the MVP and first live layer there is **one contracting party** — a single
contracting provider, or the chair as counterparty — so settlement is the ordinary P011
path (`procurement-offer` → `procurement-contract` → `procurement-receipt`) with escrow
host-owned (P016). **N-way split is post-MVP**, deferred to a dedicated
`contribution-allocation.v1` (a candidate future proposal; the name prefix is reserved
here to avoid collisions), informed by the Creator-Credits attribution graph and by
`contributor/weights[]` already carried on the answer.

## Schema Conventions, Identifiers, and Invariants

All Corpus contracts MUST follow the repo's existing signed-artifact conventions (as in
`service-offer.v1`, `procurement-offer.v1`), not ad-hoc styles:

- **Schema version**: top-level `schema/v` is the numeric schema version (`1` for v1
  contracts), matching `service-offer.v1` and `procurement-offer.v1`. The contract name
  comes from the enclosing schema id or transport context; do not encode `name.vN` into
  `schema/v`. Embedded contracts that already use `schema` (for example
  `classification.v1`) keep their own discriminator.
- **Namespacing**: slash-namespaced, hyphenated segments — `query/id`, `room/id`,
  `bidder/node-id`, `topic/term`, `correlation/id`, `idempotency/key`, etc.
- **Identifier patterns** (explicit, required):
  - `query/id` `^query:[A-Za-z0-9][A-Za-z0-9:-]*$`; `bid/id` `^bid:…$`; `answer/id`
    `^answer:…$`; `room/id` `^room:…$`; `correlation/id` `^corr:…$`;
  - participants/nodes/nyms reuse the existing DID forms:
    `^participant:did:key:z[1-9A-HJ-NP-Za-km-z]+$`, `^node:did:key:z…$`,
    `^nym:did:key:z…$`.
- **Timestamps**: `created-at`, `published-at`, `expires-at`, `deadline-at`,
  `received-at`, `updated-at`, `valid-until` (RFC3339).
- **Price**: `pricing/*` for standing-offer/request *intent* (`pricing/amount`,
  `pricing/max-amount` [+ Corpus-only optional `pricing/min-amount`], `pricing/currency`,
  `pricing/unit`, `pricing/unit-kind` ∈ `per-item | per-character-block | per-request |
  per-task | flat`); `price/*` (`price/amount` + `price/currency`) only for a concrete
  bid/procurement price. Amounts are **integers in minor units**. MVP examples use `ORC`
  (`service-credit` is a future federated symbol, not used in MVP wire examples).
  Fractional per-token/per-step rates would need a separate pricing-calculator contract
  that resolves to an integer `pricing/amount` before it enters an offer/bid.
- **Signatures** (one canonical form): `signature: { alg: "ed25519", value: "…" }` for a
  single signer; `signatures: [ { by: "<did>", alg: "ed25519", value: "…" } ]` for
  multi-signer (the answer). Do not mix in `auth/nym-signature` for these contracts.
- **Canonicalization**: every signature and idempotency key is computed over
  `orbiplex-canonical-json-jcs-v1`, the language-neutral Corpus profile implemented by
  `node/canonical-json` as `CanonicalJsonProfile::JcsV1`. It sorts object keys
  recursively using JSON Canonicalization Scheme ordering, preserves array order,
  preserves string code points without NFC folding, emits the shortest stable JSON form
  without insignificant whitespace, and does not strip or transform fields unless the
  calling artifact contract explicitly defines a pre-canonicalization pruning step.
  Implementations MUST NOT perform Unicode normalization before canonicalization; UTF-8
  bytes are derived from the original JSON string code points. This makes replay
  protection real and cross-implementation stable.
- **Idempotency-key derivation**: default
  `idempotency/key = "sha256:" + base64url(sha256(canonical_json_string(<domain tuple>)))`,
  e.g. for a bid the tuple is `(query/id, bidder/node-id, decision, bid/valid-until)`.
- **Validation invariants** (JSON Schema where expressible; offer/catalog admission
  constrainers where the check depends on external artifacts):
  - `pricing/min-amount <= pricing/max-amount` (default `pricing/min-amount = 0` when
    omitted);
  - `deadline-at > created-at`; `valid-until > created-at`;
  - `corpus/topics ⊆ terms(corpus/taxonomy-digest)`;
  - taxonomy `term` unique; per-term `labels` `uniqueItems`;
  - `content/digest` matches the inline `content` when inline.
- **Classification**: the answer carries the small `classification.v1` lattice tier
  (`Public | Community | Personal`); the AD answer envelope maps it to a full
  `classification.v1` object (Proposal 047 / `classification.v1.schema.json`) with
  tier-correct `bound_subjects` at the envelope boundary. See Resolved Decision 21.
- **Privacy/retention**: room durability and retention for `room.v1` /
  `room-membership.v1` / `room-event.v1` are governed by **P070** policy; Corpus does not
  define its own retention and explicitly defers to P070's per-exposure retention rules.

## Data Contracts

| Schema | Status | Phase | Purpose |
|---|---|---|---|
| `topic-taxonomy.v1` | new | MVP | Signed, versioned, federated taxonomy governance artifact. |
| `topic-resolution.v1` | new | MVP | Signed resolver output: canonical term or ranked `ambiguous` (with `epsilon`, `matched/labels`). |
| `service-offer.v1` (`corpus` extension) | extend | MVP | `corpus/topics`, `corpus/model-class`, `corpus/taxonomy-digest`, `corpus/taxonomy-issuer`. |
| `corpus-reasoning-query.v1` | new | MVP | Corpus decorator over `question-envelope.v1`: topic, keywords, requester ids, price bracket, `max/candidates`, deadline. |
| `corpus-reasoning-bid.v1` | new | MVP | Envelope: `decision` + `bid/valid-until` + `policy/digest` + embedded `procurement-offer.v1`. |
| `corpus-reasoning-bid-state.v1` | new | MVP | Asker read-model: per-candidate state + timestamps + reason + AD `delivery/attempt-id`. |
| `corpus-reasoning-room-policy.v1` | new | post-MVP | Exposure, acceptance, chair + credentials, quorum, budgets (incl. tokens). |
| `corpus-reasoning-room-invite.v1` | new | post-MVP | Room subject + live-transport binding + policy digest. |
| `corpus-reasoning-role-assignment.v1` | new | post-MVP | Chair-issued participant role assignment with local-acceptance semantics. |
| `corpus-reasoning-instruction-overlay.v1` | new | post-MVP | Suggested per-role/per-turn instruction overlay consumed only through local prompt policy. |
| `corpus-reasoning-arbiter-nomination.v1` | new | later (Tracker P8) | Arbiter nomination (durable room record). |
| `corpus-reasoning-arbiter-vote.v1` | new | later (Tracker P8) | Arbiter vote (durable room record). |
| `corpus-reasoning-answer.v1` | new | post-MVP, first slice implemented | Content-addressed signed answer incl. `policy/digest` (required), `contributor/weights[]`. |
| `contribution-allocation.v1` | future (reserved) | post-MVP | N-way settlement split (separate proposal). |

Reused: `room.v1` / `room-membership.v1` / `room-event.v1` (P070),
`artifact-delivery-envelope.v1`, `deferred-operation-status.v1`, `procurement-offer.v1`,
`procurement-contract.v1`, `procurement-receipt.v1`, `classification.v1`.

## Relationship to Existing Mechanisms

- **Swarm Broadcast Assistance (077, advisory companion)**: an assistance
  request may hire a Corpus deliberation as one of its resolution steps, and a
  Whisper-born association room may use Corpus repeatedly (sponsored or
  gift-priced) — see `doc/project/20-memos/whisper-corpus-composition.md` for
  the composition decisions (side-room first, in-room later; the community-work
  marker stays coarse and never identifies the room).
- **Artifact Delivery (023)**: carries MVP procurement (query/bid), the room invite, and
  the final answer. Corpus is a second marketplace-style AD consumer after Arca/Dator. It
  does **not** carry the live chat.
- **Room (P070)**: live deliberation substrate and durable skeleton. Hard prerequisite
  for phase 2. **Corpus imposes specific transport requirements on P070**: low latency,
  no retention, and a small participant count. These belong in P070's live-transport
  profile as input requirements.
- **Question Envelope (P003)**: `corpus-reasoning-query.v1` decorates
  `question-envelope.v1`; Corpus does not create a parallel question primitive.
- **Arca/Dator/offer-catalog (003/004/067)**: extended with `corpus/topics` indexing, not
  forked.
- **Inquirium (P063/P064/P066)**: per-participant model access via a full
  thread/session runtime with tool support is the target prerequisite for phase 2.
- **P011 / story-006 / P016**: procurement lifecycle and escrow.
- **Classification (047)**: the answer carries a small `classification.v1` lattice
  tier, mapped to a full `classification.v1` object at the AD answer envelope.
- **P057 notifications**: requester/operator notifications for bids, readiness, answer.

## Failure Modes and Mitigations

### Mechanical

| Failure mode | Risk | Mitigation |
|---|---|---|
| Ambiguous topic forced to a wrong term | Misrouted experts | Resolver returns `ambiguous` + `matched/labels`; asker disambiguates. |
| Silence conflated with refusal | Lost signal, wrong retries | `corpus-reasoning-bid-state.v1` distinguishes states with timestamps + reason. |
| Arbitrary topic strings indexed | Catalog pollution | `corpus/topics ⊆ terms(taxonomy/digest)` offer/catalog admission constrainer; missing or untrusted taxonomy fails closed. |
| Stale bid reused later | Wrong contract | `bid/valid-until` TTL. |
| Inline answer tampered after signing | Forged answer | `content/digest` self-reference + canonical-json signatures. |
| Replay of bids/invites | Duplicate work | Canonical idempotency keys + `correlation/id`/`query/id`. |
| Chat treated as a shared fact | Reification / privacy leak | Protocol never persists chat (P070); capture is private, classified. |

### Abuse model (LLM + marketplace)

| Abuse | Risk | Mitigation |
|---|---|---|
| Fake expertise offers | Low-quality answers | Reputation-weighted selection; post-answer rating; provider stake. |
| Topic stuffing | Offer spam | Bounded `corpus/topics`; topic⊆taxonomy gate; reputation penalty. |
| Collusive bids | Price fixing | Cartel detection on reputation graph; diversify selection; requester caps. |
| Prompt injection in the room | Hijacked reasoning | In-room content is untrusted input to Inquirium; per-node guardrails; chair review. |
| Leakage via answers | Exfiltration | `classification.v1` + egress guard; private capture stays local. |
| Price griefing / budget exhaustion | Cost attacks | Brackets, `budget/time-ms|steps|tokens`, Inquirium caps, escrow precheck. |
| Taxonomy poisoning | Misrouting | Signed `topic-taxonomy.v1` (issuer key, validity, supersession proof); pinned digest. |

## Trade-offs

- **Benefits**: MVP reuses existing procurement/delivery; live chat (later) gives low
  latency; ephemeral reasoning keeps memory small; forces the Room consolidation (P070).
- **Costs**: phase 2 depends on two unbuilt prerequisites; new (separated) N-way
  settlement; a taxonomy governance surface to curate and sign.

## Resolved Decisions

1. **Identifier governance.** `query:` / `room:` / `answer:` prefix allocation is a core
   protocol registry concern, not a per-federation policy surface.
2. **JSON canonicalization across implementations.** Corpus uses
   `orbiplex-canonical-json-jcs-v1` for signatures, digests, and idempotency keys. The
   Rust implementation is `node/canonical-json::CanonicalJsonProfile::JcsV1`, and the
   profile is specified here as a language-neutral contract rather than as a Rust-only
   behavior.
3. **Taxonomy migration between versions.** Providers and requesters may resolve against
   both the old and new taxonomy only when a valid supersession proof links the two
   digests. Without such proof, exact digest mismatch fails closed.
4. **Query vs `question-envelope.v1`.** `corpus-reasoning-query.v1` is a decorator over
   `question-envelope.v1`, not a sibling question primitive.
5. **Canonical topic hashing.** `taxonomy/digest` is byte-stable canonical JSON over the
   taxonomy artifact. `topic/term` is an exact wire string; no Unicode folding or
   case-insensitive normalization is performed in the wire contract.
6. **Discovery style.** Catalog-rich discovery through the offer-catalog topic index is
   the default. `capability-many` remains available as an explicit addressing mode, not
   the default.
7. **Chair vs election.** MVP uses requester-appointed chair. Arbiter election is
   post-MVP.
8. **Pricing model.** MVP uses flat per-answer minor-unit pricing. A pricing-calculator
   contract is deferred until token/step/participant pricing is required.
9. **N-way settlement.** `contribution-allocation.v1` becomes a separate proposal; P069
   only reserves the name and carries references/weights needed by that future contract.
10. **Bid-state retry strategy.** Requester local policy decides retry budget and
    backoff. AD reports delivery state and diagnostics; it does not own Corpus retry
    semantics.
11. **Inquirium session surface.** Phase 2 targets a full Inquirium thread/session
    runtime with tools, not a minimal single-call or minimal open/continue/close surface,
    because the component is strategically required beyond Corpus.
12. **Shared semantic validators.** `schema-gate` depends on
    `orbiplex-node-corpus-core` for Corpus taxonomy/query semantic validation. This keeps
    tree, digest, topic, price, and bid-state invariants in one semantic kernel rather
    than maintaining an independent edge-validator copy.
13. **Empty bid-state representation.** `corpus-reasoning-bid-state.v1` may represent
    discovery or dispatch failure before candidate selection as `candidates: []`.
    Requesters should not invent synthetic candidate rows for providers that were never
    selected.
14. **`extensions` byte budgets.** Corpus `extensions` fields on query, bid, taxonomy,
    and resolution artifacts have a maximum canonical JSON size of 16 KiB per field.
    Admission must reject larger extension payloads before network fan-out or digest
    materialization.
15. **Trusted taxonomy loader boundary.** Corpus offer admission is performed through a
    taxonomy-aware loader/verifier path. The generic service-offer catalog remains
    reusable and does not become a Corpus governance authority; Corpus indexing and
    production admission fail closed when trusted taxonomy material is missing.
16. **Taxonomy issuer trust policy.** Taxonomy issuer acceptance uses a composed trust
    policy: local node policy is authoritative for local use, while Seed Directory
    governance facts and/or Agora authority records may supply scoped trust evidence.
    No single published fact becomes a trust decision without local policy acceptance.
17. **AD-mediated answer delivery.** Production provider answer delivery uses a normal
    `artifact-delivery-envelope.v1` carrying `corpus-reasoning-answer.v1`; Corpus does
    not define a separate `corpus.answer` transport. The local
    `POST /v1/corpus/rounds/{query_id}/answers` surface remains operator/test/admin
    control-plane only, while requester nodes admit provider answers through the
    in-process AD `corpus.answer` acceptor.
18. **Zero-bid operator notification.** `no-routable-candidates` and `no-provider-bids`
    stay synchronous dispatch diagnostics by default. P057 notifications are emitted
    only when Corpus policy explicitly enables retry/escalation visibility for such
    zero-bid states.
19. **Story-011 trust hardening.** Story-011 should run under full `sovereign-policy`
    verification rather than `signature-only`; acceptance coverage should exercise the
    production trust mode instead of the shortcut fixture mode.
20. **Direct bid registration surface.** `POST /v1/corpus/bids` remains a local-control
    operator/test helper, requires bid signature verification, and is not a remote
    federation surface.
21. **Classification propagation.** `corpus-reasoning-answer.v1` carries the small
    `classification.v1` lattice tier (`Public`, `Community`, or `Personal`) and the AD
    answer envelope maps it to a full `classification.v1` object with tier-correct
    `bound_subjects` supplied by the provider/requester context. `Confidential` is
    intentionally not a Corpus answer tier in this phase: confidential deliberation is
    modeled by room/private capture and local policy, while a final answer artifact must
    stay in the Public/Community/Personal lattice. Missing answer classification is
    treated as `Public` only for legacy/admin compatibility; production providers SHOULD
    set it explicitly. `corpus-reasoning-query.v1` should still grow a first-class
    classification field before Personal or higher-tier Corpus queries are supported.
22. **Answer revision validation.** A local answer read-model may replace an answer by
    the same `answer/id` or by a new answer whose `supersedes` points at an existing
    answer from the same responder. If `revision/no` is present, the first revision is
    `1` and a superseding revision must be greater than the superseded revision. The
    counter is advisory for humans and diagnostics; append-only fact order plus the
    `supersedes` edge remains authoritative.

## Open Questions

No open questions remain for the hard-MVP procurement slice. Post-MVP live
deliberation questions are tracked under the Room/Inquirium/Agent phases below.

Resolved answer publication decision: local daemon round snapshots may replace a repeated
`answer/id` or a superseded answer as a latest read-model convenience, after signature,
selected-bid, and policy-digest validation. Federated answer publication is append-only:
an updated answer is a new `corpus-reasoning-answer.v1` fact with `supersedes` and
optional `revision/no`, not an overwrite. Local validation rejects dangling
`supersedes` references, cross-responder supersession, and non-monotonic advisory
revision numbers.

## Implementation Contract

This section is the execution bridge between the proposal and code. Runtime work MUST
advance slice-by-slice, and each runtime slice is blocked until its contract gate is
complete. Corpus should not introduce ad-hoc payloads in middleware or AD before the
corresponding canonical schema, examples, validation path, and negative tests exist.

### Substrate and Canonicalization

Corpus separates domain payloads from their durable carrier:

- durable/federated Corpus facts are published as `agora-record.v1` envelopes with
  `content/schema` set to the Corpus schema name and `content` set to the domain payload;
- local read-models such as `corpus-reasoning-bid-state.v1` are host-owned projections,
  not Agora authority;
- `record/id`, `author/participant-id`, `author/nym-proof`, `record/parent`,
  `record/supersedes`, relay metadata, and envelope signatures remain Agora envelope
  concerns when the payload is published through Agora;
- all Corpus signatures, digests, idempotency keys, and content-addressed refs use
  `orbiplex-canonical-json-jcs-v1`, whose Corpus test vector is:

```json
{
  "input": {"z": [3, 2, 1], "a": {"b": true, "a": "ą"}, "n": 1},
  "canonical": "{\"a\":{\"a\":\"ą\",\"b\":true},\"n\":1,\"z\":[3,2,1]}",
  "digest": "sha256:r2bAYdhk5FfM2FDmWq2HlGY4jDKM2Dcg6SG84tw7g7o"
}
```

Artifact-specific host-owned fields, such as `taxonomy/digest`, are removed only when
the artifact contract says so before canonicalization. The canonical JSON profile itself
does not know domain fields.

The first contract gate must define which Corpus payloads are public/federated Agora
facts and which are local control-plane projections. The expected default is:
`topic-taxonomy.v1`, `topic-resolution.v1`, `corpus-reasoning-bid.v1`, and final
`corpus-reasoning-answer.v1` may be Agora-carried facts; `corpus-reasoning-bid-state.v1`
remains local to the requester.

### MVP Contract Gate

The MVP procurement slice may start only after these contract artifacts exist:

1. `topic-taxonomy.v1` schema with positive/negative examples, signed fixture, and
   canonical digest rule.
2. `topic-resolution.v1` schema with `resolved`, `ambiguous`, and `unresolved` fixtures.
3. `service-offer.v1` Corpus extension contract: `corpus/topics`,
   `corpus/model-class`, `corpus/taxonomy-digest`, and `corpus/taxonomy-issuer`.
4. `corpus-reasoning-query.v1` as a decorator over `question-envelope.v1`, with
   examples showing the underlying question envelope fields and Corpus extension fields.
5. `corpus-reasoning-bid.v1` as an envelope over schema-valid `procurement-offer.v1`.
6. `corpus-reasoning-bid-state.v1` as an asker-owned read-model, not a wire authority.
7. Schema-gate sync to `node/protocol/contracts`, plus admission constrainers for checks
   that depend on external artifacts, especially `corpus/topics ⊆ terms(taxonomy/digest)`.
8. Refusal/replay tests for invalid signatures, stale deadlines, invalid taxonomy
   supersession, duplicate idempotency keys with different payloads, and offer
   withdrawal between discovery and dispatch.

The post-MVP live-deliberation slice has a separate gate: P070 Room contracts, the
Agent organ (P073) bounded reasoning session, `corpus-reasoning-room-policy.v1`,
`corpus-reasoning-room-invite.v1`, and `corpus-reasoning-answer.v1`.

### Host Runtime Reuse

Corpus must reuse existing host-owned primitives instead of creating parallel runtime
machinery:

- **Artifact Delivery (023)** owns fan-out, delivery diagnostics, retry surfaces, and
  transport-specific failures.
- **Bounded Deferred Operations (029)** owns long-running query/bid/settlement handles
  that cannot complete synchronously.
- **Replay Scheduler (020)** owns periodic cleanup/retry wakeups for bid-state and
  catalog projections.
- **Inquirium (063/064/066)** may be used by a provider as a local model executor for
  drafting an answer, but it is not a Corpus room participant, chair, or settlement
  authority. The provider host turns local Inquirium output into a signed
  `corpus-reasoning-answer.v1` fact.
- **Temporal Storage Convention (028)** owns retention, compaction, and bounded replay
  rules for local bid-state projections.
- **Middleware (019)** is the extension surface for supervised provider acceptors; it
  does not own Corpus state semantics.
- **P011/P016** own procurement, contracts, receipts, disputes, and escrow after a bid is
  selected.

### Capability and Service Type Boundary

`corpus.provider` is both an operational capability and a marketplace-visible service
category, but those layers must not be conflated:

- `capability_id = "corpus.provider"` is the routing/authorization capability used by
  AD, passports, and local allow policy;
- `service-offer.v1.service/type = "corpus.provider"` is the advertised marketplace
  category exposed through Dator/offer catalog;
- topic expertise is never embedded into the capability id; it remains offer/passport
  data (`corpus/topics`, `corpus/taxonomy-digest`, `topic/term`);
- before runtime implementation, `corpus.provider` must be added to the capability
  registry and linked to the `service-offer.v1` Corpus extension.

### External Call Budgets

Every Corpus path that crosses a component or node boundary must carry explicit budgets:

- AD fan-out uses `max/candidates` as a hard cap; the initial implementation default is
  `50` unless a stricter federation or requester policy is configured.
- Query dispatch has a request timeout, max response bytes, retry budget, backoff with
  jitter, and terminal failure class.
- Provider bid acceptors have a bounded execution time and must return a retryable vs
  terminal failure classification.
- Catalog lookups must cap result count and page size before AD target expansion.
- Settlement handoff inherits P011/P016 timeout and idempotency rules.

Budget exhaustion is diagnostic data. It must not be reinterpreted as provider refusal.

### Identifier and Idempotency Rules

Identifier patterns are contract, not UI labels:

- `query/id`: `^query:[A-Za-z0-9][A-Za-z0-9:-]*$`;
- `bid/id`: `^bid:[A-Za-z0-9][A-Za-z0-9:-]*$`;
- `answer/id`: `^answer:[A-Za-z0-9][A-Za-z0-9:-]*$`;
- `topic/term`: exact taxonomy term string, case-sensitive, no wire-time Unicode folding.

Default query idempotency key:

```text
sha256(canonical_json({
  question/id,
  requester/node-id,
  topic/term,
  corpus/taxonomy-digest,
  pricing/min-amount,
  pricing/max-amount,
  pricing/currency,
  deadline-at
}))
```

Default bid idempotency key:

```text
sha256(canonical_json({
  query/id,
  bidder/node-id,
  decision,
  bid/valid-until,
  procurement-offer.digest-or-null
}))
```

The schema/admission layer must enforce `pricing/min-amount <= pricing/max-amount` and
`deadline-at > created-at`.

### Runtime Components

MVP implementation should be stratified into small components:

1. **Topic taxonomy loader/verifier**: resolves trusted taxonomy artifacts by digest,
   verifies issuer/signature/supersession, and exposes immutable taxonomy values to
   resolver and catalog admission code.
2. **Deterministic topic resolver**: pure weighted matcher over a taxonomy value,
   returning `topic-resolution.v1`.
3. **Offer-catalog topic index**: projects active `service-offer.v1` records into
   `topic/term -> offer refs`, including parent-term fallback and supersession. The
   public query surface is path-first:
   `GET /v1/offer-catalog/corpus/taxonomies/{taxonomy_digest}/topics/{topic}/offers`.
   Runtime toggles that would make the path noisy or inefficient stay in query
   parameters, for example `limit`, `offset`, and `active=false`. The response exposes
   `has_more` and HATEOAS-style `links.self` / `links.next` / `links.prev` where
   applicable. `service/type = "corpus.provider"` is fixed by the `corpus` path segment,
   not a caller-selected query parameter.
4. **Corpus query dispatcher**: builds a `question-envelope.v1` + Corpus decorator,
   selects candidate targets from the catalog-rich index, and submits one AD fan-out.
5. **Provider bid acceptor**: validates query authority, deadline, taxonomy digest,
   local capability, and price constraints before returning `corpus-reasoning-bid.v1`.
6. **Bid-state read-model**: aggregates AD delivery attempts, received bids, declines,
   timeouts, and retry decisions without treating silence as refusal.
7. **Single-provider settlement bridge**: converts the selected bid's embedded
   `procurement-offer.v1` into the ordinary P011/P016 contract/receipt path.

### State Machines

Topic resolution states are closed for MVP:

```text
unresolved
ambiguous
resolved
```

`ambiguous` is not an error; it is a decision point requiring requester
disambiguation. `unresolved` is a terminal no-routing result unless the requester
changes keywords or taxonomy.

Bid-state values are requester-local:

```text
candidate-selected
query-sent
bid-received
declined
countered
timed-out
delivery-failed
unreachable
retry-scheduled
selected
rejected
settled
```

Only `bid-received` or explicitly accepted `countered` candidates are eligible for
selection. `delivery-failed` and `unreachable` flow into requester local retry policy;
AD reports diagnostics but does not decide Corpus retry semantics.

### Bid-State Lifecycle

`corpus-reasoning-bid-state.v1` is a requester-owned temporal projection:

- **owner**: requester node;
- **key**: `(query/id, candidate node/id)`;
- **idempotency**: `(query/id, candidate node/id, delivery/attempt-id)` plus canonical
  bid digest when a bid is received;
- **retention**: active until query deadline, selected settlement completion, or terminal
  cancellation; after that, compact according to the Temporal Storage Convention;
- **cleanup trigger**: `deadline-at + local grace period`, settlement completion, or
  explicit requester cancellation;
- **indexes**: `query/id`, `candidate node/id`, state, `deadline-at`, and
  `delivery/attempt-id`;
- **safety rule**: cleanup must not remove an active settlement, active deferred
  operation, or unresolved dispute.

### Room Integration Contract

Post-MVP live deliberation must use P070 instead of inventing a Corpus room:

- Room is independent infrastructure. It owns room identity, membership,
  presence, lifecycle, live transport, attestations, projections, and generic
  room events. Corpus is only one consumer.
- `corpus-reasoning-room-policy.v1` is a Corpus decorator over `room-policy.v1`; it adds
  chair/acceptance/quorum/budget fields but does not replace room access policy.
- `chair/agent-ref` may name a requester-owned Agent acting as the chair delegate, but
  the accountable chair subject and credentials remain explicit in the room policy.
- Live-room speakers are accountable subjects or Agents. Raw Inquirium adapters and
  model runtimes are inference providers only and must not be admitted as room members;
  single-turn model participation is represented as a degenerate Agent profile.
- `corpus-reasoning-room-invite.v1` references `room.v1`, the live transport binding, and
  the room access list; actual join decisions rely on P070 membership attestations.
- `corpus-reasoning-role-assignment.v1` records task roles for participants. A role is
  valid only after local participant acceptance or local policy acceptance, and it cannot
  widen the participant's authority, classification ceiling, or grants.
- `corpus-reasoning-instruction-overlay.v1` records suggested prompt/instruction
  overlays for a role or turn. It is never injected directly into a remote model prompt;
  each participant's local Inquirium prompt-assembly policy decides whether and how to
  apply it.
- `corpus-reasoning-answer.v1` cites `room/id`, `room-event/high-water`, policy digest,
  and relevant provenance refs. It must not embed live chat content.
- room authority, revocation, retention, live transport, and membership projection remain
  P070 responsibilities.

### Adoption and Migration Plan

Corpus is a new role, but it modifies adjacent projections:

1. Existing service offers remain valid; only offers that opt into the Corpus extension
   enter the topic index.
2. Shared Offer Catalog (P067) adds the topic index as a projection over existing
   `service-offer.v1` records; it does not replace the base offer catalog.
3. P011 procurement artifacts are reused unchanged; Corpus only supplies the query/bid
   wrapper and the selected embedded `procurement-offer.v1`.
4. No historical records are migrated into Corpus automatically. Operators may publish
   new Corpus-extended offers when providers intentionally opt in.

### Admission and Failure Rules

Corpus admission MUST fail closed for:

1. missing, untrusted, expired, or unverifiable taxonomy material;
2. `corpus/topics` that are not terms of the pinned taxonomy;
3. taxonomy migration without a valid supersession proof;
4. stale bids (`bid/valid-until <= now`) or queries past `deadline-at`;
5. embedded `procurement-offer.v1` that fails the existing procurement schema;
6. price outside the requester bracket unless `decision = "counter"`;
7. duplicate bids with the same idempotency key but different canonical payload digest;
8. missing requester authority, missing reply target, or mismatched `question/id`;
9. provider offers that were withdrawn or superseded before query dispatch;
10. classification/egress violations on final answers.

Failures should be diagnostic events with redacted payload references, not silent drops.

### MVP Acceptance Slice

The first acceptance pack should prove the narrow MVP without rooms:

1. one requester, two providers, one signed taxonomy, and one topic term;
2. both providers publish Corpus-extended `service-offer.v1` records;
3. requester resolves keywords to the canonical topic and queries the catalog topic index;
4. requester broadcasts one `corpus-reasoning-query.v1` over AD to selected targets;
5. one provider returns an `accept` bid with embedded schema-valid `procurement-offer.v1`;
6. the other provider returns `decline` or times out, and bid-state distinguishes both;
7. requester selects one bid and completes the single-provider P011/P016 settlement path;
8. replay or repeated dispatch is idempotent and does not create duplicate selected bids.

## Implementation Recommendations

These recommendations are implementation guidance for the Corpus role and protocol.
They are intentionally more concrete than the architecture model above, but they do not
replace the canonical schemas, schema-gate checks, or tracker. Field names in examples
follow §Schema Conventions; final schemas are gated in `doc/schemas/` and the node
schema-gate. `…` elides obvious values.

### Design Commitments

Corpus is a thin domain layer over existing host-owned strata. It MUST NOT become a
second marketplace, a second delivery system, a second room system, or a second LLM
session runtime. Its implementation should add only the domain vocabulary needed for
topic-routed collaborative reasoning: topic taxonomy, topic resolution, Corpus-extended
offers, query/bid facts, requester-local bid state, and later Corpus-specific room
decorators.

The MVP implementation should optimize for contract clarity over clever routing. Each
state transition should be explainable as data: taxonomy material is verified, keywords
resolve to a topic, topic-scoped offers project into an index, one AD fan-out is planned,
bids are admitted or rejected, bid-state is updated, and one accepted bid bridges into
the existing procurement path. Hidden in-memory shortcuts are acceptable only as caches
over these facts, never as the source of authority.

### Primary Rule: Compose Existing Authorities

Corpus coordinates expertise; it does not own the authority of adjacent systems. Artifact
Delivery owns delivery attempts and transport diagnostics. Dator/offer catalog owns
service offers and topic projections. P011/P016 own procurement, contracts, escrow, and
receipts. Room owns room identity, membership, live transport, presence, and room
projection. Inquirium owns model inquiry through host-selected runtime candidates.

Implementation should therefore pass typed data across those boundaries rather than
calling through private APIs. For example, a Corpus query dispatcher may build an AD
delivery envelope, but it must not directly mutate AD delivery state. A Corpus settlement
bridge may export the selected embedded `procurement-offer.v1`, but it must not create a
parallel settlement ledger. This keeps Corpus understandable as a role and protocol
instead of a hidden orchestration subsystem.

### Reuse Map (existing components, do not reinvent)

The Primary Rule is operationalized by reusing these existing strata rather than
rebuilding them inside Corpus:

| Corpus need | Reuse | Note |
| --- | --- | --- |
| Bounded reasoning session (deliberation) | Agent organ (P073); `agent-core` budget/controller | Deliberation `budget` (`time-ms`/`steps`/`tokens`) is the Agent budget contract, not a Corpus-local one. |
| `corpus.provider` capability id + admission | Capability Registry (P072 / Solution 037) | Register `corpus.provider`; admission is fail-closed via the registry, not a Corpus allow-set. |
| Taxonomy / resolution / answer signing | `agora-core` canonical (deterministic, domain-separated) | Same canonicalization discipline as `node-advertisement.v1`; no Corpus-specific canonical form. |
| Query dispatch + bid collection to a deadline | Bounded Deferred Operations (Solution 029) | Operation id, status, cancellation, deadline — not a Corpus-private task queue. |
| `retry-scheduled` dispatch retries | Replay Scheduler (Solution 020) | Backoff/jitter/launch accounting — not a private timing loop. |
| Answer provenance / durable facts | Memarium fact-plane; object-store / AD for large content (`content/ref`) | Answer facts are Memarium facts; bulk content stays by reference. |
| Answer acceptance (verified / refuted / amended) | `inquirium.inquiry-feedback.v1` (P066) | Reuse the inquiry-feedback contract pattern for chair-signed acceptance. |
| Deliberation room + attestation | Room (P070) "Corpus Deliberation Rooms" hook (Solution 036); high-water attestation | Already reused (`room-event/high-water`); decorate room policy, do not fork a room model. |
| Delivery / settlement / escrow | AD (Solution 023); P011 procurement; P016 escrow | Bridge to these; never a parallel ledger. |

**Stratify Corpus the same way as the other organs.** The pipeline stages below
are pure functions and narrow ports, so Corpus should follow the `<organ>-core` /
daemon template (DEV-GUIDELINES Layering 5) already used by `inquirium-core` and
`agent-core`: a thin `corpus-core` crate owning the contracts, the deterministic
resolver, the pipeline stages, the typed failure taxonomy, and the effect-intent
values (`DispatchPlan`, `BidAdmissionDecision`, `SelectionDecision`,
`SettlementBridgeIntent`); the daemon performs effects (AD dispatch, persistence,
settlement bridge) and supplies the read-ports. Guard the crate with a
dependency-direction lint mirroring `check-inquirium-core-deps.py`, so Corpus
never accretes daemon coupling. Decisions are values; the daemon is the imperative
shell.

### Corpus Vocabulary and Strata

Use the following implementation vocabulary consistently:

- **taxonomy artifact**: signed, content-addressed taxonomy material;
- **trusted taxonomy**: a host-loaded taxonomy value that has passed issuer, signature,
  validity, supersession, and digest checks;
- **topic resolution**: deterministic resolver output for one keyword set under one
  trusted taxonomy digest;
- **Corpus-capable offer**: a normal `service-offer.v1` with a valid Corpus extension;
- **topic index entry**: read-model projection from active Corpus-capable offers;
- **Corpus query**: requester-owned question decorator plus topic and pricing bracket;
- **Corpus bid**: provider response envelope around an embedded procurement offer;
- **bid state**: requester-local temporal read-model, never a federated authority;
- **selected bid**: one admitted bid chosen by local selection policy;
- **settlement bridge**: conversion from selected bid to the existing P011/P016 path;
- **Corpus-on-Room**: post-MVP deliberation protocol layered on generic Room.

These names should appear in code modules, tests, operator status, and tracker evidence.
Avoid names such as `room_for_corpus`, `corpus_delivery`, or `corpus_contract` when they
suggest ownership that belongs to Room, AD, or procurement.

### Phase Boundary: Procurement First, Live Deliberation Later

The MVP procurement slice must remain shippable without Room live transport and without
the Agent organ (P073) reasoning session. It should prove that a requester can discover
topic experts, solicit bids, select one provider, and enter the existing settlement path.
That is the first useful vertical slice and the least entangled one.

Live deliberation is a later layer. It should start only after P070 live-plane runtime
integration and the Agent organ (P073) runtime exist. Corpus should not fill
that gap with a smaller ad-hoc chat loop, temporary room model, or direct model adapter
membership. The boundary is important: MVP Corpus procurement can mature independently,
while Room and Inquirium continue to harden as reusable primitives.

### Request Pipeline as Explicit Stages

Implement the MVP request path as explicit stages with stable intermediate values:

1. **Load taxonomy**: resolve trusted taxonomy material by digest and issuer policy.
2. **Resolve topic**: transform keywords into `topic-resolution.v1`.
3. **Select offers**: query the topic index under the chosen taxonomy digest.
4. **Plan dispatch**: construct one bounded AD fan-out plan.
5. **Admit bids**: validate bid envelope, embedded procurement offer, deadline, price,
   requester/provider identities, taxonomy digest, and idempotency key.
6. **Update bid-state**: append or recompute requester-local projection facts.
7. **Select bid**: choose from eligible accepted/countered bids using local policy.
8. **Bridge settlement**: hand the selected procurement offer to P011/P016.

Each stage should be testable as a pure function or a narrow port. The daemon or host
composition root may perform persistence and side effects, but domain decisions should
remain data-driven and replayable from inputs.

### Taxonomy Loader and Resolver

The taxonomy loader is a trust boundary. It should accept only signed, valid,
content-addressed taxonomy artifacts from configured issuers or governance roots. It
should return immutable trusted taxonomy values to downstream code; downstream code
should never re-parse untrusted taxonomy JSON from arbitrary Corpus payloads.

The resolver should be pure and deterministic. Unicode normalization, label matching,
weighting, epsilon comparison, ranking, and tie-breaks must be pinned by tests and
fixtures. `ambiguous` is a normal outcome requiring requester choice; it must not be
silently collapsed to the first candidate. `unresolved` is a terminal no-route result
unless the requester changes keywords or taxonomy.

### Offer Projection and Capability Boundary

The Corpus offer index should be a read-model over ordinary `service-offer.v1` records.
Only offers with `service/type = "corpus.provider"` and a valid Corpus extension enter
the topic index. Invalid Corpus extensions should fail closed for Corpus indexing while
leaving the base offer record available to non-Corpus consumers if it is otherwise valid.

The `corpus.provider` capability identifies the service class, not the topic. Topic
expertise belongs in offer/passport data (`corpus/topics`, `corpus/taxonomy-digest`,
`corpus/model-class`) and in the topic index. Do not mint capability IDs such as
`corpus.provider.cpp`; that would mix routing authority with evolving domain taxonomy.

Provider status is opt-in and conjunctive. A node is a Corpus provider only when it
publishes a Corpus-capable `service-offer.v1`, carries or publishes an accepted
`corpus.provider` capability passport, and exposes a Corpus query acceptor. A generic
daemon that merely has the code installed must not auto-publish `corpus.provider` nor
accept Corpus queries by default.

### Dispatch and Bid-State Ownership

AD owns delivery attempts; Corpus owns the interpretation of those attempts for one
reasoning query. The bid-state projection should distinguish `declined`, `timed-out`,
`delivery-failed`, `unreachable`, and `retry-scheduled`. Silence is not refusal, and a
delivery failure is not a provider judgment.

Bid-state should be append/recompute friendly. Persist enough stable keys to make replay
idempotent: `(query/id, candidate node/id, delivery/attempt-id)` and the canonical bid
digest when present. A duplicate idempotency key with the same canonical digest is a
replay; the same key with a different digest is an admission failure.

### Selection and Settlement Boundary

Selection is requester-local policy over admitted bids. It should never mutate a
provider's embedded `procurement-offer.v1`; if the price is outside the bracket, reject
or counter according to the bid decision contract. The first implementation may choose
the cheapest valid accepted bid with deterministic tie-breaks, but the selection
decision should be recorded as a fact or operator-visible transition.

After selection, Corpus should hand off to the existing procurement path. The settlement
bridge should export the selected embedded offer, selected bid digest, provider identity,
and query id. It should not create Corpus-specific escrow, receipt, dispute, or contract
records. If settlement fails after selection, the round should move to an explicit
operator-visible recovery state instead of silently selecting another provider.

### Room and Inquirium Composition

Post-MVP Corpus deliberation should compose Room and Inquirium as independent strata.
Room supplies accountable participants, membership, access policy, live transport,
presence, revocation, and high-water attestations. Inquirium supplies bounded inference
through host-selected runtime candidates and prompt assembly policy. Corpus supplies
topic-expert roles, deliberation policy, answer acceptance, and answer provenance.

The implementation must not admit raw model adapters as room participants. If a model
participates in deliberation, it does so through the host-owned Agent organ (P073), or a
degenerate single-turn Agent profile, with explicit budget and accountability; the
deliberation budget is the Agent budget/controller contract, not a Corpus-local one.
Corpus instruction overlays are suggestions consumed by each participant's local Inquirium
policy; they are not remote prompt injection.

### Operator Status and Observability

Expose Corpus progress as operator-facing state rather than logs only. A useful MVP
status shape includes: `query/id`, topic resolution result, taxonomy digest, selected
candidate count, delivery attempts by state, admitted bid count, selected bid, settlement
state, and next operator action if blocked. Do not include full question text in generic
operator traces when a digest/ref is enough.

Trace records should preserve causality: keyword resolution, offer index snapshot,
dispatch plan, delivery attempt ids, bid admission decisions, selection decision, and
settlement bridge outcome. Payloads that may contain private question text, answer text,
or provider-specific details should be referenced by digest or artifact ref and governed
by classification.

### Failure Taxonomy

Use typed failure classes instead of free-form strings at boundaries. At minimum:
`taxonomy-untrusted`, `taxonomy-expired`, `topic-unresolved`, `topic-ambiguous`,
`offer-invalid`, `offer-withdrawn`, `dispatch-failed`, `bid-invalid`, `bid-stale`,
`price-out-of-bracket`, `duplicate-conflict`, `selection-empty`,
`settlement-unavailable`, and `settlement-failed`.

Each failure class should declare whether it is retryable, operator-actionable, or
terminal for the current query. For example, `topic-ambiguous` is operator-actionable,
`dispatch-failed` may be retryable, and `duplicate-conflict` is fail-closed until the
conflict is inspected.

### Conformance, Golden Fixtures, and Test Gates

Before runtime wiring, ship schema and semantic gates for every Corpus payload. Positive
fixtures should include the happy-path procurement slice. Negative fixtures should cover
invalid taxonomy signatures, duplicate terms/labels, invalid supersession, ambiguous and
unresolved resolution, invalid topic references in offers, stale deadlines, price
bracket violations, bidder/responder mismatch, duplicate idempotency conflicts, and
invalid bid-state transitions.

The acceptance pack should exercise one requester and two providers end to end without
requiring Room. It should prove that a decline is distinct from timeout, that repeated
dispatch is idempotent, that withdrawn offers are not selected, and that only an
admitted selected bid can reach settlement. The later live-deliberation pack should be
separate and blocked on P070/Inquirium readiness.

### Performance and Resource Hardening

Corpus paths are fan-out paths, so default limits matter. Cap taxonomy size, label count,
keyword count, candidate count, AD target count, bid-state rows per query, response
bytes, and settlement retry attempts. Catalog queries should page before target
expansion, and the dispatcher should never create unbounded per-provider tasks.

All payload byte budgets should be checked before canonicalization where possible and
again after canonicalization where the digest/idempotency contract depends on bytes.
Large answer content belongs in the artifact store by reference, not inline in Corpus
state or bid-state projections.

### Adoption Strategy

Adopt Corpus by adding projections and contracts, not by migrating historical records.
Existing offers remain valid. Providers opt in by publishing Corpus-capable offers.
Operators can stage rollout by first enabling trusted taxonomy loading and topic-index
projection, then requester-side query dispatch, then provider bid acceptors, and finally
the settlement bridge.

The first production-ready switch should be conservative: no live rooms, no N-way
settlement, no automatic fallback to untrusted taxonomy material, no implicit provider
selection after settlement failure, and no direct model orchestration outside Inquirium.

### Reference Wire Shapes

### A. Signed Topic Taxonomy and Deterministic Resolver

```json
{
  "schema/v": 1,
  "taxonomy/id": "orbiplex.core", "federation/id": "orbiplex",
  "version": "2026.06.0", "versioning/scheme": "calver", "digest": "sha256:...",
  "issuer/nym": "nym:did:key:z...", "issuer/public-key-ref": "key:did:key:z...",
  "valid/from": "2026-06-01T00:00:00Z", "valid/until": "2027-06-01T00:00:00Z",
  "supersedes": "sha256:...prev...", "supersession/proof": { "alg": "ed25519", "value": "..." },
  "extension/policy": { "allow-federation-subtrees": true, "override": "issuer-only" },
  "nodes": [
    { "term": "IT",                 "parent": null,             "labels": ["IT", "informatyka"] },
    { "term": "IT:programming",     "parent": "IT",             "labels": ["programming", "programowanie", "coding"] },
    { "term": "IT:programming:C++", "parent": "IT:programming", "labels": ["C++", "cpp", "cplusplus"] }
  ],
  "signature": { "alg": "ed25519", "value": "..." }
}
```

`topic-resolution.v1` (signed; reproducible):

```json
{
  "schema/v": 1,
  "taxonomy/digest": "sha256:...", "resolver/version": "matcher-1.0.0", "epsilon": 1.0,
  "query/keywords": ["programowanie", "C++", "kwestia", "sortowanie"],
  "result": "resolved", "topic/term": "IT:programming:C++", "score": 7.0,
  "matched/labels": [ { "keyword": "programowanie", "term": "IT:programming", "kind": "alias" },
                      { "keyword": "C++", "term": "IT:programming:C++", "kind": "leaf" } ],
  "candidates": [ { "topic/term": "IT:programming:C++", "score": 7.0 },
                  { "topic/term": "IT:programming",     "score": 3.0 } ],
  "ambiguous/reason": null,
  "resolver/node-id": "node:did:key:z...", "signature": { "alg": "ed25519", "value": "..." }
}
```

Deterministic weighted matcher:

```text
WEIGHTS = { exact_leaf: 4, exact_ancestor: 2, alias: 1, path_coherence_bonus: 2 }
resolve(keywords, taxonomy, weights, epsilon):
  matched = []
  for kw in normalize(keywords):                  # lowercase, strip, deterministic diacritic fold
    for node in taxonomy.nodes:
      if kw in node.labels: matched.push((node.term, classify(node)))   # leaf | ancestor | alias
  scores = {}
  for (term,_) in matched:
    s = 0
    for (m,kind) in matched:
      if m == term:                  s += weight_for(kind)
      elif is_ancestor(m,term):      s += weights.exact_ancestor
    if all_on_one_path(terms_for(term)): s += weights.path_coherence_bonus
    scores[term] = s
  ranked = sort_desc(scores, tie_break = lexicographic(term))
  if empty(ranked):                              return {result:"unresolved"}
  if len(ranked)==1 or ranked[0].score-ranked[1].score >= epsilon:
                                                 return {result:"resolved", term:ranked[0].term, candidates:ranked, epsilon, matched}
  return {result:"ambiguous", candidates:ranked, epsilon, matched, ambiguous/reason:"top scores within epsilon"}
```

### B. `service-offer.v1` with the Corpus extension (full required set)

```json
{
  "schema/v": 1,
  "offer/id": "offer:corpus:abc123", "sequence/no": 7,
  "created-at": "2026-06-23T09:00:00Z", "published-at": "2026-06-23T09:00:01Z",
  "expires-at": "2026-07-23T09:00:00Z", "offer/status": "active",
  "provider/node-id": "node:did:key:z...", "provider/participant-id": "participant:did:key:z...",
  "service/type": "corpus.provider",
  "service/description": "Collaborative C++ reasoning by a local LLM expert.",
  "pricing/amount": 4, "pricing/currency": "ORC", "pricing/unit": "1 answer", "pricing/unit-kind": "per-item",
  "delivery/max-duration-sec": 600, "queue/auto-accept": false, "queue/max-depth": 8, "hybrid": false,
  "corpus/topics": ["IT:programming:C++", "IT:programming"],
  "corpus/taxonomy-digest": "sha256:...", "corpus/taxonomy-issuer": "nym:did:key:z...",
  "corpus/model-class": "local-llm",
  "corpus/reasoning": { "max-steps": 8, "languages": ["pl", "en"] },
  "signature": { "alg": "ed25519", "value": "..." }
}
```

The `corpus/*` block is an **extension**: the offer is still a full `service-offer.v1`
with all base required fields and the same `signature`. Catalog topic index entry: key
`topic/term` → `{ offer/id, sequence/no, taxonomy/digest, provider/node-id }`, with
parent-term fallback keys.

### C. Procurement over AD

`corpus-reasoning-query.v1`:

```json
{
  "schema/v": 1,
  "query/id": "query:q1", "correlation/id": "corr:c1", "idempotency/key": "sha256:...",
  "requester/node-id": "node:did:key:zASKER", "requester/participant-id": "participant:did:key:zASKER",
  "topic/term": "IT:programming:C++", "corpus/taxonomy-digest": "sha256:...",
  "query/keywords": ["programowanie", "C++", "kwestia", "sortowanie"],
  "question": "stable_sort with a custom comparator keeps crashing on...",
  "pricing/max-amount": 10, "pricing/min-amount": 1, "pricing/currency": "ORC",
  "max/candidates": 5, "created-at": "2026-06-23T11:00:00Z", "deadline-at": "2026-06-23T12:00:00Z",
  "reply/target": { "selector/kind": "node", "node/id": "node:did:key:zASKER" }
}
```

`pricing/min-amount` is a Corpus-only buyer-bracket field (not in `service-order.v1`);
the schema MUST enforce `pricing/min-amount <= pricing/max-amount` and
`deadline-at > created-at`.

AD broadcast plan: one `parallel` stage, `success/policy: any`,
`artifact.delivery.send?mode=deferred`. Pick one addressing style per request:
catalog-rich uses explicit `node` targets from the offer-catalog topic index;
addressing-only uses one `capability-many` target (`corpus.provider`, `max/nodes` =
`max/candidates`). If combined, AD deduplicates by canonical target key
(`inac:node:<node-id>`), so each provider is queried once.

`corpus-reasoning-bid.v1` (envelope around an embedded `procurement-offer.v1`):

```json
{
  "schema/v": 1,
  "bid/id": "bid:b1", "query/id": "query:q1", "correlation/id": "corr:c1",
  "bidder/node-id": "node:did:key:zP1",
  "decision": "accept", "bid/valid-until": "2026-06-23T12:30:00Z", "policy/digest": "sha256:...",
  "procurement-offer": {
    "schema/v": 1, "offer/id": "offer:po1", "question/id": "query:q1",
    "created-at": "2026-06-23T11:05:00Z",
    "responder/node-id": "node:did:key:zP1", "responder/participant-id": "participant:did:key:zP1",
    "price/amount": 4, "price/currency": "ORC", "deadline-at": "2026-06-23T12:00:00Z",
    "answer/min-length": 200, "answer/max-length": 4000, "execution/mode": "single-responder",
    "specialization/tags": ["C++", "sorting"],
    "reputation/evidence": [
      { "kind": "service-offer", "ref": "offer:corpus:abc123", "score": 0.8 }
    ]
  },
  "signature": { "alg": "ed25519", "value": "..." }
}
```

Note the embedded offer's `question/id` equals the Corpus `query/id`, so a later
`procurement-contract.v1` chains back to the query.

`corpus-reasoning-bid-state.v1`:

```json
{ "schema/v": 1, "query/id": "query:q1",
  "candidates": [
    { "node/id": "node:did:key:zP1", "state": "bid-received",   "received-at": "2026-06-23T11:05:10Z", "updated-at": "2026-06-23T11:05:10Z", "delivery/attempt-id": "del:1" },
    { "node/id": "node:did:key:zP2", "state": "timed-out",      "received-at": null, "updated-at": "2026-06-23T12:00:00Z", "reason": "no bid before deadline", "delivery/attempt-id": "del:2" },
    { "node/id": "node:did:key:zP3", "state": "delivery-failed", "received-at": null, "updated-at": "2026-06-23T11:06:00Z", "diagnostic/code": "adapter-permanent", "delivery/attempt-id": "del:3" } ] }
```

### D. Deliberation Policy, Invite, and Answer (post-MVP, on P070)

```json
{ "schema/v": 1, "room/id": "room:r1",
  "exposure": "private-to-swarm", "answer/acceptance": "chair-signed",
  "chair/mode": "requester-appointed", "chair/nym": "nym:did:key:zASKER",
  "chair/credentials": "capability-passport:...",
  "quorum/required": 2, "tie-break": "chair", "revocation-policy": "chair-or-requester",
  "budget": { "time-ms": 120000, "steps": 12, "tokens": 200000 } }
```

```json
{ "schema/v": 1,
  "room/id": "room:r1", "query/id": "query:q1",
  "transport": { "kind": "live", "address": "wss://...", "session/ref": "room-session:s1" },
  "policy/digest": "sha256:...", "access/list": ["nym:did:key:zP1", "nym:did:key:zP3"],
  "signature": { "alg": "ed25519", "value": "..." } }
```

```json
{ "schema/v": 1,
  "answer/id": "answer:a1", "query/id": "query:q1", "room/id": "room:r1",
  "topic/term": "IT:programming:C++", "corpus/taxonomy-digest": "sha256:...",
  "content/ref": "artifact-store:...", "content/digest": "sha256:...", "answer/format": "markdown",
  "classification/ref": "classification.v1:sha256:...",
  "policy/digest": "sha256:...",
  "provenance/refs": ["..."], "contribution/refs": ["..."],
  "contributor/weights": [ { "node/id": "node:did:key:zP1", "weight": 60 },
                           { "node/id": "node:did:key:zP3", "weight": 40 } ],
  "attestation/evidence": { "room-event/high-water": 31 },
  "signatures": [ { "by": "nym:did:key:zCHAIR", "alg": "ed25519", "value": "..." } ] }
```

### E. Test Data / Fixtures (must-have for the deterministic matcher)

Ship golden fixtures so the matcher is testable and stable across implementations:

- `fixtures/topic-taxonomy.orbiplex-core.json` — the signed taxonomy above.
- `fixtures/resolution.cpp-sort.json` — keywords `["programowanie","C++","kwestia","sortowanie"]`
  → `resolved IT:programming:C++`, `score 7.0`, with `matched/labels`.
- `fixtures/resolution.ambiguous.json` — keywords that tie under `epsilon` → `ambiguous`
  with two candidates.
- `fixtures/resolution.unresolved.json` — keywords with no taxonomy hit → `unresolved`.

Each fixture pins `resolver/version`, `epsilon`, and `taxonomy/digest`, so a CI test
asserts byte-stable output.

### F. MVP Flow (procurement only)

```mermaid
sequenceDiagram
  participant A as Asker
  participant C as Offer Catalog
  participant P as Providers (P1..Pn)
  A->>A: resolve keywords -> IT:programming:C++ (or ambiguous)
  A->>C: query corpus topic index
  A->>P: AD broadcast corpus-reasoning-query.v1 (deferred, fan-out, max/candidates)
  P-->>A: corpus-reasoning-bid.v1 (accept|decline|counter) or silence
  A->>A: corpus-reasoning-bid-state (states + timestamps + reason)
  A->>A: select subset by price/reputation
  Note over A,P: MVP stops here: single contracting provider answers via P011;<br/>live deliberation is the post-MVP layer on P070
```

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision. Each item notes its tier and `blocked-by`.

### MVP — Procurement slice (no live room)

Most implementable value in the current architecture: topic resolver + offer lookup +
AD query/bid + single-provider answer. No Room runtime, no Inquirium thread/session
runtime, no N-way settlement.

#### Phase 0 — Preconditions

- [x] Confirm AD deferred mode, `capability-many`, single-owner acceptors usable for a
  second marketplace consumer. Evidence: Artifact Delivery supports `capability-many`
  recipient selectors, private/direct policy checks, deferred delivery status, and
  single-owner acceptor admission; Corpus uses those seams rather than adding a
  transport authority.
- [x] Confirm P011 artifacts + P016 escrow reachable for a single contracting provider.
  Evidence: Corpus exports the selected embedded `procurement-offer.v1`, and the daemon
  `/v1/corpus/rounds/{query_id}/settle` bridge opens the selected-responder execution,
  registers the selected procurement offer, selects it, and accepts the resulting
  contract through the existing execution/procurement host path.
- [x] Extract the language-neutral normative profile from `node/canonical-json` for
  Corpus signatures and idempotency keys. Evidence: this proposal now names and specifies
  `orbiplex-canonical-json-jcs-v1`; `orbiplex-node-corpus-core` has a byte-stable
  canonical JSON and digest vector for the profile, and Corpus digests/idempotency keys
  use `CanonicalJsonProfile::JcsV1`.
- [x] Complete the MVP Contract Gate: canonical schemas, positive/negative examples,
  node schema sync, schema-gate validation, and admission constrainers for the MVP
  procurement slice. Evidence: `topic-taxonomy.v1`, `topic-resolution.v1`,
  `corpus-reasoning-query.v1`, `corpus-reasoning-bid.v1`, and
  `corpus-reasoning-bid-state.v1` exist in `doc/schemas/`, are synced to
  `node/protocol/contracts/`, and are covered by `orbiplex-node-schema-gate`
  Corpus tests. `schema-gate` now delegates Corpus semantic validation to
  `orbiplex-node-corpus-core`, including taxonomy tree/digest checks, topic resolution
  invariants, query price brackets, bid-state invariants, and the 16 KiB canonical
  byte budget for `extensions`. `corpus-reasoning-bid-state.v1` explicitly allows an
  empty `candidates` list for dispatch failures before provider selection.

#### Phase 1 — Topic taxonomy + resolver

- [x] Define signed `topic-taxonomy.v1` (issuer key, validity, supersession proof,
  federation id, versioning scheme, unique terms/labels) and signed `topic-resolution.v1`
  (epsilon, matched/labels, resolver/version).
- [x] Implement the pure deterministic weighted matcher with `ambiguous`/`unresolved`.
  Evidence: `orbiplex-node-corpus-core` owns the deterministic resolver and tests exact,
  ambiguous, and unresolved cases.
- [x] Ship the fixtures (§E) and a byte-stable CI test. Evidence:
  `orbiplex-node-corpus-core` validates the synchronized taxonomy/query/bid fixtures and
  asserts the canonical taxonomy digest plus deterministic resolver output.
- [x] Implement canonical `taxonomy/digest` / `topic/term` hashing per Resolved
  Decision 5. Evidence: `TopicTaxonomy::canonical_digest()` recomputes the pinned
  `sha256:` digest over canonical JSON with host-owned fields removed.

#### Phase 2 — Topic-scoped offers + catalog indexing

- [x] Add the `corpus` extension to `service-offer.v1` (model-class enum, taxonomy
  digest + issuer); Dator publishes one multi-topic offer. Evidence: Dator maps
  configured Corpus offer fields onto the canonical wire keys and rejects incomplete
  `corpus.provider` offers before publication; daemon/catalog snapshots preserve
  `corpus/topics`, `corpus/taxonomy-digest`, `corpus/taxonomy-issuer`,
  `corpus/model-class`, and optional `corpus/reasoning`.
- [x] Offer/catalog admission constrainer: `corpus/topics ⊆ terms(taxonomy/digest)`;
  missing or untrusted taxonomy material fails closed. Evidence: schema-gate exposes a
  trusted-taxonomy subset constrainer, and `node/catalog::validate_corpus_offer_scope`
  applies the same check to catalog records through `TrustedTopicTaxonomy`; Corpus
  topic-index construction fails closed instead of silently hiding invalid
  `corpus.provider` records. Generic catalog storage remains neutral and is not a Corpus
  authority.
- [x] Offer-catalog topic index + supersession/partial-withdrawal (P067). Evidence:
  `node/catalog::corpus_topic_index_from_entries` and
  `corpus_topic_index_from_observed` project active Corpus-capable offers by topic; the
  shared Offer Catalog exposes the path-first
  `/v1/offer-catalog/corpus/taxonomies/{taxonomy_digest}/topics/{topic}/offers` surface;
  its observed snapshot projection preserves `corpus/*` fields and tests cover taxonomy
  filtering plus partial withdrawal by replacing an older multi-topic revision with a
  newer reduced-topic revision.

#### Phase 3 — Procurement round over AD

- [x] Define `corpus-reasoning-query.v1` as a decorator over `question-envelope.v1`
  (requester ids, keywords, `max/candidates`, bracket, deadline; invariants),
  `corpus-reasoning-bid.v1` (envelope + embedded `procurement-offer.v1`; `decision`
  enum; TTL), `corpus-reasoning-bid-state.v1` (timestamps, reason,
  `delivery/attempt-id`).
- [x] Implement broadcast fan-out, the bid-state read-model, and local selection.
  Evidence: `orbiplex-node-corpus-core` builds a schema-valid
  `artifact-delivery-envelope.v1` for `capability-many` fan-out, materializes the
  requester-owned `corpus-reasoning-bid-state.v1`, validates bid/query price semantics,
  enforces `bidder/node-id == procurement-offer.responder/node-id`, exposes the default
  bid idempotency key, preserves `decline` as refusal even after bid TTL, and selects
  the cheapest valid accepted/countered bid with longer `bid/valid-until` as the price
  tie-breaker. The daemon now persists Corpus rounds, registers query/bid facts,
  restores bid-state read models, exposes local provider bid acceptor endpoints and an
  AD inbound Corpus query acceptor, signs generated local bids with the node Ed25519
  identity key, verifies admitted bid signatures against `bidder/node-id`, filters
  dispatch candidates by taxonomy digest plus exact/parent topic support, rejects offers
  outside the query price bracket rather than mutating their price, dispatches requester
  queries through AD `capability-many` over INAC, collects accepted bids from INAC
  admission diagnostics, emits P057 operator notifications for bid readiness, and has
  operator round visibility plus passing Story-011 acceptance coverage.
- [x] Move Story-011 Corpus fan-out smoke from `signature-only` capability lookup to full
  `sovereign-policy` verification. The managed Story-011 `ad-smoke` path now creates
  B/C participants, pins them as Node A's sovereign capability passport issuers,
  restarts Node A, and exercises Seed Directory provider lookup through the production
  trust mode.

#### Phase 4 — Single-provider answer + settlement

- [x] Single contracting provider answers; bid → `procurement-offer.v1`; close via
  `procurement-contract.v1` / `procurement-receipt.v1` with host-owned escrow. Evidence:
  `orbiplex-node-corpus-core::settlement_selection` exports the selected embedded
  `procurement-offer.v1` with bid digest and selected provider node; the daemon bridge
  now opens the selected-responder execution, registers/selects the offer, and accepts
  the contract. Bridge failures after selection mark the Corpus round
  `settlement-failed` for operator-visible recovery. Story-011 now exercises the
  selection, settlement, `corpus-reasoning-answer.v1` attachment, and requester-satisfied
  close path over AD/INAC. The first answer slice includes schema-gate validation,
  answer-text digest binding, daemon round persistence, provider-local
  `inquirium.generate` drafting through the deterministic local runtime, selected-bid
  responder binding, answer signature verification, policy-digest binding to the round
  taxonomy digest, bounded answer storage, chronological answer ordering,
  provider-originated AD answer delivery through the in-process `corpus.answer` acceptor,
  AD answer envelope construction, tier-correct answer classification propagation, local
  latest-read-model replacement for superseded revisions, and Story-011 smoke coverage.
  Multi-provider contribution receipts remain post-MVP.

### Post-MVP — Live deliberation

#### Phase 5 — Room consolidation `[~] partial P070 foundation`

- [~] Land the generic Room primitive (P070). Durable room schemas, the pure
  projection core, and the Agora runtime projection adapter exist; Corpus live-room
  code still waits for P070 live-plane runtime
  integrations. Corpus contributes the transport requirements (low latency, no
  retention, small participant count) to P070's live-transport profile.

#### Phase 6 — Agent organ reasoning session `[!] blocked-by: Agent organ (P073)`

- [!] Land the Agent organ (P073) reasoning session with tool support, budgets,
  deadlines, context windows, and explicit draft boundaries. Corpus should consume that
  runtime rather than define a smaller Corpus-only LLM session surface. The current
  provider-local Inquirium slice proves only the lower boundary: a provider can ask
  Inquirium for a draft answer, while durable orchestration, multi-turn coordination,
  stop/resume, and chair authority stay above Inquirium in Agent/Room.

#### Phase 7 — Deliberation room policy + invite + join `[!] blocked-by: P070, Phase 6`

- [ ] Define `corpus-reasoning-room-policy.v1` (exposure enum bound to P009, acceptance
  enum, chair credentials, quorum/tie-break/revocation, token budget) and
  `corpus-reasoning-room-invite.v1`.
- [ ] Open rooms with access lists; deliver invites over AD; members join and signal
  ready.

#### Phase 8 — Chair, then arbiter election

- [ ] Requester-appointed chair resolves conflicts; signed `corpus-reasoning-answer.v1`
  (content-addressed, classification, contributor/weights, attestation/evidence).
- [ ] Support requester-owned Agent as `chair/agent-ref`, with host-owned budget,
  lifecycle, grants, and stop/resume controls; the Agent coordinates but does not
  self-authorize publication, settlement, membership changes, or effects.
- [ ] Define `corpus-reasoning-role-assignment.v1` for task roles such as implementer,
  reviewer, adversarial critic, or summarizer, with local participant acceptance.
- [ ] Define `corpus-reasoning-instruction-overlay.v1` for per-role/per-turn suggested
  instructions consumed through local Inquirium prompt-assembly policy, never direct
  remote prompt injection.
- [ ] Later: arbiter election (`corpus-reasoning-arbiter-nomination.v1` / `…-vote.v1`)
  with eligibility, COI, quorum, deadline, tie-break, revocation, fallback.

#### Phase 9 — N-way settlement

- [ ] `contribution-allocation.v1` (candidate separate proposal): contribution weights
  (from the answer), per-contributor receipts, dispute path.

#### Phase 10 — Hardening

- [ ] Enforce `budget/time-ms` / `budget/steps` / `budget/tokens` and Inquirium caps.
- [ ] Notifications (P057); abuse-model mitigations; observability without exposing
  ephemeral chat content.
