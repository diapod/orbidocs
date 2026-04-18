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
4. one opinion carries an optional `opinion/text` and may add
   `opinion/lang`, `opinion/tags`, a five-point `opinion/rating` in
   `1..5` (with `0` or absence meaning no rating), and relational
   fields (`opinion/in-reply-to`, `opinion/related`,
   `opinion/see-also`); the schema is also open to kind-specific
   namespaced extensions such as `rumor/credibility` and
   `rumor/rejection-reason`,
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
| topic routing | envelope `topic/key` (conventionally `ai.orbiplex.opinions/<resource-kind>`) |

The envelope's `content` object, validated by `resource-opinion.v1`,
carries **only the verbal and scalar expression** of the opinion. This
keeps the substrate layer open on `resource/kind` (the envelope accepts
any value matching the `resource-ref.v1` shape) while the opinion
content stays a small, portable shape independent of how identity is
routed.

#### 2.2. Content-body fields

Recommended minimum fields of `resource-opinion.v1`:

- `schema`
- optional `opinion/text`
- optional `opinion/lang`
- optional `opinion/rating`
- optional `opinion/tags`
- optional `opinion/subject-kind`
- optional `opinion/in-reply-to`
- optional `opinion/related`
- optional `opinion/see-also`

Ingest invariants (applied to the content body only):

1. `opinion/text`, when present, MUST be a non-empty string. An
   opinion MAY be text-less if it carries at least one of
   `opinion/rating`, `opinion/in-reply-to`, `opinion/related`,
   `opinion/see-also`, or a kind-specific extension key (see §2.4).
2. `opinion/rating`, when present, MUST be an integer in the range
   `0..5`. Values `1..5` encode a five-point scale where `1` is the
   weakest and `5` the strongest positive assessment. The value `0`
   is the explicit "no rating" marker and is semantically equivalent
   to the field being absent. Consumers MUST NOT silently rescale
   ratings to a different range or to a reputation signal.
3. `opinion/lang`, when present, annotates `opinion/text`.
4. `opinion/tags`, when present, is an array of non-empty strings.
5. `opinion/subject-kind`, when present, is a short string naming
   the kind of subject the opinion is about (e.g. `rumor`, `url`,
   `gps-location`, `public-person`, `ean`). It is a payload-level
   hint for selecting an overlay schema and does not replace
   envelope `record/about`.
6. `opinion/in-reply-to`, when present, is the `record/id` of
   another opinion the author is directly replying to. Consumers
   MUST tolerate dangling references.
7. `opinion/related`, when present, is an array of `record/id`
   values of other opinions this opinion relates to (prior takes,
   corroborating views, explicit contrasts). The relation is loose
   by design.
8. `opinion/see-also`, when present, is an array of 2-element
   vectors `[kind, id]` pointing at other opinable objects (URLs,
   rumors, resources, identities). Unlike `opinion/related`,
   entries are NOT restricted to opinions.

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

#### 2.4. Kind-specific extensions

`resource-opinion.v1` keeps `additionalProperties: true`. The core
schema is intentionally minimal; domain-specific fields live in
namespaced extension keys of the form `<kind>/<field>`, where
`<kind>` matches the `opinion/subject-kind` selector (when present)
or the kind of the primary entry in envelope `record/about`.

Rules:

1. Any field not named under the `opinion/*` namespace MUST carry a
   `<kind>/<field>` shape. Flat unprefixed extension keys are
   reserved for the core and MUST NOT be introduced by extensions.
2. Namespaces are flat strings (no nested `<kind>/<sub>/<field>`
   shapes). Multiple kinds MAY coexist on one opinion, but this is
   discouraged; the canonical pattern is one `opinion/subject-kind`
   plus one matching namespace.
3. Validation of extension keys is performed by an **overlay
   schema** registered separately from the core (e.g.
   `rumor-opinion.overlay.v1`). The overlay validates only its own
   namespace; it does not redefine `opinion/*` fields. Consumers
   without the overlay installed MUST still accept the envelope —
   unknown namespaced keys are forward-compatible.
4. Overlays MUST NOT change the meaning of any `opinion/*` field.
   In particular, `opinion/rating` always carries the five-point
   meaning defined in §2.2 regardless of kind. Kind-specific
   rating dimensions (e.g. `rumor/credibility`) live in the
   overlay namespace.

Concrete overlay defined as part of this proposal family:

- `rumor-opinion.overlay.v1` — used when `opinion/subject-kind`
  equals `rumor`. Fields:
  - `rumor/credibility` — integer `1..5` (optional). Orthogonal to
    `opinion/rating`; encodes an operator's assessment of how
    credible the rumor appears. `0` or absence means no credibility
    score.
  - `rumor/rejection-reason` — closed enum (optional). Recognized
    values: `spam`, `policy-violation`, `off-topic`, `abusive`,
    `duplicate`, `fabricated`. The presence of any value is a
    suppression signal for the node's outbound propagation policy
    (proposal 013 §Operator-mediated rumor curation).

Further overlays (e.g. `url-opinion.overlay.v1`,
`public-person-opinion.overlay.v1`, `gps-location-opinion.overlay.v1`)
may be added as separate artifacts without touching the core.

### 3. Verbal, Scalar, and Relational Opinion Are All First-Class

An opinion MAY be:

- verbal only (text + language),
- rating only (no text, just `opinion/rating`),
- relational only (no text, just `opinion/in-reply-to`,
  `opinion/related`, or `opinion/see-also`),
- kind-specific only (no text, just overlay fields such as
  `rumor/rejection-reason`),
- or any combination of the above.

This avoids splitting the first schema into separate text-review,
star-rating, and link-only artifacts while still allowing minimal
use cases such as:

- "I only want to rate this item 4/5",
- "I only want to leave a comment in Polish",
- "I want to mark this rumor as spam without writing anything",
- "I want both a text and a rating, plus a pointer to a related
  earlier opinion".

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
  "topic/key": "ai.orbiplex.opinions/url",
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
    "opinion/rating": 3
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
  "topic/key": "ai.orbiplex.opinions/ean",
  "record/about": [
    { "resource/kind": "ean", "resource/id": "5901234123457" }
  ],
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Solid packaging, product matched the description.",
    "opinion/rating": 4
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
