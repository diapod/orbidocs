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

## Future Note: Seed Directory and Contextual Participant Nyms

Seed Directory publication should not require publishing the participant's root
`participant:did:key`. A later design should prefer context-specific participant
nyms:

- the root participant key remains local or selectively disclosed;
- Seed Directory receives a public nym key and only the metadata needed for
  discovery, capability lookup, or reputation lookup;
- reputation attaches to the nym line by default, not directly to the root
  participant id;
- continuity from one nym to another is proved by a separate binding or
  succession proof, disclosed only when the workflow needs reputation carry-over;
- rotation, revocation, and private reset remain possible without burning the
  root participant identity.

The design space should be informed by several adjacent systems, not copied from
one of them:

- private messaging systems such as Signal, which minimize server-visible social
  graph disclosure and separate long-term identity from session and sender
  metadata;
- shielded cryptocurrency systems such as Zcash, which separate spending
  authority, diversified receiving identities, and selective viewing/disclosure
  keys;
- selective-disclosure credential systems such as Idemix / Hyperledger
  AnonCreds, which let holders prove scoped claims without revealing the whole
  credential or a globally linkable identity.

The intended Orbiplex shape is a hybrid:

- `participant root` is the private continuity anchor;
- `participant nym` is the public or semi-public contextual identity;
- `nym binding proof` is private by default and presented only under an explicit
  disclosure mode;
- `reputation subject` is normally the nym, with optional proof of continuity
  across rotations.

Open questions for a future proposal:

- whether nym keys are deterministically derived, randomly generated and
  root-authorized, or produced by a hardened derivation scheme;
- how to prevent cross-context correlation when the same participant uses many
  nyms;
- how a participant proves reputation continuity after rotation without
  publishing the root identity;
- which proof format is acceptable for MVP before stronger selective-disclosure
  cryptography is available.

## Future Note: Nym Classes and Accountability Gradient

Orbiplex should not define one universal pseudonymity mode. The pseudonymity
class should be selected by action scope, blast radius, and consent boundary.

Two future classes are useful to name early:

- `accountable-nym` is for public or reputation-bearing actions: federation,
  marketplace participation, governance, public publishing, moderation, and
  public service operation. The public nym is the ordinary reputation subject.
  The root participant identity remains hidden by default, but the nym may carry
  a conditional accountability hook.
- `private-nym` is for private communication, clans, groups, communities, or
  organizations where participation is voluntary and scoped. It should not
  require routine root traceability. In some contexts it may be fully
  unlinkable, with reputation handled locally, probabilistically, or through
  heavier group mechanisms.

For `accountable-nym`, ordinary sanctions should normally apply to the nym line:
reputation loss, renewal refusal, service denial, rate limits, or federation
blocking. Unsealing the hidden root should be exceptional. If supported, it
should require a separate sealed process: for example a threshold council of
high-reputation identities, explicit due process, narrow purpose limitation, and
auditable disclosure.

For `private-nym`, the system should prefer unlinkability over global
accountability. Local mechanisms may include group-scoped reputation,
membership rules, invite graphs, local attestations, rate limits, proof of
membership, or deposits/bonds where appropriate. These mechanisms should not
quietly turn a private nym into a globally linkable identity.

A private group may still need stronger local exclusion than "remove this one
nym". In particular, a group may need to reject the current nym and all future
nyms produced by the same hidden root identity, without learning that root
identity and without creating a global cross-group correlation handle.

This requires a separate mechanism. Candidate directions include:

- a group-scoped nullifier or exclusion tag, stable only inside that group, so a
  new nym can prove it is not derived from a locally removed hidden subject;
- a group issuer or membership authority that refuses future group-local
  credentials for the removed subject while keeping the root identity sealed;
- an anonymous-credential or accumulator-based proof where the joining nym proves
  membership and non-revocation against the group's local revocation set;
- a sealed adjudication path where a threshold group/council authority can map a
  reported nym to a group-local exclusion handle, but not disclose or publish the
  root identity.

The invariant is that private-group exclusion should be scoped. Removing a
subject from one private group must not automatically create a public global ban
or a reusable identifier that lets unrelated groups correlate that subject's
future nyms. If a broader sanction is needed, that is a different escalation path
and belongs to the `accountable-nym` or sealed-council layer.

The design invariant is:

```text
The stronger the public blast radius, the stronger the accountability hook.
The more consent-bound and private the context, the stronger the unlinkability default.
```

A later contract may make this explicit with fields such as:

```yaml
nym/class: accountable | private
nym/scope: public | federation | marketplace | governance | group | org | dm
unseal/policy: none | sealed-council | org-admin | group-policy
reputation/surface: public | domain | group-local | hidden | none
succession/mode: public-continuity | private-reset | group-local-continuity
exclusion/scope: none | group-local | org-local | domain | public
exclusion/proof: none | group-nullifier | issuer-refusal | non-revocation-proof | sealed-handle
```

Open questions for that later contract:

- what threshold and composition should be required for unsealing an
  `accountable-nym`;
- which reputation surfaces are public, domain-local, group-local, or hidden;
- whether a `private-nym` can carry portable reputation without weakening
  unlinkability;
- how to implement future-nym exclusion for a removed private-group subject
  without revealing root identity or creating a global correlation handle;
- how organization or group policy interacts with broader network
  accountability.

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
