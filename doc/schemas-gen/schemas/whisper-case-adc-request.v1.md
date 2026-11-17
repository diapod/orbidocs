# Whisper-case-adc-request.v1

Source schema: [`doc/schemas/whisper-case-adc-request.v1.schema.json`](../../schemas/whisper-case-adc-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-adc-request.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`command`](#field-command) | `yes` | unspecified |  |
| [`signer`](#field-signer) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`intent`](#def-intent) | object |  |
| [`receipt`](#def-receipt) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-adc-request.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-command"></a>
## `command`

- Required: `yes`
- Shape: unspecified

<a id="field-signer"></a>
## `signer`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

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

## Definition Semantics

<a id="def-intent"></a>
## `$defs.intent`

- Shape: object

<a id="def-receipt"></a>
## `$defs.receipt`

- Shape: object
