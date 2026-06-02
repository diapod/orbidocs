# Contact Catalog

`Contact Catalog` is a node-attached domain catalog for opt-in private contact
discovery. It lets a user publish a route candidate for an external contact
handle, such as an email address or phone number, without turning Seed Directory
into a people directory and without publishing raw `phone/email -> participant`
maps.

Status: `hard-MVP done` (the broader solution remains `partial` for
post-MVP privacy/federation expansion)

Date: `2026-05-16`

Hard-MVP tracker status: `100% implemented`. All `Must Implement`
capabilities in the Solution 025 sidecar and all Proposal 058 tracker rows are
`done`; remaining work named in this document is explicitly post-MVP hardening.

## Executive Summary

Contact Catalog answers one narrow question:

```text
Given a contact handle I already know, is there a safe Orbiplex route candidate
for requesting contact with the handle controller?
```

The MVP profile is intentionally conservative:

```text
authenticated caller
  -> invitation-only lookup
  -> route candidate
  -> contact-request.v1 over Artifact Delivery / INAC
  -> recipient-local consent
  -> capability-passport.v1 for messaging-receive
```

The catalog owns contact-domain admission and lookup policy. Seed Directory only
discovers Contact Catalog providers through the `contact-catalog` capability.
The Node daemon does not learn phone or email semantics; it supervises the
middleware, exposes host capabilities, and transports artifacts through existing
planes.

The solution-level Seed Directory boundary is defined separately in
`doc/project/60-solutions/031-seed-directory/031-seed-directory.md`.

## Context and Problem Statement

Proposal 058 defines Contact Catalog as a domain catalog separate from Seed
Directory. Story 010 uses it to let Daniel message Marcin by an email address
Daniel already knows.

The implementation must preserve three boundaries:

- local address-book data stays local and may contain raw handles;
- Contact Catalog records contain opt-in claims, lookup indexes, route
  candidates, expiry, revocation, and admission evidence;
- Seed Directory advertises providers and capability evidence, not people.

## Must Implement

### Contact Claim Admission

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`

Related schemas:

- `contact-claim.v1`
- `capability-passport.v1`

Responsibilities:

- accept `contact-claim.v1` only after validating contact-control evidence;
- require `email-control` or `phone-control` passport freshness for email and
  phone handles;
- reject raw handle publication in catalog records under the MVP profile;
- enforce purpose allowlists, expiry, revocation reference shape, and monotonic
  `sequence/no`;
- store admitted claims through `CatalogStore<ContactClaimRecord>` rather than a
  bespoke storage layer.

Status:

- `done` — Node `contact-catalog-core` validates canonical route-set
  `contact-claim.v1`, verifies
  participant/delegated participant signatures, rejects node-only signatures,
  evaluates `email-control@v1` / `phone-control@v1` passports, and checks
  passport signature, expiry, profile match, and revocation freshness before
  admission. It also owns shared lookup request/result DTOs and the normalized
  lookup-index helper used by consumer-side code.

### Invitation-Only Lookup

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `contact-lookup-result.v1`
- `routing-subject-binding.v1`

Responsibilities:

- expose `/v1/contact-catalog/lookup` or an equivalent supervised middleware
  endpoint under `catalog_kind = "contact"`;
- require authenticated callers and rate limits before lookup execution;
- return `contact-lookup-result.v1` as a route-set candidate or
  invitation-required result;
- never return raw `participant:did:key` by default;
- use opaque `contact-route:<digest>` invitation refs when the local
  contactability draft is participant-routed;
- emit no-match audit entries without storing or exposing raw queried handles.
- support host-composed Artifact Delivery `selector/kind = "contact-lookup"`
  without making Contact Catalog an AD payload resolver. In that integration,
  AD passes `selector/purpose = "contact-request/messaging"` to express that
  lookup is being used for a messaging contact request, not for full message
  delivery.

Status:

- `done` — Node `contact-catalog-service` exposes public invitation-only,
  blinded-digest and PSI-mode `POST /v1/contact-catalog/lookups`, returns
  `contact-lookup-result.v1` with `result/routes[]` and `selected/route`, rate
  limits by client fingerprint + digest + purpose, rejects raw handle-like
  lookup inputs, writes redacted lookup audit without raw query values or root
  participant ids, and exposes redacted counters/recent policy events in service
  status. Node `contact-catalog-client` is the provider-free consumer adapter:
  it performs bounded HTTP lookups and parses canonical `contact-lookup-result.v1`
  without owning provider admission, provider sync, or storage. The daemon uses
  that client for AD `contact-lookup` and exposes the same consumer path as
  host capability `contact.lookup`, so a node may consume Contact Catalog
  providers even when it does not run `contact-catalog-service`. The daemon owns
  an opt-in supervised runtime on stable loopback and a
  `/v1/contact-catalog/status` proxy; a process smoke starts the real service
  binary and verifies readiness plus projection status through that proxy.

### Contact Request Admission

Based on:

- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `contact-request.v1`
- `notification.v1`
- `notification-action.v1`
- `capability-passport.v1`

Responsibilities:

- register exactly one authoritative acceptor for `contact-request.v1`;
- turn accepted contact requests into durable user notifications with accept and
  reject actions;
- on acceptance, issue a narrow `messaging-receive` capability passport scoped
  to the accepted sender, recipient route, public handle reference, operation,
  expiry, and revocation reference;
- on rejection, record the local decision without minting authority.

Status:

- `done for hard-MVP` — The daemon registers a default in-process Artifact Delivery
  acceptor target `contact.request`, persists `contact-request.v1` state, creates
  durable `contact-request.received` notifications, exposes host-owned
  accept/reject actions, and issues `messaging-receive@v1` passports on
  acceptance. Validation tests cover real participant signatures, expiry, bad
  purpose, bad signature, and redacted notification wording. Story 010 strict
  smoke exercises the operator notification accept path end-to-end; broader
  failure-matrix AD accept/reject tests remain post-MVP hardening.

### Local Contact Store

> **Ownership note (cross-reference to Solution 032):** With the
> introduction of the Local Relationship Layer (Solution 032), semantic
> relationship state — classes, memberships, relationship predicates,
> and pairwise relationship facts — moves to Solution 032. Raw handles,
> UX labels, and local address-book records stay in the daemon Local
> Contact Store. Contact Catalog retains only public discovery /
> route-set lookup state. The expected flow becomes:
> `Catalog lookup (public discovery) → Local Relationship annotation (private) → consumer policy (passport-gated)`.
>
> `local-contact.v1` schema is preserved unchanged. Its recovery bundle
> remains sealed through the Pseudonym Vault, while `local-relationship`
> vault entries carry relationship facts. Relationship classes such as
> `friends` are not a Catalog concept; Catalog never sees them.

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

Related schemas:

- `local-contact.v1`

Responsibilities:

- store raw external handles, labels, and local address-book mappings locally;
- keep the store unpublished by default;
- persist user-level continuity data needed to restore local contacts after
  node recovery;
- expose only redacted or digest-bound references to network artifacts.

> Solution 032 does not make Contact Catalog the owner of private
> relationships. It only moves relationship classes, membership facts,
> predicates, and pairwise relationship facts out of Messaging/AD/Catalog
> into the Local Relationship Layer.

Status:

- `done for hard-MVP` — The daemon owns
  `<node-data-dir>/storage/local-contacts.sqlite` and exposes local
  create/list/get/patch/archive routes. Records now carry compatible `label`,
  explicit `labels[]`, `metadata {}`, UX/provenance fields, and an active
  pairwise contact-nym pointer. The store also maintains
  `local_contact_pairwise_mappings` with `active`, `rotated`, `revoked`, and
  `archived` lifecycle states so nym rotation is history-preserving. Raw handles
  remain daemon-local and are not emitted by Contact Catalog lookup, Seed
  Directory records, or shared lookup audit. Durable local recovery mirror
  records exist for messaging recovery; the local contact store can export and
  replay local-contact, pairwise-mapping, and messaging-recovery mirror records
  without reactivating revoked or archived pairwise mappings.
  `pseudonym-vault.v1` can carry a sealed
  `local-contact-recovery-bundle.v1`; vault import replays that bundle, and
  daemon startup replays the latest operational-vault-key sealed vault
  snapshot. Legacy root-only snapshots are migration/recovery inputs, not the
  normal hot-path profile. Explicit operator replay/export hooks accept
  `local_passphrase` for `root+local-passphrase` vaults without opening those
  vaults during unattended startup or weakening their wrap profile.

## May Implement

### Federated Contact Catalog Peer Fetch

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-claim.v1`

Responsibilities:

- use `ObservedCatalogStore<ContactClaimRecord>` only for communities that
  explicitly accept a private peer/fetch federation model;
- never expose a public anonymous dump of the contact catalog; ordinary clients
  use authenticated lookup, while bulk/list fetch is local-operator or
  trusted-provider sync only;
- let the host/daemon own discovery, trust policy, passport validation, auth
  material, and revocation freshness;
- use direct catalog-to-catalog HTTP as the data plane only after host policy
  has marked the provider trusted;
- implement reusable fetch/merge/replay mechanics in the generic catalog
  abstraction, while this service owns Contact Catalog runtime and privacy
  policy;
- preserve publisher and origin provenance;
- forbid raw contact handles, unsalted public hashes, and public-log-style
  contact projections in federated records;
- keep Agora out of the Contact Catalog propagation path.

Status:

- `done for hard-MVP` — `node/catalog::CatalogAdapter<T, F>` now has a generic
  `ObservedRecord<T>` fetch contract and Contact Catalog defines
  `RemoteContactClaimFilter`; `contact-catalog-service` uses a
  `RemoteContactCatalogHttpAdapter` to refresh trusted provider claims into a
  sidecar remote cache. `node/catalog` now also carries the generic
  `sync_catalog_provider(...)` mechanic for fetch, observed-record validation,
  loop guardrails, self-origin rejection when the daemon provides the local
  node id, sequence-aware merge, data-derived high-water metadata and counted
  outcomes. Contact Catalog exposes authenticated
  `GET /v1/contact-catalog/sync/claims` as the trusted provider snapshot
  contract and records provider sync state in the sidecar with last-run counts
  and cumulative totals.
  Provider tombstones are now part of the trusted-provider snapshot body and
  are cached durably; replay/restart hides remote claims whose sequence is
  covered by a cached tombstone, and sync status records a retryable/terminal
  failure class.
  Provider policy remains trusted-only for sync, but operators can now inspect
  discovered providers and set `trusted`, `uncertain`, or `blocked` from
  `/admin/contact-catalog` over the service policy endpoint. No Agora
  publication/relay path is introduced. Provider trust changes are durably
  audited with actor, a required reason capped at 1000 characters,
  previous/next state, passport hash and endpoint.
  Local tombstone facts are produced for operator-tombstoned and
  projection-revoked claims, exported through `tombstones[]`, and applied on
  active-only read paths after restart. Broader production federation matrices
  remain post-MVP hardening.

### Blinded or PSI Lookup

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-lookup-result.v1`

Responsibilities:

- replace or supplement public invitation-only digest lookup with stronger
  private discovery profiles once the cryptographic protocol is selected;
- keep the result artifact stable so clients do not depend on the lookup
  protocol internals.

Status:

- `done for hard-MVP` — `orbiplex-node-crypto::contact_psi` provides auditable
  Ristretto255 DH-PSI primitives, and the Contact Catalog service accepts
  `blinded-digest` and `psi` lookup modes with mode/index pairing, redacted
  audit, rate limiting and route-set responses. Hard-MVP PSI uses
  `POST /v1/contact-catalog/psi/evaluate` for bounded evaluated elements and
  candidate tokens, then `POST /v1/contact-catalog/lookups` with
  `lookup_mode = "psi"` plus `psi/match-token`. The service-local PSI server
  seed is stored as plain base64url in the service SQLite database; the
  hard-MVP security boundary is the local data-dir filesystem, and the seed is
  not emitted through status, audit or sync. Broader PSI failure matrices remain
  focused lower-level tests rather than a separate top-level E2E harness;
  Story-010 strict `ad-smoke` remains the E2E gate.

## Out of Scope

- becoming a global address book;
- storing raw personal address books in a network catalog;
- treating phone or email control as legal identity assurance;
- issuing general friend-class capabilities;
- owning messaging UI or mailbox storage beyond the contact-request acceptor;
- making Seed Directory contact-aware.

## Consumes

- `contact-claim.v1`
- `contact-request.v1`
- `capability-passport.v1`
- `routing-subject-binding.v1`
- Seed Directory capability provider records for `contact-catalog`,
  `email-control`, and `phone-control`

Contact Catalog provider discovery is capability-first. The daemon asks Seed
Directory for providers advertising the `contact-catalog` capability and applies
the same local multi-directory query policy used by Artifact Delivery and other
discovery consumers. Contact Catalog remains the domain lookup service after a
provider is selected; Seed Directory does not become contact-aware and does not
authorize message delivery by itself.

## Produces

- `contact-lookup-result.v1`
- notification records for `messaging.contact-request`
- `capability-passport.v1` under `messaging-receive`
- local audit facts about admission, lookup, no-match, acceptance, and rejection

## Notes

The default MVP path remains invitation-only digest lookup, and the runtime also
accepts `blinded-digest` and `psi` lookup modes for claims indexed with the
matching private mode. This keeps the common path simple while letting stricter
privacy mechanics evolve at the lookup edge without changing the route-candidate
contract.

Concrete crate/module ownership belongs in the Node implementation repository.
The expected implementation shape is a Rust supervised HTTP middleware that
links `orbiplex-node-catalog`, implements `ContactClaimRecord: CatalogRecord`,
and stores data under a middleware-owned SQLite database such as
`<node-data-dir>/storage/contact-catalog.sqlite`.
