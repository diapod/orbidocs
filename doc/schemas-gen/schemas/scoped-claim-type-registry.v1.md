# Scoped Claim Type Registry v1

Source schema: [`doc/schemas/scoped-claim-type-registry.v1.schema.json`](../../schemas/scoped-claim-type-registry.v1.schema.json)

Initial schema-gated registry surface for scoped-claim type definitions.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `scoped-claim-type-registry.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`registry/id`](#field-registry-id) | `yes` | string |  |
| [`entries`](#field-entries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `scoped-claim-type-registry.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-registry-id"></a>
## `registry/id`

- Required: `yes`
- Shape: string

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
