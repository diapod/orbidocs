# Orbiplex Node UI

`Orbiplex Node UI` is a thin control and inspection client for the Node component. It is not the protocol source of truth; it is an operator-facing surface that consumes Node APIs and exposes bounded control, diagnostics, and visibility.

## Purpose

The Node UI exists to:
- inspect Node state and protocol flows,
- expose safe operator controls,
- present provenance and policy context without re-implementing protocol semantics,
- adapt to different host environments as thin clients.

## Scope

This document defines solution-level responsibilities of the Node UI component.

It does not define:
- network protocol semantics,
- canonical persistence of protocol artifacts,
- training or archival logic as a source of truth,
- one fixed UI toolkit or deployment shell.

## Must Implement

### Node Control Surface

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/20-memos/pod-backed-thin-clients.md`

Related schemas:
- `answer-room-metadata.v1`
- `response-envelope.v1`

Responsibilities:
- expose bounded controls for room participation and answer review,
- show enough room metadata for an operator to understand scope and policy,
- avoid becoming a second protocol authority beside the Node.

Status:
- `todo`

### Provenance and Policy Inspection

Based on:
- `doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

Related schemas:
- `transcript-segment.v1`
- `transcript-bundle.v1`
- `learning-outcome.v1`

Responsibilities:
- render provenance and human-origin markers in operator-visible views,
- expose policy and scope information without flattening semantics,
- make unresolved and quarantined states clearly distinguishable.

Status:
- `todo`

## May Implement

### Archivist and Retrieval Views

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/50-requirements/requirements-003.md`

Related schemas:
- `archival-package.v1`
- `retrieval-request.v1`
- `retrieval-response.v1`

Responsibilities:
- show archival status and retrieval metadata,
- provide bounded operator affordances for archival handoff and retrieval inspection.

Status:
- `optional`

## Consumes

- `answer-room-metadata.v1`
- `response-envelope.v1`
- `learning-outcome.v1`
- `archival-package.v1`
- `retrieval-response.v1`

## Produces

- no canonical protocol artifacts by default

## Related Capability Data

- `node-ui-caps.edn`

## Notes

Different host-specific clients may exist for desktop, browser, terminal, or pod-backed thin-client contexts, but they should remain thin surfaces over Node behavior.
