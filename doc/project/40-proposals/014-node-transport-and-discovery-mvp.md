# Node Transport and Discovery MVP

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/30-stories/story-001.md`
- `doc/project/60-solutions/node.md`

## Status

Proposed (Draft)

## Date

2026-03-23

## Executive Summary

This proposal defines the smallest practical networking seed on which the first
useful Orbiplex Node can be built.

The key decisions are:

1. MVP networking addresses **nodes**, not user nyms.
2. A Node needs a stable local **node identity** before it can participate in the
   network.
3. Discovery should map **`node-id -> current signed endpoint advertisement`**, not
   `nym -> IP:port`.
4. The default transport should be **WSS over TCP 443**, with seed peers or a seed
   directory for bootstrap.
5. Direct TCP and UDP/NAT traversal are later optimizations, not day-one
   dependencies.
6. The first end-to-end protocol slice should be:
   - identity load/generation,
   - handshake,
   - capability advertisement,
   - keepalive,
   - and one simple signed application message.
7. The first useful signed application message should be **`signal-marker`**.
8. The first seed directory should support both advertisement fetch and
   advertisement publication.
9. MVP capability advertisement should expose only the **narrow core**, not
   attached roles or plugin-process surfaces as required semantics.
10. MVP capability IDs should be **schematic**, with at least one required core
    placeholder:
    - `core/messaging`

## Context and Problem Statement

Orbiplex already has richer protocol ideas:

- question envelopes,
- answer rooms,
- procurement,
- Whisper,
- archival handoff,
- and attached roles.

What is still missing for practical Node implementation is a minimal networking
baseline that says:

- how a node identifies itself,
- how another node finds it,
- how a session is established,
- what the first shared message shape looks like,
- and what can be postponed without blocking the first working Node.

Without that seed, Node implementation stays trapped in architecture talk.

## Goals

- Define the smallest credible Node networking baseline.
- Separate node identity from user or contextual nyms.
- Keep discovery simple enough for the first implementation.
- Make transport compatible with difficult real-world networks.
- Provide a practical implementation seed that can be mapped into the Node repo.

## Non-Goals

- This proposal does not define full user identity, root identity, or PoP.
- This proposal does not define a global public nym registry.
- This proposal does not require DHT, libp2p, or generalized peer-to-peer routing.
- This proposal does not define final room semantics.
- This proposal does not define final federation governance or reputation policy.

## Decision

Orbiplex should adopt the following networking MVP baseline:

1. each Node has a locally generated long-lived keypair,
2. `node-id` is derived from the node public key as a strict `node:did:key` identifier,
3. transport baseline is `WSS/443`,
4. bootstrap uses:
   - static seed peers,
   - or a minimal seed directory,
5. discovery exchanges signed endpoint advertisements,
6. peers establish a signed handshake and exchange capability advertisements,
7. the first always-supported maintenance flow is `ping/pong` and reconnect.

This means that full nym systems, advanced relay graphs, and rich room protocols can
come later without blocking the first useful networked Node.

## Proposed Model

### 1. Minimal node identity

Each Node should have:

- a local long-lived keypair,
- a stable `node-id` derived from the public key,
- and a persisted local identity file.

For Ed25519 in v1, the canonical `node-id` format should be:

- `node:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`

This means:

- the underlying public-key fingerprint uses the `did:key` Ed25519 shape,
- `z...` is the base58btc multibase fingerprint,
- `node:` is the Orbiplex-specific technical identity prefix,
- parsers should be strict,
- and alternative textual forms should not be accepted in v1.

That persisted identity record may, in early implementations, use one of two
secret-bearing shapes:

- inline `private_key_base64`,
- or `key/storage-ref` pointing at a local keystore or secret resolver.

The preferred longer-term direction is `key/storage-ref`, because it keeps the
identity record separate from the secret backend. However, bootstrap-compatible
implementations may begin with inline private key material without violating the
MVP networking seed.

This is enough for:

- peer addressing,
- signing handshake material,
- signing advertisements,
- and replay-resistant session establishment.

This MVP identity is **not** the same thing as:

- user identity,
- root identity,
- `custodian_ref`,
- or a public contextual nym.

Those are higher-layer concerns.

### 2. Discovery baseline

The first discovery target should be:

- `node-id -> current endpoint advertisement`

not:

- `nym -> IP:port`

The healthier MVP is:

- the Node knows one or more seed peers,
- or the Node knows one minimal seed directory endpoint,
- peers publish to and fetch from signed endpoint advertisements,
- advertisements expire through TTL and must be refreshed.

For `node-advertisement.v1`, the signed surface should use a sign-then-attach
pattern:

- sign the whole semantic advertisement payload,
- exclude only the `signature` field itself,
- and exclude only transport-mutable per-hop metadata if a later wire wrapper
  carries such fields outside the semantic payload.

That payload should include at least:

- `advertisement/id`,
- `node/id`,
- `sequence/no`,
- `advertised-at`,
- `expires-at`,
- key material,
- endpoint set,
- and transport support claims.

The signing input for v1 should be:

- `node-advertisement.v1\x00 || deterministic_cbor(payload_without_signature)`

This gives domain separation, deterministic verification, and malleability
resistance. If a later wire framing carries raw advertisement bytes, receivers
should verify those exact bytes rather than re-canonicalizing them.

### 3. Transport baseline

The default transport should be:

- `WSS` over TCP `443`

because it is:

- proxy-friendly,
- firewall-friendly,
- viable in mixed enterprise and consumer networks,
- already aligned with the broader communication proposal corpus.

Later transport layers may add:

- direct TCP,
- UDP hole punching,
- relay optimization,
- or more specialized transports.

But those should not block MVP.

### 4. Session baseline

The first session lifecycle should be:

1. connect to seed or known peer over WSS,
2. send signed `peer-handshake`,
3. receive signed `peer-handshake-ack`,
4. exchange `capability-advertisement`,
5. maintain liveness with `ping/pong`,
6. reconnect and refresh advertisement when needed.

This baseline should use a two-message handshake:

- `hello -> ack`

not:

- `hello -> challenge -> ack`

The `ack` is sufficient as the response-binding step in v1, provided that it
cryptographically binds to the original initiation attempt.

For `peer-handshake.v1`, the signed surface should also use sign-then-attach:

- sign the semantic handshake payload,
- exclude only the `signature` field itself,
- and keep framing-only transport metadata outside the signed payload.

The signed payload should bind at least:

- `handshake/id`,
- `handshake/mode`,
- `sender/node-id`,
- optional `recipient/node-id` when directed,
- `ts`,
- `nonce`,
- `ack/of-handshake-id` when present,
- any offered capability claims,
- and any negotiated terms.

The signing input for v1 should be:

- `peer-handshake.v1\x00 || deterministic_cbor(payload_without_signature)`

For v1 session establishment, the long-lived Node identity remains the
`node:did:key:...` Ed25519 signing identity. The corresponding static X25519
key-agreement public key may be deterministically derived from that identity key
for the DH terms that bind long-lived identity to the session attempt.

This means MVP does not need any additional static X25519 field in
`node-identity.v1` or `node-advertisement.v1`.

`peer-handshake.v1` SHOULD instead carry:

- a fresh per-handshake ephemeral X25519 public key in `session/pub`,
- encoded as raw unpadded base64url for the 32-byte X25519 public key,
- without `did:key`, multicodec prefixes, or identity wrappers.

This keeps the layers distinct:

- identity layer:
  - `node:did:key:...` -> Ed25519 signing identity, with static X25519 derivable for DH,
- session layer:
  - `session/pub` -> fresh ephemeral X25519 public key for the current handshake.

For the Noise-IK-like v1 baseline, the intended session derivation uses:

- `DH1 = X25519(EK_initiator, IK_responder_derived_x25519)`
- `DH2 = X25519(IK_initiator_derived_x25519, EK_responder)`
- `DH3 = X25519(EK_initiator, EK_responder)`

Forward secrecy in v1 relies primarily on fresh ephemeral keys and the `DH3`
term, not on the long-lived identity-derived DH terms alone.

This is accepted as a pragmatic MVP compromise. It does not provide ideal key
separation between signing and key agreement, and may later evolve into a richer
continuity or rotation model.

`ack/of-handshake-id` must be signed, because it cryptographically binds the
response to one concrete initiation attempt. Protocol version belongs in the
interpretation context and domain separator, not in the core semantic payload.
Per-hop transport profile should remain framing metadata unless it is being
asserted as a capability claim.

In v1 the handshake family should stay symmetric at schema level:

- the same `peer-handshake.v1` family covers both `hello` and `ack`,
- `ack/of-handshake-id` is the binding field that turns the second message into
  the acknowledgment of the first,
- and the existing `handshake/mode` field may remain as an explicit discriminator
  for clarity and easier interoperability, even though the semantic asymmetry is
  already visible through `ack/of-handshake-id`.

Replay resistance for the baseline handshake should be defined by:

- a clock-skew window of `+-30s`,
- a per-peer nonce cache with retention of roughly `120s`,
- and a local pending-handshake timeout of `30s` for outstanding `hello`
  attempts.

This baseline is aligned with a Noise-IK-style two-message authenticated
exchange, but the current MVP still treats transport framing and later session
crypto details as separable from the semantic handshake contract.

The capability advertisement should not try to describe the whole implementation.
It should publish a small set of schematic core capability identifiers, such as:

- required minimum:
  - `core/messaging`
- optional additions:
  - `core/discovery`
  - `core/relay`
  - `core/keepalive`

Capabilities that are already implicit in the successful execution of the
handshake, such as "can sign the handshake" or "is a protocol participant",
should not be modeled as mandatory advertised core capabilities in v1.

### 5. First useful message slice

After handshake and capability exchange, the first application-level slice should be
very small.

The first useful signed message should be:

- one simple signed `signal-marker` message.

The point is that Node can:

- sign it,
- validate it,
- send it,
- receive it,
- and trace it end to end.

Higher-layer publication such as reduced `question-envelope` may follow later, once
the seed transport and session slice is already proven end to end.

At this stage the proposal freezes the **semantic** `signal-marker` decision, not
yet a final publication-envelope schema for that marker. A concrete
`signal-marker-envelope.v1` may first live as a repo-local Node contract and only
later be promoted into canonical `orbidocs` schemas once the publish/receive flow
and signed wire shape have stabilized.

## MVP Seed Checklist

1. Define local Node identity file format.
2. Freeze `node-id` derivation rule as strict `node:did:key`.
3. Define signed endpoint advertisement shape.
4. Define peer handshake shape.
5. Define capability advertisement shape.
6. Define keepalive and reconnect behavior.
7. Define seed peer / seed directory configuration.
8. Implement load-or-generate local identity.
9. Implement WSS bootstrap connection to a seed peer.
10. Implement signed handshake and handshake acknowledgment.
11. Implement capability advertisement exchange.
12. Implement `ping/pong`.
13. Implement `signal-marker` end to end as the first signed application message.
14. Add traces and diagnostics for:
    - identity load,
    - advertisement publish/fetch,
    - handshake success/failure,
    - reconnect.

## Document Seed Needed Next

The next minimal schema set should likely be:

1. `node-identity.v1`
2. `node-advertisement.v1`
3. `peer-handshake.v1`
4. `capability-advertisement.v1`

Optionally later:

5. `peer-status.v1`

## Trade-offs

1. WSS/443 vs custom raw transport:
   - Benefit: works sooner in real networks.
   - Cost: less transport purity and some framing overhead.
2. Seed peers/directory vs global decentralized discovery:
   - Benefit: much lower bootstrap cost.
   - Cost: less ideological purity in the first version.
3. Node identity first vs full nym model first:
   - Benefit: practical implementability.
   - Cost: higher-layer identity remains deferred.
4. Minimal handshake first vs complete protocol family first:
   - Benefit: one working slice sooner.
   - Cost: more protocol surface still pending.

## Remaining Open Questions

1. Should MVP implementation stop at static seed peers first, or also include a minimal read-write seed directory?
2. Should the next implementation stage still accept only inline bootstrap private key material, or should resolver-backed `key/storage-ref` become active runtime behavior?

## Next Actions

1. Add one Node requirement for networking baseline.
2. Add the first schema quartet:
   - `node-identity.v1`
   - `node-advertisement.v1`
   - `peer-handshake.v1`
   - `capability-advertisement.v1`
3. Extend `doc/project/60-solutions/node.md`
   with the networking baseline as a first-class Node capability.
4. Extend the Node implementation ledger with the same baseline capability.
