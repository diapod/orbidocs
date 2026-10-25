# Proposal 072: Capability Registry — Enforced Core and Policy Sidecar

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

Related configuration work (proposed):

[Proposal 091: File-backed Configuration and Explainable Composition](091-file-backed-configuration-and-explainable-composition.md).
P091 proposes registering all five configuration operations under P072: only
describe/explain are module-dispatchable; plan/commit/apply are non-dispatchable
host routes with independent operator authorization. The registry remains
descriptive/enforcing metadata, not a source of grants. P091-002/005a own
registration and security proof; the entries are not claimed to exist yet.

## Local responsibility registration: 2026-10-10

P051-002 and P018-12 register six **host-local** operations in the canonical
Node registry. Their identity and dispatch admission are separate from actor
mandates, case ownership and effect authority. They are neither federation
advertisements nor capability passport grants.

| Operation | Owner | Permission boundary |
| --- | --- | --- |
| `responsibility.case.inspect` | responsibility-service | Signed own-case inspection/listing or current inspection mandate; cannot execute procedure. |
| `responsibility.procedure.execute` | responsibility-service | Exact signed command, actor/host/object/policy/case revision and required current procedural mandate; subject acknowledgment/appeal remain protected. |
| `responsibility.authorize` | daemon | Authenticated responsibility module host call; independently verifies signature and current policy/mandate admission. Registration does not grant authority. |
| `responsibility.case.commit` | daemon | Verified command and accepted prior case revision; host independently replays the pure transition before retaining a mirror. |
| `responsibility.sources.inspect` | daemon | Verified responsibility module context; returns bounded source-set revision/digest for effect CAS. |
| `responsibility.effect.apply` | daemon | Exact source/effect/decision bindings, current actor authority, validity, source-set CAS and durable retraction fence. |

S039 separately admits the registered `responsibility.case.respond` action;
notification answers call the same service, recheck the exact case/action/recipient
and preserve `marks/handled=false`. UI signing uses verified caller binding and
the narrow `orbiplex.responsibility.command.v1` domain, never a form-selected
identity. Local admission, sealed evidence and targeted operator-source control
routes require their existing control transport authorization plus the specified
actor proof or operator boundary. No implicit module grant is introduced.

Contract and evidence:
`node:docs/development/LOCAL-ACCOUNTABILITY-CONTRACT.md` and
`node:docs/evidence/local-accountability/2026-10-10-qualified-local/`.

### Planned maintenance permissions (2026-10-19)

M0 (2026-10-20) freezes the following draft names and one separate
`grant/responsibility.maintenance.<suffix>` per operation, while keeping both
the live registry and authorization policy unchanged. Current grant production
and admission belong to the authenticated host operator owner and remain M4
work; selector fields in a request are not proof. There is no detached signed
command family at M0. See [the S040 contract](../60-solutions/040-capability-limited-restrictions/040-safe-maintenance-contracts.md).

The safe-maintenance/shadow-V3 plan reserves separate host-local
`responsibility.maintenance.inspect`, `.prepare`, `.abandon`, `.verify`,
`.reconcile` and `.compact` permissions. These are **unregistered design names**,
not new callable capabilities. M4 registry/policy/route bindings and current
operator authorization must pass their own negative tests before exposure.
Inspection, case mandates, module registration and passports confer no mutation
authority. Exact approved plans, host/incarnation, revocation and idempotency are
independent gates; maintenance can neither alter participant effects nor open D7.
S037 owns eligibility metadata; the host operator boundary owns approval.
See `node:docs/development/RESPONSIBILITY-SAFE-MAINTENANCE-SHADOW-V3-PLAN-2026-10-19.md`.

## Status

`promoted`

Promoted to: `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`

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
- **Policy/governance split.** Authorization-policy-as-data per capability is now
  represented as a checked sidecar (`capability-authorization-policy.v1`) for the P071
  Workbench/Interaction Broker and P082 Sensorium Interface seed capabilities. Federation-extension governance
  (who may register federation-scoped capabilities, namespace allocation, revocation)
  remains a separate governance track.

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

- Not federation-extension governance — deferred.
- Not a redesign of `capability-passport.v1` / `capability-advertisement.v1`; this
  registers their IDs canonically and gates them, nothing more.
- Not a replacement for host policy: the registry adds canonical identity and
  fail-closed registration; the policy sidecar adds checked required-grant/posture
  metadata, while runtime enforcement still lives at host policy boundaries.

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
  `app/corpus-provider`, `room.join` → `app/room.join`, `interaction-broker.wait` →
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

### 2. Policy sidecar and deferred governance

- **Authorization-policy-as-data per capability** — required grants, COI-by-default
  rules, and autonomy levels (the table in P071 §9 is the seed) expressed as checked
  sidecar data rather than scattered prose. Decision: keep this as
  `capability-authorization-policy.v1`, referenced by the registry/tooling but not
  embedded in `capability-registry.v1`, so P072 keeps the registry identity/admission
  layer separate from runtime policy enforcement.
- **Federation-extension governance** — who may register federation-scoped
  capabilities, how namespaces are allocated, and how a federation capability is revoked.
  Decision: this also gets its own proposal, because it is governance over public
  namespace authority, not merely registry storage.
- Host policy keeps gating authorization at runtime; the sidecar supplies checked
  required-grant/posture/approval/autonomy/COI data for consumers and drift checks.
  It is not the runtime enforcement engine: the current implemented sidecar covers
  the P071 Workbench/Interaction Broker and P082 Sensorium Interface seed sets, and broader per-capability
  enforcement remains owned by the consuming host-policy boundaries.

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
- **Operator-Sovereign Extensibility (P085)**: a derived capability set is a
  signed local intersection of registered base capabilities and additional
  restrictions, not a new primitive registry authority. P085 owns the derived
  contract and operator overlay; P072 remains authoritative for every base id and
  use-specific eligibility flag.

### Assessment Exposure Is Not Capability Admission

The planned [P026 host projection](026-resource-opinions-and-discussion-surfaces.md#viewer-bound-api-projection)
reuses caller-scoped identity/authority resolution rather than adding a parallel
capability registry. `admit` answers whether a read is authorized; `expose`
determines its current viewer-safe representation. Catalog availability or a read
grant cannot reveal hidden assessments or authorize an explicit skip.

P026-005/007 audit existing read, detail, export and observation capabilities.
Reuse them where their contracts can carry the projection; register and schema-gate
only genuinely new operations. An Agent acting for a viewer cannot select a raw
relay/operator path as an implicit fallback. Privileged replication/inspection
remains explicitly outside `local-display-only`, not an invisible second read
path. This is a planned consumer binding, not a new implemented registry entry.

### Planned Local Device Discovery Admission

[P045 local device discovery continuation](045-sensorium-local-enaction-stratum.md#local-device-discovery-continuation)
owns `P045-DISC-001`–`007`. Its planned `device.discover.ble`,
`device.discover.usb-serial`, and `device.discover.mdns` actions reuse the
existing `sensorium.directive.invoke` capability. They are action identifiers,
not new transport capabilities: do not add `sensorium.device.discover`, a
transport-specific capability registry, or a universal device registry.

P072 continues to admit the capability identity and its permitted use. The
Sensorium action catalog and current host policy separately admit the concrete
`action_id`, signed provider package, profile, transport scope, mode, limits,
caller and action-scoped grant before provider launch or I/O. A grant for the
invoke capability alone does not admit every discovery action. Package signing,
catalog presence, Schema Gate validity and provider registration each preserve
their own boundary and none supplies effect authority on its own. Unknown,
unadmitted, unavailable, or out-of-scope actions fail closed.

`connector_id` remains an internal resolution detail; callers select an admitted
action rather than an arbitrary connector. Provider registration is independent
of a bound device instance, and neither registration nor an ephemeral candidate
creates acquisition, pairing, publication, or Interface read authority.
[P048's planned effect requirements](048-sensorium-os-connector-action-classes.md#planned-local-device-discovery-effect-requirements)
remain an additional enforcement condition, not a consequence of registry
eligibility. `P045-DISC-002` owns this admission/routing work and its refusal
evidence. This documentation continuation changes no machine registry entries,
authorization-policy sidecar coverage, capability availability, or completed
P072 tracker status.

## Planned Local Capability Guidance and Controller Discovery

This section began as a design continuation on 2026-10-18; the local contract
freeze and focused implementation checkpoint are recorded separately below.
The promoted registry baseline remains unchanged. This continuation supports
knowledge symmetry and human agency by making existing contracts
understandable without turning documentation into authority.

A capability is the unit of description; middleware is a provider, not the unit
of tool identity. The host owns the caller-scoped read projection. Inquirium
performs inference; the consuming controller owns continuation and dispatch.
A skill may later compose several capabilities, but no skill registry is needed
for this slice.

### Minimal Contract and Authority Boundaries

The first local implementation registers two host operations:
`capability.catalog.list` and `capability.catalog.describe`. Registration
precedes runtime dispatch: `host-local`, `dispatchable: true`,
`host-route: true`, `docs.human-registry: true`; advertisement, Passport,
signing-domain and federated-discovery flags remain false. Neither operation
grants access to the capabilities it describes.

| Contract element | Required meaning |
| --- | --- |
| Optional `capability-guidance.v1` | Exact `capability/id`, pinned `contract/ref` and `contract/digest`, `description` and `lang` (English by default). Optional `usage/when`, `usage/avoid`, bounded `usage/notes` or pinned `usage/ref`, and schema-checked examples. Reuse S007 profile vocabulary rather than inventing a second description taxonomy. |
| List request/result | Optional simple filters, bounded `limit` and opaque `cursor`; stable ordering, authorized summaries, `catalog/revision` and explicit continuation. No embedding search or total count of hidden entries. |
| Describe request/result | Exact capability id and, where necessary, an explicit opaque operation selector. Return canonical request/response schema bindings, optional guidance and its digest, source provenance, classification, and separately observed provider availability and authorization requirements. |
| Honest states | Distinguish visible-but-unavailable, unknown availability, missing guidance, unresolved/ambiguous contract and stale revision. Unknown and unauthorized ids share an externally non-disclosing response where existence is private. No single `available` boolean implies execution permission. |

Guidance is optional: its absence does not make a valid capability unusable.
Missing or ambiguous machine contracts must not be reconstructed from prose.
Provider usage notes stay bound to their exact admitted provider and contract;
several providers must not yield an arbitrary winning description. A verified
signed package and current operator admission would establish source
provenance, not semantic review of the notes. The host never treats their text
as authority.

An admitted signed provider report may be read from host-retained state without
invoking the provider handler. Package admission does not grant that module
permission to call the host catalog: module-to-host invocation retains its
own authenticated channel binding and the Agent's current caller scope.

### Local Contract Freeze (2026-10-19)

The first local slice uses `capability-catalog-request.v1`,
`capability-catalog-result.v1`, and optional `capability-guidance.v1`.
The v1 request continues to receive the original closed v1 result. An explicit
`capability-catalog-request.v2` selects `capability-catalog-result.v2` for
per-operation readiness. The controller uses v2; both versions keep the same
caller-scoped host admission and the same two catalog operations.
`list` accepts an optional exact capability-id prefix, a page limit, and an
opaque continuation cursor. `describe` requires an exact registered capability
id and accepts an operation selector only when the admitted descriptor binds
several operations. `include: "summary"` (the default) projects bounded
required fields, types and enum/const values; `include: "schema"` requests the
complete trusted local schema. `agent/id` and `binding/ref` are untrusted lookup locators
inserted by the host controller, not model arguments. The host derives principal,
scope, grants, and source revisions from the currently authenticated actor and
binding; a mismatched or absent binding receives a refusal.

| Limit | First-slice maximum |
| --- | ---: |
| List page (default) | 8 entries |
| List page (maximum) | 16 entries |
| List result | 16 KiB canonical JSON |
| Describe result | 32 KiB canonical JSON |
| Default schema summary | At most 32 top-level properties; `truncated: true` signals omission and full schema requires `include: "schema"` |
| Guidance inline text (`description` and usage combined) | 2 KiB UTF-8 |
| Guidance examples | 2, each at most 4 KiB canonical JSON |
| Local instruction/schema reference depth | 1, with at most 16 KiB resolved bytes |
| Controller catalog reads / inference rounds | 3 / 4 |
| Controller catalog pages / total catalog context | 2 / 64 KiB |
| Rendered host-observation envelope | 64 KiB, also subject to the selected prompt-token cap |
| Controller wall time | Current remaining Agent wall-time budget; no separate 30-second cutoff |

The PromptAssemblyPolicy instruction-token cap remains authoritative for
continuation layers. The controller also limits result bytes; bytes are only a
resource ceiling and do not substitute for the runtime token budget. A required
result that exceeds the selected prompt cap refuses continuation. No global cap
is raised to make catalog reads fit.

The list order is ascending canonical `capability/id`, after current caller
visibility is evaluated. It returns no total count. `catalog/revision` is a
domain-separated, host-keyed HMAC-SHA256 over the canonical visible catalog
snapshot; its `sha256:` wire prefix does not mean an unkeyed digest. Hidden
changes do not alter that snapshot. Transient provider readiness changes
`availability` but do not change the consistency revision. Each `operation/id`
is a separate domain-separated, host-keyed HMAC-SHA256 over the revision plus
the selected provider's routing, contract and effect fields. The selector is
opaque; it neither exposes nor authorizes its provider endpoint. Both values
use the host-owned cursor key and change when that key is replaced, including
after restart. A cursor binds the authenticated Agent/actor scope, filter,
limit, visible revision, next position, and an expiry no later
than five minutes. Each page rechecks current authority. A foreign, expired,
malformed, or stale cursor is a non-retryable `stale-cursor` refusal; a new list
call without cursor begins a fresh traversal. No cache of catalog results is
required.

The signed cursor payload is base64url-encoded, not encrypted. Its scope field
`s` is a third domain-separated HMAC with the same host key over the canonical
actor, Agent, binding and visible-capability scope; it contains none of those
raw identifiers. The cursor is an opaque continuation token for callers, not a
confidentiality envelope for its filter, position or expiry fields.

`describe` projects only exact admitted operation bindings and known effect
metadata. Missing effect metadata is `unknown`, never `read-only`. Multiple
operations require an explicit selector; conflicting descriptors remain
`ambiguous-contract`. Provider readiness is `ready`, `unavailable`, or
`unknown`, independent of visibility and authorization requirements. Each
described operation carries its own provider availability. The top-level
availability summarizes all providers when the contract is ambiguous, and
reflects the selected provider after an explicit operation selection.
The original closed `capability-catalog-result.v1` operation shape has no
per-operation `availability`; request v1 still emits that exact shape.
`capability-catalog-result.v2` requires the field for every described operation.
It also requires `unresolved/reason` on an unresolved operation binding:
`missing`, `untrusted`, `unknown`, `remote`, `cycle`, `constraint`, `limit`, or
`budget`. `budget` means that this describe exhausted its 16 distinct trusted
local source snapshots; `limit` means its depth or byte bounds prevented
closure. The reason is intentionally closed and omits private refs and paths.
The result v1 binding remains unchanged. A repeated source uses the same
temporary resolution result, and source order rather than the keyed operation
selector decides which distinct source receives a finite slot.
An absent field in v1 gives no basis to infer readiness or execution permission.
No consumer outside the checked Node/Orbidocs repositories has been verified;
explicit version selection preserves the old v1 wire shape. Guidance is absent unless its provider
and contract ref/digest match exactly. Multiple
eligible provider contributions do not select a winner. The first slice admits
request examples only, validated against the exact request contract. Invalid
examples or an unresolved local instruction ref exclude that guidance without
disclosing provider diagnostics;
they never trigger network retrieval. `doc/url` is never dereferenced.
Guidance `contract/digest` pins the admitted source schema snapshot;
`operations[].request.schema/digest` describes the canonical locally closed
schema projection. They are equal when closure leaves the schema unchanged,
but may differ when a trusted local `$ref` is expanded. A projection digest
must not be presented as the source pin.
The compact summary preserves `type`, `enum`, and `const` through a local
`$ref` with annotation-only siblings. Other composed `allOf` contracts stay
opaque in the summary and set `truncated: true`; callers request
`include: "schema"` for the complete contract.

An unknown id, a hidden id, and a private package id share the same externally
observable `not-found` result. Authorization and disclosure precede descriptor
or guidance dereference. Results are lower-trust data with classification and
source digests; current P090 inference-egress admission runs before each model
continuation, including reuse. A catalog read projects locally retained,
admitted provider reports; it does not invoke the provider over the middleware
channel. The controller attaches an internal read correlation to the host
result and consumes only its first matching delivery. At delivery it checks
current Agent lifecycle, binding, grants and deadline before parsing the
result body, then rechecks disclosed scope before adding an observation and
again before the next inference. The result-admission unit ignores foreign and
repeated deliveries without parsing them. A mismatch at the synchronous
controller's own handoff violates its host invariant and stops the action
without retry. A matching result after stop, withdrawal of a required grant or
deadline terminates this passage without exposing its body. Suspend and resume
invalidate the old passage through its captured lifecycle epoch, even if the
Agent is Running again. Cancellation is logical at the next
synchronous boundary: this slice does not preempt an already blocked read or
inference call, and an inference already admitted before withdrawal remains
in flight. No new channel frame or result transport follows from this rule.
Timeouts, exhausted budgets, stale scope/revision, and invalid guidance are terminal for this
continuation. No automatic retry or fallback to remote lookup occurs.

Inquirium's current role vocabulary has no correlated native tool call for a
tool-result role. The supervised checkpoint binds classified catalog data to a
host-owned, canonical `inquirium.host-observation.v1` envelope in a required,
fixed operation postamble. It carries source, opaque read ref, result digest and
JSON data, with explicit `transport: user-text` and adapter `user`-role
admission; [P064](064-inquirium-implementation-recommendations.md#planned-progressive-capability-guidance)
owns the exact assembly contract. This is structural provenance, not an
injection defense: guidance can still influence a model within otherwise
permitted behavior. Host policy, grants and effect admission remain the
enforcement boundary; model-level resistance to hostile notes is not qualified
by a deterministic controller test.

An invalid model proposal terminates the current controller action with a
non-retryable `agent_model_proposal_rejected` diagnostic (HTTP 422); it does not
stop the Agent or commit an effect. The operator may submit another action at
the unchanged step. A catalog read refusal, stale authority or classification
gate also aborts this action; a budget limit returns HTTP 429. No automatic
retry follows any of these outcomes. A single proposal outside the two catalog
operations is returned unchanged as an inert Inquirium product for the existing
Agent effect admission. A mixed catalog and effect proposal is rejected as
ambiguous; the model must propose the effect again after a catalog result.

The controller transition table is intentionally closed:

| State | Accepted event | Next state |
| --- | --- | --- |
| awaiting-inference | one valid allowlisted proposal | pending-read |
| pending-read | one matching, currently admitted result | pending-egress |
| pending-egress | classification and egress admitted | awaiting-inference |
| awaiting-inference | ordinary answer | completed |
| awaiting-inference | one non-catalog proposal | completed with unchanged inert product |
| awaiting-inference | mixed catalog and effect proposals | stopped with model-proposal diagnostic |
| any nonterminal state | refusal, cancellation, deadline, or budget exhaustion | stopped |
| completed or stopped | late or duplicate result | same terminal state |

Correlation binds Agent, binding, proposal ref, capability id, request digest,
and controller step. A result for another correlation or a repeated completion
does not start inference. The allowlist is exactly `capability.catalog.list` and
`capability.catalog.describe`; a capability named by a result is never added.

Admission derives the principal, scope and disclosure policy from authenticated
host context, never from model-selected identity fields. Apply disclosure before
enumeration, dereferencing or counting; exclude endpoint URLs, credentials,
private paths and unrelated configuration. Use existing classification and
inference-egress gates before any returned material enters model context.

Instruction text is lower-trust documentation, never host-root policy or a grant.
Source attribution is host-derived. Bind the effective guidance to its own
canonical digest: `schema/ref` alone does not identify changing descriptions.
Cache keys include authorized scope and contract/guidance revisions; recheck
revocation and disclosure on reuse. Cursors are scope/revision-bound and expire.
A later invocation always rechecks current authority and provider binding.

### Implementation Recommendations and Re-use

- Reuse `node:capability` registry/admission and its authorization-policy sidecar;
  do not equate `dispatchable` or a missing sidecar entry with caller permission.
- Reuse `node:host-capabilities` provider projections and host readiness sources.
  Keep the catalog as a derived view, not a new registry or provider supervisor.
- Reuse [P068](068-api-surface-projection.md#planned-capability-contract-projection)
  descriptor-to-capability/schema bindings. Select explicit operations; do not
  scrape a whole OpenAPI document into a model prompt or assume one endpoint per id.
- [P080](080-multiplexed-middleware-channel-executor.md#planned-local-capability-guidance-contributions)
  and [S019](../60-solutions/019-middleware/019-middleware.md#planned-local-capability-guidance)
  own optional local provider contributions over existing reports/channel calls.
  Catalog reads use ordinary host invocation, not a new channel frame or changed
  meaning of the existing routing `lookup`.
- Keep deterministic validation/projection in existing lower-level owners; host
  adapters acquire sources and enforce authority. Reuse canonical JSON/digest,
  bounded artifact resolution, schema-gate and Rust/Python host clients. No new
  crate, database, transport or recursive generic tool executor is presumed.
- [P064](064-inquirium-implementation-recommendations.md#planned-progressive-capability-guidance)
  / [S044](../60-solutions/044-inquirium/044-inquirium.md#planned-progressive-capability-guidance)
  own prompt assembly; [P073](073-agent-orchestration-organ.md#planned-bounded-local-catalog-continuation)
  / [S047](../60-solutions/047-agent/047-agent.md#planned-local-catalog-continuation)
  own the first controller loop.
- Follow `node:DEV-GUIDELINES.md`: contracts before endpoints, validation at
  boundaries, authority before effects, bounded caches and calls, no upward
  dependencies. Future implementation updates Node's ledger/MVP only for proven
  scope, regenerates registry docs and retains refusal evidence.

### First Slice and Acceptance Ownership

The first slice is **local list/describe plus one bounded Agent controller
continuation**: inference proposes a catalog read; the controller validates and
executes it; a classified result enters the next inference; the controller stops
or returns a normal answer. Reuse `propose_tool_call` as inert data, with an
explicit allowlist of only the two catalog operations. Other proposed tools do
not execute through this loop.

Use two registered local fixture capabilities, including one with no optional
guidance. A mutation-capable capability may be described, but must never be
invoked by this slice. Retain real local host/controller evidence; a projection
unit test or model-output fixture alone does not prove the continuation.

Acceptance must cover: list → describe → next inference; missing guidance;
provider loss and ambiguity; hidden/private ids; schema/guidance mismatch;
revocation between reads; stale cursors; hostile instruction text; classification
or egress refusal; bounded rounds/pages/bytes/time; cancellation and duplicate
results without duplicate continuation. A fixture must prove that neither a
catalog miss nor a supplied `doc/url` triggers network acquisition. Freeze numeric
limits and failure/retry semantics in the contract task before coding.

P072-GUIDE-003 owns one retained report referenced by all participating trackers.
Record tested source and contract revisions, controller/model identity, limits
and separate contract, host-path and model-conformance results. This is focused
local evidence, not federation, general tool execution or release qualification.

No Seed query, peer advertisement, Passport publication, remote document/schema
fetch, device scan, model startup/shutdown hook, or general skill runner belongs
to this slice. Guidance visibility also does not opt a caller into nonlocal
inference. [P024](024-capability-passports-and-network-ledger-delegation.md),
[P025](025-seed-directory-as-capability-catalog.md) and
[S007](../60-solutions/007-capability-advertisement/007-capability-advertisement.md#local-guidance-is-not-federated-discovery)
remain separate federation owners.

### Supervised Local Acceptance Checkpoint (2026-10-19)

This checkpoint composes the existing owners rather than changing catalog
identity or adding execution authority. Use one operator-admitted, supervised
local middleware report with two registered capabilities: one with an exact
pinned operation contract and admitted `capability-guidance.v1`, and one
with the same contract discipline but no guidance. Describe a mutation-capable
operation; the catalog controller must not invoke it. Record the admitted
provider, contract and guidance revisions, including an explicit
absent-guidance state. Record package signature and launch-integrity evidence
separately; an operator-configured test module without such verification does
not prove signed-package provenance.
The current bounded fixture selects the registered provider-owned local ids
`role.example.execute` (guided and effectful) and
`role.example-summarizer.execute` (no guidance), with the admitted local
`node:middleware/schemas/role-task-execute-request.schema.json` request
contract. Fixture selection is test evidence, not a new domain rule or grant.

Run the ordinary middleware channel and host routes in one bounded local
acceptance scenario. An Agent bound to the authenticated principal has both
catalog grants and one independently admitted effect grant. Its scripted
inference reads list, then describe, then proposes the effect. A single
non-catalog proposal must leave the catalog controller unchanged and reach
ordinary Agent effect admission. An ambiguous mixed catalog/effect proposal
must stop with its model-proposal diagnostic and no effect. Observe the generic
host effect-dispatch boundary: catalog reads and descriptions cause zero effect
dispatches, while any later effect execution requires the ordinary admission
and consent path. Merely describing a mutation is not proof of its execution
authority.

The retained P072-GUIDE-003 report must separate three evidence classes:

| Class | Required observation | Claim excluded |
| --- | --- | --- |
| Contract/projection | Exact admitted report and schema/guidance binding, visibility, absence and ambiguity states, bounded summaries and cursor behavior. | A pure projection test does not prove live channel or controller behavior. |
| Local host path | Supervised report attach, channel carriage, host list/describe, Agent continuation and separate effect admission in one run; boundary observers for generic effect dispatch, federation and remote fetch, P090 inference egress, and redacted trace. | A scripted adapter does not prove autonomous model use. |
| Concrete model | Only a separately bounded trial on an already available local runtime, with model/provider identity and prompt policy recorded. | A deterministic provider does not qualify model behavior. |

In the local host-path run, exercise revocation between reads, provider loss and
ambiguity, unknown/hidden/private ids, mismatched guidance, stale or foreign
cursors, hostile notes, egress refusal before context reuse, read/round, page,
byte and wall-time budgets, cancellation, late and repeated results. Observe
catalog misses, `doc/url` and unresolved refs at federation and remote-fetch
boundaries to establish that they caused no such calls. Inspect returned
bodies, errors and trace for private identifiers, endpoints, paths and
credentials. Record each case as passed, failed or unmeasured, with the
observation point and revision. Do not promote partial rows from code presence
or a configuration assertion.

The host-observation envelope and explicit `User`-transport admission must be
tested with the selected adapter, including an adapter without `user` support
that refuses before inference. Assert that each exported observation ref is
fresh and independent of the private controller correlation. The envelope
proves the host's source and result binding, not semantic isolation from
provider instructions. It grants no tools and cannot weaken host policy,
classification, egress or effect admission. The shared report remains the only
GUIDE acceptance owner. This checkpoint does not change MVP, alpha, federation
or release status.

The measured local H scenario started an operator-configured supervised Python
module over the existing channel. Its admitted report contributed both fixture
capabilities; host list and describe showed their exact contract, distinct
effect metadata and guidance presence or absence. The controller passed three
catalog observations into four scripted local inference calls. Its non-catalog
effect proposal remained inert until a separate `agent.effect.propose` request
reached ordinary admission and was deferred for human review. The role handler
was not invoked during the catalog loop or effect proposal; a separate explicit
host invocation confirmed channel dispatch. Missing or invalid control tokens
returned 401 before catalog disclosure, and a wrong Agent binding returned 403.
That first H result alone did not establish signed package provenance,
autonomous model behavior, automatic Agent effect dispatch, or the unmeasured adversarial rows
in the shared report.
Current catalog visibility is derived from the intersection of Agent spec and
binding capability grants. The process Agent therefore holds grants for both
visible provider capabilities, while only the guided mutating effect is
proposed. Visibility still does not establish readiness or completed effect
admission, but a separate describe-only visibility permission is not yet
implemented. That grant separation remains an open boundary.

### Continuation Tracker

Statuses below follow the focused implementation checkpoint; historical
completed registry phases are not reopened. The shared evidence report is
`node:docs/audits/REVIEW-LOCAL-CAPABILITY-GUIDANCE-2026-10-19.md`.
P072-GUIDE-001 precedes P068-GUIDE-001, P080-GUIDE-001 and P064-GUIDE-001.
P068/P080 feed P072-GUIDE-002; prompt assembly (P064) can proceed in parallel.
P073-GUIDE-001 joins the ready projection and prompt assembly; P072-GUIDE-003
qualifies that combined path. These are necessary dependencies, not a requirement
to finish unrelated work in any of those proposals.

| ID | Work | Status | Depends on / completion gate |
| --- | --- | --- | --- |
| P072-GUIDE-001 | Freeze local catalog and optional guidance contracts, ownership and numeric bounds. | done | Four schema-gated DTOs, registry flag matrix, numeric limits, disclosure and transition rules; contract evidence: `node:docs/audits/REVIEW-LOCAL-CAPABILITY-GUIDANCE-2026-10-19.md`. |
| P072-GUIDE-002 | Implement caller-scoped local list/describe as a projection. | done | Supervised host HTTP covers two conflicting providers, explicit operation selection, per-operation readiness through loss and restart, describe-only visibility, identical hidden/unknown/private refusals and stale revision. A later supervised run withdraws a single Agent grant and observes reduced visibility before and after daemon restart. Injected host fetch resolver and artifact sink record zero attempts across misses and rejected `doc/url`. A separately materialized signed Python instance passes current operator admission and launch integrity, reports one guided and one unguided capability, and projects both through scoped host list/describe without handler dispatch. Its own and a foreign Agent binding each receive a typed 403 refusal when the independent module calls the host catalog through its channel; signing does not create a host-call binding. This closes local signed-source provenance, not semantic guidance review or model behavior. Shared evidence: `node:docs/audits/REVIEW-LOCAL-CAPABILITY-GUIDANCE-2026-10-19.md`. |
| P072-GUIDE-003 | Qualify the local controller slice and reconcile documentation. | partial | The supervised H path covers Public-ceiling and P090 egress refusals, provider loss/restart, scope and cursor refusal, lifecycle stop, single-grant withdrawal between reads, read/page/byte/deadline exhaustion, completed-request replay and concurrent/late duplicate request refusal without double inference. A focused host-route test holds an actual catalog result for admission after stop, grant withdrawal or deadline; its admission unit ignores foreign/duplicate correlations, while a mismatch in the synchronous controller stops the action. Two supervised suspend/resume cases invalidate old initial and continued passages through the lifecycle epoch. DNS/artifact and trace observers retain their focused scope. Signed-source and module-channel cancellation H checkpoints are now measured under P072-GUIDE-002/P080-GUIDE-001. Physical inference preemption, independently asynchronous controller result delivery and concrete-model behavior remain open. Shared report: `node:docs/audits/REVIEW-LOCAL-CAPABILITY-GUIDANCE-2026-10-19.md`. |

[P066](066-inquirium-assistant-channel.md#planned-assistant-catalog-consumption)
owns a subsequent Assistant Channel consumer.
[P091](091-file-backed-configuration-and-explainable-composition.md#planned-capability-guidance-overlays)
owns the now implemented local guidance-only operator overlay, with focused
C/H evidence in `node:docs/audits/REVIEW-CAPABILITY-GUIDANCE-OVERLAY-2026-10-23.md`.
It changes effective documentation only after a reviewed P091 commit; it does
not close this catalog's separate model qualification; signed-source evidence
is now recorded under P072-GUIDE-002.
[P093](093-package-scoped-private-capabilities.md#planned-scoped-capability-guidance)
and [P085](085-operator-sovereign-extensibility-and-experiment-packages.md#capability-guidance-package-boundary)
own private-package admission constraints. These follow-ups are not prerequisites
for the first slice: initially exclude private package ids and accept only
validated local guidance with an unambiguous binding.

## Resolved Decisions

The former Q1 (source direction) and Q2 (one registry vs two) are **decided in §1** —
single repo-checked-in source with a generated docs projection, one registry with a
`surfaces` set — because leaving them open would undercut P072's purpose.

The former Q3 (grandfathering migration), Q4 (authorization-policy-as-data), Q5
(federation-extension governance), and the CR-97 follow-up questions are also decided:

1. **Grandfathering migration.** Seed every currently known capability as `active` in
   the first registry and fail closed immediately for any new unregistered capability.
   Backward compatibility is not required at this stage, and preserving the warning-only
   gap would undercut the registry's purpose.
2. **Authorization-policy-as-data.** Keep policy as a checked sidecar rather than
   embedding it into `capability-registry.v1`. The first landed sidecar is
   `capability-authorization-policy.v1`, seeded from P071 §9 and validated against the
   registry plus the P071 Workbench/Interaction Broker capability set.
3. **Federation-extension governance.** Create a separate governance proposal for
   namespace allocation, registration authority, and revocation. It is intentionally out
   of P072 implementation scope.
4. **Legacy Rust projection.** `node:capability/src/lib.rs` may retain
   `CAPABILITY_ADVERTISEMENT_MAP` as a transitional projection for older callers,
   provided it is mechanically checked for completeness over registry entries with
   `advertisable = true`. The machine registry remains the source of truth.
5. **Versioning policy for this change.** The fail-closed removal of lenient fallback
   in `capability_id_from_advertisement` is documented as a migration note rather than
   a crate version bump for now, because `orbiplex-node-capability` is still an
   internal `0.1.0` crate in this workspace.
6. **Reserved-name catalog visibility.** `reserved` entries may be visible in the
   human registry when that protects a namespace or gives developers useful guidance;
   admission still refuses them until their machine status changes.

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
`wire/name = app/corpus-provider`. A `reserved` entry carries its id and flags but
`status = "reserved"`, so the gate holds the name while refusing use. The registry file
is repo-checked-in; git history is its change authority, and the load-time check verifies
structural integrity before the daemon serves any capability surface.

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code
evidence) · `[d]` deliberately deferred out of this proposal's implementation scope.

### Current implementation coverage audit

Audited on `2026-06-24` after implementation.

Implemented now:

- `node:capability/capability-registry.v1.json` is the checked-in machine source
  of truth for federated and host-local capabilities.
- `node:capability/src/registry.rs` validates the registry, canonical id grammar,
  unique `wire/name`, status semantics, derived `surfaces`, and use-specific
  eligibility flags.
- The legacy Rust `CAPABILITY_ADVERTISEMENT_MAP` is retained only as a
  transitional runtime projection and is checked for coverage of all registry
  entries with `advertisable = true`; it is not a second authority.
- Capability advertisement signing/verification, capability passport validation,
  daemon host-capability dispatch/routing, literal control-plane `POST /v1/host/capabilities/*` routes, and supervised middleware module-report
  admission fail closed for unregistered or ineligible formal capability ids.
- Dynamic middleware reports are rejected before routing when they claim
  unregistered or ineligible host capability handlers.
- `capability-registry.v1` has mirrored schemas/examples in `orbidocs` and
  `node/protocol/contracts`; schema validation covers positive and negative
  registry examples.
- `orbidocs:scripts/check-capability-registry.py` validates the machine registry
  against the legacy Rust projection, including `advertisable` coverage, human EN/PL registry tables, and
  `capability-advertisement.v1`, `capability-passport-present.v1`,
  `seed-capability-registration.v1`, and `capability-authorization-policy.v1` fixtures
  plus the P071/P082 policy coverage sidecar. The sidecar is intentionally seed-scoped
  rather than complete over the whole registry: it covers the P071 Workbench and
  Interaction Broker capabilities plus P082 Sensorium Interface operations that need
  checked authorization metadata in this phase.

Still out of P072 implementation scope:

- federation-extension governance and public namespace allocation.

Those are intentionally separate proposal tracks, as decided in §2.

### Phase 0 — Enumerate and seed

- [x] Enumerate every capability the node currently advertises, requests, or dispatches
  (federated **and** host-local, including `/v1/host/capabilities/*`). Evidence:
  `node:capability/capability-registry.v1.json` contains the canonical active/reserved
  entries and preserves the legacy Rust advertisement projection as a checked subset.
- [x] Seed `capability-registry.v1`; grandfather every currently known capability as
  `active`, then fail closed immediately for new unregistered capabilities. Evidence:
  `node:capability/src/registry.rs` and `cargo test -p orbiplex-node-capability`.

### Phase 1 — Enforce (fail-closed)

- [x] Daemon derives dispatchable/host-route admission from the registry before
  dispatching host capability calls or exposing simple host capability routes.
- [x] Unregistered capability → denied at dispatch, advertisement, and passport gate.
  Evidence: capability passport validation, network advertisement sign/verify gates,
  daemon host-capability registry admission tests, and middleware supervisor report
  admission tests.
- [x] Load-time fail-closed for the checked-in static registry: malformed registry
  material fails the embedded registry parser/tests before runtime surfaces can treat it
  as an allow-set.
- [x] Two-layer completeness: build-time/static checks validate code/docs/fixtures plus literal daemon host-capability POST routes
  against the registry, including completeness of the legacy Rust projection for
  `advertisable` entries, and runtime admission validates dynamic middleware
  reports before routing. JSON-e binding policy-as-data remains separate authorization scope.

### Phase 2 — CI drift gate

- [x] Validate the docs projection, node allow-set, and passport/advertisement fixtures
  against the registry; drift fails the build. Evidence: `make check-capability-registry`
  now validates `capability-registry.v1`, eligibility flags, EN/PL human projection,
  the Rust projection and its `advertisable` coverage, literal daemon
  host-capability POST routes, and passport/advertisement/Seed Directory fixtures.

### Phase 3 — Register new capabilities (P069/P070/P071 prerequisite)

- [x] `room.open` / `room.join` / `room.membership-query` (P070). Registered in
  `capability-registry.v1` and covered by registry admission/drift gates.
- [x] `sensorium.workbench.*` (P071). Registered in `capability-registry.v1` and
  covered by registry admission/drift gates.
- [x] `corpus.*` (P069). `corpus.provider` is registered in
  `capability-registry.v1` and covered by registry admission/drift gates.
- [x] host `interaction-broker.wait` / `.watch` / `.probe` (P071). Registered in
  `capability-registry.v1` and covered by registry admission/drift gates.
- [x] `sensorium.interface.read` / `.subscribe` / `.manage` (P082). Registered
  with read/subscribe Passport eligibility, host-local non-Passportable manage,
  and checked authorization-policy sidecar entries.

### Phase 4 — Authorization-policy-as-data `[x] policy sidecar landed`

- [x] Express required grants / COI / autonomy levels as registry-consumable sidecar
  data. `node:capability/capability-authorization-policy.v1.json` carries the P071
  Workbench/Interaction Broker plus Sensorium Interface seed policy;
  `orbiplex-node-capability` parses and
  validates it; daemon startup preflight now validates both registry and authorization
  policy; Orbidocs schema/examples are mirrored into node protocol contracts; and `make
  check-capability-registry` validates sidecar shape, registered capability refs, mirror
  sync, and P071/P082 seed coverage. Runtime enforcement of those sidecar grants remains a
  host-policy consumer responsibility, not an extra P072 registry gate.

### Phase 5 — Federation-extension governance `[d] separate proposal track`

- [d] Federation namespace allocation, registration authority, and revocation belong in
  a separate governance proposal. P072 intentionally does not implement governance over
  public namespace authority.
- [d] Operator-local derived capability sets and experiment-package composition belong
  to P085. They must not become an alternate path for adding base capability ids or
  bypassing registry admission.


## Generic scheduled module jobs (S020)

The host-only `scheduled-job.invoke` operation and the schema-gated
`scheduled-module-job-request.v1` / `scheduled-module-job-result.v1` contracts are
a separate execution surface. Operator-approved S020 configuration binds component,
executor, operation and bounded launch budget. Every dispatch rechecks current
admission and activation; a read capability or a package fragment cannot invoke
or authorize this surface. No evidence-specific host capability is registered.
The [S020 contract](../60-solutions/020-scheduler/020-scheduler.md#generic-module-job-authority-deadline-and-failure-contract)
owns deadlines, `Transient`/`AuthorizationDenied` meanings, unknown outcomes and
consumer recovery duties. The evidence-supervision module is an opt-in consumer.
