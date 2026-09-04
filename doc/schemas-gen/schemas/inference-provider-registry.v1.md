# Inference Provider Registry V1

Source schema: [`doc/schemas/inference-provider-registry.v1.schema.json`](../../schemas/inference-provider-registry.v1.schema.json)

Bounded operator-owned display vocabulary. No credentials, endpoints, discovery or inference authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-provider-registry.v1` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`digest`](#field-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`entries`](#field-entries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-provider-registry.v1`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-digest"></a>
## `digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
