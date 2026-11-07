# Whisper-case-status-request.v1

Source schema: [`doc/schemas/whisper-case-status-request.v1.schema.json`](../../schemas/whisper-case-status-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-status-request.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
| [`reader`](#field-reader) | `yes` | string |  |
| [`response/key-digest`](#field-response-key-digest) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-status-request.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-not-after"></a>
## `not-after`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string

<a id="field-reader"></a>
## `reader`

- Required: `yes`
- Shape: string

<a id="field-response-key-digest"></a>
## `response/key-digest`

- Required: `yes`
- Shape: string
