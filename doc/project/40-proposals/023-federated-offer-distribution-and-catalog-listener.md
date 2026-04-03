# Proposal 023: Federated Offer Distribution and Catalog Listener

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/30-stories/story-007.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/60-solutions/node.md`

## Status

Implemented

## Date

2026-03-31

## Executive Summary

The hard-MVP catalog is deployment-local: only offers published by supervised
provider modules running on the same Node are visible to the buyer bridge.

That suffices for a single-deployment demonstration, but not for a federation
where buyer Nodes and provider Nodes are separate deployments.

The decisions of this proposal are:

1. offer distribution should use a hybrid push/pull transport: providers push
   newly published offers to a known catalog service, while buyers pull from
   that service on demand and at startup,
2. observed offers from the network should live in a separate store with its
   own provenance boundary, isolated from locally committed offers,
3. trust for observed offers should be two-layered: federation-based (the
   offer's origin Node is a known peer) plus an operator-managed explicit
   whitelist of always-trusted provider participants,
4. the buyer bridge should resolve offers optimistically and rely on
   provider-side rejection codes (`offer-expired`, `queue-saturated`) already
   present in the protocol rather than adding a pre-order reservation step,
5. the catalog role should stay outside the daemon's minimal trusted core, but
   it may be hosted either by a compatibility `catalog-listener` sidecar or by
   the preferred `dator` middleware-owned observed-catalog path.

This keeps the trusted core small:

- `dator` owns the local committed catalog and participant-facing publication;
  the daemon no longer holds a local offer write path,
- observed offers carry explicit provenance and trust metadata and are
  admitted only after a trust check,
- the catalog service is a bounded role that can be co-located in hard-MVP
  deployments but carries its own responsibility boundary,
- `dator` owns the supply side (local standing offers, `offer-catalog.fetch.request`
  responder) and `arca` owns the demand side (observed catalog, peer discovery,
  combined buyer view); the daemon is catalog-free.

## Context and Problem Statement

`story-006` describes a federation where `Ola`, `Adam`, and `Marcin` each run
provider Nodes with `Dator` attached, while `Roman` runs a buyer Node with
`Arca` attached.

In this shape:

- provider Nodes publish `service-offer.v1` artifacts locally through `Dator`,
  which owns the full local offer lifecycle,
- buyer Node's `Arca` must be able to browse offers from all three providers,
  not only from the co-located provider module.

The current Node only holds a locally committed catalog. There is no mechanism
for a buyer Node to observe offers from remote provider Nodes.

Without a resolved distribution model:

- every real multi-party deployment requires manual workarounds,
- `Arca` cannot be a useful standalone buyer orchestrator,
- the distinction between `local-catalog` and `observed-catalog` remains
  implicit, making trust reasoning impossible to audit.

`node.md` names the roles needed in a minimal marketplace deployment but does
not freeze the wire contracts for offer propagation, the provenance boundary
for observed offers, or the trust model for admitting remote offers into a
buyer's catalog.

## Goals

- Define `service-offer-relay.v1` as the wire envelope for relayed offers.
- Define `trusted-provider.v1` as the operator-managed provider whitelist
  contract.
- Freeze the two-layer trust model: federation trust plus explicit whitelist.
- Freeze the `CatalogAdapter` behavior contract as the interface between a
  Node and a catalog service.
- Define `ObservedCatalogStore` as a provenance-separated store alongside the
  existing `CatalogStore`.
- Freeze hybrid push/pull as the Phase F distribution model: provider push to
  catalog service, buyer pull from catalog service.
- Keep the buyer bridge change minimal: `CatalogResolver` queries both stores;
  bridge rejects untrusted offers before procurement opens.

## Non-Goals

- This proposal does not define full peer-to-peer gossip for offer propagation
  over the WSS transport layer. P2P gossip may extend this model in a later
  phase.
- This proposal does not define multi-hop transitive federation trust beyond
  direct known peers.
- This proposal does not define reputation-gated offer admission.
- This proposal does not define a pre-order slot reservation protocol. The
  optimistic model with provider-side rejection is accepted for this phase.
- This proposal does not change `service-offer.v1` or `service-order.v1`.
- This proposal does not define the full catalog service implementation. The
  catalog service is an attached role with a frozen HTTP API contract; its
  internals are outside this proposal's scope.

## Decision

### 1. Hybrid Push/Pull Distribution

Offer distribution in this phase follows a hybrid model:

**Push path (provider side):**

`Dator` owns the local offer lifecycle: it commits new or refreshed offers to
its own storage and handles `offer-catalog.fetch.request` from peer Nodes.
Push notification to remote catalog peers travels through the daemon-owned
`peer.message.dispatch` host capability. Local commit is the source of truth;
any push failure does not roll back the committed offer.

**Pull path (buyer side):**

A buyer Node runs a background periodic task that calls
`CatalogAdapter::fetch_offers()` and upserts results into the local
`ObservedCatalogStore`. One synchronous pull is also performed at daemon open
before accepting buyer traffic, so the observed catalog is warm at startup.

This model does not require the catalog service to hold authority over offers.
It is an indexer and relay, not a source of truth. Provider Nodes remain the
authority over their own offers.

### 2. Separate ObservedCatalogStore

Locally committed offers and network-observed offers must live in separate
stores with separate provenance semantics.

The `ObservedCatalogStore` trait operates alongside the existing `CatalogStore`.
It is not a superset or extension of `CatalogStore`. The two stores have
distinct query surfaces:

- `CatalogStore` is the authority for locally published offers. Its results
  are always trusted.
- `ObservedCatalogStore` is the authority for network-observed offers. Its
  query surface returns only entries that have passed the trust check at admit
  time. Untrusted entries are stored internally but excluded from results.

The buyer bridge `CatalogResolver` queries `CatalogStore` first, then
`ObservedCatalogStore`. Local offers take precedence over observed offers for
the same `offer/id`.

### 3. Two-Layer Trust Model

An observed offer is admitted as trusted if either of the following holds at
the time it is upserted into the `ObservedCatalogStore`:

**Layer 1 — Explicit whitelist:**

The offer's `provider/participant-id` is present in the local
`TrustedProviderStore`. Explicit whitelist entries are operator-managed, persisted
as append-only facts, and take effect immediately. A provider may be explicitly
trusted before it has established a peer connection with the buyer Node.

**Layer 2 — Federation trust:**

The relay envelope's `relay/origin-node-id` is present in the buyer Node's
peer store as a known peer. Only direct known peers qualify for federation
trust in this phase; transitive multi-hop trust is explicitly deferred.

If neither layer matches, the offer is admitted with trust level `untrusted`
and is excluded from `ObservedCatalogStore` query results. It may be retained
internally for diagnostic purposes with a short TTL.

Trust is evaluated at admit time, not at query time. The trust level is stored
as part of the observed entry and is not re-evaluated on every query.

When the operator adds a provider to the explicit whitelist after the fact,
previously stored `untrusted` entries for that provider should be re-evaluated
on the next pull cycle, not retroactively.

### 4. Optimistic Bridge with Provider-Side Rejection

The buyer bridge does not send a pre-order reservation request. It resolves
one offer from the catalog, validates it locally, and opens procurement. If
the offer has expired or the queue is saturated at the provider side, the
provider rejects the `service-order` with an existing classified code:

- `offer-expired`
- `queue-saturated`
- `offer-seq-mismatch`

These codes are already part of the bridge rejection vocabulary from
`proposal-021`. `Arca` already handles rejection and retry. No new protocol
roundtrip is needed.

### 5. Catalog Ownership Boundary

The catalog service is not part of the daemon's minimal trusted core. It is a
bounded role with its own storage and query boundary.

The implemented ownership split:

- `dator` is the supply side:
  - owns local standing offers and participant-facing publication,
  - handles `offer-catalog.fetch.request` through the `inbound-peer` chain,
  - exposes `POST /v1/enact/offers/snapshot` for daemon-side local dispatch
    lookups,
- `arca` is the demand side:
  - owns observed catalog storage (SQLite),
  - owns trusted-provider policy,
  - runs background peer discovery and sync,
  - handles `offer-catalog.fetch.response` and `offer-catalog.push`,
  - serves the combined participant-facing `GET /v1/enact/service-catalog`,
  - uses the `catalog.local.query` host capability to include Dator's local
    offers in the combined view,
- `catalog-listener` remains available as a compatibility relay for
  deployments that still need it, but is not the preferred path,
- the daemon is catalog-free: it provides transport primitives
  (`peer.message.dispatch`, `peer.session.establish`, `catalog.local.query`,
  `seed.directory.query`, `capability.passport.issue`) but holds no offer
  state itself.

This keeps the split explicit: the daemon owns transport, session lifecycle,
and outbound `service-offer-relay.v1` relay routing; offer truth and catalog
state live entirely in middleware.

## Proposed Artifact Shapes

### `service-offer-relay.v1`

Purpose: wire envelope for a `service-offer.v1` in transit across a catalog
service or relay boundary. The inner offer remains intact and signed by the
provider. The relay envelope adds propagation metadata.

Minimum fields:

- `schema/v` — always `1`
- `relay/id` — stable relay-scoped identifier, prefixed `offer-relay:`
- `relay/origin-node-id` — `node:did:key:...` of the Node that first emitted
  this relay (the provider Node or a trusted relay)
- `relay/hops` — unsigned integer, maximum `3`; relays MUST drop envelopes
  where `relay/hops` would exceed the maximum
- `relay/relayed-at` — RFC 3339 timestamp of the most recent relay step
- `offer` — the full embedded `service-offer.v1` payload, including its
  original `signature`

The relay envelope itself is NOT signed by the relay node in this phase. Trust
derives from the inner offer's signature (provider-signed) plus the
`relay/origin-node-id` against the buyer's peer store and whitelist.

A later phase may add relay node signing to the envelope to support
multi-hop accountability.

### `trusted-provider.v1`

Purpose: operator-managed record of one explicitly trusted provider
participant. Used as the persistent form of whitelist entries.

Minimum fields:

- `schema/v` — always `1`
- `entry/participant-id` — `participant:did:key:...` of the trusted provider
- `entry/added-at` — RFC 3339 timestamp
- `entry/added-by` — `participant:did:key:...` or `operator` for the adding
  subject
- optional `entry/note` — free-form operator note, not interpreted by the Node

Removal is modeled as a separate `trusted-provider-removal.v1` fact or as a
`removed` boolean on the same record in storage. Both forms may coexist in an
append-only fact log.

### 6. Generic Catalog Substrate

The implementation substrate underneath this proposal no longer needs to be
offer-hardcoded.

The shared `catalog` crate may expose generic typed primitives such as:

- `CatalogRecord`,
- `CatalogStore<T>`,
- `ObservedCatalogStore<T>`,
- `CatalogPredicate<T>`,
- `CatalogResolver<T, ...>`,
- optional durable stores such as `SqliteCatalog<T>`.

Offer-specific types such as `ServiceOfferRecord`, `OfferFilter`, and relay
contracts remain stable on top of that substrate. This keeps the marketplace
protocol offer-specific while letting the storage and filtering mechanics be
reused by middleware or later catalog-like roles without re-implementing
sequence-aware upsert, expiry, or observed provenance semantics.

## Behavior Contracts

### CatalogAdapter

The `CatalogAdapter` is the behavior contract between the Node and a catalog
service. It is defined in the `catalog` crate as a trait. The Node does not
know or care whether the catalog service is co-located or remote.

Required operations:

- `fetch_offers(filter)` → list of `ObservedOfferRecord`
  - Returns all currently active observed offers matching the filter, as seen
    by the catalog service. The catalog service applies its own TTL expiry
    before returning results.
  - Idempotent. Safe to call repeatedly. The Node does not modify catalog
    service state through this call.

- `notify_offer(offer, from_node_id)` → unit
  - Pushes one locally published offer to the catalog service for indexing.
  - Best-effort: a failure does not roll back the local offer commit. The Node
    logs the failure and does not retry beyond the current call.
  - The catalog service is responsible for deduplication by `offer/id` plus
    `sequence/no`.

Implementations provided by the Node workspace:

- `LocalHttpCatalogAdapter` — HTTP client to a catalog service reachable at a
  configured base URL with an optional auth token.
- `InMemoryCatalogAdapter` — in-process adapter for daemon and launcher tests.

### ObservedCatalogStore

The `ObservedCatalogStore` is the behavior contract for the local store of
network-observed offers inside the Node daemon.

Required operations:

- `upsert_observed(entry: ObservedOfferEntry)` → unit
  - Admits one observed offer. Trust level is evaluated at this point and
    stored with the entry.
  - If an entry with the same `offer/id` and equal or lower `sequence/no`
    already exists, the upsert is silently ignored (monotonic replacement).

- `get_trusted(offer_id)` → `Option<ObservedOfferEntry>`
  - Returns the entry only if its stored trust level is `ExplicitlyTrusted`
    or `FederationTrusted`. Returns `None` for `Untrusted` entries.

- `list_trusted(filter)` → list of `ObservedOfferEntry`
  - Returns all trusted entries matching the filter, sorted by
    `observed_at` descending.

- `expire_stale(now)` → count of removed entries
  - Removes entries where the inner offer's `expires-at` is before `now`.
  - Also removes `Untrusted` entries older than a short diagnostic TTL
    (configurable, default `1h`).

### TrustedProviderStore

The `TrustedProviderStore` is the behavior contract for the operator-managed
explicit whitelist.

Required operations:

- `is_trusted(participant_id)` → bool
  - Returns `true` if the participant is currently on the whitelist (added
    and not removed).

- `add(participant_id, added_by, note)` → unit
  - Adds the participant to the whitelist. Idempotent if already present.
  - Persisted as an append-only `TrustedProviderFact::Added` in the daemon
    storage log.

- `remove(participant_id)` → unit
  - Removes the participant from the whitelist.
  - Persisted as `TrustedProviderFact::Removed`.

- `list()` → list of `TrustedProviderEntry`
  - Returns all currently active whitelist entries for operator inspection.

The projector for `TrustedProviderStore` is rebuilt from the storage log at
`Daemon::open()` using the same append-only fact replay pattern as
`LocalOrcLedger` and the gateway top-up projector.

### Trust Evaluation Algorithm

The following algorithm is applied at `ObservedCatalogStore::upsert_observed()`
time. `entry` is the incoming `ObservedOfferEntry` before trust level is set.

```
evaluate_trust(entry, trusted_provider_store, peer_store):

  participant_id = entry.offer.provider.participant_id
  origin_node_id = entry.relay_envelope.relay.origin_node_id

  if trusted_provider_store.is_trusted(participant_id):
    return ExplicitlyTrusted

  if peer_store.is_known_peer(origin_node_id):
    return FederationTrusted

  return Untrusted
```

`peer_store.is_known_peer(node_id)` returns `true` if the peer store holds a
current (non-expired, non-blocked) advertisement for that `node_id`. Only
direct known peers qualify. Transitive hops are not followed in this phase.

### CatalogResolver (buyer bridge integration)

The buyer bridge calls `CatalogResolver::resolve(offer_id)` instead of calling
`CatalogStore::get_active(offer_id)` directly.

`CatalogResolver` consults both stores in order:

```
resolve(offer_id, local_catalog, observed_catalog):

  if let Some(entry) = local_catalog.get_active(offer_id):
    return Ok(entry)          // local offers are always trusted

  if let Some(entry) = observed_catalog.get_trusted(offer_id):
    return Ok(entry.into())   // returns only trusted observed entries

  return Err(OfferNotFound)
```

The bridge never receives an `Untrusted` entry from this resolver. There is no
new `offer-not-trusted` rejection code visible to the order submitter: from the
submitter's perspective, an untrusted-only offer is simply not found.

## Operator Surfaces

The following control-plane surfaces must be added to the Node:

**Trusted provider management:**

- `POST /v1/trusted-providers` — add a provider to the whitelist
- `DELETE /v1/trusted-providers/{participant_id}` — remove a provider
- `GET /v1/trusted-providers` — list current whitelist entries

**Observed catalog inspection:**

- `GET /v1/service-offers?source=observed` — filter to observed-only entries
  (extends existing listing with a new `source` filter)
- `GET /v1/service-offers/{offer_id}` — existing endpoint; adds `source` and
  `trust_level` fields to the response when the entry is observed

**Launcher commands:**

- `trusted-provider-add --participant-id ... [--note ...]`
- `trusted-provider-remove --participant-id ...`
- `trusted-provider-list`

## Catalog Service HTTP API Contract

The catalog service must expose the following minimum HTTP API for the
`LocalHttpCatalogAdapter` to function. The internals of the catalog service
are outside this proposal's scope.

- `GET /v1/service-offers` — return active offers, with at minimum
  `service_type`, `provider_participant_id`, `provider_node_id`, and `limit`
  as query parameters
- `POST /v1/service-offers` — accept one `service-offer-relay.v1` envelope
  from a provider Node; respond `200 OK` or `409 Conflict` for duplicate
  `(offer/id, sequence/no)`

The catalog service may apply its own TTL expiry and deduplication. The Node
does not depend on the catalog service's internal storage model.

An optional authentication header (Bearer token) may be configured per
adapter instance. The same `authtok` pattern used for supervised middleware
modules is suitable.

## Deployment Notes

In a hard-MVP co-located deployment, one Node instance may run:

- the provider module (`Dator`) publishing offers locally,
- the catalog service as a supervised attachment receiving and serving those
  offers,
- the buyer module (`Arca`) pulling from the same local catalog service.

In a federated deployment:

- provider Nodes push offers to a shared catalog service,
- buyer Nodes pull from that shared catalog service,
- no direct peer connection between buyer Node and provider Node is required
  for catalog browsing; it is only required for actual procurement execution.

The catalog service URL is operator-configured per Node. There is no protocol
mechanism in this phase for catalog service discovery; that is intentionally
deferred.

## Open Questions (Deferred)

- Whether the relay envelope should carry a relay node signature for multi-hop
  accountability once `relay/hops` exceeds `1`.
- Whether `ObservedCatalogStore` should retain a bounded historical snapshot
  for audit and reputation purposes, or only keep currently active offers.
- Whether the catalog service should expose a subscription or long-poll
  endpoint for push-style buyer notification rather than periodic pull.
- Whether federation trust should expand to one-hop transitive peers once the
  peer governor semantics are more stable.
- How the catalog service should handle provider Node key rotation when
  `provider/participant-id` is stable but the signing key changes.
