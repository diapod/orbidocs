# Orbiplex Node

`Orbiplex Node` is the primary runtime component of the system. It participates in protocol flows, enforces room and policy constraints, preserves provenance, and acts as the main bridge between network-facing protocol semantics and local execution.

Node-scoped roles such as archivist, memarium provider, or sensorium provider are not assumed to be in-process features of a single monolith. They may be implemented as separate programs or processes, written in different languages, as long as they attach to the Node through explicit protocol and API contracts.

## Purpose

The Node is responsible for the solution-level execution path of:
- peer identity, handshake, and endpoint discovery,
- question room lifecycle,
- federated answer procurement,
- local learning and knowledge promotion,
- archival handoff and retrieval,
- optional transcript observation and later curation/training handoff.

## Scope

This document defines solution-level responsibilities of the Node component.

It does not define:
- concrete module layout in an implementation repository,
- implementation details of Node-attached plugin or process roles,
- rich end-user UI,
- protocol-external payment execution,
- default direct mutation of base models.

## Must Implement

### Peer Identity, Discovery, and Session Baseline

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/50-requirements/requirements-006.md`

Related schemas:
- `node-identity.v1`
- `node-advertisement.v1`
- `peer-handshake.v1`
- `capability-advertisement.v1`

Responsibilities:
- generate or load a stable local node identity,
- derive and expose a stable `node-id`,
- publish or consume signed endpoint advertisements,
- establish signed peer handshakes and capability exchange over the baseline transport,
- maintain keepalive and reconnect behavior for the first networked Node baseline.

Status:
- `todo`

### Question Room Lifecycle

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/50-requirements/requirements-001.md`

Related schemas:
- `question-envelope.v1`
- `answer-room-metadata.v1`
- `response-envelope.v1`

Responsibilities:
- open or bind a room to `question/id`,
- enforce exposure mode and room policy profile,
- preserve provenance across room outputs.

Status:
- `todo`

### Federated Answer Procurement

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/50-requirements/requirements-001.md`

Related schemas:
- `procurement-offer.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:
- collect and evaluate offers,
- select responders under policy,
- record contracts and receipts without coupling protocol semantics to crypto rails.

Status:
- `todo`

### Local Learning and Knowledge Promotion

Based on:
- `doc/project/30-stories/story-002.md`
- `doc/project/50-requirements/requirements-002.md`

Related schemas:
- `learning-outcome.v1`
- `knowledge-artifact.v1`

Responsibilities:
- classify outcomes as `confirmed`, `corrected`, or `unresolved`,
- promote only policy-accepted outcomes,
- keep unresolved material out of trusted retrieval by default.

Status:
- `todo`

### Archivist and Vault Handoff

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`
- `doc/project/50-requirements/requirements-003.md`

Related schemas:
- `archival-package.v1`
- `archivist-advertisement.v1`
- `retrieval-request.v1`
- `retrieval-response.v1`

Responsibilities:
- prepare archival packages,
- select archivists under policy,
- preserve publication scope, integrity, and retrieval provenance.

Status:
- `todo`

## May Implement

### Transcript Monitoring

Based on:
- `doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

Related schemas:
- `transcript-segment.v1`
- `transcript-bundle.v1`

Responsibilities:
- observe only policy-allowed traffic,
- preserve consent and human-origin semantics,
- emit transcript artifacts suitable for curation.

Status:
- `optional`

## Consumes

- `question-envelope.v1`
- `retrieval-response.v1`
- `archivist-advertisement.v1`

## Produces

- `answer-room-metadata.v1`
- `response-envelope.v1`
- `learning-outcome.v1`
- `knowledge-artifact.v1`
- `archival-package.v1`

## Related Capability Data

- `node-caps.edn`

## Notes

Implementation-specific decomposition, file ownership, and delivery status belong in the concrete Node repository.

Role components attached to the Node may live in separate repositories, runtimes, or processes. This document defines what the Node must coordinate and expose, not that every role must be compiled into one binary.
