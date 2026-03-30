# Requirements 013: Monus as Host-Granted Local Observation Middleware

Based on:
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/022-monus-as-host-granted-local-observation-middleware.md`
- `doc/project/50-requirements/requirements-010.md`

Date: `2026-03-30`
Status: Draft

## Executive Summary

`Orbiplex Monus` is defined as a local Node-attached middleware module that may
observe admitted local signals and prepare candidate social-signal drafts, but
only through host-granted capability contracts.

The key boundary is:

- `Monus` may observe and prepare,
- `Node` grants bounded access and enforces policy,
- `Whisper` remains the bounded publication layer.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MAY support `Orbiplex Monus` as a supervised Node-attached middleware module. | Fact | Proposal 022 |
| FR-002 | A Node claiming Monus support MUST expose Monus only through explicit host-granted capability contracts rather than through ambient unrestricted access to local state. | Fact | Proposal 022 |
| FR-003 | Host-granted Monus capability contracts MUST remain separately grantable for memory/read-model access, local signal intake, model-assisted draft shaping, audit emission, and publication requests. | Fact | Proposal 022 |
| FR-004 | `Monus` MUST be able to operate with only a subset of those host-granted capabilities when deployment policy does not grant the full set. | Fact | Proposal 022 |
| FR-005 | `Monus` MUST NOT directly publish outbound `whisper-signal.v1` artifacts onto the network without Node-owned validation and egress. | Fact | Proposal 022 + Proposal 013 |
| FR-006 | `Monus` MAY prepare local concern drafts, candidate Whisper drafts, or explicit do-not-publish recommendations. | Fact | Proposal 022 |
| FR-007 | When an outgoing `whisper-signal.v1` was materially prepared by Monus, the publication path MUST preserve `source/class = monus-derived` or `monus-sensorium-derived` as appropriate. | Fact | Proposal 013 + Proposal 022 |
| FR-008 | `Monus` MUST preserve the distinction between purely user-authored rumor input and middleware-derived rumor preparation. | Fact | Memo + Proposal 022 |
| FR-009 | A Monus-capable Node SHOULD retain local audit trace indicating which host-granted capabilities were used in preparing a candidate concern or publication request. | Inference | Proposal 022 |
| FR-010 | If a deployment grants Monus memory/query access, that access MUST remain bounded by admitted local scopes rather than unrestricted access to all local storage. | Fact | Proposal 022 |
| FR-011 | If a deployment grants Monus model-assisted draft shaping, the draft-shaping path MUST remain host-owned and policy-visible rather than allowing direct vendor side channels from Monus. | Fact | Proposal 022 + Requirements 010 |
| FR-012 | If a deployment grants Monus publication-request capability, the request path MUST target a Node-owned or Whisper-owned review/publication contract rather than direct transport egress. | Fact | Proposal 022 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | The Monus integration surface SHOULD preserve stratyfikacja between local observation, host capability grants, and bounded social-signal publication. | Fact | Project values + Proposal 022 |
| NFR-002 | Monus support MUST remain optional at deployment level and MUST NOT be assumed by the core Node transport or procurement baseline. | Fact | Proposal 022 |
| NFR-003 | Host-granted Monus capabilities SHOULD be inspectable by operators as explicit configuration or capability-report state rather than hidden middleware assumptions. | Inference | Operability |
| NFR-004 | A future Monus implementation MAY be written in Python or another language as long as it attaches through the supervised middleware surface and honors the host capability contracts. | Fact | Proposal 022 + Proposal 019 |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Monus silently reads more local state than intended | Hidden privacy violation and broken trust boundary | Require explicit host-granted capability contracts and bounded local scope for memory/query access. |
| Monus publishes directly through transport without host validation | Unbounded rumor publication and broken accountability | Keep transport egress Node-owned and Whisper-mediated. |
| Monus calls external model vendors directly | Hidden side channel and audit gap | Require host-owned model-assisted draft-shaping path. |
| Deployment grants only partial capability set | Feature brittleness | Require Monus to degrade gracefully under partial host grants. |
