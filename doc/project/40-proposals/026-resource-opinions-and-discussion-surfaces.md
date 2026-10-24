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

The assessment-exposure continuation has a bounded local-SQLite pilot, qualified
on 2026-10-24 as recorded in the local evidence checkpoint below. Its contract
freeze, implementation, focused component tests and real host/browser acceptance
are separate claims. The wider consumer continuation remains partial; sealed
rounds remain planned. The P026-001–003 qualification retains its original scope.

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

### 6. Assessment Exposure and Sealed Rounds

**Design decision, 2026-10-23.** Reduce social anchoring without confusing
popularity with value, delaying urgent protection, or claiming to prove an
individual's psychological independence. This section owns the shared contract;
[S008](../60-solutions/008-agora/008-agora.md#planned-assessment-exposure-and-round-projections)
owns Agora's service boundaries. [P013](013-whisper-social-signal-exchange.md#assessment-exposure-profile)
binds rumor opinions, [P051](051-swarm-membership-and-reputation-bootstrap.md#11-first-review-must-be-anti-collusive-and-temporarily-blind)
binds panel judgments, and [P069](069-corpus.md#shared-sealed-round-binding)
binds Corpus first judgments. These profiles reuse mechanics, not each other's
authority or payload semantics.

Two independently deliverable levels are required:

| Level | Guarantee | Boundary |
|---|---|---|
| Local exposure gate | `local-display-only`: the host shapes the authorized viewer's assessment read model | Does not stop publication, replication, another client/relay, or off-protocol disclosure; UI hiding alone does not satisfy it. |
| Sealed round | An admitted commitment belongs to a signed closed set and its later reveal verifies against it | Prevents counting an uncommitted adaptive answer in that round under the declared barrier authority; not global secrecy, trusted timestamping, Sybil resistance or psychological independence. |

Exposure is scoped to **(viewer, subject)** or a named round, not to the age of
each opinion. A late visitor should not inherit everybody else's expired window.
The local gate must not be marketed as anonymous voting or moderation. Existing
`hide-local`, topic ACLs and the right to appeal retain their separate meanings.

#### Host Read Policy and Local Facts

The service pipeline is `admit -> expose -> render`. Admission retains existing
authorization semantics, including omission of inaccessible topics in a paged
query; an operation-level refusal is not converted into `withheld`. Only after
admission does the pure exposure policy shape a view. It neither grants access
nor discloses the existence of unauthorized records.

Prospective `assessment-exposure-profile.v1` contains:

| Field | Contract |
|---|---|
| `profile/id`, canonical digest | Exact admitted profile identity; operator configuration through P091, with explicitly bounded user choices. |
| `applies-to` | Record and subject selectors; resource namespaces remain open. |
| `mode` | Closed enum: `open`, `blind-until-own-judgment`, `sealed-round`; the latter delegates to the round owner. |
| `withheld` | Closed item enum: `peer-ratings`, `peer-rationales`, `aggregates`, `counts`, `rating-order`, `popularity-badges`, `peer-discussion`. |
| `unlock` | Closed item enum for local mode: `own-first-judgment`, `explicit-skip`, `subject-window-elapsed`. A round requires its validated barrier instead, not a personal skip. |
| `subject-window/seconds` | Bounded local duration from a durably recorded first encounter, not opinion publication or an arbitrary UI clock. |
| `exempt/record-kinds` | Closed, versioned set of registered protective kind contracts admitted for this profile; not arbitrary sender strings. |
| `guarantee` | `local-display-only` for local mode; never an independence credential. |

The policy objects are closed (`additionalProperties: false` at their object
boundaries; `enum` on array items), unlike the open opinion body. Unknown policy
fields or modes fail validation, never fall back to `open`. Conditional schema
branches carry explicit `required` lists; cross-field invariants also live in
the pure core. There is no worldwide default duration: `172800` seconds is an
example, not a measured optimum. Prefer hiding ratings, aggregates and popularity
badges in the first pilot. Rationales capable of revealing ratings are covered
by the same pilot profile. `peer-discussion` is an explicit profile choice, not
a silent global suppression of conversation.

Prospective `assessment-exposure-fact.v1` binds `viewer/ref`, `subject/key`
(the existing `ResourceRef::to_key()`), optional `round/ref`, `event`, optional
`cause/record-id`, `profile/digest`, `recorded/at`, and an idempotency key. In
addition to `own-first-judgment`, `explicit-skip`, `subject-window-elapsed` and
`barrier-released`, the closed event vocabulary needs `subject-first-seen` and
`view-released`: a timer needs a durable origin and an open-mode disclosure must
not later be mistaken for an unseen subject. These are host-accepted local facts,
not client assertions about what a human actually saw. The read evaluator receives
explicit `now`; an authenticated encounter/unlock command records transitions.
No hidden database mutation in a nominally pure query. Persist a release before
returning peer content; retry is idempotent and a failed fact write cannot grant
a new release. Request cancellation after recording release may conservatively
overstate exposure, never certify an unseen judgment.

Store these private facts under the service's S028 temporal owner, **not** in
Agora's relay-rebuildable `ProjectionStore`. Reuse temporal event/log/profile
mechanics and private storage controls, with a manifest, bounded subject count,
retention and replay. Full events may compact to a sufficient exposure summary.
If that summary is also erased, return unknown history: conservative re-hiding
is permitted, but it does not restore an independence claim. Profile tightening
does not undo a recorded release for that scope; authorization revocation still
denies access. New rounds have distinct scopes. Do not silently merge resource
aliases or viewers; account switching and delegated reads preserve the binding.

An `own-first-judgment` unlock requires an accepted, viewer-authored opinion for
that subject, not a draft or publication attempt. Existing supersession links
classify known revisions, but absence of `record/supersedes` in a partial replica
does not prove a globally first opinion. Multiple roots, unknown ancestry and
agent-authored contributions require explicit handling; none earns independence
from local exposure history. V1 adds no self-declared `assessment/exposure`
overlay to the public opinion.

#### Viewer-Bound API Projection

The proposed `resource-assessment-view.v1` has this illustrative withheld shape
(placeholder refs are not executable schema fixtures):

```json
{
  "schema": "resource-assessment-view.v1",
  "viewer/ref": "participant:viewer-placeholder",
  "subject/key": "url:https://example.org/article",
  "exposure": {
    "state": "withheld",
    "profile/digest": "sha256:…",
    "withheld": ["peer-ratings", "peer-rationales", "aggregates", "counts", "rating-order", "popularity-badges"],
    "unlock/options": ["own-first-judgment", "explicit-skip"],
    "guarantee": "local-display-only"
  },
  "own": [],
  "exempt": [],
  "peers": null
}
```

Withheld is not zero: omit peer totals, completeness, cursors, projection
versions, `as-of`, ETags and hidden-data-dependent freshness markers. Own and
protective lanes have independent bounded pagination if needed; they cannot
carry peer-page metadata. With own/exempt/public-policy inputs fixed, varying
hidden peer data must not change the serialized response shape or length,
ranking, page boundaries or event emission. Use neutral ordering before ranking
or limiting a cross-subject result; filtering after popularity sorting leaks.
Avoid scanning hidden peers merely to produce the withheld response. Scope or
disable caches; never share a viewer projection across callers or profiles.
This is a testable application-channel boundary, not a claim of eliminating
every network timing or external correlation side channel.

HTTP, UI (including no-JS pages), CLI, [Agent observations](073-agent-orchestration-organ.md#assessment-observations)
and [S039 notifications](../60-solutions/039-notifications/039-notifications.md#planned-assessment-exposure-rendering)
must consume this same projection. Direct detail/by-id queries, searches,
exports, counts and streams in the viewer surface cannot bypass it. Raw relay
replication and explicitly privileged inspection remain outside the local-display
guarantee and must be identified as such, not silently used by a viewer's Agent.
An Agent inherits the represented viewer's scope; it cannot synthesize a skip
from tool availability. A skip requires that viewer's authorized, explicit choice.

#### Local Pilot Contract Freeze (2026-10-24)

The first local slice freezes `assessment-exposure-profile.v1`,
`assessment-exposure-fact.v1`, `assessment-exposure-command.v1` and
`resource-assessment-view.v1`. Runtime qualification is recorded separately in
the local evidence checkpoint; the freeze does not establish runtime completion.
Each own/released-peer entry retains its admitted open `opinion` body, including
rumor credibility and rejection overlays; the legacy `opinions.v2` projection is
unchanged. This preserves P013's typed content rather than reducing every opinion
to the optional generic scalar. The view additionally binds `viewer/ref`; the authenticated host derives that
value from its current caller binding. Public commands contain only a subject,
an optional admitted transition, idempotency key and accepted-record cause.
An asserted viewer, module identity or Agent `participant_ref` alone grants no
viewer authority. The existing authenticated host/middleware channel carries the
resolved binding to the service; the product's shared token cannot represent it. The
first browser binding requires explicit operator authentication; a loopback UI
without authentication or a regular user session cannot borrow the backend's
operator control identity.

The pilot withholds all six rating/rationale/aggregate/count/order/badge items;
`peer-discussion` remains an explicit optional selection. The local profile's
resource-kind selectors remain open. Sealed-round mode is recognized and refused
until its separate owner contracts and acceptance exist. No public exposure
assertion or independence credential is added to an opinion.

Encounter and unlock are explicit authenticated commands. Reading a view is pure;
an elapsed window or open policy needs a durable release transition before peer
content can be returned. An explicit encounter may record that transition, including a repeated command evaluated with a new explicit time (the reviewed monotone semantics below). A local
encounter names an opaque subject and neither probes record existence nor grants
record access. Every rendered record still passes the ordinary topic admission.
The private service-owned S028 store is independent of relay projection rebuild.
It retains sufficient summaries through compaction and records unknown history
after loss, with bounded subject and event populations.

The first implementation profile requires the explicit local-SQLite backend;
Matrix startup refuses while exposure is configured until publication-receipt
metadata is independently qualified. Reference-bearing parent/supersedes signing
also refuses until it can use viewer-bound admission. Signed-record ingest and
operator projection rebuild are explicit transport/maintenance operations outside
the viewer display guarantee and cannot be observation fallbacks for an Agent.

The initial viewer projection is bounded to 100 entries per lane. Mixed raw relay
pages and raw record inspection using only the shared product token refuse while
the profile is configured; their relay cursors, counts and SSE cannot safely be
reused as viewer metadata. Consumers use the host projection instead. Rich
viewer-safe pagination and a separately privileged raw inspection interface need
their own implementation and evidence before introduction. Existing typed rumor
propagation, protection and appeal owners retain their admitted paths. The
protective opinion exception list is empty until concrete closed kind contracts
are admitted; sender urgency or a generic moderation marker cannot populate it.

#### Local Pilot Review Amendment (2026-10-24)

The operator accepted two review amendments before implementation. Local command
idempotency is monotone per viewer/subject/command kind, grounded in retained facts;
repeated encounters evaluate a new explicit `now`. Client request keys are
correlation references, not permanent request-result receipts. Balanced/minimal
S028 retention compacts sufficient summaries at the event bound. No compaction
removes release/history facts or creates an independence credential. Full-audit
retains its no-pruning rule and an explicit capacity refusal.

A diagnosed opinion is quarantined rather than vetoing its whole subject. The
released lane uses deterministic bounded author contributions; its conservative
`degraded: true` marker always denotes bounded/incomplete coverage, not a count or
health oracle for denied topics. This marker is absent while peers are withheld.
The first candidate policy takes up to 64 topics per author (4096 total candidates)
and up to 16 admitted opinions per author, round-robin before the 100-entry limit.
It does not claim global completeness, Sybil resistance or constant database cost.
Whole opinion entries may be omitted to satisfy the host response byte bound;
fields within a retained opinion are never silently truncated.

An open/out-of-selector read with no release fact returns
`disclosure-not-recorded`, empty withholding/unlock lists and `peers: null` until
an explicit encounter records disclosure. Withheld views may show the viewer's
own window origin/deadline/state. A probe-only read distinguishes an exact
`exposure-not-configured` refusal from closed/active state without resolving a
viewer or reading that viewer's assessments. UI authentication precedes a real
viewer query. Product routes use an audited allowlist with default refusal;
record-target moderation markers and state-probing POSTs cannot bypass exposure.
Rendered UI/CLI commands may pin the displayed `profile/digest`; a mismatch
refuses before effects. Client keys do not grant authorization. The private store
uses SQLite FULL as a disclosure-before-content durability floor; this is not
physical power-loss qualification. Its stopped-owner local inspection/compaction
utility exposes private capacity counters, never a viewer-facing history export.
Capacity, forbidden unlock and transient storage failure have distinct status and
retryability contracts; scope and full-audit bounds remain operator-visible.
These contract amendments do not renew the earlier runtime checkpoint; their
implementation and new acceptance evidence are recorded separately.

#### Local Pilot Evidence Checkpoint (2026-10-24)

The accepted local freeze covers four closed profile/fact/command/view contracts.
Node implements the pure policy, separate private S028 fact store and authenticated
host projection, with bounded UI, CLI, registered Agent and notification adapters.
Focused component tests cover clock uncertainty, failed writes, retention gaps,
idempotency, profile changes, viewer isolation and replay. A common-view regression
releases a view, revokes its topic admission, verifies omitted peer content and
retains the same durable release summary after reopen/replay. Agent-controller and
notification-owner fixtures use scripted owner responses and retain that scope.

The original `2026-10-24-local-04` report pins clean Node `63ece2a4` and Orbidocs
`7cf59bf4`. Nine real local-SQLite host/API/UI/CLI cases passed, including authenticated
caller refusals, byte-stable withheld views after hidden judgment changes, rumor
body withholding/release, accepted own judgment, process restart and Agora projection
rebuild. Actual Chrome runs cover JavaScript enabled and disabled. Independent
qualification verifies the retained original witness bytes and hashes; negative
verifier regressions use copies of that passed report. Evidence and the two prior
refused attempts are retained under `node:docs/evidence/agent-runtime/2026-10-24-rate-exposure/README.md`.

This checkpoint qualifies the bounded local display pilot. P026-005 remains partial
because round/protective-kind contracts have separate gates. P026-007/008 retain
wider consumer acceptance work, including the complete P013, notification and Agent
matrices. The rumor fixture preserves opinion extension fields through the common
view; it does not introduce a standalone rumor-overlay admission schema or qualify
the complete Whisper curation/propagation workflow. Registered notices remain
informational and polling-only, without an automatic assessment-notification
producer. Matrix/federation, sealed rounds, P051/P069, real models, full campaigns,
psychological independence, social effectiveness and release readiness remain
outside this evidence.

#### Local Pilot Review Evidence Checkpoint (2026-10-24)

Review run `2026-10-24-review-01` pins clean Node `91babeb0` and Orbidocs
`414acd72`. Nine bounded real-process cases pass, including byte-identical hidden
views with the viewer's own running window, a viewer-free closed probe, default
new-route refusal, record-marker queries, identical known/missing POST refusals,
stale profile consent without effects, CLI parity, restart/rebuild and Chrome
JavaScript/no-JavaScript window/deadline rendering. Cleanup is confirmed.
Independent v2 qualification agrees normally, with Python `-O` and after archive
extraction; all 38 evidence mutations refuse. Historical reports and the v1
qualifier remain unchanged. See
`node:docs/evidence/agent-runtime/2026-10-24-rate-exposure-review/README.md` and
`node:docs/audits/REVIEW-RATE-EXPOSURE-2026-10-24.md`.

Migration from full legacy receipts, the exact event-capacity boundary, full-audit
refusal, offline maintenance, 4,097-topic author isolation, open/unselected state
and explicit-time expiry remain component evidence. The current real UI/CLI
viewer is the node operator. Other represented participants and Agent/notification
bindings retain synthetic-host scope, including pre-read identity/classification
refusal and centralized attention exclusions. No actual assessment notification
producer, full Agent prior-context matrix, multi-user runtime, physical power-loss,
complete/Sybil-resistant coverage, Matrix/federation or release readiness is
qualified. P026-005/007/008 and P013/P057/P073 continuation statuses remain partial;
P026-006 remains done only for local policy/private facts.

#### Q-02 Bounded Qualification Contract (2026-10-24)

Accepted scope: the module-as-viewer case uses a harness-admitted `CallerBinding`
inserted into the daemon's existing resolver through its normal owner API. No
resolver replacement, viewer assertion from a module, or production provisioning
surface is admitted. The insertion/removal hook exists only under an explicit
acceptance build feature; evidence binds that feature set, source and executable.
These cases have class `fixture-bound-input`, separate from production-path
`runtime` cases. The ordinary `module:*` binding must return `viewer-unbound`,
without operator fallback, raw observation fallback or automatic skip.

Expiry and revocation must refuse the next read while preserving durable release
facts. Restart must not restore the harness lease; re-admission may demonstrate
that the original release facts survived. Agent qualification uses existing local
control, independently of the harness binding. A deterministic test adapter may
exercise its actual controller/observation/trace path without a real model; it is
not inference, prior-context completeness or cognitive-independence qualification.

The module path is qualified only with a harness-admitted binding. Production
modules cannot be assessment viewers until the separate identity-host provisioning
slice exists. P026-005/007 remain partial. This contract is not runtime evidence.

#### Shared Commitment and Barrier Contract

The shared primitive is `salted-sha256-jcs-v1`: SHA-256 of an exact JCS preimage
with a domain discriminator and fresh 32-byte cryptographically random salt;
encode digests using existing `sha256:` plus unpadded base64url conventions.
Reuse canonical-json and crypto utilities. Extract a small pure `commitment-core`
only for shared mechanics, with bounded inputs and no I/O, clocks, randomness
acquisition or domain admission inside it. The host supplies the salt securely.

For Agora the preimage binds `domain = orbiplex.agora.assessment-commitment.v1`,
`round/ref`, `author/participant-id`, `subject/key`, `opinion` (a validated
`resource-opinion.v1` value) and `salt`. Corpus keeps
`orbiplex.corpus.first-judgment-commitment.v1` and its Room/round/participant/judgment
binding. Responsibility freezes its own domain and review payload. Reuse never
coerces a panel verdict or free-form deliberation into a resource rating.

Canonicalization must not change the committed value in transit. Agora's
envelope normalization and JCS are not interchangeable. Freeze a transport-safe
binding before coding: carry bounded canonical JCS bytes opaquely where needed,
or validate and declare normalization before commitment, never after it.
Include non-NFC, Unicode, numeric and cross-language golden fixtures and the
Matrix carrier budget/encoding from P035. A parsed reveal must validate against
its domain schema as well as match the digest.

Agora's prospective kind contracts are separate from `opinion`:

Before closure, the round publication path emits commitments only; bodies and
salts remain in the participant's protected local pending store. This is the
publication barrier, unlike local hiding of already published opinions. It
neither retroactively makes public data secret nor prohibits an ordinary opinion
outside the round. Such outside publication is not proof of a qualified reveal
and remains an explicitly excluded leakage channel.

| `record/kind` | Required binding | Signer |
|---|---|---|
| `assessment-round` | Subject; profile revision/digest; eligibility (`open` or `enumerated`, exact set ref/digest); barrier rule; authority ref; commit/reveal/max close times; limits; scheme | Authorized opener |
| `assessment-commitment` | Round, authenticated author, fixed-size commitment digest and scheme; no body, salt or content-dependent hints | Participant |
| `assessment-barrier` | Round, release time/reason, exact bounded sorted distinct commitment-id list, count and domain-separated JCS set digest | Authority designated by the admitted round |
| `assessment-reveal` | Round, **barrier ref**, commitment ref, salt and exact committed typed body in the frozen transport encoding | Same participant |

Unknown kinds must not be indexed as ordinary opinions by legacy consumers.
Only the round-aware projection emits eligible revealed opinion views, with
round and outcome provenance retained. `OpinionView` need not become the owner
of round state. Corpus/Responsibility use equivalent signed domain facts through
their existing owner, not a mandatory public Agora publication of private votes.

The authority serializes commitment admission and barrier closure using its
existing durable owner/CAS and outbox patterns. It freezes one accepted set,
persists the closure before publishing its signed barrier, and refuses later
commitments for that phase. A participant needs an authenticated admission receipt
if it relies on inclusion before the cutoff; the freeze must define receipt/set
reconciliation and admission-time evidence. `authored/at` and unsigned, prunable
`relay/received-at` are not that evidence. Deadline evaluation belongs to the
admitted authority with a declared clock/uncertainty policy; uncertain cutoff
must not silently count a judgment.

**A barrier reference proves binding, not publication time.** A digest can be
precomputed, an authority can backdate, omit or fork, and collaborators can leak
bodies. Verification therefore depends on the declared authority and retained
closure/admission evidence, not a claim of global chronology. Conflicting signed
barriers or a receipted commitment missing from the closed set invalidate counting
pending resolution; do not select the first relay's version. Replicas must fetch
and validate the referenced set before qualification. Partial history or an
unavailable authority yields unresolved evidence, not an invented empty set.

| State | Event | Result |
|---|---|---|
| `committing` | Eligible commitment admitted before cutoff | Remain `committing`; exact replay is idempotent. |
| `committing` | Valid signed barrier closing the accepted set | `revealing`; subsequent reveals must bind this barrier. |
| `committing` | No closure by mandatory `round/max-closes-at` at the owner | `void`; no independent-judgment result. A replica missing evidence cannot infer global void from local absence alone. |
| `revealing` | Valid bounded reveal from the committed author before reveal cutoff | Remain `revealing`; verify body, membership, authority and domain. |
| `revealing` | `reveal/closes-at` | `closed`; report missing and invalid reveals explicitly. |
| `closed` | Later opinion/revision/rebuttal | Separate post-barrier lane; cannot enter the first-judgment set. |

Freeze valid deadline ordering (`commit < reveal <= max`) and fail-closed late
barrier behavior; no adaptive extension after seeing judgments. Open eligibility
permits only a deadline barrier. Quorum or all-eligible release requires a pinned,
finite eligibility set and a declared COI/recusal policy. All policies bound
participants, records, bytes, verification work, retries and round lifetime.
Scheduler S020 may wake work; it does not own deadline truth or barrier authority.

Per-commitment outcomes are closed: `counted`, `missing-reveal`, `invalid-reveal`,
`outside-barrier`, `equivocation`, `round-void`. Distinct commitments by one author
in one round cause equivocation; exact retransmission does not. The projection
must diagnose conflicting commitments even if only one was placed in the barrier;
an incomplete input set cannot certify their absence. Scope outcomes to an
evidence snapshot, retaining correction provenance when later admissible evidence
changes a result. A missing reveal is not zero or disagreement. Short reveal
windows limit but do not eliminate selective-abort bias.

Only a verified `counted` result can carry `independent-first-judgment = true`,
explicitly meaning **protocol-qualified commitment**, not psychological or social
independence. Local hiding, a client claim, hidden panel names or parallel model
calls never suffice. P051 may use only such results for a round-derived
independent-assessment input; this does not prohibit separately substantiated
procedural reputation or immediate evidence-based protective action.

#### Protection, Defaults and Remaining Choices

Urgent protection, harm evidence and appeal access must not wait for either gate.
Freeze a closed mapping of admitted protective **kind contracts**, authority and
minimum necessary fields; the names `safety-warning`, `harm-evidence` and
`appeal-notice` are proposed roles, not a claim that those schemas already exist.
Their contracts reject `opinion/rating` and equivalent aggregate/badge fields;
sender labels or prose claiming urgency cannot grant an exception. Reuse existing
protective paths without forcing sensitive evidence into a public opinion lane.
Safety narratives may still influence a reviewer: do not claim cognitive blindness
after necessary disclosure, and never conceal evidence or panel composition needed
for defense, recusal or appeal. Whisper propagation budgets/thresholds remain
independent of presentation. Protection is not a popularity vote.

V1 choices and freeze questions:

1. **Q-01 resolved:** no client exposure overlay or reputation weight for it.
2. **Q-02 proposed safe default:** round creation requires an admitted opener
   policy, quotas and consumer selection by explicitly trusted authority and
   round ref. Multiple rounds remain distinct; do not auto-select the largest,
   latest or most favorable. Exact open-resource opener policy remains to freeze
   in P026-005 before enabling rounds.
3. **Q-03 proposed default:** `peer-discussion` is profile opt-in; ratings and
   aggregates remain separately controlled. A discussion preview may itself
   disclose judgments, so narrower profiles must state this limitation.
4. Freeze barrier authority/receipt recovery, private-salt retention, clock
   uncertainty and exception-kind bindings before the sealed-round slice.

Trade-offs include slower feedback, withholding useful rationales, local-state
privacy cost, a trusted closure owner and selective non-revelation. There is no
global secrecy guarantee for already public opinions. The social-effectiveness
hypothesis requires its own evaluation, separate from implementation acceptance;
neither a successful UI fixture nor a chosen window proves reduced herding.

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

### Assessment Exposure: Reuse and Acceptance

Inspect and reuse these seams before adding endpoints (inspection: 2026-10-23):

| Layer | Existing seam / planned addition | Boundary |
|---|---|---|
| Primitive | Existing canonical-json and crypto helpers; small shared commitment module/crate if justified by both bindings | JCS hashing/verification only; domain, typed payload, salt generation and admission remain explicit inputs/owners. Panel-draw entropy commitments are not assessment voting. |
| Policy | Planned pure `assessment-exposure-core` | Validated profile + scoped facts + explicit time -> typed `ExposureDecision`; closed enums, no host dependencies. |
| Contracts | Existing Schema Gate and Agora kind-contract dispatch | Add/version profile, fact, view and four round-kind contracts with `x-dia-basis`; preserve the open resource namespace and signed legacy bytes. |
| Projection | `node:agora-projections/src/lib.rs` | Reuse opinion parsing/revision rules; separate round projection and outcome provenance. `OpinionView` is not the policy or private exposure store. |
| Service | `node:agora-service/src/opinion_query.rs` | Existing `admit` callback remains authorization. Add `expose` after admission, before peer scanning/ranking/pagination; raw `OpinionPage` is not a client DTO. |
| Local persistence | [S028](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md) temporal event log/profile/manifest | Private exposure facts are a separate recovery domain; relay projection rebuild cannot delete them. Persist only bounded necessary facts, never unrelated browsing history. |
| Effects and surfaces | Existing Agora signer/relay, domain outboxes, P072 registry, P073 observations, P057/S039 rendering | No second signing, scheduler, notification or capability system. UI/CLI render the same host-projected data. |

The first deliverable is the local gate for opinions and rumor curation, including
every admitted viewer surface. It can close without sealed rounds. The second
deliverable adds commitments/barriers and explicit profile bindings; it must not
retroactively label the first as protocol-independent. Do not block the alpha
path or reopen qualified baseline rows merely by adding this continuation.

Acceptance starts with refusal, restart and replay, using synthetic participants
and fixtures rather than real people's ratings:

- With identical own/exempt/public-policy inputs, vary hidden peer values, count,
  order and arrival: API bytes, cursors, ETags, rankings, page membership, rendered
  output and notification/SSE activity must not reveal the variation. Check list,
  detail, search, by-id, export, CLI and Agent paths, not only browser CSS.
- No-JS and JS browser clients show `withheld`, not zero, expose an explicit skip
  and preserve it across restart. Verify separate viewers, profile tightening,
  denied reads, accepted own judgment, local-window expiry and concurrent unlock.
- Rebuild opinions from the relay without losing private exposure facts. Test
  compaction, missing history, storage failure, clock rollback and no synthetic
  independence after retention. Scheduler outage cannot extend a true deadline.
- Different salts for equal low-entropy bodies produce different commitments;
  wrong body/salt/domain/author/round and noncanonical encodings fail. Replayed
  records are idempotent, distinct duplicate commitments equivocate, absent reveal
  is reported, out-of-set commitment is `outside-barrier`, and missing/invalid
  barrier refs cannot count. Verify bounded verifier work and restart recovery.
- Test closure racing admission, missing receipted commitment, barrier forks,
  withheld barrier, partial relay history, reveal cutoff and transport round trips.
  A late submission cannot enter the first set; corrections retain prior provenance.
- A forged safety label or rating smuggled into a protective kind is rejected.
  Genuine urgent protection, defense/recusal and appeal remain reachable while
  ordinary peer judgments are withheld; no exposure result grants enforcement.

Retain one source-pinned report with separate local/round/profile qualifications,
negative fixtures, declared exclusions and recovery evidence in Node. Reuse the
open-reference/Agora harness and local-accountability/Corpus fixtures for their
respective bindings. Update Node ledger/MVP claims only with matching evidence;
social-effectiveness and federation claims need separate qualification.

Research motivation, not a window-setting rule: Muchnik, Aral and Taylor's
[randomized experiment](https://pubmed.ncbi.nlm.nih.gov/23929980/) found asymmetric
effects of prior ratings, including accumulating positive herding. This supports
testing concealment of aggregates/popularity cues first; it does not establish
an Orbiplex-specific duration or guarantee that delayed disclosure improves every
community's judgments.

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

The retained `node:docs/evidence/open-references/2026-10-12-review/qualification.json`
qualifies these corrections with 20 SQLite and 18 Matrix runtime cases and
453 conformance tests per backend. Runtime source revisions are Node `9f114aae`
and Orbidocs `308e936`; the evidence index explains rejected-history, visibility
and materialized-block observations. General decimal gossip is still unqualified.

### Pruned-source continuation

| ID | Task | Status | Dependencies | Completion gate |
|---|---|---|---|---|
| P026-004 | Explicit carry-forward for pruned opinion sources | todo | P026-002; S028 | Keep strict rebuild as the default. An explicit carry-forward mode retains prior opinion/tag/link/block rows only where source loss is proven; record prior projection revision, source bounds and per-record inherited provenance. Reports distinguish recomputed from inherited rows, preserve earlier blocks and unknown completeness, and never claim full-source replay equivalence. Restart, concurrent ingest, source-loss and future-format fixtures qualify the mode before status promotion. |

P026-001 and P026-002 may proceed independently against the existing pair
contract; P026-003 closes their joint slice. Public-gossip related-link indexing
and navigation remain the single-source task
[Agora P17](../60-solutions/008-agora/008-agora-backlog.md#p17-public-gossip-resource-links),
which can proceed independently and must not block basic open-namespace support.

<a id="assessment-exposure-continuation-planned"></a>

### Assessment-exposure continuation

| ID | Task | Status | Dependencies | Completion gate |
|---|---|---|---|---|
| P026-005 | Freeze shared exposure and round contracts | partial | Existing P026 identity and admission contracts; P091; S028 | Audit all read/notification/ranking/raw-access paths; freeze closed policy/fact/view shapes, authenticated viewer and encounter/release semantics, limits, protected-kind bindings and Q-02/Q-03. Freeze typed domain bindings, exact commitment bytes, authority/receipt/clock/fork rules and secret retention for rounds separately. Add Schema Gate positive/negative fixtures; no new runtime capability claim from schema presence. Local checkpoint 2026-10-24: the four local contracts and their Schema Gate fixtures are frozen. Round authority/receipts/commitment bytes and concrete protective-kind bindings remain deferred; the local exemption list is empty. Review amendment: monotone command facts, new explicit encounter time, bounded degraded coverage, disclosure-pending/window and probe shapes are adopted; this does not close round contracts. |
| P026-006 | Local exposure policy and private temporal facts | done | 005 local contracts | Pure policy with explicit time, durable encounter/unlock/release facts and replayable bounded summaries; use S028 mechanics outside ProjectionStore. Prove restart, idempotency, authorization revocation, profile change, retention gaps, clock uncertainty and failed-write behavior. Local checkpoint 2026-10-24: pure/core and private-store tests cover the stated local gates; the common-view revocation regression preserves durable release while omitting denied content. Original run 04 adds real process restart and projection rebuild evidence. This closes local policy/private facts only. Review boundary/migration tests cover full legacy receipts, atomic balanced/minimal compaction, full-audit refusal and stopped-owner maintenance while retaining disclosure/history. |
| P026-007 | Viewer projection across Agora consumers | partial | 006 | Compose admit/expose in the service; gate every audited list/detail/search/export/ranking/stream/CLI/Agent surface without changing authorization. No peer-derived cursors, ETags, counts or zero placeholders while withheld; own/protective lanes remain bounded. Register only actual new operations through P072 if existing operations cannot carry the contract. Local checkpoint 2026-10-24: the bounded view (up to 100 entries per own/peer lane) and registered adapters are implemented; mixed raw reads/streams/reference-signing probes refuse unbound access. Rich pagination, wider consumer qualification and separately privileged viewer-safe inspection remain future work. Review implementation uses a default-deny route allowlist, record-marker/POST refusal, pre-read UI/Agent admission and one attention exclusion policy; bounded coverage remains explicit. |
| P026-008 | Local exposure acceptance | partial | 007; P013-AE-001; P057-014; P073 assessment-exposure-observations | Source-pinned host/API/no-JS and JS browser evidence passes the local cases above, including notifications, Agent identity, leak matrix, rebuild and retention. Local-display-only scope remains explicit; no sealed-round or social-effectiveness claim. Original run 04 qualifies nine local host/API/UI/CLI cases and real JS/no-JS browsers. Component/synthetic-host Agent and notification fixtures are recorded separately. The full joint P013/P057/P073 matrix and wider transport/profile qualification remain open. Review run 01 adds the new refusal/window witnesses at clean Node 91babeb0 / Orbidocs 414acd72; independent v2 and 38 negative verifier cases agree before and after extraction. |
| P026-009 | Shared commitment and barrier mechanics | todo | 005 round contracts | Reuse canonical JSON/crypto, signer and durable owner primitives. Prove salt/domain isolation, exact transport bytes, bounded accepted-set closure, admission receipts, forks/equivocation, explicit deadlines and replay. Library mechanics do not count as an implemented domain publication barrier. |
| P026-010 | Agora sealed-round owner and projections | todo | 009; 007 | Implement four admitted record kinds, owner/CAS/outbox, protected local body/salt retention and round-aware projection with per-commitment outcomes. Unknown kinds remain unindexed by legacy opinion consumers; no private governance/Room payload is forced into public Agora. |
| P026-011 | Sealed-round adversarial acceptance | todo | 010 | Retain round cases above through real signer, relay, owner and viewer APIs; test cutoff races, omitted receipted entries, forked authority, abort, missing history, restart and bounds. Public transport qualification remains scoped; P051/P069 bindings require their own evidence and are not prerequisites for local-gate delivery. |
| P026-012 | Provision represented local callers | todo | Identity host; P073; P066; P026-005 | Freeze the accountable participant, authenticated module selector, consent/delegation basis, exact permitted scope, bounded expiry, revocation and restart semantics before implementation. Reuse caller-binding ownership, never trust module-supplied participant/ref or a passport merely sharing a key. Retain real operator admission/revocation evidence and audit without exposing secrets. Q-02 harness admission does not close this gate. |

## Open Questions

No unresolved questions remain for the original opinion slice. The decisions
below record its approved defaults; the planned exposure continuation has its
own freeze questions in section 6, without reopening those baseline decisions.

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
