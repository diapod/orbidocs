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

- **Source of truth (decided, was Open Q1):** a single **repo-checked-in**,
  machine-readable `capability-registry.v1` is the source of truth. The human
  `CAPABILITY-REGISTRY` document is a **generated/validated projection** of it — never a
  parallel hand-synced surface. Leaving the source direction open would defeat P072's
  purpose (closing drift), so it is fixed here.
- **One registry with a `surface` discriminator (decided, was Open Q2):** one registry
  covers **both** federated and host-local capabilities, distinguished by `surface`. The
  host-local omission in today's registry is precisely the gap this closes.
- **Entry shape — explicit eligibility flags, not one coarse class.** One `capability/id`
  may be several things at once (a host dispatch route, a passport-advertised federated
  capability, a signing domain), so a single `auth-class` is too poor. Each entry carries
  `capability/id`, `owner` (role / runtime class), `surface`
  (`federated` | `host-local`), `wire/name`, `status` (`active` | `deprecated` |
  `reserved`), and explicit boolean eligibility flags: `dispatchable`, `advertisable`,
  `passport/eligible`, `signing-domain`, `host-route`, `federated-discovery`. The flags
  say which uses an id is registered for; an unflagged use is denied.
- **Three gate layers, kept distinct.** Authority is checked in three independent layers,
  not collapsed into one: **schema-gate** validates artifact *shape*; a
  **registry-admission gate** validates that the `capability/id` is *registered and
  eligible for the surface/use in play*; **runtime policy** decides *use* (grants /
  authorization). Schema validity never implies registration, and registration never
  implies authorization.
- **Fail-closed registration.** The daemon **derives** its dispatchable and
  advertisable / passport-eligible sets from the registry. An **unregistered or
  ineligible capability is denied** at the registry-admission gate: dispatch refused,
  advertisement rejected, and a `capability-passport.v1` / `capability-advertisement.v1`
  carrying an unregistered or ineligible `capability_id` rejected — independently of
  shape validity.
- **CI drift gate.** The docs projection, the node allow-set, and passport / advertisement
  fixtures are validated against the registry; any drift fails the build.
- New capabilities MUST be registered **before** runtime work: `room.open` / `room.join`
  / `room.membership-query` (P070), `sensorium.workbench.*` (P071), `corpus.*` (P069),
  and the host `interaction-broker.wait` / `.watch` / `.probe` (P071). This makes the
  P069/P070/P071 "register capability IDs" prerequisite concrete.

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
| `capability-registry.v1` | new | Canonical entries: `capability/id`, `owner`, `surface`, `wire/name`, `status`, and eligibility flags (`dispatchable`, `advertisable`, `passport/eligible`, `signing-domain`, `host-route`, `federated-discovery`). |
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
`surface` discriminator — because leaving them open would undercut P072's purpose.

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

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[!]` blocked/needs decision.

### Phase 0 — Enumerate and seed

- [ ] Enumerate every capability the node currently advertises, requests, or dispatches
  (federated **and** host-local, including `/v1/host/capabilities/*`).
- [ ] Seed `capability-registry.v1`; grandfather every currently known capability as
  `active`, then fail closed immediately for new unregistered capabilities.

### Phase 1 — Enforce (fail-closed)

- [ ] Daemon derives its dispatchable and advertisable sets from the registry.
- [ ] Unregistered capability → denied at dispatch, advertisement, and passport gate.

### Phase 2 — CI drift gate

- [ ] Validate the docs projection, node allow-set, and passport/advertisement fixtures
  against the registry; drift fails the build.

### Phase 3 — Register new capabilities (P069/P070/P071 prerequisite)

- [ ] `room.open` / `room.join` / `room.membership-query` (P070).
- [ ] `sensorium.workbench.*` (P071).
- [ ] `corpus.*` (P069).
- [ ] host `interaction-broker.wait` / `.watch` / `.probe` (P071).

### Phase 4 — Authorization-policy-as-data `[!] separate proposal`

- [!] Express required grants / COI / autonomy levels as registry data in a separate
  proposal (seed: P071 §9).

### Phase 5 — Federation-extension governance `[!] separate proposal`

- [!] Federation namespace allocation, registration authority, and revocation in a
  separate governance proposal.
