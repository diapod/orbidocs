# Proposal 067: Shared Offer Catalog Over Agora

Based on:
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/30-stories/story-006-voluntary-swarm-exchange.md`
- `doc/project/30-stories/story-009-arca-dator-sensorium-swarm-workflow.md`
- `doc/project/60-solutions/000-node/000-node.md`

## Status

Draft

## Date

2026-06-08

## Executive Summary

The current implementation already contains most of the substrate needed for a
shared or federated offer catalog:

- `Dator` owns local standing offers and provider-side execution.
- `Dator` can publish signed `offer-snapshot` records to Agora.
- `Arca` can replay Agora offer snapshots into an `observed_offers` SQLite
  projection.
- `Arca` can merge local offers and observed offers for buyer-side workflow
  orchestration.

However, the current responsibility split overloads the phrase
`offer-catalog`. It can mean:

- the local provider-side offer catalog owned by `Dator`;
- the buyer-side observed catalog projection owned by `Arca`;
- a future public/shared catalog that admits offers from many providers.

This proposal freezes the next architectural step:

```text
Agora is the durable federated publication log.
Shared Offer Catalog is the domain projection and query layer over that log.
Dator remains provider authority.
Arca remains buyer orchestration.
```

The goal is not to create a second source of truth. The shared catalog should be
a domain read model: it admits, indexes, and serves signed offer snapshots. The
provider runtime remains authoritative for actual offer validity at order time:
capacity, expiry, queue saturation, provider-side rejection, and execution.

## Context and Problem Statement

The original federation model expected public offer catalogs maintained by the
project or by known communities. Provider nodes would publish offers to such
catalogs, and buyer nodes would query them.

The current implementation solved the hard-MVP need by splitting the catalog
behavior across `Dator` and `Arca`:

- `Dator` maintains the local provider catalog in `local_offers`.
- `Dator` answers `offer-catalog.fetch.request` with local offers.
- `Dator` can push offer relay envelopes.
- `Dator` can publish `offer-snapshot` Agora records.
- `Arca` maintains `observed_offers`.
- `Arca` handles peer fetch responses, pushes, and Agora replay.
- `Arca` exposes a combined service catalog view for its own buyer workflows.

This is pragmatic, but it creates an ontology problem. `Arca` is a buyer-side
workflow orchestrator. Its observed catalog is a local projection for its own
decisions, not a public catalog service. `Dator` is a provider-side authority
over local offers, not a shared catalog for other providers.

If the project wants a public/shared catalog, it should be a separate role with
a narrow domain contract, not an accidental extension of either `Dator` or
`Arca`.

## Goals

- Preserve `Dator` as the source of truth for local provider offers.
- Preserve Agora as a neutral append-only publication substrate.
- Define Shared Offer Catalog as an admission/query projection over signed
  offer snapshots.
- Reuse existing `Arca` observed-catalog mechanics where possible.
- Avoid moving offer catalog state into the daemon trusted core.
- Reduce capability naming ambiguity around `offer-catalog`.
- Keep `Arca` focused on buyer workflow orchestration.

## Non-Goals

- This proposal does not make Agora semantically aware of offers.
- This proposal does not make Shared Offer Catalog authoritative for execution.
- This proposal does not change `service-order.v1`, and changes `service-offer.v1`
  only by introducing one optional lifecycle field (`offer/status`) for withdrawal
  (see Open Questions / Phase 8).
- This proposal does not require rewriting the catalog substrate in Rust.
- This proposal does not remove direct peer fetch from the hard-MVP path.
- This proposal does not define reputation scoring beyond admission metadata.

## Decision

### 1. Agora Is the Publication Log, Not the Offer Catalog

Agora can carry public/federated offer facts as `offer-snapshot` records.
It should not become the domain offer catalog itself.

Agora stores records. It should remain neutral about:

- offer expiry semantics;
- latest sequence selection;
- provider trust policy;
- provider queue state;
- service type indexing;
- tombstone and revocation interpretation;
- task-specific query behavior.

Those are catalog-domain concerns. They belong in an offer-catalog projection.

**Agora is the primary federated path; direct peer fetch/push is a fallback.**
Proposal 035 makes the Agora topic the durable federated substrate, so the shared
catalog's federated input is Agora replay. The bespoke `offer-catalog.fetch`/`push`
peer protocol stays only as an optimization/fallback (low-latency local discovery,
offline resilience) and is on a path to retire — not a second parallel federation
protocol the catalog must treat as co-equal. Fewer protocols, one federated source
of truth for the log.

### 2. Shared Offer Catalog Is a Projection and Admission Layer

Shared Offer Catalog should be a middleware/read-model role that:

- reads `offer-snapshot` records from Agora;
- **requires** a verified outer Agora record authentication — the outer record
  signature, or an explicitly verified Agora record-attestation that provably stands
  in for it. A public/shared catalog **must not** admit an unauthenticated record;
  "where available" is not acceptable on a federated surface (it would let a relay
  inject unattributable offers). The optional case is the *mechanism* (signature vs
  attestation), never the *requirement*;
- verifies the inner provider-authored `service-offer.v1` signature;
- applies admission policy;
- stores admitted and rejected/skipped diagnostics;
- maintains an indexed current-offer projection;
- exposes query APIs for buyers and operators.

This role may be implemented as a Python middleware module. It does not need to
live in the Rust daemon. The daemon should continue to provide host capabilities
and transport primitives only.

### 3. Dator Remains Provider-Side Authority

`Dator` continues to own:

- `local_offers`;
- participant-facing offer publication;
- configured standing offers;
- provider-side offer refresh;
- provider-side execution routing;
- `service-order.dispatch.request` handling;
- optional publication of signed `offer-snapshot` records to Agora.

The local `Dator` catalog remains the provider-side source of truth.

### 4. Arca Becomes a Catalog Consumer

`Arca` should remain the buyer-side workflow orchestrator:

- consume a (read-only) catalog API to discover offers;
- select an offer for a workflow step;
- fund the order;
- dispatch the order and receive the result over **Artifact Delivery** (a separate,
  private transport plane — not the catalog and not a catalog-adjacent peer protocol);
- track execution and fulfillment.

This is the key separation: **offer discovery (catalog, read-only) and order
fulfilment (Artifact Delivery, private transport) are different planes.** The catalog
never carries a `service-order` or a result; once `Arca`/`Dator` move procurement onto
Artifact Delivery, the catalog code left in `Arca` is purely publication-facing
(observed offers, replay, admission, query), which is exactly what this proposal
extracts.

`Arca` may retain a local cache for availability and performance, but it should
not be the public shared catalog role.

### 5. Capability Names Should Distinguish Local and Shared Catalogs

The current `offer-catalog` capability is useful but ambiguous. It currently
means "this node can answer offer-catalog fetch requests", which is often a
local Dator provider catalog.

Future capability naming should distinguish:

- `local-offer-catalog` or `role/local-offer-catalog`: provider-side catalog of
  this node's own offers;
- `shared-offer-catalog` or `role/shared-offer-catalog`: federated/public
  catalog projection over offers from many providers;
- `offer-snapshot-publisher`: optional role/capability for publishing signed
  offer snapshots to Agora.

The exact formal identifiers may be frozen in a follow-up requirements document,
but implementation should avoid further entrenching a single overloaded
`offer-catalog` meaning.

## Proposed Component Split

```text
Dator
  local_offers SQLite
  provider-side offer authority
  signed offer-snapshot publisher
  provider-side service execution

Agora
  append-only public/federated record log
  topic: orbiplex/offer-catalog/v1/...
  record/kind: offer-snapshot

Shared Offer Catalog
  replay from Agora
  admission policy
  current-offer projection
  query and diagnostics API

Arca
  buyer workflow orchestration
  offer selection from catalog API
  service-order construction and AD dispatch/result handling
```

**Topic naming note.** The current code defaults to
`orbiplex/offer-catalog/v1/shared/offers` for Arca replay and Dator publication.
The previous `orbiplex/offer-catalog/v1/local/offers` topic is a compatibility
alias for older harnesses/configs, not the federated default. Keep targeting a
`shared`-segment topic for the federated catalog, so the topic name states its
scope.

## Minimal Implementation Slice

The fastest path is to create a new Python middleware module, tentatively:

```text
middleware-modules/offer-catalog/service.py
```

It should extract or reuse the catalog-domain portions already present in
`Arca`:

- `observed_offers` SQLite schema;
- `SqliteCatalog` usage;
- Agora replay cursor and diagnostics;
- `offer-snapshot` validation;
- `service-offer.v1` inner signature verification;
- sequence and expiry projection;
- `GET /v1/enact/service-catalog`;
- `GET /v1/offer-catalog/replay/status`;
- `POST /v1/offer-catalog/replay/resync`;
- `POST /v1/offer-catalog/replay/reset-cursor`.

`Arca` can then be changed from "owner of observed catalog" to "consumer of the
catalog API". During migration, `Arca` may keep its current local projection as
a fallback or cache.

**One module, two deployments — this is the key reuse.** The extracted catalog
projection is a *single* component that runs in either of two shapes from the same
code:

- **Public/shared catalog node** — runs standalone, replays the Agora offer-catalog
  topic, applies admission, and exposes a public query API; registers the
  `shared-offer-catalog` capability in Seed Directory so buyers can discover it.
- **Buyer-local cache** — the same module embedded by `Arca` for offline/latency
  resilience, with no public surface.

So "public offer catalog" is not new machinery: it is the existing `Arca`
observed-catalog code, extracted once and deployed in the public shape. Whether the
first deployment is local-only or immediately public is a configuration choice, not
an architectural fork.

## Implementation Shape

The hosted offer-catalog module is a **Python process**, consistent with the rest of
the Orbiplex middleware layer. It owns the HTTP surface, deployment shape (public node
‖ buyer-local cache), operator UI, diagnostics — and the offer-catalog mechanics
(state, replay-fed projection, sequence-aware upsert, expiry, admission).

**The mechanics stay in Python; the reuse is Python-internal.** The offer catalog
must *not* reimplement catalog machinery per module — it reuses the shared Python
catalog library `middleware-modules/lib/catalog.py` (`SqliteCatalog`, `CatalogCodec`,
sequence-aware upsert, expiry) that `Arca`, `Dator`, and `recovery-service` already
import. The dedup that applies here is "all Python offer consumers share one Python
catalog lib", which already holds; the extracted module imports the same lib rather
than copying it.

**Decision: do not promote offers onto the Rust `catalog` crate.** It is tempting to
route offer mechanics through the Rust `node/catalog` crate, but the code does not
justify it:

- The Rust crate's **offer layer** (`catalog::offer`, `observed.rs`) currently has
  **no live consumer** outside the crate's own tests. Python (`lib/catalog.py` plus
  `Arca`/`Dator` SQLite) is the de-facto source of truth for offers; the daemon keeps
  only an in-memory mirror (`node/control` DTOs) and delegates offer queries down to
  the Python middleware.
- Moving offers onto the Rust offer layer would mean promoting unproven scaffolding to
  the reference implementation and rewriting working Python — a speculative rewrite,
  not a dedup of an actively-shared implementation. Rejected on YAGNI / "do not rewrite
  working code speculatively" grounds.
- The Rust `catalog` crate's **generic layer** remains legitimately in use by the
  contact catalog (`contact-catalog-core`/`-service`, Proposal 058), a *separate*
  domain. That convergence is real and stays; it does not pull offers along.

**One hardening survives the Python decision:** admission signature verification must
not be hand-rolled. `Arca` currently verifies `service-offer.v1` inner signatures with
a bespoke pure-Python ed25519 implementation (`ed25519_scalar_mult`,
`verify_ed25519_signature`, …). Hand-rolled crypto at a trust boundary violates the
minimal-trusted-core principle regardless of language. Staying in Python, the fix is to
route verification through a **vetted Python ed25519 library** (e.g. PyNaCl /
`cryptography`), shared via `lib/`, not bespoke curve arithmetic. (Whether to instead
expose `node/crypto` to Python is a larger, separate question and is *not* assumed
here.)

## Admission Policy

The shared catalog should admit an offer snapshot only when:

- the record has `record/kind = "offer-snapshot"`;
- the record has `content/schema = "service-offer.v1"`;
- the content is shaped as `service-offer.v1`;
- the inner content signature verifies against `provider/participant-id`;
- `offer/id` and `sequence/no` are valid;
- the provider node and participant pass provider-trust admission (see below);
- the offer is not expired unless the query explicitly asks for historical or
  inactive offers.

Rejected or skipped records should be retained as diagnostics, not silently
discarded.

**Provider trust reuses Seed Directory, not a bespoke trust store.** Admission
verifies the provider against the existing federated trust surface, per Proposal 025
(Seed Directory: passport registration + federated revocation surface). The catalog
does not maintain its own primary list of trusted providers.

What admission actually checks (and what it does **not**):

- **Participant identity** — `provider/participant-id` resolves to a passport
  registered in Seed Directory, and the inner `service-offer.v1` signature verifies
  against that participant's key. This binds the offer to a real, known participant.
- **Offer-publisher capability** — that participant (on `provider/node-id`) holds the
  capability under which offer snapshots are published (the `offer-snapshot-publisher`
  role from Decision 5), and that passport is **not revoked**. This authorizes
  *listing*, i.e. "may this party advertise offers in the shared catalog".
- **Not checked at admission: execution capability.** Whether the provider can
  actually deliver the advertised `service/type` is the provider's own claim. The
  catalog admits the *listing*; authorization to *execute* is verified downstream by
  `Arca`/`Dator` at order/dispatch time against the order contract. Conflating "may
  advertise" with "may execute" would be ontology theft — the catalog is a directory,
  not an execution authority.

`trusted-provider.v1` (Proposal 023) is retained only as a **local operator
override**, with a deliberately narrow, fail-closed semantics:

- it **may locally admit** a provider the operator explicitly trusts even if absent
  from Seed Directory (operator sovereignty — a local allowlist entry), and **may
  raise/annotate** the trust level of an already-known provider;
- it **may not override a Seed Directory revocation** — a revoked provider stays
  rejected regardless of any local allowlist entry (revocation is fail-closed and
  always wins);
- the default for a provider neither in Seed Directory nor in the local allowlist is
  **reject** (retained as diagnostic).

This removes `trusted-provider` as a primary trust source (demoting it to a local
override over a fail-closed federated baseline), binds offer admission
to the same revocation mechanism the rest of the swarm already uses, and keeps local
operator discretion additive-only over a fail-closed federated baseline.

## Query Surface

The minimum query surface should support:

- filter by `service_type`;
- filter by provider participant id;
- filter by provider node id;
- active-only by default;
- limit;
- provenance/trust metadata in responses;
- stable deterministic ordering.

This is intentionally close to existing `Arca` and `Dator` query behavior so
that migration can reuse code and tests.

## Migration Notes

Current implementation evidence:

- `Dator` already owns `local_offers` and `offer-snapshot` publication.
- `Arca` already owns `observed_offers`, Agora replay, admission diagnostics,
  and combined service catalog listing.
- Proposal 023 already describes a bounded catalog role outside the daemon.
- Proposal 035 already allows expressing offer snapshots as Agora records and
  retiring bespoke replication.

Therefore the migration is mostly a responsibility extraction:

1. create `offer-catalog` middleware from the `Arca` observed-catalog subset;
2. keep `Dator` as-is except for capability naming cleanup;
3. teach `Arca` to query `offer-catalog` instead of owning the shared observed
   projection;
4. retain peer fetch/push compatibility during transition;
5. update Seed Directory capability names to distinguish local provider
   catalogs from shared/federated catalogs.

**Storage migration is a move, not a schema change.** Because Python stays the source
of truth (see *Implementation Shape*), the offer catalog keeps the existing Python
`observed_offers` table driven by `lib/catalog.py`'s `SqliteCatalog`. We do **not**
migrate offers onto the Rust generic `catalog_records` storage, and we do **not**
introduce a Rust-backed projection. The migration is: the `observed_offers` schema +
its `SqliteCatalog` usage **move from `Arca` into the new offer-catalog module**
(ownership transfer), and `Arca` switches from owning the table to querying the module
(Phase 5). No table rewrite, no dual-write, no adapter onto a second store — one table,
relocated.

## Open Questions

- ~~Should the first module be deployment-local only or immediately public?~~
  **Resolved:** one module, two deployment shapes (public node ‖ Arca cache);
  deployment is configuration, not an architectural fork (see Minimal
  Implementation Slice).
- ~~Should direct `offer-catalog.push` remain supported?~~ **Resolved:** Agora
  replay is the primary federated path (P035); `fetch`/`push` stays as a
  fallback/optimization on a path to retire (see Decision 1).
- ~~Should provider node trust be catalog-local, Seed Directory, or both?~~
  **Resolved:** Seed Directory (passport + revocation, P025) is the source of
  provider trust; `trusted-provider.v1` (P023) is only a local operator override
  (see Admission Policy).
- ~~Should Arca keep a local cache of shared catalog results?~~ **Resolved:** yes —
  the same catalog module embedded as a buyer-local cache (one module, two
  deployments).
- ~~Should tombstone/revocation be modeled as a separate `offer-tombstone`
  Agora record kind?~~ **Resolved: no separate record-kind — withdrawal is a
  higher-`sequence/no` snapshot of the same `offer/id` carrying an explicit
  withdrawal marker (`offer/status = "withdrawn"`).** The offer catalog is a
  service-mechanical projection, not a social ledger; an offer *disappearing* carries
  no first-class systemic value, so minting a withdrawal record-kind only adds an
  admission path and a schema without buying anything.

  Constraint that rules out the naive form: withdrawal must **not** be expressed as a
  snapshot with `expires-at` in the past. The `service-offer.v1` contract requires
  `expires-at > published-at` (`node/catalog/src/offer/mod.rs` `validate` rejects
  `expires-at <= published-at`), so a past-expiry "withdrawal" is not a representable
  offer — it fails validation and the inner content signature would attest an invalid
  record. Instead the withdrawal snapshot keeps a contract-valid `expires-at` and sets
  the explicit marker; the projection treats a withdrawn snapshot as inactive
  regardless of timestamp. This still reuses existing machinery: monotonic
  `sequence/no` upsert supersedes the prior snapshot (`stale` outcome when incoming ≤
  existing), and `active_only` queries hide it. The active rule becomes
  `active = (status != "withdrawn") AND (expires_at > now)`. (Lighter alternative, if
  the contract owner prefers zero new fields: relax the bound to `expires-at >=
  published-at` and let `expires-at == published-at` mean "withdrawn now" — rejected
  here as more implicit, since it overloads a timestamp coincidence with lifecycle
  meaning instead of stating it in data.)

  **Provider revocation** (provider no longer trusted) is a *different* concern and
  lives in admission via Seed Directory (P025), not in a snapshot — keeping "offer
  withdrawn" (provider-attested, mechanical) cleanly separate from "provider revoked"
  (federated trust, social).

- ~~Should the public shared catalog renew and republish its
  `shared-offer-catalog` capability passport in-process before
  `passport_expires_in_sec`, or is supervisor-driven restart the correct operational
  boundary for this role?~~ **Resolved:** supervisor-driven restart is the default
  operational boundary. The middleware publishes the passport at start; automatic
  in-process renewal remains optional future hardening, not the baseline contract.
- ~~Should public shared catalog deployments require HTTPS/TLS for non-loopback
  `agora.base_url`, and how should local reverse-proxy deployments declare an
  intentional exception?~~ **Resolved:** non-loopback `agora.base_url` must use
  HTTPS/TLS. Loopback HTTP (`127.0.0.1`, `localhost`, `[::1]`) remains allowed for
  local smoke, dev, and reverse-proxy topologies where the public TLS boundary is
  outside the middleware process. The Node shared catalog middleware enforces this
  before public/shared replay.

## Consequences

This proposal reduces ontology drift:

- `Dator` means supply authority.
- `Arca` means demand orchestration.
- `Agora` means durable public/federated append log.
- `Shared Offer Catalog` means offer-domain projection and query.

It also avoids moving domain catalog state into the daemon and avoids making
Agora responsible for offer semantics. The system keeps simple strata: facts in
Agora, domain projection in catalog middleware, procurement decisions in Arca,
execution authority in Dator, and **order/result transport on Artifact Delivery**.

**Relationship to Artifact Delivery (enabler, not precondition).** Moving `Arca`/`Dator`
service-order dispatch and result return onto Artifact Delivery (a private transport
plane; see solution 023 / the `arca-dator-ad` migration) is a *companion* change that
sharpens this proposal's stratification: with fulfilment transport gone to AD, the
catalog code left in `Arca` is purely publication/projection/query, so the extraction
lands clean with no transport responsibility to disentangle. It also makes Agora-replay
the natural catalog path and the bespoke `offer-catalog.fetch`/`push` clearly legacy.
The two efforts are sequencing-independent — neither blocks the other — but the AD
migration reduces the coupling this proposal then removes. This proposal still owns the
real work: extracting observed-offers / replay / admission / query out of `Arca` into a
separate `middleware-modules/offer-catalog`, then switching `Arca` to consume that module
instead of owning the projection.

**Note on a generic catalog substrate (direction, not mandate).** The shape
"replay a topic/source → admission → projection → query" now recurs across Seed
Directory (capabilities, P025), service-schema catalog (P028), workflow-template
catalog (P029), contact catalog (P058), and this offer catalog — and P023 §6
already gestures at a *Generic Catalog Substrate*. There is a real opportunity to
factor a shared projection/admission/query kernel parameterized by record-kind and
admission policy. This proposal deliberately does **not** mint that framework now:
the offer catalog is built as a concrete module, reusing the `Arca` code. A generic
substrate should be extracted only when a second catalog is rebuilt on the same
kernel — let contract pressure mint the abstraction, not anticipation.

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

**Invariants the implementation must hold (check on every step):**

- **`daemon-dep: 0`** — the offer-catalog module is middleware; it must not add a
  dependency on the daemon crate. Verify: no daemon import in
  `middleware-modules/offer-catalog/`.
- **Reuse, not fork** — the public catalog node and Arca's embedded cache run the
  *same* module code. The slimming win is real only if Arca *imports/queries* the
  extracted module rather than keeping a copied projection. Verify: Arca's
  catalog-domain functions are deleted or reduced to thin client calls, not
  duplicated.
- **Admission fail-closed** — unknown/unverifiable provider trust ⇒ reject (retain
  as diagnostic), never admit. Verify: admission default branch rejects.
- **Agora-primary** — replay from the Agora offer-catalog topic is the federated
  source of record; `fetch`/`push` is fallback only (Decision 1).
- **Plane separation** — catalog APIs carry offer discovery/projection data only.
  They must not carry `service-order` artifacts, dispatch requests, or execution
  results. Remote fulfilment stays on Artifact Delivery.
- **Reuse the shared Python catalog lib, do not reimplement** — the module drives
  `middleware-modules/lib/catalog.py` (`SqliteCatalog`, `CatalogCodec`, sequence
  upsert, expiry), the same lib `Arca`/`Dator`/`recovery-service` already import. Do
  **not** copy catalog mechanics per module; do **not** promote the idle Rust
  `catalog::offer` layer (see *Implementation Shape*).
- **No hand-rolled crypto at the admission boundary** — replace `Arca`'s bespoke
  pure-Python ed25519 with a vetted Python ed25519 library shared via `lib/`.

### Phase 0 — Preconditions (verify substrate)

- [x] Rust `catalog` crate separates generic mechanics from offer semantics.
  Evidence: `node/catalog/src/lib.rs` doc + `observed.rs`, `offer.rs`, `agora.rs`,
  `trusted.rs`.
- [x] Agora offer topic + `offer-snapshot` record kind defined. Evidence:
  `arca/service.py` / `dator/service.py` `OFFER_AGORA_TOPIC`
  (`orbiplex/offer-catalog/v1/shared/offers` by default),
  `OFFER_AGORA_RECORD_KIND`.
- [x] Dator publishes signed `offer-snapshot` to Agora and owns `local_offers`.
  Evidence: `dator/service.py`.
- [x] Arca consumes the shared offer-catalog runtime for observed projection,
  Agora replay, and admission diagnostics.
  Evidence: `node/middleware-modules/lib/offer_catalog.py` and
  `node/middleware-modules/arca/service.py` `OFFER_CATALOG`.

### Phase 1 — Extract the offer-catalog module

- [x] Create `middleware-modules/offer-catalog/service.py` as a Python module that
  **reuses** the shared `lib/catalog.py` (`SqliteCatalog`/`CatalogCodec`/sequence
  upsert/expiry) — HTTP surface, deployment shape, diagnostics; **no** per-module
  reimplementation of catalog mechanics.
- [x] Move the catalog-domain subset out of `arca/service.py` into the new module:
  `observed_offers` schema + `SqliteCatalog` usage; Agora replay cursor + diagnostics;
  `offer-snapshot` validation; sequence + expiry projection. `Arca` then imports/queries
  it (Phase 5).
- [x] Replace hand-rolled ed25519 in `arca/service.py` with a **vetted Python ed25519
  library** (PyNaCl / `cryptography`), placed in `lib/` and shared by both `Arca` and
  the offer-catalog module. Do **not** keep bespoke curve arithmetic.
- [x] Keep the operational shared offer-catalog runtime in the shared Python module;
  the Rust `catalog` crate is not the deployed shared catalog. It is only contract-synced
  for `service-offer.v1` lifecycle semantics (`offer/status`) so Rust fixtures and
  control-plane schemas do not drift.

### Phase 2 — Admission via Seed Directory

- [x] Admission verifies participant identity + `offer-snapshot-publisher` capability
  passport + non-revocation against Seed Directory
  (P025); fail-closed on unknown.
- [x] Provider admission is not bypassed by `trusted_provider_node_ids`; public/shared
  replay still requires Seed Directory authorization unless the whole deployment is
  explicitly configured as a local harness with
  `require_seed_directory_admission = false`.
- [x] Rejected/skipped records retained as diagnostics.

### Phase 3 — Query surface parity

- [x] Implement query API: filter by `service_type` / provider participant /
  provider node; active-only default; limit; provenance/trust metadata;
  deterministic ordering.
- [x] Endpoints: `GET /v1/enact/service-catalog`,
  `GET /v1/offer-catalog/replay/status`, `POST .../replay/resync`,
  `POST .../replay/reset-cursor`.
- [x] Reuse Arca/Dator query tests to prove behavioral parity.

### Phase 4 — Two deployments from one module

- [x] Standalone **public/shared catalog node** shape: replays Agora, applies
  admission, exposes public query API, refreshes a `shared-offer-catalog` passport
  through the host, and exposes only passport metadata in `/healthz`/`/readyz`.
- [x] **Buyer-local cache** shape: same module embedded by Arca, no public surface.
- [x] Deployment shape is a config switch, not a code fork.

### Phase 5 — Arca slimming (the reuse payoff)  ⟵ *answers "can Arca be slimmed?"*

- [x] Arca queries the offer-catalog module API (or embeds it as a cache) instead of
  owning the shared observed projection.
- [x] Delete from `arca/service.py` the now-shared catalog-domain functions
  (observed upsert, replay cursor/diagnostics, snapshot validation, ed25519 verify,
  projection); keep only a thin catalog client + buyer logic.
- [x] `merge_catalog_snapshots` thins to "merge buyer-local Dator offers (if any)
  with catalog-API results"; the observed half comes from the module.
- [x] Arca's remaining responsibility is the buyer brain only: workflow
  orchestration, offer selection, `service-order` construction, AD dispatch/result
  wait, settlement.
- [x] Confirm net reduction: Arca no longer *declares* the ~catalog-ish half of its
  functions; it *imports* them. (Baseline: ~6061 LOC, roughly half catalog-domain.)

### Phase 6 — Capability naming

- [x] Split `offer-catalog` into `local-offer-catalog`, `shared-offer-catalog`,
  `offer-snapshot-publisher`.
- [x] Update Seed Directory registration so buyers discover `shared-offer-catalog`
  nodes; freeze identifiers in a follow-up requirements doc.

### Phase 7 — Retire bespoke peer protocol

- [x] Keep `offer-catalog.fetch`/`push` working during transition (compat).
- [x] Mark them deprecated; document the retirement path to Agora-only.

### Phase 8 — Withdrawal semantics (resolved: explicit marker, no tombstone record-kind)

Decision: **withdrawal = higher-`sequence/no` snapshot carrying an explicit
`offer/status = "withdrawn"` marker, with a contract-valid `expires-at`.** No
`offer-tombstone` record kind, and **not** a past-`expires-at` hack (that violates the
`expires-at > published-at` contract in `offer/mod.rs`). Provider *revocation* is
handled separately at admission via Seed Directory (P025), not as an offer record.

- [x] Extend the `service-offer.v1` contract with an optional withdrawal marker
  (`offer/status`, default `active`); update `ServiceOfferRecord` (and its Python
  mirror) and keep the inner content signature covering it.
- [x] Confirm `Dator` can publish a superseding withdrawal snapshot (same `offer/id`,
  higher `sequence/no`, `status = "withdrawn"`, valid `expires-at`) on retirement.
- [x] Update the projection active rule to
  `active = (status != "withdrawn") AND (expires_at > now)`; confirm monotonic
  supersession (`stale` outcome guards) and `active_only` filtering hide it.
- [x] Confirm provider revocation removes offers via admission (Seed Directory
  non-revocation check, Phase 2), independent of snapshot status/expiry.
