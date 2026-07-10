# Middleware Module HTTP Response v1

Source schema: [`doc/schemas/middleware-module-http-response.v1.schema.json`](../../schemas/middleware-module-http-response.v1.schema.json)

Bounded module response projection returned through the host-mediated HTTP bridge.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-module-http-response.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | integer |  |
| [`headers`](#field-headers) | `yes` | object |  |
| [`body/encoding`](#field-body-encoding) | `yes` | const: `base64url` |  |
| [`body`](#field-body) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-module-http-response.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: integer

<a id="field-headers"></a>
## `headers`

- Required: `yes`
- Shape: object

<a id="field-body-encoding"></a>
## `body/encoding`

- Required: `yes`
- Shape: const: `base64url`

<a id="field-body"></a>
## `body`

- Required: `yes`
- Shape: string
