# Whisper-adc-proposal-request.v1

Source schema: [`doc/schemas/whisper-adc-proposal-request.v1.schema.json`](../../schemas/whisper-adc-proposal-request.v1.schema.json)

Private ADC threshold query from a named executor. The signature binds the exact PEX exchange and response key. This is a read of a bounded observation, without a case transition.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-adc-proposal-request.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`release/id`](#field-release-id) | `yes` | string |  |
| [`executor`](#field-executor) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`response/key-digest`](#field-response-key-digest) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
| [`exchange`](#field-exchange) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-adc-proposal-request.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-release-id"></a>
## `release/id`

- Required: `yes`
- Shape: string

<a id="field-executor"></a>
## `executor`

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

<a id="field-response-key-digest"></a>
## `response/key-digest`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string

<a id="field-exchange"></a>
## `exchange`

- Required: `yes`
- Shape: string
