# Whisper-case-result.v1

Source schema: [`doc/schemas/whisper-case-result.v1.schema.json`](../../schemas/whisper-case-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-result.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`evaluated/at`](#field-evaluated-at) | `yes` | string |  |
| [`outcome`](#field-outcome) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-result.v1`

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

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-evaluated-at"></a>
## `evaluated/at`

- Required: `yes`
- Shape: string

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: unspecified
