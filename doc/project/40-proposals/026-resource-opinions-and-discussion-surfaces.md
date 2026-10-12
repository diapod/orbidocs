# Proposal 026: Resource Opinions and Discussion Surfaces

Based on:
- `doc/project/20-memos/resource-opinions-and-discussion.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/20-memos/orbiplex-whisper.md`

## Status

Accepted. P026-001–003 are implemented and runtime-qualified as of 2026-10-12:
shared open-reference authoring, pair-only opinion reads and recoverable domain
rebuild, with retained SQLite and Matrix evidence. Rich discussion surfaces and
Agora P17 navigation remain future work; this qualification does not establish
production readiness or cross-homeserver federation.

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

#### 1.1. Country-scoped identifier namespaces

A resource kind MAY name a country-scoped identifier namespace, using a
lower-case ISO 3166-1 alpha-2 country code followed by an unambiguous scheme
name, separated by hyphens: `<country>-<scheme>`. Where a scheme name alone
is ambiguous, include the registry qualifier, for example `pl-nil-pwz` for
PWZ numbers in the Polish Central Register of Physicians and Dentists.
This is an Orbiplex naming convention, not a claim that the resulting slug
is an official external identifier-system code.

For example, the resource reference and its derived key are:

```json
{
  "resource/kind": "pl-nil-pwz",
  "resource/id": "<pwz-number>"
}
```

```text
pl-nil-pwz:<pwz-number>
```

`<pwz-number>` is a documentation placeholder, not an issued or
domain-validated number. The example establishes the namespace convention;
it does not claim an implemented registry lookup or PWZ validator.

The following invariants preserve the generic resource contract:

- The entire `resource/kind` is the namespace key. Generic consumers MUST NOT
  infer authority or parse its hyphen-separated parts. Country qualifiers
  describe the identifier system's jurisdiction, not the holder's nationality,
  residence, or current location.
- Kinds remain an open catalogue. Operators and communities MAY propose new
  kind contracts; this convention neither introduces a global allow-list nor
  requires country prefixes for existing or international kinds. Unknown kinds
  remain opaque under the generic contract, subject to ordinary admission and
  disclosure policy; they MUST NOT be silently mapped to a familiar namespace.
- A kind contract MUST identify the relevant scheme/registry, what its values
  identify (for example a person, licence, organization, or registry entry),
  canonicalization and validation rules, and any known reassignment or alias
  semantics. Official namespace URIs/OIDs MAY be documented for interoperability;
  these are mappings, not additional fields required in every resource reference.
- Values remain strings. Country- and registry-specific normalization, check
  digits, and lookups belong to optional kind-specific validators or adapters,
  not the generic schema, Agora index, or core. Merely adding a `country` field
  cannot disambiguate the existing key, which uses only kind and id.
- Identifier equality establishes a shared reference within that namespace,
  not verified identity across namespaces, current professional entitlement,
  reputation, or the truth of a claim. Identifying a person through a public
  register does not itself authorize disclosure or public aggregation.

The design follows the namespace/value separation of
[FHIR Identifier](https://hl7.org/fhir/R5/datatypes.html#Identifier) and the
jurisdiction/list-code precedent in
[org-id.guide](https://docs.org-id.guide/en/latest/metadata.html#assigning-a-code),
without importing their complete data models or catalogues into the core.

#### 1.2. References in opinions and gossip

An opinion about such a resource keeps the qualified pair in envelope
`record/about[0]`; no country field or identity copy is added to the content.
Public gossip (`public-gossip.v1`) MAY use the same pair in its optional
envelope `record/about`. Neither use changes the record's epistemic status.

When `opinion/see-also` or `gossip/see-also` refers directly to the same
resource, its compact representation is `["pl-nil-pwz", "<pwz-number>"]`:
the tuple's first element carries the full namespace and the second carries
only its identifier, not the derived `resource/key`. Existing record/topic
reference kinds keep their own contracts. Each surface retains its existing
size bounds; both `see-also` fields limit an id to 512 characters, whereas
`resource-ref.v1` allows 2048. A bridge MUST NOT truncate an identifier to fit.

An opinion evaluating a rumor still references the rumor record, as specified
by [P013](013-whisper-social-signal-exchange.md), rather than replacing that
target with the person or resource mentioned in it. `opinion/subject-kind`
remains an overlay-selection hint, not a substitute for the envelope reference.

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

## Implementation Recommendations

Follow `node:DEV-GUIDELINES.md`: reuse the existing resource pair, signing and
admission boundaries, and replay-fed projections. This continuation closes
consumer gaps; it does not introduce another identifier protocol, a country
registry in the core, or a prerequisite NIL lookup.

### Reuse and Consumer Boundaries

Consumer review on 2026-10-10 found these remaining seams:

- `node:agora-core/src/envelope.rs` already owns `ResourceRef`;
  `node:agora-relay-trait/src/subject_index.rs` indexes the full opaque pair.
  Reuse these rather than adding a country-aware identity type.
- `node:agora-ui/src/agora.rs` already has subject lookup and an opinion builder
  with separate kind/id values, but its opinion form forces `url`; the generic
  compose builder does not populate envelope `record/about`.
- `node:agora-projections/src/lib.rs` currently derives the opinion
  `resource_key` as a digest of the pair, and `node:agora-service/src/main.rs`
  queries that stored key directly. This is a consumer mismatch with §1, not a
  replacement for the accepted `kind:id` contract.
- Public gossip retains `gossip/see-also` in its content, but does not project
  those links as opinions do. The separate owner is
  [Agora backlog P17](../60-solutions/008-agora/008-agora-backlog.md#p17-public-gossip-resource-links);
  it is not a dependency of basic resource publication or subject lookup.

These are code-level findings, not a claim of retained runtime acceptance.
Implementation evidence and detailed migration notes belong in Node.

### Small Data Shapes, Shared Conversions

Keep the following shapes distinct; they are bindings of existing contracts,
not new wire schemas:

| Surface | Shape | Rule |
|---|---|---|
| Resource value | `{"resource/kind": "pl-nil-pwz", "resource/id": "<pwz-number>"}` | Reuse `ResourceRef`; kind remains open, id remains a string. |
| Primary opinion subject | `record/about[0] = ResourceRef` | Required for an opinion; later entries must not reorder or replace the primary subject. |
| Generic compose subjects | `record/about = [ResourceRef, ...]` | Optional for record families that do not require a subject, including public gossip. |
| Related reference | `[kind, id]` in `opinion/see-also` or `gossip/see-also` | Preserve the complete namespace and id; do not substitute the derived key for the second element. |
| Public derived key | `kind + ":" + id` | Split on the first colon only; if supplied alongside the pair, reject disagreement. |

Use a shared UI resource editor with separate kind/id inputs and a convenient
URL mode. URL mode selects `kind = url`; generic mode must not run a URL parser
or require a registered validator. Namespace suggestions are optional, not an
allow-list. Preserve leading zeroes, case, punctuation and embedded colons in
opaque ids; no numeric coercion or silent trimming/normalization. Kind-specific
normalization belongs to an explicitly selected kind contract, not the generic
editor or relay. Escape displayed values and percent-encode each local route
segment; an unfamiliar id is not an automatically navigable external URL.

Both forms should map their local draft fields into the existing envelope
builder before signing. Do not place `record/about` inside `content`, infer it
from `see-also`, or replace an opinion's rumor-record target with a person
mentioned by that rumor. Reuse the existing signer/unlock flow and admission
policy; client validation does not replace Schema Gate at protocol boundaries.
Apply each receiving field's limits explicitly (including the 512-character
`see-also` id limit versus 2048 in `resource-ref.v1`); reject oversize input with
a field diagnostic rather than truncate it or partially publish it.

Implement pair-to-key, key-to-pair and pair-to-tuple conversions once as pure
operations at the lowest existing shared owner. Do not create a new service or
crate merely for these helpers. Test `decode(encode(pair)) = pair`, including
ids containing colons, and keep each carrier's validation at its boundary.

### Projection-Key Compatibility and Recovery

The authoritative lookup is the exact pair, with case-sensitive (`BINARY`)
comparison. The public `agora-projections.opinions.v2` DTO exposes
`subject/kind`, `subject/id`, and a derived `subject/key`. `subject/key`
presents the conceptual §1 `resource/key`; it avoids confusing that identity
with middleware `effects[].resource/key`, which has an independent contract.
No digest or derived key is authoritative or stored for new opinion rows.

**Decision (2026-10-12):** opinion queries accept only `resource_kind` and
`resource_id`, each exactly once. The old `resource_key` and `resource-key`
parameter names always return HTTP 400 `legacy-digest-parameter-removed`, for
any value and even alongside a valid pair. A legacy `sha256:<digest>` is itself
a valid open reference; heuristic value detection or reserving `sha256` would
break open namespaces. The inventoried in-tree consumer is Agora service; it
changes together with the projection API. HATEOAS uses the full pair.

Migration creates a `(resource_kind, resource_id, authored_at, record_id)`
index. The obsolete `resource_key NOT NULL` column remains readable only to
old software: existing values stay intact and new rows write an empty value.
Current readers never consult it. Signed source records, their ids and
signatures remain unchanged.

Follow [S028 Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md)
for the separate operator replay `rebuild` mode (default `incremental`, initially
only the opinions domain). Stage opinions, tags, links and indexed current
subject blocks together, persist
source cursors, catch up concurrent ingest and swap the domain atomically.
Network reads and verification run outside write transactions. Missing/pruned
source or interrupted work preserves the active projection and reports
incomplete reconstruction. Failures attributable to a pair degrade only that
pair; unassignable failures explicitly report unknown completeness. Incremental
replay and rebuild use the same projection decision: malformed retained records
are diagnosed as rejected and advance the source cursor. Missing source is a
different failure and still preserves the active projection. Current subject
blocks are indexed state; the diagnostic journal is not scanned on each read.

Topic read admission precedes the visible result limit. A bounded scan returns
`complete` and a pair-bound `next_cursor`, including a partial empty page when
the scan budget is exhausted. UI continuation uses the full pair. Reference
errors expose typed `field` and kebab-case `reason` values.

### Authoring and Historical References

Pure ResourceRef conversions preserve the pair and split a key on the first
colon. Validation is a separate operation: new builders, signing endpoints and
queries enforce slug kind, 1–2048 Unicode code points (at most 8192 UTF-8 bytes),
ECMA-262 whitespace boundaries, no control characters and NFC. NFC uses the
same definition as signature canonicalization. Do not normalize opaque ids or
reject every format/bidi character. Display accepted format characters with
visible code-point markers and direction isolation.

The creation-only [Agora authoring profile](../../schemas/agora-record-authoring.v1.schema.json)
limits new `record/about` arrays to eight unique references. Existing signed
v1 envelopes do not inherit this stricter profile. Ingress, indexing and replay
retain admitted history and record warnings in projection diagnostics. A
historical non-NFC id retains its original pair and record-id readback; a strict
query for that invalid pair returns 400. Carrier-specific constraints remain
local, including `see-also`'s 512-character id limit.

New publication has a shared 48 KiB JSON-envelope budget, including the
signature and relay metadata. Check an estimate before signing and the actual
signed envelope before publication, with field/envelope diagnostics and no
truncation. This leaves a conservative allowance within Matrix's 64 KiB full
PDU limit; real Matrix acceptance must confirm it. Query `+` decodes to a space,
`%2B` to a plus; path `+` is literal. One URI encoder emits only unreserved
characters literally. A 32 KiB request-line allowance is local to subject and
opinion reads; other routes retain 8 KiB.

The shared no-JavaScript editor keeps drafts in form fields. CSRF-protected
preview POST intents add, remove and reorder rows without signing. Opinion row
zero is explicitly the main subject. The preview freezes author, timestamp,
exact document and digest; editing requires another preview, and 423/unlock
retries preserve that document. Subject UI combines opinion projection reads
with public gossip from the relay subject index, deduplicating record ids and
showing source diagnostics. This does not implement P17 related-link navigation.

### Acceptance Boundary

Publication transport is a separate planned continuation owned by
[P035-001–003](035-agora-topic-addressed-record-relay.md#delivery-integration-tracker):
compose/opinion/comment producers sign through the existing host and hand exact
records to AD's Agora adapter. Preserve `record/about`, open resource namespaces,
topic authority and record ids; expose queued versus relay-accepted publication.
Do not introduce an opinion-specific sender or retry queue. P026-001–003 remain
independently closable on the existing publication path; after migration, rerun
their consumer assertions through AD rather than claiming old evidence proves
the new path.

Use synthetic fixtures for `pl-nil-pwz` and an unregistered namespace, two kinds
sharing an identical id, an id with leading zeroes, and an id containing colons
and URL-sensitive characters. No live professional register or real-person
opinion is needed. A new kind must work without a code or allow-list change.

Retain evidence for both UI builders and the ordinary sign → publish → subject
query → projection query → UI read path, then repeat reads after restart/replay.
Include public gossip on its accepted public-signals topic, keeping its
epistemic status unchanged. Separately exercise `see-also` shape preservation;
gossip link navigation is qualified only by Agora P17, not this basic slice.
Negative cases include missing opinion subject, removed digest parameter names,
missing or duplicate pair components,
malformed/oversize references, denied publication and escaped malicious display
text. Unknown namespaces alone are not a refusal reason under generic shape
validation; ordinary admission and disclosure policy still apply.

Schema fixtures and unit tests alone do not close the UI/runtime gate. Record
the tested revisions, commands, runtime/backend scope and retained report in
Node; reconcile its implementation ledger and any affected MVP claims when the
implementation lands, rather than marking them complete from this plan.

## Implementation Tracker

This tracker covers the consumer continuation, not a retrospective inventory of
the already implemented substrate. Statuses are `todo`, `partial`, `done` and
`blocked`; `done` requires the stated gate and linked Node evidence.

| ID | Task | Status | Dependencies | Completion gate |
|---|---|---|---|---|
| P026-001 | Generic resource authoring in opinion and compose UI | done | Existing Agora signer and subject-index baseline | Both forms reuse a kind/id editor and populate envelope `record/about`; URL convenience remains; an unknown kind works without registration; opaque ids, field limits, escaping and denied-publication tests pass. |
| P026-002 | Canonical public opinion keys and legacy projection migration | done | §1 identity contract; S028 | Shared conversions preserve `kind:id`; queries use the exact pair; removed digest parameter names are rejected; the obsolete column is never read; domain rebuild and consumer changes are documented; interrupted rebuild, replay equivalence and incomplete-source diagnostics are tested without rewriting signed records. |
| P026-003 | Open-namespace consumer acceptance | done | P026-001, P026-002 | Retained UI and runtime evidence covers the Acceptance Boundary matrix for opinions and public gossip, including two namespaces with the same id, restart/replay and refusal paths; report scope distinguishes basic references from Agora P17 link navigation; relevant Node ledger/MVP evidence is reconciled. |

Qualified checkpoint (2026-10-12): `node:docs/evidence/open-references/README.md`
retains the existing `story-008.smoke-result.v1` profile, its qualifier and
per-case process/HTTP artifacts: 20 SQLite and 18 Matrix runtime cases plus
separate conformance processes. Matrix B builds the subject index from inbound
`/sync` before projecting opinions, then repeats UI/API reads after restart and
replay. Signed non-NFC history is retained exactly and diagnosed. Both backends
publish a 49,134-byte envelope under the 48 KiB budget and refuse oversize
creation. Node ledger and Story-008 MVP entries record this consumer scope.

Matrix uses distinct clients on one homeserver; this proves distribution, not
federation. **Matrix gossip is qualified only for integer JSON numbers**;
the retained fixture has `confidence=1`. Ordinary fractional confidence, such
as `0.5`, remains unqualified. This is a transport-contract mismatch: Matrix
canonical JSON permits integers only, in `[-(2^53)+1, (2^53)-1]`. Conduit v0.7.0
exposed it as HTTP 500 (`IntConvert`); that response is an observation, not the
cause of the restriction. [Matrix canonical JSON](https://spec.matrix.org/latest/appendices/#canonical-json)

[P035-004](035-agora-topic-addressed-record-relay.md#matrix-carrier-tracker)
owns the opaque-carrier replacement and its encoded PDU budget. Closing these
three rows does not qualify general decimal-valued gossip, other P026 surfaces
or production readiness. The original process artifacts and revisions remain
frozen; the qualification report and evidence index carry this scope correction.

Review corrections (2026-10-12): live projection, incremental replay and domain
rebuild share opinion rejection decisions and diagnostics. Content rejection
advances the staged source cursor; source loss remains an incomplete rebuild.
Current pair blocks live in an indexed `opinion_subject_blocks` read model,
separate from the append-only journal, and are replaced with the staged domain.
Read admission precedes the visible result limit through bounded page scanning;
`complete` and a pair-bound `next_cursor` distinguish exhaustion from unfinished
work. DTO subject fields use `subject/kind`, `subject/id`, `subject/key`. Review
hashes use JCS without string normalization. Recent historical diagnostics link
to record-id retrieval without relaxing strict pair queries.

### Pruned-source continuation

| ID | Task | Status | Dependencies | Completion gate |
|---|---|---|---|---|
| P026-004 | Explicit carry-forward for pruned opinion sources | todo | P026-002; S028 | Keep strict rebuild as the default. An explicit carry-forward mode retains prior opinion/tag/link/block rows only where source loss is proven; record prior projection revision, source bounds and per-record inherited provenance. Reports distinguish recomputed from inherited rows, preserve earlier blocks and unknown completeness, and never claim full-source replay equivalence. Restart, concurrent ingest, source-loss and future-format fixtures qualify the mode before status promotion. |

P026-001 and P026-002 may proceed independently against the existing pair
contract; P026-003 closes their joint slice. Public-gossip related-link indexing
and navigation remain the single-source task
[Agora P17](../60-solutions/008-agora/008-agora-backlog.md#p17-public-gossip-resource-links),
which can proceed independently and must not block basic open-namespace support.

## Open Questions

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-05:

1. `resource/kind` remains open. Individual kind contracts may gain dedicated
   validation when interoperability or safety requires it; this does not close
   the generic namespace catalogue (see §1.1).
2. `node` and `org` resource opinions require explicit anti-harassment, appeal,
   or moderation rules before they appear in public aggregates.
3. `gps` resources use a precision-bounded location key. Raw `lat,lon` is not
   the default public resource identifier.
4. One author has at most one active opinion per resource. Revisions are
   append-only and linked through `supersedes`.
5. Text and rating stay in one artifact family for v1. They may split later if
   their moderation policies diverge.
6. The first attached discussion medium is an archival forum/thread reference,
   not an ephemeral chat-like channel.
7. Future discussion artifacts mark human-authored versus agent-authored
   contributions through explicit authorship/origin flags reusing the P004/P011
   provenance pattern.

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

- `resource/kind` remains open and individual kind contracts may require later
  normalization work,
- the proposal intentionally leaves moderation and deduplication
  unresolved,
- `resource/key` is derived rather than authoritative, so consumers
  must validate it instead of trusting it blindly,
- and implementers must remember that subject identity is **not** in
  the content body — any tool that reads opinions must read from the
  envelope's `record/about[0]`, not from `resource-opinion.v1` fields,
  which intentionally no longer carry them.

## Follow-Up

The immediate consumer slice is P026-001 and P026-002 followed by P026-003.
The broader follow-up list below includes existing artifacts and later work;
it is not evidence that the new consumer tasks are complete:

1. one schema for `resource-opinion.v1`,
2. one requirements note for normalization and revision policy,
3. optionally one separate proposal for attached resource forum or channel
   semantics,
4. proposal 040 (custodial redelivery and tombstones) covers how opinions
   survive relay data loss and how participants place copies with other
   nodes under capability-passport-backed custody; opinion-specific
   retention or right-to-forget flows build on that substrate.
5. Keep kind-specific validation and alias lifecycle rules explicit without
   turning the open `resource/kind` catalogue into a closed core enum. Country-
   scoped namespaces follow §1.1; validators remain outside the generic core.
6. Add moderation prerequisites for `resource/kind = node` and
   `resource/kind = org`: explicit anti-harassment, appeal, or moderation rules
   must exist before public aggregates are exposed.
7. Specify the precision-bounded GPS key contract for `resource/kind = gps`; raw
   `lat,lon` is not the default public resource identifier.
8. Document one-active-opinion-per-author semantics: revisions are append-only,
   linked through `supersedes`, and projected as the latest active opinion plus
   append-only history.
9. Reaffirm v1 unification: `opinion/text` and `opinion/rating` remain in one
   artifact family unless moderation policies later diverge.
10. Require future forum/thread/channel discussion artifacts to mark human-authored
    versus agent-authored contributions through explicit authorship/origin flags,
    reusing the P004/P011 provenance pattern.
