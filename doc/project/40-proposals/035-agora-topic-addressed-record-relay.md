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

Related configuration work (proposed):

[Proposal 091: File-backed Configuration and Explainable Composition](091-file-backed-configuration-and-explainable-composition.md).
P091 inventories Agora's standalone configuration reader and its legacy
file-selection/error behavior, then plans shared Rust consumption and explicit
migration. This affects operator configuration, not Agora record identity,
publication authority or relay semantics. See P091-001a/010a/011/015.

## Status

Accepted

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
  `ai.orbiplex.proposals/035`, `mycompany/build-log`,
- random or content-derived identifiers, for example
  `01JRCY0Y7T4Y9JQK8K7R6K4M3M` or `sha256:4b7c...`,
- human-readable channel names scoped by operator, for example
  `example-coop/announcements`.

Applications that want topics derived from resource identity (proposal 026)
MAY construct topic keys that embed the resource identity as a substring
(for example `ai.orbiplex.opinions/url/sha256:4b7c...`), but this is a convention of
the *record kind contract*, not a rule of the substrate.

Two applications that pick the same `topic/key` will share a topic. The
substrate does not enforce global namespacing; applications SHOULD use
operator- or project-scoped prefixes to avoid collisions. Kind contracts
MAY require stricter prefixes.

The recommended namespace scheme — six named prefix classes
(`ai.orbiplex.<subsystem>/<name>`, `participant:<pid>/…`,
`node:<node-id>/…`, `federation:<fid>/…`, `local/…`, `private/…`)
plus the rules that turn those prefixes into cryptographic ownership
at the relay ingress — is defined in **proposal 046 (Agora Topic-Key
Namespace Conventions)**. That proposal is non-normative for the
substrate: `topic/key` remains opaque here; all enforcement lives in
relay policy and author-side hygiene. Deployments that adopt 046
run the one-compare core discriminator (`starts_with("ai.orbiplex.")`)
and the five-check ingest policy before any 041 attestation tiering.

#### 1.2. Record Identifier

`record/id` is a content-addressed identifier computed as:

- `record/id = "sha256:" + base64url-no-pad(sha256(canonical-json(record-without-id-signature-and-relay-fields)))`

The relay fields excluded from this payload are `relay/received-at`,
`relay/id`, and `relay/hops`.

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
- `record/policy` — one policy record reference. For comment threads this
  points to a `thread-policy` record whose `content/schema` is
  `comment-thread-policy.v1`.
- `record/tags` — short free-form tags (application use)
- `record/lang` — BCP 47 language tag
- `author/nym-proof` — when `author/participant-id` carries a
  `nym:did:key:...` pseudonymous identity (see invariant 9 below), this
  optional field carries a `nym-authorship-proof.v1`; in the M4 baseline
  the proof inlines enough `nym-certificate.v1` material to verify the current
  nym without remote lookup, while optional refs may point to longer lineage,
  audit, or reputation history. The proof is part of the signed canonical bytes
  so the binding cannot be stripped in transit.
- `relay/received-at` — stamped by the relay on ingest; never part of the
  signed payload
- `relay/id` — identifier of the relay that first ingested the record
- `relay/hops` — relay-local hop count stamped by relay implementations;
  never part of the signed payload

Ingest invariants:

1. `topic/key` MUST satisfy the canonicalization rules from section 1.1.
2. `record/id` MUST equal the content hash of the canonical payload with
   `record/id`, `signature`, `relay/received-at`, `relay/id`, and
   `relay/hops` omitted.
3. `signature` MUST be a valid Ed25519 signature by the envelope author subject
   key named by `author/participant-id`. For ordinary records this is the
   participant key and is verifiable against the participant's current capability
   passport chain (proposals 024 and 032). For records whose kind permits
   pseudonymous authorship, invariant 10 defines the nym-key path.
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
7. `author/participant-id` MUST carry a currently valid author subject:
   normally `participant:did:key:...`, or `nym:did:key:...` only when the record
   kind explicitly permits pseudonymous authorship. Sanctioned or revoked author
   subjects are still stored but excluded from default query output.
8. `record/about`, when present, MUST follow the resource identity rules of
   proposal 026. The substrate MUST NOT derive `topic/key` from
   `record/about` and MUST NOT require `record/about` to match the topic.
9. `record/policy`, when present, MUST resolve to a known policy record under
   the same `topic/key` or be flagged `dangling` until the policy appears.
   The substrate validates only the reference shape. Kind-specific policy
   evaluators decide whether a missing or stale policy blocks publication.
10. **Pseudonymous authorship.** `author/participant-id` MAY carry a
   `nym:did:key:...` identity in addition to a
   `participant:did:key:...` identity, when the record kind permits
   pseudonymous authorship (currently: `whisper`, see §3). In that case:
   - the envelope signature MUST be Ed25519 by the private key of the
     nym, not of any underlying participant;
   - the envelope MUST carry `author/nym-proof` containing a currently
     valid `nym-authorship-proof.v1`; in the M4 baseline this proof inlines a
     `nym-certificate.v1` (proposal 015) that binds the nym to its issuing
     council's authorization scope and can be verified without a network lookup;
   - the ingest-attestation gate (proposal 041) MUST accept the nym
     certificate in place of a participant capability passport for
     ingest admission, under the consumer-local ingest mode configured
     for the topic;
   - subject sanctions and revocations attach to the nym identity for
     the nym's bounded validity window; no attempt is made to
     retroactively correlate nym records with the underlying
     participant on the substrate layer.

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
| `thread-policy` | `comment-thread-policy.v1` | Agora base kind |
| `gossip` | `public-gossip.v1` | Agora base kind |
| `annotation` | `plain-annotation.v1` | Agora base kind |
| `whisper` | `whisper-signal.v1` | proposal 013 |
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
  "records": [ { ...agora-record.v1... }, ... ],
  "next_cursor": "opaque-next-cursor",
  "cursor_pruned": {
    "requested_from": 5,
    "first_available": 10
  },
  "query_attestation": { "...agora-query-attestation.v1...": "..." }
}
```

Cursors MUST be opaque. Relays MAY reorder within a given time slice but
MUST be stable for a given cursor.

#### 5.1a. Query attestations

Historical query responses SHOULD include an `agora-query-attestation.v1`
object under `query_attestation`.

The attestation binds:

- query mode (`topic-records` or `subject-records`),
- topic key or subject resource,
- normalized filter after URL decoding and limit defaults,
- returned `record/id` values in page order,
- `next_cursor`,
- cursor-pruning notice, if any,
- deterministic response digest.

The digest is `sha256:` over canonical JSON using the Agora NFC profile
(`jcs-nfc-sha256-base64url`). It covers the query scope, normalized filter,
returned record ids, and pagination/pruning metadata. It intentionally does
not cover local HTTP headers or transport details.

An attestation MAY be unsigned in early local relays. In that case it is still
useful as a deterministic page proof for local audit and replay comparison,
but it does not prove relay accountability. Signed deployments SHOULD sign the
canonical JSON of `agora-query-attestation.v1` with `signature` omitted.

Subject-index queries MUST attach the attestation after subscribe-policy
filtering. Otherwise the proof would describe the unfiltered subject index
instead of the response actually returned to the caller.

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
returns the canonical stored record (with `relay/received-at`, `relay/id`,
and `relay/hops`) or an error.

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

The Agora middleware SHOULD declare its own operator-facing UI surface through
the middleware module report. The host UI may mount that surface under its local
middleware namespace, but the Agora component owns the Agora-specific views and
operator vocabulary. A Node-attached Agora service SHOULD expose a local
`operator_visibility` status read model covering relay endpoint, namespace
policy, topic ACL, authority-root summary, strict gates, Matrix posture,
HTTP/SSE limits, rate-limit persistence, retention summary, passport state, and
client-auth posture. Full authority-root lists should be shown only on a
client-authenticated local operator surface; unauthenticated status responses
should expose counts and redaction markers instead. This read model is
diagnostic only; it is not a federation protocol and does not authorize publish
or subscribe operations.

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

### 5.6.1. Agora CLI TLS trust configuration

Local CLI clients MAY connect to Agora over either `http://` or `https://`
base URLs. The CLI TLS trust contract is deliberately small:

- the default HTTPS mode uses the built-in WebPKI root set and rejects
  self-signed or otherwise untrusted certificates;
- `--tls-ca-file PATH` adds one or more PEM-encoded CA certificates to
  the trust store; `ORBIPLEX_AGORA_TLS_CA_FILE` provides the same value
  from the environment, and the explicit CLI flag takes precedence;
- `--tls-insecure-skip-verify` is a diagnostic-only bypass for local
  debugging. It MUST print an operator-visible warning and MUST NOT be
  used in production.

The custom CA mode is for local labs, private CA deployments, and small
operator-controlled federations. It is not a substitute for explicit
relay identity policy. Certificate or SPKI pinning remains a future
extension for public relay deployments that need tighter endpoint
continuity than CA trust alone.

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
`doc/project/60-solutions/008-agora/agora-relay-capability.v1.md`. It includes at least the relay API
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
3. The default writer MUST carry an `agora-record.v1` in a Matrix event of type
   `org.orbiplex.agora.record.v2`, using the opaque carrier defined below. Its
   base64url author bytes retain the signed envelope, including `topic/key` and,
   when present, `record/about`, without local relay stamps. The initial default
   publication profile uses room v10. Explicit legacy configuration MAY instead
   write `org.orbiplex.agora.record.v1` with the envelope as a JSON object in
   `content`, under its integer-only number restrictions. Readers support both.
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

### Matrix carrier compatibility correction (2026-10-12)

The legacy v1 object mapping in rule 3 is narrower than Agora's payload contract.
[Matrix canonical JSON](https://spec.matrix.org/latest/appendices/#canonical-json)
allows only integer JSON numbers in `[-(2^53)+1, (2^53)-1]`, without decimal or
exponent syntax. Modern room versions enforce this restriction. A conforming
homeserver cannot carry the ordinary `public-gossip.v1` confidence value `0.5`
in the v1 event object. The observed Conduit `IntConvert` / HTTP 500 is
retained evidence of this mismatch, not a Conduit-specific protocol restriction.
The same boundary affects future accepted payloads with fractional numbers,
including applicable P096 sample content. P026-003's Matrix evidence is scoped
to integer JSON numbers (`confidence=1`).

The replacement direction is an explicitly versioned opaque Agora carrier:
Matrix stores a string containing JSON or base64url of the exact serialized
Agora envelope bytes. Decode once under a byte bound, preserve the envelope,
then apply the existing Agora signature, schema, topic and admission gates.
A Matrix room/event signature remains transport provenance, not Agora authority.
P035-004 below freezes the event type, discriminator, base64url encoding and
legacy-object read policy, and qualifies v2 with fractional confidence. The
write-default decision below adopts v2 as the normal writer and v1 as an explicit
integer-only legacy mode. JSON text remains a future encoding option.

The authoring budget must include carrier expansion and the rest of the PDU.
Base64url of 48 KiB occupies 64 KiB before wrapper or PDU metadata; escaped JSON
strings have content-dependent expansion. The old 48 KiB raw-envelope budget
therefore cannot be transferred unchanged. Derive bounded encoding and metadata
headroom and verify actual events against the [65,536-byte full-event limit](https://spec.matrix.org/latest/client-server-api/#size-limits),
including homeserver signatures. Refuse before signing/publication, without
truncation, when the selected backend budget cannot be met.

### P035-004 opaque carrier decision (2026-10-12)

**Status:** accepted design; implementation and runtime qualification are separate gates.
The transport preserves Agora author authority and auditability without imposing
Matrix's integer-only JSON model on Agora content. `agora-matrix` owns encoding;
Whisper is a consumer. The gossip and signature contracts remain unchanged.

The v2 event type is `org.orbiplex.agora.record.v2`. Its content is:

```json
{"schema":"agora-matrix-carrier.v1","envelope/encoding":"base64url","envelope/bytes":"<unpadded canonical base64url>","relay/id":"<forwarding relay>","relay/hops":1}
```

The immutable buffer contains the signed author envelope without top-level
`relay/received-at`, `relay/id` or `relay/hops`. Hop provenance is unsigned
carrier context; each relay records its own receipt time. Forwarding and replay
reuse this buffer. Typed adapters serialize once and cannot recover discarded
JSON spelling. Decode rejects padding, invalid alphabet/noncanonical trailing
bits, BOM, invalid UTF-8, trailing non-whitespace data, duplicate decoded keys
at every object level and nesting beyond 128. Verification, content schema,
topic, delegated/nym proof, admission and Whisper disclosure gates still apply.
Malformed v2 never falls back to v1. Read v1 as legacy object content without an
original-byte claim. `json-text` remains a considered future encoding only.

The original pre-release rollout decision defaulted writers to v1 and required
explicit `matrix_carrier_write_version=v2`. The write-default decision below
supersedes that policy: v2 is the adopted default and v1 is explicit legacy.
All participating readers must support v2. There is no room-state negotiation
or automatic downgrade. V1 refuses unsupported numbers before signing.
V2 transaction IDs include both version and
room: `agora.v2.<record-digest>.<room-digest>`. Device/endpoint transaction
idempotency and domain `record/id` idempotency are distinct. Publishing v2 after
v1 must create a new event; retries reuse the prepared carrier bytes.

The first profile is room v10 with the explicitly patched pinned Conduit fixture: 36 KiB author
bytes, 48 KiB base64url, 4 KiB carrier metadata and 12 KiB remaining PDU metadata,
within 64 KiB for the complete Matrix canonical JSON including signatures.
The analytical profile assumes at most 10 auth references, 20 predecessor
references, 44-byte event references, 255-byte Matrix identifiers, one origin
server, two Ed25519 signatures, 128-byte signing-key identifiers and 1 KiB of
other metadata. Count JSON escaping. These are profile assumptions, not universal
homeserver bounds. Keep the historical ingress bound of 48 KiB separate from
creation's 36 KiB; SQLite creation retains its 48 KiB limit. Pre-sign estimates
and final-byte checks precede local publication admission. Actual full PDU
exports must independently confirm the profile.

**Fixture correction (2026-10-12):** the replacement profile is
`conduit-v0.10.15-full-pdu-1`, upstream
`db3776328839604e2a1b0b0bf6cd0e8e98cf5cc5` plus the disclosed
`node:tools/matrix-fixture/opaque/full-pdu.patch`. The initial inspection found
Ruma's content-hash check, which excludes hashes, signatures and unsigned fields.
Runtime boundary testing corrected that incomplete inference: the pinned Ruma
also checks the full signed PDU, with a conservative 65,535-byte maximum;
Conduit maps this refusal to HTTP 400 `M_INVALID_PARAM`. Preserve that response
and the pinned format-check source alongside actual HTTP 413 `M_TOO_LARGE`.
The patch independently checks complete Matrix
canonical JSON after signing and unsigned assembly before persistence and returns
`M_TOO_LARGE`. Pin the source archive, builder and patch digests; retain them with
new reports. Qualification applies to this corrected fixture profile and does
not assert conformance of unmodified upstream Conduit. The historical failed
run remains evidence. See `node:tools/matrix-fixture/opaque/README.md`.

Sources are additive facts keyed by `(room,event_id)`, with author bytes,
record ID, transport context and local admission sequence. Alternative valid
bytes for one ID (including `0.50`/`0.5`) record `alternate-envelope-bytes` and
retain the first admitted source. Legacy provenance never fabricates original
bytes. Replay chooses that first retained source deterministically and reports
missing/pruned sources as incomplete. Sources and relay retention are coordinated.

One receiver owns an account checkpoint. Network, decoding and verification
happen outside the write transaction. Sources, admission decisions, diagnostics
and `next_batch` commit together under S028; index notifications follow commit.
Limited timelines trigger `/messages` backfill to the retained continuity
anchor: 64 events per page, at most eight pages per room per cycle, including
the initial current-end page. Each page commits admitted source facts, rejected
decisions and its pagination token together; verification remains outside the
transaction. Recovery retains constant-size progress, not accumulated events.
The existing 8 MiB bound limits each HTTP response, not total history. Never advance beyond an
unresolved gap; unavailable history records `matrix-history-gap` and incomplete
status. Operator replay supports `source=matrix-carriers` without forwarding.

Local HTTP 201 proves local persistence. The publication read model separately
reports `not-requested`, `pending`, `blocked`, `forwarded` or `rejected-permanent` through
record HATEOAS and `/v1/agora/records/{id}/publication`, under record-read ACLs.
Prepared publications and attempt outcomes are durable S028 facts. Size refusals
and `M_TOO_LARGE` stop retry; transient failures retain bounded retry and bytes.
`M_FORBIDDEN` is transient: three attempts use durable exponential backoff and
respect `retry_after_ms`; exhaustion becomes `blocked`. A HATEOAS POST retry
requires client authentication and topic write access and reuses the same prepared
bytes and transaction. Permanent content/size refusals cannot be requeued.
New room registration preserves the account checkpoint and triggers no-anchor
history backfill, including a non-limited timeline or absence from incremental
sync. Admission uses the same room snapshot as recovery, so registration racing
network I/O cannot establish an unrecovered anchor. Completed bootstrap stores
its start token even for an empty room; first-page facts and completion are atomic.
Preserve Matrix `sender` independently of self-declared relay identity. Optional
sender expectations produce diagnostics rather than author admission authority;
untrusted hops saturate and remain loop hints. Typed v1/v2 bridge reasons and
strict-parser reasons must not depend on diagnostic message wording.


Acceptance extends Story-008's existing report with `matrix-opaque-envelope`:
gossip confidence 0.5, proof-bearing permitted Whisper signals, trace and signed
threshold regression, exact byte variants, two clients, new-client history,
restart, crash boundaries, limited sync/backfill, carrier replay, mixed v1/v2,
malformed/proof/disclosure refusals and creation/full-PDU size boundaries.
Runtime evidence owns process observations and actual requests; conformance and
controlled `M_TOO_LARGE` fault injection are distinct classes. A consistent
fixture SQLite export supplies full PDU hashes/signatures/auth/prev references.
The export retains Conduit's original stored row separately. For room v10 the
protocol PDU omits only its local `event_id` lookup field, since the identifier
is derived from the reference hash; every remaining field is counted.
Matrix canonicalization does not apply Agora NFC. Missing Node PDU evidence,
unresolved gaps, or a Node-publication PDU above the protocol bound prevent
carrier qualification. Cross-check every Node PDU against observed `/send`
acknowledgements. Direct Client-Server boundary sends separately determine
`fixture/full-pdu-enforced`; an accepted oversized direct event is an environment
interoperability risk, not a Node publication failure or success. Preserve this
result independently and never substitute it for the Node gate. The disclosed
corrected fixture supplies a separate positive environment measurement. One
homeserver proves distribution only; it does not qualify federation, production
readiness, all Whisper surfaces or broaden historical P026 confidence=1 evidence.

**Initial measured result (2026-10-12): refused, retained unchanged.** The
implementation is present with
default-v1/optional-v2 writes. Frozen Node `31daa07c` and Orbidocs `5624bcb`
runtime evidence passes four SQLite cases and 17 of 18 Matrix cases, including
confidence 0.5, permitted Whisper signal/trace/threshold paths, exact byte variants,
restart/crash recovery, limited backfill and deterministic carrier replay.
The original combined full-PDU gate failed: pinned Conduit v0.7.0 admitted a
**65,798-byte**
complete canonical PDU above 65,536. Node's 36-KiB author boundary publications
measured 50,042/50,043 bytes; the oversized event used the separate direct
Client-Server protocol path. The qualifier refused closure, including negative
controls against falsified success markers and corrupted artifacts. Retained
reports, full PDU exports and the refusal are at
`node:docs/evidence/matrix-opaque-envelope/README.md`.
The reviewed decision separates Node publication proof from homeserver enforcement;
this initial refused run is never relabelled as qualified.

**Reviewed measured result (2026-10-12): qualified.** Frozen clean Node
`20c4c16c52021582f5536b34b9c04c514f43b323` and Orbidocs
`862586f9547d438b6b76a759505b112e214e755b` reports pass all four SQLite and
21 Matrix cases. The qualifier returns exit 0 at
`node:docs/evidence/matrix-opaque-envelope/2026-10-12-review/qualification.json`.
Host-signed/UI gossip confidence 0.5, permitted inline-proof Whisper signals
from two independent nodes, trace and host-signed threshold, exact author bytes,
restart/crash recovery, limited backfill and deterministic source replay qualify.
Review cases additionally prove durable transient backoff, blocked membership
refusal with explicit retry, late room binding recovery, and authenticated Matrix
sender provenance independent of relay declarations. Record-bound nonce receipts
already share bounded parent retention; expiry/reopen conformance preserves the
same-fact retry rule and rejects reuse for another record.

All **41 Node-created PDUs** are measured completely and matched against observed
`/send` acknowledgements; maximum **50,043 bytes**, within 65,536. Six separate
direct Client-Server boundary events reach **65,534 bytes**.
`fixture/full-pdu-enforced=true` is an independent environment finding for the
pinned, disclosed `conduit-v0.10.15-full-pdu-1` profile. Actual `M_TOO_LARGE` and
Ruma's conservative 65,535-byte `M_INVALID_PARAM` refusals retain their codes and
source provenance. Seven qualifier controls prevent replacing old failures with
success markers, missing Node PDU proof, artifact tampering and path escape.
Both backends retain 59 separate conformance tests without invented HTTP results.

This closes the carrier slice, not unmodified homeserver conformance, all Whisper,
nym issuance, Anon, federation or production readiness. The frozen run used
default-v1/explicit-v2 configuration; it does not prove the subsequently adopted
v2 default. Historical P026 confidence=1 evidence and the global Agora `partial`
assessment remain unchanged. P035-005 separately
owns positive interoperability qualification on an unmodified reference server.

### Matrix write-default decision (2026-10-12)

**Status:** accepted; implementation and default-path qualification are P035-006.
This supersedes the pre-release default-v1/optional-v2 rollout policy, without
changing P035-004's qualified transport contract or its frozen reports.

**Context:** no release or deployed infrastructure exists. Maintaining a default
object carrier that cannot carry ordinary fractional Agora content has no deployed
compatibility benefit. The opaque carrier already qualifies author-byte identity,
fractional gossip and the named Whisper families.

**Decision:** omitted `matrix_carrier_write_version` and explicit `v2` select v2.
Explicit `matrix_carrier_write_version=v1` selects legacy object writing, retaining
its pre-sign number refusals and lack of an original-byte guarantee. Readers keep
v1/v2 support for mixed histories, fixtures and retained evidence. No room-state
negotiation, silent downgrade or history rewrite is introduced. Existing prepared
publications retain their recorded carrier version, bytes and transaction ID.

**Consequences:** the initial default publication profile is still room v10 with
36 KiB author creation, 48 KiB historical Matrix ingress and the complete-PDU
budget; SQLite creation remains 48 KiB. Require v2-capable readers for new rooms.
Unsupported room profiles use the typed blocked-publication path. Other room
versions need their own profile; changing the default does not qualify them,
unmodified reference homeservers, federation or production readiness.

**Implementation gate:** the inspected Node default remains `CarrierVersion::V1`.
P035-006 changes the config/runtime defaults, fixtures and current qualifier, then
retains a clean-revision real Matrix case with the config key absent: protected
host signing of gossip confidence 0.5, v2 forwarding, B `/sync` read, restart and
carrier replay. Add explicit legacy-v1 authoring/refusal and mixed-history controls;
preserve frozen prepared publications. Use existing Story-008 report conventions,
with source and artifact integrity. Old reports retain their recorded default v1
and explicit v2 selection and cannot be relabelled as default-v2 evidence.

### Unmodified reference homeserver qualification (P035-005)

**Status:** qualified reference profile; independent Node and homeserver gates passed.
**Date:** 2026-10-13.

The reference profile selects official, unmodified Synapse v1.162.0 at upstream
`63dc0cbfe514f60743212566374ffeb5e9e295c2`, pinned image digest, PostgreSQL 16.13
and room v10. Node explicitly selects v2 until P035-006 qualifies the omitted-config
path. No homeserver patch, custom validation module or silent downgrade is allowed.
The existing 36 KiB creation and 48 KiB historical ingress profiles remain scoped.

The Story-008 `matrix-opaque-envelope` report retains two independent gates:
every acknowledged Node publication must have a complete canonical PDU within
65,536 bytes; the reference homeserver must separately refuse oversized direct
Client-Server sends while retaining accepted signed PDUs near the boundary.
Direct protocol tests do not qualify Node authoring. Actual request/response and
process observations, the pinned upstream size-check source and complete PDU
exports establish the environment result, rather than proxy or body-size limits.

A consistent read-only PostgreSQL snapshot preserves selected public storage
rows; the same stock Synapse version's room-v10 serializer exports protocol PDUs
with hashes, server signatures, auth/prev references and all protocol fields.
Matrix canonical JSON sizing does not normalize strings through Agora's NFC profile.
The runtime matrix repeats protected host signing of gossip confidence 0.5,
permitted Whisper signal/trace/threshold carriage, exact author bytes and byte
variants, A/B and homeserver/database restart, limited-sync backfill, source-based
replay without forwarding, compatibility and typed refusal/recovery controls.

P035-005 qualified at clean Node `dcc8133c` and Orbidocs `c84df99`: four SQLite
and 22 Matrix cases. Every one of the 42 acknowledged Node PDUs fits 65,536 bytes
(maximum 49,927). Seven separately attributed direct Client-Server PDUs reach
65,535; actual HTTP 413 `M_TOO_LARGE` refusals include 64,901-byte requests, proving
the gate is not merely a request-body ceiling. Content hashes, server signatures
and event IDs are verified through the stock serializer and public server keys.
Retained qualification: `node:docs/evidence/matrix-opaque-envelope/2026-10-13-synapse/qualification.json`.

The initial stock-Synapse attempt failed honestly: resetting the account cursor on
room registration could return a cached initial sync older than the durable anchor.
Node now preserves the checkpoint and bootstraps a room without an anchor through
bounded `/messages`, including rooms absent from incremental sync. Restart/offline
limited recovery and late binding both pass in the fresh qualified run. The failed
report and qualifier refusal remain retained; no Synapse validation code was changed.

P035-005 requires both gates and the runtime cases at clean frozen sibling revisions. A failed environment gate does not erase a passed
Node budget gate. Preserve original Conduit findings and patched-fixture evidence;
one unmodified server does not qualify cross-homeserver federation, all Whisper
or production readiness. Runnable fixture and exporter ownership stays in Node:
`node:tools/matrix-fixture/synapse/README.md`.

### History recovery and evidence retention decision (2026-10-13)

**Status:** accepted; Node implementation and focused conformance completed after
P035-005 qualification. This is not a new homeserver runtime qualification.

**Context and options:** collecting all recovered events imposed a deterministic
8 MiB bootstrap ceiling. An explicit operator limit would preserve that failure
for long-lived rooms. Choose incremental page admission instead: persist each
page's sources, admission decisions and progress in one S028 transaction. The
account cursor and continuity anchor advance only when its pending batch finishes.
Old buffered progress is admitted once; where it omitted the reached-anchor fact,
continuity is rechecked from the retained batch boundary. Empty completion retains
the `/messages` start token without fabricating an event ID.

**Consequences:** total history is no longer bounded by the HTTP response cap.
Crash recovery repeats at most an uncommitted page. Pages arrive backwards, with
events within a page admitted oldest first; retained source sequence expresses
local admission order, not global room chronology. First-source selection and
replay remain deterministic. Exhausting one room's page budget does not skip
the others' recovery work in that round, but one unfinished room still holds the account checkpoint, current timeline
delivery and subsequent sync batches. Eight pages per room per round plus the
five-second retry delay and request/verification time bound each round's work;
unavailable continuity has no finite account-latency bound. A failed current-end
bootstrap request can still stop batch preparation. Per-room independent
sync is a separate architectural change, not implied by this correction.

The direct regression is: skip events before a room binding, bind during prepared
I/O, receive a new event in a non-limited timeline, then backfill the old events
before establishing its anchor. Conformance also covers more than 8 MiB, resume,
empty rooms, atomic rollback, common admission and legacy progress. P035-006 must
exercise the new path on its real default-v2 profile; P035-005's original source
revisions and results remain frozen.

New public evidence larger than 256 KiB uses reviewable reports, qualification and
a complete member/hash index alongside a deterministic archive. Actual bytes stay
retained; hashes alone cannot substitute for runtime observations or PDUs. Initial
retention is in the repository, with no unowned external blob dependency. Bounded
extraction, member integrity and loose/archive qualifier equivalence must be
integrated before archived output is adopted by P035-006. The existing report
format remains unchanged. Node owns the operational convention:
`node:docs/evidence/RETENTION.md`. Do not rewrite dated loose evidence.

### Matrix Carrier Tracker

This transport continuation is independent of AD publisher migration and keeps
its status here; S008 Agora P18 links to this row.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P035-004 | Opaque Agora envelope carrier over Matrix | done | Existing Matrix mapping and Agora verification; S028 | Qualified 2026-10-12 at clean Node 20c4c16c and Orbidocs 862586f: 4 SQLite and 21 Matrix cases, confidence 0.5, permitted Whisper families, exact bytes, B `/sync` index, crash/restart/replay and review corrections. All 41 Node PDUs fit 65,536 (maximum 50,043); direct-protocol maximum 65,534 and fixture enforcement are separate observations. Retained qualification: `node:docs/evidence/matrix-opaque-envelope/2026-10-12-review/qualification.json`. That frozen run selected v2 explicitly; the adopted default-v2 policy is implemented/qualified separately in P035-006. One disclosed patched fixture does not qualify federation or production readiness. |
| P035-005 | Unmodified reference homeserver PDU interoperability | done | P035-004; room-version budget profile | Qualified 2026-10-13 at clean Node dcc8133c / Orbidocs c84df99 on official unmodified Synapse v1.162.0, PostgreSQL 16.13 and room v10: 4 SQLite and 22 Matrix cases. Separate gates pass: all 42 Node complete PDUs fit 65,536 (maximum 49,927); direct protocol maximum 65,535 and actual HTTP 413 M_TOO_LARGE, including requests below the PDU ceiling. Confidence 0.5, permitted Whisper families, exact bytes, A/B and server/database restart, limited recovery, late binding and source replay pass. Stock serializer verifies hashes, signatures and event IDs. Evidence: `node:docs/evidence/matrix-opaque-envelope/2026-10-13-synapse/qualification.json`. Initial Synapse failure, v0.7.0 finding and patched proof stay frozen; explicit v2 only, no federation or production claim. |
| P035-006 | Default v2 writer and explicit legacy v1 | todo | P035-004; accepted write-default and history-recovery decisions | Change Node/config defaults to v2; select v1 only through explicit legacy configuration. Qualify the real omitted-config confidence-0.5 sign/forward/B-sync/read/restart/replay path, explicit-v1 controls and unchanged prepared publication versions. Include page-durable long-history recovery, empty bootstrap and the non-limited late-binding path. Integrate bounded evidence archives and verify qualification equivalence after extraction. Update the current harness/qualifier under existing Story-008 contracts, retaining original default-v1 evidence. Room v10 and current byte budgets remain scoped; P035-005's original qualification remains independent and frozen. |

The envelope is backend-neutral. A later native Orbiplex transport may
replace Matrix for topics that must not leave the Orbiplex federation, but
such a transport is out of scope for this proposal.

#### 6.1. Federation trust boundary

Matrix federation is a transport and replay channel, not an admission oracle.
A receiving Agora relay MUST NOT trust a donor relay merely because the record
arrived through Matrix or because the Matrix event itself is valid. The receiving
relay MUST treat the Matrix event as a carrier for an `agora-record.v1` envelope
and run the same local admission pipeline it would run for any other inbound
record.

The receiver therefore verifies, at minimum:

1. the `agora-record.v1` envelope shape and canonical `record/id`,
2. the envelope signature, author key, nym certificate, or delegated/proxy proof,
   as applicable,
3. content-schema conformance for `content/schema`,
4. topic ACL and relay-role policy,
5. authority, capability, revocation, and custody policy required by the topic
   or record kind,
6. idempotent deduplication by `record/id`.

The Matrix homeserver signature and Matrix event id are transport provenance and
diagnostics. They may support relay health, abuse analysis, or federation trust
scoring, but they are not sufficient proof that the embedded Agora record is
valid or locally admissible.

Operationally:

```text
relay is transport
envelope is evidence
local policy is admission
```

This allows two Agora servers to synchronize accepted records without requiring
full mutual trust between relay operators. A malicious or buggy donor may deliver
bytes, but the receiver admits only records whose envelope and local policy pass.

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
  "topic/key": "ai.orbiplex.opinions/url",
  "record/about": [
    { "resource/kind": "url", "resource/id": "https://example.org/article" }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Useful overview, but the sourcing is thin in the final section.",
    "opinion/lang": "en",
    "opinion/rating": 1
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
  "topic/key": "ai.orbiplex.opinions/url/sha256:4b7c9fzkMyAL8GBfQExamplePerUrlTopic01",
  "record/about": [
    { "resource/kind": "url", "resource/id": "https://example.org/article" }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Useful overview, but the sourcing is thin in the final section.",
    "opinion/lang": "en"
  },
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
  "topic/key": "ai.orbiplex.announcements/default",
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
  "topic/key": "ai.orbiplex.proposals/035/discussion",
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

A thread policy record can be published in the same topic before the root
comment. The root comment then references it through `record/policy`. The
policy is not embedded in `plain-comment.v1`; comments carry speech, while a
`thread-policy` record carries the access rule for joining the thread.

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:PolicyPhoneConfirmedExample001",
  "record/kind": "thread-policy",
  "topic/key": "ai.orbiplex.proposals/035/discussion",
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-11T10:29:00Z",
  "content/schema": "comment-thread-policy.v1",
  "content": {
    "schema": "comment-thread-policy.v1",
    "policy/thread-topic-key": "ai.orbiplex.proposals/035/discussion",
    "policy/min-attestation": "phone-confirmed",
    "policy/inheritance": "descendants",
    "policy/may-tighten": true,
    "policy/may-loosen": false
  },
  "signature": { "alg": "ed25519", "value": "BASE64URL..." }
}
```

The effective policy for a comment is inherited from the nearest applicable
ancestor policy:

```text
root or ancestor policy
  -> child comment
  -> child may attach stricter policy for its own subtree
  -> child MUST NOT loosen inherited policy
```

Domain policy, not the Agora substrate, defines the ordering among attestation
levels such as `phone-confirmed`, `national-id`, or `community-trusted`.

A public log entry produced by a workflow run. The topic is derived from
the run identifier, and there is no external subject to reference:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:WF001rk5d8m2hxQP4N7bT6vLYcFj3gsOwueazR9ikmt",
  "record/kind": "public-log",
  "topic/key": "ai.orbiplex.workflow-runs/01JRCY0Y7T4Y9JQK8K7R6K4M3M",
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
| `agora-vault-entry.v1` encrypted opaque artifact vault | Yes |
| E2E-encrypted private topics | Deferred |
| Kind-specific schema registry | Deferred |
| Native Orbiplex transport (non-Matrix) | Deferred |
| WebSocket subscription | Deferred |

Deferred items are post-MVP and MUST NOT be implemented before the MVP
scope is clean and tested.

Hard-MVP closure note: the implemented Node runtime covers every `Yes` row in
the table above for the reference deployment, including local signing/ingest,
query, SSE subscription, Matrix-backed federation, retention, subject indexing,
and Agora Vault. The later "deferred or limited" ingest invariants remain
explicit post-MVP hardening or deployment-policy choices; they MUST NOT keep the
P035 hard-MVP tracker below completion.

## Agora Vault

Agora Vault is a separate encrypted-artifact surface, not a topic record
profile. It exists for cases where the system needs durable,
admission-controlled opaque storage but must not expose the author,
participant, nym, topic, or domain metadata that ordinary `agora-record.v1`
would reveal.

The canonical entry schema is `agora-vault-entry.v1`. Its public shape exposes
only:

- `vault-entry/id`;
- opaque `artifact/id`;
- `artifact/kind`;
- the cryptographic envelope;
- ciphertext.

The artifact payload and all domain metadata live inside ciphertext. A vault
entry that contains plaintext payload fields, lacks ciphertext, or lacks at
least one key envelope is invalid. Public lookup is `GET
/v1/agora/vault-artifacts/{artifact_id}` and returns ciphertext-bearing entries
only. Scoped list/get/delete use `GET|DELETE
/v1/agora/vaults/{vault_subject}/artifacts...`. In the supervised local Node
runtime those routes are gated by the Agora service client token and daemon host
capability dispatch. Federated or remote-provider deployments bind the same
operations to the frozen `agora-vault@v1` capability/passport profile scoped to
the opaque `vault_subject`.

The MVP writer used by recorded messaging may emit `key-wrap =
"dev-key-commitment"`. This is a development custody commitment to the
discarded symmetric key; it proves that ciphertext was produced but does not
make the entry decryptable by itself. Production recovery uses recipient key
wrapping under `x25519-hkdf-sha256+xchacha20-poly1305`.

The implemented MVP runtime exposes these concrete operations:

| Operation | Runtime path | Authorization boundary | Notes |
|---|---|---|---|
| Put encrypted artifact | `POST /v1/agora/vaults/{vault_subject}/artifacts` | Agora client token locally; `agora-vault@v1` remotely | Request body is an `agora-vault-entry.v1`; invalid plaintext or missing key envelopes are refused. |
| List scoped artifacts | `GET /v1/agora/vaults/{vault_subject}/artifacts` | Same scoped vault authority | Response includes list items with `artifact/id`, `artifact/kind`, `vault-entry/id`, `stored/at`, and optional ciphertext digest. |
| Get scoped artifact | `GET /v1/agora/vaults/{vault_subject}/artifacts/{artifact_id}` | Same scoped vault authority | Returns the full encrypted entry after export schema validation. |
| Delete scoped artifact | `DELETE /v1/agora/vaults/{vault_subject}/artifacts/{artifact_id}` | Same scoped vault authority | Performs a soft delete; scoped and public reads ignore deleted entries. |
| Public encrypted lookup | `GET /v1/agora/vault-artifacts/{artifact_id}` | Public lookup by opaque artifact id | Returns filtered ciphertext-bearing entries only and does not reveal `vault_subject`, participant, nym, author, topic, or plaintext domain metadata. |

The supervised `agora-service` stores MVP vault entries in
`agora-vault.v1.sqlite`. The scoped uniqueness boundary is
`(vault_subject, artifact_id)`, so the same opaque `artifact/id` may exist in
multiple vault subjects. Public lookup by artifact id may return more than one
ciphertext entry, but each entry remains subject-opaque.

The supervised `agora-service` also registers daemon host capability handlers:

- `agora.vault.put`;
- `agora.vault.list`;
- `agora.vault.get`;
- `agora.vault.delete`.

Recovery is deliberately separated from the public Agora record surface.
`agora-vault-ref.v1` is a plaintext record shape intended to be sealed inside
`pseudonym-vault.v1`; it maps recovered participant or nym material to the
provider, opaque `vault/subject`, capability references, and allowed artifact
kinds. A bare public participant id is not enough to list, get, or delete vault
contents.

Recorded messaging is the first profile that uses Agora Vault: it stores a
signed `message-envelope.v1` as a generic encrypted artifact rather than as an
Agora topic record. Vault writes are best-effort: temporary failure does not
roll back message delivery, and the messaging outbox worker retries due
`failed-retryable` vault jobs.

## Interaction With Existing Proposals

| Proposal | Relation |
|---|---|
| 013 — Whisper social signal exchange | `whisper-signal.v1` is a first-class Agora `content/schema` under `record/kind = "whisper"`, using pseudonymous `nym:did:key:...` authorship (§2 invariant 9) anchored by `author/nym-proof` with inline-first `nym-certificate.v1` material. Bounded provenance statements use the separate `record/kind = "whisper-trace"` with `content/schema = "whisper-trace.v1"`, so they cannot enter social-signal projections accidentally. Agora is one of two distribution mechanisms (the other is direct node-to-node exchange, see proposal 013 §Distribution), and Memarium is the local storage surface for both. Threshold-reached events remain a separate `whisper-durable` kind for when a whisper crosses bootstrap thresholds and needs a different durability posture. |
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
- **Relay metadata stamping**: `relay/received-at` (RFC 3339 UTC),
  `relay/id`, and `relay/hops` are stamped by the relay on every ingest,
  as specified in section 2. These fields are excluded from content
  address and signature (via `VerifiedRecord` relay metadata helpers), so
  stamping does not break the envelope invariant.
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
a backend-neutral `SubjectIndex` trait in `agora-relay-trait`. It is populated
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
- **Query attestations**: historical query pages include
  `agora-query-attestation.v1`. The reference adapter emits unsigned
  attestations that bind query scope, normalized filter, record ids, cursor
  metadata, and a deterministic digest. Relay signatures over attestations are
  a later signer/authority integration, not an `agora-core` concern.

#### Local runtime data-dir ownership

An Agora service instance has exclusive ownership of its local runtime
data directory. This is the Agora middleware data directory, not the
Node profile root. Under daemon supervision the default path is:

```
<node-data-dir>/middleware/agora-service/data
```

The Agora middleware data directory is a single-writer local state root,
not a multi-process database contract. At most one live Agora service
instance MUST use a given Agora middleware data directory at a time.

This ownership invariant covers the SQLite relay store, the subject
index rebuild cycle, retention sweeps, rate-limiter snapshots, and any
other process-local caches or timers derived from the same root. Adding
file locks around individual snapshot reads and writes would protect
only those I/O operations; it would not make two Agora runtimes share one
coherent timeline, one cache state, or one retention policy execution.

Implementations SHOULD enforce the invariant with an exclusive
startup-time lock file inside the Agora middleware data directory and
fail fast with an operator-readable error when the lock is already held.
Snapshot writes SHOULD remain crash-safe through the usual temp-file,
fsync, and atomic rename discipline.

Per-file shared/exclusive locks MAY be added later as a compatibility
mechanism for external diagnostic, backup, or migration tools that need
to read snapshot files while Agora is running. Such locks MUST NOT be
interpreted as permission to run multiple Agora service instances against
the same Agora middleware data directory.

### Explicit local service backend (`2026-10-05`)

The operator accepted an explicit `local-sqlite` backend for `agora-service`
during P094 qualification. This uses the existing SQLite store and shared
relay contracts, not a fake Matrix sink. Signature/delegation verification,
namespace and topic policy, duplicate admission, queries, subscriptions,
subject indexing and retention remain unchanged. The receipt proves durable
local admission; remote discovery and order/result delivery require their own
network evidence. The status surface must name the selected backend and must
not claim Matrix forwarding in this mode. The default remains Matrix, and
missing Matrix credentials must not cause an implicit local fallback.

| ID | Task | Status | Closure gate |
| :--- | :--- | :--- | :--- |
| `P035-local-sqlite-service` | Expose an explicit local SQLite service backend | `done` | 2026-10-05: backend-neutral subject index/retention/stamping reuse the existing core/relay/store contracts; signed local ingest/query/subscription and restart tests pass, and ambiguous Matrix/local configuration refuses. The service reports local durable admission, never Matrix distribution. Deployed Dator ordinary publication/replay/withdrawal passes in P094's clean-source local MLX/vfkit run `s13-1791156863-88b339`. P094-016 independently qualifies network discovery/order/AD-result; this item does not claim it. |

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
- **Relay metadata stamping**: `relay/received-at`, `relay/id`, and
  `relay/hops` stamped by the federated relay (`agora-relay-matrix`) on
  ingest, via `VerifiedRecord` relay metadata helpers which preserve the
  envelope invariant (relay fields are excluded from content address and
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
- **Subject index** (`agora-relay-trait`): in-memory `SubjectIndex`
  for cross-topic `record/about` queries, idempotent, rebuildable from
  local store.
- **HTTP API surface** (`agora-http`): framework-neutral adapter for
  proposal 035 §5 endpoints. Opaque cursors, SSE subscriptions, topic
  mismatch validation, partial about-filter rejection.
- **Service and daemon integration** (`agora-service` + supervised
  middleware): the relay runs as a daemon-managed local HTTP middleware
  service. The daemon supervises the process, provisions module/client
  auth tokens, and exposes capability-provider discovery while the
  service owns its REST/SSE surface.
- **Retention** (age + count + scheduling): `sweep_retention()` with
  automatic subject index rebuild after purge, driven by the
  `agora-service` retention sweep thread when topic policies are
  configured.

#### Ingest invariants still deferred or limited

The following invariants from section 2 use "flag, not reject" semantics
in this proposal and are not blocking for the first deployment:

- **Invariant 5** (`authored/at` clock skew window) — not checked; the
  field is validated as non-empty only.
- **Invariant 6** (`record/parent` / `record/supersedes` dangling
  detection) — implemented at the publisher edge in `agora-service`.
  The default is warn-and-accept to preserve eventual consistency;
  `strict_parent_refs = true` turns unresolved references into HTTP 422.
  Federation ingress remains warn-only.
- **Invariant 7** (passport chain verification via proposals 024 and
  032) — the Rust `AgoraSignature` struct now carries a stratified
  shape with `key/public` (the actual signing key bytes) and an
  optional `key/delegation` block (delegation proof chain per
  proposal 032). Direct-key signatures are fully verified end-to-end
  (key match against the author's participant id is a hard block
  via `SignAdapterError::PublicKeyMismatch`). Delegated signatures
  are accepted structurally and verified through the
  `CapabilityDelegationVerifier` trait wired in L4.b of the
  035-impl doc; the default deployment installs a permissive
  verifier, and hardened deployments plug in the
  `agora-capability-bridge` proof checker. The legacy
  `signature.key/ref` shape is retired and no longer appears in the
  schema or the code.
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

#### Still deferred / intentionally limited

- **Subject index persistence**: for MVP, the `record/about`
  `SubjectIndex` is intentionally a derived, rebuildable view over the
  local relay store. It is not a source of truth and does not need its own
  persisted projector to satisfy the v1 contract. `rebuild_subject_index()`
  reconstructs it from the local SQLite store on startup; a SQLite-backed
  subject index should be added later only when listing volume, restart
  latency, or retention churn makes rebuild cost material.
- **Room-to-topic name mapping** (section 6, rule 2): the relay does
  not yet maintain a human-readable room-name mapping for operator
  tooling.

#### Post-MVP hardening queue

The hard-MVP relay is complete without these items, but production hardening
SHOULD track them explicitly rather than rediscovering them from prose:

- `authored/at` skew policy: decide the local/federated skew budget and reject
  records outside it at the relay boundary.
- Delegated-signature proof enforcement: replace the permissive default
  `CapabilityDelegationVerifier` with the `agora-capability-bridge` checker in
  hardened deployments.
- `record/about` structural validation: validate each resource reference
  against `resource-ref.v1` before subject-index admission.
- Schema-pattern parity: ensure relay-side schema-gate rejects malformed
  `record/kind`, `content/schema`, and `record/id` values before verification
  library calls.
- Topic-key NFC admission: decide whether the relay rejects non-NFC topic keys
  or normalizes them before ingest diagnostics.
- Federation ingress parent/supersedes policy: decide whether Matrix/federated
  ingress stays warn-only or gains a stricter reference-resolution mode.
- Operator status product: expose federation lane diagnostics, ingest rejection
  counters, retention sweeps, and relay role health in the Node UI.

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

## P081 Scoped-Claim Ingest Path

Agora now has an optional P081 path for nym-authored records. A
`nym-authorship-proof.v1` may carry both `scoped-claim/request` and
`scoped-claim/presentation`; either both are present or neither is. The service first
verifies the complete signed Agora envelope, then binds the scoped request to a
canonical digest of the exact ingest candidate with the nested scoped values removed
to avoid a self-referential digest. Only after that check may the durable replay cache
consume the nonce.

The shared verifier returns evidence only. Agora still applies topic ACL, namespace,
content-schema, disclosure, certificate-scope, and publish authority policy through
its existing gates. Valid scoped evidence can therefore be denied, and a malformed or
badly signed outer envelope cannot consume a valid presentation nonce. The path is
disabled by default and fails closed unless trusted council issuers and fresh local
revocation snapshot metadata are configured.

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

## Producer Delivery Through Artifact Delivery

Planned continuation (2026-10-11), not a reopening of the completed relay MVP.
Node-owned producers should submit already signed `agora-record.v1` artifacts
through [S023 Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
and its existing `agora-default` adapter. This includes P026 authoring, P067
offer publication and accepted Seed Directory facts. It does not replace the
Agora ingest API, historical queries, SSE or Matrix relay replication; those
remain independently usable protocol surfaces. Public publication does not
require INAC, and private artifacts must never acquire a public fallback.

### Implementation Recommendations

- Keep `authorize -> sign -> AD submission -> Agora admission` explicit. AD
  outbound permission does not substitute for Agora topic, author, capability,
  attestation or fresh revocation checks, including on delayed attempts.
  Preserve the original caller and publication authority across the host bridge;
  the adapter must not become an ambient privileged publisher.
- Reuse `ad-host`, the AD delivery ledger, object retention and deferred-operation
  status. Producers retain domain intent and exact signed bytes before submission;
  restart retries the same artifact and destination, not a newly signed record.
  Journal the intent-to-delivery-id association so a crash between domain commit
  and AD submission is reconcilable without a second transport retry queue.
- Project `record/id`, target relay, AD delivery id and domain publication outcome
  into the existing UI/status surfaces. Queued, relay-accepted and failed are
  different observations; relay acceptance is not proof of all-peer replication
  or permanent retention. A timeout after remote acceptance remains uncertain
  until idempotent retry/readback reconciles it. Do not report it as unpublished.
- Feed bounded publication outcome facts into Memarium through existing
  observation ports and S028 temporal storage conventions. Retaining a local
  artifact is not permission to republish after expiry, withdrawal or deletion.
  Inventory existing publisher outboxes first; preserve domain jobs but give AD
  sole ownership of transport retries after successful submission.
- Keep adapters thin under `node:DEV-GUIDELINES.md`: pure mapping below host I/O,
  schema-gated boundaries, bounded retention and redacted diagnostics. Migrate
  producers incrementally with one selected path per publication, never dual-send.

### Delivery Integration Tracker

All rows are post-MVP `todo`; `done` requires retained Node runtime evidence and
reconciliation of its implementation ledger and any affected MVP scope. S008
links here rather than maintaining duplicate task status.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P035-001 | Freeze producer-to-AD publication binding | todo | Existing S023 `agora-default` | Inventory UI, Dator, Seed Directory and other direct publishers; classify local-only/test clients separately; pin caller/authority propagation, exact signed bytes, intent/delivery correlation, timeout semantics and ownership of every existing outbox. Contract fixtures cover policy refusal before effects and recovery after submission ambiguity. |
| P035-002 | Migrate Node-owned publishers | todo | P035-001 | P026 compose/opinion/comment authoring, P067 Dator offer snapshots and accepted Seed facts use the same host delivery seam with explicit route configuration. UI reports pending versus confirmed publication. No duplicate sends or component-private transport retries; raw/unaccepted Seed requests are never published. Domain state survives delivery failure. |
| P035-003 | Retain local and remote relay acceptance | todo | P035-002 | Exercise actual producer -> signer -> AD -> local/remote Agora -> query with unchanged record id/signature/about fields; outage, remote-accepted/lost-response, restart, duplicate retry, expired/revoked authority and denied topic fixtures pass. Private fallback is refused; Matrix federation and direct relay API compatibility remain intact. |

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
   Agora records and Node-local stores,
7. proposal 040 (custodial redelivery and tombstones) defines the readback
   tombstone vocabulary (`410 Gone` with `retention_expired`,
   `removed_by_policy`, `storage_lost`, `superseded`), operator sovereignty
   over re-acceptance, custodian negotiation via `capability-passport.v1`,
   and the author-scoped sondage endpoints (count, listing, digest) gated
   by `agora-author-proof.v1`. Agora implementations SHOULD implement the
   tombstone surface as soon as the relay serves more than one node; pure
   local-only MVP relays MAY keep `404` as the sole absence signal,
8. proposal 041 (Agora ingest attestation and tiered access) defines the
   `author/attestation_ref` optional signed envelope field, the
   `agora-attestation-proof.v1` short-lived proof token, the ingest mode
   matrix (`open`, `allowlist`, `passport`, `passport_scoped`, `layered`),
   a predicate grammar for tiered gates, and a stable refusal reason-code
   vocabulary symmetric with proposal 040's tombstone matrix. The
   verification primitive is placed as a reusable `attestation-gate`
   alongside signer and sealer in the daemon's trust-boundary zone and
   is consumable by every component that needs to ask "is this author
   attested under a passport I currently accept", not only Agora.
