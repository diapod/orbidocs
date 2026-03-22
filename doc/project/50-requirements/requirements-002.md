# Requirements 002: Federated Peer Learning and Consensus Correction

Based on:
- `doc/project/30-stories/story-002.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/50-requirements/requirements-004.md`

Date: `2026-03-22`
Status: Draft (MVP scope)

## Executive Summary

This document defines MVP requirements for a federated peer-learning loop where a
question-bound answer room becomes the place for contradiction review, correction, and
bounded knowledge consolidation.

The requirements prioritize:
- correction inside the existing answer-room flow instead of ad-hoc public side
  channels,
- explicit outcome states (`confirmed`, `corrected`, `unresolved`),
- provenance-rich promotion of accepted learning artifacts,
- transcript-aware but policy-gated observation,
- strict separation between immediate correction, durable archival, and later
  training.

## Context and Problem Statement

`story-002.md` no longer models learning as "ask on a public thematic channel, then
silently ingest whatever came back".

The current corpus assumes:

- a signed question envelope and a room bound to `question/id`,
- exposure mode and room policy profile as explicit constraints,
- secretary/summary functions as durable room outputs,
- transcript monitoring only under explicit policy,
- learning promotion that preserves provenance and does not silently turn unresolved
  debate into trusted knowledge.

The system therefore needs a stable correction model for when room participants detect
that a candidate answer materially conflicts with other evidence or domain knowledge.

## Proposed Model / Decision

### Actors and Boundaries

- `Asking Node`: opened the question and remains responsible for answer acceptance or
  delegated acceptance.
- `Participant Node`: contributes candidate answers, objections, examples, or
  counter-evidence.
- `Secretary`: may emit intermediate or accepted summaries linked to the room.
- `Transcription Monitor`: may observe and preserve transcript material if room policy
  allows it.
- `Local Orchestrator`: applies promotion rules to local retrieval assets and later
  handoff to curation or training layers.

### Protocol Phases

1. `Question Context`: a question envelope opens or binds a room.
2. `Candidate Intake`: the room accumulates candidate answers and evidence.
3. `Divergence Review`: a node or secretary identifies a material mismatch.
4. `Correction Path`: participants compare evidence inside the same question-bound
   room or a tightly linked review path preserving the same provenance root.
5. `Outcome Classification`: the room or delegated decider labels the disputed claim
   as `confirmed`, `corrected`, or `unresolved`.
6. `Knowledge Promotion`: only accepted outcomes enter trusted local retrieval or
   downstream curation flows according to policy.

### Core Data Contracts (normative)

- `QuestionEnvelope`:
  - stable question identity and scope root for all later correction artifacts.
- `AnswerRoomMetadata`:
  - room policy, visibility, and provenance expectations for learning events.
- `RoomSummary` or accepted summary artifact:
  - durable representation of intermediate or final room understanding.
- `ResponseEnvelope`:
  - accepted or corrected answer artifact returned to the asker.
- `TranscriptSegment` / `TranscriptBundle`:
  - source evidence for later archival or curation when monitoring is allowed.
- `LearningOutcome` (not yet frozen as schema):
  - `question_id`, disputed answer ref, outcome status, supporting refs, decider ref,
    timestamp.
- `KnowledgeArtifact` (not yet frozen as schema):
  - local promotion target with provenance linking back to room outcomes.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST treat the answer room bound to `question/id` as the primary place for peer correction and consensus review. | Fact | Story steps 1-4 |
| FR-002 | The system MUST support detecting a material mismatch between candidate answers, local retrieval evidence, federation procedure, or specialization-specific knowledge. | Fact | Story step 2 |
| FR-003 | Correction flow MUST preserve the provenance root of the original question and MUST NOT require a detached public correction channel as the normative path. | Fact | Story step 3 |
| FR-004 | Participants MUST be able to exchange counter-evidence, implementation notes, examples, and objections inside the correction flow. | Fact | Story step 4 |
| FR-005 | The system SHOULD support one or more intermediate summaries so that durable correction state does not depend only on raw room history. | Inference | Story step 4 |
| FR-006 | If transcript observation is enabled by room policy, captured correction discussion MUST preserve visibility scope, provenance, and human-origin markers where applicable. | Fact | Story step 5 |
| FR-007 | Every disputed correction outcome MUST be classified as `confirmed`, `corrected`, or `unresolved`. | Fact | Story step 6 |
| FR-008 | If a correction is accepted, the system MUST emit a durable room-linked artifact such as an accepted summary or corrected response envelope. | Fact | Story step 7 |
| FR-009 | The local node MUST record enough provenance to reconstruct question, participants, supporting evidence, and human-linked influence for accepted learning outcomes. | Fact | Story step 8 |
| FR-010 | The local node MAY promote `confirmed` and policy-accepted `corrected` material into trusted local retrieval assets. | Fact | Story step 9 |
| FR-011 | Material classified as `unresolved` MUST NOT enter trusted retrieval by default. | Fact | Story step 10 |
| FR-012 | `Unresolved` material MAY be retained for later review, adversarial evaluation, or curator inspection under separate policy. | Fact | Story step 10 |
| FR-013 | If the discussion is later promoted into archival or corpus flows, that promotion MUST happen through explicit curation steps rather than ambient room-history retention. | Fact | Story step 11 |
| FR-014 | Raw discussion and unresolved corrections MUST NOT directly become training data. | Fact | Story step 12 |
| FR-015 | Training eligibility for peer-learning artifacts MUST depend on explicit later approval in corpus or curation layers. | Inference | Story step 12 + Req-004 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Correction semantics MUST be explicit and versionable so heterogeneous nodes can interpret `confirmed`, `corrected`, and `unresolved` consistently. | Inference | Interoperability |
| NFR-002 | The system MUST preserve auditable provenance from corrected outcome back to room context and supporting evidence. | Inference | Story steps 7-9 |
| NFR-003 | Policy uncertainty around transcript export or human-linked material MUST fail closed. | Inference | Story step 5 + Req-004 |
| NFR-004 | Promotion into trusted retrieval SHOULD be deterministic under identical policy and evidence inputs. | Inference | Story steps 6-10 |
| NFR-005 | The correction path SHOULD tolerate partial node absence as long as durable summaries and evidence refs survive. | Inference | Current room/event model |
| NFR-006 | Later archival or training subsystems MUST remain separable from immediate answer-serving and correction mechanics. | Inference | Story steps 11-12 |
| NFR-007 | The system SHOULD make accepted and unresolved outcomes inspectable without requiring full replay of raw room history. | Inference | Story step 4 |

## Trade-offs

1. Correction inside the room vs separate adjudication channel:
   - Benefit: one provenance root and less transport complexity.
   - Risk: busy rooms may need stronger summarization discipline.
2. Explicit outcome states vs free-form debate:
   - Benefit: stable promotion policy.
   - Risk: forces a sharper closure model than some discussions naturally have.
3. Transcript-aware correction vs privacy burden:
   - Benefit: stronger evidence and later auditability.
   - Risk: room policy and consent handling become operationally important.
4. Policy-gated promotion vs immediate learning speed:
   - Benefit: lower contamination of trusted retrieval.
   - Risk: slower accumulation of reusable knowledge.
5. Separation of correction from training vs simplicity:
   - Benefit: safer model specialization path.
   - Risk: requires more explicit later pipeline stages.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Divergent answers never converge | No reliable correction outcome | Emit `unresolved`, isolate from trusted retrieval, and allow later curator review. |
| Accepted correction loses provenance | Audit and replay failure | Reject promotion when required room/evidence references are missing. |
| Transcript monitor exports discussion without valid basis | Privacy or dignity breach | Require room-policy checks and fail closed on ambiguity. |
| Over-eager auto-promotion contaminates local retrieval | Lower answer quality | Gate promotion by outcome status and explicit policy profile. |
| Human-linked input is flattened into ordinary node output | Provenance loss and invalid future training assumptions | Preserve origin and gateway semantics in room-linked artifacts. |
| Summary contradicts underlying room evidence | Durable false correction | Keep evidence refs mandatory and allow secretary or curator challenge. |
| Unresolved debate leaks into training pipeline | Epistemic drift | Require explicit corpus-level training approval and exclude unresolved state by default. |

## Open Questions

1. What exact threshold defines a `material mismatch` worth formal correction?
2. What is the MVP default decision rule for `confirmed` vs `corrected` when no single authority exists?
3. Should `corrected` outcomes require stronger evidence than `confirmed` outcomes before local trusted promotion?
4. What exact schema should freeze `LearningOutcome` and `KnowledgeArtifact` v1?
5. Should adversarial or unresolved material be retained in a dedicated evaluation corpus profile?
6. What minimum evidence reference set is required before a secretary summary may drive trusted promotion?

## Next Actions

1. Define v1 schema for `LearningOutcome`.
2. Define v1 schema for local `KnowledgeArtifact` promotion records.
3. Align room summaries and response-envelope semantics with correction outcomes.
4. Define material-mismatch and tie-handling policy for early federations.
5. Add end-to-end test: question room -> divergence review -> accepted correction -> trusted local promotion.
6. Add negative test: unresolved correction MUST remain outside trusted retrieval and training paths.
