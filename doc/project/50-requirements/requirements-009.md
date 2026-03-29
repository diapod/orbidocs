# Requirements 009: Layered `capability_limited` Participant Restrictions

Based on:
- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/50-requirements/requirements-006.md`
- `doc/normative/30-core-values/en/CORE-VALUES.en.md`
- `doc/normative/50-constitutional-ops/en/UNIVERSAL-BASIC-COMPUTE.en.md`

Date: `2026-03-29`
Status: Draft (participant restriction baseline)

## Executive Summary

This document defines the first implementation-facing requirements for
participant-scoped layered restriction state under the frozen
`capability_limited` label.

The MVP baseline must support:

- always-on soft degradation factors,
- optional hard blocked operations,
- explicit authorship and expiry for hard blocks,
- a protected non-blockable floor,
- and the first narrow Node enforcement hooks.

## Context and Problem Statement

Transport already has a peer-quality downgrade path. What it does not yet have is
one canonical participant-facing restriction artifact that can:

- narrow privileged operations without cutting the participant off from the
  network,
- keep soft and hard effects separate,
- anchor hard restrictions in a named authority and review basis,
- and keep sanctions bounded in time.

Without this contract, sanction behavior remains partly implicit and partly mixed
into peer state that was never meant to carry all operation-level semantics.

## Proposed Model / Decision

### Canonical Artifact

The canonical MVP artifact family is:

- `participant-capability-limits.v1`

The artifact is participant-scoped and freezes:

- `status = capability_limited`
- mandatory `soft.priority-factor`
- mandatory `soft.rate-limit-factor`
- optional `hard.blocked-operations`
- optional `hard.reason/ref`
- optional `hard.decision/author`
- optional `hard.expires-at`

### Protected Floor

The MVP baseline treats the following operations as non-blockable through this
artifact:

- `core/messaging`
- `keepalive`
- `dispute/file`
- `ubc/claim`
- `signal-marker/send`

### First Runtime Hooks

The first Node rollout should:

- reject `procurement/request` when hard-blocked,
- reject `procurement/offer` when hard-blocked,
- preserve `signal-marker/send` as an explicitly allowed path,
- consume `soft.priority-factor` as a procurement-ranking penalty,
- and consume `soft.rate-limit-factor` through a deterministic per-participant
  cooldown on the first admitted daemon operations.

Broader governor policies remain later work, but the field itself is no longer
paper-only.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST support a canonical participant restriction artifact `participant-capability-limits.v1`. | Fact | Proposal 018 |
| FR-002 | `participant-capability-limits.v1` MUST be participant-scoped and require canonical `participant/id = participant:did:key:...`. | Fact | Proposal 018 |
| FR-003 | The artifact MUST freeze exactly one MVP state label: `status = capability_limited`. | Fact | Proposal 018 |
| FR-004 | The artifact MUST require a `soft` layer with `priority-factor` and `rate-limit-factor`, each normalized to `(0.0, 1.0]`. | Fact | Proposal 018 |
| FR-005 | The artifact MAY carry a `hard` layer, but if present it MUST require non-empty `blocked-operations`, `reason/ref`, `decision/author`, and `expires-at`. | Fact | Proposal 018 |
| FR-006 | `decision/author` in the hard layer MUST be an accountable canonical subject id in MVP; at minimum `participant:did:key:...`, `org:did:key:...`, and `council:did:key:...` MUST be admitted. | Fact | Proposal 018 |
| FR-007 | `hard.blocked-operations` MUST remain an open operation namespace rather than a closed enum of transport capabilities. | Fact | Proposal 018 |
| FR-008 | `hard.blocked-operations` MUST NOT admit `core/messaging`, `keepalive`, `dispute/file`, `ubc/claim`, or `signal-marker/send`. | Fact | Proposal 018 |
| FR-009 | The first Node runtime enforcement MUST reject `procurement/request` when the asking participant carries an active hard block for that operation. | Fact | Proposal 018 |
| FR-010 | The first Node runtime enforcement MUST reject `procurement/offer` when the responder participant carries an active hard block for that operation. | Fact | Proposal 018 |
| FR-010a | The first expanded Node runtime enforcement MUST reject `response/deliver` when the responding participant carries an active hard block for that operation. | Fact | Proposal 018 |
| FR-010b | The first expanded Node runtime enforcement MUST reject `response/accept` when the asking participant carries an active hard block for that operation. | Fact | Proposal 018 |
| FR-010c | The first expanded Node runtime enforcement MUST reject `response/reject` when the asking participant carries an active hard block for that operation. | Fact | Proposal 018 |
| FR-011 | The first Node runtime enforcement MUST keep `signal-marker/send` admissible even when the participant is otherwise `capability_limited`. | Fact | Proposal 018 |
| FR-012 | The first Node runtime SHOULD consume `soft.priority-factor` as a deterministic procurement-ranking penalty rather than ignoring the soft layer completely. | Fact | Proposal 018 |
| FR-013 | The first Node runtime MUST consume `soft.rate-limit-factor` through a deterministic per-participant operation cooldown for the first admitted daemon operations. | Fact | Proposal 018 |
| FR-014 | The first admitted daemon operation set for the generic cooldown hook MUST include at least `procurement/request`, `procurement/offer`, `response/deliver`, `response/accept`, `response/reject`, and `signal-marker/send`. | Fact | Proposal 018 |
| FR-015 | Participant restriction state MUST complement rather than replace transport-facing peer governor state. | Fact | Proposal 018 + Proposal 014 |
| FR-016 | Runtime traces and operator-visible diagnostics SHOULD make it possible to distinguish blocked privileged operations from protected floor operations and from cooldown rejections. | Inference | Proposal 018 + project values |
| FR-017 | Participant-side `response/accept` and `response/reject` MUST be exposed through a participant-scoped daemon control contract rather than through infrastructure-operator action endpoints. | Fact | Proposal 018 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Hard restrictions MUST stay time-bounded in MVP; sanction artifacts without expiry are inadmissible. | Fact | Proposal 018 |
| NFR-002 | The restriction artifact SHOULD remain small, append-only in spirit, and auditable without requiring a full governance subsystem rewrite. | Inference | Proposal 018 + project values |
| NFR-003 | Operation-level sanction semantics MUST stay separate from transport handshake capability semantics. | Fact | Proposal 018 |
| NFR-004 | The protected floor MUST preserve minimum dignity, communication, and appeal paths even when privileged operations are curtailed. | Fact | Proposal 018 + UBC + core values |
| NFR-005 | Soft degradation factors SHOULD be stable enough for deterministic ranking and later throttling, rather than host-local folklore. | Fact | Proposal 018 |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Transport peer downgrade is mistaken for participant sanction | Layer confusion and wrong enforcement target | Keep participant restriction in its own artifact and preserve peer governor as a separate layer. |
| A hard restriction blocks communication or appeal | De facto exile under a lighter procedure | Freeze a protected non-blockable floor and reject such artifacts at schema level. |
| Sanction author is implicit or anonymous | Accountability dissolves into process folklore | Require `decision/author` and `reason/ref` on every hard block. |
| Hard restriction never expires | Temporary measure becomes silent ban | Require `expires-at` for every hard block. |
| Runtime ignores soft factors entirely | `capability_limited` becomes a paper state with no practical effect | Require both a ranking penalty and a deterministic cooldown hook in the first Node rollout. |

## Open Questions

1. When should `rate-limit-factor` become a generic throttle hook beyond procurement?
2. Should the initial cooldown grain stay at `(participant, operation)` or later move toward `(participant, operation, question)` for concurrent contracts?
3. Should a later rollout add a sibling org-scoped restriction artifact or generalize this one to `subject/kind`?
4. Which blocked operations should be elevated into a more formal registry first?
5. Which review or case artifact should become the long-term normative companion of this restriction record?

## Next Actions

1. Sync `participant-capability-limits.v1` into the Node protocol contract mirror.
2. Add Node-side import validation for the new artifact.
3. Wire the first procurement and messaging hooks against it.
4. Keep launcher-facing participant decision flows on a distinct control surface from operator actions.
4. Revisit generic throttling after the operation-facing governor grows beyond the first MVP hooks.
