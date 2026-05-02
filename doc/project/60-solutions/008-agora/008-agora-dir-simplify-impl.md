# Directory Simplification Through Agora Records

Status: implementation guidance / design note.

Implementation status:

- Reference adapter slice exists in Node:
  `seed-directory::agora` and `catalog::agora`.
- Strict Agora content-schema validation recognizes the first domain payloads:
  `service-offer.v1`, `node-advertisement.v1`,
  `seed-capability-registration.v1`, and
  `capability-passport-revocation.v1`.
- Runtime dual-publish / replay wiring is partially implemented:
  Dator can best-effort publish accepted `service-offer.v1` snapshots to an
  Agora topic, Arca can replay those `offer-snapshot` records into its observed
  catalog projection, and Seed Directory has a publish-after-accept hook for
  accepted advertisement/capability/revocation facts.
- Story-009 laptop profiles wire node B/C Dator instances to node A's local
  Agora service and configure node A Arca to replay the shared Story-009 offer
  topic.

## Thesis

Use `agora-record.v1` as the default envelope for public, federated,
topic-shaped, append-only records.

Several Orbiplex subsystems currently want almost the same substrate:

- signed append-only records,
- topic or subject addressing,
- replay and subscription,
- local indexes,
- relay/federation,
- retention,
- query,
- materialized views.

Agora was designed as that neutral substrate: a signed, timestamped,
content-addressed record under an opaque topic, with domain payload semantics
selected by `record/kind` and `content/schema`.

The simplification is:

```text
less bespoke logs
more domain payloads inside one record substrate
```

Do not turn every domain API into a raw Agora query. Agora should carry records.
Domain components should interpret records.

## Truth Boundaries

Do not describe Agora as the full source of truth for offers.

Use the narrower contract:

```text
Agora is the durable public record substrate for offer publication snapshots.
```

The offer plane has several different truth boundaries:

| Layer | Truth it owns |
| --- | --- |
| Dator `local-offers.db` | locally published standing offers of the provider |
| provider-signed `service-offer.v1` | cryptographic offer artifact |
| Agora `offer-snapshot` | public/federated fact that a snapshot was published |
| Arca `observed-catalog.db` | local materialized view of offers admitted or observed by the buyer |
| provider runtime | execution-time truth about capacity, expiry, queue saturation, and rejection |

This preserves proposal 023's authority split: a catalog service is an indexer
and relay, not the authority over provider offers. Provider nodes remain the
authority over their own standing offers and runtime acceptance decisions.

## Default Rule

If a new artifact is all of the following:

- public or federation-scoped,
- append-only,
- topic-shaped or subject-addressed,
- signed by a participant, nym, node, or delegated key,
- queryable through local indexes or materialized views,

then the default transport/storage envelope should be:

```text
schema         = "agora-record.v1"
record/kind    = "<domain event kind>"
topic/key      = "<opaque domain topic>"
content/schema = "<domain payload schema>"
content        = <domain payload>
record/about   = <optional subject index hints>
```

Examples:

| Domain artifact | Agora `record/kind` | `content/schema` |
| --- | --- | --- |
| service offer snapshot | `offer-snapshot` | `service-offer.v1` |
| resource opinion | `opinion` | `resource-opinion.v1` |
| public comment | `comment` | `plain-comment.v1` |
| comment thread policy | `thread-policy` | `comment-thread-policy.v1` |
| public gossip | `gossip` | `public-gossip.v1` |
| whisper public weak signal | `whisper` | `whisper-signal.v1` |
| whisper threshold record | `whisper-durable` | `whisper-threshold-record.v1` |
| Seed Directory accepted advertisement | `seed.node-advertisement.accepted` | `node-advertisement.v1` |
| Seed Directory accepted capability registration | `seed.capability-registration.accepted` | `seed-capability-registration.v1` |
| Seed Directory accepted revocation | `seed.capability-revocation.accepted` | `capability-passport-revocation.v1` |
| capability public announcement | `capability.public-announcement` | domain-specific capability announcement schema |
| topic log entry | `topic-log-entry` | domain-specific topic log entry schema |

Names should follow existing code and schema names when they already exist. Do
not invent prettier names if a stable implementation name already carries the
contract.

## Boundary: Agora vs Memarium

Do not merge Agora and Memarium.

Agora answers:

```text
Where do public/federated topic-addressed records live?
```

Memarium answers:

```text
What must not disappear, what is locally remembered, and under which local
classification/durability policy?
```

Agora is the public/federated record substrate. Memarium is local memory,
classification, retention, backup, and constitutional durability.

A subsystem may observe Agora records into Memarium, but Agora should not become
Memarium and Memarium should not become the public relay.

## General Implementation Shape

Prefer this shape:

```text
Domain API
  -> domain engine validates and normalizes
  -> local materialized projection/store
  -> accepted semantic event published as agora-record.v1

Agora replay/subscription
  -> verify agora-record.v1 envelope
  -> verify domain payload and policy
  -> upsert materialized projection

Domain reads
  -> query local materialized projection
  -> return domain response
```

Avoid this shape:

```text
Domain API
  -> raw Agora query
  -> ad-hoc mapping of records into domain response
```

That bad shape moves domain indexing, policy, joins, revocation checks, retry
semantics, and query rules into every client.

## M1 Authorization Decisions

The M1 implementation must preserve these separations:

```text
signing authority
  != publish authorization
  != domain acceptance
  != local trust decision
  != execution-time provider truth
```

### Namespace Semantics

A namespace defines topic semantics, expected schema contracts, and moderation or
trust context. It does not by itself establish a write monopoly.

Write authority comes from a policy gate such as `agora-publish@v1`, with an
`agora/publish` grant over concrete topic patterns plus `record/kind` and
`content/schema` constraints.

M1 topic conventions:

| Topic pattern | M1 write policy |
| --- | --- |
| `ai.orbiplex.announcements/**` | authority roots or delegated authority with matching `agora/publish` grant |
| `ai.orbiplex.proposals/**` | authority roots for canonical proposal records; discussion topics use participation policy |
| `ai.orbiplex.proposals/<id>/discussion` | `ial1` participants and above, unless a stricter thread policy applies |
| `ai.orbiplex.opinions/<resource-kind>/...` | `ial1` participants and above |
| `ai.orbiplex.comments/<thread-id>` | `ial1` participants and above, with optional tightening through `comment-thread-policy.v1` |
| `ai.orbiplex.gossip/<topic-class>` | `ial1` participants and above; payload must be public and marked as non-evidence |
| `ai.orbiplex.whispers/...` | `ial1-pseudonymized` participants or stricter local whisper policy |
| `participant:<pid>/...` | the participant or a valid delegation chain resolving to that participant |
| `node:<node-id>/...` | the node/operator chain after node-binding verification is wired |
| `federation:<fid>/...` | federation policy |

`ai.orbiplex.*` is reserved for Orbiplex-defined semantics from orbidocs.
Publishing into that namespace is allowed only when local policy and the
presented passport authorize the concrete record.

### Record Authorization Classes

Authorization is keyed by:

```text
topic pattern
record/kind
content/schema
caller
required assurance or authority profile
```

M1 classes:

| `record/kind` | Authorization class |
| --- | --- |
| `announcement` | authority publish |
| `proposal` | authority publish when speaking for Orbiplex/project/federation authority |
| `comment` | participation publish |
| `opinion` | participation publish |
| `gossip` | participation publish |
| `whisper` | pseudonymous participation publish |
| `whisper-durable` | domain acceptance plus publish authorization for the publishing component |
| `thread-policy` | policy creation/tightening for the target thread or subtree |
| `offer-snapshot` | accepted domain fact published by an authorized offer publisher |
| `seed.node-advertisement.accepted` | accepted domain fact published by Seed Directory |
| `seed.capability-registration.accepted` | accepted domain fact published by Seed Directory |
| `seed.capability-revocation.accepted` | accepted domain fact published by Seed Directory |

Rules:

- Authority records require authority roots or delegated authority.
- Participation records require sufficient author attestation, not authority
  roots.
- `thread-policy` records require the caller to be allowed to create or tighten
  policy for the target thread/subtree. They may tighten inherited policy but
  must not loosen it.
- Accepted domain facts require the domain engine to accept the source fact
  before publication. Agora carries the accepted fact; it does not perform the
  domain acceptance decision.

### Assurance Names

Canonical M1 names:

- `ial1` — minimum participation assurance. It is the configuration name for an
  ISO/IEC 29115 Level 1-like baseline, mapped by the deployment to concrete
  passport or attestation evidence.
- `ial1-pseudonymized` — `ial1` where the public record may use a permitted nym
  identity and the real participant binding remains outside the public record or
  inside an allowed pseudonymization proof.
- `authority-root` — configured accountable subject that may establish
  namespace authority. It is not merely a signing key.

Do not implement `community-trusted` in M1. It is a later computed,
time-bounded, community-scoped status derived from signed reputation facts under
`ai.orbiplex.reputation/**` and a local `ReputationProjection`.

### Authority Root Resolver

An authority root is a configured accountable subject that may establish or
delegate publishing authority for a protected namespace.

The authority-root configuration is not a list of keys that may publish. It is
a list of identities that may establish publishing authority.

Accepted M1 root identity kinds:

- participant id,
- org id using the current single-custodian org model,
- delegated or derived key proven by `key-delegation.v1`.

Resolver path:

```text
record author / presented capability
  -> participant or org identity
  -> optional key delegation chain
  -> authority root membership
  -> topic/kind/schema constraints
```

### Topic Matching Grammar

Topic matching is exact and case-sensitive after the substrate canonicalization
pass. Invalid authoring shapes are rejected, never silently normalized.

Grant grammar:

- `topic:<literal>` matches exactly one topic.
- `topic:<prefix>/**` matches descendants below a slash prefix.
- Do not add single-segment `*` until a real use case needs it.
- Prefer explicit subsystem grants such as `topic:ai.orbiplex.comments/**`,
  `topic:ai.orbiplex.opinions/**`, and
  `topic:ai.orbiplex.proposals/**`.

Topic-key comparison:

- Unicode NFC normalization is applied once at the substrate boundary.
- Matching is exact and case-sensitive.
- Canonical namespace prefixes are lowercase.
- Case variants of reserved prefixes are rejected by authoring/relay policy as
  confusable, for example `Private/...`, `LOCAL/...`, or `Ai.Orbiplex...`.
- Agora core remains opaque and exact; the namespace policy layer performs the
  rejection.

Slash policy:

- Agora core treats slash as an ordinary character.
- Agora namespace policy rejects leading slash, trailing slash, and multiple
  consecutive slashes unless a kind contract explicitly allows them.
- Public/federated relay policy rejects non-conforming topic keys at the policy
  layer. It does not normalize slashes and does not trim.

### Subscribe Semantics

`agora-subscribe@v1` controls protected read/replay/stream access. Public topics
remain public unless topic policy says otherwise.

M1 rules:

- Public read by default is acceptable for public `ai.orbiplex.*` topics such as
  announcements, canonical proposals, public comments, and public opinions.
- Public read by default is not assumed for restricted, private,
  federation-scoped, local, whisper, or policy-bound topics.
- `private/...` is never carried by Agora.
- `local/...` is only legitimate for an intra-node relay and must not federate.
- Whisper disclosure policy decides whether a whisper topic is readable.
- `agora-subscribe@v1` is required for restricted, private-equivalent,
  federation-scoped, or non-public topics.
- Subject-index queries must filter by the caller's topic authorization and must
  not bypass topic grants.

One `agora/subscribe` grant covers both historical query and live SSE stream in
M1. The history/live distinction is a transport or query mode, not a separate M1
authorization contract. If a future use case requires separation, add an
optional profile constraint:

```json
{ "modes": ["history", "live"] }
```

Historical query responses SHOULD carry `agora-query-attestation.v1`. The
attestation is a response proof, not a new read-authorization primitive. It
binds the query mode, scope, normalized filter, returned record ids, cursor
metadata, and a deterministic page digest. Subject-index responses MUST attach
or refresh the attestation after topic authorization filtering so the proof
describes the exact response returned to the caller.

### Revocation Freshness Defaults

Publish and protected subscribe use bounded revocation staleness. Defaults live
in the `agora-publish@v1` / `agora-subscribe@v1` profile evaluator. Operators
may only tighten them unless a deployment explicitly documents a looser policy.

| Class | `max_revocation_staleness_seconds` | Failure mode |
| --- | ---: | --- |
| Authority publish (`announcement`, canonical `proposal`, policy records) | 60 | fail closed |
| Restricted subscribe | 120 | fail closed |
| Participation publish (`comment`, `opinion`, `gossip`) | 300 | fail closed for revoked passport/delegation |
| Public read | 3600 | fail open with diagnostics |
| Whisper publish/subscribe where policy requires authorization | 120 | fail closed |

A stale revocation view must be visible in audit/diagnostics. Replay of
historical accepted facts is not the same as live write admission; projections
must document their historical revocation semantics.

### Signing Grant vs Publish Capability

`signing/agora-record` and `agora-publish@v1` are independent checks.

- `signing/agora-record` is a grant in `key-delegation.v1`. It says that a
  proxy or derived key may sign Agora records within its delegated scope.
- `agora-publish@v1` is a profile in `capability-passport.v1`. It says that a
  caller/component/subject may publish records under `agora/publish` topic
  grants and profile constraints.
- Both must pass for authority publish when a delegated/proxy key is used.
- Direct participation publish may use the author's own key for envelope
  signing, but still requires the appropriate participation publish profile or
  attestation gate.

Authority publish verification order:

```text
1. Verify agora-record.v1 envelope signature.
2. If a delegated/proxy key is used, verify key-delegation.v1 including
   signing/agora-record.
3. Verify agora-publish@v1 passport/profile:
   allowed_callers, agora/publish topic grants, record/kind constraints,
   content/schema constraints.
4. Resolve authority root or delegated authority where the record claims to
   speak with namespace/project/federation authority.
5. Verify revocation freshness.
6. Ingest/publish only if all required gates pass.
```

Participation publish verification order:

```text
1. Verify envelope signature against the author or allowed nym key.
2. Verify required author attestation, for example ial1 or ial1-pseudonymized.
3. Verify the applicable participation publish profile/topic policy.
4. Verify revocation freshness.
```

### Runtime Caller Identity

Runtime authorization evaluates the bound caller, not merely the process or
transport that reached Agora.

Recommended M1 caller kinds:

- local operator,
- middleware module,
- peer node,
- participant,
- org through custodian/delegation,
- delegated key,
- nym where policy allows it.

Local HTTP/module calls must map to a concrete caller identity before topic
authorization. Middleware module identity alone is not enough for authority
publish.

Module publish path:

```text
module auth token
  -> CallerBinding, for example kind: "http-module", subject_key: "module:dator"
  -> capability-passport.v1 with allowed_callers including that subject_key
  -> agora-publish@v1 profile with matching topic grant
  -> revocation freshness
  -> authorized
```

M1 examples:

- Dator publishing `offer-snapshot` needs an `agora-publish@v1` passport with
  `allowed_callers` including `module:dator` and an `agora/publish` grant for
  the offer-catalog topic pattern, for example
  `topic:orbiplex/offer-catalog/v1/**`.
- Seed Directory publishing `seed.*.accepted` needs a matching passport for the
  Seed Directory publishing module and the Seed Directory topic patterns.

## Seed Directory

Seed Directory should remain a semantic facade and policy surface. Agora may
become its publication, replay, and federation substrate.

Keep the Seed Directory API and Rust interface domain-shaped:

```text
PUT  /adv/{node-id}
GET  /adv/{node-id}
GET  /adv?since=...
PUT  /cap/{node-id}/{capability-id}
GET  /cap?...
POST /revoke
GET  /revocations?since=...
```

The Seed Directory is not just a collection of records. It owns domain policy:

- node advertisement acceptance,
- passport signature verification,
- sovereign issuer policy,
- `node_id` and `capability_id` consistency,
- expiry,
- revocation checks,
- stale sequence checks,
- endpoint joins,
- node-address attestation,
- capability query shape.

Agora should not learn those meanings. Agora verifies the envelope and stores
topic records. Seed Directory interprets accepted records as discovery state.

Recommended layering:

```text
1. SeedDirectoryApi
   HTTP wire compatibility.

2. SeedDirectoryEngine
   Domain validation and policy:
   passport checks, sovereign policy, expiry, revocation, stale sequence,
   endpoint join, node-address attestation.

3. SeedDirectoryProjection
   Materialized read model:
   node_advertisements, capability_registrations, capability_passports,
   revocations, cursors, hot indexes.

4. SeedDirectoryAgoraAdapter
   Publish/replay:
   accepted adv/cap/revoke facts as agora-record.v1, plus subscription/rebuild
   of the projection.
```

Rust interface should remain domain-specific:

```rust
trait SeedDirectory {
    fn put_advertisement(&self, adv: NodeAdvertisement) -> Result<StoredAdv>;
    fn get_advertisement(&self, node_id: NodeId) -> Result<Option<NodeAdvertisement>>;
    fn list_advertisements_since(&self, cursor: Cursor) -> Result<Batch<NodeAdvertisement>>;

    fn put_capability(&self, req: CapabilityRegistrationRequest) -> Result<StoredCapability>;
    fn find_capabilities(&self, query: CapabilityQuery) -> Result<CapabilityBatch>;
    fn publish_revocation(&self, rev: CapabilityPassportRevocation) -> Result<StoredRevocation>;
    fn list_revocations_since(&self, cursor: Cursor) -> Result<Batch<Revocation>>;
}
```

Implementations can differ:

```text
SqliteSeedDirectory
AgoraBackedSeedDirectory
CompositeSeedDirectory
RemoteSeedDirectoryClient
```

Preferred production implementation:

```text
CompositeSeedDirectory

write path:
  request
  -> SeedDirectoryEngine validates
  -> local projection/store commit
  -> publish accepted semantic event to Agora
  -> return normal Seed Directory response

read path:
  request
  -> local materialized projection
  -> normal Seed Directory response

sync path:
  Agora subscription/replay
  -> verify record envelope
  -> verify domain payload
  -> upsert projection
```

Publish accepted facts, not raw requests. Raw requests may be invalid,
expired, unauthorized, or spammy.

Suggested topics:

```text
orbiplex/seed-directory/v1/{federation-id}/adv
orbiplex/seed-directory/v1/{federation-id}/cap
orbiplex/seed-directory/v1/{federation-id}/revocations
```

Suggested payload mapping:

```text
record/kind    = "seed.node-advertisement.accepted"
content/schema = "node-advertisement.v1"

record/kind    = "seed.capability-registration.accepted"
content/schema = "seed-capability-registration.v1"

record/kind    = "seed.capability-revocation.accepted"
content/schema = "capability-passport-revocation.v1"
```

M1 records carry full accepted facts in `content`:

- `seed.node-advertisement.accepted` carries full `node-advertisement.v1`.
- `seed.capability-registration.accepted` carries full
  `seed-capability-registration.v1`, including the nested accepted capability
  passport or registration payload required by that schema.
- `seed.capability-revocation.accepted` carries full
  `capability-passport-revocation.v1`.
- `record/about` may add `orbiplex:blob:sha256:...` or subject references for
  indexing, but references do not replace `content`.

This keeps replay self-contained. A node that does not fully trust a Seed
Directory can still verify the inner domain artifact signature where one
exists.

Rejected requests may have an audit stream, but treat it carefully:

```text
orbiplex/seed-directory/v1/{federation-id}/rejections
```

That stream can leak intent or become an enumeration/spam channel. It should be
operator/debug scoped unless there is a clear public value.

Invariant:

```text
SeedDirectoryHTTP(ProjectionFromSqlite)
==
SeedDirectoryHTTP(ProjectionFromAgoraReplay)
```

## Offer Relay And Offer Catalog

Offer Relay can become an Agora adapter. Offer Catalog should remain a domain
facade and materialized view.

```text
Agora        = feed / replay / federation substrate
Offer Relay  = publisher/compatibility adapter
Offer Catalog = domain projection / query surface
CatalogResolver = bridge-facing decision surface
```

### Offer Relay

`service-offer-relay.v1` currently acts as a transport envelope for
`service-offer.v1`, adding propagation metadata such as origin node, hops,
do-not-forward, and relayed-at.

Agora already provides the generic federation envelope:

- `topic/key`,
- `record/id`,
- `record/kind`,
- `content/schema`,
- author,
- authored-at,
- signature,
- relay receive metadata,
- query, replay, subscribe.

Target shape:

```text
Dator
  -> local commit of service-offer.v1
  -> OfferRelayAdapter::notify_offer(...)
  -> Agora submit record
```

Canonical target record:

```json
{
  "schema": "agora-record.v1",
  "record/kind": "offer-snapshot",
  "topic/key": "orbiplex/offer-catalog/v1/{federation-id}",
  "content/schema": "service-offer.v1",
  "content": {
    "...": "provider-signed service-offer.v1"
  },
  "record/about": [
    { "resource/kind": "participant", "resource/id": "participant:..." },
    { "resource/kind": "node", "resource/id": "node:..." },
    { "resource/kind": "service-type", "resource/id": "..." },
    { "resource/kind": "service-offer", "resource/id": "offer:..." }
  ]
}
```

During migration, `service-offer-relay.v1` may remain as a compatibility
payload, but the target is not envelope-in-envelope. The long-term canonical
feed is:

```text
agora-record.v1
  record/kind    = "offer-snapshot"
  content/schema = "service-offer.v1"
```

The migration must preserve enough provenance for Arca to make the same trust
admission decision it made from `service-offer-relay.v1`.

At minimum, an `offer-snapshot` record or its replay context must expose:

- `provider_participant_id`,
- `provider_node_id`,
- Agora record author,
- publisher/origin node id when known,
- ingest or observation timestamp,
- `topic/key`,
- `record/id`,
- inner `service-offer.v1` signature verification result.

Mapping from legacy relay metadata to Agora-native replay:

| `service-offer-relay.v1` | Agora-native source |
| --- | --- |
| `offer` payload | `content` with `content/schema = "service-offer.v1"` |
| `relay/origin-node-id` | publisher/origin node id in replay context, or derived from trusted publisher context |
| `relay/hops` | `relay/hops` |
| `relay/relayed-at` | `relay/received-at` |
| `relay/do-not-forward` | no M1 Agora envelope field; preserve only when wrapping legacy `service-offer-relay.v1`, or define a future extension/topic policy |
| relay envelope identity | `record/id`, `topic/key`, `author/participant-id`, `relay/id`, replay source |

`ObservedOfferRecord` should keep existing relay/provenance fields and add Agora
diagnostics:

```rust
agora_record_id: Option<String>
agora_topic: Option<String>
agora_record_author: Option<String>
agora_relay_id: Option<String>
```

Existing fields such as `relay_origin_node_id`, `relay_hops`, and
`relay_do_not_forward` may remain for compatibility. In Agora-native replay,
`relay_hops` is filled from `relay/hops`; `relay_do_not_forward` is `None`
unless a legacy wrapped payload supplied it.

Transport fields from `service-offer-relay.v1` do not all need one-to-one
survivors. The invariant is narrower:

```text
Arca replay from Agora MUST be able to reach the same trusted/untrusted
admission decision that it previously reached from service-offer-relay.v1.
```

### Offer Catalog

Offer Catalog is not a raw record list. It owns domain behavior:

- offer activity,
- TTL and `expires_at`,
- sequence numbers,
- deduplication,
- local vs observed provenance,
- trust level,
- provider whitelist,
- known-peer trust,
- hiding untrusted entries,
- query by service type, provider, node, and limit,
- resolving service-order intent toward procurement.

Do not make buyer-side flows query raw Agora:

```text
bad:
  Arca / buyer bridge -> Agora query -> raw offer records
```

Use a projection:

```text
good:
  Arca sync task
    -> Agora topic replay / subscribe
    -> verify offer signature
    -> evaluate trust
    -> upsert ObservedCatalogStore

  Buyer / UI / bridge
    -> OfferCatalog / CatalogResolver
    -> local CatalogStore first
    -> trusted ObservedCatalogStore second
```

The public HTTP contract can stay as a facade:

```text
GET  /v1/service-offers
POST /v1/service-offers
```

Implementation:

```text
POST /v1/service-offers
  -> accept legacy service-offer-relay.v1
  -> validate / normalize
  -> submit agora-record offer-snapshot

GET /v1/service-offers
  -> read materialized OfferCatalogProjection
  -> return domain response
```

### Dator And Arca

The Dator/Arca split remains healthy:

```text
Dator:
  owns local standing offers
  signs / publishes service-offer.v1
  exposes local offer snapshot
  pushes offer snapshot to Agora through adapter

Arca:
  owns observed catalog projection
  subscribes / replays Agora offer topics
  evaluates trust
  exposes combined service catalog
  creates service-order intent

Node / host bridge:
  validates service-order against active offer
  projects into procurement
  owns settlement, policy, traceability
```

Arca should not own procurement. The host-owned bridge protects procurement
identity, settlement semantics, policy gating, and traceability.

## Resource Opinions, Public Comments, Public Gossip, Topic Logs

Resource opinions are already the cleanest Agora-native example:

```text
record/kind    = "opinion"
content/schema = "resource-opinion.v1"
record/about   = referenced resource identity
```

Use the same pattern for public comment threads:

```text
record/kind    = "comment"
content/schema = "plain-comment.v1"
topic/key      = resource/thread/topic key
record/about   = resource or topic index hints
record/parent  = parent comment, when the record is a reply
record/policy  = optional comment-thread-policy.v1 record
```

Public gossip is the public, low-friction sibling of private Whisper exchange:

```text
record/kind    = "gossip"
content/schema = "public-gossip.v1"
topic/key      = ai.orbiplex.gossip/<topic-class>
record/about   = optional resource or place/person/topic index hints
```

The payload MUST carry `disclosure/scope = "public"` and an
`epistemic/class`. It is intentionally not evidence. Private or
federation-scoped rumor exchange remains `whisper-signal.v1` or another
non-public transport policy; do not smuggle it into `public-gossip.v1`.

Thread participation policy should not be embedded in `plain-comment.v1`.
Use a separate Agora record:

```text
record/kind    = "thread-policy"
content/schema = "comment-thread-policy.v1"
```

The policy is inherited by descendants. A subtree may tighten the inherited
minimum attestation level, but it must not loosen it. Parent/reply semantics
and participation policy are still Agora record conventions, not a new bespoke
comment-log transport.

M1 participation defaults:

- `comment`, `opinion`, and `gossip` records require at least `ial1` author
  attestation.
- `thread-policy` records require the author to be allowed to create or tighten
  policy for the target thread or subtree.
- A policy-bound comment uses the stricter of the topic policy and the inherited
  `comment-thread-policy.v1` records that apply to it.

Topic logs should be materialized views over Agora topics unless they need
private/local durability, in which case Memarium may observe and preserve them.

## Whisper Durable And Public Signals

Whisper already distinguishes public/federated and private/direct distribution.

Use Agora only when the whisper posture permits public/federated topic
distribution:

```text
record/kind    = "whisper"
content/schema = "whisper-signal.v1"
```

For threshold-crossed durable records:

```text
record/kind    = "whisper-durable"
content/schema = "whisper-threshold-record.v1"
```

Do not push private-correlation or direct-only whispers into Agora. Those should
use direct node exchange, INAC, invitation-tokened transfer, or another bounded
private channel. Memarium remains the local memory surface for both public and
private whispers under classification policy.

## Capability And Listing Announcements

Public announcements about capabilities, listings, or operator-intended
availability can use Agora when they are public/federated and append-only.

Do not replace capability passport verification with Agora verification.

Agora can carry:

```text
record/kind    = "capability.public-announcement"
content/schema = "<announcement schema>"
```

The domain consumer still verifies:

- capability passport signatures,
- issuer policy,
- node acceptance,
- expiry,
- revocation,
- profile compatibility.

## M1 Implementation Phases

Use phases, not a flag-day rewrite.

### Phase 0: Current Model

Keep existing SQLite stores, HTTP APIs, and domain flows.

### Phase 1: Topic Policy And Publish Evaluator

Implement:

- config topic policy,
- authority roots config,
- `ial1` and `ial1-pseudonymized` attestation labels mapped to current passport
  or attestation evidence,
- hardcoded profile evaluator for publish authorization,
- tests for topic/kind/schema allow/deny.

Do not implement `community-trusted` in this phase.

Dual-publish remains valid in this phase: after a domain component accepts and
commits a record locally, publish the equivalent accepted semantic fact to
Agora. Reads still use existing stores.

### Phase 2: Capability-Passport Publish Authorization

Implement:

- capability-passport-backed `agora-publish@v1`,
- revocation freshness defaults from this document,
- delegation support through `key-delegation.v1` and `signing/agora-record`,
- module caller binding for Dator and Seed Directory publishers.

### Phase 3: Protected Subscribe And Replay Rebuild

Implement:

- `agora-subscribe@v1` for restricted topics,
- one `agora/subscribe` grant covering historical query and live subscribe in
  M1,
- `agora-query-attestation.v1` on historical query responses,
- subject-index query filtering by topic authorization,
- replay/subscription from Agora into materialized projections.

Required test shape:

```text
ProjectionFromLegacyStore
==
ProjectionFromAgoraReplay
```

### Phase 4: Agora-Backed Projection And Future Attestations

Let catalog/directory projections be fed primarily by Agora replay while
keeping their domain APIs intact.

This is also the earliest phase for:

- org policy beyond the current single-custodian model,
- richer attestation profiles,
- `community-trusted` as computed status from signed reputation facts and local
  `ReputationProjection`,
- rate budgets,
- operator UI for roots, grants, denials, revocation freshness, and replay
  diagnostics.

### Phase 5: Legacy Relay As Compatibility Shim

Keep legacy relay formats only for old clients, tests, or bridge surfaces.
Canonical public/federated feeds use `agora-record.v1`.

## Implementation Checklist

For each candidate subsystem:

1. Identify whether the artifact is public/federated, topic-shaped, signed, and
   append-only.
2. If yes, define the `record/kind`, `topic/key` convention,
   `content/schema`, and `record/about` hints.
3. Keep the domain API and materialized projection unless the domain is truly
   just an Agora UI surface.
4. Publish accepted semantic facts, not raw unvalidated requests.
5. Add replay/subscription into the projection.
6. Add equivalence tests between legacy projection and Agora-rebuilt
   projection.
7. Keep rejection/audit feeds separate and scoped to avoid enumeration and spam.
8. Do not move capability, passport, revocation, trust, or settlement semantics
   into Agora core.

## Anti-Goals

- Do not make every client learn Agora topic naming and raw record query rules.
- Do not remove Seed Directory or Offer Catalog as semantic facades.
- Do not merge Agora with Memarium.
- Do not put private/direct-only whispers on public Agora topics.
- Do not replace domain validation with envelope verification.
- Do not publish rejected/spammy requests into public feeds by default.

## North Star

```text
Agora stores and federates accepted public records.
Domain components interpret those records as discovery state, offers, opinions,
signals, logs, or announcements.
Memarium remembers what must not disappear under local classification policy.
```

## Additional Implementation Hints

These hints are intentionally narrower than a protocol specification. If an
existing proposal, schema, or `agora-core` primitive already owns a contract,
this document should reference it rather than define a parallel variant.

### Agora Publish, Replay, And Subscribe Authorization

Implement `agora-publish@v1` and `agora-subscribe@v1` as capability-passport
profiles rather than local transport ACLs.

Publish authorization shape:

```text
caller/domain adapter
  -> CallerBinding
  -> capability-passport.v1 allowed_callers check
  -> agora-publish@v1 topic/kind/schema profile check
  -> revocation freshness check
  -> accepted agora-record.v1
```

Subscribe authorization shape:

```text
caller/query adapter
  -> CallerBinding
  -> public-topic fast path OR capability-passport.v1 allowed_callers check
  -> agora-subscribe@v1 topic/mode profile check
  -> revocation freshness check
  -> historical replay, live stream, or subject-index query
```

Rules:

- No component may publish or subscribe to arbitrary topics just because it can
  reach Agora.
- Topic namespace authorization is a capability/profile boundary, not merely an
  HTTP auth-token boundary.
- Domain adapters request the narrowest topic prefix needed by their projection
  or publication task.
- Public topics can use public read by default; restricted or policy-bound
  topics require `agora-subscribe@v1`.
- Subject-index queries are not a bypass. They must filter by the caller's
  topic authorization.
- Module-local auth tokens identify the transport caller; they do not replace
  capability passport authorization.

### Agora Envelope Canonicalization

Do not redefine Agora signing in this note. Use `agora-core` as the executable
contract.

Current contract:

```text
record/id payload:
  canonical agora-record with record/id, signature, relay/received-at, relay/id, relay/hops omitted

signature payload:
  canonical agora-record with signature, relay/received-at, relay/id, relay/hops omitted
  record/id is included after it has been computed and stamped
```

Consequences:

- `record/id` is a content address, not a structured sequencer.
- The author signature binds the stamped content address.
- Relay metadata is hop-local and not author-signed.
- Envelope verification is not domain payload validation; domain payload rules
  stay in the owning domain engine.

### Record IDs

Do not introduce structured IDs such as:

```text
record:agora:<topic-hash-prefix>:<kind>:<content-sha256-prefix>
```

Agora already has a content-addressed `record/id` computed by `agora-core`.
If humans need diagnostics, expose `topic/key`, `record/kind`, `record/about`,
and `content/schema` next to the opaque record ID.

### Historical Replay And Authorization

Replay of accepted facts is not the same operation as accepting a new write.
Keep two paths separate:

```text
live write admission:
  domain validation
  current authorization
  current revocation freshness
  local commit
  Agora publication of the accepted fact

projection replay:
  envelope verification
  domain payload verification
  projection rules for already accepted facts
  domain-specific revocation interpretation for historical facts
```

A replay path that silently skips revocation semantics is a security defect. A
replay path that reruns today's live admission checks against every historical
accepted record is usually a correctness defect. The projection must document
whether it rebuilds from trusted accepted facts, from raw requests, or from a
mixed stream.

### Relay Metadata In Agora-Native Model

Use the existing Agora relay fields:

```text
relay/received-at
relay/id
relay/hops
```

Do not invent a new `relay/received` object in this document. Additional origin
or `do-not-forward` metadata needs an Agora extension proposal before it becomes
envelope shape. `relay/hops` is now part of the Agora envelope and is excluded
from both `record/id` and author-signature payloads, like `relay/id` and
`relay/received-at`.

During transition:

- Phase 1 may wrap legacy `service-offer-relay.v1` as `content`.
- The Agora envelope still uses the existing relay fields.
- Later phases can move toward `content/schema = "service-offer.v1"`, with
  relay-specific metadata remaining in the Agora envelope or in a formally
  specified extension.

### Crate Boundaries

Do not split crates first. Start with adapter traits/modules inside the current
owners and extract only after a second implementation makes the boundary real.

Practical first cut:

```text
agora-core / agora-service
  owns agora-record.v1, canonicalization, signing, storage, relay/query surface

seed-directory
  owns SeedDirectoryEngine, Projection, and SeedDirectoryAgoraAdapter

catalog / Dator / Arca
  own offer publication, observed-offer projection, trust admission, and query surfaces

capability / capability-binding
  own passports, bindings, profile evaluation, and authorization caches

memarium / memarium-runtime
  own local durable memory and read/write capability enforcement
```

Adapters translate domain semantic events into Agora records and replayed Agora
records back into projections. They do not own domain policy.

### Capability Passport Authorization Cache

The optimization should follow the implemented `capability-binding` shape, not
a weaker ad-hoc key.

Current safe cache dimensions:

```text
passport signature cache:
  passport_id + signed_artifact_digest

profile evaluation cache:
  passport_id + signed_artifact_digest + operation_hash

authorization decision cache:
  caller_digest
  operation_hash
  passport_id
  signed_artifact_digest
  binding_fingerprint
  revocation_view_fingerprint
  local_t_max_seconds
```

Keep per-call audit emission even when a cache is hit. Do not cache an
Authorized decision across a changed passport digest, binding fingerprint, or
revocation view fingerprint.

### Write Path Signature Separation

Accepted public facts can involve two different proofs:

1. Domain proof: authorizes the request or domain artifact, for example a
   capability passport, node advertisement signature, or provider-signed
   service offer.
2. Agora envelope signature: attests that a participant, nym, node, or delegated
   key recognized by local policy published this accepted fact into Agora.

Do not conflate them. A Seed Directory or Offer Catalog engine may validate a
client/domain artifact, commit an accepted fact, and then publish an Agora
record signed by the local publishing authority. The exact Agora author key must
follow the existing Agora author/delegation policy; it should not be hard-coded
as "the node/operator key" in this document.

### Topic Naming Stability

Agora topics are part of the federation contract. Once a topic convention is
established and records are published, changing the topic path is a breaking
change for subscribers.

```text
stable:
  orbiplex/seed-directory/v1/{federation-id}/adv

breaking without migration:
  orbiplex/v2/seed-directory/{federation-id}/advertisements
```

If a topic convention must change, version it explicitly in the path and keep
the old topic readable during a migration window. Replay subscribers should be
able to consume old and new topics during transition.

### Rejection/Audit Feed Scope

A public rejection feed is optional and risky. It can become an oracle for
probing policy, enumerating identities, or leaking intent. Prefer an
operator-local rejection feed first.

Public rejection records MUST NOT include:

- the full raw request body
- caller passports or identity-binding artifacts
- internal policy evaluation traces
- precise diagnostics that reveal gate internals

Public rejection records MAY include:

- attempted `record/kind` or operation class
- stable rejection class, such as `expired`, `unauthorized`, `invalid`,
  `stale`, `revoked`, or `policy-denied`
- canonical request digest
- timestamp

Operator-local rejection records may carry richer diagnostics because they stay
inside the operator control plane.

## Code Review Disposition 2026-05-01

The review below is retained as a historical checklist. After verification:

- Finding 1 is obsolete: `schema-gate`, `catalog`, and `seed-directory` compile and the referenced schema files exist in the working tree.
- Findings 2-4 are real architectural gaps. The M1 contract above now defines
  the intended capability-passport design for `agora-publish@v1`,
  `agora-subscribe@v1`, caller binding, and revocation freshness; the remaining
  work is implementation, not a local transport tweak.
- Finding 5 is valid cleanup, but not a correctness bug; keep it as a later `agora-core` builder extraction.
- Finding 6 is intentional for the signing adapter contract: `/v1/agora/records.sign` documents `sha256:pending` as a placeholder and overwrites it before ingest.
- Finding 7 is addressed for Seed Directory HTTP responses by surfacing `agora_publish_status` when a publisher is configured.
- Finding 8 is valid duplication in the Python bridge; no local fix without introducing a shared service-offer conversion boundary.
- Finding 9 requires an Agora envelope/schema extension and remains architectural.
- Findings 10 and 11 are addressed: Seed Directory records now carry diagnostic tags and topic segment normalization strips leading/trailing replacement dashes with `default` fallback.
- Finding 12 is already covered semantically by `seed-directory::agora` mismatch tests; schema-gate intentionally validates only structure.

## Code Review

Review of `node/` changes (working tree, state as of 2026-05-01) against the
guidance in this document and the Additional Implementation Hints section.

### Critical (will not compile)

**1. Missing `node_advertisement_validator()` and related definitions**

`schema-gate/src/lib.rs` references `node_advertisement_validator()` in the
`ContractFamily::NodeAdvertisementContent` branch, but does not define that
function. It also lacks the static `NODE_ADVERTISEMENT_CONTENT_VALIDATOR`
validator and the `"node-advertisement.v1.schema.json"` branch in
`compile_schema`. The `node_advertisement_v1_accepts_seed_listing_payload`
test will not compile either.

The same applies to `service-offer.v1.schema.json` and
`seed-capability-registration.v1.schema.json`: the `compile_schema` branches
exist, but the corresponding files under `schema-gate/contracts/schemas/agora/`
must exist as tracked files. They appear as untracked in `git status`, so they
exist physically but still need to be added formally.

### Serious

**2. Missing `agora-publish@v1` and `agora-subscribe@v1` profiles**

The "Agora Publish Authorization" section states explicitly: "Publishing to an
Agora topic is a capability-gated operation". The code, however, does not define
either `agora-publish@v1` or `agora-subscribe@v1` in
`capability-binding/src/lib.rs` (`ProfileRegistry::with_builtins()`).
`SeedDirectoryAgoraPublisher` publishes facts through a trait, but nothing
checks whether the publisher has a passport authorizing publication to the
specific topic. The same applies to Dator publishing offers: it uses an HTTP
auth token, not a passport.

Recommendation: add an `agora-publish@v1` profile with `agora/publish` grants
and a `topics` field for topic-prefix patterns, plus `agora-subscribe@v1` with
`agora/subscribe`.

**3. Python adapters (Dator, Arca) bypass the passport pipeline**

Dator (`middleware-modules/dator/service.py`):
- `offer_agora_json_request` authorizes through `OFFER_AGORA_AUTH_HEADER` plus
  auth token (module capability authtok), not through a capability passport.
- `publish_offer_snapshot_to_agora` calls `/v1/agora/records.sign` and
  `/v1/agora/topics/.../records` without an `agora-publish` passport.

Arca (`middleware-modules/arca/service.py`):
- `sync_agora_offer_snapshots_once` replays topic records without an
  `agora-subscribe` passport. It uses a URL query auth token, not a passport.

Both adapters work in a "trusted localhost daemon" model where authtok is
sufficient. If Agora is to become a multi-tenant federated substrate, however,
topic-level authorization through passports becomes necessary.

**4. Arca replay does not pass through the `authorize()` pipeline**

`sync_agora_offer_snapshots_once` fetches records from Agora and inserts them
directly into `upsert_observed_offer`. It does not perform:
- record-author signature verification (it assumes Agora already verified it),
- revocation freshness checking (`max_revocation_staleness_seconds`),
- `agora-subscribe` passport evaluation,
- `allowed_callers` checking.

Trust is delegated entirely to the Agora endpoint. This is acceptable when
replaying from the local daemon; it is not acceptable for federated replay.

**5. Duplicate `unsigned_record()` and `normalize_topic_segment()`**

Identical helper functions appear in `catalog/src/agora.rs` (lines 121-166)
and `seed-directory/src/agora.rs` (lines 226-277). They should move into a
shared module, for example `agora-core` as `AgoraRecord::builder()`.

**6. `record_id = "sha256:pending"` as a signing placeholder**

Status: clarified contract, not a bug.

`sha256:pending` is intentionally syntactically valid as `sha256:*`, because
the same `agora-record.v1` structure is used as unsigned input for
`POST /v1/agora/records.sign`. That endpoint is the only one allowed to accept
the placeholder, and it must overwrite it with the real content-addressed
`record/id`.

Runtime invariant: ingest, replay, and federation do not rely on format checks
alone. They must call full record verification, where `verify_record_id`
rejects `sha256:pending` as a content-address mismatch.

### Moderate

**7. `SeedDirectoryAgoraPublisher` does not distinguish error classes**

The `publish_advertisement` / `publish_capability_registration` /
`publish_revocation` trait methods return `Result<(), SeedDirectoryError>`.
The handler logs `warn!()` and returns 200/201 to the client even if Agora
publication failed. This is intentional best-effort behavior, documented in the
trait docstring, but:

- For revocations this is risky: the client received 200 and may believe the
  revocation is federated when it is not.
- There is no metric or operator-facing feedback beyond the log.
- Suggestion: add an optional `agora_publish_status` field in the HTTP
  response, or at least a metric for operator diagnostics.

**8. Python Dator: manual offer-key mapping**

`service_offer_content_from_snapshot` (dator/service.py) manually converts
keys from snake_case (local form) to kebab-case (wire format). The mapping is
scattered and prone to drifting from `ServiceOfferRecord` in Rust. If the
`service-offer.v1` schema changes, both places must be updated.

**9. `ObservedOfferRecord.relay_hops` is always 0 in the Agora adapter — resolved**

`agora-record.v1` already has `relay/hops` as a relay-local field. The offer
catalog adapter maps it to `ObservedOfferRecord.relay_hops`; a missing field
means 0.

### Minor

**10. Missing `record/tags` in Seed Directory records**

Seed Directory adapters (`advertisement_record`, `capability_registration_record`,
`revocation_record`) do not set `record_tags`. Dator sets
`["offer-catalog", "dator", "snapshot"]`, which helps filtering and diagnostics.
This should be made consistent: Seed Directory should tag its records, for
example with `["seed-directory", "federation"]`.

**11. `normalize_topic_segment` allows `-` as the normalization result**

Both implementations replace disallowed characters with `-`. If
`federation_id` ends with a special character, for example `test!`, the topic
gets `--` (double hyphen) when segments are joined, for example
`orbiplex/seed-directory/v1/test-/adv`. Rule: strip leading/trailing `-` after
normalization, or document that `federation_id` must be pre-validated.

**12. `seed_capability_registration_v1_accepts_registration_payload` test — dead code?**

The test in `schema-gate/src/lib.rs` (lines ~790-830 in the diff) constructs a
complete `seed-capability-registration.v1` payload, but does not check the
`passport.node_id == content.node/id` or
`passport.capability_id == content.capability/id` invariants. Those are checked
only in `seed-directory/src/agora.rs:57-67`. The schema-gate test should be
explicitly understood as validating structure only, not business semantics.
Consider adding a negative seed-directory test for mismatches in those fields.

### Compliance With dir-simplify.md — Summary

| Guidance | Status |
|---|---|
| Agora publish through capability passport | ✅ `agora-publish@v1` profile + daemon `agora.publish.authorize` + Agora `topic_acl: capability` |
| Agora subscribe through capability passport | ✅ `agora-subscribe@v1` profile + daemon `agora.subscribe.authorize`; subject index filters by topic auth |
| `agora-record.v1` signing contract (canonical JSON) | ✅ in `agora-core` |
| `record/id` content-addressed | ✅ `sha256:...`, but the builder emits pending |
| Revocation freshness in replay path | ✅ passport-gated subscribe uses capability-binding revocation freshness; domain projection replay still must document its own trust source |
| Relay metadata outside domain payload | ✅ `relay/received-at`, `relay/id`, `relay/hops` |
| Crate boundaries — adapters, not a monolith | ✅ `agora.rs` in catalog and seed-directory |
| Passport signature cache | ✅ capability-binding has signature/profile/authorization caches keyed by passport digest and revocation view |
| Write path: two distinct signatures | ✅ conceptually separated |
| Topic naming stability | ✅ `/v1/` prefixes |
| Rejection feed scope | ❌ rejection feed not implemented |
| Publish accepted facts, not raw requests | ✅ Seed Directory publishes after acceptance |
| Dual publish (Phase 1) | ✅ Seed Directory + Dator |
