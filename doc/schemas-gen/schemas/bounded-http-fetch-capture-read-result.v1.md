# Bounded-http-fetch-capture-read-result.v1

Source schema: [`doc/schemas/bounded-http-fetch-capture-read-result.v1.schema.json`](../../schemas/bounded-http-fetch-capture-read-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-capture-read-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`body/digest`](#field-body-digest) | `yes` | string |  |
| [`body/size-bytes`](#field-body-size-bytes) | `yes` | integer |  |
| [`offset`](#field-offset) | `yes` | integer |  |
| [`bytes/base64`](#field-bytes-base64) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-capture-read-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-body-digest"></a>
## `body/digest`

- Required: `yes`
- Shape: string

<a id="field-body-size-bytes"></a>
## `body/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-offset"></a>
## `offset`

- Required: `yes`
- Shape: integer

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `yes`
- Shape: string
