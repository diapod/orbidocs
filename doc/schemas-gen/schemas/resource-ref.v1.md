# Resource Ref v1

Source schema: [`doc/schemas/resource-ref.v1.schema.json`](../../schemas/resource-ref.v1.schema.json)

Machine-readable schema for the generic resource identity model introduced in proposal 026. A resource reference is a typed opaque identifier used across Orbiplex to name things that records, opinions, offers, or other artifacts may refer to: URLs, products, nodes, organizations, places, workflow runs, and swarm-internal artifacts. The kind names the category, the id is opaque within that category and carries no assumed URI semantics unless the kind contract explicitly says so. This file exists so that any schema referencing proposal 026 can use a single shared definition instead of re-declaring the shape.

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`resource/kind`](#field-resource-kind) | `yes` | string | Resource kind slug. Early kinds include `url`, `ean`, `node`, `org`, `gps`. Swarm-internal kinds include `proposal`, `workflow-run`, `artifact`, `capability`. The list of kinds is open; kind contracts are registered per subsystem, not in this schema. |
| [`resource/id`](#field-resource-id) | `yes` | string | Opaque identifier within the named kind. Consumers MUST NOT assume URI, URN, or hierarchical semantics unless the kind contract explicitly says so. Canonicalization rules (Unicode NFC, no control characters, no leading or trailing whitespace) are enforced by libraries on ingest; JSON Schema expresses only the trim and non-empty constraints. |
## Field Semantics

<a id="field-resource-kind"></a>
## `resource/kind`

- Required: `yes`
- Shape: string

Resource kind slug. Early kinds include `url`, `ean`, `node`, `org`, `gps`. Swarm-internal kinds include `proposal`, `workflow-run`, `artifact`, `capability`. The list of kinds is open; kind contracts are registered per subsystem, not in this schema.

<a id="field-resource-id"></a>
## `resource/id`

- Required: `yes`
- Shape: string

Opaque identifier within the named kind. Consumers MUST NOT assume URI, URN, or hierarchical semantics unless the kind contract explicitly says so. Canonicalization rules (Unicode NFC, no control characters, no leading or trailing whitespace) are enforced by libraries on ingest; JSON Schema expresses only the trim and non-empty constraints.
