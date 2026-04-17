# Proposal 043: Node Address Attestation Fallback

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`

## Status

Draft

## Date

2026-04-17

## Executive Summary

Seed Directory remains the trusted primary source for resolving
`node-id -> current reachable endpoint`. It is operated by trusted
network or organization operators and is the normal authority a node
uses before dialing an unknown or stale peer.

There is still one useful fallback case: Seed Directory is temporarily
unreachable, but the node can still ask already trusted peers whether
they have recent address evidence for another node. This proposal
defines a narrow artefact for that case:

- `node-address-attestation.v1`

The artefact is not a replacement for Seed Directory. It is a
content-addressed evidence packet that can travel over INAC (proposal
042) when a node asks friends for the last known signed advertisement
or reachability evidence for a target node.

`node-address-attestation.v1` belongs to the broader Orbiplex
signed-credential/passport family, but it is intentionally not encoded
as `capability-passport.v1`: capability passports grant authority,
while address attestations carry freshness-bound evidence about
observed reachability.

The core distinction:

- Seed Directory answers: "this is the current trusted directory view",
- `node-address-attestation.v1` answers: "this is address evidence I
  can show you, with signatures and freshness bounds",
- the receiver still makes a local dial decision under its own policy.

## Context and Problem Statement

Proposal 014 defines the baseline node discovery model around signed
advertisements. Proposal 025 gives the federation a trusted catalog
surface for those advertisements. Proposal 042 defines INAC as a direct
node-to-node artefact channel.

The gap is a degraded discovery mode:

1. Node A wants to reach Node C.
2. Seed Directory is unavailable, stale, or partitioned from Node A.
3. Node A still has live peer sessions with trusted peers B1, B2, ...
4. A asks those peers for address evidence for C.
5. A receives signed evidence and decides whether to attempt a bounded
   dial.

Without a dedicated artefact, this fallback becomes an informal gossip
surface. Informal address gossip is dangerous because it can turn the
network into a reflected traffic generator: an attacker can mint many
node ids whose alleged endpoint is the same victim address, causing
honest nodes to "verify" the victim into the ground.

This proposal keeps the fallback useful but non-magical: evidence may
cross the network, but dialing remains a local, rate-limited decision.

## Goals

- Define `node-address-attestation.v1` as a portable fallback evidence
  artefact.
- Preserve Seed Directory as the trusted primary authority.
- Allow trusted peers to share last-known address evidence when Seed
  Directory is unavailable.
- Prevent self-signed address floods from causing outbound probe
  amplification.
- Keep address evidence distinct from capability authorization.

## Non-Goals

- This proposal does not replace Seed Directory.
- This proposal does not define DHT, DNS, mDNS, NAT traversal, or
  hole-punching.
- This proposal does not make third-party peers authoritative for node
  identity.
- This proposal does not guarantee future reachability. It carries signed
  evidence about a past observation or directory validation that a receiver
  may evaluate before dialing.
- This proposal does not define a public address gossip network.

## Decision

### 1. Artefact Purpose

`node-address-attestation.v1` is a signed evidence packet for a single
target node address claim.

It may carry:

- the target node's own signed `node-advertisement.v1`,
- a Seed Directory countersignature when available,
- a Seed Directory reachability transcript hash when the directory actively
  probed the endpoint before issuing the attestation,
- one or more peer reachability attestations from nodes that have
  successfully connected to the target endpoint,
- freshness and expiry bounds for each attestation.

The artefact does not itself authorize dialing. Dialing is a local
policy decision by the receiver.

### 2. Required Shape

The schema should include at least:

- `schema`: constant `"node-address-attestation.v1"`,
- `attestation/id`: stable packet identifier with the
  `attestation:node-address:` prefix,
- `target/node-id`,
- `endpoint`: normalized endpoint descriptor (`scheme`, `host`, `port`,
  `path`),
- `claim/digest`: `sha256:<base64url-no-pad>` over canonical JSON
  containing only `target/node-id` and the normalized `endpoint`,
- `node-advertisement`: either the full `node-advertisement.v1` or a
  content-addressed reference to it,
- `advertisement/digest`,
- `observed/at`,
- `expires/at`,
- `evidence`: array of signed evidence entries,
- `signature`: optional envelope-level signature by the node that
  assembled the packet.

Each evidence entry should include:

- `kind`: `self-advertisement`, `seed-directory`, or
  `peer-reachability`,
- `signer/id`: node id or Seed Directory operator id,
- `signed/at`,
- `expires/at`,
- `claim/digest`: digest of the normalized address claim being signed,
- `signature`: Ed25519 signature over that claim digest and evidence
  metadata,
- required `session/transcript-hash` for `peer-reachability`, binding
  the witness to an actual successful peer session rather than to a
  naked TCP connect,
- optional `session/transcript-hash` for `seed-directory` evidence. When
  present, the evidence class is `directory-confirmed`; when absent, the
  evidence class is only `directory-accepted`.

The transcript hash must not contain plaintext transcript material.

### 3. Trust Semantics

Seed Directory evidence is primary, but it has two classes:

- `directory-confirmed`: the directory signed the claim after a successful
  `peer-handshake.v1` probe carrying `probe/challenge` and
  `probe/purpose = "seed-directory-address-verification"`;
- `directory-accepted`: the directory accepted and signed the target
  `node-advertisement.v1`, but no active probe transcript is attached.

When a valid `directory-confirmed` Seed Directory signature is present and
fresh, the receiver may treat the artefact as equivalent to a cached Seed
Directory response, subject to local expiry and dial budget.

`directory-accepted` is still more trustworthy than self-only evidence because
the directory verified the signed advertisement and applied its local policy,
but it is not a proof that the advertised endpoint answered a live handshake.

Peer evidence is fallback. It can upgrade a stale or unavailable
directory view, but only inside local policy. A cautious operator may
require:

- Seed Directory signature, or
- at least one trusted peer reachability signature, or
- `k` independent trusted peer signatures before dialing.

Self-advertisement alone proves only that a key holder signed an
endpoint claim. It does not prove the endpoint is safe to probe.

### 4. Anti-Reflection Rules

The core threat is reflected or amplification DDoS. An attacker can
mint many node ids, self-sign claims that all point to one victim
`address:port`, and hope honest nodes will probe those addresses.

The protocol therefore freezes these rules:

1. **Self-only evidence MUST NOT trigger eager outbound probing.**
   A receiver MAY cache or quarantine the packet, but MUST NOT dial it
   automatically.
2. **Self-only probe budgets are global and tiny.** If an operator
   enables exploratory probing, the budget is shared across all
   self-only claims, not per claimed node id.
3. **Address collision is a flood signal.** When multiple distinct
   `node-id`s claim the same endpoint, the receiver MUST quarantine
   the collision group until corroborated by Seed Directory or trusted
   peer evidence.
4. **Peer reachability evidence is not verification-on-demand.** A peer
   signs only endpoints it reached for its own reason, not because a
   third party asked it to probe.
5. **Seed Directory signatures are not echoes.** Seed Directory signs
   only after its own validation under its own rate limits.

These rules make self-signed floods create at most storage pressure,
not outbound probe amplification.

### 5. INAC Integration

INAC may carry this artefact as a registered kind:

- `artifact/schema = "node-address-attestation.v1"`,
- `reason = "address-fallback"`,
- usual INAC `offer`, `request`, and `push` operations apply.

Recommended flow:

1. Node A cannot resolve Node C through Seed Directory.
2. Node A sends an INAC `request` to already trusted peer B:
   `filter = { artifact/schema, target/node-id }`.
3. B returns `decline` if it has no evidence, or `push` with
   `node-address-attestation.v1`.
4. A validates signatures, freshness, collision state, and local policy.
5. A may attempt a bounded dial or keep the evidence quarantined.

The INAC channel does not interpret the address evidence beyond kind
routing. Verification belongs to the address-attestation consumer.

### 6. Relationship to Seed Directory

Seed Directory remains the normal source of truth. The fallback artefact
exists because temporary directory unavailability should not force a
node to forget everything its trusted neighbours know.

When Seed Directory is available again, the node should reconcile:

- discard expired fallback evidence,
- prefer fresh Seed Directory entries over peer-only evidence,
- preserve peer evidence as local diagnostic context if it explains
  why a fallback dial was attempted,
- never publish peer-only evidence back into Seed Directory as if it
  were directory-verified.

### 7. Local Policy Classes

Receivers should classify evidence before dialing:

| Class | Minimum evidence | Default action |
|---|---|---|
| `directory-confirmed` | fresh Seed Directory signature with reachability transcript hash | may dial under normal peer budget |
| `directory-accepted` | fresh Seed Directory signature over accepted advertisement, no transcript hash | may dial under cautious/normal policy; receiver MAY perform its own bounded probe |
| `trusted-peer-confirmed` | one or more trusted peer reachability signatures | may dial under degraded/fallback budget |
| `self-only` | target self-advertisement only | cache/quarantine; no eager dial |
| `collision` | multiple node ids claim the same endpoint | quarantine until directory or trusted corroboration |
| `expired` | all evidence expired | refuse or keep only for audit |

Operators may make the fallback stricter. They should not make
self-only evidence equivalent to directory-confirmed evidence.

## Consequences

Positive:

- gives INAC a safe address-discovery fallback use case without
  turning INAC into discovery infrastructure,
- lets friends help one another reconnect during Seed Directory
  outage,
- keeps Seed Directory as the primary authority,
- makes anti-reflection rules explicit before implementation,
- gives operators a forensic artefact explaining why a degraded dial
  was attempted.

Negative / watch items:

- adds one more signed artefact family to maintain,
- requires careful canonicalization and endpoint normalization,
- can create storage pressure if self-only evidence is not bounded,
- needs UI/operator wording that distinguishes "evidence" from
  "trusted current directory state".

## Follow-Up / Next Actions

1. Implement runtime validation and local policy classification for
   `node-address-attestation.v1`.
2. Add a refusal/reason vocabulary for address fallback:
   `address-evidence-expired`, `address-evidence-self-only`,
   `address-collision-quarantine`, `address-evidence-untrusted`,
   `address-fallback-budget-exhausted`.
3. Extend proposal 025 with the reconciliation rule: Seed Directory
   view wins over peer-only fallback evidence.
4. Extend proposal 014 with degraded address resolution semantics and
   probe-budget constraints.
5. Add INAC kind registration notes once proposal 042 is promoted to
   requirements.
