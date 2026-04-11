# Proposal 026: Resource Opinions and Discussion Surfaces

Based on:
- `doc/project/20-memos/resource-opinions-and-discussion.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/20-memos/orbiplex-whisper.md`

## Status

Draft

## Date

2026-04-10

## Executive Summary

Orbiplex currently has subject-oriented trust and signal concepts, but it does
not yet have one portable way for participants to express opinions about
arbitrary resources such as:

- a URL,
- a product identified by EAN,
- a node,
- an organization in the swarm,
- a place identified by GPS coordinates,
- a future publication artifact,
- or another externally referenceable object.

This proposal introduces a small MVP artifact:

- `resource-opinion.v1`

The key decisions are:

1. a target resource is identified by the pair `resource/kind` and
   `resource/id`,
2. the canonical derived key is `resource/kind + ":" + resource/id`,
3. one opinion may contain free text, a `lang`, and an optional `rating` in
   `1..5`,
4. resource opinion artifacts remain distinct from participant or node
   reputation,
5. a later discussion surface may attach to the same canonical resource key,
   but discussion threads and forum semantics are not part of the hard-MVP
   opinion artifact.

This keeps the core small:

- resource identity stays generic,
- opinion expression stays cheap,
- and richer discussion semantics can evolve later without forcing a large
  first schema.

## Context and Problem Statement

Orbiplex already has concepts for:

- subject identity,
- reputation-like signals,
- social-signal exchange,
- and protocol-visible publication artifacts.

What is missing is a resource-facing review layer.

Without such a layer:

- opinions about external resources remain application-local,
- there is no shared contract for simple review or recommendation traces,
- and any future resource discussion feature would have to invent its own
  target identity model from scratch.

The target resource may be heterogeneous. For example:

- `url:https://example.org/article`
- `ean:5901234123457`
- `node:node:did:key:z6MkExampleNode`
- `org:org:did:key:z6MkExampleOrg`
- `gps:51.107883,17.038538`

The identity model therefore must stay generic and must not assume one global
resource ontology.

## Goals

- Define one minimal portable artifact for participant-authored resource
  opinions.
- Freeze the resource identity rule using `resource/kind` and `resource/id`.
- Allow both verbal and scalar expression.
- Reserve a clean extension path for attached resource discussion surfaces.
- Keep the semantics separate from reputation and sanctions.

## Non-Goals

- This proposal does not define a final moderation model.
- This proposal does not define forum, channel, or threaded-comment schemas.
- This proposal does not define resource discovery, ranking, or recommendation
  algorithms.
- This proposal does not define one global registry of valid `resource/kind`
  values.
- This proposal does not define AI-agent delegation policy beyond preserving
  room for explicit authorship labeling in future discussion artifacts.

## Decision

### 1. Resource Identity

Every opinion target MUST be identified by:

- `resource/kind`
- `resource/id`

The canonical derived key is:

- `resource/key = resource/kind + ":" + resource/id`

Rules:

- `resource/id` MUST be treated as opaque within its kind,
- consumers MUST split `resource/key` only on the first `:`,
- and no consumer may assume that `resource/id` has URI semantics unless the
  kind contract explicitly says so.

This is necessary because some ids, such as URLs, already contain `:`.

Common early resource kinds MAY include:

- `url`
- `ean`
- `node`
- `org`
- `gps`

For `node` and `org`, `resource/id` should use canonical protocol-visible
identifiers. For `gps`, `resource/id` stays opaque in this proposal; a later kind
contract should freeze coordinate order, precision, and privacy rules.

### 2. `resource-opinion.v1` as the MVP Artifact

The MVP artifact for a participant-authored opinion is:

- `schema = "resource-opinion.v1"`

Recommended minimum fields:

- `schema`
- `opinion/id`
- `resource/kind`
- `resource/id`
- optional `resource/key`
- `author/participant-id`
- `authored/at`
- optional `body/text`
- optional `body/lang`
- optional `rating`
- optional `supersedes`

Ingest invariants:

1. `resource/key`, when present, MUST equal the derived composite key
2. `rating`, when present, MUST be an integer in `1..5`
3. at least one of `body/text` or `rating` MUST be present
4. `body/lang` MUST NOT appear without `body/text`
5. `author/participant-id` MUST identify the immediate authoring participant
6. `supersedes`, when present, points to one prior opinion artifact replaced by
   this revision

### 3. Verbal and Scalar Opinion Are Both First-Class

An opinion may be:

- verbal only,
- rating only,
- or verbal plus rating.

This avoids splitting the first schema into separate text-review and star-rating
artifacts while still allowing minimal use cases such as:

- "I only want to rate this item 4/5",
- "I only want to leave a comment in Polish",
- "I want both".

### 4. Resource Opinion Is Not Reputation

`resource-opinion.v1` MUST remain semantically separate from:

- `reputation-signal.v1`,
- participant assurance,
- sanctions,
- or governance incident records.

The distinction is:

- resource opinion attaches to an external or internal resource,
- reputation attaches to a subject such as a participant, node, org, or nym.

When `resource/kind` is `node` or `org`, the target is subject-addressable, but
the artifact is still an opinion about a resource view, not a
`reputation-signal.v1`. Consumers MUST NOT silently translate resource ratings
into subject reputation.

If a federation wants node or org opinions to affect reputation, it needs an
explicit policy and a separate reputation artifact or validation path.

### 5. Discussion Surface Is a Later Attached Layer

Future discussion surfaces may attach to the same resource identity through one
separate artifact family or registry entry, for example:

- `resource/channel-link.v1`
- `resource-forum-thread.v1`

Those are placeholders only. This proposal freezes only the layering rule:

1. resource identity is the stable base,
2. opinions are one append-only expression layer over that base,
3. richer discussion media may attach later without replacing the opinion
   artifact.

## Recommended Example

```json
{
  "schema": "resource-opinion.v1",
  "opinion/id": "opinion:resource:01JRCY0Y7T4Y9JQK8K7R6K4M3M",
  "resource/kind": "url",
  "resource/id": "https://example.org/article",
  "resource/key": "url:https://example.org/article",
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-10T08:15:00Z",
  "body/text": "Useful overview, but the sourcing is thin in the final section.",
  "body/lang": "en",
  "rating": 3
}
```

## MVP Read-Model Consequences

The minimum read-models implied by this proposal are:

- list opinions by exact `resource/key`,
- list opinions by `author/participant-id`,
- compute simple aggregates such as opinion count and average rating where
  ratings exist.

Hard-MVP consumers SHOULD tolerate:

- resources with no ratings and text only,
- resources with ratings and no text,
- multiple opinions over time from the same author when `supersedes` is not yet
  enforced by policy.

## Open Questions

- Should `resource/kind` remain semi-open forever, or should some kinds become
  schema-governed later?
- Should `node` and `org` resource opinions require explicit anti-harassment,
  appeal, or moderation rules before they appear in public aggregates?
- Should `gps` be represented as raw `lat,lon`, geohash, or a
  precision-bounded location key?
- Should one author have at most one active opinion per resource, with
  append-only revisions through `supersedes`?
- Should text and rating stay in one artifact family, or split when moderation
  policy becomes richer?
- Should the first attached discussion medium be ephemeral chat-like channels or
  archival forum threads?
- How should future discussion artifacts mark human-authored versus
  agent-authored contributions?

## Consequences

Positive:

- one small portable contract for resource review,
- clean separation from reputation,
- generic identity model reusable across many resource classes,
- and a clear extension seam for later discussion surfaces.

Tradeoffs:

- `resource/kind` remains semi-open and may require later normalization work,
- the proposal intentionally leaves moderation and deduplication unresolved,
- and `resource/key` is derived rather than authoritative, so consumers must
  validate it instead of trusting it blindly.

## Follow-Up

If adopted, the next artifacts should be:

1. one schema for `resource-opinion.v1`,
2. one requirements note for normalization and revision policy,
3. optionally one separate proposal for attached resource forum or channel
   semantics.
