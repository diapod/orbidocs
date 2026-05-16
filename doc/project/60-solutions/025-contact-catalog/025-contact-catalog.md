# Contact Catalog

`Contact Catalog` is a node-attached domain catalog for opt-in private contact
discovery. It lets a user publish a route candidate for an external contact
handle, such as an email address or phone number, without turning Seed Directory
into a people directory and without publishing raw `phone/email -> participant`
maps.

Status: `partial`

Date: `2026-05-16`

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

- `done` — Node `contact-catalog-core` validates `contact-claim.v1`, verifies
  participant/delegated participant signatures, rejects node-only signatures,
  evaluates `email-control@v1` / `phone-control@v1` passports, and checks
  passport signature, expiry, profile match, and revocation freshness before
  admission.

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
- return `contact-lookup-result.v1` as a route candidate or invitation-required
  result;
- never return raw `participant:did:key` by default;
- emit no-match audit entries without storing or exposing raw queried handles.
- support host-composed Artifact Delivery `selector/kind = "contact-lookup"`
  without making Contact Catalog an AD payload resolver. In that integration,
  AD passes `selector/purpose = "contact-request/messaging"` to express that
  lookup is being used for a messaging contact request, not for full message
  delivery.

Status:

- `done` — Node `contact-catalog-service` exposes authenticated invitation-only
  `POST /v1/contact-catalog/lookups`, returns `contact-lookup-result.v1`, rate
  limits by auth fingerprint + digest + purpose, rejects raw handle-like lookup
  inputs, writes redacted lookup audit without raw query values or root
  participant ids, and exposes redacted counters/recent policy events in service
  status. The daemon owns an opt-in supervised runtime on stable loopback and a
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

- `partial` — The daemon registers a default in-process Artifact Delivery
  acceptor target `contact.request`, persists `contact-request.v1` state, creates
  durable `contact-request.received` notifications, exposes host-owned
  accept/reject actions, and issues `messaging-receive@v1` passports on
  acceptance. Validation tests cover real participant signatures, expiry, bad
  purpose, bad signature, and redacted notification wording. Broader supervised
  multi-process AD accept/reject tests remain open.

### Local Contact Store

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`

Related schemas:

- `local-contact.v1`

Responsibilities:

- store raw external handles, labels, local relationship state, and pairwise
  nym mappings locally;
- keep the store unpublished by default;
- persist user-level continuity data needed to restore accepted contacts after
  nym regeneration or node recovery;
- expose only redacted or digest-bound references to network artifacts.

Status:

- `partial` — The daemon owns
  `<node-data-dir>/storage/local-contacts.sqlite` and exposes local
  create/list/get/patch/archive routes. Raw handles remain daemon-local and are
  not emitted by Contact Catalog lookup, Seed Directory records, or shared
  lookup audit. Recovery/backup semantics for local contacts and pairwise nym
  mappings remain open.

## May Implement

### Federated Contact Catalog Peer Fetch

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-claim.v1`

Responsibilities:

- use `ObservedCatalogStore<ContactClaimRecord>` only for communities that
  explicitly accept a private peer/fetch federation model;
- preserve publisher and origin provenance;
- forbid raw contact handles, unsalted public hashes, and public-log-style
  contact projections in federated records;
- keep Agora out of the Contact Catalog propagation path.

Status:

- `partial` — `node/catalog::CatalogAdapter<T, F>` now has a generic
  `ObservedRecord<T>` fetch contract and Contact Catalog defines
  `RemoteContactClaimFilter`; `contact-catalog-service` uses a
  `RemoteContactCatalogHttpAdapter` to refresh trusted provider claims into a
  sidecar remote cache. Provider policy remains trusted-only and no Agora
  publication/relay path is introduced. Broader multi-process trusted-provider
  acceptance remains open.

### Blinded or PSI Lookup

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-lookup-result.v1`

Responsibilities:

- replace or supplement authenticated invitation-only lookup with stronger
  private discovery profiles once the cryptographic protocol is selected;
- keep the result artifact stable so clients do not depend on the lookup
  protocol internals.

Status:

- `deferred`

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

## Produces

- `contact-lookup-result.v1`
- notification records for `messaging.contact-request`
- `capability-passport.v1` under `messaging-receive`
- local audit facts about admission, lookup, no-match, acceptance, and rejection

## Notes

The MVP is deliberately invitation-only. This leaves enough room for a useful
first implementation while avoiding the false precision of low-entropy lookup
handles. Stronger private lookup protocols can later replace the lookup edge
without changing the route-candidate contract.

Concrete crate/module ownership belongs in the Node implementation repository.
The expected implementation shape is a Rust supervised HTTP middleware that
links `orbiplex-node-catalog`, implements `ContactClaimRecord: CatalogRecord`,
and stores data under a middleware-owned SQLite database such as
`<node-data-dir>/storage/contact-catalog.sqlite`.
