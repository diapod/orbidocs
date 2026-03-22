# Requirements 003: Remote Memory Preservation via Memory Nodes

Based on: `doc/project/30-stories/story-003.md`  
Date: `2026-02-22`  
Status: Draft (MVP scope)

## Executive Summary

This document defines MVP requirements for preserving knowledge artifacts beyond a node runtime lifetime by using remote memory nodes in a federated network.

The requirements prioritize:
- explicit storage offer/selection contracts,
- privacy-aware storage flows (`public` vs `private`),
- verifiable storage confirmation and retrieval validation,
- durable provenance for later retrieval and settlement.

## Context and Problem Statement

A node may need durable memory that outlives its own process, host, or lifecycle. In a federated environment, this requires:
- discovery of storage providers,
- negotiation of retention and pricing terms,
- secure transfer and confirmation of stored artifacts,
- reliable retrieval paths over time.

The key challenge is to make this operationally simple while preserving privacy, auditability, and interoperability.

## Proposed Model / Decision

### Actors and Boundaries

- `Node A` (requesting node): requests remote storage and retrieves stored knowledge later.
- `Node B` (memory provider): offers storage capacity and retention terms, stores and serves memory objects.
- `Arbiter` (optional): validates contractual behavior when payment/settlement requires it.
- `Local Orchestrator`: manages offer selection, transfer, tracking identifiers, and retrieval workflows.

### Core Data Contracts (normative)

- `StorageRequest`:
  - `request_id`, `required_capacity`, `subject`, `visibility_mode` (`public|private`), optional `preferred_retention`.
- `StorageOffer`:
  - `offer_id`, `node_id`, `price`, optional `max_storage_duration`, optional `max_idle_ttl`, `privacy_terms`.
- `MemoryObject`:
  - `metadata`, `payload_base64`, optional `encryption_metadata`, `content_hash`.
- `StorageConfirmation`:
  - `knowledge_ids`, `provider_node_id`, `stored_at`, optional `expires_at`, `validation_mode`.
- `RetrievalRequest`:
  - `knowledge_id`, `requester_node_id`, optional `proof_context`.
- `RetrievalResponse`:
  - `knowledge_id`, `metadata`, `payload_base64`, optional `integrity_proof`.

### Concrete Scenario (MVP happy path)

1. Node A publishes a `StorageRequest` in a thematic channel.
2. Multiple nodes return `StorageOffer` objects.
3. Node A selects Node B and moves to a private execution channel.
4. Node A transfers `MemoryObject`; Node B stores it and returns `StorageConfirmation`.
5. Node A records identifiers and later retrieves the artifact directly (or via distributed/public channel when applicable).

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST allow Node A to initiate remote memory preservation for artifacts that should outlive local runtime. | Fact | Story step 1 |
| FR-002 | The system MUST support joining thematic discovery channels to advertise storage requests. | Fact | Story step 2 |
| FR-003 | Storage requests MUST include required capacity, short subject description, and visibility mode (`public` or `private`). | Fact | Story step 3 |
| FR-004 | The system MUST ingest multiple storage offers from peer nodes. | Fact | Story step 4 |
| FR-005 | Offers MAY include paid terms and MUST support private-storage constraints for non-public artifacts. | Fact | Story step 4 |
| FR-006 | Offers SHOULD support optional retention constraints: maximum storage duration and maximum idle TTL. | Fact | Story step 5 |
| FR-007 | Node A MUST be able to select one offer for execution. | Fact | Story step 6 |
| FR-008 | Execution between Node A and Node B MUST occur in a private channel. | Fact | Story step 7 |
| FR-009 | If payment applies, arbitration flow MUST be compatible with `story-001.md` settlement behavior. | Fact | Story step 8 |
| FR-010 | Memory transfer MUST support JSON with metadata plus Base64 payload. | Fact | Story step 9 |
| FR-011 | Node B MUST confirm successful storage and provide validation retrieval access for Node A and arbiters when present. | Fact | Story step 10 |
| FR-012 | Node A MUST persist returned knowledge identifier(s) and provider node identifier for later access. | Fact | Story step 11 |
| FR-013 | Retrieval MUST support direct Node A -> Node B requests and public/distributed retrieval path when memory is distributed/public. | Fact | Story step 12 |
| FR-014 | For private memory, retrieval access MUST be restricted to authorized parties according to privacy terms. | Inference | Story steps 3-4, 12 |
| FR-015 | The system MUST retain provenance linking request, offer, stored artifact, and retrieval events. | Inference | Story steps 9-12 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Storage and retrieval contracts MUST be explicit and versioned for interoperability across heterogeneous nodes. | Inference | Core intent: interoperability |
| NFR-002 | Private memory flow MUST prevent unauthorized payload disclosure in public channels. | Fact | Story steps 3-4, 7 |
| NFR-003 | Stored artifact integrity SHOULD be verifiable via stable content hash and retrieval validation flow. | Inference | Story steps 9-10 |
| NFR-004 | Retrieval metadata MUST be auditable (who stored, where, when, and under which terms). | Inference | Story steps 10-11 |
| NFR-005 | Offer selection SHOULD be deterministic for identical offer sets under identical policy configuration. | Inference | Story step 6 |
| NFR-006 | Expiration and idle-TTL behavior SHOULD be policy-driven and explicit to avoid silent data loss. | Inference | Story step 5 |
| NFR-007 | The system SHOULD degrade gracefully if selected storage provider becomes unreachable (clear error + alternative retrieval path where possible). | Inference | Story step 12 |

## Trade-offs

1. Durability vs cost:
   - longer retention and replication improve availability,
   - but increase storage and settlement cost.
2. Privacy vs operability:
   - stronger privacy controls protect sensitive memory,
   - but can reduce retrieval flexibility in federated channels.
3. Simple payload format vs efficiency:
   - JSON + Base64 improves interoperability and debugging,
   - but adds payload overhead versus binary-native transport.
4. Single-provider simplicity vs resilience:
   - one provider is easier to coordinate,
   - but raises availability risk if provider disappears.
5. Flexible retention terms vs predictability:
   - customizable TTL and duration fit diverse use cases,
   - but increase policy and user-comprehension complexity.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Provider confirms storage but cannot later retrieve | Data durability failure | Require validation retrieval after confirmation and periodic health checks for high-value artifacts. |
| Private memory leaked through misrouted channel | Confidentiality breach | Enforce channel-type checks and private-mode policy gating before payload transmission. |
| Missing/invalid knowledge identifiers | Artifact cannot be located | Make confirmation schema mandatory and reject incomplete confirmations. |
| Offer omits retention constraints | Unexpected expiration semantics | Apply explicit defaults and surface them before offer acceptance. |
| Provider disappears after selection | Retrieval outage | Support fallback request path and optional multi-provider replication policy. |
| Payload corruption at rest or in transit | Incorrect retrieval content | Require content hash verification on store and retrieval operations. |
| Arbitration mismatch with payment flow | Settlement disputes | Reuse `story-001` contract criteria and receipt model for paid storage interactions. |

## Open Questions

1. Should high-value memory support mandatory multi-provider replication in MVP, or only optional replication?
2. What is the canonical integrity proof format (simple hash, signed hash, or merkle-based proof)?
3. Should idle TTL refresh on any retrieval, or only on successful paid retrieval?
4. For private memory, what key-management model is primary (provider-sees-ciphertext only vs shared decryption roles)?
5. What retrieval timeout and retry policy should be standard before failover behavior triggers?
6. Should public/distributed retrieval require provenance score thresholds before accepting returned content?

## Next Actions

1. Define v1 schemas for `StorageRequest`, `StorageOffer`, `MemoryObject`, `StorageConfirmation`, `RetrievalRequest`, and `RetrievalResponse`.
2. Define selection policy for storage offers (cost, retention, privacy terms, reliability, and deterministic tie-break rules).
3. Define private-memory key and access policy, including retrieval authorization checks.
4. Define retention semantics (`max_storage_duration`, `max_idle_ttl`) and default values when omitted.
5. Implement end-to-end test: request -> offers -> private transfer -> confirmation -> validation retrieval -> later retrieval.
6. Add integrity verification tests for content hash roundtrip and corrupted payload detection.
7. Add outage scenarios for provider unavailability and validate fallback behavior.
