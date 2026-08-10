# Bounded HTTP Fetch Artifact Read Request v1

Source schema: [`doc/schemas/bounded-http-fetch-artifact-read-request.v1.schema.json`](../../schemas/bounded-http-fetch-artifact-read-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-artifact-read-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`consumer/action`](#field-consumer-action) | `yes` | string |  |
| [`artifact/ref`](#field-artifact-ref) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`artifact/size-bytes`](#field-artifact-size-bytes) | `yes` | integer |  |
| [`bytes/max`](#field-bytes-max) | `yes` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-artifact-read-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-consumer-action"></a>
## `consumer/action`

- Required: `yes`
- Shape: string

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-artifact-size-bytes"></a>
## `artifact/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-bytes-max"></a>
## `bytes/max`

- Required: `yes`
- Shape: integer

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
