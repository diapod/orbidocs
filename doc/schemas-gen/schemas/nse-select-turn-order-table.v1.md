# NSE Select Turn Order Table v1

Source schema: [`doc/schemas/nse-select-turn-order-table.v1.schema.json`](../../schemas/nse-select-turn-order-table.v1.schema.json)

Deterministic target-free role-priority table for the Corpus select-turn-order hook.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-select-turn-order-table.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`policy/name`](#field-policy-name) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | const: `select-turn-order` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`role/order`](#field-role-order) | `yes` | array | A partial role priority. Listed roles are ordered first; unlisted roles retain their relative order from the host-built offer after all listed roles. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-select-turn-order-table.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-policy-name"></a>
## `policy/name`

- Required: `yes`
- Shape: string

<a id="field-hook-id"></a>
## `hook/id`

- Required: `yes`
- Shape: const: `select-turn-order`

<a id="field-hook-v"></a>
## `hook/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-role-order"></a>
## `role/order`

- Required: `yes`
- Shape: array

A partial role priority. Listed roles are ordered first; unlisted roles retain their relative order from the host-built offer after all listed roles.
