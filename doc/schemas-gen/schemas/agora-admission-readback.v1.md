# Agora-admission-readback.v1

Source schema: [`doc/schemas/agora-admission-readback.v1.schema.json`](../../schemas/agora-admission-readback.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-admission-readback.v1` |  |
| [`receipt/profile`](#field-receipt-profile) | `yes` | enum: `full-record`, `detached-manifest` |  |
| [`reference`](#field-reference) | `yes` | string |  |
| [`issuance`](#field-issuance) | `yes` | unspecified |  |
| [`material`](#field-material) | `yes` | ref: `agora-admission-material.v1.schema.json` |  |
| [`links`](#field-links) | `yes` | object |  |
| [`payload/state`](#field-payload-state) | `no` | enum: `retained`, `payload-pruned` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "receipt/profile": {
      "const": "detached-manifest"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "material": {
      "not": {
        "required": [
          "author/bytes"
        ]
      },
      "properties": {
        "statuses": {
          "maxItems": 0
        },
        "certificates": {
          "maxItems": 0
        }
      }
    },
    "links": {
      "not": {
        "required": [
          "publication"
        ]
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-admission-readback.v1`

<a id="field-receipt-profile"></a>
## `receipt/profile`

- Required: `yes`
- Shape: enum: `full-record`, `detached-manifest`

<a id="field-reference"></a>
## `reference`

- Required: `yes`
- Shape: string

<a id="field-issuance"></a>
## `issuance`

- Required: `yes`
- Shape: unspecified

<a id="field-material"></a>
## `material`

- Required: `yes`
- Shape: ref: `agora-admission-material.v1.schema.json`

<a id="field-links"></a>
## `links`

- Required: `yes`
- Shape: object

<a id="field-payload-state"></a>
## `payload/state`

- Required: `no`
- Shape: enum: `retained`, `payload-pruned`
