# Nym Certificates and Renewal Baseline

Based on:
- `doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`
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
- issuer identity,
- optional predecessor and succession proof for public continuity,
- council signature.

Receivers verify:

1. council signature over the certificate,
2. expiry or leniency semantics,
3. application-message signature by the `nym` key itself.

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
- attributable to the issuer,
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
- or stronger revocable-anonymity constructions.

The stable invariant should remain:

- `nym` is an application-layer pseudonym,
- transport does not route on `nym`,
- and upgrading anonymity must not contaminate the networking boundary.

## Candidate Embedding Pattern

Application artifacts that want `nym`-level authorship may later carry:

- authored payload,
- `nym/id`,
- attached or referenced `nym-certificate`,
- and a `nym` signature over the payload.

This proposal does not yet freeze a generic shared envelope for that embedding,
because different application families may want different provenance and replay
semantics.

## Open Questions

1. Should public continuation be the default renewal mode, or should public
   continuation and private reset become two separate contract families?
2. Should Phase 1 certificates always carry `leniency-until`, or should that
   field become optional when no grace semantics are granted?
3. When the first nym-authored application artifact is frozen, do we want a
   reusable envelope or artifact-local embedding?
