# Proposal 029: Workflow Template Catalog

## Status

Draft / Under Discussion.

## Problem

The market has two sides.

**Buyers** (workflow authors) need to know: which `workflow_kind` to use, which
`service_type` values compose into a useful pipeline, and what to put in each
step's `request/input`.

**Sellers** (offer providers) need to know: how to configure and publish an
offer for a given `service_type` so that buyers can find and use it.

There is currently no place to save a working plan or a working offer
configuration as a reusable starting point, no way to share that starting point
with other participants, and no discovery surface for finding templates that
others have published.

## Idea

Two complementary stores:

1. **Local template store** — templates saved on the node, associated with a
   participant identity.  Acts as a personal collection of "in-use" or
   "favourites" blueprints for both consuming and providing services.

2. **Public template catalog** — an optional network service (implemented by
   the same module family as the offer catalog) that participants can browse to
   find templates, download them into their local store, and optionally publish
   their own.

The two stores are independent layers.  A node without a catalog connection
still has a fully functional local store.

## Template Kinds

There are three kinds of templates, covering both sides of the market:

- `workflow` — buyer side, full plan skeleton
- `step` — buyer side, single-step `request/input` recipe
- `offer` — seller side, offer configuration starting point

### Workflow template

A full plan skeleton: `workflow_kind`, an ordered list of steps each with
`service_type` and default `request/input`.  It is the starting point for a
new `WorkflowDefinition`.

```json
{
  "template_id":   "redact-then-summarise.v1",
  "template_kind": "workflow",
  "workflow_kind": "service-order-orchestration",
  "label":         "Redact then summarise",
  "description":   "Two-step text pipeline: PII redaction followed by abstractive summary.",
  "plan": {
    "steps": {
      "redact": {
        "depends_on":  [],
        "service_type": "text/redaction",
        "request_input": { "redact_kinds": ["phone", "email"] }
      },
      "summarise": {
        "depends_on":  ["redact"],
        "input_from":  "redact",
        "service_type": "text/summary",
        "request_input": { "max_sentences": 3 }
      }
    }
  }
}
```

### Step template

A single-step descriptor: `service_type` and a default or example
`request/input` map.  It answers "what do I put in this field?" without
requiring a full workflow context.  This complements the per-provider schema
descriptor from Proposal 028 (`/v1/schema-catalog`): Proposal 028 describes
the shape; a step template is a named, human-curated example of using that
shape.

```json
{
  "template_id":   "redact-phone-email.v1",
  "template_kind": "step",
  "service_type":  "text/redaction",
  "label":         "Redact phone numbers and email addresses",
  "description":   "Standard PII redaction covering phone and email fields.",
  "request_input": { "redact_kinds": ["phone", "email"] }
}
```

Step templates have an independent lifecycle: users create them by saving any
step from a workflow definition ("Save as step template") or by authoring them
manually.  They are not derived from the provider's schema catalog, though a
UI may offer to pre-fill a new step template from a schema catalog entry.

### Offer template

A starting-point configuration for publishing an offer for a given
`service_type`.  It answers "how do I configure my Arca offer for
`text/redaction`?" without the provider needing to know what buyers expect from
first principles.

```json
{
  "template_id":        "text-redaction-offer.v1",
  "template_kind":      "offer",
  "service_type":       "text/redaction",
  "label":              "Standard text redaction offer",
  "description":        "Covers phone, email and name redaction. Suitable for document pre-processing pipelines.",
  "request_input_hints": {
    "redact_kinds": ["phone", "email", "name"]
  }
}
```

`request_input_hints` is purely documentary — the same open `JsonValue` as
`request/input` on a workflow step.  It shows what buyers typically send for
this `service_type`, helping a provider configure their module correctly.

**Offer templates intentionally have no `capabilities` field.**  Node
capabilities (`workflow-orchestration`, `peer-messaging`, etc.) are an
infrastructure-level concept declared in the node passport; they describe what
a node can do at the protocol level.  Service-level features of an offer
(which variants of `redact_kinds` are supported, which languages, which file
formats) live in the provider's schema catalog entry (Proposal 028) and in the
`request_input_hints` of the offer template itself.  Conflating the two
namespaces would couple domain semantics to infrastructure routing — a clear
case of *complecting*.

## Local Template Store

The daemon stores templates in the commit log under a per-participant namespace:

```
state/workflow-template/{participant_id}/{template_id}
```

Record type: `daemon/workflow-template.v1`.

```rust
pub struct WorkflowTemplateRecord {
    pub template_id:          String,
    pub template_kind:        String,        // "workflow" | "step" | "offer"
    pub participant_id:       String,
    pub workflow_kind:        Option<String>, // workflow templates only
    pub service_type:         Option<String>, // step + offer templates only
    pub label:                String,
    pub description:          String,
    pub plan:                 Option<serde_json::Value>, // workflow templates
    pub request_input:        Option<serde_json::Value>, // step templates
    pub request_input_hints:  Option<serde_json::Value>, // offer templates
    pub deleted:              bool,
    pub created_at:           String,
    pub updated_at:           String,
}
```

### Daemon REST endpoints

```
GET    /v1/workflow-templates
       ?participant_id=…&kind=workflow|step|offer&service_type=…

POST   /v1/workflow-templates
PUT    /v1/workflow-templates/:id
DELETE /v1/workflow-templates/:id
```

Response shape mirrors `WorkflowDefinitionSnapshot`: a flat view without the
`deleted` field.

## Public Template Catalog

A module that provides a template catalog declares it via the generic
`catalog_endpoints` array introduced in Proposal 028:

```json
"catalog_endpoints": [
  { "catalog_kind": "template", "path": "/v1/template-catalog" }
]
```

The daemon's single `CatalogEndpointRegistry` (built from all active module
reports) proxies the request to the right module:

```
GET  /v1/catalog/template?q=…&kind=workflow|step|offer&service_type=…
POST /v1/catalog/template/publish
```

No new registry struct or handler is needed in the daemon — the same
`rebuild()` / proxy loop that handles `catalog_kind: "schema"` from Proposal
028 handles `"template"` automatically.

The catalog module exposes on its own loopback address:

```
GET  /v1/template-catalog?q=…&kind=workflow|step|offer&service_type=…
POST /v1/template-catalog        (publish — requires auth token or participant passport)
```

Download flow: UI calls `GET /v1/catalog/template` → presents results → user
selects → daemon `POST /v1/workflow-templates` (saves locally) → template
appears in the local store.

Publish flow: from the local store management view the user clicks **Share** →
Node UI `POST /v1/catalog/template/publish` (daemon proxies to catalog module)
→ template becomes visible to other catalog subscribers.

The catalog module is the same process family as the offer catalog (e.g. Dator).
Enabling it is a configuration flag.  A node without it loses discovery but
keeps the local store.

## UI Flows

### `/workflow-definitions/create` — template picker

- A **Load from template** dropdown (or panel) lists locally stored workflow
  templates, filtered by `workflow_kind` if one is already selected.
- Selecting a template pre-fills the form: label, steps, `request_input` defaults.
- A **Search catalog** button opens a search panel that queries
  `GET /v1/catalog/template?kind=workflow`.  Results can be previewed and
  downloaded into the local store in one click.

### Step-level save

Each step row in the step-builder has a **Save step** button (distinct from the
form submit).  Clicking it opens a small inline form (label, description) and
POSTs to `/v1/workflow-templates` as `template_kind: "step"`.  No page
navigation — HTMX swap of a confirmation badge within the step block is
sufficient.

### `/workflow-templates` — local store management

A new top-level page in Node UI:

- Three tabs: **Workflow templates** / **Step templates** / **Offer templates**.
- Each row: label, kind/service_type, last updated, buttons: **Load**, **Edit**,
  **Share**, **Delete**.
- **Share** is visible only when a catalog module is connected (daemon signals
  this via a presence flag in `/v1/status` or similar).
- **Load** from the workflow template tab navigates to `/workflow-definitions/create`
  with `?template_id=…` pre-selected.
- **Load** from the offer template tab navigates to the offer creation form
  (future) with `?template_id=…` pre-selected.

## Participant Association

Templates are stored with `participant_id` explicitly so that:

- the local store is multi-tenant-ready without a schema migration,
- future sync or export operations have a clear ownership key,
- the UI can filter the list to the node's own participant without leaking
  templates across participants if multiple are ever added to one node.

Today a node has exactly one participant (the operator).  The participant_id is
taken from the node's configured identity; no user-facing selection is needed yet.

## Relationship to Proposal 028 and Re-use of Existing Abstractions

| Proposal 028 (`schema`) | This proposal (`template`) |
| :--- | :--- |
| Machine-readable description of `request/input` fields | Human-curated named examples and reusable defaults |
| Published by the provider module (Arca, etc.) | Published by any participant |
| Authoritative for the provider's contract | Informational — "this worked for me" |
| Proxied at `GET /v1/catalog/schema` | Proxied at `GET /v1/catalog/template` |
| Drives structured form generation | Drives template picker and step-save UX |

Both catalogs declare themselves via the same `catalog_endpoints` array in the
module report and are proxied by the same `CatalogEndpointRegistry` handler in
the daemon.  They can coexist in the same catalog module process; they are
separate endpoints with different semantics.

### Re-use of the `catalog` crate

The daemon already ships a `catalog` crate with three generic traits:

```
CatalogRecord          // id, sequence_no, expiry, validate
CatalogStore<T>        // upsert / get / get_active / list / expire_stale
CatalogPredicate<T>    // matches + limit
```

and a ready `InMemoryCatalog<T>` implementation.  The offer catalog uses this
today (`ServiceOfferRecord` + `OfferFilter`).

Two re-use opportunities for this proposal:

1. **Daemon-side cache of remote catalog results.** When the daemon proxies
   `GET /v1/catalog/template`, it may cache the response in an
   `InMemoryCatalog<WorkflowTemplateCacheRecord>` with TTL, so repeated queries
   do not always hit the catalog module.  `WorkflowTemplateCacheRecord` just
   needs to implement `CatalogRecord`.

2. **Catalog module storage.** Dator already stores local offers in its own
   SQLite.  A `template` catalog extension of Dator can reuse the same DB with
   a `local_templates` table, and expose a `SqliteCatalog<WorkflowTemplateRecord>`
   if a persistent `CatalogStore<T>` backend is eventually extracted from the
   in-memory one.

The local template store on the daemon side (commit-log persistence, CRUD via
REST) is intentionally separate from `CatalogStore<T>` — it is a user-owned
mutable record, not an ephemeral cache.

## Market Symmetry

The three template kinds close the buyer–seller loop:

| Template kind | Market side | Answers the question |
| :------------ | :---------- | :------------------- |
| `step`        | Buyer       | What do I put in `request/input` for this `service_type`? |
| `workflow`    | Buyer       | How do I compose multiple steps into a pipeline? |
| `offer`       | Seller      | How do I configure and publish an offer for this `service_type`? |

A provider who downloads a `step` template for `text/redaction` can see exactly
what buyers send — and use that to validate their own Arca configuration.  A
buyer who downloads an `offer` template for `text/redaction` can see what
providers typically expose — and use that to fill `request/input` with
confidence.  The templates are informational bridges, not contracts.

## Stratification

```
Layer 0  open request/input JsonValue              (no schema, no template)
Layer 1  provider schema catalog (028)             (machine-readable field descriptions)
Layer 2  step + offer templates in local store     (curated examples per service_type)
Layer 3  workflow templates in local store         (full plan skeletons)
Layer 4  public template catalog                   (shared, searchable, community-curated)
```

Each layer is optional and additive.  The daemon stays thin and convention-driven;
the market builds the ontology.

## Risks and Non-Goals

**Templates are not authoritative.**  A template's `request/input` may be
outdated relative to what a provider currently accepts.  The daemon must never
validate `request/input` against a template schema — this would reintroduce
central coupling.

**No versioning protocol in MVP.**  `template_id` carries a version suffix by
convention; there is no negotiation or compatibility check.

**No access control on the public catalog in MVP.**  Anyone connected to a
catalog-enabled module can publish.  Spam and quality control are out of scope
for the daemon and Node UI; they belong to the catalog module's own policy layer.

**Step and offer templates are not the same as `service_type` namespaces.**
Community ontologies (Layer 2 from Proposal 028) require a separate governance
discussion; this proposal is limited to tooling.

**Offer templates must not encode pricing or SLA expectations.**  If they did,
they would become de-facto standards that disadvantage smaller providers.
`request_input_hints` describes what buyers typically send; it says nothing
about what a provider must charge or guarantee.

## Minimal Viable Step

1. `WorkflowTemplateRecord` in daemon commit log + CRUD REST endpoints.
2. `/workflow-templates` page in Node UI with local list.
3. **Load from template** dropdown in `/workflow-definitions/create`.
4. **Save step** button in the step-builder (HTMX, no navigation).

Public catalog integration (search, publish, module declaration) can follow in a
subsequent iteration once the local store UX is validated.

When that iteration arrives, the only daemon-side addition is populating
`CatalogEndpointRegistry` from `catalog_endpoints` in module reports — the same
infrastructure already needed for Proposal 028.
