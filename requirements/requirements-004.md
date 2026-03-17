# Requirements 004: Transcript Curation and Safe Model Specialization

Based on:
- `proposals/003-question-envelope-and-answer-channel.md`
- `proposals/004-human-origin-flags-and-operator-participation.md`
- `memos/transcription-monitors-and-public-vaults.md`
- `memos/swarm-broadcast-assistance.md`
- `memos/swarm-communication-exposure-modes.md`

Date: `2026-03-17`
Status: Draft

## Executive Summary

This document defines requirements for turning valuable swarm discussions into durable,
curated transcript corpora and then using approved corpora for safe model
specialization.

The requirements prioritize:
- dignity, privacy, and consent before data extraction,
- auditable provenance from transcript segment to adapter artifact,
- adapter-first specialization (`LoRA` / `QLoRA`) instead of silent base-model mutation,
- reversible, policy-gated training and deployment,
- clear separation between raw discussion, curated corpora, and deployable model assets.

## Context and Problem Statement

Orbiplex aims to create a practical learning flywheel:

- nodes ask and answer real questions,
- high-value debates become source transcripts,
- transcripts are curated into reusable corpora,
- corpora are used to specialize models for future swarm work.

The challenge is to do this without violating privacy, collapsing governance
boundaries, poisoning future models with unresolved or harmful material, or turning
swarm communication into indiscriminate surveillance.

The system therefore needs explicit controls for:

- who may observe and transcribe,
- what may leave a channel,
- how transcript bundles are redacted and curated,
- when material becomes eligible for training,
- how specialized adapters are evaluated, published, revoked, and attributed.

## Proposed Model / Decision

### Actors and Boundaries

- `Asking Node`: opens or participates in a question/answer channel.
- `Participant Node`: contributes to discussion and evidence.
- `Human Operator`: a human behind a participating node who may be consulted privately or may join a live room under policy.
- `Transcription Monitor`: observes selected channels and produces source transcripts.
- `Secretary / Curator`: writes summaries, applies redaction, and promotes or rejects transcript material.
- `Archivist Node`: stores accepted transcript bundles in federation or public vaults.
- `Training Node`: builds specialization artifacts from approved corpora.
- `Model Governor` (human or policy-gated process): approves deployment, rollback, and visibility of trained artifacts.

### Content States

Artifacts MUST move through explicit states:

1. `raw-transcript`
2. `redacted-transcript`
3. `curated-corpus-entry`
4. `training-approved`
5. `adapter-built`
6. `adapter-validated`
7. `adapter-deployed` or `adapter-rejected`

No artifact may skip state transitions implicitly.

### Core Data Contracts (normative)

- `TranscriptSegment`:
  - `segment_id`, `question_id`, `channel_id`, `message_id`, `speaker_ref`, `gateway_node_ref`, `origin_class`, `operator_presence_mode`, `human_origin`, `ts`, `content`, `visibility_scope`, `consent_basis`, `provenance_refs`, optional `redaction_markers`.
- `TranscriptBundle`:
  - `bundle_id`, `question_id`, `source_scope`, `created_at`, `segments`, `source_nodes`, `contains_human_origin`, `contains_direct_human_live`, `consent_basis`, `redaction_status`, `integrity_proof`.
- `CurationDecision`:
  - `decision_id`, `bundle_id`, `status` (`accepted|accepted-redacted|quarantined|rejected`), `reason_codes`, `curator_ref`, `ts`.
- `CorpusEntry`:
  - `entry_id`, `bundle_id`, `content_pointer`, `domain_tags`, `quality_grade`, `risk_grade`, `training_eligibility`, `provenance_manifest`.
- `TrainingJob`:
  - `job_id`, `base_model_ref`, `method` (`lora|qlora`), `dataset_refs`, `policy_profile`, `started_at`, `ended_at`, `operator_ref`.
- `AdapterArtifact`:
  - `adapter_id`, `job_id`, `base_model_ref`, `adapter_hash`, `eval_report_ref`, `deployment_scope`, `rollback_ref`, `creator_refs`.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST support a `Transcription Monitor` role that can observe selected channels according to explicit scope and policy. | Fact | Memo |
| FR-002 | A monitor MUST bind every captured transcript segment to `question_id` or equivalent source channel identifier. | Fact | Memo |
| FR-003 | Transcript capture MUST preserve speaker attribution, timestamps, provenance links, and integrity metadata sufficient to detect later tampering. | Fact | Memo |
| FR-004 | The system MUST support channel policies that forbid transcription entirely, allow only redacted export, or allow archival export under explicit conditions. | Inference | Exposure modes + values |
| FR-005 | Transcript publication outside the original live channel MUST require an explicit `consent_basis` or another policy basis recorded in the artifact metadata. | Inference | Dignity/privacy/servant integrity |
| FR-006 | The system MUST support redaction before archival promotion, including removal or masking of personal data, sensitive context, and protected identifiers. | Fact | Memo + values |
| FR-007 | Curators MUST be able to classify transcript bundles as `accepted`, `accepted-redacted`, `quarantined`, or `rejected`. | Inference | Operational model |
| FR-008 | Archivist nodes MUST advertise willingness to receive transcript bundles and MUST store accepted bundles in a vault with stable identifiers and retrieval metadata. | Fact | Memo |
| FR-009 | Vaults MUST support federation-local and public visibility modes as separate publication classes. | Fact | Memo + exposure modes |
| FR-010 | The system MUST maintain provenance from every curated corpus entry back to transcript bundle and original question/channel context. | Inference | Auditability |
| FR-011 | The system MUST support `LoRA` and `QLoRA` as specialization methods for approved corpora. | Fact | User intent |
| FR-012 | The system MUST treat adapter-based specialization as the default path; direct mutation or overwrite of base models MUST NOT be the default workflow. | Inference | Reversibility + immutability |
| FR-013 | Only corpus entries with explicit `training_eligibility` MAY enter a training job. | Inference | Safety model |
| FR-014 | Material labeled `quarantined`, `rejected`, or unresolved-sensitive MUST NOT be used for training. | Inference | Epistemic safety + non-harm |
| FR-015 | The system MUST support separate policy profiles for private, federation-local, and public training corpora. | Inference | Exposure modes |
| FR-016 | Every training job MUST emit a `TrainingJob` record and a resulting `AdapterArtifact` record with hashes and evaluation references. | Inference | Auditability |
| FR-017 | Deployment of a newly trained adapter MUST be reversible and linked to a rollback reference or disable path. | Inference | Reversibility |
| FR-018 | Specialized adapters MUST remain attributable to their source corpora and creators or contributors where attribution policy requires it. | Inference | Creator credits / authorship |
| FR-019 | The system MUST support publishing model cards or equivalent manifests describing domain, training scope, excluded data classes, known risks, and intended use. | Inference | Transparency |
| FR-020 | Training nodes MUST be able to consume vault material without needing unrestricted access to raw private channels. | Inference | Boundary separation |
| FR-021 | The system MUST preserve `origin_class` for transcript segments, distinguishing at least `node-generated`, `node-mediated-human`, and `human-live`. | Inference | Proposal 004 |
| FR-022 | If a human contribution enters a live room through a node gateway, the transcript layer MUST preserve both `speaker_ref` and `gateway_node_ref`. | Inference | Proposal 004 |
| FR-023 | The system MUST record whether operator presence was `none`, `mediated`, or `direct-live` for transcript material derived from active debates. | Inference | Proposal 004 |
| FR-024 | Channel or room policy MUST be able to forbid direct live human participation while still allowing mediated operator consultation. | Inference | Proposal 004 |
| FR-025 | Direct human live material MUST NOT be promoted to `training-approved` unless curation records an explicit policy basis for archival and training eligibility. | Inference | Proposal 004 + dignity |
| FR-026 | Curators MUST be able to exclude, isolate, or separately grade human-originated material when assembling corpora. | Inference | Proposal 004 |
| FR-027 | Training profiles MUST support excluding or separately weighting `human-live` and `node-mediated-human` corpus entries. | Inference | Proposal 004 |
| FR-028 | Summaries derived from debates containing human-linked material MUST preserve enough provenance to indicate whether accepted reasoning relied on mediated or direct human input. | Inference | Proposal 004 |
| FR-029 | If a secretary preserves or republishes human-linked material after node failure, the secretary MUST preserve the original origin class and MUST NOT silently flatten provenance. | Inference | Proposal 004 |
| FR-030 | Public-vault publication policy SHOULD default to stricter handling for `human-live` material than for purely node-generated debate unless a federation explicitly relaxes that rule. | Inference | Proposal 004 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Transcript, curation, and training contracts MUST be versioned and interoperable across heterogeneous nodes and federations. | Inference | Interoperability |
| NFR-002 | The pipeline MUST preserve dignity and privacy by default: least disclosure, bounded retention, and explicit scope separation. | Inference | Core values |
| NFR-003 | Training eligibility decisions MUST be auditable through stored reason codes and signed or otherwise tamper-evident metadata. | Inference | Procedural justice |
| NFR-004 | Redaction operations SHOULD be reproducible or at least traceable, so later reviewers can distinguish source omission from original absence. | Inference | Auditability |
| NFR-005 | Adapter evaluation MUST include quality checks, regression checks, and risk checks before deployment. | Inference | Safe learning |
| NFR-006 | Base-model references, adapter hashes, dataset references, and evaluation artifacts MUST remain stable enough for replay and rollback. | Inference | Reproducibility |
| NFR-007 | Fine-tuning workloads SHOULD be isolated from live serving paths so failed training jobs do not degrade answer-serving availability. | Inference | Operational safety |
| NFR-008 | Public vault publication SHOULD support deduplication, integrity verification, and efficient incremental sync across redundant archivist nodes. | Inference | Durability |
| NFR-009 | The system MUST fail closed on policy uncertainty: when consent, redaction, or eligibility status is ambiguous, the material is blocked from archival promotion and training by default. | Inference | Servant integrity / least harm |
| NFR-010 | Deployment policy SHOULD allow federation-specific acceptance thresholds so one federation may reject an adapter another federation accepts. | Inference | Pluralism + federation autonomy |
| NFR-011 | Provenance semantics for human-linked material MUST survive transcript export, curation, archival storage, and dataset assembly without lossy flattening. | Inference | Proposal 004 |
| NFR-012 | User-facing and curator-facing tooling SHOULD make human-originated material inspectable and filterable without requiring exposure of real-world identity. | Inference | Proposal 004 |

## Trade-offs

1. Rich transcripts vs privacy:
   - Benefit: stronger future synthesis and better specialized adapters.
   - Risk: higher sensitivity and redaction burden.
2. Adapter-first training vs maximal model change:
   - Benefit: reversibility, lower operational risk, cleaner provenance.
   - Risk: some tasks may improve less than with full fine-tuning.
3. Strict curation gates vs learning speed:
   - Benefit: lower contamination and harm risk.
   - Risk: slower growth of reusable corpora.
4. Public vaults vs federation-local vaults:
   - Benefit: public vaults increase reuse and commons value.
   - Risk: broader disclosure and more complex consent/governance.
5. Human-governed promotion vs automatic pipelines:
   - Benefit: stronger safety and contextual judgment.
   - Risk: higher latency and labor cost.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Private or sensitive discussion is archived without valid basis | Privacy and dignity breach | Require explicit `consent_basis`, scope policy checks, and fail-closed archival gating. |
| Redaction misses critical identifiers | Re-identification risk | Add redaction review stage, sensitive-pattern checks, and vault publication hold until review passes. |
| Low-quality or manipulative debate enters corpus | Training contamination | Require curation status, quality grade, and risk grade before `training-approved`. |
| Unresolved or contested claims are trained as fact | Model epistemic drift | Keep unresolved material out of training by default; require explicit quarantine handling. |
| Human live input is flattened into ordinary node output | Provenance loss and invalid training assumptions | Make `origin_class`, `gateway_node_ref`, and operator-presence fields mandatory in transcript and corpus metadata. |
| Human-originated content is published or trained without valid basis | Dignity, consent, or scope breach | Require explicit eligibility gates for `human-live` and stricter default policy for public publication. |
| Adapter regresses critical behavior | Lower answer quality or safety | Require evaluation suite, shadow deployment, and rollback path before general release. |
| Base model and adapter provenance diverge | Impossible audit or rollback | Make `base_model_ref`, `adapter_hash`, and `job_id` mandatory deployment metadata. |
| Archivist node stores tampered transcript bundle | Corrupted commons memory | Require integrity proof verification and periodic revalidation across redundant vault nodes. |
| Training node overreaches visibility scope | Policy breach across federations | Enforce scope-aware dataset access and federation-specific training policy profiles. |

## Open Questions

1. What canonical `consent_basis` taxonomy should be used (`explicit-consent`, `public-scope`, `federation-policy`, `emergency-exception`, etc.)?
2. What minimum redaction standard is required before federation-local material becomes public-vault eligible?
3. Should unresolved transcript material ever be used for adversarial or debate-style adapters under a separate policy profile?
4. What is the minimum evaluation suite for an adapter to move from `adapter-built` to `adapter-validated`?
5. How should creator attribution and compensation interact with transcript-derived training corpora?
6. When should a specialized adapter expire, decay, or require revalidation against newer corpora?
7. Should archivist nodes replicate raw transcript bundles, redacted bundles, or both under separate visibility domains?
8. What consent basis is sufficient for `human-live` material to move from archive eligibility to training eligibility?
9. Should federations maintain separate evaluation suites for adapters trained on corpora containing direct human live material?

## Next Actions

1. Define v1 schemas for `TranscriptSegment`, `TranscriptBundle`, `CurationDecision`, `CorpusEntry`, `TrainingJob`, and `AdapterArtifact`.
2. Define `consent_basis`, `redaction_status`, `quality_grade`, and `risk_grade` enumerations.
3. Define federation policy profiles for archival export and training eligibility.
4. Define evaluation gates for adapter promotion, including rollback and shadow-deployment rules.
5. Define vault sync and integrity verification behavior for redundant archivist nodes.
6. Define attribution policy for transcript-derived corpora and adapter artifacts.
7. Implement end-to-end test flow: live channel -> transcript bundle -> redaction -> curation -> vault -> LoRA/QLoRA job -> evaluation -> deploy/rollback.
8. Define `origin_class`, `operator_presence_mode`, and `human_origin` enumerations and validation rules.
9. Define public-vault defaults and override policy for `human-live` and `node-mediated-human` material.
