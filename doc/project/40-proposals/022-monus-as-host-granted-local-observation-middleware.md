# Proposal 022: Monus as Host-Granted Local Observation Middleware

Based on:
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/50-requirements/requirements-010.md`

Date: `2026-03-30`
Status: Draft

## Context

`Orbiplex Monus` is currently present only as a memo-level concept and as a source
classification hook inside `whisper-signal.v1`.

That is enough to preserve semantic room for a future local wellbeing-observation
module, but not enough to implement it cleanly.

The main architectural risk is splątanie:

- local observation,
- memory access,
- model-assisted draft shaping,
- policy enforcement,
- and social-signal publication

could collapse into one implicit plugin if the host boundary remains vague.

## Decision

`Orbiplex Monus` should be implemented as a supervised Node-attached middleware
module, preferably through the same `http_local_json` attachment surface already
used for bundled middleware.

`Monus` is not the protocol authority for outgoing social-signal publication.
Instead:

1. `Monus` consumes host-granted capabilities exposed by `Orbiplex Node`,
2. `Monus` prepares local drafts, recommendations, or concern summaries,
3. `Node` remains the authority that grants memory/model/signal access,
4. `Whisper` remains the bounded publication layer for outgoing social signals.

## Goals

- keep `Monus` local-first,
- prevent side-channel publication or hidden memory access,
- preserve explicit responsibility boundaries between `Monus`, `Node`, and
  `Whisper`,
- make future implementation possible without inventing a separate Monus-specific
  wire protocol.

## Non-Goals

- defining a new network artifact family for Monus in hard MVP,
- making `Monus` itself a transport or publication authority,
- forcing every Node deployment to include `Monus`,
- freezing one specific wellbeing scoring algorithm.

## Proposed Model

### 1. Role split

- `Sensorium` or other local signal providers supply local observations.
- `Monus` aggregates and weighs admitted local signals.
- `Node` exposes bounded capability contracts and owns policy enforcement.
- `Whisper` publishes bounded outgoing social-signal artifacts if policy allows it.

### 2. Host-granted capability model

`Monus` should consume explicit host-granted capabilities rather than ambient
access to local state.

The first useful capability families are:

- bounded local memory or read-model queries,
- bounded local signal ingestion,
- bounded model-assisted draft shaping,
- local audit/event emission,
- request submission for Whisper-side review or publication.

Each deployment may grant a subset only.

### 3. Publication boundary

`Monus` may prepare:

- a local concern draft,
- a candidate Whisper draft,
- or a recommendation not to publish.

But `Monus` should not directly push outgoing `whisper-signal.v1` traffic to the
network. Publication remains Node-owned and Whisper-mediated.

### 4. Trace and accountability

When an outgoing social signal is materially prepared by Monus, the resulting
`whisper-signal.v1` should preserve that provenance through:

- `source/class = monus-derived`
- or `source/class = monus-sensorium-derived`

The local host should also retain an audit trace that the draft was middleware-
assisted rather than purely user-authored.

## Trade-offs

### Benefits

- preserves stratyfikacja between observation, preparation, and publication,
- reuses existing middleware hosting work,
- allows Monus to be implemented in Python or another language without changing
  the protocol core,
- keeps the trusted host boundary small and auditable.

### Costs

- requires explicit capability contracts from the host,
- adds one more attached-module surface to supervise,
- leaves some Monus behavior local and implementation-defined until later
  requirements narrow it further.

## Open Questions

1. Which local memory surfaces should Monus be allowed to query directly, and
   which only through pre-filtered host views?
2. Should the first Monus baseline emit its own local draft artifact, or only
   in-memory middleware decisions?
3. Which capability grants should be mandatory for a Node deployment claiming
   Monus support?
4. How should acute emergency patterns be split between Monus, Sensorium, and
   emergency/help flows?

## Next Actions

1. Add requirements for host-granted capability contracts and publication
   boundaries.
2. Add a dedicated Monus solution component under `60-solutions`.
3. Record in Node solution docs that Monus is a future supervised middleware
   consumer of host-granted memory/model/publication contracts.
