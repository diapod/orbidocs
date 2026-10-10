# Operator-task-loop-mandate.v1

Source schema: [`doc/schemas/operator-task-loop-mandate.v1.schema.json`](../../schemas/operator-task-loop-mandate.v1.schema.json)

Domain-separated operator signature over the JCS payload. The host verifies exact bytes, current authority, opening, bounds, expiry and durable revocation before every use.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-loop-mandate.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`mandate/ref`](#field-mandate-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`payload`](#field-payload) | `yes` | ref: `operator-task-loop-mandate-payload.v1.schema.json` |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-loop-mandate.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-mandate-ref"></a>
## `mandate/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: ref: `operator-task-loop-mandate-payload.v1.schema.json`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
