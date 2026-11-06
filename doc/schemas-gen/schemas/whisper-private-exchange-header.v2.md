# Whisper-private-exchange-header.v2

Source schema: [`doc/schemas/whisper-private-exchange-header.v2.schema.json`](../../schemas/whisper-private-exchange-header.v2.schema.json)

Authenticated binary PEX header for explicit confirmed audience delivery and its private domain receipt. A scoped random response key is not a source-node route; legacy one-way v1 is unchanged.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-private-exchange-header.v2` |  |
| [`family`](#field-family) | `yes` | enum: `case-presentation-carried-confirmed`, `case-presentation-referenced-confirmed`, `case-reception` |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
| [`recipient/key-digest`](#field-recipient-key-digest) | `yes` | string |  |
| [`sender/ephemeral-key`](#field-sender-ephemeral-key) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`plaintext/size`](#field-plaintext-size) | `yes` | integer |  |
| [`response/public-key`](#field-response-public-key) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "family": {
      "enum": [
        "case-presentation-carried-confirmed",
        "case-presentation-referenced-confirmed"
      ]
    }
  }
}
```

Then:

```json
{
  "required": [
    "response/public-key"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-private-exchange-header.v2`

<a id="field-family"></a>
## `family`

- Required: `yes`
- Shape: enum: `case-presentation-carried-confirmed`, `case-presentation-referenced-confirmed`, `case-reception`

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

<a id="field-response-public-key"></a>
## `response/public-key`

- Required: `no`
- Shape: string
