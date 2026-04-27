# Learning Outcomes, Knowledge Artifacts, and Archival Contracts

Based on:
- `doc/project/50-requirements/requirements-002.md`
- `doc/project/50-requirements/requirements-003.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

## Status

Proposed (Draft)

## Date

2026-03-22

## Executive Summary

This proposal defines the missing contract layer between:

1. answer-room correction and local knowledge promotion,
2. archival export and later retrieval,
3. durable storage and later curation or training use.

The key decision is to introduce a small family of explicit, portable contracts
instead of overloading existing transcript or procurement artifacts with extra
semantics.

## Context and Problem Statement

`requirements-002.md` now defines how accepted room corrections become
`confirmed`, `corrected`, or `unresolved` outcomes.

`requirements-003.md` defines how valuable artifacts move into archivist and vault
flows with explicit publication scope.

What remains underspecified is the contract layer between those two points:

- what exactly is the durable record of a learning outcome,
- what exactly is promoted into local retrieval,
- what package is actually handed to an archivist,
- how an archivist advertises storage capability,
- how later retrieval should look.

Without explicit contracts:

- learning and archival semantics leak into prose only,
- implementations may flatten provenance differently,
- archivist and retrieval behavior becomes transport-coupled,
- later training or curation may consume under-specified blobs.

## Goals

- Introduce a small, interoperable contract set for learning and archival flows.
- Preserve one provenance root from question room to promoted artifact and archived package.
- Keep archival transport settlement-neutral.
- Separate local promotion semantics from archivist-facing packaging semantics.
- Make later retrieval explicit and scope-aware.

## Non-Goals

- This proposal does not freeze transcript schemas beyond their current v1 scope.
- This proposal does not define the full curation workflow.
- This proposal does not define the full training dataset contract.
- This proposal does not require a specific transport or storage backend.

## Decision

Orbiplex should adopt the following v1 contract family:

1. `LearningOutcome`
2. `KnowledgeArtifact`
3. `ArchivalPackage`
4. `ArchivistAdvertisement`
5. `RetrievalRequest`
6. `RetrievalResponse`

These contracts should be treated as separate layers:

- `LearningOutcome` describes what epistemic result emerged from room correction,
- `KnowledgeArtifact` describes what the local node promoted for later use,
- `ArchivalPackage` describes what is handed to an archivist or vault flow,
- `ArchivistAdvertisement` describes what an archivist is willing to accept,
- `RetrievalRequest` and `RetrievalResponse` describe later access to archived material.

## Proposed Model

### 1. `LearningOutcome`

Purpose:

- freeze the durable result of a correction event linked to one question room,
- classify the outcome as `confirmed`, `corrected`, or `unresolved`,
- preserve supporting references and decider provenance.

It should not itself describe where data was later promoted or archived.

### 2. `KnowledgeArtifact`

Purpose:

- record what the local node promoted from a learning outcome,
- distinguish trusted local retrieval from review-only or training-candidate paths,
- keep promotion policy explicit.

It should remain local- or federation-portable data, not an implementation-specific
vector index record.

### 3. `ArchivalPackage`

Purpose:

- package an artifact for durable retention or publication,
- carry publication scope, archival basis, classification label, redaction state, integrity proof, and
  retention hints,
- remain generic enough to wrap summaries, transcript bundles, corpus candidates, or
  promoted knowledge artifacts.

### 4. `ArchivistAdvertisement`

Purpose:

- let archivists advertise what scopes and artifact classes they accept,
- declare default retrieval and retention posture,
- optionally expose whether settlement or negotiated terms are required.

### 5. Retrieval contracts

`RetrievalRequest` and `RetrievalResponse` should:

- preserve scope-aware access semantics,
- distinguish success, denial, temporary unavailability, and tombstoned state,
- keep integrity verification explicit.

## Design Principles

1. One provenance root:
   - later contracts should link back to room/question lineage rather than invent a
     disconnected identity tree.
2. Data first:
   - contracts stay portable JSON/EDN-friendly values, not transport-bound objects.
3. Minimal trusted core:
   - contracts preserve what later layers need, but do not freeze storage backend or
     retrieval implementation.
4. Settlement-neutral archival:
   - retention/payment terms may exist, but archival semantics must not depend on a
     crypto-specific rail.
5. Explicit trust transitions:
   - `unresolved` must not silently become trusted local retrieval or training input.

## Trade-offs

1. More contracts vs fewer overloaded objects:
   - Benefit: cleaner semantics and thinner abstractions.
   - Cost: more files and validation surface.
2. Generic archival package vs transcript-only package:
   - Benefit: one archival layer can serve multiple artifact classes.
   - Cost: some specialization moves to conventions and policy.
3. Explicit retrieval contracts vs implicit blob fetch:
   - Benefit: auditability and scope safety.
   - Cost: more protocol surface.

## Open Questions

1. Should `LearningOutcome` remain generic, or later split into room-summary and response-correction specializations?
2. Should `KnowledgeArtifact` distinguish local-only from federation-shareable promotion more strongly in v1?
3. Should `ArchivalPackage` support inline payloads in v1, or only stable content references?
4. Should archivist advertisements expose replication guarantees explicitly in v1 or only policy hints?

## Next Actions

1. Add v1 schemas for the six contracts.
2. Add positive and negative examples for each schema family.
3. Align validator mappings and generated schema docs.
4. Revisit curation and training proposal set after these contracts stabilize.
