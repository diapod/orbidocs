# Nym-issuance-request.v1

Source schema: [`doc/schemas/nym-issuance-request.v1.schema.json`](../../schemas/nym-issuance-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-request.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `issue`, `renew`, `private-reset` |  |
| [`applicant/id`](#field-applicant-id) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`reply/recipient`](#field-reply-recipient) | `yes` | string |  |
| [`reply/key`](#field-reply-key) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`nym/id`](#field-nym-id) | `yes` | string |  |
| [`request/nonce`](#field-request-nonce) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`prior/certificate-digest`](#field-prior-certificate-digest) | `no` | string |  |
| [`nym/proof`](#field-nym-proof) | `yes` | object |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`topic/key`](#field-topic-key) | `yes` | string |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string | Independent opaque 256-bit transport correlation; never the private signed request digest. |
| [`bootstrap/key-public`](#field-bootstrap-key-public) | `yes` | string | Domain-separated ephemeral Ed25519 bootstrap proof key; not the participant or nym public key. |
| [`bootstrap/proof`](#field-bootstrap-proof) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "operation": {
      "const": "issue"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "prior/certificate-digest"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-request.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `issue`, `renew`, `private-reset`

<a id="field-applicant-id"></a>
## `applicant/id`

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

<a id="field-reply-key"></a>
## `reply/key`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

<a id="field-request-nonce"></a>
## `request/nonce`

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

<a id="field-prior-certificate-digest"></a>
## `prior/certificate-digest`

- Required: `no`
- Shape: string

<a id="field-nym-proof"></a>
## `nym/proof`

- Required: `yes`
- Shape: object

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-topic-key"></a>
## `topic/key`

- Required: `yes`
- Shape: string

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

Independent opaque 256-bit transport correlation; never the private signed request digest.

<a id="field-bootstrap-key-public"></a>
## `bootstrap/key-public`

- Required: `yes`
- Shape: string

Domain-separated ephemeral Ed25519 bootstrap proof key; not the participant or nym public key.

<a id="field-bootstrap-proof"></a>
## `bootstrap/proof`

- Required: `yes`
- Shape: object
