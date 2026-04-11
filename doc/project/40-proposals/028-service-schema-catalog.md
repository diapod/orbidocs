# Proposal 028: Service Schema Catalog

## Status

Draft / Under Discussion.

## Problem

`service_type` in an offer's payload is currently an opaque string.  The daemon
routes it and Arca executes it, but neither the UI nor any workflow author has
a machine-readable description of what a particular `service_type` expects in
`request/input`.

The `request/input` field is intentionally an open `JsonValue` — no inner
validation by the daemon.  This openness is a strength: it lets providers evolve
their contracts without a central registry.  But without any opt-in way to
advertise what a type accepts, every integration becomes tribal knowledge.

Consequences today:

- Workflow authors must read Arca source code to know which fields are valid.
- The step-builder UI in `workflow_definitions` hardcodes a `request_input`
  textarea with `placeholder="{}"` — no field hints, no examples.
- Two providers offering `text/redaction` may accept entirely different shapes
  with no way for a consumer to distinguish them before making a request.

## Context

`plan_schema_path` (Proposal V2) solved a related problem one layer up: the
daemon can proxy a module's per-`workflow_kind` step-field schema so that the
UI renders a structured builder instead of a raw JSON textarea.

But `plan_schema_path` describes the step envelope (which step fields exist, what
types they have) — not the domain content inside `request/input`.  The two
concerns are complementary:

- step-field schema → how to build a plan in the UI
- service schema catalog → what to put in `request/input` for each `service_type`

## Idea

Each middleware module that provides offer-services may expose a schema catalog
endpoint:

```
GET /v1/schema-catalog
```

The response is a JSON array of schema descriptors:

```json
[
  {
    "service_type":  "text/redaction",
    "schema_id":     "text-redaction.v1",
    "description":   "Redacts personally identifiable information from plain text.",
    "json_schema":   {
      "type": "object",
      "properties": {
        "text":         { "type": "string" },
        "redact_kinds": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["text"]
    },
    "examples": [
      {
        "label": "Basic redaction",
        "value": { "text": "Call me at +48 123 456 789.", "redact_kinds": ["phone"] }
      }
    ]
  }
]
```

This endpoint is purely descriptive.  No code in the daemon or the calling
client is expected to branch on the schema — it exists to guide human authors
and tool-assisted form builders.

## Registration

The daemon already maintains several proxy registries
(`WorkflowKindRegistry`, `HostCapabilityRegistry`, `LocalRouteRegistry`,
`ModuleDispatchRegistry`).  Each is a specialised `BTreeMap` rebuilt from the
module report on startup.  Adding a per-kind dedicated registry for every new
catalog would mean copy-pasting the same `rebuild()` / proxy pattern each time.

Instead, the module report gains one generic array:

```json
"catalog_endpoints": [
  { "catalog_kind": "schema", "path": "/v1/schema-catalog" }
]
```

The daemon builds a single `CatalogEndpointRegistry`
(`BTreeMap<catalog_kind, Vec<CatalogEndpointEntry>>`), rebuilt from all active
module reports, and exposes one aggregated proxy per kind:

```
GET /v1/catalog/{catalog_kind}?…
```

For this proposal, the concrete endpoint becomes:

```
GET /v1/catalog/schema?service_type=text/redaction
```

The aggregated endpoint makes it trivial for the Node UI (or an external tool)
to fetch the descriptor for whatever `service_type` appears in an offer without
knowing which module provides it.

Adding a new catalog kind in the future (e.g. `template` from Proposal 029)
requires only a new entry in `catalog_endpoints` — no new registry struct, no
new daemon handler.

## Offer-level Schema Reference

Optionally, individual offers may carry a `schema_ref` field pointing directly
to a descriptor — either a URL to the module's schema catalog or an entry
within a published community collection:

```json
{
  "service_type": "text/redaction",
  "schema_ref":   "http://127.0.0.1:7702/v1/schema-catalog#text-redaction.v1"
}
```

This is a hint, not an authority.  Consumers may ignore it.  It enables
point-to-point schema exchange without a central registry while still being
compatible with one.

## Stratification

The schema catalog idea fits naturally into a four-layer stack:

| Layer | Name | What it contains |
| :---- | :--- | :--------------- |
| 0 | **Open contract** | `request/input: JsonValue` — any shape accepted |
| 1 | **Named schemas** | per-provider `GET /v1/schema-catalog` — opt-in description |
| 2 | **Domain ontologies** | community-curated `service_type` namespaces (e.g. `text/*`, `image/*`, `audio/*`) with agreed base schemas |
| 3 | **Workflow templates** | pre-built plan definitions referencing known `service_type` values with example inputs |

A provider can stay at Layer 0 indefinitely — no breaking change.  A provider
that wants to participate in a shared ontology moves to Layer 1 voluntarily.
Layer 2 and 3 emerge from convention among participants, not from daemon-enforced
constraints.

This mirrors how the web grew: open TCP → HTTP → agreed media types → REST
conventions.  The daemon stays thin; the market builds the ontology.

## Relationship to Existing `plan_schema_path`

`plan_schema_path` (V2/V3) is orthogonal:

- `plan_schema_path` → UI knows how to build a workflow plan step-by-step.
- `catalog_endpoints[schema]` → UI (and humans) know what to put inside each
  step's `request/input`.

In practice both endpoints could be served by the same module process.
`plan_schema_path` remains a dedicated field in `workflow_kind_handlers` because
it is tightly scoped to `WorkflowKindRegistry`; the schema catalog is a
module-level, `service_type`-keyed resource and fits the generic
`catalog_endpoints` slot instead.

The Node UI step-builder could load `GET /v1/catalog/schema?service_type=…` for
the selected service type and render inline field hints inside the
`request_input` textarea or, eventually, replace it with a structured sub-form.

## UI Integration (Future)

Once the daemon exposes `GET /v1/catalog/schema?service_type=…`, the
workflow-definition form could:

1. Fetch the descriptor when a user types a `service_type` value.
2. Show `description` as a tooltip or inline help text.
3. Render `examples` as a dropdown of starter templates for the `request_input`
   field.
4. Eventually: replace the raw JSON textarea with a generated sub-form driven
   by `json_schema.properties`.

Steps 1–3 are low-cost and immediately useful; step 4 can follow the same
HTMX server-side pattern as the step-builder.

## Risks and Non-Goals

**Schema should be purely descriptive.**  The daemon must not branch on schema
content.  If a request does not match a schema, that is a business-level concern
handled inside the provider module — not a transport-level rejection by the
daemon.  Introducing validation at the daemon layer would couple the daemon to
domain knowledge and break the open-contract principle.

**No mandatory registry.**  Providers that do not declare a `schema` entry in
`catalog_endpoints` continue to work exactly as today.  The feature is entirely
opt-in.

**No schema versioning protocol (yet).**  `schema_id` carries a version suffix
by convention (e.g. `text-redaction.v1`), but there is no negotiation mechanism.
Consumers should treat the schema as advisory documentation, not as a
compatibility guarantee.

**Community ontologies are out of scope for the daemon.**  The daemon proxies
schemas; it does not curate them.  A separate orbidocs or community project is
the right home for agreed `service_type` namespaces.

## Consequences

Positive:

- Workflow authors gain machine-readable documentation for `request/input`
  shapes without changing the open-contract daemon architecture.
- Node UI can progressively enhance the step-builder without a big rewrite.
- Market participants can build a shared ontology through convention, not
  through central enforcement.
- The `catalog_endpoints` registration pattern reuses the existing
  `rebuild()`-from-module-report idiom already present in all daemon registries
  — low implementation cost, zero new structural patterns.

Trade-off:

- One more optional endpoint per provider module to maintain.
- Schema drift (provider changes shape without updating schema) is invisible to
  the daemon — consumers must handle unexpected shapes defensively regardless.

## Minimal Viable Step

1. Add `catalog_endpoints: Vec<CatalogEndpointDecl>` to `MiddlewareModuleReport`
   where `CatalogEndpointDecl` is `{ catalog_kind: String, path: String }`.
2. Daemon builds `CatalogEndpointRegistry` from active module reports on startup
   and exposes `GET /v1/catalog/{catalog_kind}` as a generic proxy.
3. Arca serves `GET /v1/schema-catalog` listing its known `service_type` values
   and declares `{ "catalog_kind": "schema", "path": "/v1/schema-catalog" }` in
   its module report.
4. No UI change required for MVP.

Proposal 029 reuses the same `catalog_endpoints` slot with
`{ "catalog_kind": "template", "path": "/v1/template-catalog" }` — the daemon
machinery is identical.
