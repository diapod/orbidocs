# Proposal 072: Capability Registry — Enforced Core, Deferred Authorization Policy

Based on:

- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/007-capability-advertisement/007-capability-advertisement.md`
- `node/DEV-GUIDELINES.md` (Code Review #2 "Missing Authority Means Denial", #5
  "Identifiers Must Be Explicit And Canonical", "Implementation Planning and Capability
  Mapping")

## Status

`draft`

## Date

`2026-06-23`

## Executive Summary

The repository has a human-facing `CAPABILITY-REGISTRY` that maps federated capability
IDs to meaning, role, and wire name. But it has two gaps that CR-87/CR-88 surfaced as a
P0:

1. **It is documentation, not an enforced source of truth.** Nothing fails closed when
   the runtime advertises, requests, or dispatches a capability that the registry does
   not contain.
2. **It explicitly excludes host-local capabilities** (e.g. `recovery.sign`,
   `catalog.local.query`, and the whole `/v1/host/capabilities/*` surface) — which are
   exactly the capabilities the daemon dispatches. CR-88 noted a GET enumeration
   endpoint was added, but **enumeration is not enforcement**.

With `room.*` (P070), `sensorium.workbench.*` (P071), `corpus.*` (P069), and a host
`interaction-broker.*` (P071) about to land, the risk of capability-ID collision,
docs↔runtime drift, and **ambient (unregistered) authority** compounds.

This proposal deliberately splits the concern, because the framing "Capability Registry
is a separate product decision" is only half true:

- **Enforced core (now, not a product decision).** One canonical, machine-checkable
  registry covering **both** federated capability IDs **and** host-local capabilities;
  the daemon derives its dispatchable/advertisable set from it and **fails closed on any
  unregistered capability**. This is a hygiene requirement implied by DEV-GUIDELINES
  ("Missing Authority Means Denial", "Identifiers Must Be Explicit And Canonical"), not
  a product call. It is what actually closes CR-87/88 P0-1; the GET endpoint stays as a
  read surface only.
- **Deferred product/governance decision (a real fork).** Authorization-policy-as-data
  per capability (required grants, COI rules, autonomy levels) and federation-extension
  governance (who may register federation-scoped capabilities, namespace allocation,
  revocation). These get their own track and SHOULD become a separate proposal.

## Context and Problem Statement

- CR-87 raised "full capability registration" as **P0**; CR-88 downgraded it to
  "partially open" because a GET `/v1/host/capabilities/*` endpoint was added. That
  endpoint answers *what capabilities exist* (observability); it does not gate
  *whether an unregistered capability may be dispatched* (authority). The original P0
  concern — canonical identity + fail-closed authority — is therefore **not closed**.
- `CAPABILITY-REGISTRY` has historically been kept in sync with the node and passport
  contracts by hand, and historically excluded host-local capabilities. Its current
  P072 note acknowledges that this boundary is obsolete, but the enforced source of
  truth still does not exist.
- DEV-GUIDELINES requires reflecting capability ownership before changing runtime
  surfaces, and treats unregistered authority as denial. Several new components are
  about to add capabilities; without enforcement, each is an opportunity for drift.

## Goals

- One canonical registry as the source of truth for every capability the node may
  advertise, request, or dispatch — **federated and host-local**.
- Daemon **fail-closed** on dispatch/advertisement/passport of an unregistered
  capability.
- The human `CAPABILITY-REGISTRY`, the runtime allow-set, and
  `capability-passport.v1` / `capability-advertisement.v1` fixtures are all checked
  against the same registry; CI catches drift.
- A concrete registration prerequisite for P069/P070/P071 capabilities.

## Non-Goals

- Not (yet) authorization-policy-as-data per capability — deferred (see Resolved Decisions).
- Not federation-extension governance — deferred.
- Not a redesign of `capability-passport.v1` / `capability-advertisement.v1`; this
  registers their IDs canonically and gates them, nothing more.
- Not a replacement for host policy: the registry adds canonical identity and
  fail-closed registration; imperative authorization gates remain until §2 lands.

## Decision

### 1. Enforced canonical registry (the core — now)

- **Identifier grammar (canonical).** A `capability/id` is one of four registered shapes,
  validated by the registry-admission gate before anything else:
  - **bare dotted** — an application/host capability name in lowercase dotted segments,
    e.g. `room.join`, `interaction-broker.wait`, `corpus.provider`
    (`` ^[a-z][a-z0-9-]*(\.[a-z0-9-]+)*$ ``);
  - **protocol-native slash id** — a baseline protocol surface in the reserved `core/`
    namespace, e.g. `core/messaging`, `core/discovery`, `core/keepalive`
    (`` ^core/[a-z][a-z0-9-]*$ ``); these are mandatory infrastructure ids that already
    exist in the registry and node constants, so the grammar MUST accept them;
  - **sovereign** — a name anchored to an identity outside the global bare namespace,
    `name@participant:did:key:z…` (or `@org:did:key:z…`);
  - **operator/custom** — a sovereign form prefixed with `~`, e.g.
    `~article-review@participant:did:key:z…`, signalling a self-issued, non-endorsed
    capability.

  The bare shape covers registered formal service and application capabilities; the
  `core/*` shape covers protocol-native baseline capabilities; and the sovereign/custom
  shapes follow the existing sovereign-id parser and the human registry's public passport
  class distinction. P072 **pins them as the validated id grammar** so "canonical
  identity" is enforceable, not aspirational. An id matching none of the four shapes is
  rejected at registration.
- **Source of truth (decided, was Open Q1):** a single **repo-checked-in**,
  machine-readable `capability-registry.v1` is the source of truth. The human
  `CAPABILITY-REGISTRY` document is a **generated/validated projection** of it — never a
  parallel hand-synced surface. Leaving the source direction open would defeat P072's
  purpose (closing drift), so it is fixed here.
- **One registry with a `surfaces` set (decided, was Open Q2):** one registry covers
  **both** federated and host-local capabilities, distinguished by a `surfaces` set. The
  host-local omission in today's registry is precisely the gap this closes.
- **Entry shape — explicit eligibility flags, not one coarse class.** One `capability/id`
  may be several things at once (a host dispatch route, a passport-advertised federated
  capability, a signing domain), so a single `auth-class` is too poor. Each entry carries
  `capability/id`, `owner` (role / runtime class), `surfaces` (a non-empty subset of
  `{ federated, host-local }`), `wire/name`, `status` (`active` | `deprecated` |
  `reserved`), and explicit boolean eligibility flags: `dispatchable`, `advertisable`,
  `passport/eligible`, `signing-domain`, `host-route`, `federated-discovery`. The flags
  say which uses an id is registered for; an unflagged use is denied.
- **`surfaces` is a declared field validated as a derived set.** A capability may
  legitimately be both federated and host-local (a federated capability the host also
  dispatches locally), so the entry carries `surfaces` as a set (a non-empty subset of
  `{ federated, host-local }`). The registry validator recomputes the expected set from
  eligibility flags: `advertisable | passport/eligible | federated-discovery`
  contributes `federated`; `host-route | dispatchable` contributes `host-local`. An
  entry whose declared `surfaces` contradicts the recomputed set is rejected at
  registration, so `surfaces` remains a checked summary, not a second authority that can
  drift.
- **`wire/name` is explicit, unique, and validated — not a global transformation.**
  `wire/name` is the on-the-wire canonical form and is a **semantic** namespace mapping,
  not a mechanical transform of `capability/id`: the prefix is the capability's wire
  namespace (`app/`, `host/`, `role/`, `plugin/`, `core/`), e.g. `corpus.provider` →
  `app/corpus.provider`, `room.join` → `app/room.join`, `interaction-broker.wait` →
  `host/interaction-broker.wait`, `core/messaging` → `core/messaging`. Each entry states
  its `wire/name` explicitly; the registry validates that it is unique and uses a known
  namespace prefix. A default derivation MAY be a helper for new entries, but it is not a
  global contract and never rewrites existing wire names.
- **`status` semantics at the gate.** `active` is admitted; `reserved` is
  registered-but-denied — a name reservation where the id is known but dispatch/advertise
  is refused, so a future id cannot be squatted by an unregistered actor; `deprecated` is
  admitted with an operator-visible warning until a declared removal deadline, then
  denied.
- **Three gate layers, kept distinct.** Authority is checked in three independent layers,
  not collapsed into one: **schema-gate** validates artifact *shape*; a
  **registry-admission gate** validates that the `capability/id` is *registered and
  eligible for the surface/use in play*; **runtime policy** decides *use* (grants /
  authorization). Schema validity never implies registration, and registration never
  implies authorization.
- **Fail-closed registration — registry is the runtime authority.** At runtime the
  registry is the allow-set: the registry-admission gate admits only a registered,
  eligible `capability/id`. An **unregistered or ineligible capability is denied**:
  dispatch refused, advertisement rejected, and a `capability-passport.v1` /
  `capability-advertisement.v1` carrying an unregistered or ineligible `capability_id`
  rejected — independently of shape validity.
- **Load-time fail-closed.** A missing, malformed, or unparseable `capability-registry.v1`
  is a **readiness failure with an operator diagnostic**, never a silent empty allow-set
  and never a silent open one. The daemon does not start serving capability surfaces
  until a valid registry is loaded.
- **Two-layer completeness: build-time static + runtime dynamic.** Capability sources are
  partly static (code constants, dispatch/advertise call sites) and partly **dynamic**
  (middleware module reports, JSON-e bindings, provider sources resolved at runtime), so
  no single static scan is sufficient. A **build-time checker** validates the static
  declarations against the registry (every static site has a registered, eligible entry;
  docs projection and passport/advertisement fixtures match). **Runtime readiness /
  admission** validates each dynamic provider report or config entry against the registry
  **before** it is admitted to routing — an unregistered or ineligible dynamic capability
  is rejected, not routed. Neither layer silently swallows an unknown capability; together
  they keep the registry the effective allow-set without pretending every capability is
  statically enumerable.
- New capabilities MUST be registered **before** runtime work: `room.open` / `room.join`
  / `room.membership-query` (P070), `sensorium.workbench.*` (P071), `corpus.*` (P069),
  and the host `interaction-broker.wait` / `.watch` / `.probe` (P071). This makes the
  P069/P070/P071 "register capability IDs" prerequisite concrete. Where a capability
  already shipped code-first (the P070 `room.*` runtime exists today), its entry is a
  **retroactive registration + conformance** item, not a precondition blocking
  already-built code; the enumeration-by-construction check above catches it.

### 2. Deferred product / governance decision (the real fork)

- **Authorization-policy-as-data per capability** — required grants, COI-by-default
  rules, and autonomy levels (the table in P071 §9 is the seed) expressed as registry
  data rather than scattered imperative checks. Decision: this gets its own proposal, so
  P072 remains the small registry identity/admission core rather than becoming the policy
  engine.
- **Federation-extension governance** — who may register federation-scoped
  capabilities, how namespaces are allocated, and how a federation capability is revoked.
  Decision: this also gets its own proposal, because it is governance over public
  namespace authority, not merely registry storage.
- Until both land, host policy keeps gating authorization imperatively; the enforced
  core (§1) only adds canonical identity and fail-closed registration, which is safe to
  ship independently.

## Data Contracts

| Schema | Status | Purpose |
|---|---|---|
| `capability-registry.v1` | new | Canonical entries: `capability/id`, `owner`, `surfaces` (set), `wire/name`, `status`, and eligibility flags (`dispatchable`, `advertisable`, `passport/eligible`, `signing-domain`, `host-route`, `federated-discovery`). |
| `CAPABILITY-REGISTRY` (doc) | becomes generated/validated view | Human-facing projection of the registry. |

Reuses (gated against the registry, not changed): `capability-passport.v1`,
`capability-advertisement.v1`.

## Relationship to Existing Mechanisms

- **CR-87/88 P0-1**: this proposal is what closes it. The GET `/v1/host/capabilities/*`
  endpoint remains a read surface, not the source of truth.
- **P069 / P070 / P071**: register their new capability IDs here; the "register
  capability IDs + ledger rows" prerequisite from their reviews resolves to §1.
- **DEV-GUIDELINES**: §1 directly implements "Missing Authority Means Denial" (#2) and
  "Identifiers Must Be Explicit And Canonical" (#5), and satisfies "Implementation
  Planning and Capability Mapping".
- **Capability passports/advertisement (006/007/024)**: unchanged contracts, now gated
  by registered identity.

## Resolved Decisions

The former Q1 (source direction) and Q2 (one registry vs two) are **decided in §1** —
single repo-checked-in source with a generated docs projection, one registry with a
`surfaces` set — because leaving them open would undercut P072's purpose.

The former Q3 (grandfathering migration), Q4 (authorization-policy-as-data), and Q5
(federation-extension governance) are also decided:

1. **Grandfathering migration.** Seed every currently known capability as `active` in
   the first registry and fail closed immediately for any new unregistered capability.
   Backward compatibility is not required at this stage, and preserving the warning-only
   gap would undercut the registry's purpose.
2. **Authorization-policy-as-data.** Create a separate proposal when this becomes the
   next implementation slice.
3. **Federation-extension governance.** Create a separate governance proposal for
   namespace allocation, registration authority, and revocation.

## Implementation Recommendations

The registry file carries the standard `schema/v` discriminator and an `entries` array;
each entry's `surfaces` set is computed from the flags and `wire/name` is its explicit
semantic wire form. One host-local entry:

```json
{
  "capability/id": "interaction-broker.wait",
  "owner": "daemon interaction broker",
  "surfaces": ["host-local"],
  "wire/name": "host/interaction-broker.wait",
  "status": "active",
  "flags": {
    "dispatchable": true, "advertisable": false, "passport/eligible": false,
    "signing-domain": false, "host-route": true, "federated-discovery": false
  }
}
```

A federated entry (`corpus.provider`) instead sets `advertisable`, `passport/eligible`,
and `federated-discovery` true (⇒ `surfaces = { federated }`), with
`wire/name = app/corpus.provider`. A `reserved` entry carries its id and flags but
`status = "reserved"`, so the gate holds the name while refusing use. The registry file
is repo-checked-in; git history is its change authority, and the load-time check verifies
structural integrity before the daemon serves any capability surface.

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Current implementation coverage audit

Audited on `2026-06-24`.

What exists today:

- `node:capability/src/lib.rs` has a static `CAPABILITY_ADVERTISEMENT_MAP` and
  formal constants for the P069/P070/P071 capability IDs.
- `orbidocs:doc/project/60-solutions/CAPABILITY-REGISTRY.en.md` and `.pl.md`
  already include host-local rows such as `sensorium.workbench.*` and
  `interaction-broker.*`.
- `orbidocs:scripts/check-capability-registry.py` plus `make
  check-capability-registry` validate the human registry tables against the node
  runtime capability map and core protocol capability constants.

What does **not** exist yet:

- no checked-in `capability-registry.v1` machine-readable source of truth;
- no `surfaces` set or eligibility flags consumed by runtime code;
- no daemon admission gate that derives dispatchable / advertisable /
  passport-eligible sets from that registry;
- no registry check for `capability-passport.v1` or
  `capability-advertisement.v1` fixtures beyond the current docs↔node map
  drift check;
- no fail-closed rejection for every unregistered formal capability ID. Current
  advertisement mapping still supports generic and sovereign IDs, and host-local
  routing is provider-source based rather than registry-derived.

### Phase 0 — Enumerate and seed

- [~] Enumerate every capability the node currently advertises, requests, or dispatches
  (federated **and** host-local, including `/v1/host/capabilities/*`). Evidence:
  interim enumeration exists in `CAPABILITY_ADVERTISEMENT_MAP`,
  `CAPABILITY-REGISTRY.*.md`, and host capability provider sources; it is not yet
  exhaustive or machine-authoritative for all `/v1/host/capabilities/*` routes.
- [ ] Seed `capability-registry.v1`; grandfather every currently known capability as
  `active`, then fail closed immediately for new unregistered capabilities. No
  `capability-registry.v1` source exists yet.

### Phase 1 — Enforce (fail-closed)

- [ ] Daemon derives its dispatchable and advertisable sets from the registry. Current
  daemon routing derives host-local providers from runtime sources, not from a
  canonical registry.
- [ ] Unregistered capability → denied at dispatch, advertisement, and passport gate.
  Current code validates shapes and some identity bindings, but it does not apply
  a registry-admission gate for all formal capability IDs.
- [ ] Load-time readiness fail-closed: a missing/malformed `capability-registry.v1` fails
  daemon readiness with a diagnostic, never a silent empty or open allow-set.
- [ ] Two-layer completeness: a build-time checker validates static declarations against
  the registry, and runtime readiness/admission validates dynamic provider reports,
  JSON-e bindings, and config against the registry before routing them, so neither a
  static nor a dynamic capability is admitted unregistered.

### Phase 2 — CI drift gate

- [~] Validate the docs projection, node allow-set, and passport/advertisement fixtures
  against the registry; drift fails the build. Evidence: `make
  check-capability-registry` validates `CAPABILITY-REGISTRY.en.md` and `.pl.md`
  against `node:capability/src/lib.rs` plus core protocol constants. Missing:
  validation against `capability-registry.v1`, eligibility flags, and
  passport/advertisement fixtures.

### Phase 3 — Register new capabilities (P069/P070/P071 prerequisite)

- [x] `room.open` / `room.join` / `room.membership-query` (P070). Registered in
  `node:capability/src/lib.rs` and `CAPABILITY-REGISTRY.*.md`; enforcement still
  waits for Phase 1.
- [x] `sensorium.workbench.*` (P071). Registered in `node:capability/src/lib.rs`
  and `CAPABILITY-REGISTRY.*.md`; enforcement still waits for Phase 1.
- [x] `corpus.*` (P069). `corpus.provider` is registered in
  `node:capability/src/lib.rs` and `CAPABILITY-REGISTRY.*.md`; enforcement still
  waits for Phase 1.
- [x] host `interaction-broker.wait` / `.watch` / `.probe` (P071). Registered in
  `node:capability/src/lib.rs` and `CAPABILITY-REGISTRY.*.md`; enforcement still
  waits for Phase 1.

### Phase 4 — Authorization-policy-as-data `[!] separate proposal`

- [!] Express required grants / COI / autonomy levels as registry data in a separate
  proposal (seed: P071 §9).

### Phase 5 — Federation-extension governance `[!] separate proposal`

- [!] Federation namespace allocation, registration authority, and revocation in a
  separate governance proposal.
