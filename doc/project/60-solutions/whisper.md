# Orbiplex Whisper

`Orbiplex Whisper` is a Node-attached solution component for privacy-bounded social-signal exchange. It prepares rumor-style signals for publication, preserves their weaker epistemic status, and coordinates thresholded association bootstrap without silently escalating rumors into evidence.

`Whisper` does not own transport anonymity. It only declares routing and privacy intent on outgoing artifacts and relies on Node egress to satisfy that intent through whatever outbound privacy capability is available.

## Purpose

The component is responsible for the solution-level execution path of:
- rumor intake and local preparation,
- redaction, paraphrase, and idiolect flattening with user approval,
- publication of bounded `whisper-signal` artifacts,
- reception of interest signals,
- threshold recognition,
- and bootstrap of opt-in association rooms.

## Scope

This document defines solution-level responsibilities of the Whisper component.

It does not define:
- concrete module layout in an implementation repository,
- the implementation of transport privacy or onion-like relay,
- final evidentiary case management,
- automatic human enrollment into shared rooms,
- semantic duplicate detection for rumors in v1.

## Must Implement

### Rumor Intake and Publication

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-signal.v1`

Responsibilities:
- capture rumor-style input without flattening it into evidence,
- run bounded local redaction and idiolect-reduction workflows,
- require user approval before publication,
- emit `whisper-signal` artifacts with explicit epistemic class, node-scoped
  routing, nym-authored pseudonymous participation, attached `nym-certificate`,
  and routing/privacy intent.

Status:
- `todo`

### Interest and Threshold Coordination

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

Responsibilities:
- register local relevance without premature disclosure,
- recognize threshold crossings under policy,
- derive deterministic bootstrap sets,
- publish association proposals that preserve opt-in enrollment.

Status:
- `todo`

## May Implement

### Aggregate Topic Notices

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-threshold-reached.v1`

Responsibilities:
- emit coarse aggregate notices after threshold crossing,
- keep those notices weaker than case disclosure,
- separate aggregate discovery hints from raw rumor exchange.

Status:
- `optional`

## Out of Scope

- transport-layer anonymity and relay topology
- final governance or adjudication
- automatic exposure of identities to one another
- hard semantic duplicate suppression in v1

## Consumes

- `whisper-signal.v1`
- `whisper-interest.v1`

## Produces

- `whisper-signal.v1`
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

## Related Capability Data

- `whisper-caps.edn`

## Notes

Whisper may be implemented as an in-process module or as a separate program/process attached to Node through explicit contracts. Its solution role is stable either way.

When `Monus` is present, Whisper should treat it as an upstream local draft
preparation module rather than as a peer publication authority. Monus may prepare
candidate concern drafts, but Whisper and the host still own the bounded outgoing
publication path.
