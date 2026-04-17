# Proposal 026: Resource Opinions and Discussion Surfaces

Based on:
- `doc/project/20-memos/resource-opinions-and-discussion.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/20-memos/orbiplex-whisper.md`

## Status

Accepted; hard-MVP `resource-opinion.v1` content schema and Agora/node-ui
compose path implemented. Rich discussion surfaces remain future work.

## Date

2026-04-10

## Executive Summary

Orbiplex has subject-oriented trust and signal concepts. This proposal defines
the portable hard-MVP way for participants to express opinions about arbitrary
resources such as:

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
3. subject identity, authorship, and timing are carried by the
   enclosing envelope (`agora-record.v1` `record/about[0]`,
   `author/participant-id`, `authored/at`); `resource-opinion.v1`
   itself is a content-body schema and does **not** duplicate those
   fields,
4. one opinion contains `opinion/text` and may add `opinion/lang`,
   `opinion/tags`, and a coarse `opinion/rating` in `-1|0|1`,
5. resource opinion artifacts remain distinct from participant or
   node reputation,
6. a later discussion surface may attach to the same canonical
   resource key, but discussion threads and forum semantics are not
   part of the hard-MVP opinion artifact.

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

The MVP artifact for a participant-authored opinion is the content body
of an `agora-record.v1` envelope:

- `schema = "resource-opinion.v1"`

#### 2.1. Envelope vs content separation

When a resource opinion is published on the Agora substrate (the MVP
transport, see proposal 035 and requirements-014 FR-001/FR-002/FR-011),
identity, authorship, timing, subject reference, and the canonical
record identifier live in the **envelope** (`agora-record.v1`), not in
the content body:

| Concern | Where it lives |
|---|---|
| subject of the opinion | envelope `record/about[0] = {resource/kind, resource/id}` |
| authoring participant | envelope `author/participant-id` |
| authoring timestamp | envelope `authored/at` |
| canonical record identifier | envelope `record/id` (derived from canonical signed bytes) |
| signature | envelope `signature` |
| topic routing | envelope `topic/key` (conventionally `opinions/<resource-kind>`) |

The envelope's `content` object, validated by `resource-opinion.v1`,
carries **only the verbal and scalar expression** of the opinion. This
keeps the substrate layer open on `resource/kind` (the envelope accepts
any value matching the `resource-ref.v1` shape) while the opinion
content stays a small, portable shape independent of how identity is
routed.

#### 2.2. Content-body fields

Recommended minimum fields of `resource-opinion.v1`:

- `schema`
- required `opinion/text`
- optional `opinion/lang`
- optional `opinion/rating`
- optional `opinion/tags`

Ingest invariants (applied to the content body only):

1. `opinion/text` MUST be a non-empty string.
2. `opinion/rating`, when present, MUST be one of `-1`, `0`, or `1`.
3. `opinion/lang`, when present, annotates `opinion/text`.
4. `opinion/tags`, when present, is an array of non-empty strings.

Invariants tied to envelope fields (enforced by the envelope
contract, not by `resource-opinion.v1`):

5. envelope `record/about` MUST contain at least one
   `{resource/kind, resource/id}` entry; the first entry is treated as
   the primary subject for indexing and aggregation
6. envelope `author/participant-id` MUST identify the immediate
   authoring participant
7. consumers MUST NOT split `resource/key` derived from envelope fields
   on any `:` other than the first one

#### 2.3. Standalone (non-envelope) usage

For archival exports, off-line snapshots, or bridges to systems that
do not carry the Agora envelope, a receiver MAY present the opinion as
a flat object that inlines the envelope-native fields (`resource/kind`,
`resource/id`, optional `resource/key`, `author/participant-id`,
`authored/at`, `record/id`) alongside the content body. That flat form
is a **projection** of the envelope plus content, not a second
authoritative schema; it does not gain fields that the envelope does
not already carry.

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

A resource opinion as it travels through the Agora substrate — one
`agora-record.v1` envelope carrying a `resource-opinion.v1` content
body. The envelope holds identity and routing; the content body holds
the opinion itself.

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:4b7c9fzkMyAL8GBfQExampleRecordId00000000000000",
  "record/kind": "opinion",
  "topic/key": "opinions/url",
  "record/about": [
    {
      "resource/kind": "url",
      "resource/id": "https://example.org/article"
    }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-10T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Useful overview, but the sourcing is thin in the final section.",
    "opinion/lang": "en",
    "opinion/rating": 1
  },
  "signature": {
    "alg": "ed25519",
    "value": "sig_example_opinion_url_article_0001"
  }
}
```

The same opinion published about a non-URL subject reuses the same
content body shape and swaps only the envelope's `record/about[0]` and
`topic/key`:

```json
{
  "schema": "agora-record.v1",
  "record/kind": "opinion",
  "topic/key": "opinions/ean",
  "record/about": [
    { "resource/kind": "ean", "resource/id": "5901234123457" }
  ],
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Solid packaging, product matched the description.",
    "opinion/rating": 1
  }
}
```

This illustrates why substrate layers (ingest, query, subject-index,
topic ACL) stay open on `resource/kind`: a new kind adds no new
content-body schema and no new relay surface.

## MVP Read-Model Consequences

The minimum read-models implied by this proposal are:

- list opinions by exact `resource/key`, resolved from the envelope's
  `record/about[0]`,
- list opinions by envelope `author/participant-id`,
- compute simple aggregates such as opinion count and average rating
  where ratings exist.

All three read-models are built over envelope fields plus the
`resource-opinion.v1` content body; no read-model reads identity out
of the content body.

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
- envelope-vs-content layering keeps `resource-opinion.v1` content-body
  shape independent of how identity, authorship, and routing are
  carried, so the same content schema works across Agora relays,
  archival exports, and future transports,
- and a clear extension seam for later discussion surfaces.

Tradeoffs:

- `resource/kind` remains semi-open and may require later normalization
  work,
- the proposal intentionally leaves moderation and deduplication
  unresolved,
- `resource/key` is derived rather than authoritative, so consumers
  must validate it instead of trusting it blindly,
- and implementers must remember that subject identity is **not** in
  the content body — any tool that reads opinions must read from the
  envelope's `record/about[0]`, not from `resource-opinion.v1` fields,
  which intentionally no longer carry them.

## Follow-Up

If adopted, the next artifacts should be:

1. one schema for `resource-opinion.v1`,
2. one requirements note for normalization and revision policy,
3. optionally one separate proposal for attached resource forum or channel
   semantics,
4. proposal 040 (custodial redelivery and tombstones) covers how opinions
   survive relay data loss and how participants place copies with other
   nodes under capability-passport-backed custody; opinion-specific
   retention or right-to-forget flows build on that substrate.
