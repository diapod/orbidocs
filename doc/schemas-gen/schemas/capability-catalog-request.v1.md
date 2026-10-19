# Local Capability Catalog Request v1

Source schema: [`doc/schemas/capability-catalog-request.v1.schema.json`](../../schemas/capability-catalog-request.v1.schema.json)

Agent and binding references are untrusted locators. Caller identity and effective scope are derived from authenticated host state.

## Governing Basis

- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-catalog-request.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `list`, `describe` |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`limit`](#field-limit) | `no` | integer |  |
| [`id/prefix`](#field-id-prefix) | `no` | string |  |
| [`cursor`](#field-cursor) | `no` | string |  |
| [`capability/id`](#field-capability-id) | `no` | string |  |
| [`operation/id`](#field-operation-id) | `no` | string |  |
| [`catalog/revision`](#field-catalog-revision) | `no` | string |  |
| [`include`](#field-include) | `no` | enum: `summary`, `schema` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-catalog-request.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `list`, `describe`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-limit"></a>
## `limit`

- Required: `no`
- Shape: integer

<a id="field-id-prefix"></a>
## `id/prefix`

- Required: `no`
- Shape: string

<a id="field-cursor"></a>
## `cursor`

- Required: `no`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `no`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `no`
- Shape: string

<a id="field-catalog-revision"></a>
## `catalog/revision`

- Required: `no`
- Shape: string

<a id="field-include"></a>
## `include`

- Required: `no`
- Shape: enum: `summary`, `schema`
