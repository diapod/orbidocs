# Inquirium Adapter Response v1

Source schema: [`doc/schemas/inquirium.adapter.response.v1.schema.json`](../../schemas/inquirium.adapter.response.v1.schema.json)

Neutral text-generation response emitted by middleware-hosted Inquirium adapters.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.adapter.response.v1` |  |
| [`provider`](#field-provider) | `yes` | string |  |
| [`provider_request_id`](#field-provider-request-id) | `no` | string \| null |  |
| [`model`](#field-model) | `no` | string \| null |  |
| [`output`](#field-output) | `yes` | array |  |
| [`stop_reason`](#field-stop-reason) | `no` | string \| null |  |
| [`usage`](#field-usage) | `yes` | object |  |
| [`diagnostics`](#field-diagnostics) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`outputChunk`](#def-outputchunk) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.adapter.response.v1`

<a id="field-provider"></a>
## `provider`

- Required: `yes`
- Shape: string

<a id="field-provider-request-id"></a>
## `provider_request_id`

- Required: `no`
- Shape: string | null

<a id="field-model"></a>
## `model`

- Required: `no`
- Shape: string | null

<a id="field-output"></a>
## `output`

- Required: `yes`
- Shape: array

<a id="field-stop-reason"></a>
## `stop_reason`

- Required: `no`
- Shape: string | null

<a id="field-usage"></a>
## `usage`

- Required: `yes`
- Shape: object

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-outputchunk"></a>
## `$defs.outputChunk`

- Shape: object
