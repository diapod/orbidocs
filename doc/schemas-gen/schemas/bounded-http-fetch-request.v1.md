# Bounded HTTP Fetch Request v1

Source schema: [`doc/schemas/bounded-http-fetch-request.v1.schema.json`](../../schemas/bounded-http-fetch-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`consumer/action`](#field-consumer-action) | `yes` | string |  |
| [`method`](#field-method) | `yes` | enum: `GET`, `HEAD` |  |
| [`url`](#field-url) | `yes` | string |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-consumer-action"></a>
## `consumer/action`

- Required: `yes`
- Shape: string

<a id="field-method"></a>
## `method`

- Required: `yes`
- Shape: enum: `GET`, `HEAD`

<a id="field-url"></a>
## `url`

- Required: `yes`
- Shape: string

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object
