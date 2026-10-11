# Operator Task Order Collection v1

Source schema: [`doc/schemas/operator-task-order-collection.v1.schema.json`](../../schemas/operator-task-order-collection.v1.schema.json)

Bounded keyset read model of Dator-owned immutable orders. It exposes references, dispatch state and retained links, not private question text, request bytes or authority to execute. Corrupt rows consume their page position and yield diagnostics; they do not block healthy orders. New admissions append after earlier cursors. Reading the collection performs no reconciliation or dispatch.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-collection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`next/cursor`](#field-next-cursor) | `yes` | unspecified |  |
| [`items`](#field-items) | `yes` | array |  |
| [`diagnostics`](#field-diagnostics) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`cursor`](#def-cursor) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-collection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-next-cursor"></a>
## `next/cursor`

- Required: `yes`
- Shape: unspecified

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: string
