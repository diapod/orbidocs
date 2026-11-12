# Whisper-case-status.v1

Source schema: [`doc/schemas/whisper-case-status.v1.schema.json`](../../schemas/whisper-case-status.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-status.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`head`](#field-head) | `yes` | object |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-status.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-head"></a>
## `head`

- Required: `yes`
- Shape: object

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
