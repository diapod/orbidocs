# Sensorium Web Durable Source v1

Source schema: [`doc/schemas/sensorium-web-durable-source.v1.schema.json`](../../schemas/sensorium-web-durable-source.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-durable-source.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`source`](#field-source) | `yes` | ref: `sensorium-web-source.v1.schema.json` |  |
| [`fetch/request`](#field-fetch-request) | `yes` | ref: `bounded-http-fetch-request.v1.schema.json` |  |
| [`schedule`](#field-schedule) | `yes` | object |  |
| [`retention`](#field-retention) | `yes` | object |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-durable-source.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `sensorium-web-source.v1.schema.json`

<a id="field-fetch-request"></a>
## `fetch/request`

- Required: `yes`
- Shape: ref: `bounded-http-fetch-request.v1.schema.json`

<a id="field-schedule"></a>
## `schedule`

- Required: `yes`
- Shape: object

<a id="field-retention"></a>
## `retention`

- Required: `yes`
- Shape: object

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
