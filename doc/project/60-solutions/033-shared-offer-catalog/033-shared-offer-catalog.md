# Shared Offer Catalog

The `Shared Offer Catalog` is a Node-attached middleware solution component that
materializes a public/federated offer read model from Agora `offer-snapshot`
records.

It is deliberately not the provider authority. `Dator` owns local standing
offers and provider execution. Agora owns the durable publication log. The
Shared Offer Catalog owns the domain projection, admission diagnostics, and
query surface over that log.

## Purpose

The component is responsible for:

- replaying configured Agora offer-snapshot topic pages,
- verifying outer Agora record admission through the daemon
  `agora.record.admit` host capability,
- verifying provider publication authority through the daemon
  `seed.directory.query` host capability,
- requiring an active `offer-snapshot-publisher` capability for the provider
  node and provider participant,
- verifying the inner provider-authored `service-offer.v1` signature through
  the shared Python `offer_catalog` library,
- storing the current offer projection in SQLite through the shared
  `lib/catalog.py` `SqliteCatalog` substrate,
- exposing active-offer query APIs with provenance and trust metadata,
- retaining rejected/skipped replay diagnostics.

## Scope

The component does not own:

- local standing-offer publication,
- service-order dispatch or result delivery,
- provider execution,
- settlement or procurement authority,
- peer-message fetch/push listeners.

Those concerns remain in `Dator`, `Arca`, and daemon-owned transport layers.

## Capability Names

- `local-offer-catalog` — provider-side local catalog of one node's own offers,
  owned by Dator.
- `offer-snapshot-publisher` — provider authority to publish signed offer
  snapshots into shared catalog admission.
- `shared-offer-catalog` — public/federated projection and query role owned by
  this component.

Legacy peer-message names such as `offer-catalog.fetch.request` and
`offer-catalog.push` remain compatibility wire names only.

## Implementation

Reference implementation:

- `node/middleware-modules/lib/offer_catalog.py`
- `node/middleware-modules/offer-catalog/service.py`
- `node/middleware-modules/offer-catalog/config/00-offer-catalog.json`

The same Python runtime is embedded by Arca as a buyer-local cache, so public
catalog deployment and buyer-local cache deployment reuse one implementation
instead of forking catalog mechanics.

## Query Surface

- `GET /v1/enact/service-catalog`
- `GET /v1/offer-catalog/replay/status`
- `GET /v1/offer-catalog/replay/diagnostics?limit=N`
- `POST /v1/offer-catalog/replay/resync`
- `POST /v1/offer-catalog/replay/reset-cursor`

The service-catalog query supports `service_type`, provider participant,
provider node, `active` / `active_only`, and `limit`. Active-only is default.

## Withdrawal

Withdrawal is modeled as a higher-`sequence/no` `service-offer.v1` snapshot with
`offer/status = "withdrawn"` and a contract-valid `expires-at`. The projection
retains the row for inspection but hides it from active queries.

## Status

`partial/done-slice`: the reference Node implementation has the shared Python
runtime, standalone middleware service, Arca embedded-cache integration,
fail-closed host Agora admission hook, Seed Directory provider admission hook,
query surface, replay diagnostics, and withdrawal active filtering.

Remaining follow-up is operational: public deployment profiles should enable
`publish_passport_on_start` or publish the `shared-offer-catalog` passport
through the existing host capability-passport publication flow.
