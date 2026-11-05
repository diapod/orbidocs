# Whisper-private-exchange-header.v1

Source schema: [`doc/schemas/whisper-private-exchange-header.v1.schema.json`](../../schemas/whisper-private-exchange-header.v1.schema.json)

Authenticated JCS header of the binary PEX sealed artifact. Encryption authenticates bytes, not sender or domain authority. No source node or plaintext digest is carried.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-private-exchange-header.v1` |  |
| [`family`](#field-family) | `yes` | enum: `case-registration`, `case-request`, `case-result`, `case-status-request`, `case-status-response`, `case-presentation-carried`, `case-presentation-referenced` |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
| [`recipient/key-digest`](#field-recipient-key-digest) | `yes` | string |  |
| [`sender/ephemeral-key`](#field-sender-ephemeral-key) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`plaintext/size`](#field-plaintext-size) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-private-exchange-header.v1`

<a id="field-family"></a>
## `family`

- Required: `yes`
- Shape: enum: `case-registration`, `case-request`, `case-result`, `case-status-request`, `case-status-response`, `case-presentation-carried`, `case-presentation-referenced`

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

<a id="field-recipient-key-digest"></a>
## `recipient/key-digest`

- Required: `yes`
- Shape: string

<a id="field-sender-ephemeral-key"></a>
## `sender/ephemeral-key`

- Required: `yes`
- Shape: string

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-plaintext-size"></a>
## `plaintext/size`

- Required: `yes`
- Shape: integer
