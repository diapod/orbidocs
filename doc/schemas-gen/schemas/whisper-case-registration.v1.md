# Whisper-case-registration.v1

Source schema: [`doc/schemas/whisper-case-registration.v1.schema.json`](../../schemas/whisper-case-registration.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-registration.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`case/not-after`](#field-case-not-after) | `yes` | string |  |
| [`authorization/public-key`](#field-authorization-public-key) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | array |  |
| [`inputs/digest`](#field-inputs-digest) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-registration.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-case-not-after"></a>
## `case/not-after`

- Required: `yes`
- Shape: string

<a id="field-authorization-public-key"></a>
## `authorization/public-key`

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

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: array

<a id="field-inputs-digest"></a>
## `inputs/digest`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
