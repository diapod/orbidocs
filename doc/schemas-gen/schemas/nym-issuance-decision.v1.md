# Nym-issuance-decision.v1

Source schema: [`doc/schemas/nym-issuance-decision.v1.schema.json`](../../schemas/nym-issuance-decision.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-decision.v1` |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`reply/recipient`](#field-reply-recipient) | `yes` | string |  |
| [`decision`](#field-decision) | `yes` | enum: `issued`, `refused`, `reset-required` |  |
| [`decided/at`](#field-decided-at) | `yes` | string |  |
| [`certificate`](#field-certificate) | `no` | ref: `whisper-source-certificate.v1.schema.json` |  |
| [`reason`](#field-reason) | `no` | enum: `policy-denied`, `request-expired`, `binding-unavailable`, `context-unavailable`, `capacity-exceeded`, `reset-required` |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`decision/nonce`](#field-decision-nonce) | `yes` | string | Fresh private 256-bit entropy, signed and retained only inside the erasable decision payload; prevents retained decision digests from becoming identity-mapping oracles. |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string | Independent opaque 256-bit transport correlation; never the private signed request digest. |
| [`status/min-revision`](#field-status-min-revision) | `no` | integer | Private minimum status generation required by this issued decision. The public certificate floor stays one. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "decision": {
      "const": "issued"
    }
  },
  "required": [
    "decision"
  ]
}
```

Then:

```json
{
  "required": [
    "certificate",
    "status/min-revision"
  ],
  "not": {
    "required": [
      "reason"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "decision": {
      "const": "reset-required"
    }
  },
  "required": [
    "decision"
  ]
}
```

Then:

```json
{
  "properties": {
    "reason": {
      "const": "reset-required"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-decision.v1`

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-reply-recipient"></a>
## `reply/recipient`

- Required: `yes`
- Shape: string

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `issued`, `refused`, `reset-required`

<a id="field-decided-at"></a>
## `decided/at`

- Required: `yes`
- Shape: string

<a id="field-certificate"></a>
## `certificate`

- Required: `no`
- Shape: ref: `whisper-source-certificate.v1.schema.json`

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: enum: `policy-denied`, `request-expired`, `binding-unavailable`, `context-unavailable`, `capacity-exceeded`, `reset-required`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-decision-nonce"></a>
## `decision/nonce`

- Required: `yes`
- Shape: string

Fresh private 256-bit entropy, signed and retained only inside the erasable decision payload; prevents retained decision digests from becoming identity-mapping oracles.

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

Independent opaque 256-bit transport correlation; never the private signed request digest.

<a id="field-status-min-revision"></a>
## `status/min-revision`

- Required: `no`
- Shape: integer

Private minimum status generation required by this issued decision. The public certificate floor stays one.
