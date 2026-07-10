# Middleware Module HTTP Request v1

Source schema: [`doc/schemas/middleware-module-http-request.v1.schema.json`](../../schemas/middleware-module-http-request.v1.schema.json)

Filtered host-mediated request projection for one declared module-owned HTTP or server-html route.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-module-http-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`method`](#field-method) | `yes` | enum: `GET`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE` |  |
| [`path`](#field-path) | `yes` | string |  |
| [`query`](#field-query) | `yes` | string |  |
| [`headers`](#field-headers) | `yes` | ref: `#/$defs/headers` |  |
| [`body/encoding`](#field-body-encoding) | `yes` | const: `base64url` |  |
| [`body`](#field-body) | `yes` | ref: `#/$defs/body` |  |
| [`caller/scope`](#field-caller-scope) | `yes` | enum: `public`, `user`, `pod-user`, `operator`, `host` |  |
| [`ui/mount`](#field-ui-mount) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`headers`](#def-headers) | object |  |
| [`body`](#def-body) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-module-http-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-method"></a>
## `method`

- Required: `yes`
- Shape: enum: `GET`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE`

<a id="field-path"></a>
## `path`

- Required: `yes`
- Shape: string

<a id="field-query"></a>
## `query`

- Required: `yes`
- Shape: string

<a id="field-headers"></a>
## `headers`

- Required: `yes`
- Shape: ref: `#/$defs/headers`

<a id="field-body-encoding"></a>
## `body/encoding`

- Required: `yes`
- Shape: const: `base64url`

<a id="field-body"></a>
## `body`

- Required: `yes`
- Shape: ref: `#/$defs/body`

<a id="field-caller-scope"></a>
## `caller/scope`

- Required: `yes`
- Shape: enum: `public`, `user`, `pod-user`, `operator`, `host`

<a id="field-ui-mount"></a>
## `ui/mount`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-headers"></a>
## `$defs.headers`

- Shape: object

<a id="def-body"></a>
## `$defs.body`

- Shape: string
