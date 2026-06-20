# Proposal 068: API Surface Projection (Aggregated OpenAPI)

Based on:
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

## Status

Draft

## Date

2026-06-13

## Executive Summary

Orbiplex exposes HTTP surfaces from many components: the Rust daemon control
plane, supervised HTTP middleware (messaging, contact-catalog, attestation,
Inquirium adapters, simulator, …), and external/operator-supplied modules. The
"what endpoints exist and what flows through them" knowledge is today implicit
in route-match code and middleware handlers, scattered across two languages.

This proposal introduces an **API Surface Projection**: a single, aggregated
OpenAPI document, served from one place, that lets developers and authors of
third-party clients/middleware **see the cross-cutting HTTP surface and test
flows live**.

It is deliberately **not** a source of truth for contracts. The canonical
contracts remain the versioned JSON Schemas in `node/protocol/contracts/schemas`
and the semantic authority model (auth, `classification.v1`, capability/passport
scope, fail-closed, idempotency). The projection is generated from those
schemas where the endpoint binds one, with a manual-registration escape hatch
for endpoints whose shapes are not Orbiplex data contracts (external components
with their own API paths).

The architectural rule:

> Components contribute **data** (a small, uniform API descriptor); the daemon
> contributes the single **runtime** (one aggregator, one served OpenAPI). No
> component runs its own Swagger server, and no body shape is re-declared — the
> projection `$ref`s the canonical schemas.

This dissolves the two ways an OpenAPI requirement usually backfires: it never
becomes a second source of truth (bodies are single-sourced by `$ref`), and it
never rots as a hand-maintained artifact (it is generated from schemas and
collected live from running components).

## Context and Problem Statement

Three real frictions motivate this:

1. **No cross-cutting view.** Reading the daemon's `route_request_with_auth`
   match arms and each middleware's `do_POST`/`do_GET` is the only way to learn
   the surface. Third parties writing a client or a new middleware have no
   browsable, testable map.
2. **Two languages, one surface.** The daemon is Rust; adapters are Python.
   A language-neutral description is the only way one tool/test/client works
   across both — consistent with the project's "agnostic implementations" and
   "neutral data territory" values.
3. **Drift is invisible.** Route renames, response-shape changes, manifest
   shape changes (e.g. the Inquirium simulator's `simulated_model_bindings`,
   the local-readiness-gate response) are caught late. A projection validated
   against the running surface surfaces drift the same way `schema-gate`
   surfaces schema drift.

The non-goal is equally important: this must not be mistaken for the contract.
OpenAPI describes **shape**, not **semantics**. Authority (reflective CSRF,
capability/passport scope), classification, fail-closed behavior and idempotency
are not expressible in OpenAPI and stay in the schemas plus solution docs.

## Current Implementation Evidence

What already exists and is reused, not rebuilt:

- **Canonical schemas, JSON Schema 2020-12.** `node/protocol/contracts/schemas/*.json`
  declare `"$schema": "https://json-schema.org/draft/2020-12/schema"`. **OpenAPI
  3.1 is a superset of JSON Schema 2020-12**, so the projection can `$ref` these
  schemas with no conversion (OpenAPI 3.0 would have required lossy munging).
- **A uniform component seam already exists.** Every supervised HTTP middleware
  serves a health/init surface (`/healthz`, `/readyz`, `/v1/middleware/init`
  init report — e.g. `InquiriumAdapterHandler._init_report`, extended by the
  simulator to add `adapter_manifest.simulated_model_bindings`). The daemon
  already collects these during supervision and knows each component's bind/port.
  **Relation to the new field:** `api/surface` is a **sibling** of
  `adapter_manifest` in the init report, not nested under it — the descriptor is
  uniform across every component type (adapter, store, service), while
  `adapter_manifest` stays adapter-specific. The two coexist; do not fold the
  surface descriptor into the adapter manifest.
- **Shared handler libraries.** The Inquirium adapters share
  `inquirium_adapter.InquiriumAdapterHandler` and the bounded HTTP server; the
  daemon has route families. Descriptor generation for common endpoints can
  live in the shared layer and be inherited, exactly as the manifest exposure
  pattern already works.
- **`schema-gate`** already validates payloads with positive/negative fixtures —
  the projection's "does it match reality" check is the same discipline applied
  to the HTTP surface.

## Proposed Model / Decision

### 1. Contribution unit: a per-component API descriptor (data)

Each HTTP component declares its surface as a small, normalized JSON document,
`orbiplex.api-descriptor.v1`. It is **not** hand-written OpenAPI. Each endpoint
entry references either a canonical schema id (`schema_ref`) or, only where no
data contract applies, an inline minimal shape/example.

### 2. Aggregation: one runtime in the daemon

The daemon is the aggregation point (it already supervises every middleware,
knows their binds, and proxies them). It reads the `api/surface` section from
the init reports it already collects (resolved seam; a dedicated
`GET /v1/api-descriptor` is the fallback for components that do not report),
includes `protocol`-surface entries by default and non-`protocol` `surface`
entries (`operator`/`developer`/`internal-loopback`/`external-component`) only
when opted in (resolved scope), resolves every `schema_ref` against the
canonical schema registry, and assembles **one** OpenAPI 3.1 document. It is
served from a single daemon endpoint (`GET /v1/openapi.json`) with an optional
single Swagger UI (`GET /v1/docs`). No component runs its own Swagger server.

### 3. Generation first, manual registration as escape hatch

- **Generated path (preferred):** where an endpoint binds a canonical schema,
  the descriptor entry carries only the schema id; the aggregator pulls the
  schema content. The descriptor itself should be **derived from the
  route↔schema binding**, not hand-listed, wherever the route registration makes
  that derivable (Rust: a route registry/derive at route definition; Python: the
  shared handler enumerates its routes). Hand-listing generated entries just
  moves the rot from OpenAPI into the descriptor.
- **Manual path (escape hatch):** external components with their own API paths
  not tied to Orbiplex data contracts register a descriptor of the **same shape**
  with inline schemas/examples. The daemon ingests these (operator-dropped file
  or config) and merges them identically. Manual entries are the only rot
  surface, kept honest by a contract test that each `schema_ref` resolves **or**
  the `inline` schema validates through schema-gate, and that the declared route
  exists in dispatch — **without live-probing mutating routes** (see *Descriptor
  Boundary Rules*).

### 4. Projection, not authority

The aggregated document is operator/developer-facing and explicitly descriptive.
It must not leak secrets, auth tokens, or sealed internals, and it carries a
banner that the authoritative contract is the schemas plus the semantic model.
This is the same "projection, never authority" discipline used for the
Local Relationship SQLite projection and the readiness-gate views.

## Contract Sketch

`orbiplex.api-descriptor.v1` (what every component contributes):

```text
{
  "schema": "orbiplex.api-descriptor.v1",
  "component/id": "messaging-service",
  "base/path": "/v1/messaging",
  "endpoints": [
    {
      "method": "GET",
      "path": "/v1/messaging/outbox/{envelope_id}/body",   # host-exposed path
      "summary": "Bounded outbox body read",
      "tags": ["messaging", "read"],
      "surface": "protocol",          # protocol | operator | developer | internal-loopback | external-component
      "path/owner": "daemon-proxy",   # daemon-proxy | middleware-direct | external
      "path/exposure": "host-public", # host-public | operator | internal-loopback
      "loopback/path": "/v1/messaging/outbox/{envelope_id}/body",  # raw middleware path behind the proxy
      "path/params": [               # canonical {snake_case}; params are data; optional semantic/ref must be a known P068-16 vocabulary entry
        { "name": "envelope_id", "required": true,
          "schema": { "type": "string" } }
      ],
      "request": { "schema_ref": null },
      "responses": {
        "200": { "schema_ref": "urn:orbiplex:schema:messaging-message-body-local:v1" },
        "404": { "schema_ref": "urn:orbiplex:schema:error-local:v1" }
      },
      "x-orbiplex-auth": "module-authtok",        # descriptive label, never the token
      "x-orbiplex-effect": "read-only",           # read-only | mutates-state
      "x-orbiplex-classification": { "schema_ref": "urn:orbiplex:schema:classification:v1", "tier": "personal-local" },
      "x-orbiplex-authority": "descriptive-only"
    },
    {
      "method": "POST",
      "path": "/v1/host/capabilities/notification.create",
      "summary": "Create a notification (mutating)",
      "surface": "operator",
      "path/owner": "daemon-proxy",
      "path/exposure": "operator",
      "request":  { "schema_ref": "urn:orbiplex:schema:notification-create:v1" },
      "responses": { "200": { "schema_ref": "urn:orbiplex:schema:notification-created:v1" } },
      "x-orbiplex-auth": "operator-session",
      "x-orbiplex-capability": "notification.create",
      "x-orbiplex-effect": "mutates-state",
      "x-orbiplex-idempotency": "required",
      "x-orbiplex-classification": { "schema_ref": "urn:orbiplex:schema:classification:v1", "tier": "Community" },
      "x-orbiplex-authority": "descriptive-only"
    },
    {
      "method": "POST",
      "path": "/external/their/own/path",
      "summary": "External component endpoint (no Orbiplex data contract)",
      "surface": "external-component",
      "path/owner": "external",
      "request":  { "inline": { /* minimal JSON Schema or example */ } },
      "responses": { "200": { "inline": { /* … */ } } },
      "x-orbiplex-authority": "descriptive-only"
    }
  ]
}
```

Field semantics:

- **`surface`** (taxonomy): `protocol` (stable client/protocol API — the default
  projected set), `operator` (operator/control plane), `developer`
  (debug/dev/test surface), `internal-loopback` (supervisor/private loopback),
  `external-component` (manual descriptor for foreign modules). Only `protocol`
  is projected by default; the rest are opt-in (see Resolved Decisions #2).
- **`path` vs `loopback/path`**: `path` is the **host-exposed** path a client
  actually calls; `loopback/path` is the raw middleware path behind the daemon
  proxy. A descriptor MUST describe the host-exposed path; the raw loopback path
  is projected only for `developer`/`internal-loopback` entries and is never the
  public client contract.
- **`schema_ref`**: the canonical schema `$id` (URN, e.g.
  `urn:orbiplex:schema:message-envelope:v1`), resolved through the schema
  registry — see *Descriptor Boundary Rules*. Not a filename.
- **`x-orbiplex-*`**: OpenAPI vendor extensions carrying the minimum semantic
  metadata OpenAPI cannot express (auth class, capability, effect, idempotency,
  classification). They keep causality/security visible but remain
  `x-orbiplex-authority: descriptive-only` — never authority.
  `x-orbiplex-classification` MUST reference `classification.v1`
  (`{ schema_ref: "urn:orbiplex:schema:classification:v1", tier: … }`) where the
  `tier` is a value from that schema's enum — **not** a free string, so
  descriptors cannot drift from the canonical classification taxonomy.

Aggregator output: one OpenAPI 3.1 document where each `schema_ref` URN resolves
to a **local** `#/components/schemas/<name.vN>` populated by reference from the
canonical registry (not an external `$ref` to a file path — that would leak the
on-disk layout), and inline entries are inlined verbatim.

Invariants:

- the projection **never copies** a canonical schema body — it references it;
- a `schema_ref` that does not resolve is a build/test failure, not a silent
  drop (boundary parsers must not swallow corruption);
- no secrets/tokens/sealed internals appear in the output;
- the document is labelled non-authoritative.

## Descriptor Boundary Rules

These are the freeze-before-implementation rules. The largest risk here is not
Swagger itself — it is letting the registry/table become a hand-maintained list
*beside* the router, which rots exactly like hand-written OpenAPI. If the
registry/table is genuinely the data the dispatch reads, the projection is
clean; if it is a parallel description, it is not.

- **`schema_ref` resolution is frozen to the canonical `$id`.** Schemas already
  declare a stable URN `$id` (e.g. `urn:orbiplex:schema:message-envelope:v1`).
  `schema_ref` is that URN, resolved through one schema registry that maps
  URN → schema content. Versioning lives in the URN (`:v1`); there are **no
  aliases** (one id per schema). The aggregator emits a **local**
  `#/components/schemas/<name.vN>` populated by reference — never a filename, an
  external `$ref`, or a second id scheme. Without this, a parallel mini-registry
  appears.
- **`api/surface` is an optional additive field of `middleware-module-report`.**
  The current `middleware-module-report.schema.json`
  (`node/middleware/schemas/`) is `additionalProperties: false`, so `api/surface`
  will be rejected until the schema is extended. Add `api/surface` as an optional
  property referencing `orbiplex.api-descriptor.v1`; **absence is legal** (a
  component without an API surface is valid). Bump the report schema additively.
- **Host-exposed path is the contract; raw loopback is debug-only.** A descriptor
  describes the daemon-exposed path (`path`), not the raw middleware port/path,
  unless the entry is `surface: developer` or `internal-loopback` and carries
  `path/exposure: internal-loopback`. A loopback path MUST NOT be projected as
  the public client contract.
- **`x-orbiplex-*` metadata stays descriptive.** Vendor extensions may carry
  auth/capability/effect/idempotency/classification, but every entry is
  `x-orbiplex-authority: descriptive-only`. They do not make OpenAPI authority;
  they keep causality and security visible.
- **Mutating routes are never probed live.** The drift test splits: *route
  coverage* asserts registry↔dispatch parity **without executing any handler
  effect**; *response shape* is checked only in an isolated test harness/daemon,
  never against a live operator daemon. `POST`/`DELETE`/`release`/`cancel`/
  `passport.issue` and anything `x-orbiplex-effect: mutates-state` are excluded
  from any live smoke. The Swagger UI is operator-gated and disables request
  execution entirely.
- **Existing static OpenAPI is not maintained in parallel.** The current hand
  written, inline-schema file
  `orbidocs/doc/project/60-solutions/008-agora/agora-record-relay.v1.openapi.yaml`
  is **not** kept as a second OpenAPI model. No backward compatibility is owed:
  the Agora record-relay endpoints get descriptors (`schema_ref` to the canonical
  schemas), and the old YAML is either retired or repurposed as a **test oracle
  / fixture** for the aggregator output — not a living parallel contract.

## Aggregation Lifecycle, Conflicts, and UI Boundary

- **Lifecycle / component status.** The aggregate reflects component runtime
  state, it does not pretend everything is up. Default mode projects the stable
  daemon surface plus `ready` components; `?include=configured` additionally
  shows `configured`/`stopped`/`failed` components as **unavailable** (using
  their last persisted module report if present). Every contribution carries
  `component/status` (`ready|starting|stopped|failed|configured`),
  `descriptor/source` (`generated|manual|persisted-report`), and `generated/at`,
  so a reader can tell a live surface from a stale persisted one.
- **Surface include toggle.** Default projects `surface: protocol` only. An
  `?include=` query selects additional surfaces for the requester —
  `?include=operator,developer,internal-loopback` — and `?include=configured`
  composes with it for lifecycle state. This serves both audiences: a clean
  protocol surface for third-party client authors by default, and the full
  operator/control-plane view (which is mostly Node-UI-facing) on demand.
- **Caching.** Because the output encodes component status and the included
  surface set, projection endpoints (`/v1/openapi.json`, `/v1/docs`) send
  `Cache-Control: no-store` — a cached document would misreport which components
  are up. The projection is a live view, not a cacheable artifact.
- **Self-description (no gap for the projection endpoint itself).** The
  projection endpoints are daemon-exposed, not raw middleware loopback, so they
  are described as `surface: developer` with `path/exposure: operator`
  (not `internal-loopback`, which is reserved for raw loopback behind the proxy)
  — projected only under `?include=developer`. They are not part of the default
  `protocol` surface, so `GET /v1/openapi.json` does not appear in its own
  default output, but it is not invisible either.
- **Path/method conflict rule.** Conflicts are detected on two keys — the
  canonical *display key* (`METHOD + canonical_path`) and the parameter-erased
  *shape key* (`METHOD + /v1/receipts/{}`); see *Path Template Normalization* for
  the full rule, including the `{receipt_id}` vs `{id}` same-shape case. A
  `protocol`/`operator` host-exposed conflict is **fail closed** (two owners of a
  public/operator route is a real defect); `developer`/`internal-loopback` may
  downgrade to a warning unless namespaced by a distinct `path/owner`. Never
  silently last-writer-wins.
- **Swagger UI boundary (security).** `/v1/openapi.json` is the MVP artifact;
  `/v1/docs` (Swagger UI) is a developer/operator convenience. The daemon builds
  the projection server-side and embeds the resulting OpenAPI JSON into the HTML
  shell, so client JS is **not** handed a daemon authtok and does not perform a
  privileged second fetch. Request execution is disabled (`supportedSubmitMethods:
  []`); the UI is descriptive, not a mutation console. The inline bootstrap
  script is gated by a per-request CSP nonce, and `frame-ancestors 'none'`
  blocks clickjacking embeds.
- **External-asset hardening (the remaining gap).** `/v1/docs` currently loads
  the Swagger UI JS/CSS from a public CDN (unpkg). No tokens leak, but this is
  the one place the node reaches the public internet, which is incoherent with
  the offline-first / no-phone-home stance: an air-gapped or offline node renders
  a blank docs page, and the page beacons to a third party on open. The driver is
  architectural coherence, not acute exploitability. Two tiers:
  - *cheap stopgap (done):* pin the exact Swagger UI version, add Subresource
    Integrity (`integrity=`) to the CDN `<script>`/`<link>`, and keep script
    execution behind a per-request CSP nonce plus `frame-ancestors 'none'`.
    This closes the supply-chain/integrity hole (a substituted/MITM'd asset
    cannot inject different JS into the operator-auth context) and avoids
    arbitrary inline script execution. The current node pins
    `swagger-ui-dist@5.32.6` with SHA-384 SRI. This does not fix offline.
  - *full hardening (low-priority post-MVP, P068-06 follow-up):* vendor the
    pinned Swagger UI dist and serve it from the daemon's own origin, which fixes
    offline + supply-chain + phone-home at once and lets `/v1/docs` keep a strict
    `self`-only CSP that loads nothing external. A smaller single-file bundle
    (e.g. Redoc) is an acceptable substitute if asset size matters. Tracks the
    pinned version for CVEs.

## Path Template Normalization

The merged OpenAPI `paths` are assembled from two languages with different
routers. The decision is **not** to normalize multiple dialects at runtime —
that would turn normalization into hidden semantics, where Rust and Python
descriptors that mean the same route arrive as different strings. Instead,
**freeze one canonical descriptor path format and enforce it on both sides.**

**RESOLVED.** Path templates in `orbiplex.api-descriptor.v1` use canonical
OpenAPI-style `{snake_case}` segment parameters. Producers in Rust and Python
MUST emit canonical templates directly. Framework-native syntax (`:id`, `<id>`,
glob/splat, regex captures, partial-segment params) is **not accepted** in
descriptors; it may exist only in migration/lint tooling, never in a stored
descriptor.

Canonical path rules:

- starts with `/`; no trailing slash except the root `/`;
- a parameter occupies a whole segment: `{receipt_id}`, never `receipt-{id}`;
- parameter name is snake_case, `^[a-z][a-z0-9_]*$`;
- no catch-all/splat in hard-MVP;
- query string is not part of the path-pattern;
- duplicate parameter names within one path are forbidden;
- paths are case-sensitive.

**Parameters are data, not just a name in the path.** Each templated parameter
is declared explicitly so the OpenAPI generator has `parameters` to emit and
neither language guesses meaning from the name. `semantic/ref` is **optional**
(MVP descriptors omit it and emit one canonical parameter name; it exists to
carry cross-component parameter meaning and to support the alias collapse rule
below). **When present, `semantic/ref` MUST be a known entry in the
`semantic-refs` vocabulary registry (P068-16)** — an unknown or free-form value
is a validation failure, never an ad-hoc label.

```text
{
  "method": "GET",
  "path": "/v1/receipts/{receipt_id}",
  "path/params": [
    { "name": "receipt_id", "required": true,
      "schema": { "type": "string" },
      "semantic/ref": "record-id" }      /* optional; if present, a known vocabulary entry */
  ]
}
```

### Semantic Refs Vocabulary (P068-16)

`semantic/ref` values are not free strings; they are drawn from one closed,
extensible registry so the same conceptual identifier reads identically across
components (and so the alias collapse rule can equate `{receipt_id}` with `{id}`
only when both declare the same `semantic/ref`).

- **Entry shape.** Each registry entry carries both the `semantic/ref` id and
  the **canonical parameter name** the alias-collapse rule emits (validation
  needs only the id; alias collapse needs `canonical_param`, so both are
  declared up front):

  ```text
  {
    "schema": "semantic-refs.v1",
    "entries": [
      { "id": "participant-id", "canonical_param": "participant_id" },
      { "id": "record-id",      "canonical_param": "record_id" },
      { "id": "envelope-id",    "canonical_param": "envelope_id" },
      { "id": "question-id",    "canonical_param": "question_id" },
      { "id": "contract-id",    "canonical_param": "contract_id" }
    ]
  }
  ```

  `id` form: `^[a-z][a-z0-9-]*$` (hyphenated, e.g. `envelope-id`, not
  `message-envelope/id`). `canonical_param` form: the path-template
  `{snake_case}` rule, `^[a-z][a-z0-9_]*$`. The set is extensible by reviewed PR.
- **Rule:** a descriptor's `semantic/ref` MUST match a registered `id`; the
  aggregator and schema-gate reject an unregistered value (boundary parsers must
  not swallow corruption). New concepts are added to the registry first, in a
  reviewed change, before a descriptor may reference them — the same
  no-aliases / one-id discipline used for schema `$id`s. Alias collapse uses the
  entry's `canonical_param`; an entry without one fails the build rather than
  guessing.
- **Storage:** the registry is a single declared list
  (`node/protocol/contracts/schemas/semantic-refs.v1.json`) resolved the same way
  the schema registry resolves URNs — one source of truth, no second mini-list.

**Hard invariant — `path` and `path/params` must agree exactly.** Every
`{param}` segment in `path` has **exactly one** matching entry in `path/params`,
and every `path/params` entry names a `{param}` that appears in `path`. No
missing, no extra, no duplicate. A descriptor that violates this is rejected at
validation (not silently accepted), because otherwise the generator emits
OpenAPI with missing or surplus `parameters`. This is a schema-gate check on
`orbiplex.api-descriptor.v1`, not a runtime best-effort.

**Conflict detection uses two keys** (this refines the path/method conflict rule
above):

- *display key:* `METHOD + canonical_path`, e.g. `GET /v1/receipts/{receipt_id}`;
- *shape key:* `METHOD + path with every parameter erased to {}`, e.g.
  `GET /v1/receipts/{}`.

Rules:

- same display key → may merge only if the operations are **compatible**,
  defined explicitly as: identical `request.schema_ref` (or both none), identical
  `x-orbiplex-effect`, and response sets that do not collide (same status code
  must carry the same response `schema_ref`; otherwise it is a conflict, not a
  merge). Any other divergence on the same display key is a conflict;
- same shape key, different display key (e.g. `{receipt_id}` vs `{id}`) →
  **conflict**, unless the parameters carry the same `semantic/ref` and an
  explicit alias rule is declared — a renamed parameter is the same OpenAPI path
  shape and must not silently split;
- a `protocol`/`operator` host-exposed conflict is **fail-closed**;
- `developer`/`internal-loopback` may downgrade to a warning, but never inside
  one public OpenAPI document without `surface`/`include` separation.

**Alias emission rule (OpenAPI cannot hold two equivalent templated paths).**
Because OpenAPI 3.1 forbids two paths that differ only in parameter name, an
allowed alias is a **descriptor-level convenience only**, never two paths in the
output. When an alias is permitted (same `semantic/ref`, explicit alias rule),
the aggregator MUST collapse the aliased entries into **exactly one** canonical
path in the output. The winning parameter name is deterministic: the
`canonical_param` declared for that `semantic/ref` entry in the vocabulary
registry (e.g. `record-id` → `record_id`); if the entry declares no
`canonical_param`, the build fails rather than guessing. Aliases therefore live in lint/migration tooling and in
the merge step, never as two `paths` entries. There is no MVP need to introduce
aliases at all — prefer making producers emit the one canonical name.

Tooling stance: emit canonical descriptors directly (best for MVP). A
`normalize_path_pattern(":id" → "{id}")` helper is allowed **only** as a
lint/migration aid; a descriptor written into the system is already canonical. A
path AST (`segments: [{static}, {param}]`) rendered to OpenAPI is the cleanest
long-term shape if the surface grows, but is overkill for MVP. Framework-native
extraction is rejected — the routing is not uniformly framework-based and the
projection must stay runtime-agnostic.

This keeps the projection free of Rust/Python routing detail: the canonical
template is the data both sides agree on, and the aggregator validates rather
than guesses.

## Reference Flow

```text
component (Rust route family | Python shared handler | external module)
  -> emits orbiplex.api-descriptor.v1
       (generated from route<->schema binding, or manually registered inline)
daemon aggregator
  -> collects descriptors via the existing init/health seam
  -> resolves schema_ref against the canonical schema registry (2020-12)
  -> assembles one OpenAPI 3.1 document
  -> GET /v1/openapi.json  (+ GET /v1/docs Swagger UI)
developer / third-party client author
  -> browses surface and generates a client
  -> contract still lives in schemas + semantics, not in this view
```

## Phased Implementation

1. **Descriptor contract + schema-gate fixtures.** Define
   `orbiplex.api-descriptor.v1` in `orbidocs/doc/schemas`, mirror to
   `node/protocol/contracts/schemas`, with positive/negative fixtures.
2. **Per-language generation source.** Python: a declarative shared route table
   in the shared handler (`InquiriumAdapterHandler`, bounded HTTP server) that
   both dispatches and generates the descriptor, so every adapter contributes for
   free. Rust: an explicit data registry co-located with the daemon route
   dispatch, with a coverage test that registry and dispatch stay in sync. Both
   are read at runtime (no build-time codegen).
3. **Daemon aggregator + endpoint.** Collect the `api/surface` section from the
   init reports the daemon already gathers during supervision (resolved seam),
   resolve `schema_ref`, serve `GET /v1/openapi.json`. Include only
   `protocol`-surface entries by default; carry non-`protocol` `surface` entries
   only when opted in (resolved scope). The dedicated `GET /v1/api-descriptor` is the
   fallback for components that do not serve an init report.
4. **Manual registration path.** Ingest operator/config-supplied descriptors of
   the same shape for external components; merge identically. Inline schemas in
   manual descriptors are validated through schema-gate (positive/negative
   fixtures), not trusted as-is.
5. **Swagger UI** at `GET /v1/docs`, dev/operator-gated and descriptive-only.
6. **Drift/contract test.** Assert every `schema_ref` URN resolves, every inline
   schema validates through schema-gate, the `path`↔`path/params` invariant
   holds, and registry↔dispatch parity holds — **without live-probing mutating
   routes** (response-shape only in an isolated harness).

### Sequencing and Rollout

- **`P068-01` + `P068-09` land together** (descriptor schema + the
  `middleware-module-report` extension): the contribution shape and the field
  that carries it are one change set.
- **`P068-10` (URN resolution) is gated on the `$id` backfill** (`P068-15`): a
  few canonical schemas still carry URL-form `$id`
  (`https://schemas.orbiplex.org/…`, e.g. `inac-control.v1`, `memarium-blob.v1`)
  instead of the `urn:orbiplex:schema:<name>:v<n>` convention; the resolver would
  silently miss them. Normalize them in a separate commit **before** wiring the
  resolver.
- **Bootstrap before hooking dispatch.** Start the `protocol` surface from a
  small whitelist of stable endpoints declared as sidecar data
  (`<data-dir>/api-descriptors/*.json`), not an immediate hook into the Rust/
  Python dispatch. This lets the mechanism land incrementally; the generated
  registry/table replaces the sidecar per component as it migrates.

## Trade-offs

Benefits:

- one cross-cutting, testable view across Rust + Python surfaces;
- single source of truth preserved (bodies `$ref` the canonical schemas);
- one runtime, not N Swagger servers (thin-core preserved);
- live drift detection over the HTTP surface.

Costs:

- descriptor generation must hook the route registration to stay non-rotting;
- the manual escape hatch is a (bounded) rot surface, mitigated by a contract
  test;
- OpenAPI describes shape only — risk that a reader mistakes it for the full
  contract, mitigated by the explicit non-authoritative banner.

Constraints:

- OpenAPI 3.1 (for JSON Schema 2020-12 `$ref` without conversion);
- projection is descriptive; no secret/sealed-internal leakage.

## Failure Modes and Mitigations

| Failure | Mitigation |
| --- | --- |
| Projection becomes a second source of truth. | `schema_ref` only; copying a canonical body is forbidden and caught by the contract test. |
| Hand-maintained descriptors drift. | Generated entries derive from route↔schema binding; only inline external entries are manual, and a contract test checks them. |
| Secret/token/internal leaks into the public view. | Descriptors carry descriptive auth labels, never material; output scrubbed; review gate. |
| Readers treat OpenAPI as the contract. | Explicit non-authoritative banner; `x-orbiplex-authority: descriptive-only`; authority/classification/fail-closed stay in schemas + solution docs. |
| Per-component Swagger servers proliferate. | Aggregation is daemon-only; components contribute data, not runtime. |
| Registry/table becomes a hand-list beside the router. | The table the dispatch reads **is** the descriptor source; coverage test enforces registry↔dispatch parity. |
| Loopback endpoint published as public client API. | `path` = host-exposed; raw `loopback/path` only for `developer`/`internal-loopback`; default projects `protocol` only. |
| Live drift test causes side effects on mutating routes. | Coverage = parity without effect; response-shape only in isolated harness; mutating routes never live-probed. |
| Two components claim the same `method+path`. | Fail-closed for protocol/operator; warn for developer/internal; never silent last-writer-wins. |
| Second OpenAPI model drifts from descriptors. | Static files (Agora YAML) retired or repurposed as test oracle; no parallel living contract. |

## Resolved Decisions

1. **Seam — RESOLVED: init-report section.** The descriptor is carried as an
   `api/surface` section inside the existing `/v1/middleware/init` report for
   components that already report. A dedicated `GET /v1/api-descriptor` endpoint
   is the fallback only for components that do not serve an init report. Zero new
   endpoints for the common case; the aggregator reads `api/surface` from the
   reports it already collects during supervision.
2. **Daemon control-plane scope — RESOLVED: stable protocol by default, internal
   opt-in.** The projection covers the stable/versioned protocol surface by
   default; fast-churn internal control-plane endpoints are excluded unless a
   component (or the daemon route family) explicitly opts an entry in
   (a non-`protocol` `surface` value on the descriptor entry, e.g. `operator` /
   `developer` / `internal-loopback`). A component may surface
   an internal endpoint it judges important to expose, but the default keeps the
   thin core uncluttered and stable for third-party client authors.
3. **Generation tooling — RESOLVED: explicit data registry (Rust) + shared route
   table (Python), runtime assembly.** The descriptor is derived from the
   route↔schema binding and lives next to the route definition; the mechanism is
   internal per language, the emitted `api/surface` section is uniform.
   - *Rust daemon:* a single explicit data registry co-located with the route
     dispatch listing `{method, path, request_schema_id, response_schema_ids,
     auth, tags, surface}`, with a coverage test. **The daemon dispatch is a
     multi-layer tree, not one match arm** — path-prefix → file → method →
     handler across `endpoint_routes/*` (identity, messaging, common, …),
     `host_capabilities_host.rs::dispatch`, `catalog_host.rs`,
     `peer_runtime_host.rs::dispatch_peer_message_request`, and the
     middleware inbound-local dispatch in `lib.rs`. The coverage test is
     therefore **hierarchical**: registry↔dispatch parity per layer, not a
     single flat router check. No third-party derive crate (the hand-rolled
     router would have to be restructured toward a framework) — "data, not macro
     magic", consistent with the imperative→data preference.
   - *Python middleware:* a declarative shared route table
     `(method, path-pattern) -> {handler, schema ids, surface}` in the shared
     handler; `do_GET`/`do_POST` dispatch from it **and** the descriptor
     generates from it, so dispatch and description cannot drift (one table, two
     uses). The current `if path == …` chains are refactored into the table.
     Operational authoring guidance and copyable examples live in
     `doc/ops/faq/middleware-faq.en.md` / `doc/ops/faq/middleware-faq.pl.md`.
   - *Assembly is runtime, not build-time codegen:* the registry/table is read
     at startup and the aggregator merges generated descriptors with
     runtime-registered manual external descriptors at the same point — runtime
     is where the generated and manual paths converge.
   - Rejected: per-adapter hand-written descriptor files for generated endpoints
     (the rot path; allowed only as the manual escape hatch for external
     components); deriving solely from scattered schema-gate validator calls
     (incomplete — usable only as a cross-check).

## Open Questions

None at this time. The previously-open path-pattern normalization question is
resolved in *Path Template Normalization* (canonical `{snake_case}`, enforced
both sides, two-key conflict detection). New questions are expected to surface
when the Rust registry coverage test and the Python table refactor land.

## Next Actions

The MVP and post-MVP closure slice (P068-01..17) has landed; see Implementation
Tracking. The remaining, forward-looking work:

1. **Broaden Rust route registry coverage opportunistically.** Extend the Rust
   registry beyond the read-only MVP layer to other dispatch layers as those
   routes are made stable enough for projection, under the existing hierarchical
   coverage test.
2. **Keep future middleware adapters route-table-derived.** New Python
   middleware should use the shared descriptor helper rather than re-declaring a
   parallel OpenAPI surface by hand.
3. **Replace explicit untyped response placeholders.** The five Python
   contributors now make untyped response debt explicit, but their routes should
   gain concrete `response_schema_ref` or `response_inline_schema` values as
   those middleware contracts freeze.
4. **Swagger UI offline/vendor hardening (P068-06a follow-up, low priority).**
   `/v1/docs` is live but still loads assets from a public CDN (unpkg) — the
   only spot the node reaches the internet. The stopgap is done: exact version +
   SRI `integrity=`, nonce-based `script-src`, and `frame-ancestors 'none'`.
   Full hardening later: vendor the pinned dist from the daemon origin with a
   strict `self`-only CSP (or a smaller Redoc bundle), restoring
   offline/air-gapped coherence and removing the third-party beacon. Driver is
   offline-first consistency, not acute exploitability.

## Implementation Tracking

Status values: `pending`, `partial`, `done`, `deferred`.

| ID | Work item | Status | Notes |
| --- | --- | --- | --- |
| P068-01 | `orbiplex.api-descriptor.v1` schema + schema-gate fixtures (incl. `path`↔`path/params` invariant validation) | done | landed with P068-09; `schema_ref` xor `inline` per response; dynamic `path`↔`path/params` invariant is enforced by typed boundary validation |
| P068-02 | Python shared route table (dispatch + descriptor from one table); Inquirium adapter seam first | done | landed for the shared Inquirium adapter handler; `/v1/inquirium/invoke` reports neutral invoke/response `schema_ref` bindings, while the OpenAI-compatible shim remains inline compatibility shape; simulator inherits the same surface; Dator, recovery-service, Agora verifier, Sensorium OS, and offer-catalog now contribute `api/surface` through the shared Python helper; untyped response placeholders are now explicit opt-in debt rather than a hidden helper fallback |
| P068-03 | Rust daemon explicit route registry + **hierarchical** coverage test | done | landed for the read-only/control MVP layer as `READ_ONLY_API_SURFACE_ROUTES` co-located with `read_only_health_response`; daemon descriptor generation and registry-size/protocol-surface tests prevent a parallel hand list |
| P068-04 | Daemon aggregator + `GET /v1/openapi.json` (OpenAPI 3.1; `schema_ref` URN → local `#/components/schemas`) | done | daemon-owned runtime projection; `?include=` supports non-default surfaces, `?include=configured` includes persisted configured reports, and direct HTTP response carries `Cache-Control: no-store` |
| P068-05 | Manual-registration path for external components | done | daemon ingests validated JSON sidecars from `<data_dir>/api-descriptors`; invalid sidecars are quarantined as projection warnings without leaking absolute paths |
| P068-06 | Optional Swagger UI `GET /v1/docs` | done | landed as an operator-gated descriptive shell; the daemon embeds the generated OpenAPI projection server-side, no daemon authtok is present in JS, and Swagger request execution is disabled |
| P068-06a | Swagger UI external-asset hardening | partial | stopgap landed: `swagger-ui-dist@5.32.6` is pinned, both CDN assets carry SHA-384 SRI plus `crossorigin=anonymous`, inline bootstrap uses a per-request CSP nonce, and `frame-ancestors 'none'` blocks embedding; remaining full hardening is to vendor the pinned dist from daemon origin + strict `self`-only CSP (or a smaller Redoc bundle), restoring offline/air-gapped coherence and removing the third-party beacon |
| P068-07 | Drift/contract test — registry↔dispatch parity (no effect) + **inline schemas validated via schema-gate** + `path`↔`path/params` invariant + response-shape in isolated harness only; never probe mutating routes live | done | schema-gate covers descriptor fixtures and nested module reports; typed validation enforces `path`↔`path/params`; daemon tests cover registry-derived descriptor and conflict policy without probing mutating routes |
| P068-08 | Non-authoritative banner + privacy scrub | done | projection carries `x-orbiplex-authority: descriptive-only`, descriptive auth labels only, no token values, no sealed payloads, and sidecar warnings use filenames rather than local absolute paths |
| P068-09 | Extend `middleware-module-report.schema.json` with optional additive `api/surface` (sibling of `adapter_manifest`) → `orbiplex.api-descriptor.v1` (absence legal); keep `additionalProperties: false` + explicit property; update schema-gate fixtures; verify all in-flight reports still validate; CI signal if anyone adds a field without a PR here | done | landed with P068-01; `api/surface` is optional and absent reports remain valid |
| P068-10 | Freeze `schema_ref` resolution: URN `$id` → single registry → local `#/components/schemas`; no aliases, no filename refs | done | daemon projection resolves through `SCHEMA_REGISTRY`; tests verify each embedded schema `$id` matches its URN |
| P068-11 | `surface` taxonomy (`protocol`/`operator`/`developer`/`internal-loopback`/`external-component`) + host-exposed vs `loopback/path` separation | done | descriptor schema and typed DTOs freeze the taxonomy; projection includes only `protocol` by default, with opt-in `include=` for other surfaces; middleware-direct loopback paths stay explicit metadata |
| P068-12 | Path/method conflict policy: explicit "compatible" rule (same `request.schema_ref`, same `x-orbiplex-effect`, non-colliding responses); fail-closed for protocol/operator | done | aggregator rejects shape conflicts and incompatible duplicate contributions; compatible duplicates collapse with a warning; unit tests cover semantic drift rejection |
| P068-13 | Agora `agora-record-relay.v1.openapi.yaml`: retire or repurpose as aggregator test oracle/fixture; not a parallel contract | done | source docs now call the YAML a legacy test/reference fixture; canonical OpenAPI projection is daemon-owned at `GET /v1/openapi.json` |
| P068-14 | Canonical path templates (`{snake_case}`) enforced both sides + `path/params` data + two-key (display/shape) conflict detection | done | typed descriptor validation rejects framework-native/partial-segment params and enforces exact `path`↔`path/params`; aggregation tracks both display and parameter-erased shape keys |
| P068-15 | Backfill non-URN schema `$id`s to `urn:orbiplex:schema:<name>:v<n>` (`inac-control.v1`, `memarium-blob.v1`, audit the full set) | done | prerequisite for P068-10 complete; audited `node/protocol/contracts/schemas` and `orbidocs/doc/schemas` for URL-form `$id`s |
| P068-16 | `semantic-refs.v1.json` vocabulary registry for `path/params.semantic/ref`: entries `{id, canonical_param}` (`participant-id`→`participant_id`, `record-id`→`record_id`, `envelope-id`→`envelope_id`, `question-id`→`question_id`, `contract-id`→`contract_id`); `id` form `^[a-z][a-z0-9-]*$`, `canonical_param` form `^[a-z][a-z0-9_]*$`; a present `semantic/ref` MUST match a registered `id`, else validation fails; alias collapse emits `canonical_param` | done | landed with `semantic-refs.v1.json` mirrored to node/orbidocs, typed registry validation, schema-gate fixtures for unknown/bad refs, and daemon alias normalization before OpenAPI merge |
| P068-17 | `x-orbiplex-classification` references `classification.v1` (`schema_ref` + enum `tier`), never a free string | done | descriptor schema and typed validation require `schema_ref = urn:orbiplex:schema:classification:v1` and `tier ∈ {Personal, Community, Public}` |
