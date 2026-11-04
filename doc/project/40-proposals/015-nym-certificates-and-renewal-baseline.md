# Nym Certificates and Renewal Baseline

Based on:
- `doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`
- `doc/project/20-memos/nym-authored-payload-verification.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`

## Status

Proposed (Draft)

## Date

2026-03-28

## Executive Summary

This proposal freezes the first concrete application-layer artifacts for `nym`
issuance and renewal in Orbiplex Swarm.

The v1 baseline is intentionally modest:

- `nym` stays above the networking boundary,
- transport and session establishment remain ignorant of `nym`,
- Phase 1 uses ordinary Ed25519 signatures plus council-issued certificates,
- blocking is expressed operationally through refused renewal rather than strong
  verifier-local revocation,
- and later anonymity upgrades may replace the attestation or renewal mechanics
  without changing the basic `nym:did:key:...` identifier family.

## Context

Orbiplex already froze these identity boundaries:

- infrastructure trust and routing belong to `node-id`,
- authored participation belongs to `participant-id`,
- transport MUST NOT require `nym` resolution.

What was still missing was a concrete application-layer baseline for:

- issuing a fresh `nym`,
- renewing a `nym` line,
- carrying publicly visible continuity between pseudonymous epochs when desired,
- and rejecting renewal without disclosing whether the private cause was policy,
  operator choice, or ordinary departure.

## Goals

- Freeze concrete v1 artifacts for Phase 1 `nym` issuance and renewal.
- Keep the contract fully above the encrypted node-to-node session.
- Keep the cryptographic surface small enough for an MVP implementation.
- Leave room for later batch renewal, private reset, and stronger revocable
  anonymity.

## Non-Goals

- This proposal does not define true group signatures.
- This proposal does not yet define verifier-local revocation.
- This proposal does not force every application artifact to use a `nym`.
- This proposal does not define the full council governance process behind
  issuance, blocking, or unsealing.

## Decision

Orbiplex should adopt the following Phase 1 application-layer artifact family:

1. `nym-issue-request.v1`
2. `nym-certificate.v1`
3. `nym-succession.v1`
4. `nym-renew-request.v1`
5. `nym-renew-rejected.v1`

All of them are application-layer artifacts. They are exchanged over an already
established encrypted node-to-node session or another equivalently protected
application channel.

## Artifact Semantics

### 1. `nym-issue-request.v1`

The participant asks the council to certify a fresh `nym:did:key:...`.

Required semantic elements:

- participant identity,
- requested `nym` identity,
- requested TTL,
- freshness material,
- participant signature.

The request does not require networking-layer support. It is simply a signed
application artifact sent to the issuing authority.

### 2. `nym-certificate.v1`

The council certifies that a `nym` is valid for a bounded epoch and expiry
window.

The certificate carries:

- `nym/id`,
- epoch number,
- issue and expiry timestamps,
- optional leniency window for late continuity handoff,
- issuer identity in canonical `council:did:key:...` form,
- optional predecessor and succession proof for public continuity,
- council signature.

Public continuation is the default renewal mode for this baseline. Private reset is
a mode within the same contract family rather than a separate artifact family.

Receivers verify:

1. canonical council identity and whether it is present in the local trusted
   council list,
2. council signature over the certificate,
3. expiry or leniency semantics,
4. application-message signature by the `nym` key itself.

The canonical issuer form for Phase 1 is:

- `council:did:key:z...`

This keeps verification mechanical:

- parse the role-prefixed `did:key`,
- check local trust policy,
- verify the signature with the derived Ed25519 key.

The MVP trust model may start as a singleton in practice, but the configuration
shape should already admit a list so later council pluralism does not require a
format break.

Example direction:

```yaml
trust:
  councils:
    - "council:did:key:z6Mk..."
```

A council compromise should be treated as a compromise of an infrastructural
trust anchor, not as an ordinary operational failure. In particular:

- the trapdoor may become a tool for deanonymization,
- renewal refusal may become a tool of censorship,
- and nym certificates lose their epistemic value.

Therefore the `EMERGENCY-ACTIVATION-CRITERIA` layer SHOULD classify such a case
as an infrastructural-compromise trigger requiring trapdoor freeze, rotation of
`council:did:key`, and an ad hoc audit. This direction is already stated
explicitly in `DIA-EMRG-ACT-001`.

### 3. `nym-succession.v1`

This artifact is signed by the old `nym` and declares the next public `nym`
line.

It allows a public carry-over of pseudonymous reputation without exposing the
underlying participant.

It is optional in the overall system, but required for the public-continuation
path of Phase 1 renewal.

Limitation (2026-10-27): v1 is a one-sided declaration that works after expiry
only until `leniency-until`. This remains the current schema baseline until
P015-004 closes; it is planned to be replaced by the narrow
[`nym-succession.v2`](#succession-after-expiry-and-the-narrow-successor-2026-10-27)
(`P015-004`, MVP scope).

### 4. `nym-renew-request.v1`

The participant asks the council to accept a public continuation into the next
epoch.

The request includes:

- participant identity,
- succession proof already signed by the old `nym`,
- request freshness,
- participant signature over the whole request.

This lets the council check both:

- participant entitlement,
- and continuity of control over the old pseudonym line.

### 5. `nym-renew-rejected.v1`

The council can reject renewal through a coarse rejection artifact.

The rejection should be:

- correlated to the original request,
- attributable to a canonical `council:did:key:...` issuer,
- signed,
- and intentionally low-detail.

The baseline should prefer opaque reasons such as `policy` rather than revealing
whether denial came from explicit blocking, rate limits, custody failure, or
other internal criteria.

## Renewal and Leniency

Phase 1 supports a public continuation path with bounded grace semantics:

- while the certificate is active, the `nym` may sign ordinary application
  traffic,
- after `expires-at` but before `leniency-until`, the old `nym` is only valid
  for succession-related continuity work,
- after `leniency-until`, the old line is dead.

`leniency-until` appears only when grace semantics are granted. Absence of the field
means no leniency period; consumers must treat absence as strict mode.

This gives a simple operational way to:

- preserve pseudonymous continuity when desired,
- deny renewal without explicit public revocation,
- and avoid making every expiry look like immediate punishment.

## Blocking Semantics

In Phase 1, blocked participants are handled operationally:

- the council refuses renewal,
- the old `nym` expires naturally,
- external observers see non-renewal rather than a public linkage to the hidden
  participant.

This is intentionally weaker than true verifier-local revocation, but it keeps
the privacy boundary intact while preserving a small MVP cryptographic surface.

## Relationship to Later Phases

These v1 artifacts are a stepping stone, not the final anonymity model.

Later phases may add:

- synchronized epoch batches,
- private resets with no public predecessor link,
- non-revocation proofs,
- contextual participant nyms for Seed Directory publication, where the public
  discovery/reputation handle is not the root `participant:did:key`,
- or stronger revocable-anonymity constructions.

The stable invariant should remain:

- `nym` is an application-layer pseudonym,
- transport does not route on `nym`,
- Seed Directory should not require routine disclosure of root participant
  identity when a scoped nym can carry discovery and reputation semantics,
- and upgrading anonymity must not contaminate the networking boundary.

The later contextual-nym design should draw from multiple adjacent privacy
families: private messaging systems that minimize graph disclosure, shielded
cryptocurrency key/address hierarchies, and selective-disclosure credential
systems. The intended direction is not to make one of those systems normative,
but to preserve these properties: per-context identifiers, rotation, selective
continuity proofs, and avoidance of a globally linkable participant identity.

Later work should also split nym semantics by accountability class. Public,
reputation-bearing actions may use `accountable-nym` with a conditional
sealed-council unseal path, while private, consent-bound communication may use
`private-nym` with much stronger unlinkability and only local or group-scoped
reputation. This v1 certificate baseline does not freeze those classes, unseal
policy, or private group pseudonymity. It only keeps enough room for them by
keeping `nym` above transport and by avoiding routine disclosure of the root
participant identity.

Private-group removal has a separate unresolved requirement: a group may need to
exclude not only the current nym, but also future nyms controlled by the same
hidden subject, without learning the root participant identity. A later proposal
should define a scoped mechanism for that, such as group-local nullifiers,
issuer-side refusal, anonymous non-revocation proofs, or sealed group-local
exclusion handles. The mechanism must avoid turning private removal into a
globally linkable identifier.

## First Concrete Embedding

The first concrete nym-authored artifact should be:

- `whisper-signal.v1`

In that first artifact:

- routing and infrastructure attribution remain node-scoped,
- authored pseudonymous participation is expressed through `rumor/nym`,
- the artifact carries an attached `nym-certificate`,
- and the artifact body is signed by the `nym` key itself.

The backing `participant-id` stays on the local or issuing side of the trust
boundary and is not required on the wire for the receiving peer to validate the
rumor artifact.

## Candidate Embedding Pattern

Application artifacts that want `nym`-level authorship may later carry:

- authored payload,
- `nym/id`,
- attached or referenced `nym-certificate`,
- and a `nym` signature over the payload.

The first frozen path should use artifact-local embedding in
`whisper-signal.v1`, not a generic shared nym envelope. Different application
families may still want different provenance and replay semantics later.

Reusable receiver-side verification guidance now lives in:

- `doc/project/20-memos/nym-authored-payload-verification.md`

Messaging, contact, and Corpus application families should inherit this
artifact-local embedding pattern wherever artifacts are nym-authored. Each adoption
should remain schema-gated in its own family rather than introducing a generic shared
nym envelope prematurely.

## Contextual Whisper continuation (2026-10-25)

The accepted [contextual authorship profile](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)
adds private exchange, cumulative source revocation, backend-proven publication
time, lazy renewal and bounded issuer erasure. It supersedes public-continuation
as the default only for that Whisper profile; the generic baseline and historical
evidence retain their scope. Its two runtime gates remain pending.

## Succession After Expiry and the Narrow Successor (2026-10-27)

### Current State

- **Fact.** `nym-succession.v1` carries `old-nym/id`, `new-nym/id`, `epoch` and
  one signature by the old nym. Its signing preimage is not defined, and the
  example signature is a placeholder. It has no successor confirmation, scope,
  purpose, identifier, nonce, validity bound, audience or binding to the
  predecessor's certificate or records, and it allows additional properties.
- **Fact.** After `expires-at` the old nym may sign only succession work, and
  only until `leniency-until`. Without that field there is no grace at all. The
  contextual verifier bounds `leniency-until` to at most 24 hours after expiry
  and to the end of the epoch (`node:nym-core/src/status.rs`).
- **Fact.** The contextual Whisper profile publishes no succession: routine
  renewal keeps the source, and a private reset names no successor.
- **Fact.** Node validates the v1 shape in Schema Gate; no semantic succession
  verifier or renewal flow exists yet.
- **Inference.** Succession after the grace window, for example a year later,
  is impossible today, and v1 cannot express succession limited to one case.

### Decision

The planned narrow `nym-succession.v2` will replace v1 without a compatibility
path before the first release, when P015-004 closes. That single migration will
remove the v1 schema, example and acceptance, move `line/succession` in
`nym-certificate.v1` and `succession` in `nym-renew-request.v1` to v2, and update
all references, generated COVERAGE/schema pages and Node acceptance together.
The existing v1 artifacts and section 3 are the current baseline, not evidence
that this migration has happened.

v2 proves that the holder of an authorized predecessor key and the holder of
the successor key agree on one transition. It does not prove that one person
controls both keys: the two signatures may come from one participant or from
two people agreeing to hand over control. No v2 purpose therefore identifies
sources, and no counting authority merges two sources on the basis of a
succession. Source equivalence would need a separate attestation by the
issuer.

| Field | Meaning |
|---|---|
| `schema` | Constant schema id |
| `succession/id` | A random identifier; the replay key, and the `request/id` of a `case` succession |
| `succession/scope` | `line` (public continuation of a pseudonym line) or `case` (one matter) |
| `succession/purpose` | A closed enum: `continue-line` or `continue-case` |
| `predecessor/nym` | The predecessor nym id |
| `predecessor/certificate` | The predecessor certificate digest; required for scope `line` and forbidden for scope `case` |
| `authorization/mode` | `nym-key` or `continuity-key` |
| `authorization/public-key` | The authorizing public key; for `continuity-key` it must match the commitment in the `case/anchor` record |
| `successor/nym` | The successor nym id |
| `successor/certificate` | The digest of the successor's current certificate |
| `case/anchor` | The original signed record digest, from the shared case request header of P013; required for scope `case` and forbidden for scope `line`. The order of a `case` succession comes from the case authority's acceptance, not from this artifact |
| `audience` | The named recipients; `line` successions are public by nature |
| `issued-at`, `not-after` | A short validity window |
| `signatures` | Exactly two semantic authorizations: predecessor authorization and successor acceptance; both Ed25519 in Phase 1 |

- **Suite boundary.** The first wire profile uses strict Ed25519 for both
  authorizations and the continuity key. P081 separates verification from its
  suite, but does not make this artifact algorithm-agile. No free-form `alg`
  field is admitted; another suite needs a versioned, allowlisted profile and
  new golden/refusal vectors. The two-authorization semantics stay independent
  of that choice.
- **Preimage.** Both signatures cover the same bytes: the ASCII domain
  `orbiplex.nym-succession.v2`, one NUL byte and the JCS of the artifact
  without `signatures`, following the contextual profile's signing rules and
  strict Ed25519 verification. The successor signature is also its proof of
  possession.
- **Authorization modes.** `nym-key` is valid only for scope `line` and only
  until the predecessor's `leniency-until`; it preserves Phase 1 public
  continuation. `continuity-key` uses a key committed in advance and remains
  usable after the grace window, for scope `case`
  ([P013 case-bound succession](013-whisper-social-signal-exchange/long-lived-rumors.md#case-continuity-key-and-case-bound-succession)).
- **Successor.** The successor performs a new operation, so its certificate
  must be valid now.
- **Signature uses.** The successor's signature is a proof of possession inside
  this domain-separated protocol. Only the succession verifier accepts it, with
  a currently valid certificate; it is not a publication and needs no Agora
  scope, and a publication verifier never accepts it. Any new nym publication,
  such as a Whisper correlation notice, needs its bound kind/schema/topic/scope
  tuple explicitly authorized by the post-MVP P015-005 profile
  ([P013 signature uses](013-whisper-social-signal-exchange/long-lived-rumors.md#signature-uses-and-certificate-scope)).
- **Currency.** Offline verification shows that a `case` succession is
  authentic, not that it is still the effective succession of its case. That
  requires the case status of
  [P013 case state](013-whisper-social-signal-exchange/long-lived-rumors.md#case-state-and-currency),
  whose `case/current-succession` must name this event.
- **Narrow schema.** No additional properties, closed enums and negative
  fixtures.
- **Limits.** Succession renews no certificate, does not make the
  predecessor's records valid now (historical verification is separate), never
  adds a counted source and never merges two sources.

| Predecessor state | Treatment |
|---|---|
| Certificate expired, key still controlled | `nym-key` within grace; afterwards only `continuity-key` succession |
| Key lost or deleted | No direct proof. With a retained continuity key, `case` succession still works; otherwise there is no succession, because the council keeps no mapping after its retention |
| Key compromised or authority revoked | A signature by the predecessor nym key never suffices. A separate continuity key is required, and a closed or conflicted case status blocks succession |

Disclosure is deliberate. A recipient of a succession proof learns the link
between the two nyms, and a scope limits the permitted effects, not that
knowledge. `case` successions therefore travel only to their audience over the
private exchange path.

### Succession and Scope: Implementation Recommendations

Planned refinement, 2026-10-28; implementation status is unchanged. Use the
[P013 reuse dispositions](013-whisper-social-signal-exchange.md#implementation-reuse)
and the existing `node:nym-core` owner instead of separate succession verifiers
in Whisper, Vault and relay code. The MVP verifier remains pure and does not
acquire a dependency on post-MVP case storage or delivery.

[P013-LLR-009 owns the portable case-succession presentation](013-whisper-social-signal-exchange/long-lived-rumors.md#portable-case-succession-verification).
It supplies verified anchor/certificate inputs to this verifier, then checks
ordered acceptance and current case status separately. Reuse the existing nym
certificate representation and
[P032's cross-artifact verification contract](032-key-delegation-passports.md#shared-verification-operations);
P076 is one consumer precedent. Do not wrap
Whisper succession in a Messaging passport or accept its grant status as case
currency. A detached ADC manifest plus a P035 receipt can establish the anchor's
key/authority/lifetime binding under an admitted profile without disclosing the
private body; its result records reliance on that receipt signer. A missing
safe anchor proof is unresolved, not permission to fetch the private signal.
Presentation limits, safe assembly and network-denied host acceptance are
post-MVP LLR work, not additional completion conditions for P015-004.

The [Whisper family matrix](013-whisper-social-signal-exchange.md#portable-verification-profiles)
also applies that contract to signals, notices and manifest signatures through
their existing nym adapters. P015-005 freezes the minimum certificate/profile
evidence for both publication and auxiliary use, including their disclosure and
resource bounds; the common byte verifier does not turn one use into another.

Reuse `nym-core`'s canonical parsing, NFC refusal, canonical base64 decoding and
per-use signing-byte pattern, backed by `canonical-json` and
`crypto::verify_message_strict_base64url`. Add a closed succession signing-use
wrapper that removes only `signatures` and applies the prescribed domain; no
caller supplies an arbitrary domain or list of unsigned fields. Preserve the
existing certificate preimage, including its existing domain treatment. A
cleanup must not rewrite already signed artifacts or historical verifier rules.

The narrow verifier consumes the artifact, verified certificate/anchor inputs,
an admitted profile, expected audience and explicit evaluation time. In order:

1. Enforce byte/depth bounds, Schema Gate, canonical encoding, closed field
   combinations, and the scope/mode/purpose matrix.
2. Select the predecessor authorization from the verified line certificate or
   the verified anchor's continuity-key commitment; never infer it from a key
   presented in the request. Check the appropriate validity/grace bound and,
   for case scope, the verified anchor's case lifetime.
3. Resolve the successor key from its current verified certificate, check the
   artifact window and audience, and build the preimage once.
4. Verify both named signature roles over those same bytes using the closed
   Phase 1 suite. Return a typed authentic succession binding, not a publication
   permit or a statement that the case is current.

Keep three results separate: `AuthenticSuccession` (this verifier),
`AcceptedCaseSuccession` (LLR's ordered acceptance) and current authorization
(fresh LLR case status). An idempotency owner stores the verified artifact
digest under its scoped succession id: equal bytes replay, different bytes
conflict. A pure verifier alone cannot detect replay across process restarts.
P015-004 qualifies the replay decision with supplied prior state; LLR-007/008
own durable case replay. Do not put an in-memory seen-id cache inside the crypto
verifier and call it durable protection.

For P015-005, use one typed publication-use tuple and one matching operation
through issuance request, issuer narrowing, certificate and receiver checks:

```text
PublicationUse = (record_kind, schema, topic, disclosure_scope)
AuxiliaryUse = (signing_domain, declared_publication_context)
```

Match a whole admitted tuple using the owning profile's topic rules. Never
match four independent sets or infer auxiliary permission from publication
permission. The new closed profile must adapt at its boundary; the old
signal-only profile keeps its exact validation. Golden and negative fixtures
are shared by producer and consumers, including crossed tuple fields, altered
signature roles/preimages, a manifest presented as publication, wrong audience
and missing anchor proof. The two uses share cryptographic mechanics, not grants.

### Succession Tracker

`P015-004` is MVP scope: it must close before the MVP release, not as a
post-MVP follow-up.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P015-004 | Replace `nym-succession.v1` with the narrow v2 successor (MVP) | todo | P015-001 | `nym-succession.v2` schema with the fields, closed enums and the two-signature preimage above; v1 schema, example and acceptance removed; references in `nym-certificate.v1` and `nym-renew-request.v1` moved. A semantic verifier in Node covers both authorization modes, the grace bound for `nym-key`, the current successor certificate, replay and the `case/anchor` rule; the successor signature is accepted only on this possession-only path. Negative fixtures: one signature only, signatures over different bytes, `nym-key` after grace, continuity-key mismatch, extra fields, expired `not-after`, a reused `succession/id` with different bytes, a `case` succession without `case/anchor`, a `line` succession with it, and a successor signature presented to a publication verifier. MVP covers `continuity-key` mode only at the verifier level: a pure decision over a given anchor commitment and revealed key, with golden vectors. Vault custody of continuity keys, case state, private delivery and the Whisper flows are post-MVP in P013-LLR-006–008. Follow the pure verifier sequence and shared byte-law fixtures in the implementation recommendations; supplied replay state remains separate from durable LLR runtime. |

### Embargo Authorship Scope Tracker

Post-MVP; independent of the narrow MVP verifier in P015-004. The existing
contextual profile remains restricted to `whisper-signal`/`whisper-signal.v2`.
A key's ability to sign is not permission to publish another kind.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P015-005 | Issue and verify explicit notice and manifest scopes | todo | P015-001 | Freeze and version a closed contextual profile with authorized **tuples** of `(record/kind, schema, topic, disclosure/scope)`, never independent lists granting their Cartesian product. Issuance requests, issuer policy, certificates and receiving verifiers preserve the same tuple. A separate domain-bound auxiliary use permits `whisper-embargo-manifest.v1`, checked against its declared publication context, key and validity at admission; it grants no Agora publication by itself. Reuse P015/P081 signature and scope verifiers. Negative fixtures substitute kind/schema/topic/scope, present a manifest signature as publication, and use an ordinary signal-only certificate for notice or manifest. Positive fixtures admit an explicitly scoped notice and manifest while keeping the predecessor narrow profile unchanged. ADC consumes this grant; this task does not depend on ADC runtime. Use one typed tuple matcher across request, issuer and receiver, with separate auxiliary-use admission; preserve the old profile's golden/refusal vectors. |

P015-005's gate also freezes bounded certificate/profile evidence for the notice
and manifest uses under the [P032 contract](032-key-delegation-passports.md#shared-verification-operations).
Network-denied producer/consumer fixtures cover both uses, wrong scope, missing
evidence and self-supplied authority; valid cryptography never widens a grant.

Both tracker rows include the shared primitive/refusal fixtures and the
[milestone convergence gate](013-whisper-social-signal-exchange.md#milestone-convergence-gate),
within their own MVP or post-MVP scope.

The profile contract is owned here and detailed in the
[contextual continuation](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#notice-and-embargo-manifest-scope-extension).

## P081 Scoped-Claim Adoption

The certificate baseline now has one reusable, suite-neutral verification adapter in
Solution 043. `orbiplex.nym-ed25519-cert.v1` verifies an allowlisted council
signature, certificate validity, possession of the certified nym key, supported
predicate scope, and fresh local revocation evidence before returning scoped claim
evidence. It does not turn the certificate into a capability and does not claim zero
knowledge.

The first adapter emits only `nym/certificate-current` and, when the certificate
explicitly supports it, `nym/context-authorized`. Its durable nonce runtime binds a
presentation to request digest, audience, context, expiry, and linkability. The first
suite rejects nullifiers because this certificate profile cannot prove their domain
separation. Stronger unlinkable suites and richer verifier-local non-revocation remain
post-MVP work under P081 rather than hidden extensions of this certificate baseline.

## Private Issuance Delivery: Implementation Recommendations

Planned continuation (2026-10-11): issuance and renewal use
[S023 Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
with [S017 INAC](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md)
as the private carrier. This refines the protected application channel above;
it does not put nym resolution in the networking handshake or replace P081
certificate/presentation verification.

The flow is `authorized applicant -> AD/INAC -> issuer acceptor -> issuer
decision -> AD/INAC -> applicant result acceptor`. Configure exactly one domain
acceptor per artifact family. Reuse existing schema/signing primitives and
hosted middleware contracts instead of adding council-specific peer listeners.
Local key custody remains with the host/Pseudonym Vault, not the issuer transport.

Freeze an exchange binding over exact request digest, applicant proof, issuer,
permitted reply recipient, purpose and expiry. A supplied reply address is not
authority to forward identity material. Bootstrap delivery authorization must
work without the not-yet-issued nym certificate, through an independently admitted
invitation/capability profile. Issuance policy remains the council's responsibility.

Recheck validity before each irreversible issuer action. Persist the domain
request/decision correlation atomically or through a replayable journal; duplicate
delivery reuses the retained decision rather than issuing another certificate.
AD acceptance only confirms delivery/admission, not certification. A private reset
must not disclose predecessor linkage; public succession requires its own explicit
publication decision, not fallback from failed private delivery. Minimize and
bound applicant-to-nym mappings in logs, ledgers, status and retained artifacts.

### Delivery Integration Tracker

These rows track the contextual continuation separately from the existing P081
verification adapter. The 2026-10-25 schema, pure-verifier and erasable custody
foundation does not qualify issuer/applicant runtime or either acceptance gate.
The optional Node issuer foundation now includes ciphertext-only phase preparation,
metadata-only offer bootstrap, key custody, encrypted-image preflight and the
context-scoped decision/status lifecycle. Its ordinary applicant and issuer host
adapters and closed local API contracts are being integrated on the authorship
branch. Software conformance does not qualify the two-daemon AD/INAC path: actual
issue/renew/reject/reset, host signing, cleanup, restart and replay still require
Gate A/B runtime evidence. Partial Node diagnostics recorded on 2026-10-30 now
observe real private AD issue, source-preserving renewal, private reset activation
waiting and ordinary protected host signing. Explicitly authenticated HTTP UI
readback and independent signature inspections remain narrow observations: the
complete lifecycle/refusal, erasure, aggregate, SQLite/Synapse and retained-replica
gates are still open. See `node:docs/MVP.md` and the current authorship runner at
`node:tools/acceptance/whisper-authorship/README.md`; these prefixes do not change
the partial tracker states below. A subsequent clean Node continuation observes
actual SQLite/Synapse source-journal/replay, stable expiry, renewal/reset basis
`2 -> 1 -> 2`, held AD reply recovery and bounded old-ciphertext erasure checks.
Those are private prefixes with original refusals, not the complete authority,
uniqueness, erasure/privacy matrix or qualified two-store evidence. Both formal
gates remain open. The new public v2 content contracts do not renew the
historical node-counting M4 qualification. Follow `node:DEV-GUIDELINES.md` and update Node's ledger when
implementation evidence exists.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P015-001 | Freeze private issuance/renewal exchange binding | partial | S023/S017 admission contracts | Existing artifacts are checked for request/reply correlation coverage; any additive or versioned schema changes and negative fixtures are explicit. Independent bootstrap authority, reply binding, expiry, replay key and privacy/retention budget are pinned before runtime exposure. |
| P015-002 | Wire issuer and applicant acceptors | partial | P015-001 | Reuse hosted middleware, host signer and AD client/acceptor seams; issuance/refusal is a separately persisted domain decision. No new peer listener, issuer retry queue, implicit key export or public fallback. |
| P015-003 | Prove two-node issue/renew/reject recovery | partial | P015-002 | Retain real private carrier evidence for initial issuance, renewal, private reset and refusal, duplicate request/reply, restart, lost reply, stale authority, wrong issuer/recipient and expiry. No second issuance or participant/predecessor leakage in public surfaces; delivery never displays as certificate approval. |


Checkpoint 2026-11-02: ordinary protected AD issue, real-expiry lazy renewal and
private reset now have fresh independent predicates on the corrected runtime,
including latest-lease drain and one concrete post-ACK ciphertext refusal.
A subsequent controlled private-response failure/restart case on frozen runtime
`bde3272f` and clean capture `e100b94d` has fresh independent predicates for
issue, reference readback, duplicate submission and recovery of the same reply
across A/D restart. Its original fault-injected class, deadlines and owner state
are preserved; this is not spontaneous ACK loss or retransport after AD expiry.
The clean full software gate passes 9,264/0/127. P015-001–003 remain `partial`:
these subsets do not replace the complete authority/recovery/privacy matrices,
SQLite/Synapse Gate B or qualified both-store retention. See
[the contextual checkpoint](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#qualification-checkpoint-2026-11-02)
and the Node implementation ledger.

The later native-provider subset on `7da785e9` independently verifies four
process-interruption cuts with metadata-only startup inspection before recovering
key methods. The earlier weaker shape refuses that predicate. This leaves the
remaining old-database, authority/status/privacy, backend and both-store gates
open; no tracker row advances to `done`. See the
[encrypted-provider checkpoint](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#encrypted-provider-process-interruption-subset-2026-11-02).

### Current qualification boundary — 2026-11-03

Clean Node `c6f57910` / Orbidocs `92d0fe7b` independently verifies42/67 required
prefix obligations. Six newly composed C-class requirements bind the original
component-test receipts, concrete nonignored assertions and48 exact canonical/Node
schema byte pairs. They establish conformance, without granting runtime HTTP or
scheduled-renewal execution. The original UI/AD, source-uniqueness, both backend
reset/current-result cuts, complete selected Matrix PDU and explicit fixture
image-backup preflight keep their original heterogeneous source/tool identities.

The clean `bb060dd8` / `92d0fe7b` full software gate passes9315/0/128 with
incremental disabled, strict workspace Clippy and final paths. This does not close
A/B. Thirteen A and twelve backend B obligations remain, as do final single-candidate
qualification, optional scheduled continuation and qualified two-store retention.
Post-ACK diagnostics still require adequate owner/process composition; a recovering
key API's `KeyDestroyed` result alone proves no earlier maintenance execution.
P015-001–003 stay `partial`. See the contextual profile and Node ledger/audit for
exact source and proof scope.

## Open Questions

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-04:

1. Public continuation is the default renewal mode. Private reset remains a mode
   within the same contract family rather than a separate artifact family for
   this baseline.
2. Phase 1 certificates carry `leniency-until` only when grace semantics are
   granted. Absence of the field means no leniency period.
3. Messaging, contact, and Corpus application families should inherit the same
   nym-certificate embedding pattern where artifacts are nym-authored.

## Next Actions

1. Document `public-continuation` as the default renewal mode in `nym-certificate.v1`
   schema docs; `private-reset` remains a mode within the same contract family.
2. Add the `leniency-until` schema invariant: field presence implies grace, field
   absence implies no leniency.
3. Apply the artifact-local embedding pattern to messaging, contact, and Corpus
   nym-authored artifact families as separate schema-gate tasks.

The clean Node `b212be6a` continuation freshly verifies43/67 obligations in
composition613 (103 native calls). Its new original post-ACK predicate derives all
73 explicit retained key references and19 old ciphertext buffers, verifies the
signed closing status and local ACK deadline, and checks native key-file absence
before recovering provider open. Capture and later qualifier have distinct source
pins. Twelve A and12 backend B obligations, final single-candidate execution,
privacy and retained-store equivalence remain open; P015-001–003 remain partial.
Implementation review:
`node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#complete-original-retirement-inventory-review-2026-11-03`.


## Independently verified source replay checkpoint (2026-11-03)

Clean Node `b7b2cf49` composition627 freshly verifies **45/67** obligations through
111 native inspections. Actual Matrix619 and SQLite622 restart after loss of only
the derived contextual cache and perform real owner replay. Original source,
admission, nonce, receipt, first-emission and history tables remain unchanged.
A separate ended-epoch/no-cache verifier checks the actual current readback; it
neither weakens fresh-view assertions nor supplies fresh active-epoch evidence.
Original fresh-only refusal624 remains preserved.

Twelve A authority/status/privacy and five B cases per backend remain. Runtime,
capture and verifier pins differ explicitly. The heterogeneous prefix inventory
does not close final single-candidate A/B or loose/extracted/fresh two-store
qualification. P015-001–003 and complete contextual authorship remain partial.
See `node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#independent-original-backend-replay-qualification-2026-11-03`.


The subsequent original631 controlled AD receiver cases observe rejection of
four encrypted invalid private requests, with no prepared decision or new target
context. Clean Node `e75dd92a` independently reinspects their valid baselines,
council offers and isolated faults in633. The temporary local source adapter is
explicit fault injection and is restored after D stops; it proves no INAC/network
authority. An expired anonymous first leg remains a separate narrower witness.
Process/input/effect qualification and recomposition are still required, so
coverage remains45/67 and both complete gates remain partial.


## Independently qualified private receiver refusal checkpoint (2026-11-03)

Clean Node `f270f62a` composition636 freshly verifies **49/67** obligations through
115 native inspections. Four original631 full-request refusals now have complete
process, exact input, AD receipt, offer/outbox/recipient and no-effect predicates.
No decision is prepared and no new issuer context appears. The temporary local
fault adapter is restored after D stops; this does not prove INAC authority.
The expired anonymous first leg remains separate from full-request expiry.

Eight A and five B cases per backend remain. Capture, runtime, fixture client,
native verifier and profile revisions are independently pinned. Final
single-candidate A/B, privacy and retained two-store equivalence remain open;
P015-001–003 and complete contextual authorship stay partial. Review:
`node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#independent-original-private-ad-refusal-qualification-2026-11-03`.


### Independent original full private-request expiry checkpoint (2026-11-03)

Clean Node `8d590a16` independently qualifies original638: a full, unchanged
private request and signed council key offer were valid when frozen; after the
original 30-second deadline, actual D runtime `103c8fae` permanently rejected
that exact sealed buffer with `expires/at: expired`. No decision or new target
context was created. Owned cleanup and temporary local adapter restoration
completed. Capture, client and native verifier are pinned to clean `153932f9`;
this controlled local AD refusal is distinct from INAC transport authority and
from the earlier narrower expired anonymous first leg.

Fresh composition641 covers **50/67** obligations through 116 native calls.
Seven A authority/status/privacy obligations and five B obligations per backend
remain open. The remaining B scope is late first receipt, collection/emission
freshness, public privacy, retired acceptance environment and UI refusals.
273 Python profile tests, 24 native inspector tests, five negative-client tests
and strict all-target Clippy for both affected crates pass without incremental
compilation. Scoped headers and the light gate pass; a broader header migration
audit separately refuses an existing unrelated Sensorium inventory mismatch,
which this work leaves untouched. Final single-candidate A/B and fresh two-store
retention remain unqualified. P015-001–003, full Whisper and global readiness
retain their partial/bounded scopes; historical runtime evidence is unchanged.


### Independently qualified status-HWM checkpoint (2026-11-03)

Complete qualification653 at clean Node `bc480a7a` binds original648's actual
A/D processes, S020 proxy response bytes, scoped HTTP reads and immutable source
images. It verifies signed revision4→5 progression, refusal of older still-valid
bytes and the higher retained HWM/API after A restart. Native42 independently
checks original signature/time/cursor semantics. Original652's discriminator
refusal is preserved; the correction requires canonical integer `schema/v = 1`.
The final cached forward read remains distinct from a completed healing fetch.

Fresh composition654 covers **52/67** obligations in 118 native calls. Five A
cases and five B cases per backend remain open, along with final single-candidate
A/B and fresh retention from both adopted stores. Tests: 282 Python profile and
25 native inspector cases, affected all-target Clippy, scoped headers and light
gate pass without incremental compilation. No full historical runtime cohort
is renewed. P015-001–003, full Whisper and global readiness retain partial/bounded
scope. Owned A/D and proxy stopped and original A adoption was restored.


### Independently qualified private-minimum checkpoint (2026-11-03)

At clean Node `9e2c4dcb`, independent665 verifies original664: ordinary renew
retains public floor1 while the local private minimum13 refuses still-valid
signed status12. Actual preview returns the typed status-revision-unavailable
503 and readback has no authoring result. After actual status15 arrives, the same
certificate signs the reviewed confidence0.5 document through the ordinary host;
readback preserves the exact signed record. Four native checks verify certificate,
both statuses and reviewed record. Exact source/process/HTTP/proxy pins, original
time windows and cleanup/restoration bind the controlled runtime. No private
decision plaintext is reconstructed. Earlier producer failures remain unchanged.

Fresh composition666 covers **53/67** obligations in 122 native calls. Four A
cases remain: wrong exchange digest, revoked bootstrap authority, status
equivocation and private AD/tombstone privacy. Five B cases per backend, final
single-candidate A/B and fresh retention from both adopted stores remain open.
All 297 Python profile tests and scoped headers/light gate pass. Runtime source
`103c8fae` is unchanged; no full historical runtime or software gate is renewed.
P015-001–003, full Whisper and global readiness retain partial/bounded scope.
Owned A/D and proxy stopped; original A adoption restored. No merge/push.


### Independently qualified withdrawn-bootstrap checkpoint (2026-11-03)

Clean Node `b8dbfd76` inspection673 independently verifies original669: exact
valid INAC offer, signed active-to-revoked bootstrap authority, unlocked but
blocked issuer, actual403 before and after owned restart and absent issuer
reply/applicant certificate. Two native owner calls preserve the independently
adopted root and original times. The reason-only HTTP projection is retained
exactly and bound to separate captured coarse owner results; it is not expanded
into a claim of raw HTTP preservation. Original668 and672 coordinator failures
retain their original outcomes. Withdrawal is permanent, without reimport or
automatic authority replacement.

Fresh composition674 covers **54/67** obligations in 124 native calls over
8,446 logical reads/322,724,216 bytes; result SHA-256 is
`0319cbfc5bc6d6796bc6540516f3440425ee778d3054ca6fd202367c456c10b7`.
Three A cases remain (wrong exchange digest, status equivocation and private
AD/tombstone privacy), plus five B cases per backend, final single-candidate
qualification and fresh two-store retention. All310 Python profile tests pass;
the28 native and affected strict Clippy/paths evidence retains its stated source.
Native43 uses clean `85b8c9e3`, without incremental; runtime `103c8fae` is unchanged.
This does not renew the complete software/transport qualification or close
P015-001–003, either full gate, Whisper or release readiness. No merge/push.


### Independently qualified status-equivocation checkpoint (2026-11-03)

Clean Node `d14a3c89` inspection682 binds original681 actual host S020, exact
proxy response bodies, owner/control/process identities and four immutable
source images. Two correctly signed statuses have the same revision4 and
different canonical digests. The owner refuses the conflict before and after
A restart, preserving the original status, durable cursor and actual API view.
Three fresh native calls verify the certificate and both original-time conflict
transitions. Fixture-only operator signing and proxy adoption are restored;
no council key is exported. Native44 uses clean `107b436b`, separately from
runtime `103c8fae` and the later inspection source.

Fresh composition683 covers **55/67** obligations in127 native calls over
8,502 logical reads/323,488,096 bytes, with result SHA-256
`bde6f2270965e6f786f96e7e8524fc17b9ec1994d50b296a17f4d156ad06d181`.
The324 profile Python and29 native example tests, affected strict Clippy/paths,
scoped headers and light gate pass. At that checkpoint, two A cases remained
(wrong exchange digest and private AD/tombstone privacy), five B cases per backend, final single-candidate
qualification and fresh two-store retention. P015-001–003 and both full gates
retain their partial scope; no new full transport, software or release claim.

Original680 completes ordinary protected AD issue with two explicit recovery
exports. Original679 expiry and684 missing-decision outcomes remain failures.
For684, the correlated receiver row says `expires/at: expired`, while its AD
admission timestamp is5.274067 seconds before the original deadline. Exact
subsequent owner verification time is unknown. The earlier diagnostic's
arrival-after-expiry assumption is explicitly refused; the corrected source
snapshot/row correlation is retained separately. This does not qualify a
wrong-digest refusal or justify extending the signed deadline. Owned actors
are stopped, protected originals retained, and no merge/push occurs.


### Independently qualified private-decision binding (2026-11-03)

Clean Node039b46ec inspection697 now qualifies `A/wrong-exchange-digest` from
original694. The profile binds actual owned A/D processes, authenticated controlled
AD submission, the exact INAC offer/notification/consent and sealed reply, the
stored typed applicant refusal, and unchanged absent decision/certificate after
restart. Later read-only source snapshots696 verify the exact original A/D
admissions without pretending to have been captured at the original admission
time. Native45 (cleanbe2781d6) freshly checks both council signatures, the anonymous
proof at original time and exact sealed public-recipient binding. It never
reconstructs the private request, decrypts, signs or creates admission.

Fresh composition698 verifies **56/67** obligations through128 native calls over
8,635 logical reads/344,823,251 bytes; result SHA-256
`16a18e3144219707ee004bfa0368e7c9599c520f072a012f4537a2da9e33e2a8`.
The339 profile conformance tests include corrupt/missing sources, rebound causes,
foreign owners, nonunique source identities and incomplete INAC/restart witnesses.
One A privacy obligation, five B obligations per backend, final current-candidate
qualification and identical fresh retained-store qualification remain.
P015-001--003 and both full gates stay partial; global Agora, full Whisper and
release readiness are unchanged. Earlier failed attempts and prefix-only claims
remain historical. No merge or push occurs.


### Independently audited private storage (2026-11-04)

Clean Node73dc0288 composition703 verifies **57/67** obligations, including all30
A predicates, through128 fresh native calls. This remains an original-prefix
composition; the final current-candidate cohort and qualified retained retrieval
are not inferred. Five B obligations per backend remain. P015-001--003 and both
full gates stay partial. See the [profile closeout](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#independently-audited-private-storage-2026-11-04)
for private INAC authorization disclosure, source boundaries and exact results.

The final source-boundary review rejects hidden/generated columns and user tables
resembling SQLite internals; fresh703 repeats the full57-predicate closure under
that guard. The earlier702 source-bound result remains historical and unchanged.


2026-11-04 later SQLite receipt checkpoint: clean Node61b27ba8 composition719
verifies58/67 obligations, now including real first receipt after certificate
expiry plus skew with the original signed publication time. Nine B predicates,
final current-candidate cohort and two-store retained qualification remain open.
P015-001--003 and both complete gates stay partial. See the
[contextual checkpoint](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#actual-late-first-sqlite-reception-2026-11-04).
