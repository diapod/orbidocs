# Memarium-admission-custody-export.v1

Source schema: [`doc/schemas/memarium-admission-custody-export.v1.schema.json`](../../schemas/memarium-admission-custody-export.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `memarium-admission-custody-export.v1` |  |
| [`material`](#field-material) | `yes` | unspecified |  |
| [`custody`](#field-custody) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "custody": {
      "properties": {
        "payload/state": {
          "enum": [
            "unreachable",
            "key-destroyed",
            "absent"
          ]
        }
      },
      "required": [
        "payload/state"
      ]
    }
  },
  "required": [
    "custody"
  ]
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
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `memarium-admission-custody-export.v1`

<a id="field-material"></a>
## `material`

- Required: `yes`
- Shape: unspecified

<a id="field-custody"></a>
## `custody`

- Required: `yes`
- Shape: object
