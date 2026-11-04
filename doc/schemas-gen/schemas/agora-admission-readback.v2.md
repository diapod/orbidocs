# Agora-admission-readback.v2

Source schema: [`doc/schemas/agora-admission-readback.v2.schema.json`](../../schemas/agora-admission-readback.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-admission-readback.v2` |  |
| [`receipt/profile`](#field-receipt-profile) | `yes` | enum: `full-record`, `detached-manifest` |  |
| [`reference`](#field-reference) | `yes` | string |  |
| [`issuance`](#field-issuance) | `yes` | unspecified |  |
| [`material`](#field-material) | `yes` | unspecified |  |
| [`links`](#field-links) | `yes` | object |  |
| [`payload/state`](#field-payload-state) | `no` | enum: `retained`, `payload-pruned` |  |
| [`local/admission`](#field-local-admission) | `yes` | unspecified |  |

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
- Shape: const: `agora-admission-readback.v2`

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
- Shape: unspecified

<a id="field-links"></a>
## `links`

- Required: `yes`
- Shape: object

<a id="field-payload-state"></a>
## `payload/state`

- Required: `no`
- Shape: enum: `retained`, `payload-pruned`

<a id="field-local-admission"></a>
## `local/admission`

- Required: `yes`
- Shape: unspecified
