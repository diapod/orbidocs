# Weak-signal-original-result.local.v1

Source schema: [`doc/schemas/weak-signal-original-result.local.v1.schema.json`](../../schemas/weak-signal-original-result.local.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `weak-signal-original-result.local.v1` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`body/digest`](#field-body-digest) | `yes` | string |  |
| [`total/bytes`](#field-total-bytes) | `yes` | integer |  |
| [`offset/bytes`](#field-offset-bytes) | `yes` | integer |  |
| [`bytes/base64`](#field-bytes-base64) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `weak-signal-original-result.local.v1`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-body-digest"></a>
## `body/digest`

- Required: `yes`
- Shape: string

<a id="field-total-bytes"></a>
## `total/bytes`

- Required: `yes`
- Shape: integer

<a id="field-offset-bytes"></a>
## `offset/bytes`

- Required: `yes`
- Shape: integer

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `yes`
- Shape: string
