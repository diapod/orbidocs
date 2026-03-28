# Requirements 006: Node Networking Baseline MVP

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-23`
Status: Draft

## Executive Summary

This document defines the smallest networking baseline required to build the first
useful Orbiplex Node.

The baseline prioritizes:
- node and participant role split before multi-user pod identity,
- signed discovery artifacts before rich federation semantics,
- `WSS/443` as the default transport,
- bootstrap through seed peers or a minimal seed directory,
- `signal-marker` as the first end-to-end signed application message after handshake,
- and a narrow-core capability advertisement for MVP.

## Context and Problem Statement

Orbiplex already has richer protocol ideas for:

- question envelopes,
- answer rooms,
- procurement,
- Whisper,
- archival handoff,
- attached roles and plugins.

Those flows cannot be implemented credibly until Nodes can:

- identify themselves,
- discover peers,
- establish sessions,
- exchange baseline capabilities,
- and maintain liveness over unstable networks.

The networking seed therefore needs its own explicit requirements, separate from
higher-layer identity, room, or federation semantics.

## Proposed Model / Decision

### Actors and Boundaries

- `Node`: a protocol participant with a stable local identity and one or more live endpoints.
- `Seed Peer`: a known bootstrap Node configured locally.
- `Seed Directory`: an optional minimal service that returns current endpoint advertisements and may accept advertisement publication.
- `Remote Peer`: another Node that validates advertisements, handshake material, and capability claims.

### Core Data Contracts (normative)

- `NodeIdentity`:
  - `node/id`, `participant/id`, `created-at`, `key/alg`, `key/public`, required `key/storage-ref`, optional `identity/status`.
- `NodeAdvertisement`:
  - `advertisement/id`, `node/id`, `sequence/no`, `advertised-at`, `expires-at`, `key/alg`, `key/public`, `endpoints`, `transports/supported`, `signature`.
- `PeerHandshake`:
  - `handshake/id`, `handshake/mode`, `ts`, `sender/node-id`, optional `recipient/node-id`, `key/alg`, `key/public`, `session/pub`, optional `protocol/version`, optional `transport/profile`, `nonce`, optional `ack/of-handshake-id`, optional `capabilities/offered`, optional `terms/negotiated`, `signature`.
- `CapabilityAdvertisement`:
  - `advertisement/id`, `node/id`, `published-at`, `protocol/version`, `transport/profiles`, `capabilities/core`, optional `roles/attached`, optional `surfaces/exposed`, `messages/supported`, `signature`.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | Every network-participating Node MUST have a stable locally persisted identity with a long-lived keypair. | Fact | Proposal 014 |
| FR-001a | The persisted `NodeIdentity` record MUST expose public identity material and MUST include a resolver-friendly private key reference (`key/storage-ref`) instead of inline private key material. | Fact | Proposal 014 |
| FR-001b | The MVP baseline MUST support `local-file:` as the first concrete `key/storage-ref` resolver scheme, with the secret record stored locally under the node data directory. | Fact | Freeze note |
| FR-001c | The persisted `NodeIdentity` record MUST also carry a stable `participant-id` role identifier even in the one-operator-per-node MVP baseline. | Fact | Proposal 014 |
| FR-002 | `node-id` MUST be derived from the Node public key and MUST be stable across restarts until explicit rotation occurs. | Inference | Proposal 014 |
| FR-002a | The canonical v1 `node-id` string MUST be `node:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`. Parsers MUST be strict, and alternative textual variants MUST be rejected for v1. | Fact | Freeze note |
| FR-002b | Rotating the Ed25519 node keypair MUST produce a new `node-id`; v1 does not attempt continuity by reusing the old `node-id` across keys. | Fact | Freeze note |
| FR-003 | The baseline protocol semantics MUST distinguish Node infrastructure identity from participant identity, and both MUST remain distinct from later pod-user or contextual nym layers. | Inference | Proposal 014 |
| FR-003a | The canonical v1 `participant-id` string MUST be `participant:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`. Parsers MUST be strict, and alternative textual variants MUST be rejected for v1. | Fact | Freeze note |
| FR-003b | In the MVP baseline, `node-id` and `participant-id` MAY share the same underlying Ed25519 `did:key` fingerprint and signing material, but protocol implementations MUST NOT assume that role equality follows from shared key material. | Fact | Freeze note |
| FR-003c | Networking-layer implementations for the MVP baseline MUST depend only on `node-id`, `participant-id`, and the signing or verification material needed for those roles. They MUST NOT require `anchor-identity`, `pod-user-id`, `nym`, or federation continuity bindings as part of the networking contract. | Inference | Freeze note |
| FR-004 | A Node MUST support signed endpoint advertisements with TTL-bounded freshness. | Fact | Proposal 014 |
| FR-004a | A signed `node-advertisement.v1` payload MUST include both `advertised-at` and a monotonic `sequence/no`. | Fact | Freeze note |
| FR-004b | The signing input for `node-advertisement.v1` MUST be domain-separated as `node-advertisement.v1\\x00 || deterministic_cbor(payload_without_signature)`. | Fact | Freeze note |
| FR-004c | Transport-mutable per-hop metadata MUST NOT be part of the `node-advertisement.v1` signed surface; if such metadata exists later, it MUST live outside the semantic advertisement payload. | Inference | Freeze note |
| FR-004d | Discovery state in v1 MUST treat `node-advertisement.v1` as one current advertisement per `node-id`; a newer `sequence/no` replaces the previous one, while stale or equal sequence numbers MUST be rejected as non-current. | Fact | Freeze note |
| FR-004e | `node-advertisement.v1` MAY carry an optional future-facing `succession` object naming a successor `node-id` and later proof slots, but the MVP runtime MUST treat it only as non-authoritative seed data for a later rotation layer. | Fact | Freeze note |
| FR-005 | Endpoint discovery for MVP MUST target `node-id -> current endpoint advertisement`, not `nym -> IP:port`. | Fact | Proposal 014 |
| FR-006 | Every Node MUST support bootstrap from one or more statically configured seed peers. | Fact | Proposal 014 |
| FR-006a | Static seed-peer configuration MAY carry operator-facing local labels or names in addition to `node-id` and bootstrap address, but such labels MUST remain non-identifying operational metadata outside signed network identity. | Inference | Freeze note |
| FR-007 | A Node MAY support a minimal seed directory in addition to static seed peers, but the MVP implementation baseline does not require a seed directory before static seed bootstrap is working. | Fact | Freeze note |
| FR-007a | If a minimal seed directory is present, it SHOULD support `PUT /adv/{node-id}` for publish-or-update, `GET /adv/{node-id}` for fetch-by-node, and incremental `GET /adv?since={cursor}` batch synchronization. | Fact | Freeze note |
| FR-007b | A minimal seed directory SHOULD remain open for reads, and open for signed writes from any node, while enforcing freshness checks and per-publisher rate limits. | Inference | Freeze note |
| FR-007c | A minimal seed directory MUST NOT require an explicit delete operation for advertisements; expiry and removal SHOULD be driven by advertisement freshness and TTL sweep. | Fact | Freeze note |
| FR-008 | The MVP baseline transport MUST support `WSS` over TCP `443`. | Fact | Proposal 014 |
| FR-008b | In the MVP baseline, `WSS/TLS` MUST be treated as a carrier layer: TLS server authentication protects endpoint reachability and channel confidentiality/integrity, while peer identity authentication still happens through signed `peer-handshake.v1` artifacts rather than client-certificate semantics. | Fact | Freeze note |
| FR-008c | For public `wss://` endpoints, a Node SHOULD validate the presented server certificate against the advertised endpoint hostname using normal WebPKI rules. | Inference | Freeze note |
| FR-008d | Controlled or private deployments MAY configure additional local trust roots out of band, but such trust anchors MUST remain deployment-local and MUST NOT be encoded as protocol semantics or carried inside `node-advertisement.v1` in the MVP baseline. | Fact | Freeze note |
| FR-008a | When multiple endpoints are advertised, a Node SHOULD first filter unsupported transports and then respect sender-advertised endpoint priority among the remaining compatible endpoints, unless stronger local constraints override that hint. | Inference | Freeze note |
| FR-009 | Direct TCP, UDP traversal, and richer relay topologies MAY be added later but MUST NOT be prerequisites for the first interoperable Node. | Inference | Proposal 014 |
| FR-010 | A Node MUST support a signed peer handshake before application-level message exchange begins. | Fact | Proposal 014 |
| FR-010a | The signing input for `peer-handshake.v1` MUST be domain-separated as `peer-handshake.v1\\x00 || deterministic_cbor(payload_without_signature)`. | Fact | Freeze note |
| FR-010b | `ack/of-handshake-id`, when present, MUST be part of the signed handshake payload. | Fact | Freeze note |
| FR-010c | `protocol/version` SHOULD be treated as interpretation context and domain-separation input rather than as mutable handshake business data. | Inference | Freeze note |
| FR-010d | Per-hop `transport/profile` metadata MUST NOT be part of the signed payload unless it is being asserted as a capability claim rather than carried as framing. | Inference | Freeze note |
| FR-010e | `peer-handshake.v1` MUST carry a fresh per-handshake ephemeral X25519 public key in `session/pub`, encoded as raw unpadded base64url for the 32-byte public key, without `did:key` wrapping or multicodec prefixes. | Fact | Freeze note |
| FR-010f | The long-lived static key-agreement contribution for the handshake MAY be deterministically derived from the Ed25519 `node:did:key` identity, so no extra static X25519 advertisement field is required in `node-identity.v1` or `node-advertisement.v1` for MVP. | Inference | Freeze note |
| FR-010g | `peer-handshake.v1` MUST remain node-scoped in the MVP baseline and MUST NOT require `participant-id`; participant authentication belongs to application messages sent over the established encrypted channel rather than to the transport-session handshake itself. | Fact | Freeze note |
| FR-010h | `peer-handshake.v1` MUST NOT require or interpret higher identity-layer concepts such as `anchor-identity`, `pod-user-id`, or `nym`. | Inference | Freeze note |
| FR-011 | The handshake MUST include enough information to validate peer identity, protocol version, and transport profile. | Inference | Proposed model |
| FR-012 | The baseline v1 handshake flow MUST be `hello -> ack`; a third explicit challenge message MUST NOT be required for the first interoperable Node. | Fact | Freeze note |
| FR-012a | The handshake family MUST remain symmetric at schema level: `hello` and `ack` are artifacts of the same `peer-handshake.v1` family, while `ack/of-handshake-id` binds the acknowledgment to one prior initiation attempt. | Inference | Freeze note |
| FR-012b | v1 replay protection MUST include a clock-skew window of `+-30s`, a per-peer nonce retention window of roughly `120s`, and a pending-handshake timeout of `30s` for unanswered local `hello` attempts. | Fact | Freeze note |
| FR-012c | Forward secrecy in the v1 baseline SHOULD rely primarily on fresh ephemeral X25519 keys and the ephemeral-ephemeral DH term, not solely on identity-derived static DH terms. | Inference | Freeze note |
| FR-012d | Local identity records with `identity/status` other than `active` MUST be rejected by the MVP runtime; richer status handling such as `rotating` or `retired` is deferred. | Fact | Freeze note |
| FR-013 | After handshake, a Node MUST support capability advertisement exchange. | Fact | Proposal 014 |
| FR-014 | Capability advertisement MUST include at least transport profiles and narrow core protocol capabilities. Attached roles and plugin-process surfaces MUST remain optional in MVP. | Inference | Proposal 014 |
| FR-014a | `capabilities/core` MUST be interpreted as a schematic set of capability identifiers, not a free-form implementation description. | Inference | Proposal 014 |
| FR-014b | Every MVP Node MUST advertise `core/messaging` as the minimal explicit core capability proving that the established session is usable for post-handshake message exchange. | Fact | Freeze note |
| FR-014c | Capabilities that are already implicit in a successful signed handshake, such as baseline protocol participation or the ability to sign the handshake itself, SHOULD NOT be modeled as separate mandatory advertised core capabilities in v1. | Inference | Freeze note |
| FR-015 | A Node MUST support liveness maintenance through `ping/pong` or an equivalent keepalive flow. | Fact | Proposal 014 |
| FR-016 | A Node MUST support reconnect behavior after transient peer or transport failure. | Fact | Proposal 014 |
| FR-016a | Reconnect after transient transport failure SHOULD establish a fresh carrier connection and repeat the signed `peer-handshake.v1` flow rather than assuming protocol continuity from TLS session resumption alone. | Inference | Freeze note |
| FR-017 | The first supported application-level slice MUST include `signal-marker` as a signed application message that can be sent, validated, and traced end to end. | Fact | Proposal 014 |
| FR-017a | The first application-level slice SHOULD already be modeled as participant-scoped rather than infrastructure-scoped, even when MVP currently uses one operator-participant per Node. | Inference | Freeze note |
| FR-017b | Participant authentication in the MVP baseline SHOULD therefore occur through participant-scoped application artifacts over an already established node-scoped session, not by extending the handshake to enumerate or reveal participant identities. | Inference | Freeze note |
| FR-017c | For application-level message families such as `question-envelope`, `procurement-*`, and `response-envelope`, `node-id` SHOULD remain the routing or hosting identity while `participant-id` remains the authored participation identity. Higher identity layers MAY appear only as optional payload metadata. | Inference | Freeze note |
| FR-018 | Nodes MUST reject or quarantine malformed, expired, or signature-invalid advertisements and handshakes. | Inference | Contract integrity |
| FR-019 | The baseline capability surface SHOULD be small enough that heterogeneous Node implementations can interoperate without sharing one runtime or language stack. | Inference | Architecture principles |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Networking contracts MUST remain implementation-agnostic across Rust, Python, JVM, and other future runtimes. | Inference | Architecture principles |
| NFR-002 | All baseline networking artifacts MUST be versioned and suitable for validation at the edge. | Inference | Contract-first design |
| NFR-003 | The baseline MUST prefer real-world reachability over protocol purity; `WSS/443` is chosen primarily for practical network traversal. | Fact | Proposal 014 |
| NFR-004 | The baseline MUST fail closed on signature mismatch, unsupported protocol version, or expired advertisement freshness. | Inference | Security + interoperability |
| NFR-005 | The Node SHOULD emit traces for identity load, advertisement publish/fetch, handshake success/failure, keepalive, and reconnect. | Inference | Transparency of operation |
| NFR-006 | Discovery and session establishment SHOULD tolerate partial failures without forcing full local identity regeneration. | Inference | Resilience |
| NFR-007 | The baseline MUST avoid introducing a mandatory global public registry or federation-wide trust fabric before the first Node can operate. | Fact | Proposal 014 |
| NFR-008 | The first seed-directory synchronization surface SHOULD prefer incremental cursor-based advertisement fetch over full topology dump to reduce scraping and unnecessary bandwidth. | Inference | Freeze note |

## Trade-offs

1. `WSS/443` vs custom raw transport:
   - Benefit: earlier success in hostile enterprise and consumer networks.
   - Cost: framing overhead and less transport minimalism.
2. Seed peers / seed directory vs generalized decentralized discovery:
   - Benefit: much smaller bootstrap surface.
   - Cost: lower ideological purity and less autonomy on day one.
3. Node identity first vs full user/nym identity first:
   - Benefit: practical implementability.
   - Cost: higher-layer identity semantics stay deferred.
4. Small capability baseline vs rich protocol family:
   - Benefit: faster interoperable seed.
   - Cost: more protocol surface still needs later freezing.
5. Schematic capability IDs vs rich feature descriptions:
   - Benefit: low ambiguity and easy interop across runtimes.
   - Cost: less expressive detail in MVP advertisements.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Node regenerates identity implicitly after restart | Broken addressing and trust discontinuity | Persist identity file and require explicit rotation workflow. |
| Advertisement points to stale endpoint | Failed connection attempts and noisy bootstrap | TTL-bounded advertisements plus refresh and expiry checks. |
| Peer impersonates another node | Identity confusion and possible routing abuse | Require signed advertisements and signed handshake material tied to `node-id`. |
| Unsupported protocol versions connect silently | Undefined session behavior | Fail closed on version mismatch during handshake. |
| Keepalive is missing or too weak | Peers appear alive long after disconnect | Require explicit liveness flow and reconnect behavior. |
| Network seed depends on one runtime-specific artifact | Cross-language interoperability failure | Keep contracts JSON-friendly, signed, and runtime-neutral. |

## Remaining Open Questions

None for the baseline identity storage shape. `key/storage-ref` with a
`local-file:` resolver is now part of the MVP baseline.

## Next Actions

1. Keep `NodeIdentity`, `NodeAdvertisement`, `PeerHandshake`, and `CapabilityAdvertisement` aligned as one versioned networking family.
2. Extend `doc/project/60-solutions/node.md` and `node-caps.edn` to point directly at the first networking schema quartet.
3. Add matching implementation-ledger rows in the sibling `node` repository.
4. Implement load-or-generate local identity, WSS seed bootstrap, signed handshake, capability exchange, and keepalive as the first Node networking slice.
