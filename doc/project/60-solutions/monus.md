# Orbiplex Monus

`Orbiplex Monus` is a Node-attached local observation middleware focused on
wellbeing, tension, and weak-signal preparation. It is not a protocol authority.

Its proper role is:

- observe admitted local signals,
- weigh them over time,
- prepare candidate concern drafts or recommendations,
- and rely on host-granted capability contracts for memory access, model help,
  and bounded publication requests.

`Monus` does not own transport egress. It does not directly publish outgoing
social-signal artifacts on the network.

## Purpose

The component is responsible for the solution-level execution path of:

- local wellbeing/tension observation,
- bounded aggregation of admitted local signals,
- candidate concern or rumor draft preparation,
- and handoff into Whisper-side review or publication requests.

## Scope

This document defines solution-level responsibilities of the Monus component.

It does not define:

- a dedicated Monus wire protocol,
- unrestricted access to Node memory or storage,
- direct transport egress,
- acute emergency activation logic as a replacement for emergency/help paths,
- one fixed scoring or wellbeing algorithm.

## May Implement

### Local Signal Weighting and Draft Preparation

Based on:
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/30-stories/story-005.md`
- `doc/project/40-proposals/022-monus-as-host-granted-local-observation-middleware.md`

Related schemas:
- `whisper-signal.v1`

Responsibilities:
- aggregate admitted local weak signals over time,
- keep the distinction between user-authored and middleware-derived concern drafts,
- prepare candidate concern drafts or explicit do-not-publish recommendations,
- preserve `monus-derived` and `monus-sensorium-derived` provenance for later
  Whisper publication.

Status:
- `todo`

### Host-Granted Capability Consumption

Based on:
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/022-monus-as-host-granted-local-observation-middleware.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/50-requirements/requirements-013.md`

Related schemas:
- none frozen yet

Responsibilities:
- consume only host-granted memory, signal, and draft-shaping capabilities,
- degrade gracefully when some capability grants are absent,
- submit bounded publication requests through Node or Whisper contracts instead of
  direct transport egress,
- keep capability use inspectable and auditable from the host side.

Status:
- `todo`

## Out of Scope

- direct network publication of `whisper-signal.v1`
- unrestricted memory access
- direct vendor/model side channels bypassing Node
- replacing emergency/help activation flows

## Consumes

- host-granted local memory or read-model views
- host-granted local signal summaries
- host-granted model-assisted draft-shaping services

## Produces

- local concern drafts
- local recommendation records
- bounded publication requests aimed at Whisper-side processing

## Related Capability Data

- `monus-caps.edn`

## Notes

Monus should fit naturally into the same supervised middleware surface as other
Node-attached modules, but unlike Dator or Arca it is not a marketplace or
workflow module. Its primary value lies in local-first interpretation under a
strict host boundary.
