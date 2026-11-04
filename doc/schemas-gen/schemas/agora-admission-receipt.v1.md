# Agora-admission-receipt.v1

Source schema: [`doc/schemas/agora-admission-receipt.v1.schema.json`](../../schemas/agora-admission-receipt.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-admission-receipt.v1` |  |
| [`receipt/profile`](#field-receipt-profile) | `yes` | enum: `full-record`, `detached-manifest` |  |
| [`author/bytes-digest`](#field-author-bytes-digest) | `yes` | string |  |
| [`certificate/digest`](#field-certificate-digest) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`policy/digest`](#field-policy-digest) | `yes` | string |  |
| [`status/digest`](#field-status-digest) | `yes` | string |  |
| [`status/revision`](#field-status-revision) | `yes` | integer |  |
| [`witness/node-id`](#field-witness-node-id) | `yes` | string |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`committed/at`](#field-committed-at) | `yes` | string |  |
| [`outcome`](#field-outcome) | `yes` | const: `accepted` |  |
| [`witness/delegation-digest`](#field-witness-delegation-digest) | `yes` | string |  |
| [`witness/delegation`](#field-witness-delegation) | `yes` | ref: `witness-key-delegation.v1.schema.json` |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`record/id`](#field-record-id) | `no` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `no` | string |  |
| [`case/continuity-key-digest`](#field-case-continuity-key-digest) | `no` | string |  |
| [`case/status-authority`](#field-case-status-authority) | `no` | string |  |
| [`case/not-after`](#field-case-not-after) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "receipt/profile": {
      "const": "full-record"
    }
  }
}
```

Then:

```json
{
  "required": [
    "record/id"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "manifest/digest"
        ]
      },
      {
        "required": [
          "case/continuity-key-digest"
        ]
      },
      {
        "required": [
          "case/status-authority"
        ]
      },
      {
        "required": [
          "case/not-after"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-admission-receipt.v1`

<a id="field-receipt-profile"></a>
## `receipt/profile`

- Required: `yes`
- Shape: enum: `full-record`, `detached-manifest`

<a id="field-author-bytes-digest"></a>
## `author/bytes-digest`

- Required: `yes`
- Shape: string

<a id="field-certificate-digest"></a>
## `certificate/digest`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: string

<a id="field-status-digest"></a>
## `status/digest`

- Required: `yes`
- Shape: string

<a id="field-status-revision"></a>
## `status/revision`

- Required: `yes`
- Shape: integer

<a id="field-witness-node-id"></a>
## `witness/node-id`

- Required: `yes`
- Shape: string

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-committed-at"></a>
## `committed/at`

- Required: `yes`
- Shape: string

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: const: `accepted`

<a id="field-witness-delegation-digest"></a>
## `witness/delegation-digest`

- Required: `yes`
- Shape: string

<a id="field-witness-delegation"></a>
## `witness/delegation`

- Required: `yes`
- Shape: ref: `witness-key-delegation.v1.schema.json`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-record-id"></a>
## `record/id`

- Required: `no`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `no`
- Shape: string

<a id="field-case-continuity-key-digest"></a>
## `case/continuity-key-digest`

- Required: `no`
- Shape: string

<a id="field-case-status-authority"></a>
## `case/status-authority`

- Required: `no`
- Shape: string

<a id="field-case-not-after"></a>
## `case/not-after`

- Required: `no`
- Shape: string
