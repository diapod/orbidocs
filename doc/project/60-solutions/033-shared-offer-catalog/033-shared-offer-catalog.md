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
- `node/middleware-modules/offer-catalog/config/profiles/public-shared-catalog.json`

The same Python runtime is embedded by Arca as a buyer-local cache, so public
catalog deployment and buyer-local cache deployment reuse one implementation
instead of forking catalog mechanics.

## Public Deployment Profile

The hard-MVP public deployment profile is data-only configuration:

- `deployment_shape = "public-shared"`,
- Agora replay enabled with `source_mode = "agora-primary"`,
- host `agora.record.admit` required,
- host `seed.directory.query` required for `offer-snapshot-publisher`,
- `shared-offer-catalog` capability passport publication enabled at startup.

The service keeps `/healthz` available for diagnosis, but `/readyz` stays
pending until the host issues and publishes the `shared-offer-catalog`
capability passport. The status surface exposes only passport identifiers and
pending reasons, not the full passport artifact.

The Node worktree carries a local public-profile smoke runner that imports the
real middleware under that profile, mocks only host/Agora HTTP boundaries,
verifies passport publication readiness, replays one authorized offer snapshot,
rejects bad-signature and unknown-provider records, keeps withdrawn records
hidden from active queries while visible for inspection, and checks the HTTP
service-catalog result.

## Passport Lifecycle

The `shared-offer-catalog` capability passport has a bounded validity requested
through `passport_expires_in_sec`. The hard-MVP public profile uses 24 hours
(`86400` seconds), requests the passport at service start, publishes it once, and
keeps `/readyz` pending until publication succeeds.

Supervisor-driven restart is the default operational boundary for renewal. For
the hard-MVP slice, operators should run the service under a supervisor that
restarts it before passport expiry or restart it manually as part of the
deployment runbook. Automatic in-process renewal remains optional future
hardening, not the baseline contract.

Public deployments must use HTTPS/TLS for non-loopback `agora.base_url` values;
the Node middleware fails closed before replay when public/shared mode is configured
with non-loopback HTTP. Loopback HTTP remains acceptable for local smoke runs,
development, and reverse-proxy topologies where the public TLS boundary sits
outside the middleware process.

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

`hard-MVP done`: the reference Node implementation has the shared Python
runtime, standalone middleware service, Arca embedded-cache integration,
fail-closed host Agora admission hook, Seed Directory provider admission hook,
query surface, replay diagnostics, withdrawal active filtering, a public/shared
deployment profile, classified/redacted passport-publication readiness
semantics, classified/redacted Host Agora and Seed Directory admission
diagnostics, and a local public-profile smoke runner with positive and negative
admission coverage.

Remaining work is post-MVP hardening: richer production monitoring, broader
multi-catalog deployment matrices, and eventual retirement of legacy
`offer-catalog.fetch` / `offer-catalog.push` compatibility wire names after
Agora-backed deployments cover the needed federation paths.
