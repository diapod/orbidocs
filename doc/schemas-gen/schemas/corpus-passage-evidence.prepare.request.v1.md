# Corpus Passage Evidence Preparation Request v1

Source schema: [`doc/schemas/corpus-passage-evidence.prepare.request.v1.schema.json`](../../schemas/corpus-passage-evidence.prepare.request.v1.schema.json)

Request to fix the evidence one Agent passage will read (P094-023a). It names the Corpus inference-Flow binding of the passage and each wanted item by exact ref and digest; `latest` is never an input. The host reads every item as the binding's Room subject and answers an immutable manifest, or refuses.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-passage-evidence.prepare.request.v1` |  |
| [`inference-flow-binding/ref`](#field-inference-flow-binding-ref) | `yes` | string |  |
| [`projection`](#field-projection) | `yes` | ref: `#/$defs/projection` |  |
| [`bytes/max`](#field-bytes-max) | `yes` | integer |  |
| [`items`](#field-items) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`projection`](#def-projection) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-passage-evidence.prepare.request.v1`

<a id="field-inference-flow-binding-ref"></a>
## `inference-flow-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-projection"></a>
## `projection`

- Required: `yes`
- Shape: ref: `#/$defs/projection`

<a id="field-bytes-max"></a>
## `bytes/max`

- Required: `yes`
- Shape: integer

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-projection"></a>
## `$defs.projection`

- Shape: object
