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
- node identity before user identity,
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
  - `node/id`, `created-at`, `key/alg`, `key/public`, and either `private_key_base64` or `key/storage-ref`, optional `identity/status`.
- `NodeAdvertisement`:
  - `advertisement/id`, `node/id`, `advertised-at`, `expires-at`, `key/alg`, `key/public`, `endpoints`, `transports/supported`, `signature`.
- `PeerHandshake`:
  - `handshake/id`, `handshake/mode`, `ts`, `sender/node-id`, `key/alg`, `key/public`, `protocol/version`, `transport/profile`, `nonce`, optional `ack/of-handshake-id`, `signature`.
- `CapabilityAdvertisement`:
  - `advertisement/id`, `node/id`, `published-at`, `protocol/version`, `transport/profiles`, `capabilities/core`, optional `roles/attached`, optional `surfaces/exposed`, `messages/supported`, `signature`.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | Every network-participating Node MUST have a stable locally persisted identity with a long-lived keypair. | Fact | Proposal 014 |
| FR-001a | The persisted `NodeIdentity` record MUST expose public identity material and MUST include either inline bootstrap private key material (`private_key_base64`) or a resolver-friendly private key reference (`key/storage-ref`). | Fact | Proposal 014 |
| FR-002 | `node-id` MUST be derived from the Node public key and MUST be stable across restarts until explicit rotation occurs. | Inference | Proposal 014 |
| FR-003 | The baseline network identity of a Node MUST be distinct from any user, pod-user, or contextual nym identity. | Inference | Proposal 014 |
| FR-004 | A Node MUST support signed endpoint advertisements with TTL-bounded freshness. | Fact | Proposal 014 |
| FR-005 | Endpoint discovery for MVP MUST target `node-id -> current endpoint advertisement`, not `nym -> IP:port`. | Fact | Proposal 014 |
| FR-006 | Every Node MUST support bootstrap from one or more statically configured seed peers. | Fact | Proposal 014 |
| FR-007 | A Node MAY support a minimal seed directory in addition to static seed peers. If present, the first seed directory SHOULD support both advertisement fetch and advertisement publication. | Fact | Proposal 014 |
| FR-008 | The MVP baseline transport MUST support `WSS` over TCP `443`. | Fact | Proposal 014 |
| FR-009 | Direct TCP, UDP traversal, and richer relay topologies MAY be added later but MUST NOT be prerequisites for the first interoperable Node. | Inference | Proposal 014 |
| FR-010 | A Node MUST support a signed peer handshake before application-level message exchange begins. | Fact | Proposal 014 |
| FR-011 | The handshake MUST include enough information to validate peer identity, protocol version, and transport profile. | Inference | Proposed model |
| FR-012 | The handshake flow MUST support an acknowledgment step that binds the remote peer to the same session attempt. | Inference | Session integrity |
| FR-013 | After handshake, a Node MUST support capability advertisement exchange. | Fact | Proposal 014 |
| FR-014 | Capability advertisement MUST include at least transport profiles and narrow core protocol capabilities. Attached roles and plugin-process surfaces MUST remain optional in MVP. | Inference | Proposal 014 |
| FR-014a | `capabilities/core` MUST be interpreted as a schematic set of capability identifiers, not a free-form implementation description. | Inference | Proposal 014 |
| FR-014b | Every MVP Node MUST advertise `core/node-participant` as the minimal placeholder proving baseline participation in the Node protocol. | Fact | Proposal 014 |
| FR-015 | A Node MUST support liveness maintenance through `ping/pong` or an equivalent keepalive flow. | Fact | Proposal 014 |
| FR-016 | A Node MUST support reconnect behavior after transient peer or transport failure. | Fact | Proposal 014 |
| FR-017 | The first supported application-level slice MUST include `signal-marker` as a signed application message that can be sent, validated, and traced end to end. | Fact | Proposal 014 |
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

## Remaining Open Question

1. How much handshake metadata should be included in the signed surface in v1?

## Next Actions

1. Keep `NodeIdentity`, `NodeAdvertisement`, `PeerHandshake`, and `CapabilityAdvertisement` aligned as one versioned networking family.
2. Extend `/Users/siefca/kody/FREE/AI/orbiplex/orbidocs/doc/project/60-solutions/node.md` and `node-caps.edn` to point directly at the first networking schema quartet.
3. Add matching implementation-ledger rows in `/Users/siefca/kody/FREE/AI/orbiplex/node`.
4. Implement load-or-generate local identity, WSS seed bootstrap, signed handshake, capability exchange, and keepalive as the first Node networking slice.
