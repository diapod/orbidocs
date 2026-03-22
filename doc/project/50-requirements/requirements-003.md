# Requirements 003: Remote Memory Preservation, Archivists, and Vault Publication

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

Date: `2026-03-22`
Status: Draft (MVP scope)

## Executive Summary

This document defines MVP requirements for preserving valuable knowledge artifacts
beyond the lifetime of a single node runtime by using explicit archivist and vault
flows instead of an underspecified `memory node` concept.

The requirements prioritize:
- explicit publication scope (`private-retained`, `federation-vault`,
  `public-vault`),
- fail-closed archival export rules,
- provenance-rich storage contracts and confirmations,
- integrity-preserving retrieval,
- clear separation between durable storage, publication, and later training
  eligibility.

## Context and Problem Statement

`story-003.md` no longer models remote memory as a public storage request on a
knowledge-classification channel followed by opaque transfer to a provider.

The current corpus assumes:

- archivists and vaults as explicit roles and preservation targets,
- curator-gated or policy-gated promotion before broader publication,
- transcript bundles and other knowledge artifacts that preserve provenance,
  redaction state, and integrity metadata,
- publication scope that may remain private, federation-bounded, or public,
- storage/procurement terms that may exist but do not force a crypto-native
  settlement model.

The system therefore needs an operational contract for taking a valuable artifact and
making it durably retrievable without flattening policy, provenance, or later
publication semantics.

## Proposed Model / Decision

### Actors and Boundaries

- `Preserving Node`: wants an artifact to outlive its current runtime or host.
- `Secretary / Curator`: verifies whether the artifact is eligible for archival export
  and may redact or quarantine it.
- `Archivist Node`: receives eligible artifacts, stores them durably, and exposes
  retrieval capability within the allowed scope.
- `Vault`: the durable publication surface for accepted retained or published
  artifacts.
- `Local Orchestrator`: prepares archival packages, selects archivists, tracks
  confirmations, and later retrieves material.
- `Settlement / Procurement Layer` (optional): negotiates retention or payment terms
  when storage is not free.

### Preservation States

Artifacts SHOULD move through explicit states such as:

1. `locally-retained`
2. `export-eligible`
3. `curator-accepted` or `quarantined`
4. `archived-private`
5. `archived-federation`
6. `archived-public`

Promotion between these states MUST be explicit and traceable.

### Core Data Contracts (normative)

- `KnowledgeArtifact` or source artifact:
  - accepted summary, transcript bundle, corpus candidate, or another provenance-rich
    knowledge object.
- `TranscriptBundle`:
  - transcript-specific durable source package where relevant.
- `ArchivalPackage` (not yet frozen as schema):
  - artifact id, provenance refs, publication scope, redaction status, integrity
    proof, retention hints.
- `ArchivistAdvertisement` (not yet frozen as schema):
  - willingness to accept bounded classes of artifacts under declared scope and
    retention policy.
- `StorageOffer` / `ProcurementOffer`:
  - optional retention, price, access, and replication terms when archival storage is
    negotiated.
- `StorageConfirmation` / `ProcurementReceipt`:
  - stable retrieval identifiers and accepted storage terms.
- `RetrievalRequest` / `RetrievalResponse` (not yet frozen as schema):
  - later scope-aware retrieval contract.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST support preserving valuable knowledge artifacts beyond the lifetime of the originating runtime instance. | Fact | Story step 1 |
| FR-002 | Before export, the system MUST classify intended preservation scope as `private-retained`, `federation-vault`, or `public-vault`. | Fact | Story step 2 |
| FR-003 | If the artifact originates from a live room, archival export MUST be blocked unless room policy, exposure mode, and consent or policy basis allow it. | Fact | Story step 3 |
| FR-004 | Ambiguous archival basis MUST fail closed to local retention or quarantine. | Fact | Story step 3 |
| FR-005 | The system MUST prepare a durable archival package containing artifact identity, provenance refs, publication scope, redaction status, integrity metadata, and retention hints where relevant. | Fact | Story step 4 |
| FR-006 | The system MUST support curator-gated review where artifacts may be accepted, accepted-redacted, quarantined, or rejected for publication. | Fact | Story step 5 |
| FR-007 | The system MUST support selecting an archivist or vault target according to federation policy and artifact scope. | Fact | Story step 6 |
| FR-008 | The system MAY use explicit storage or procurement terms when retention, replication, or cost constraints require negotiation. | Fact | Story steps 6-7 |
| FR-009 | Negotiated archival terms SHOULD support maximum duration, idle TTL, replication level, and publication timing profile. | Fact | Story step 7 |
| FR-010 | Transfer of private or federation-bounded artifacts MUST occur over an execution path appropriate to the artifact sensitivity and scope. | Fact | Story step 8 |
| FR-011 | The archivist MUST validate integrity metadata and return stable retrieval identifiers and scope metadata on successful storage. | Fact | Story step 9 |
| FR-012 | The preserving node MUST record archival result provenance including archivist identity, publication scope, retention policy, and optional contract or receipt references. | Fact | Story step 10 |
| FR-013 | Retrieval capability MUST respect stored scope: retained, federation-bounded, and public artifacts MUST NOT be treated as equivalent discovery surfaces. | Fact | Story steps 11-12 |
| FR-014 | Promotion from one publication scope to another MUST be an explicit later transition, not an automatic side effect of storage. | Fact | Story step 11 |
| FR-015 | Durable storage MUST NOT by itself imply training eligibility for the stored material. | Fact | Story step 13 |
| FR-016 | Later curation, synthesis, or training layers MUST consume archived material through provenance-carrying contracts rather than opaque blob fetches. | Fact | Story step 13 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Archival and retrieval contracts MUST be explicit and versionable for interoperable federated implementations. | Inference | Interoperability |
| NFR-002 | The system MUST preserve provenance, redaction state, and integrity semantics across archival export and retrieval. | Inference | Story steps 4, 9-13 |
| NFR-003 | Scope and consent uncertainty MUST fail closed rather than widen publication implicitly. | Inference | Story step 3 |
| NFR-004 | Retrieval identifiers and integrity proofs SHOULD be stable enough for later audit, replay, and verification. | Inference | Story steps 9-12 |
| NFR-005 | Storage terms SHOULD remain settlement-neutral so the archival subsystem does not require crypto-specific payment semantics. | Inference | Story step 7 + Proposal 011 |
| NFR-006 | High-value artifact storage SHOULD support explicit replication and failover policy rather than assume a single durable archivist. | Inference | Story step 7 |
| NFR-007 | Publication timing and broader vault promotion SHOULD remain independently configurable from mere storage success. | Inference | Story steps 7, 11 |

## Trade-offs

1. Explicit archivist/vault roles vs simpler "just store it somewhere":
   - Benefit: clearer provenance, policy, and publication semantics.
   - Risk: more contracts and operational steps.
2. Fail-closed archival export vs convenience:
   - Benefit: lower privacy and dignity risk.
   - Risk: some artifacts remain stranded locally until policy is clarified.
3. Rich archival package vs minimal blob storage:
   - Benefit: later audit, retrieval, and curation stay tractable.
   - Risk: more metadata discipline is required.
4. Settlement-neutral storage terms vs one concrete payment rail:
   - Benefit: avoids overcommitting the protocol core to one regulatory or technical model.
   - Risk: external settlement integration remains underspecified in MVP.
5. Explicit publication scopes vs one generic memory pool:
   - Benefit: predictable disclosure semantics.
   - Risk: more state transitions and client UX complexity.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Artifact exported without valid archival basis | Privacy or governance breach | Fail closed and require curator or policy review before export. |
| Stored artifact loses provenance or redaction semantics | Later misuse or invalid publication | Reject archival package when mandatory metadata is incomplete. |
| Archivist accepts artifact but returns unstable or unusable identifiers | Retrieval failure | Make storage confirmation contract mandatory and validated. |
| Public promotion happens implicitly after private retention | Scope breach | Keep promotion as a separate explicit state transition with trace. |
| Single archivist disappears | Loss of availability | Define replication or fallback retrieval policy for high-value artifacts. |
| Stored artifact is later treated as training-safe by default | Unsafe model contamination | Keep training eligibility outside archival success and require later approval. |
| Payment or retention terms leak into protocol core assumptions | Architecture lock-in and regulatory drag | Keep settlement rail neutral and external to core archival semantics. |

## Open Questions

1. What exact v1 schema set should freeze `ArchivalPackage`, `ArchivistAdvertisement`, and retrieval contracts?
2. Which artifact classes require curator review before `federation-vault` or `public-vault` promotion?
3. What minimum integrity proof should archivists return in MVP?
4. When should high-value artifacts require multi-archivist replication by default?
5. Should transcript bundles and generic knowledge artifacts share one archival package contract or separate specializations?
6. What federation-level approval, if any, should be required before `public-vault` promotion of sensitive-but-redacted material?

## Next Actions

1. Define v1 schema for `ArchivalPackage`.
2. Define v1 schema for `ArchivistAdvertisement` and retrieval contracts.
3. Align archival confirmations with existing procurement contract and receipt semantics where paid retention applies.
4. Define replication and failover policy for high-value artifacts.
5. Add end-to-end test: eligible artifact -> curator gate -> archivist transfer -> storage confirmation -> later retrieval.
6. Add negative test: ambiguous archival basis MUST block export and keep artifact local or quarantined.
