# Bounded HTTP Fetch Error Codes v1

Source schema: [`doc/schemas/bounded-http-fetch-error-codes.v1.schema.json`](../../schemas/bounded-http-fetch-error-codes.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-error-codes.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`entries`](#field-entries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`code`](#def-code) | enum: `invalid-request`, `consumer-denied`, `origin-denied`, `dns-failed`, `dns-answer-limit`, `destination-denied`, `connect-failed`, `tls-failed`, `redirect-invalid`, `redirect-denied`, `redirect-limit`, `header-limit`, `compressed-body-limit`, `decompressed-body-limit`, `unsupported-content-encoding`, `timeout`, `concurrency-limit`, `artifact-store-failed`, `transport-failed` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-error-codes.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-code"></a>
## `$defs.code`

- Shape: enum: `invalid-request`, `consumer-denied`, `origin-denied`, `dns-failed`, `dns-answer-limit`, `destination-denied`, `connect-failed`, `tls-failed`, `redirect-invalid`, `redirect-denied`, `redirect-limit`, `header-limit`, `compressed-body-limit`, `decompressed-body-limit`, `unsupported-content-encoding`, `timeout`, `concurrency-limit`, `artifact-store-failed`, `transport-failed`
