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
(P070) and a minimal **Inquirium assistant-session** (extending P066). The MVP needs
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
| **Room primitive (P070)** | live deliberation (post-MVP) | **proposed, not built** |
| **Inquirium `assistant-session`** (extends P066) | live multi-turn reasoning (post-MVP) | **not built** |

The MVP depends only on the first three rows. The live-deliberation layer is
**blocked-by** P070 and the Inquirium assistant-session, stated explicitly rather than
assuming a live room exists.

### Minimal Inquirium assistant-session

Full Corpus needs a multi-turn reasoning session bound to a room, with bounded
steps/deadline/tokens and context ingestion. This proposal requires a minimal
`inquirium.assistant-session` contract (a natural extension of P066) providing:
open/continue/close a session, a step/deadline/token budget, context-window assembly,
and a draft-output boundary. Until it exists, only the MVP procurement slice is
implementable.

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
  marker removes all of the offer's topic-index entries.

### 4. Procurement over Artifact Delivery (the MVP)

1. The asker broadcasts `corpus-reasoning-query.v1` to candidate nodes through one AD
   delivery plan (`?mode=deferred`, a single parallel stage). The query carries the
   topic, `corpus/taxonomy-digest`, the question, the original `query/keywords` (for
   audit reproducibility), `requester/node-id` + `requester/participant-id`, a price
   bracket, `max/candidates` (fan-out cap), and a `deadline-at`.
2. Each provider's single `corpus-reasoning-query.v1` acceptor replies with a signed
   `corpus-reasoning-bid.v1` (§4.1) to `reply/target`, correlated by `correlation/id` +
   `query/id`.
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
plane and reason synchronously through their Inquirium assistant-sessions. The chat is
ephemeral reasoning, never a protocol fact (P070 §1).

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

### 6. Answer Contract (concrete, content-addressed, signed)

Convergence yields one `corpus-reasoning-answer.v1`: `answer/id`, `query/id`, `room/id`,
`topic/term`, `corpus/taxonomy-digest`, `content/ref` **or** inline `content` **plus
`content/digest`** (so a verifier can confirm the inline content matches what was
signed), `answer/format` (`plain-text | markdown | json | edn`), `classification`
(a `classification.v1` object/ref, not a bare string), `policy/digest` (required),
`provenance/refs`, `contribution/refs`, `contributor/weights[]` (present even though
N-way settlement is post-MVP, so a later settlement can use the same answer),
`attestation/evidence` (e.g. the deliberation `room-event.v1` high-water mark, proving
the answer came from the room and not a single responder), and `signatures[]` per
`answer/acceptance`.

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
- **Canonicalization**: every signature and idempotency key is computed over the
  canonical JSON form produced by `node/canonical-json`
  (`agora-core::canonical::canonical_json_string`) — the same rule already used for Agora
  records — to make replay protection real and cross-implementation stable.
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
- **Classification**: reference `classification.v1` (Proposal 047 /
  `classification.v1.schema.json`) through `classification/ref` or an inline
  `classification` object; never use a bare string.
- **Privacy/retention**: room durability and retention for `room.v1` /
  `room-membership.v1` / `room-event.v1` are governed by **P070** policy; Corpus does not
  define its own retention and explicitly defers to P070's per-exposure retention rules.

## Data Contracts

| Schema | Status | Phase | Purpose |
|---|---|---|---|
| `topic-taxonomy.v1` | new | MVP | Signed, versioned, federated taxonomy governance artifact. |
| `topic-resolution.v1` | new | MVP | Signed resolver output: canonical term or ranked `ambiguous` (with `epsilon`, `matched/labels`). |
| `service-offer.v1` (`corpus` extension) | extend | MVP | `corpus/topics`, `corpus/model-class`, `corpus/taxonomy-digest`, `corpus/taxonomy-issuer`. |
| `corpus-reasoning-query.v1` | new | MVP | Broadcast query: topic, keywords, requester ids, price bracket, `max/candidates`, deadline. |
| `corpus-reasoning-bid.v1` | new | MVP | Envelope: `decision` + `bid/valid-until` + `policy/digest` + embedded `procurement-offer.v1`. |
| `corpus-reasoning-bid-state.v1` | new | MVP | Asker read-model: per-candidate state + timestamps + reason + AD `delivery/attempt-id`. |
| `corpus-reasoning-room-policy.v1` | new | post-MVP | Exposure, acceptance, chair + credentials, quorum, budgets (incl. tokens). |
| `corpus-reasoning-room-invite.v1` | new | post-MVP | Room subject + live-transport binding + policy digest. |
| `corpus-reasoning-arbiter-nomination.v1` | new | later (Tracker P8) | Arbiter nomination (durable room record). |
| `corpus-reasoning-arbiter-vote.v1` | new | later (Tracker P8) | Arbiter vote (durable room record). |
| `corpus-reasoning-answer.v1` | new | post-MVP | Content-addressed signed answer incl. `policy/digest` (required), `contributor/weights[]`. |
| `contribution-allocation.v1` | future (reserved) | post-MVP | N-way settlement split (separate proposal). |

Reused: `room.v1` / `room-membership.v1` / `room-event.v1` (P070),
`artifact-delivery-envelope.v1`, `deferred-operation-status.v1`, `procurement-offer.v1`,
`procurement-contract.v1`, `procurement-receipt.v1`, `classification.v1`.

## Relationship to Existing Mechanisms

- **Artifact Delivery (023)**: carries MVP procurement (query/bid), the room invite, and
  the final answer. Corpus is a second marketplace-style AD consumer after Arca/Dator. It
  does **not** carry the live chat.
- **Room (P070)**: live deliberation substrate and durable skeleton. Hard prerequisite
  for phase 2. **Corpus imposes specific transport requirements on P070**: low latency,
  no retention, and a small participant count. These belong in P070's live-transport ADR
  as an input requirement (see Open Questions / P070).
- **Arca/Dator/offer-catalog (003/004/067)**: extended with `corpus/topics` indexing, not
  forked.
- **Inquirium (P063/P064/P066)**: per-participant model access via a minimal
  assistant-session (prerequisite for phase 2).
- **P011 / story-006 / P016**: procurement lifecycle and escrow.
- **Classification (047)**: the answer carries a `classification.v1`.
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

## Open Questions

1. **Identifier governance.** Patterns are fixed here (§Schema Conventions); who governs
   the `query:`/`room:`/`answer:` namespaces and prefix allocation?
2. **JSON canonicalization across implementations.** Corpus pins
   `agora-core::canonical::canonical_json_string`; is that the cross-language normative
   rule (key order, Unicode normalization, number forms) for all non-Rust nodes?
3. **Taxonomy migration between versions.** What happens when a provider published offers
   under an older `taxonomy/digest` and an asker cites a newer one — re-map, reject, or
   resolve against both?
4. **Query vs `question-envelope.v1`.** Should `corpus-reasoning-query.v1` be a
   *decorator* of `question-envelope.v1` (P003) rather than a sibling type? Fields
   overlap; decide alias vs distinct flow.
5. **Canonical topic hashing.** Exact `taxonomy/digest` and `topic/term`
   canonicalization (case, separators, Unicode folding) so scoping and passports are
   stable.
6. **Discovery style.** Catalog-rich vs `capability-many` as default — or both.
7. **Chair vs election.** When does election replace requester-appointed chair, with what
   eligibility/quorum/COI rules?
8. **Pricing model.** Per-answer/participant/token; bracket reconciliation; when does the
   pricing-calculator contract become necessary?
9. **N-way settlement.** Does `contribution-allocation.v1` become its own proposal, and
   what authority declares `contributor/weights[]`?
10. **Bid-state retry strategy.** For `delivery-failed`/`unreachable`: retry budget,
    backoff, and who decides?
11. **Minimal Inquirium assistant-session.** Smallest surface to start phase 2.

## Implementation Recommendations

Non-normative shapes. Field names follow §Schema Conventions; final schemas are gated in
`doc/schemas/` and the node schema-gate. `…` elides obvious values.

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
AD query/bid + single-provider answer. No Room runtime, no Inquirium assistant-session,
no N-way settlement.

#### Phase 0 — Preconditions

- [ ] Confirm AD deferred mode, `capability-many`, single-owner acceptors usable for a
  second marketplace consumer.
- [ ] Confirm P011 artifacts + P016 escrow reachable for a single contracting provider.
- [ ] Confirm `node/canonical-json` is the signature/idempotency canonicalization rule.

#### Phase 1 — Topic taxonomy + resolver

- [ ] Define signed `topic-taxonomy.v1` (issuer key, validity, supersession proof,
  federation id, versioning scheme, unique terms/labels) and signed `topic-resolution.v1`
  (epsilon, matched/labels, resolver/version).
- [ ] Implement the pure deterministic weighted matcher with `ambiguous`/`unresolved`.
- [ ] Ship the fixtures (§E) and a byte-stable CI test.
- [ ] Resolve canonical `taxonomy/digest` / `topic/term` hashing (Open Q5).

#### Phase 2 — Topic-scoped offers + catalog indexing

- [ ] Add the `corpus` extension to `service-offer.v1` (model-class enum, taxonomy
  digest + issuer); Dator publishes one multi-topic offer.
- [ ] Offer/catalog admission constrainer: `corpus/topics ⊆ terms(taxonomy/digest)`;
  missing or untrusted taxonomy material fails closed.
- [ ] Offer-catalog topic index + supersession/partial-withdrawal (P067).

#### Phase 3 — Procurement round over AD

- [ ] Define `corpus-reasoning-query.v1` (requester ids, keywords, `max/candidates`,
  bracket, deadline; invariants), `corpus-reasoning-bid.v1` (envelope + embedded
  `procurement-offer.v1`; `decision` enum; TTL), `corpus-reasoning-bid-state.v1`
  (timestamps, reason, `delivery/attempt-id`).
- [ ] Implement broadcast fan-out, the bid-state read-model, and local selection.

#### Phase 4 — Single-provider answer + settlement

- [ ] Single contracting provider answers; bid → `procurement-offer.v1`; close via
  `procurement-contract.v1` / `procurement-receipt.v1` with host-owned escrow.

### Post-MVP — Live deliberation

#### Phase 5 — Room consolidation `[!] blocked-by: P070`

- [!] Land the generic Room primitive (P070). Corpus forces this; do it before any
  Corpus live-room code. Corpus contributes the transport requirements (low latency, no
  retention, small participant count) to P070's transport ADR.

#### Phase 6 — Inquirium assistant-session `[!] blocked-by: Inquirium (extends P066)`

- [!] Land a minimal `inquirium.assistant-session` (open/continue/close, step/deadline/
  token budget, context window, draft boundary).

#### Phase 7 — Deliberation room policy + invite + join `[!] blocked-by: P070, Phase 6`

- [ ] Define `corpus-reasoning-room-policy.v1` (exposure enum bound to P009, acceptance
  enum, chair credentials, quorum/tie-break/revocation, token budget) and
  `corpus-reasoning-room-invite.v1`.
- [ ] Open rooms with access lists; deliver invites over AD; members join and signal
  ready.

#### Phase 8 — Chair, then arbiter election

- [ ] Requester-appointed chair resolves conflicts; signed `corpus-reasoning-answer.v1`
  (content-addressed, classification, contributor/weights, attestation/evidence).
- [ ] Later: arbiter election (`corpus-reasoning-arbiter-nomination.v1` / `…-vote.v1`)
  with eligibility, COI, quorum, deadline, tie-break, revocation, fallback.

#### Phase 9 — N-way settlement

- [ ] `contribution-allocation.v1` (candidate separate proposal): contribution weights
  (from the answer), per-contributor receipts, dispute path.

#### Phase 10 — Hardening

- [ ] Enforce `budget/time-ms` / `budget/steps` / `budget/tokens` and Inquirium caps.
- [ ] Notifications (P057); abuse-model mitigations; observability without exposing
  ephemeral chat content.
