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
only until `leniency-until`. It is replaced by the narrow
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

The narrow `nym-succession.v2` replaces v1 without a compatibility path, which
is acceptable before the first release. The v1 schema, its example and its
acceptance are removed. `line/succession` in `nym-certificate.v1` and
`succession` in `nym-renew-request.v1` move to v2, and no node accepts v1
afterwards.

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
| `succession/id` | A random identifier; the replay key |
| `succession/scope` | `line` (public continuation of a pseudonym line) or `case` (one matter) |
| `succession/purpose` | A closed enum: `continue-line` or `continue-case` |
| `predecessor/nym` | The predecessor nym id |
| `predecessor/certificate` | The predecessor certificate digest; required for scope `line` and forbidden for scope `case` |
| `authorization/mode` | `nym-key` or `continuity-key` |
| `authorization/public-key` | The authorizing public key; for `continuity-key` it must match the commitment in the `case/anchor` record |
| `successor/nym` | The successor nym id |
| `successor/certificate` | The digest of the successor's current certificate |
| `case/anchor`, `case/revision`, `case/previous` | The shared case event header of P013: the original signed record digest and the event order; required for scope `case` and forbidden for scope `line` |
| `audience` | The named recipients; `line` successions are public by nature |
| `issued-at`, `not-after` | A short validity window |
| `signatures` | Exactly two Ed25519 signatures, authorization and successor acceptance |

- **Preimage.** Both signatures cover the same bytes: the ASCII domain
  `orbiplex.nym-succession.v2`, one NUL byte and the JCS of the artifact
  without `signatures`, following the contextual profile's signing rules and
  strict Ed25519 verification. The successor signature is also its proof of
  possession.
- **Authorization modes.** `nym-key` is valid only for scope `line` and only
  until the predecessor's `leniency-until`; it preserves Phase 1 public
  continuation. `continuity-key` uses a key committed in advance and remains
  usable after the grace window, for scope `case`
  ([P013 case-bound succession](013-whisper-social-signal-exchange.md#case-continuity-key-and-case-bound-succession)).
- **Successor.** The successor performs a new operation, so its certificate
  must be valid now.
- **Signature uses.** The successor's signature is a proof of possession inside
  this domain-separated protocol. Only the succession verifier accepts it, with
  a currently valid certificate; it is not a publication and needs no Agora
  scope, and a publication verifier never accepts it. Any new nym publication,
  such as a Whisper correlation notice, needs its record kind and schema listed
  explicitly in the certificate scope
  ([P013 signature uses](013-whisper-social-signal-exchange.md#signature-uses-and-certificate-scope)).
- **Currency.** Offline verification shows that a `case` succession is
  authentic, not that it is still the effective succession of its case. That
  requires the case status of
  [P013 case state](013-whisper-social-signal-exchange.md#case-state-and-currency),
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

### Succession Tracker

`P015-004` is MVP scope: it must close before the MVP release, not as a
post-MVP follow-up.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P015-004 | Replace `nym-succession.v1` with the narrow v2 successor (MVP) | todo | P015-001 | `nym-succession.v2` schema with the fields, closed enums and the two-signature preimage above; v1 schema, example and acceptance removed; references in `nym-certificate.v1` and `nym-renew-request.v1` moved. A semantic verifier in Node covers both authorization modes, the grace bound for `nym-key`, the current successor certificate, replay and the `case/revision`/`case/previous` rules; the successor signature is accepted only on this possession-only path. Negative fixtures: one signature only, signatures over different bytes, `nym-key` after grace, continuity-key mismatch, extra fields, expired `not-after`, a reused `succession/id`, a `case` succession without `case/revision` and a successor signature presented to a publication verifier. MVP covers `continuity-key` mode only at the verifier level: a pure decision over a given anchor commitment and revealed key, with golden vectors. Vault custody of continuity keys, case state, private delivery and the Whisper flows are post-MVP in P013-LLR-006–008. |

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
The optional Node issuer currently provides ciphertext-only phase preparation,
a durable metadata-only offer bootstrap, key custody and encrypted-image
preflight; domain acceptors, decisions, status delivery and scheduled cleanup
remain pending. Follow `node:DEV-GUIDELINES.md` and update Node's ledger when
implementation evidence exists.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P015-001 | Freeze private issuance/renewal exchange binding | partial | S023/S017 admission contracts | Existing artifacts are checked for request/reply correlation coverage; any additive or versioned schema changes and negative fixtures are explicit. Independent bootstrap authority, reply binding, expiry, replay key and privacy/retention budget are pinned before runtime exposure. |
| P015-002 | Wire issuer and applicant acceptors | partial | P015-001 | Reuse hosted middleware, host signer and AD client/acceptor seams; issuance/refusal is a separately persisted domain decision. No new peer listener, issuer retry queue, implicit key export or public fallback. |
| P015-003 | Prove two-node issue/renew/reject recovery | todo | P015-002 | Retain real private carrier evidence for initial issuance, renewal, private reset and refusal, duplicate request/reply, restart, lost reply, stale authority, wrong issuer/recipient and expiry. No second issuance or participant/predecessor leakage in public surfaces; delivery never displays as certificate approval. |

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
