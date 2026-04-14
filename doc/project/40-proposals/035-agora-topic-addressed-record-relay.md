# Proposal 035: Agora — Topic-Addressed Record Relay and Shared Record Substrate

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/normative/20-vision/en/VISION.en.md` (Memarium, Swarm)
- `doc/project/60-solutions/SOLUTIONS.en.md`
- `orbidocs/AGENTS.md` (Node-attached roles)

## Status

Draft

## Date

2026-04-11

## Executive Summary

Orbiplex today has several subsystems that each maintain their own
append-only, signed, topic-shaped state:

- the seed directory replicates capability passports and service offers,
- the offer catalog holds federated offer listings,
- `resource-opinion.v1` from proposal 026 authors opinions about external
  resources with no shared substrate to store or retrieve them,
- and `whisper-signal.v1` from proposal 013 dispatches privacy-bounded social
  rumors without any durable query surface.

Every one of these subsystems invents its own *topic*, its own *relay*, its
own *replication rhythm*, and its own *query API*. The consequence is that
adding one more kind of shared record — a comment under a URL, a note under a
product, a public log entry under a workflow run — means designing one more
bespoke store.

This proposal introduces one neutral substrate:

- **Agora** — a topic-addressed, append-only, signed *record* relay, operated
  by umbrella operators and consumable by any Node.

And one neutral envelope:

- `agora-record.v1`

The key decisions are:

1. a record is a signed, timestamped, content-addressed artifact authored by
   a participant and placed under one *topic*,
2. a topic is addressed by an **opaque** `topic/key` string; the substrate
   does not interpret, type, or split it, and no single use case owns the
   shape of topic keys,
3. the record envelope is extensible by `record/kind` and `content/schema`,
   so that opinions, comments, public logs, offer snapshots, or swarm
   gossip can all live side by side under one transport contract,
4. when a record is meaningfully *about* an external subject (a URL, a
   product, a node, an org), it MAY carry an optional `record/about` list
   that references the resource identity model from proposal 026; this
   relation is orthogonal to topic placement and is *not* used as the
   primary key,
5. Agora relays are umbrella-operated and federated, following the same
   operational pattern as the seed directory (proposal 025) and the offer
   distribution layer (proposal 023),
6. Matrix (via a dedicated homeserver deployment) is the reference backend
   for the first implementation, but the `agora-record.v1` envelope is
   backend-neutral and a later native transport may replace or complement it.

Agora is **orthogonal** to Memarium. Memarium, as described in the vision
document, is the curated memory-and-knowledge layer that decides *what must
not disappear*. Agora is a lower primitive: a durable, citeable log of
public records indexed by topic. A community-scale Memarium space may *use*
Agora as one of its underlying substrates, but it is not the only one and
Agora does not depend on Memarium being present.

## Context and Problem Statement

Several existing proposals implicitly demand a public, topic-addressed,
append-only substrate:

- **Proposal 013** (Whisper) defines a privacy-bounded rumor flow. Rumors are
  ephemeral by design and therefore do not need Agora, but the interest
  semantics and the threshold-reached events can cleanly degrade into durable
  records once a threshold is crossed.
- **Proposal 023** (federated offer distribution) is a domain-specific
  append-only replication layer. It works, but it reinvents parts of what
  Agora would provide once, centrally.
- **Proposal 025** (seed directory as capability catalog) is a similar
  replication layer with a different payload shape and a different query
  model.
- **Proposal 026** (resource opinions) defines the opinion artifact and the
  generic resource identity model, but explicitly leaves the storage and
  discussion surface as a later attached layer.

Three separate systems, three separate relay mechanisms, three separate
caches, three separate federation rhythms, three separate retention rules.
The cost of adding the fourth one — comments on proposal pages, public notes
under workflow runs, shared annotations under a code artifact — is
disproportionately high.

The missing contract is not a schema. The missing contract is one neutral
substrate that any future topic-shaped record can sit on without rewriting
the transport.

### What is absent today

| Need | Current state |
|---|---|
| One portable record envelope usable for many record kinds | Not present |
| A generic, backend-neutral topic addressing model shared across subsystems | Not present; each subsystem invents its own (proposal 026's resource identity addresses *subjects*, not topics, and is orthogonal to this question) |
| One umbrella-operated relay role for topic replication | Per-subsystem ad hoc |
| Subscription and replay under one topic | Per-subsystem ad hoc |
| A stable place for comments, public annotations, long-lived notes | Missing |
| A substrate for the community layer of Memarium | Missing |

## Goals

- Define one neutral, signed, content-addressed record envelope
  (`agora-record.v1`) suitable for many record kinds.
- Address topics by an **opaque** `topic/key` string, so that the substrate
  never has to interpret, type, parse, or split topic identifiers, and no
  single use case dictates their shape.
- Keep resource identity (proposal 026) as an *orthogonal* axis, reachable
  through an optional `record/about` field, so that the two questions
  *where is this record?* and *what is this record about?* remain cleanly
  separated.
- Define the role of an *Agora topic relay* and its federation responsibilities.
- Define one minimal query and subscription API that any Node can call.
- Pick a reference backend (Matrix homeserver) but keep the envelope backend-
  neutral.
- Leave room for migrating existing subsystems (offer catalog, opinion
  storage) onto Agora without breaking them.

## Non-Goals

- This proposal does not define how Memarium curates, indexes, or retrieves
  records semantically. Memarium remains a separate primitive.
- This proposal does not define E2E-encrypted private topics. Agora records
  are public-by-default at the relay level; private channels are a later
  proposal.
- This proposal does not define moderation, sanctions, or content policy.
  Those attach to record kinds, not to the substrate.
- This proposal does not mandate Matrix. Matrix is picked as the reference
  backend to avoid inventing a new transport before the envelope is proven.
- This proposal does not migrate existing offer catalog or seed directory
  storage onto Agora. That migration is a later decision, discussed under
  Consequences.

## Decision

### 1. Record Identity and Addressing

Every Agora record MUST be addressable by the pair:

- `topic/key` — an opaque string identifying the topic under which the
  record lives,
- `record/id` — a content-addressed identifier of the record itself.

#### 1.1. Topic Key

`topic/key` is an **opaque** UTF-8 string. The substrate MUST NOT:

- parse `topic/key` for internal structure,
- split it on any delimiter,
- attach type semantics to any prefix or suffix,
- assume URI, URN, hierarchical, or resource-identity semantics.

The substrate MUST enforce only the following canonicalization rules:

- Unicode NFC normalization,
- printable characters only; control characters (C0, C1, DEL) are rejected,
- leading and trailing whitespace is rejected (not trimmed),
- maximum length of 512 bytes after UTF-8 encoding,
- empty `topic/key` is rejected.

Applications choose their own topic-key conventions. Common patterns
include:

- namespace-prefixed path-like strings, for example
  `orbiplex/proposals/035`, `mycompany/build-log`,
- random or content-derived identifiers, for example
  `01JRCY0Y7T4Y9JQK8K7R6K4M3M` or `sha256:4b7c...`,
- human-readable channel names scoped by operator, for example
  `example-coop/announcements`.

Applications that want topics derived from resource identity (proposal 026)
MAY construct topic keys that embed the resource identity as a substring
(for example `opinions/url/sha256:4b7c...`), but this is a convention of
the *record kind contract*, not a rule of the substrate.

Two applications that pick the same `topic/key` will share a topic. The
substrate does not enforce global namespacing; applications SHOULD use
operator- or project-scoped prefixes to avoid collisions. Kind contracts
MAY require stricter prefixes.

#### 1.2. Record Identifier

`record/id` is a content-addressed identifier computed as:

- `record/id = "sha256:" + base64url-no-pad(sha256(canonical-json(record-without-id-signature-and-relay-fields)))`

This matches the Orbiplex canonical hash convention already used by
`node/capability/src/lib.rs::sha256_base64url` for signed artifacts and
passport hashes, so that a single content-address prefix covers both the
capability layer and the record layer.

Content addressing is necessary so that citations across relays, mirrors,
and cached views reliably resolve to the same record regardless of which
relay served it.

#### 1.3. Optional Subject Reference

A record MAY carry an optional `record/about` field that links the record
to one or more external subjects using the resource identity model from
proposal 026:

```json
"record/about": [
  { "resource/kind": "url", "resource/id": "https://example.org/article" },
  { "resource/kind": "ean", "resource/id": "5901234123457" }
]
```

Rules:

- `record/about` is OPTIONAL and MAY be empty or absent.
- When present, each entry MUST follow the resource identity rules from
  proposal 026.
- `record/about` is **not** a topic key and MUST NOT be used as the primary
  index by the substrate. It is a secondary, optional index that enables
  cross-topic queries of the form *show me every record about this
  subject, regardless of where it was posted*.
- A kind contract MAY require `record/about` to be present for records of
  a given `record/kind` (for example `opinion` records MAY be required to
  carry exactly one `record/about` entry). The substrate itself does not
  enforce such rules.

### 2. `agora-record.v1` Envelope

The MVP envelope is:

- `schema = "agora-record.v1"`

Required fields:

- `schema`
- `record/id`
- `record/kind`
- `topic/key`
- `author/participant-id`
- `authored/at`
- `content/schema`
- `content`
- `signature`

Optional fields:

- `record/about` — list of `{ resource/kind, resource/id }` entries naming
  external subjects this record refers to (see section 1.3)
- `record/parent` — one parent `record/id` when the record is a reply,
  annotation, or successor
- `record/supersedes` — one prior `record/id` replaced by this revision
- `record/tags` — short free-form tags (application use)
- `record/lang` — BCP 47 language tag
- `relay/received-at` — stamped by the relay on ingest; never part of the
  signed payload
- `relay/id` — identifier of the relay that first ingested the record

Ingest invariants:

1. `topic/key` MUST satisfy the canonicalization rules from section 1.1.
2. `record/id` MUST equal the content hash of the canonical payload with
   `record/id`, `signature`, `relay/received-at`, and `relay/id` omitted.
3. `signature` MUST be a valid Ed25519 signature by the participant key of
   `author/participant-id`, verifiable against the participant's current
   capability passport chain (proposals 024 and 032).
4. `content/schema` MUST be present and MUST name a known content schema
   identifier; relays MUST accept unknown schemas but MAY mark them as
   non-indexable until a schema contract is registered.
5. `authored/at` MUST be within the relay's configured clock skew window
   (default: ±10 minutes) relative to relay wall clock, or the record is
   flagged `clock_skew` and still stored but excluded from live query
   results until the window passes.
6. `record/parent` and `record/supersedes`, when present, MUST resolve to
   known records under the same `topic/key` or be flagged `dangling` until
   the parent appears.
7. `author/participant-id` MUST carry a currently valid participant identity;
   sanctioned or revoked participants are still stored but excluded from
   default query output.
8. `record/about`, when present, MUST follow the resource identity rules of
   proposal 026. The substrate MUST NOT derive `topic/key` from
   `record/about` and MUST NOT require `record/about` to match the topic.

### 3. Record Kinds and Content Schema Extension

`record/kind` names the *what* of the record. `content/schema` names the
*shape* of the payload inside `content`.

The envelope is generic: it does not prescribe the list of kinds, only the
registration rule. Each record kind is defined by a separate, small schema
contract that lives next to the subsystem that owns it. Examples for MVP:

| `record/kind` | `content/schema` | Owner |
|---|---|---|
| `opinion` | `resource-opinion.v1` | proposal 026 |
| `comment` | `plain-comment.v1` | Agora base kind |
| `annotation` | `plain-annotation.v1` | Agora base kind |
| `whisper-durable` | `whisper-threshold-record.v1` | proposal 013 follow-up |
| `public-log` | `public-log-entry.v1` | application use |

Rules:

- An unknown `record/kind` MUST be stored and served, but MUST be treated as
  *opaque* by the relay query layer until a schema contract is registered.
- A schema contract MUST be a separate proposal or schema file; it MUST NOT
  be merged into this proposal.
- Applications MUST NOT assume that all relays understand all kinds.

### 4. Topic Relay Role

An **Agora topic relay** is an umbrella-operated Node-attached service whose
responsibilities are:

1. **Ingest** — accept signed `agora-record.v1` records from authorized
   participants, verify them, content-address them, and write them to
   durable storage under their `topic/key`.
2. **Federate** — replicate records across peer relays according to a
   configured federation policy; relays do not have to replicate every
   topic, only the topics they carry.
3. **Serve** — expose query and subscription APIs for Nodes.
4. **Retain** — enforce per-topic retention rules (time, count, size).
5. **Exclude** — honor participant sanctions and record-level flags by
   excluding records from default query output without deleting them.

Three operational modes are defined:

- **Canonical relay** — operated by an umbrella operator, publishes a stable
  base URL, holds the durable source of truth for a set of topics.
- **Cache relay** — operated by a Node, mirrors a subset of topics for local
  availability and offline operation. A cache relay does not have to be
  reachable by other relays.
- **Origin relay** — operated by the author's Node, used to sign and first-
  ingest the record before it reaches a canonical relay. An origin relay is
  ephemeral and MAY be the same process as a cache relay.

The deployment pattern is analogous to the seed directory (proposal 025) and
the federated offer catalog (proposal 023): each umbrella operator runs one
or more canonical relays, Nodes run cache relays, and federation happens
between canonicals.

### 5. Query and Subscription API

Minimum Node-visible API contract. Every path parameter that carries a
`topic/key` MUST be percent-encoded by the caller; the substrate MUST NOT
interpret the decoded value beyond the canonicalization rules from
section 1.1.

#### 5.1. List records under a topic

```
GET /v1/agora/topics/{topic-key}/records
  ?since={cursor}
  &limit={n}
  &kind={record-kind}
  &include_flagged={bool}
```

Response:

```json
{
  "topic/key": "orbiplex/proposals/035",
  "records": [ { ...agora-record.v1... }, ... ],
  "cursor": "opaque-next-cursor",
  "more": true
}
```

Cursors MUST be opaque. Relays MAY reorder within a given time slice but
MUST be stable for a given cursor.

#### 5.2. Fetch one record by content id

```
GET /v1/agora/records/{record-id}
```

Returns the stored record or `404`. This endpoint MUST return the same
record regardless of which relay serves it, for a given `record/id`.

#### 5.3. Subscribe to live updates

```
POST /v1/agora/topics/{topic-key}/subscribe
```

Opens a streaming connection (long-poll or server-sent events in MVP;
WebSocket post-MVP) that delivers new records under the topic. The
subscription is advisory and MAY be dropped by the relay under load.

#### 5.4. Submit a record

```
POST /v1/agora/topics/{topic-key}/records
```

Body: `agora-record.v1` signed by the author. Relay verifies invariants and
returns the canonical stored record (with `relay/received-at` and
`relay/id`) or an error.

#### 5.5. Cross-topic query by subject

```
GET /v1/agora/about/{resource-kind}/{resource-id}/records
  ?since={cursor}
  &limit={n}
  &kind={record-kind}
  &include_flagged={bool}
```

Returns records whose `record/about` list contains an entry matching the
given resource identity, regardless of `topic/key`. This endpoint answers
questions like *what records across all topics refer to this URL / this
product / this node?*. It is a secondary index and MAY be served more
slowly than topic-keyed queries; relays MAY limit its result window.

This endpoint MUST NOT be used as a substitute for topic-keyed queries.
Authors who want their records to be findable under a subject SHOULD
populate `record/about` explicitly; the substrate does not synthesize
`record/about` from topic keys.

### 5.6. Local deployment channels and authentication

When Agora is attached to a Node as a supervised local service, it SHOULD expose
the Agora HTTP API on its own port rather than through the daemon's
request-response middleware proxy. SSE subscriptions are long-lived streams, and
a dedicated port lets the operator decide whether the relay API remains on
loopback or is exposed on a public interface.

The Node-attached deployment has three distinct communication relationships:

| Channel | Direction | Purpose | Token boundary |
|---|---|---|---|
| Lifecycle | daemon -> Agora | readiness, initialization, shutdown | daemon-generated middleware authtok, validated by Agora |
| Host capability API | Agora -> daemon | node identity, capability passport lookup/publication, future policy checks | daemon-generated host-capability authtok, validated by daemon |
| Agora API | UI/CLI/client -> Agora | ingest, query, fetch, subscribe | open in MVP; a separate client authtok MAY be enabled post-MVP |

The host capability API is a local, authenticated, module-initiated channel.
Agora MUST NOT implement node identity, Seed Directory publication, or
capability-passport issuance itself. It asks the daemon for those host-owned
capabilities, and the daemon remains the broker for identity and passport
policy. In concrete Node deployments this is represented by environment
variables equivalent to:

```text
ORBIPLEX_HOST_CAPABILITY_BASE_URL
ORBIPLEX_HOST_CAPABILITY_AUTH_HEADER
ORBIPLEX_HOST_CAPABILITY_AUTHTOK_FILE
```

If client authentication is enabled for the Agora API, it MUST use a token
separate from both lifecycle and host-capability tokens. Absence of such a token
means open access for development and local-only MVP operation.

### 5.7. Capability passport semantics for `agora.relay`

The middleware capability report and the capability passport are separate
facts:

- the module report declares capability: "this supervised process can serve
  `agora.relay`";
- the capability passport declares authorization: "the operator officially
  offers `agora.relay` from this node under this issuer, scope, and metadata".

Passport issuance MUST NOT be automatic merely because Agora reports
`agora.relay`. The operator issues the passport through the same host-owned
identity and capability flow used by other passport-backed capabilities. This
allows the passport to be signed by a high-assurance participant or delegated
operator key rather than by an ephemeral module identity.

Operationally:

- Agora without an `agora.relay` passport remains a valid local relay: UI, CLI,
  and local Python clients may still ingest and query records.
- Agora with an `agora.relay` passport becomes discoverable through the Seed
  Directory and eligible for federation according to local policy.
- At startup, a Node-attached Agora service SHOULD query the daemon for its
  current `agora.relay` passport through the host capability API and expose the
  result in its status surface.

The `agora.relay` passport metadata schema is defined in
`doc/schemas/agora-relay-capability.v1.md`. It includes at least the relay API
endpoint, relay role, relay domain, supported transport set, API version, and
advertised canonical topic set.

### 6. Reference Backend: Matrix

The first reference implementation of the topic relay role MUST use a
Matrix homeserver (Dendrite or Conduit are preferred for footprint reasons)
as the underlying durable substrate. Rationale:

- Matrix rooms map cleanly to Agora topics (one room per `topic/key`).
- Matrix events are already signed, content-addressed, and ordered in a DAG,
  which matches the `agora-record.v1` invariants.
- Matrix federation provides cross-relay replication without Orbiplex having
  to invent transport.
- Matrix is already cited as prior inspiration for Orbiplex's messaging
  strata.

Mapping rules:

1. A topic MUST be represented as a Matrix room. The room alias MUST be
   derived deterministically from the opaque `topic/key` using a fixed
   transformation, so that the same topic resolves to joinable rooms on
   every relay that carries it. The MVP derivation is:

   ```
   alias = "#agora." + lowercase-hex(sha256(topic/key)) + ":" + relay-domain
   ```

   The hash is computed over the UTF-8 bytes of the already-canonicalized
   `topic/key`. Lowercase hex is used here — rather than the canonical
   Orbiplex `sha256_base64url` convention used for `record/id` — because
   the Matrix room-alias localpart is case-insensitive and restricted to
   `[a-z0-9._=/+-]`; base64url would introduce uppercase letters that
   Matrix would silently fold, breaking deterministic resolution. The
   choice is a Matrix-compatibility concession, not a second content
   address: the authoritative record identifier remains `record/id`.
   Relays MUST NOT derive the alias from parsed or typed parts of the
   topic key; the key is treated as an opaque byte string by the
   derivation function.
2. The relay MUST maintain a separate mapping from `topic/key` to
   human-readable Matrix room names for operator tooling. This mapping is
   advisory; it MUST NOT be used as the canonical identifier of the topic.
3. An `agora-record.v1` MUST be serialized into a Matrix event of type
   `org.orbiplex.agora.record.v1` whose `content` field carries the full
   record envelope including `topic/key` and, when present,
   `record/about`.
4. `record/id` is computed from the Agora canonical payload, not from the
   Matrix `event_id`. Consumers MUST index by `record/id` for citation.
5. The Matrix homeserver's own event signature provides relay-level
   authority; the Orbiplex `signature` field provides author-level
   authority. Both MUST be verified.
6. Matrix E2E encryption MUST be disabled on Agora rooms in MVP; Agora
   records are public by default.
7. The cross-topic `record/about` index from section 5.5 is maintained by
   the relay *outside* the Matrix room model, as a secondary index over
   ingested events. Matrix itself is not asked to answer subject-based
   queries.

The envelope is backend-neutral. A later native Orbiplex transport may
replace Matrix for topics that must not leave the Orbiplex federation, but
such a transport is out of scope for this proposal.

### 7. Retention

Retention is configured per topic and per record kind, with relay-level
defaults. Minimum retention policy dimensions:

- `max_age` — oldest allowed record age,
- `max_count` — maximum number of records kept per topic,
- `max_bytes` — maximum total size per topic,
- `pin_by_kind` — kinds that MUST NOT be evicted regardless of age or count.

The relay MUST expose the active retention policy for every topic via
`GET /v1/agora/topics/{topic-key}/retention`. Authors MAY submit records
that exceed policy; the relay MAY reject, truncate, or accept-and-evict
depending on configuration, but MUST return a clear error in the reject
case.

Retention does not imply deletion from origin relays. Content-addressed
records may persist in cache relays or in participant-local archives even
after a canonical relay evicts them.

### 8. Sanctions and Exclusion

Agora is a substrate, not a moderation engine. It honors two exclusion
signals without defining policy:

1. **Participant revocation** — records authored by a participant whose
   current capability passport chain is revoked MUST be excluded from
   default query output. The records are retained so that audit queries
   (`include_flagged=true`) can still reach them.
2. **Record-level flags** — a separate artifact (out of scope for this
   proposal) may flag a record as `hidden`, `under-review`, or `withdrawn`.
   Relays MUST honor these flags in default query output. Flag artifacts
   MUST be content-addressed and verifiable themselves.

No substrate-level moderation is defined. Kind-specific moderation rules
belong in the schema contract for that kind.

## Record Envelope Examples

An opinion about a URL. The topic is a named channel dedicated to URL
opinions; the subject relation is carried in `record/about`:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:4Q7x3kCDfm2yVwrbn8Hj5tlsOe9zApiU6Gq3wXYAbCd",
  "record/kind": "opinion",
  "topic/key": "orbiplex/opinions/url",
  "record/about": [
    { "resource/kind": "url", "resource/id": "https://example.org/article" }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "opinion/id": "opinion:resource:01JRCY0Y7T4Y9JQK8K7R6K4M3M",
    "resource/kind": "url",
    "resource/id": "https://example.org/article",
    "body/text": "Useful overview, but the sourcing is thin in the final section.",
    "body/lang": "en",
    "rating": 3
  },
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

The same opinion, placed instead under a per-URL topic (an alternative
convention some applications may prefer). The substrate accepts both
shapes; which one to use is a decision of the kind contract for
`record/kind = "opinion"`:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:4Q7x3kCDfm2yVwrbn8Hj5tlsOe9zApiU6Gq3wXYAbCd",
  "record/kind": "opinion",
  "topic/key": "orbiplex/opinions/url/sha256:4b7c9fzkMyAL8GBfQExamplePerUrlTopic01",
  "record/about": [
    { "resource/kind": "url", "resource/id": "https://example.org/article" }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": { "...": "..." },
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

A plain comment in a general channel. No external subject, no
`record/about`:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:Zp2m9ThKqgX4r7v8C5n1Yb6jD3WlFsTaephQkU2mov8",
  "record/kind": "comment",
  "topic/key": "orbiplex/announcements",
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T09:00:00Z",
  "content/schema": "plain-comment.v1",
  "content": {
    "body": "Agora MVP landed on canary relay.",
    "lang": "en"
  },
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

A comment thread under a proposal. The topic is freely named by the
publishing application; the parent link points to the first record in the
same topic:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:TH7q1WknMyAL8GBfQC5XrExampleThreadStart01",
  "record/kind": "comment",
  "topic/key": "orbiplex/proposals/035/discussion",
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T10:30:00Z",
  "content/schema": "plain-comment.v1",
  "content": {
    "body": "Retention rules should be configurable per record kind, not only per topic.",
    "lang": "en"
  },
  "record/parent": "sha256:PR0p05kFtQYABcD1eFgH2iJKlMnOpExampleParent9",
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

A public log entry produced by a workflow run. The topic is derived from
the run identifier, and there is no external subject to reference:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:WF001rk5d8m2hxQP4N7bT6vLYcFj3gsOwueazR9ikmt",
  "record/kind": "public-log",
  "topic/key": "orbiplex/workflow-runs/01JRCY0Y7T4Y9JQK8K7R6K4M3M",
  "author/participant-id": "participant:did:key:z6MkWorkflow",
  "authored/at": "2026-04-11T11:00:00Z",
  "content/schema": "public-log-entry.v1",
  "content": {
    "step": "fan-out",
    "outcome": "any_one_satisfied",
    "dispatch_count": 3
  },
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

## Hard MVP Scope

| Feature | MVP |
|---|---|
| `agora-record.v1` envelope | Yes |
| Content-addressed `record/id` | Yes |
| Opaque `topic/key` with canonicalization rules | Yes |
| Optional `record/about` linking to proposal 026 resource identity | Yes |
| Cross-topic query by `record/about` (secondary index) | Yes |
| Matrix backend (Dendrite or Conduit) | Yes |
| Three relay roles (canonical, cache, origin) | Yes |
| Query by topic with cursor | Yes |
| Fetch by `record/id` | Yes |
| Subscribe via long-poll or SSE | Yes |
| Retention: age + count | Yes |
| Retention: size + pin-by-kind | Deferred |
| Record-level flags and hidden/withdrawn handling | Deferred |
| E2E-encrypted private topics | Deferred |
| Kind-specific schema registry | Deferred |
| Native Orbiplex transport (non-Matrix) | Deferred |
| WebSocket subscription | Deferred |

Deferred items are post-MVP and MUST NOT be implemented before the MVP
scope is clean and tested.

## Interaction With Existing Proposals

| Proposal | Relation |
|---|---|
| 013 — Whisper social signal exchange | Whisper rumors stay ephemeral; threshold-reached events become an optional `whisper-durable` record kind on Agora |
| 023 — federated offer distribution | The offer catalog today maintains its own storage; a future migration may express offer snapshots as Agora records under an operator-chosen topic key (for example `orbiplex/offer-catalog`) with `record/kind = "offer-snapshot"`, retiring the bespoke replication layer |
| 024 — capability passports | Author signatures on Agora records are verified via the same passport chain |
| 025 — seed directory as capability catalog | Seed directory remains a separate primitive for capability discovery; it MAY later publish its listings as records on an Agora topic for uniform federation |
| 026 — resource opinions and discussion surfaces | Proposal 026 remains the single source of truth for resource identity (`resource/kind` + `resource/id`). Agora does not embed resource identity in its primary key; it reaches proposal 026 only through the optional `record/about` field. `resource-opinion.v1` becomes the first `content/schema` on Agora, with `record/kind = "opinion"`, and opinion records carry the referenced resource in `record/about` |
| 032 — key delegation passports | Delegated signing keys used for authoring Agora records follow the passport verification rules |
| 034 — node operator binding | Orthogonal. Agora does not participate in operator assurance gating |

## Relationship to Memarium

Memarium, as defined in the vision document, is the **memory-and-knowledge
layer**: curated archives, community resources, cultural artifacts, with
federation, replication, versioning, durability rules, and semantic
retrieval. Memarium answers the question *what must not disappear*.

Agora is a narrower primitive. It answers the question *where do topic-
addressed public records live and how are they federated*. It is a
substrate, not a curator, and it makes no decisions about what is worth
preserving.

The relationship:

- A community-scale Memarium space MAY use Agora as one of its underlying
  substrates for the ingestion of public records into the community layer.
- Memarium's private and personal spaces are out of scope for Agora.
  Personal notes, idiolectal archives, and private working spaces belong in
  a Node-local store.
- Memarium curation (indexing, semantic search, summarization) happens *on
  top of* Agora records or Node-local stores, not inside the substrate.
- A Node may run a cache relay for Agora without running any Memarium
  component, and vice versa.

When a separate Memarium proposal lands, it will describe how curation
attaches to Agora records and Node-local stores, and will not redefine
Agora.

## Implementation Notes

The suggested first implementation path is:

1. **Relay shell** — a Rust service that wraps a Dendrite or Conduit
   homeserver, exposes the Agora HTTP API, and translates calls into Matrix
   room operations.
2. **Record verification library** — a standalone Rust crate that encodes
   the canonical JSON rules, computes `record/id`, verifies signatures, and
   enforces ingest invariants. Reusable across relay, Node, and any future
   native transport.
3. **Node client** — a thin client in `node/agora-client` that lets the
   daemon submit, query, subscribe, and cache.
4. **Middleware seam** — Agora relay may run as a middleware-attached
   service on an umbrella operator's Node, following the same supervision
   pattern as proposal 019 (supervised local HTTP-JSON middleware).

The first concrete migration target is proposal 026: serve resource
opinions through Agora as `record/kind = "opinion"` with
`content/schema = "resource-opinion.v1"`.

### Implemented crate architecture

The implementation follows a stratified layering, where each crate has a
single responsibility and communicates through thin trait or data
contracts:

```
L4.b  agora-http             REST/SSE surface (framework-neutral)
L4.a  agora-relay-matrix     composition: SQLite store + Matrix transport
L3    agora-matrix-client    MatrixRelayTransport<S: MatrixEventSink>
      agora-matrix           pure data bridge (alias, content translation)
L2    HttpMatrixEventSink    thin Matrix CS API sink (reqwest + ruma types)
L1    MatrixCsClient         typed join/send/sync over Matrix CS API
L0    AuthenticatedHttpClient bearer-auth HTTP + rate-limit retry
      agora-relay-sqlite     persistent local relay (SQLite WAL)
      agora-relay-mem        in-memory reference relay
      agora-relay-trait      AgoraRelayTransport / AgoraRelay / SequencedRecord
      agora-core             envelope verification, canonical JSON, signatures
```

#### Matrix transport: thin HTTP sink

The Matrix transport uses `reqwest::blocking` and `ruma 0.14.1` (types
and endpoint definitions only, feature `client-api-c`) plus a small
hand-written Client-Server HTTP wrapper. This keeps the transport
auditable, avoids a full client state machine, and keeps Agora relay
semantics in the relay crates rather than in a Matrix runtime. The
`MatrixEventSink` trait decouples `MatrixRelayTransport` from the
concrete HTTP implementation while preserving a single production path
for the MVP.

Three Matrix CS API endpoints are used:

- `POST /_matrix/client/v3/join/{roomIdOrAlias}` — idempotent room join
- `PUT /_matrix/client/v3/rooms/{roomId}/send/{eventType}/{txnId}` —
  send event with Agora `record/id` as deterministic `txnId` for
  server-side idempotency
- `GET /_matrix/client/v3/sync` — one global long-poll loop per sink,
  events demultiplexed to per-(room, event_type) subscribers

#### Federated relay composition (L4.a)

`MatrixBackedRelay<S: MatrixEventSink>` composes `SqliteRelay` (local
persistent store) with `MatrixRelayTransport<S>` (federation channel)
and implements the full `AgoraRelay` trait (ingest + subscribe + query +
fetch). Key properties:

- **Local-first ingest**: records are persisted in SQLite before being
  forwarded to Matrix. Matrix failure does not block local persistence.
- **Forward-only-fresh**: duplicate records (by `record/id`) are not
  forwarded to Matrix, preventing redundant federation traffic.
- **Relay metadata stamping**: `relay/received-at` (RFC 3339 UTC) and
  `relay/id` are stamped by the relay on every ingest, as specified in
  section 2. These fields are excluded from content address and
  signature (via `VerifiedRecord::with_relay_metadata`), so stamping
  does not break the envelope invariant.
- **Inbound bridge**: a background thread per topic subscribes to the
  Matrix transport, verifies inbound events, and ingests them into the
  local store. The bridge starts lazily (Cache mode) or eagerly
  (Canonical mode) and includes a cooldown to prevent tight respawn
  loops on transport failure.
- **Retention sweep**: `sweep_retention()` enforces `max_age` and
  `max_count` per topic, then rebuilds the subject index to prune
  evicted entries.
- **Three relay roles** are configuration, not separate implementations:
  `Canonical` (eager inbound bridges for configured topics), `Cache`
  (lazy bridges on first subscribe/query), `Origin` (outbound only).

#### Subject index (L4.a internal)

The cross-topic `record/about` index from section 5.5 is implemented as
a `SubjectIndex` trait internal to `agora-relay-matrix`. It is populated
as a side-effect of ingest and queried by the HTTP API for subject-based
lookups. The MVP implementation is in-memory (`InMemorySubjectIndex`)
and rebuildable from the local SQLite store via
`rebuild_subject_index()`. The index is idempotent: re-indexing the same
record is a no-op. The trait supports `clear()` for rebuild cycles
triggered by retention sweeps or process restarts.

#### HTTP API surface (L4.b)

`agora-http` is a framework-neutral adapter that maps proposal 035 §5
endpoints to `AgoraRelay` + `SubjectIndex` calls. It depends on no HTTP
framework (`axum`, `hyper`, `actix-web`); a daemon or middleware layer
wraps it in actual HTTP routing. Key design choices:

- **Opaque cursors**: pagination uses base64url-encoded sequence numbers.
  Clients must treat cursors as opaque strings. The `Cursor` type
  encodes/decodes on the HTTP boundary; relay internals use bare `u64`
  sequences via `SequencedRecord`.
- **SSE for subscriptions**: `SseRecordStream` formats verified records
  as standard Server-Sent Events (`event: agora.record`, `id:
  {record/id}`, `data: {json}`).
- **Topic mismatch validation**: `POST /topics/{topic-key}/records`
  rejects records whose `topic/key` does not match the URL path.
- **Partial about-filter rejection**: when exactly one of `about_kind`
  or `about_id` is present, the API returns an explicit error instead of
  silently ignoring the filter.
- **`include_flagged` wire compatibility**: the parameter is accepted
  but has no effect in MVP; flag semantics are deferred per section 8.

### MVP implementation status vs this proposal

#### Implemented

- **Envelope verification** (`agora-core`): content address, Ed25519
  signature, schema version, topic key syntax (empty, length,
  whitespace, control chars). Cross-language fidelity verified against
  a Python verifier (`agora-verifier` middleware module).
- **Local relays** (`agora-relay-mem`, `agora-relay-sqlite`): ingest
  with idempotent duplicate detection, per-topic append log, monotonic
  sequence assignment, `QueryFilter`-based query with `SequencedRecord`
  results, replay-capable subscriptions, fetch by `record/id`.
- **Relay metadata stamping**: `relay/received-at` and `relay/id`
  stamped by the federated relay (`agora-relay-matrix`) on ingest, via
  `VerifiedRecord::with_relay_metadata()` which preserves the envelope
  invariant (relay fields are excluded from content address and
  signature).
- **Matrix transport** (`agora-matrix-client`): thin HTTP sink using
  `reqwest::blocking` + `ruma 0.14.1` types. Three CS API endpoints
  (join, send with deterministic `txnId`, global sync with demux).
- **Matrix data bridge** (`agora-matrix`): deterministic room alias
  derivation (`#agora.<hex-sha256-nfc>:<domain>`), event type
  `org.orbiplex.agora.record.v1`, bidirectional record ↔ event content
  translation with full envelope verification on inbound.
- **Federated relay** (`agora-relay-matrix`): `MatrixBackedRelay<S>`
  composing SQLite + Matrix transport. Local-first ingest,
  forward-only-fresh, lazy/eager inbound bridges with cooldown,
  three relay roles (Canonical/Cache/Origin), retention sweep
  (`max_age`, `max_count`).
- **Subject index** (`agora-relay-matrix`): in-memory `SubjectIndex`
  for cross-topic `record/about` queries, idempotent, rebuildable from
  local store.
- **HTTP API surface** (`agora-http`): framework-neutral adapter for
  proposal 035 §5 endpoints. Opaque cursors, SSE subscriptions, topic
  mismatch validation, partial about-filter rejection.
- **Retention** (age + count): `sweep_retention()` with automatic
  subject index rebuild after purge.

#### Deferred ingest invariants

The following invariants from section 2 use "flag, not reject" semantics
in this proposal and are not blocking for the first deployment:

- **Invariant 5** (`authored/at` clock skew window) — not checked; the
  field is validated as non-empty only.
- **Invariant 6** (`record/parent` / `record/supersedes` dangling
  detection) — not checked; the fields are accepted structurally.
- **Invariant 7** (passport chain verification via proposals 024 and
  032) — the signature is verified against the direct participant key
  only; delegated signing keys are not yet supported.
  `signature.key/ref` is defined in the schema but not yet represented
  in the Rust `AgoraSignature` struct.
- **Invariant 8** (`record/about` resource identity structural
  validation per proposal 026) — the array is accepted structurally;
  individual entries are not validated against `resource-ref.v1`.
- **Schema-level patterns** (`record/kind`, `content/schema`,
  `record/id` length bounds) — not enforced by the verification
  library; the library checks non-empty semantics only. Schema-level
  validation is a relay-side concern.
- **Topic key NFC normalization** — the verification library checks
  syntax only (empty, length, whitespace, control chars). NFC
  normalization is applied by the canonical JSON layer before hashing
  and signing, so content addresses are stable regardless of input NFC
  form, but the relay does not currently reject or normalize non-NFC
  topic keys at the ingest boundary.

#### Not yet wired

- **Daemon integration**: the HTTP API (`agora-http`) and federated
  relay (`agora-relay-matrix`) are not yet wired into the Node daemon
  control flow. The crates are self-contained and tested but require a
  daemon-level lifecycle hook to start inbound bridges and expose the
  REST/SSE surface.
- **Retention scheduling**: `sweep_retention()` is a callable primitive
  but is not yet driven by a periodic timer or cron-like scheduler.
- **Subject index persistence**: the in-memory `SubjectIndex` does not
  survive process restarts. `rebuild_subject_index()` reconstructs it
  from the local SQLite store on startup, but a SQLite-backed subject
  index would eliminate the rebuild cost.
- **Room-to-topic name mapping** (section 6, rule 2): the relay does
  not yet maintain a human-readable room-name mapping for operator
  tooling.

## Consequences

Positive:

- one portable record envelope replaces several bespoke storage contracts
  across future subsystems,
- proposal 026 gains a concrete storage and federation substrate without
  having to invent one,
- the offer catalog and seed directory gain a future migration target if
  umbrella operators want to consolidate replication on one substrate,
- Matrix reuse avoids inventing a federation transport,
- topic addressing is unified with resource addressing across Orbiplex.

Tradeoffs:

- introducing Matrix as a backend adds an operational dependency for
  umbrella operators running canonical relays; Nodes running cache relays
  can avoid it via HTTP-only cache mode,
- Agora records are public by default in MVP, which forces applications
  that need private channels to wait for a later proposal,
- content addressing forces strict canonical-JSON discipline on authors;
  any post-signature mutation invalidates the record,
- the offer catalog currently maintains its own storage; migration is a
  future decision, not a hard requirement of this proposal.

## Alternatives Considered

- **NATS JetStream as backend.** Rejected because NATS is optimized for
  low-latency messaging, not citeable archive state, and because its
  cluster model assumes trusted operators rather than cross-umbrella
  federation. A later proposal may add JetStream as an optional backend for
  latency-sensitive record kinds that do not require long-term archival.
- **Invent a native transport from the start.** Rejected because the
  envelope value is independent of the transport, and shipping the envelope
  on a proven transport first lets the schema mature before the transport
  is locked in.
- **Extend proposal 025 (seed directory) into a generic substrate.**
  Rejected because the seed directory has a specific payload contract
  (capability passports and offers) that would blur if generalized.
- **Extend proposal 023 (offer distribution) into a generic substrate.**
  Rejected for the same reason.

## Known Limitations

- MVP has no private topics. Any record submitted to Agora is considered
  public and visible to every participant that can reach the relay.
- MVP has no substrate-level moderation. Record-kind contracts must carry
  their own moderation rules.
- MVP has no formal schema registry for `record/kind`; registration happens
  through proposals and schema files.
- Matrix homeservers have their own operational footprint; small Nodes
  running cache relays only SHOULD NOT be required to run a full Matrix
  homeserver.

## Open Questions

1. Should Agora topics have a lightweight per-topic policy document (for
   example `agora-topic-policy.v1`) that constrains authorized record
   kinds, retention, and writer set, or should those constraints remain
   relay-wide?
2. Should `record/supersedes` be enforced as one-author-one-current-record
   per topic for specific kinds (for example `opinion`), or is that a
   kind-specific rule? Proposed: kind-specific, not substrate-level.
3. Should the offer catalog and seed directory migrate onto Agora?
   Proposed: not in this proposal. Evaluate after the MVP is in production
   for at least one umbrella operator.
4. Should Agora records be signable by delegated keys issued under a
   capability passport, or only by the participant root key? Proposed:
   delegated keys are allowed via proposal 032 passport chains.
5. Should the substrate offer any supported topic-key conventions (for
   example a recommended hierarchy grammar) even though it does not parse
   them, or should convention be left entirely to kind contracts?
   Proposed: publish a non-normative conventions note alongside the schema
   file, not a substrate rule.
6. Should the `record/about` cross-topic index be rate-limited or quota-
   bounded by relays to prevent abuse of subject-driven fan-out? Proposed:
   relays MAY impose result windows and rate limits, with defaults chosen
   during MVP deployment.
7. Should the relay expose a canonical federation tick rate and a
   federation lag metric, and if so, where should it be surfaced?
   Proposed: reuse the observability pattern from proposal 023.

## Follow-Up

If adopted, the next artifacts should be:

1. one schema file for `agora-record.v1`,
2. one schema file for `plain-comment.v1` as the first general-purpose
   base kind,
3. one schema file registering `resource-opinion.v1` as an Agora
   `record/kind = "opinion"`,
4. one implementation note describing the Matrix mapping and the Dendrite
   or Conduit deployment footprint,
5. one separate proposal for private (encrypted) Agora topics,
6. one separate proposal for Memarium, describing how curation attaches to
   Agora records and Node-local stores.
