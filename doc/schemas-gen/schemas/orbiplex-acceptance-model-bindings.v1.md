# Orbiplex Acceptance Model Bindings v1

Source schema: [`doc/schemas/orbiplex-acceptance-model-bindings.v1.schema.json`](../../schemas/orbiplex-acceptance-model-bindings.v1.schema.json)

Private host-local locators binding one physical acceptance slot to exact model/runtime qualification evidence.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `orbiplex-acceptance-model-bindings.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`scope`](#field-scope) | `yes` | object |  |
| [`bindings`](#field-bindings) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`token`](#def-token) | string |  |
| [`rawDigest`](#def-rawdigest) | string |  |
| [`absolutePath`](#def-absolutepath) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `orbiplex-acceptance-model-bindings.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

<a id="field-bindings"></a>
## `bindings`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-rawdigest"></a>
## `$defs.rawDigest`

- Shape: string

<a id="def-absolutepath"></a>
## `$defs.absolutePath`

- Shape: string
