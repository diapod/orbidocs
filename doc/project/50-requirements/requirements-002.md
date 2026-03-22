# Requirements 002: Federated Peer Learning and Consensus Correction

Based on: `doc/project/30-stories/story-002.md`
Date: `2026-02-22`
Status: Draft (MVP scope)

## Executive Summary

This document defines MVP requirements for a node-to-node learning loop where a node asks in a public thematic channel, receives responses from other nodes, escalates disagreements into an ad-hoc discussion channel, and consolidates resulting knowledge into local retrieval and learning assets.

The requirements prioritize:
- interoperable peer exchange,
- explicit disagreement handling,
- auditable knowledge consolidation,
- bounded autonomy for model updates.

## Context and Problem Statement

A single node can improve answer quality over time by learning from other specialized nodes. The challenge is to support this learning in a federated environment while controlling quality drift, misinformation propagation, and resource usage.

The system needs an operational flow for:
- public query/response exchange,
- contradiction-driven peer review,
- consensus-oriented correction,
- safe persistence into local memory and optional mini-model training.

## Proposed Model / Decision

### Actors and Boundaries

- `Querying Node`: initiates query and consolidates learned knowledge.
- `Responding Nodes`: provide candidate answers and observations.
- `Consensus Participants`: nodes joining an ad-hoc channel due to detected mismatch.
- `Local Orchestrator`: coordinates ingestion and persistence into retrieval/training targets.

### Protocol Phases

1. `Discovery/Exchange`: node joins thematic public channel and publishes query.
2. `Response Intake`: node receives one or more answers with metadata.
3. `Divergence Review`: nodes detecting substantial mismatch can open or join an ad-hoc discussion channel bound to the specific Q&A.
4. `Consensus Outcome`: participants share observations and converge on one of: `confirmed`, `corrected`, `unresolved`.
5. `Knowledge Consolidation`: querying node persists artifacts into local vector memory, scanned-directory files, and/or mini-model training queue.

### Core Data Contracts (normative)

- `PublicQuery`:
  - `query_id`, `channel_id`, `query_text`, `specialization_tags`, `timestamp`.
- `PeerResponse`:
  - `response_id`, `query_id`, `node_id`, `answer_text`, optional `evidence_refs`, `timestamp`.
- `DivergenceSignal`:
  - `query_id`, `response_id`, `node_id`, `mismatch_reason`, optional `confidence`.
- `AdHocDiscussion`:
  - `discussion_id`, `query_id`, `response_id`, participant set, message log.
- `ConsensusOutcome`:
  - `query_id`, `response_id`, `status` (`confirmed|corrected|unresolved`), summary, participants.
- `KnowledgeArtifact`:
  - `artifact_id`, `source_type` (`vector|file|train-queue`), content pointer, provenance metadata.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The node MUST connect to an IRC-like network and join at least one public thematic channel. | Fact | Story step 1 |
| FR-002 | The node MUST publish a query message to the joined channel. | Fact | Story step 2 |
| FR-003 | The node MUST ingest responses from peer nodes and associate them with the original query. | Fact | Story step 3 |
| FR-004 | The protocol MUST allow peers to flag suspected incorrect responses when they significantly diverge from their knowledge. | Fact | Story step 4 |
| FR-005 | The protocol MUST support creating/joining an ad-hoc channel scoped to the specific question and response under review. | Fact | Story step 4 |
| FR-006 | Participants in the ad-hoc channel MUST be able to exchange observations aimed at reaching consensus. | Fact | Story step 4 |
| FR-007 | The querying node MUST persist collected knowledge with provenance sufficient to trace source query/response/discussion. | Inference | Story steps 3-5 |
| FR-008 | The node MUST support immediate vector-memory enrichment from accepted knowledge artifacts. | Fact | Story step 5 |
| FR-009 | The node MUST support deferred enrichment by writing artifacts to files in scanned directories. | Fact | Story step 5 |
| FR-010 | The node MUST support routing accepted artifacts to a mini-model training pipeline for specialization or general knowledge support. | Fact | Story step 5 |
| FR-011 | The node MUST classify each consolidated artifact as `confirmed`, `corrected`, or `unresolved` before downstream use. | Inference | Story step 4 |
| FR-012 | The node MUST prevent automatic promotion of `unresolved` artifacts into trusted retrieval context without explicit policy allowance. | Inference | Story steps 4-5 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Channel and message contracts MUST be explicit and versioned to preserve interoperability across heterogeneous nodes. | Inference | Core intent: interoperability |
| NFR-002 | Knowledge consolidation operations MUST be auditable through provenance metadata and immutable identifiers. | Inference | Core intent: auditability |
| NFR-003 | Consensus discussion SHOULD be bounded by configurable time and message limits to avoid unbounded resource consumption. | Inference | Story step 4 |
| NFR-004 | The system MUST expose policy controls for auto-ingestion and auto-training to preserve human agency. | Inference | Core intent: human agency |
| NFR-005 | Divergence detection SHOULD remain deterministic for identical inputs under the same configured thresholds. | Inference | Story step 4 |
| NFR-006 | The pipeline MUST fail safely: if consensus is unavailable, artifacts remain labeled `unresolved` and are isolated from trusted context by default. | Inference | Story step 4 |
| NFR-007 | The system SHOULD tolerate partial network failures and continue local consolidation of already received data. | Inference | Story steps 3-5 |

## Trade-offs

1. Open public exchange vs noise:
   - Benefit: broad peer coverage and faster knowledge acquisition.
   - Risk: higher variance in answer quality.
2. Ad-hoc consensus vs latency:
   - Benefit: improved correctness through peer correction.
   - Risk: slower finalization of knowledge artifacts.
3. Immediate vector ingestion vs strict validation:
   - Benefit: faster retrieval improvement.
   - Risk: contamination by unresolved or low-quality artifacts.
4. Mini-model training vs operational complexity:
   - Benefit: long-term specialization gains.
   - Risk: extra compute cost and governance overhead.
5. Flexible federated participation vs Sybil/abuse exposure:
   - Benefit: openness and scale.
   - Risk: manipulation pressure on consensus and quality signals.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| No peer responses | No enrichment from federation | Return explicit no-response state and optionally retry on additional channels. |
| Conflicting responses with no consensus | Ambiguous knowledge artifact | Mark as `unresolved`, keep outside trusted retrieval by default. |
| Ad-hoc discussion spam/flood | Resource exhaustion and poor signal quality | Enforce participant caps, rate limits, and discussion TTL. |
| Incorrect artifact promoted to trusted memory | Retrieval quality degradation | Require status gate (`confirmed` or policy-approved `corrected`) before trusted ingestion. |
| Broken provenance links | Loss of auditability | Reject persistence when required provenance fields are missing. |
| Training queue poisoned by low-quality data | Model drift | Apply quality thresholding and manual approval mode for training-bound artifacts. |
| Network partition during discussion | Premature finalization | Persist intermediate state and allow discussion resume/reconciliation. |

## Open Questions

1. What exact threshold defines "significant mismatch" for `DivergenceSignal`?
2. Which consensus rule is the MVP default (majority, weighted trust, curator decision)?
3. Should `corrected` artifacts be auto-ingested into trusted retrieval, or require additional verification?
4. What is the minimum provenance payload needed to keep storage efficient but auditable?
5. How should trust weighting be calculated for responding/discussing nodes in early network bootstrap?
6. What guardrails are required before moving artifacts from file/vector memory into mini-model training?

## Next Actions

1. Define v1 schemas for `PublicQuery`, `PeerResponse`, `DivergenceSignal`, `AdHocDiscussion`, `ConsensusOutcome`, and `KnowledgeArtifact`.
2. Create ADR-003 for consensus semantics (status model, thresholding, and tie handling).
3. Create ADR-004 for knowledge-ingestion policy gates (`confirmed/corrected/unresolved` behavior).
4. Implement protocol-validation tests for query/response linkage and provenance completeness.
5. Implement deterministic divergence-detection tests with fixed thresholds.
6. Implement end-to-end test: public query -> peer responses -> ad-hoc discussion -> consensus outcome -> vector/file/train-queue persistence.
7. Define operational limits (participant cap, message rate, discussion TTL) and validate with stress scenarios.
