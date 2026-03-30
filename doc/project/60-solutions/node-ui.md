# Orbiplex Node UI

`Orbiplex Node UI` is a thin control and inspection client for the Node component. It is not the protocol source of truth; it is an operator-facing surface that consumes Node APIs and exposes bounded control, diagnostics, and visibility.

## Purpose

The Node UI exists to:
- inspect Node state and protocol flows,
- expose safe operator controls,
- present provenance and policy context without re-implementing protocol semantics,
- present settlement policy health and disclosure trail context for paid flows,
- adapt to different host environments as thin clients.

## Scope

This document defines solution-level responsibilities of the Node UI component.

It does not define:
- network protocol semantics,
- canonical persistence of protocol artifacts,
- training or archival logic as a source of truth.

## Architecture Direction

The chosen hard-MVP implementation direction is recorded in:

- `doc/project/20-memos/node-ui-htmx-hateoas-architecture.md`

In summary: the Node UI is a thin HTMX web client backed by a server-side
template renderer (`node-ui` crate, Rust + Axum + MiniJinja) that proxies the
daemon HTTP control API and renders HTML fragments. HATEOAS is the navigational
model. The daemon remains the sole authority; the web server holds no protocol
state.

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
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

Responsibilities:
- render provenance and human-origin markers in operator-visible views,
- expose policy and scope information without flattening semantics,
- make unresolved and quarantined states clearly distinguishable,
- render settlement policy degradation, suspension, and manual-review conditions before an operator commits to a paid path.

Status:
- `todo`

### Settlement Policy Inspection

Based on:
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/50-requirements/requirements-007.md`
- `doc/project/50-requirements/requirements-008.md`

Related schemas:
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:
- show the active settlement policies attached to a paid procurement path,
- surface recent settlement disclosure events with their scope and impact mode,
- let the operator inspect why a paid path is blocked, degraded, or forced into manual review,
- preserve audit joins from procurement contracts and receipts back to their governing settlement policies.

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
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

## Produces

- no canonical protocol artifacts by default

## Related Capability Data

- `node-ui-caps.edn`

## Notes

Different host-specific clients may exist for desktop, browser, terminal, or pod-backed thin-client contexts, but they should remain thin surfaces over Node behavior.

Settlement inspection belongs in the UI because operators need a bounded view of
why paid actions are available, delayed, or suspended. The UI still must not
become an independent settlement authority.
