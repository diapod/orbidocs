# Proposal 041: Agora Ingest Attestation and Tiered Access

Based on:
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/40-proposals/040-custodial-redelivery-and-tombstones.md`
- `doc/project/50-requirements/requirements-014.md`

## Status

Draft

## Date

2026-04-17

## Executive Summary

Agora today verifies that a record envelope is **cryptographically
authentic** — the signer's key matches the declared
`author/participant-id`, the canonical bytes reproduce `record/id`, and
the signature verifies in the `agora.record.v1` domain (requirements-014
FR-008, FR-009). It does not verify that the author is a **swarm
participant**. Because `participant:did:key:…` is self-minted, anyone
with a keyboard can produce unlimited mathematically-valid envelopes
under freshly generated identities.

Proposal 040 (custodial redelivery) does not close this gap and does not
widen it either: a custodian is a byte-custodian, not an attestation
proxy. A re-shipped envelope is byte-identical to an author-shipped
envelope, so whatever gate decision the relay makes on one must hold on
the other.

The gap is therefore in the **ingest gate** of Agora — but the
verification primitive it needs (resolve passport, check scope, verify
a short-lived proof token, cache the decision) is **not** Agora-specific.
The same check is needed by middleware dispatch, offer-catalog
submission, whisper surface, memarium custody acceptance, reputation
signal publication, and any other component that needs to ask "is this
author attested under a passport my operator accepts right now". This
proposal therefore places the verification primitive as a **reusable
component alongside the existing signer/sealer trust-boundary gate**,
and models Agora ingest as the first consumer rather than the owner.

This proposal freezes:

1. an optional, signed `author/attestation_ref` field on
   `agora-record.v1` that lets an author commit, in the envelope
   itself, to the passport under which they claim to speak,
2. a short-lived, relay-bound `agora-attestation-proof.v1` token,
   carried as an HTTP header on ingest, proving current control of the
   key referenced by the passport,
3. a small matrix of **ingest modes** (`open`, `allowlist`, `passport`,
   `passport_scoped`, `layered`) that an operator selects per topic or
   per record kind,
4. a predicate-composition grammar so operators can build tiered
   access policies (by topic, by record kind, by content schema, by
   subject resource kind, by author assurance level, by rate budget,
   by blocklist),
5. a stable ingest-refusal reason-code vocabulary so custodians and UI
   layers can react with intent,
6. the explicit guarantee that the gate is **symmetric**: fresh
   author-shipped and custodian-reshipped envelopes are evaluated by
   the same predicates against the same current policy,
7. the placement of the verification primitive as a reusable
   `attestation-gate` component living in the same trust-boundary
   zone as the signer and sealer, with a shared passport-resolution
   cache used by every consumer.

The ingest gate is infrastructure-level trust ("this `did:key` crossed
a threshold the operator recognizes"), not personhood or truth. Those
live in reputation and moderation layers.

## Context and Problem Statement

The architecture already has every piece needed to attest participation
and to verify that attestation at the relay:

- `capability-passport.v1` (proposal 024) is the generic signed
  delegation artifact — a natural carrier for "this `did:key` is an
  attested participant under scope X, with expiry Y",
- seed directory (proposal 025) replicates passports across the swarm
  and gives relays a local cache to resolve references against,
- node operator binding and derived node assurance (proposal 034)
  provide the upstream trust chain from operator to node to
  participant,
- reputation signals (proposal 026 §4, separated from
  `resource-opinion.v1`) provide the reweighting layer **on top** of
  attested authorship, not a substitute for it.

None of these are wired into `POST
/v1/agora/topics/{key}/records`. Proposal 035 §5.7 leaves ingest ACL to
operator policy but does not freeze:

- where the author's attestation claim lives (envelope field? HTTP
  header? both?),
- how the relay verifies it cheaply and offline where possible,
- what configurable gating modes operators can choose between,
- how tiered access policies compose (per topic / per kind / per
  scope),
- what refusal reasons are stable enough for clients to branch on.

Leaving this un-frozen invites three failure modes:

- **silent openness**: an operator launches a relay thinking "defaults
  are safe" and in fact accepts envelopes from any freshly minted
  `did:key`, becoming a flood target,
- **accidental lock-out**: an operator bolts on a bespoke ACL whose
  semantics drift from what custodians and clients understand, making
  redelivery (proposal 040) brittle,
- **attestation laundering**: a well-meaning custodian reships on
  behalf of an un-attested author and is blamed for "bringing in
  strangers", even though it is merely transporting bytes.

## Goals

- Freeze the author-side surface for presenting an attestation claim
  (envelope field + proof token).
- Freeze a small, composable set of relay-side ingest modes that cover
  the realistic operator choices.
- Provide a predicate grammar for tiered access granular enough to
  express "this topic is open-membership, this other topic is
  operator-allowlist only".
- Freeze refusal reasons so clients, custodians, and UIs can react
  with stable logic.
- Make the gate symmetric across fresh-shipment and re-shipment, so
  proposal 040's byte-custody model remains clean.
- Keep the contract orthogonal to reputation and moderation.
- Place the verification primitive as a reusable component in the
  daemon's trust-boundary zone (next to signer and sealer), so that
  Agora, middleware dispatch, offer catalog, whisper, memarium
  custody, reputation, workflow sinks, and any future consumer share
  one resolution cache and one policy-evaluation path.

## Non-Goals

- This proposal does not define how passports are issued, signed, or
  distributed — that lives in proposals 024, 025, 034.
- This proposal does not define sybil-hardness. Sybil resistance comes
  from the combined layering of attestation + assurance + reputation;
  this gate only enforces the first of those.
- This proposal does not define moderation, takedown, or content
  policy. Those are higher-layer concerns built on top of attested
  authorship.
- This proposal does not define quotas or billing. Rate budgets appear
  as one predicate in the gate grammar, but their economics are
  operator-local.
- This proposal does not mandate any specific passport taxonomy. It
  names one scope ID (`agora.ingest`) and leaves richer profiles to
  operator configuration.
- This proposal does not exhaustively catalog every consumer of the
  reusable `attestation-gate`. The list in §9 is illustrative;
  additional consumers MAY adopt the primitive without amending this
  document.

## Decision

### 1. Envelope Field: `author/attestation_ref`

`agora-record.v1` gains one optional field in the **signed** portion of
the envelope:

- `author/attestation_ref` — optional string, shape
  `"passport:<kind>:<opaque>"` conforming to the passport-id grammar
  of proposal 024 (for example `"passport:participant:ab12…"`).

Rules:

- The field is **part of the canonical bytes** used to compute
  `record/id` and to verify the signature. An author who commits to a
  passport commits to it cryptographically; a relay or custodian that
  tries to strip or swap it will invalidate the signature.
- Presence of the field is the author's **claim**, not a proof.
  Verification happens at the relay gate, against the current state of
  the referenced passport.
- Absence of the field means "I make no attestation claim". Whether
  absence is accepted depends on the ingest mode (§4).
- The field does not impose one passport taxonomy; the relay's
  configured ingest mode decides which `capability_id` values, which
  issuer scopes, and which validity predicates are acceptable.

Rationale for putting the claim in the signed envelope rather than in
a header:

- it is tamper-evident end-to-end across custody and redelivery,
- it survives archival and cross-relay propagation without separate
  metadata channels,
- a reader of the archive a year later can still see under which
  passport the author was speaking, independently of any live
  verification.

### 2. Proof Token: `agora-attestation-proof.v1`

Live proof of key control is a separate artifact, carried out-of-band
of the envelope (HTTP header on ingest), not stored with the record:

```json
{
  "schema": "agora-attestation-proof.v1",
  "author/participant-id": "participant:did:key:...",
  "author/attestation_ref": "passport:participant:...",
  "relay/id": "relay.example.org",
  "issued_at": "2026-04-17T10:00:00Z",
  "expires_at": "2026-04-17T10:05:00Z",
  "nonce": "..."
}
```

signed by the author's key in a dedicated `agora.attestation.proof.v1`
signing domain.

Rules:

- `author/participant-id` MUST equal the envelope's
  `author/participant-id`.
- `author/attestation_ref` MUST equal the envelope's
  `author/attestation_ref`.
- `relay/id` MUST match the receiving relay's identity; this prevents
  cross-relay replay of one token.
- `expires_at - issued_at` MUST be short (recommended ≤ 5 minutes);
  relays MAY refuse tokens with longer windows.
- The token is **not** included in canonical envelope bytes; it is not
  part of `record/id`. Redelivery from memarium or from a custodian
  (proposal 040) requires the re-shipper to obtain a fresh token if
  the ingest mode requires one.

Rationale for the separation: the envelope is the durable artifact
(byte-identical across time and relays); the token is the freshness
signal (per-ingest, per-relay). Collapsing them would either make the
record sensitive to replay windows or make proof permanent — neither
is desirable.

### 3. Relay-Side Passport Resolution

On ingest with `author/attestation_ref` present, the relay:

1. resolves the passport id against its local cache of seed-directory
   replicas (proposal 025), falling back to a configured resolver if
   absent,
2. verifies the passport signature, expiry, and revocation status,
3. checks that the passport binds the claimed `author/participant-id`
   to a `capability_id` and scope acceptable under the current ingest
   mode (§4),
4. if a proof token is required, verifies the token's signature,
   domain, `relay/id`, time window, and nonce uniqueness within the
   token's expiry window.

All four checks MUST be cheap and offline-capable for the common path.
Relays SHOULD cache resolved-passport decisions with an explicit TTL
(recommended ≤ passport `expiry` minus a safety margin).

**Nym-certificate as an alternate attestation artifact.** When the
ingest target permits pseudonymous authorship (e.g. `record/kind =
"whisper"` per proposal 035 §2 invariant 9 and proposal 013), the
envelope carries `author/nym-certificate-ref` instead of (or alongside)
`author/attestation_ref`. The gate then resolves a `nym-certificate.v1`
(proposal 015) through the same cache path as passports and performs
the analogous checks:

- verify the council's signature on the nym certificate,
- verify that the certificate's bound nym matches the envelope's
  `author/participant-id` (`nym:did:key:...`),
- verify that the certificate is within its validity window and not
  revoked,
- verify that the certificate's authorization scope (council,
  federation, signal-grade bound, disclosure-scope bound) matches what
  the topic's ingest mode requires.

Nym certificates and capability passports share the resolution cache
but are distinct artifact families; a gate configured to accept one
does not automatically accept the other. The consumer-local ingest
mode (§4) decides which families are acceptable for the topic.

### 4. Ingest Modes

An operator configures one ingest mode per topic-pattern or record-kind
scope. The modes are:

| Mode | Meaning | Attestation required? |
|---|---|---|
| `open` | Anyone with a mathematically valid signature may ingest. | no |
| `allowlist` | Only authors whose `participant-id` (or parent `node-id`) appears in the operator's configured set may ingest. | no (local list) |
| `passport` | Authors MUST present `author/attestation_ref` to any passport the relay accepts (configurable `capability_id` set), plus a valid proof token. | yes |
| `passport_scoped` | As `passport`, plus scope predicates: the passport must grant a specific scope (e.g. `{"topic":"ai.orbiplex.opinions/*"}` or `{"assurance_level":">=A2"}`) matching the ingest target. | yes |
| `layered` | A conjunction of predicates from the grammar in §5. | per predicate |

Defaults:

- The MVP local-only profile (requirements-014 FR-012, NFR-001) MAY
  use `open`, because authorship in that profile is the local
  participant and no federation exists; the relay MUST NOT enable
  `open` silently on a non-local listener.
- A relay exposed on anything other than loopback MUST have an explicit
  mode set for every topic-pattern it accepts; if none matches, ingest
  MUST be refused with `ingest_mode_unset`.

This closes the "silent openness" footgun.

### 5. Predicate Grammar for Tiered Access

`layered` ingest modes compose from predicates. The grammar is small
and all predicates are pure functions of envelope + passport + relay
state. A predicate expression is a list of clauses AND-ed together;
each clause is one of:

| Predicate | Example | Notes |
|---|---|---|
| `topic_match` | `{"topic_match":"ai.orbiplex.opinions/*"}` | glob on `topic/key` |
| `record_kind` | `{"record_kind":"opinion"}` | exact on `record/kind` |
| `content_schema` | `{"content_schema":"resource-opinion.v1"}` | exact |
| `subject_kind` | `{"subject_kind":"url"}` | exact on `record/about[0].resource/kind` |
| `passport_capability` | `{"passport_capability":"agora.ingest"}` | `capability_id` of the attestation passport |
| `assurance_at_least` | `{"assurance_at_least":"A2"}` | requires derived-node-assurance (proposal 034) |
| `issuer_in` | `{"issuer_in":["op:did:key:..."]}` | passport issuer allowlist |
| `author_not_in_blocklist` | `{"author_not_in_blocklist":true}` | operator-local blocklist |
| `rate_budget` | `{"rate_budget":{"per":"hour","max":100}}` | per-author rate cap |
| `proof_fresh_within` | `{"proof_fresh_within":"300s"}` | max age of proof token |
| `nym_certificate_valid` | `{"nym_certificate_valid":true}` | envelope's `author/nym-certificate-ref` resolves to a valid `nym-certificate.v1` |
| `nym_council_in` | `{"nym_council_in":["council:did:key:..."]}` | issuing council allowlist for the nym certificate |
| `pseudonymous_authorship` | `{"pseudonymous_authorship":"allowed"}` or `"required"` or `"forbidden"` | whether `author/participant-id` may / must / must-not be a `nym:did:key:...` |

A topic-pattern gate is the conjunction of its clauses. Unsupported
predicates MUST cause the relay to refuse with
`ingest_predicate_unknown` rather than silently passing — "fail
closed".

Example tier configuration (illustrative, operator-local):

```json
{
  "gates": [
    {
      "topic_match": "ai.orbiplex.announcements/critical",
      "mode": "layered",
      "predicates": [
        {"passport_capability":"agora.ingest"},
        {"assurance_at_least":"A3"},
        {"issuer_in":["op:did:key:z6MkOperator..."]},
        {"proof_fresh_within":"60s"}
      ]
    },
    {
      "topic_match": "ai.orbiplex.opinions/*",
      "mode": "passport",
      "accepted_capabilities": ["agora.ingest"],
      "predicates": [
        {"proof_fresh_within":"300s"},
        {"author_not_in_blocklist": true},
        {"rate_budget": {"per":"hour","max":100}}
      ]
    },
    {
      "topic_match": "scratch/*",
      "mode": "allowlist",
      "allowlist": ["participant:did:key:z6MkOla..."]
    }
  ],
  "default": {
    "mode": "refuse",
    "reason": "ingest_mode_unset"
  }
}
```

This lets one relay host strict-announcement, open-opinion, and
private-scratch surfaces side by side — which is exactly the
"granulacja poziomów dostępowych" that motivates this proposal.

### 6. Refusal Reason Codes

On refusal, the relay responds with `403 Forbidden` (or `429 Too Many
Requests` for rate limits) and a JSON body:

```json
{
  "error": "ingest_refused",
  "reason": "author_not_attested",
  "topic/key": "ai.orbiplex.opinions/url",
  "gate_ref": "ai.orbiplex.opinions/*"
}
```

Stable reasons:

| Reason | Meaning |
|---|---|
| `ingest_mode_unset` | No gate matched the topic; fail-closed. |
| `ingest_mode_open_disabled` | `open` mode not allowed on this listener. |
| `attestation_ref_missing` | Envelope lacks `author/attestation_ref` but the gate requires one. |
| `attestation_ref_shape_invalid` | Field present but does not match the passport-id grammar. |
| `attestation_proof_missing` | Gate requires a proof token; none was presented. |
| `attestation_proof_invalid` | Proof token signature or domain check failed. |
| `attestation_proof_expired` | Proof token window has elapsed. |
| `attestation_proof_relay_mismatch` | Proof token `relay/id` does not match this relay. |
| `passport_unknown` | `author/attestation_ref` does not resolve. |
| `passport_expired` | Passport `expiry` elapsed. |
| `passport_revoked` | Passport revoked in seed directory. |
| `passport_capability_mismatch` | Passport `capability_id` not in accepted set. |
| `attestation_scope_mismatch` | Passport scope does not cover the ingest target. |
| `author_allowlist_miss` | `allowlist` mode and author not on list. |
| `author_on_blocklist` | Author explicitly blocked. |
| `assurance_insufficient` | Derived node assurance below gate threshold. |
| `issuer_not_accepted` | Passport issuer not in `issuer_in`. |
| `ingest_predicate_unknown` | Gate references a predicate the relay cannot evaluate. |
| `rate_limited` | `rate_budget` exceeded; `429` with `Retry-After`. |
| `nym_certificate_unknown` | `author/nym-certificate-ref` does not resolve. |
| `nym_certificate_expired` | Nym certificate outside validity window. |
| `nym_certificate_revoked` | Nym certificate revoked by the issuing council. |
| `nym_certificate_scope_mismatch` | Certificate scope (council, disclosure bound, signal-grade bound) does not cover the ingest target. |
| `nym_council_not_accepted` | Issuing council not in the gate's `nym_council_in` allowlist. |
| `pseudonymous_authorship_forbidden` | Envelope uses `nym:did:key:...` under a gate that forbids pseudonymous authorship. |
| `pseudonymous_authorship_required` | Envelope uses `participant:did:key:...` under a gate that requires pseudonymous authorship. |

Clients and custodians MAY branch on reason. In particular, custodians
performing redelivery SHOULD treat permanent reasons (`passport_revoked`,
`author_on_blocklist`, `passport_capability_mismatch`, and similar
policy-final outcomes) as **do-not-retry**, exactly analogous to the
tombstone matrix of proposal 040 §2. Transient reasons (`rate_limited`,
`attestation_proof_expired` with a refreshable token) are retryable.

### 7. Symmetry with Custody and Redelivery

A redelivery path (proposal 040) ships a byte-identical envelope. The
gate evaluates the same envelope against the same current policy; the
only moving part is the proof token, which the re-shipper MUST obtain
freshly. Consequences:

- custody **cannot** launder an un-attested author into an attested
  relay: the gate reads `author/attestation_ref` from the envelope,
  which was fixed at the author's signing time. If the field was
  absent or points to a passport the relay rejects, the reship
  refuses exactly as the original would have,
- custody **can** carry an attested envelope through transient
  relay-policy changes (e.g. the author's passport was briefly
  unresolvable, now is): the envelope is stable, the live gate sees
  today's state,
- a relay whose policy tightened between original acceptance and
  reship MUST refuse the reship, with a reason the custodian can
  interpret (typically `passport_capability_mismatch` or
  `attestation_scope_mismatch`). Operator sovereignty (proposal 040
  §1) overrides historical acceptance.

### 8. Interaction with MVP Local-Only

Requirements-014 FR-012 / NFR-001 keep local-only deployment a
first-class configuration. Under this proposal:

- A loopback-only relay MAY run `open` mode on all topics; this is the
  default for the MVP profile.
- `author/attestation_ref` on records authored by the local primary
  participant is OPTIONAL and typically absent in local-only mode.
- A relay MUST NOT silently inherit `open` mode when its listen
  address changes to a non-loopback interface; transition MUST require
  an explicit operator gate configuration. This prevents an MVP relay
  from accidentally becoming a public open relay by an address change.

### 9. Component Placement: Reusable `attestation-gate`

The verification primitive — resolve passport, check scope, verify
proof token, cache the decision — is a cross-cutting concern, not an
Agora-internal detail. It is placed as a reusable component in the
daemon's trust-boundary zone, alongside the existing signer and sealer
primitives.

**Zone rationale.** Signer and sealer are the *authentication and
protection* primitives (produce a signature, seal a payload). The
attestation gate is their *authorization counterpart* (decide whether a
given authenticated author is admissible under the current policy).
All three share the same architectural position: they sit between
participant-facing surfaces and the daemon core, they are fail-closed
on error, and they are the places where keys, passports, and policies
meet. Putting them in one zone means one audit boundary, one set of
cache invariants, and one place where operator policy is enforced
regardless of which caller asked.

**Component surface.** The gate exposes a narrow trait:

```
verify_attestation(
  claim:       AttestationClaim,   // { participant_id, passport_ref }
  proof:       Option<ProofToken>, // agora-attestation-proof.v1 or its unified successor
  context:     GateContext,        // { relay_or_component_id, predicates, now }
) -> AttestationOutcome             // { Accept | Refuse(reason) }
```

and one cache:

```
PassportResolutionCache {
  key:   (passport_id, relay_or_component_id, policy_version),
  value: ResolvedPassport { issuer, capability_id, scope, expiry, revoked_at },
  ttl:   min(passport.expiry - margin, operator_max_ttl),
}
```

Resolution is cache-first, seed-directory-next, resolver-last. The
cache is shared across consumers because the underlying passport
facts do not depend on who is asking.

**Consumers (non-exhaustive).** The §4 ingest modes and §5 predicate
grammar are Agora's consumption of this primitive. Other expected
consumers:

| Consumer | What it asks the gate |
|---|---|
| Agora ingest (this proposal §4–§6) | "admit this envelope under this topic's gate?" |
| Middleware peer-message dispatch (proposal 027) | "admit this peer message from this author under chain policy?" |
| Offer catalog submission (proposal 021 / 023) | "admit this offer from this author under catalog policy?" |
| Whisper surface (proposal 013) | "admit this signal under this privacy scope?" |
| Memarium custody acceptance (proposal 040 §3) | "accept custody request from this counterparty?" |
| Reputation signal publication | "admit this reputation signal author?" |
| Workflow event sinks | "admit this workflow-run emission?" |
| Seed directory write (proposal 025) | "admit this passport update?" |

Each consumer supplies its own `GateContext.predicates`. The §5
grammar is intended to be a superset useful across consumers;
consumer-specific predicates MAY be added without invalidating the
shared resolution cache.

**Separation from signer and sealer.** The gate MUST NOT hold
participant private keys and MUST NOT perform signing or sealing
operations. Its inputs are already-signed claims and already-signed
proof tokens; its outputs are Accept / Refuse decisions. The
signer/sealer primitives sit next to it but remain distinct: an
operator who audits signing does not need to audit authorization
logic, and vice-versa.

**Policy versioning.** The cache key includes `policy_version` because
a policy change (operator edits the predicate set) MUST invalidate
prior Accept decisions even if the passport itself is unchanged.
Proposal 040 §1 (operator sovereignty over current policy) requires
exactly this invariant.

**Ingest-mode config is consumer-local.** The §4 mode matrix
(`open`, `allowlist`, `passport`, `passport_scoped`, `layered`) is
Agora's configuration schema. Other consumers choose their own
configuration shapes on top of the same gate primitive. Nothing in
the gate itself is Agora-aware.

### 10. What This Gate Does Not Promise

- It does not assert personhood. `participant:did:key:…` remains a
  key, not a human.
- It does not assert truthfulness of `content`. Reputation and
  moderation layers address that; the gate only admits the author to
  the surface on which their statements will be judged.
- It does not unify trust across relays. Two relays MAY accept the
  same passport under different predicates; a record accepted by one
  may be refused by another without any contradiction.
- It does not prevent a participant from publishing to their own
  relay. Self-custody of one's own relay + own passport is allowed
  and useful; federation may then reject that relay's records on
  their own terms, which is exactly the sovereignty model.

## Consequences

Positive:

- authorship attestation becomes a first-class, operator-configurable
  part of the ingest contract rather than an ad-hoc ACL per relay,
- `author/attestation_ref` in the signed envelope gives archival
  readers a durable "under which passport was this said" signal,
- the predicate grammar lets one relay host very different trust
  surfaces side by side (announcements strict, opinions moderate,
  scratch private) without multiple daemons,
- custodian redelivery remains trivially compatible: bytes unchanged,
  gate symmetric,
- the reason-code vocabulary aligns with the tombstone vocabulary of
  proposal 040, giving clients one consistent outcome ontology across
  ingest refusal and readback absence,
- the "fail-closed on unknown predicate" rule prevents quiet
  mis-configurations from admitting more than intended,
- placing the verifier and its cache alongside signer/sealer
  consolidates the trust boundary into one auditable zone and lets
  every component (Agora, middleware dispatch, offer catalog,
  whisper, memarium custody, reputation, workflow sinks) share one
  passport-resolution cache, removing the temptation to re-implement
  attestation ad hoc per component.

Tradeoffs:

- relays that today accept any mathematically valid envelope will need
  an explicit configuration to remain that way on non-loopback
  listeners; this is a deliberate footgun-removal,
- authors publishing to multiple attested relays need one proof token
  per relay per ingest (short-lived, relay-bound), which adds one
  signing operation per shipment but prevents cross-relay replay,
- passport resolution introduces a dependency on seed-directory
  availability for the strict modes; relays SHOULD cache aggressively
  and operators SHOULD pick predicate sets whose cached state degrades
  gracefully,
- "passport taxonomy" choices leak into operator configuration; the
  proposal accepts this as operator-scoped complexity rather than
  freezing one global taxonomy.

## Open Questions

- Should `agora-attestation-proof.v1` and `agora-author-proof.v1`
  (proposal 040 §5) be unified into one short-lived self-proof
  artifact family, given that both carry
  `(participant-id, relay/id, issued_at, expires_at, nonce)` and
  differ only in audience?
- Should `assurance_at_least` be defined here or deferred until
  proposal 034 freezes the assurance-level lattice?
- Should the relay publish its own `GET /v1/agora/ingest/policy`
  endpoint so authors can discover the predicate set before signing,
  to avoid producing envelopes that will be refused?
- Should operator-local blocklists be a relay-private detail or a
  signed artifact that can itself be replicated across cooperating
  relays?
- Should `passport_scoped` mode also allow **author-declared** scope
  narrowing (an author choosing to publish "under the narrower half
  of their passport") as a privacy-preserving primitive?

## Follow-Up

If adopted, the next artifacts should be:

1. a schema file for `agora-attestation-proof.v1`,
2. an addition to the `agora-record.v1` schema registering
   `author/attestation_ref` as an optional signed field,
3. a capability-id registration for `agora.ingest` within the proposal
   024 scope grammar, with a minimal recommended profile shape,
4. a requirements document (federated profile, successor of
   requirements-014) that translates ingest modes and predicates into
   FR/NFR form,
5. an operational playbook for operators describing the default-safe
   gate configurations for the common deployment classes
   (local-only, community-hosted, public-open, strict-operator),
6. a cross-reference from proposal 040 §2 so the ingest-refusal
   reason-code matrix and the readback tombstone matrix are
   documented as one outcome ontology,
7. a crate-layout note for the reusable `attestation-gate` component
   placing it in the daemon's trust-boundary zone alongside
   `signer-core` and the sealer primitive, with a shared
   `PassportResolutionCache` consumable by every component listed in
   §9 (Agora ingest, middleware dispatch, offer catalog, whisper,
   memarium custody, reputation, workflow sinks, seed-directory
   writes), and an explicit non-goal of holding private keys.
