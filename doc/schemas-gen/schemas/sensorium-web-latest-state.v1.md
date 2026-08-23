# Sensorium Web Latest State v1

Source schema: [`doc/schemas/sensorium-web-latest-state.v1.schema.json`](../../schemas/sensorium-web-latest-state.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-latest-state.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`source/ref`](#field-source-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`snapshot`](#field-snapshot) | `yes` | ref: `sensorium-web-document-snapshot.v1.schema.json` |  |
| [`snapshot/digest`](#field-snapshot-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`representation`](#field-representation) | `yes` | unspecified |  |
| [`observation/id`](#field-observation-id) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-latest-state.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-snapshot"></a>
## `snapshot`

- Required: `yes`
- Shape: ref: `sensorium-web-document-snapshot.v1.schema.json`

<a id="field-snapshot-digest"></a>
## `snapshot/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-representation"></a>
## `representation`

- Required: `yes`
- Shape: unspecified

<a id="field-observation-id"></a>
## `observation/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
