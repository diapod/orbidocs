# Local Capability Catalog Refusal v1

Source schema: [`doc/schemas/capability-catalog-refusal.v1.schema.json`](../../schemas/capability-catalog-refusal.v1.schema.json)

Non-disclosing local catalog refusal; carries no resource identifier or caller-supplied text.

## Governing Basis

- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-catalog-refusal.v1` |  |
| [`state`](#field-state) | `yes` | enum: `denied`, `invalid-request`, `not-found`, `stale-cursor`, `stale-revision`, `limit-exceeded`, `source-unavailable`, `projection-unavailable` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-catalog-refusal.v1`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `denied`, `invalid-request`, `not-found`, `stale-cursor`, `stale-revision`, `limit-exceeded`, `source-unavailable`, `projection-unavailable`
