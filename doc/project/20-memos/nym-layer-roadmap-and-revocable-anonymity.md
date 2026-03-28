# Nym Layer Roadmap and Revocable Anonymity

## Status

Memo

## Date

2026-03-28

## Purpose

This memo captures the intended stratification and phased cryptographic roadmap
for `nym` handling in Orbiplex Swarm.

It does not freeze the final anonymity design. It records:

- the hard boundary that keeps `nym` above the networking layer,
- the MVP-compatible transitional mechanism for pseudonymous participation,
- and the later target of stronger revocable-anonymity cryptography.

## Hard Boundary

The networking layer MUST NOT require `nym` resolution.

More concretely:

- transport and session establishment see only `node:did:key:...` and
  `participant:did:key:...`,
- `peer-handshake.v1`, `node-advertisement.v1`, keepalive, and reconnect remain
  ignorant of `nym`,
- `nym` signatures and `nym` certificate validation happen above the encrypted
  node-to-node session,
- a message signed by a `nym` is, from the networking layer's perspective, only
  opaque application payload carried over a valid channel.

This keeps the previously frozen boundary intact:

- infrastructure trust and routing belong to `node-id`,
- participant-scoped authorship belongs to `participant-id`,
- pseudonymity belongs above that boundary.

## Rate Limiting and Backpressure

`nym` should not become a transport-layer identity only because abuse control
needs buckets.

The baseline rule is:

- transport-layer rate limiting and backpressure are **per-node**,
- the sending node is responsible for shaping the behavior of its
  participants and nyms,
- if a remote node emits too much traffic through many nyms, peers degrade the
  **node**, not the hidden participant.

This preserves pseudonymity without leaking higher-layer resolution pressure into
the transport boundary.

## Cryptographic Roadmap

The long-term target is:

- pseudonymous participation through strong revocable-anonymity mechanisms,
- with verifier-local revocation or an equivalent property that lets verifiers
  reject blocked nyms without requiring transport-layer identity resolution.

However, the MVP-compatible path should be described honestly as a phased
roadmap:

- Phase 1 is a simpler council-issued certificate model,
- Phase 2 improves unlinkability operationally,
- Phase 3 moves toward stronger non-revocation or revocable-anonymity proofs.

Phase 1 is therefore **not yet** a full group-signature or verifier-local
revocation design. It is a pragmatic stepping stone.

## Phase 1: Council-Issued Nym Certificates

### Goal

Provide a working pseudonym layer with:

- application-level pseudonymous signatures,
- council-side custody of `nym -> participant` binding,
- renewable pseudonym lines,
- and no new heavy cryptographic dependency beyond Ed25519 and signed
  certificates.

### Shape

The first operational model may use:

1. participant-generated fresh Ed25519 keypair for each new `nym`,
2. a participant-signed issuance request sent to the council over an encrypted
   channel,
3. a council-signed `nym` certificate with:
   - `nym`,
   - `epoch`,
   - `issued-at`,
   - `expires-at`,
   - optional `leniency-until`,
   - issuer id,
   - optional predecessor line metadata,
4. council-local encrypted storage of the hidden `nym -> participant` binding,
5. application messages signed by the `nym` key and accompanied by the council
   certificate.

### Verification

Receivers should verify:

1. council signature over the `nym` certificate,
2. certificate freshness or grace semantics,
3. application-message signature against the `nym` key.

No participant identity is revealed to the verifier.

### Revocation Semantics

In this phase, revocation is primarily operational:

- the council refuses renewal for blocked participants,
- old nyms expire naturally,
- observers see expiry or non-renewal, not the private cause.

This is privacy-preserving enough for an MVP path, but it is not the same as
strong verifier-local revocation.

## Phase 2: Epoch Rotation and Better Unlinkability

### Goal

Reduce correlation around renewal and blocking without changing the basic signing
primitive used by application messages.

### Main Changes

- synchronized renewal epochs,
- batch council processing of renewal requests,
- staggered publication of renewed nyms,
- support for two renewal modes:
  - public continuation with explicit predecessor link and reputational carry-over,
  - private reset with fresh pseudonymous start and no public predecessor link.

This phase improves unlinkability and operational privacy but still relies on the
council as issuer and renewal gatekeeper.

## Phase 3: Stronger Non-Revocation Proofs

### Goal

Move toward the real long-term target:

- revocable anonymity with stronger verifier-local rejection properties,
- without forcing normal message verification to contact the council.

### Direction

Later phases may replace council-issued per-nym certificates with:

- revocation accumulators,
- non-revocation proofs,
- or group-signature-style constructions with revocable anonymity.

At that point:

- the council shifts from direct issuer to revocation authority,
- verifiers can reject blocked nyms locally,
- unlinkability improves materially,
- and the application-message signing surface can remain stable even while the
  renewal or attestation layer changes underneath.

## Stable Invariant Across Phases

Across all phases, the architectural invariant should remain:

- `nym` is an application-layer pseudonym,
- transport does not route on `nym`,
- session establishment does not authenticate `nym`,
- and stronger anonymity machinery upgrades the pseudonym layer without
  contaminating the networking boundary.

## Promote To

Phase 1 contract seeding has now been promoted into:

- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`

Further promotion should happen when:

- renewal mode split between public continuation and private reset is frozen more
  sharply,
- the first reusable nym-authored application envelope is frozen,
- or stronger revocable-anonymity cryptography replaces the certificate path.
