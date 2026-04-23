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

## Open Questions

1. Should public continuation be the default renewal mode, or should public
   continuation and private reset become two separate contract families?
2. Should Phase 1 certificates always carry `leniency-until`, or should that
   field become optional when no grace semantics are granted?
3. Which later application families, besides Whisper, should inherit the same
   nym-certificate embedding pattern?
