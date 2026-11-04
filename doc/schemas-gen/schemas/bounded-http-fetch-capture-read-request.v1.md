# Bounded-http-fetch-capture-read-request.v1

Source schema: [`doc/schemas/bounded-http-fetch-capture-read-request.v1.schema.json`](../../schemas/bounded-http-fetch-capture-read-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-capture-read-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`consumer/action`](#field-consumer-action) | `yes` | string |  |
| [`read/binding`](#field-read-binding) | `yes` | string |  |
| [`body/digest`](#field-body-digest) | `yes` | string |  |
| [`body/size-bytes`](#field-body-size-bytes) | `yes` | integer |  |
| [`offset`](#field-offset) | `yes` | integer |  |
| [`bytes/max`](#field-bytes-max) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-capture-read-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-consumer-action"></a>
## `consumer/action`

- Required: `yes`
- Shape: string

<a id="field-read-binding"></a>
## `read/binding`

- Required: `yes`
- Shape: string

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

<a id="field-bytes-max"></a>
## `bytes/max`

- Required: `yes`
- Shape: integer
