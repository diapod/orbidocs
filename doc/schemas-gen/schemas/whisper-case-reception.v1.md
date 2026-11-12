# Whisper-case-reception.v1

Source schema: [`doc/schemas/whisper-case-reception.v1.schema.json`](../../schemas/whisper-case-reception.v1.schema.json)

Recipient-signed exact-byte domain reception. Neither transport custody nor a grant of continue-case permission; no owner scope or source node is disclosed.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-reception.v1` |  |
| [`request/family`](#field-request-family) | `yes` | enum: `case-presentation-carried-confirmed`, `case-presentation-referenced-confirmed` |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
| [`recipient`](#field-recipient) | `yes` | string |  |
| [`presentation/digest`](#field-presentation-digest) | `yes` | string |  |
| [`response/key-digest`](#field-response-key-digest) | `yes` | string |  |
| [`received/at`](#field-received-at) | `yes` | string |  |
| [`handoff/not-after`](#field-handoff-not-after) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-reception.v1`

<a id="field-request-family"></a>
## `request/family`

- Required: `yes`
- Shape: enum: `case-presentation-carried-confirmed`, `case-presentation-referenced-confirmed`

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

<a id="field-recipient"></a>
## `recipient`

- Required: `yes`
- Shape: string

<a id="field-presentation-digest"></a>
## `presentation/digest`

- Required: `yes`
- Shape: string

<a id="field-response-key-digest"></a>
## `response/key-digest`

- Required: `yes`
- Shape: string

<a id="field-received-at"></a>
## `received/at`

- Required: `yes`
- Shape: string

<a id="field-handoff-not-after"></a>
## `handoff/not-after`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
