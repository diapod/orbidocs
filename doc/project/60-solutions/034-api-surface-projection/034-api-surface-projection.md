# API Surface Projection

API Surface Projection is the daemon-owned descriptive API map for Orbiplex
Node deployments. It aggregates daemon routes, ready supervised middleware
reports, and operator-registered external descriptors into one OpenAPI 3.1
projection.

It is intentionally a projection, not authority. Canonical authority remains in
versioned JSON Schemas, typed route/descriptor contracts, capability/passport
policy, classification policy, idempotency rules, and the owning runtime code.
The projection makes those surfaces visible and testable without creating a
second contract source.

## Status

`done`: Proposal 068 has been implemented as the hard-MVP and post-MVP API
surface projection slice for the Node workspace.

## Based On

- `doc/project/40-proposals/068-api-surface-projection.md`
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/044-inquirium/044-inquirium.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`

## Purpose

The solution provides:

- one daemon-served `GET /v1/openapi.json` projection,
- one operator-gated `GET /v1/docs` Swagger UI shell,
- one normalized component contribution shape, `orbiplex.api-descriptor.v1`,
- one schema-ref resolver from stable URN `$id` values into OpenAPI local
  components,
- one conflict policy for duplicate path/method contributions,
- one privacy boundary that keeps auth tokens, sealed payloads, and local paths
  out of the projection.

The practical user is a developer, operator, or middleware author who needs to
see the running HTTP surface without reading Rust route dispatch and Python
middleware handlers by hand.

## Contract Model

Components contribute data, not Swagger servers.

A component contribution is an `orbiplex.api-descriptor.v1` descriptor. Each
endpoint declares method, host-exposed path, optional loopback path, parameter
metadata, request binding, response bindings, surface taxonomy, auth label,
effect classification, idempotency, and descriptive-only authority.

Response/request bindings use exactly one of:

- `schema_ref` — a canonical URN `$id`, resolved through the daemon schema
  registry;
- `inline` — a local JSON Schema shape for external or not-yet-frozen surfaces.

The daemon resolves `schema_ref` values from a closed embedded registry into
local `#/components/schemas/<component-name>` entries in the emitted OpenAPI
3.1 document. Registry entries must use `urn:orbiplex:schema:<name>:v<n>` form;
filename references and URL-form aliases are not valid projection identifiers.

## Surfaces

The descriptor surface taxonomy is:

- `protocol` — stable client/protocol API, included by default;
- `operator` — operator/control plane, opt-in through projection include flags;
- `developer` — debug/dev/test surface, opt-in;
- `internal-loopback` — private middleware/supervisor loopback, opt-in;
- `external-component` — manually registered foreign component surface, opt-in.

The host-exposed `path` is the projection contract. Raw loopback ports and paths
may be described only as internal/developer metadata; they are not the public
contract unless the surface explicitly says so.

## Runtime Ownership

The daemon owns aggregation and serving:

- reads static daemon route descriptors from the daemon route registry,
- reads ready middleware `api/surface` contributions from module reports,
- optionally reads configured external descriptor sidecars from
  `<data_dir>/api-descriptors`,
- validates descriptor shape and typed path invariants,
- resolves schema references through the registry,
- detects path-shape and method conflicts,
- emits OpenAPI 3.1 JSON and the Swagger UI shell.

Middleware and external components do not run their own Swagger servers for
Orbiplex projection. They publish small descriptor data and let the daemon own
the cross-component view.

## Conflict Policy

Duplicate path/method contributions are compatible only when they preserve the
same schema reference, effect, and non-colliding response bindings. Protocol and
operator conflicts fail closed. Compatible duplicates collapse with a warning;
incompatible duplicates are rejected from the projection.

Path parameters use canonical `{snake_case}` syntax. Optional semantic refs must
come from the `semantic-refs.v1` vocabulary, allowing semantically identical
aliases to collapse only when the registry says they are equivalent.

## Security and Privacy

The projection is descriptive-only:

- no daemon authtok reaches Swagger UI JavaScript,
- auth is expressed as labels such as `operator-session` or `module-authtok`,
  never as token material,
- sidecar warnings do not include local absolute paths,
- sealed payloads and raw request bodies are not embedded,
- `/v1/docs` is operator-gated, no-store, read-only, and disables request
  execution,
- external Swagger UI assets are exact-version pinned and protected by SRI until
  the bundle is vendored from daemon origin.

## Implemented Contributors

The current Node implementation projects:

- daemon read-only/control MVP routes,
- Inquirium adapter invoke/response surfaces,
- Dator, recovery-service, Agora verifier, Sensorium OS, and offer-catalog
  middleware module reports,
- shared middleware status/decision response schemas,
- Artifact Delivery admission response schema,
- offer-catalog query/status response schemas,
- deferred-operation status schema,
- manually registered external descriptor sidecars.

Module-local or not-yet-frozen response shapes remain inline until their narrow
contracts become stable enough to promote into canonical schemas.

## Implementation References

Reference implementation lives in the Node repository:

- `node:daemon/src/api_surface_projection.rs`
- `node:middleware/src/api_surface.rs`
- `node:middleware/schemas/middleware-module-report.schema.json`
- `node:middleware-modules/lib/api_surface.py`
- `node:protocol/contracts/schemas/orbiplex.api-descriptor.v1.schema.json`
- `node:protocol/contracts/schemas/semantic-refs.v1.json`
- `node:protocol/contracts/schemas/classification.v1.schema.json`

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Hand-maintained projection drifts from dispatch | derive daemon routes from route registry and middleware routes from route tables used by dispatch |
| Components create parallel Swagger servers | daemon is the only aggregation and serving runtime |
| `schema_ref` points to a filename or URL alias | schema registry accepts only `urn:orbiplex:schema:<name>:v<n>` form |
| OpenAPI appears authoritative for policy | projection carries descriptive-only authority labels and points back to schemas/solutions |
| Sensitive local state leaks into docs | scrub tokens, sealed payloads, absolute paths, and raw private payloads |
| External descriptors rot | validate sidecars, quarantine invalid entries as warnings, and keep them opt-in |

## Open Questions

- Whether `/v1/docs` should vendor Swagger UI assets from daemon origin for
  offline/air-gapped deployments.
- How far to broaden daemon route-registry coverage beyond the current stable
  protocol/operator subset.
- Which remaining inline middleware response shapes deserve promotion into
  canonical schemas.

## Next Actions

1. Vendor the pinned Swagger UI bundle if offline-first deployment becomes a
   release requirement.
2. Keep new middleware route surfaces route-table-derived and schema-bound.
3. Promote additional inline response schemas only after their semantics become
   integration dependencies.

## Capability Catalog

- `034-api-surface-projection-caps.edn`
