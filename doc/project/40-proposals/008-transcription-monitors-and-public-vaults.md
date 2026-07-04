# Transcription Monitors, Archivists, and Public Vaults

Based on:
- `doc/project/20-memos/transcription-monitors-and-public-vaults.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`

## Status

Proposed (Draft)

## Date

2026-03-21

## Executive Summary

This proposal defines the role chain by which valuable swarm discussions become durable
cultural memory:

1. `transcription-monitor` nodes observe selected channels and preserve source
   transcripts,
2. `curator` or `secretary` functions redact, classify, and approve bundles,
3. `archivist` nodes receive approved bundles and publish them into federation or
   public vaults.

The key decision is that transcript preservation should be treated as an explicit,
policy-governed subsystem rather than an accidental side effect of room history.

## Context and Problem Statement

`003-question-envelope-and-answer-channel.md` defines how live debate happens, but not
how culturally valuable discussions become durable source memory without collapsing
into indiscriminate logging.

The project already assumes a learning flywheel:

- questions open live rooms,
- discussions produce transcript-worthy material,
- archivists preserve durable bundles,
- later synthesis and training nodes consume curated corpora.

Without an explicit operational model:

- transcript capture becomes inconsistent across nodes,
- archivists cannot reliably know what they may store,
- private rooms risk accidental over-export,
- later training and curation layers inherit weak provenance.

## Goals

- Define explicit roles for transcript observation, curation, and archival storage.
- Preserve source transcripts, not only summaries.
- Support private, federation-local, and public vault publication classes.
- Keep consent, redaction, and publication timing policy explicit.
- Prevent transcript preservation from becoming ambient surveillance.

## Non-Goals

- This proposal does not freeze final transcript schemas.
- This proposal does not define the full training pipeline.
- This proposal does not require every room to permit transcription.
- This proposal does not force immediate public publication of all preserved material.

## Decision

Orbiplex should adopt a three-role baseline for durable discussion memory:

1. `transcription-monitor`
2. `curator` / `secretary`
3. `archivist`

These roles may be co-located on one node, but their semantics must remain distinct.

At baseline:

1. a monitor MAY observe a room only under explicit room policy or visibility basis,
2. a monitor SHOULD preserve discussion as structured source transcript rather than
   summary-only output,
3. archival publication MUST pass through a curation or policy gate,
4. archivist publication scope MUST remain explicit (`federation-local` vs `public`),
5. transcript preservation and publication timing MUST be independently configurable.

## Proposed Model

### 1. Role chain

#### `transcription-monitor`

Purpose:

- detect valuable discussions,
- join or observe channels under policy,
- emit transcript segments and bundles with provenance.

Typical triggers:

- operator-configured topic interests,
- detected knowledge gap or culturally valuable discussion,
- explicit invitation from another node,
- federation policy for designated rooms.

#### `curator` / `secretary`

Purpose:

- classify transcript quality and sensitivity,
- apply or verify redaction,
- decide whether a bundle is retained privately, published federation-locally,
  published publicly, quarantined, or rejected.

#### `archivist`

Purpose:

- receive accepted bundles,
- store them durably,
- advertise retrieval and replication capability,
- expose vault material under declared publication scope.

Archivists replicate raw bundles and redacted bundles as separate artifacts under
separate policies. Raw and redacted material must not share one indistinct custody
surface; each artifact carries its own retention, access-control, and audit trail.

### 2. Preservation targets

Transcript preservation should retain:

- original `question_id` or channel id,
- participant and speaker segmentation,
- timestamps,
- provenance markers,
- uncertainty and redaction markers,
- integrity proof sufficient to detect tampering.

The baseline value is preserving how reasoning unfolded, not only what answer was
eventually accepted.

### 3. Publication scopes

Archival publication should distinguish at least:

- `private-retained` - preserved for bounded local or policy reasons, not published,
- `federation-vault` - available inside a federation or other bounded trust scope,
- `public-vault` - available to broader commons consumption.

Promotion between scopes is a meaningful state transition and should leave a trace.

### 4. Publication timing profiles

The system should support at least three publication timing profiles:

- `live-mirror` - transcript stream is mirrored in near real time under explicit room
  policy,
- `delayed-bundle` - transcript is published only after room closure or TTL expiry,
- `curator-gated` - transcript leaves the room only after review, redaction, and
  approval.

`curator-gated` should be the safest default for high-sensitivity or human-linked
material.

`live-mirror` outside tightly scoped rooms is allowed only for emergency profiles or
explicitly public event profiles. The room must make live onward transmission visible
before it starts.

### 5. Selection and non-surveillance rule

Transcript preservation is not ambient logging.

The baseline rule should be:

- rooms may forbid transcription,
- rooms may allow transcript capture but forbid publication,
- rooms may allow publication only in redacted or delayed form,
- policy uncertainty should fail closed.

If a monitor cannot establish whether archival export is allowed, it may preserve only
the minimum internal evidence needed for later authorized review, not publish by
default.

Monitor observation always requires room-visible declaration. Federation policy may
authorize the monitor, but visibility is the participation and consent boundary.

## Trade-offs

1. Stronger cultural memory vs higher privacy burden:
   - Benefit: preserves reasoning paths and domain memory.
   - Cost: more policy and redaction complexity.
2. Dedicated roles vs operational simplicity:
   - Benefit: clearer responsibility and provenance.
   - Cost: more coordination between nodes.
3. Curator-gated publication vs immediate usefulness:
   - Benefit: safer publication and better quality.
   - Cost: slower release into vaults.

## Open Questions

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-04:

1. Live-mirror mode is allowed outside tightly scoped rooms only for emergency
   profiles or explicitly public event profiles. The room must make live onward
   transmission visible before it begins.
2. Archivists replicate raw bundles and redacted bundles as separate artifacts
   under separate policies. Raw and redacted material must not share one
   indistinct custody surface.
3. Public-vault promotion requires a minimum `2-of-3` curator quorum. A single
   curator is insufficient for default public promotion.
4. Monitor observation always requires a room-visible declaration. Federation
   policy may authorize the monitor, but visible declaration is the participation
   and consent boundary.

## Next Actions

1. Align transcript role semantics with `requirements-004-transcript-curation.md`.
2. Define publication-state vocabulary for transcript bundles and vault promotion.
3. Define archivist advertisement and replication contract, including separate raw
   and redacted artifact families under separate policies.
4. Define curator review and redaction workflow for public-vault promotion.
5. Define the `2-of-3` curator quorum contract for public-vault promotion; a single
   curator is insufficient for default public promotion.
6. Define the room-visible monitor declaration contract and fail-closed behavior when
   declaration or publication permission is missing.
