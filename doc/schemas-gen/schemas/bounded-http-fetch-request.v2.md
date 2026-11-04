# Bounded-http-fetch-request.v2

Source schema: [`doc/schemas/bounded-http-fetch-request.v2.schema.json`](../../schemas/bounded-http-fetch-request.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-request.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`consumer/action`](#field-consumer-action) | `yes` | string |  |
| [`method`](#field-method) | `yes` | const: `GET` |  |
| [`url`](#field-url) | `yes` | string |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
| [`conditional`](#field-conditional) | `no` | object |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-request.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

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
- Shape: const: `GET`

<a id="field-url"></a>
## `url`

- Required: `yes`
- Shape: string

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object

<a id="field-conditional"></a>
## `conditional`

- Required: `no`
- Shape: object

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`
