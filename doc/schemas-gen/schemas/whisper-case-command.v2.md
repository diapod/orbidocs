# Whisper-case-command.v2

Source schema: [`doc/schemas/whisper-case-command.v2.schema.json`](../../schemas/whisper-case-command.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-command.v2` |  |
| [`family`](#field-family) | `yes` | enum: `case-registration`, `case-request`, `case-status-request` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`exchange`](#field-exchange) | `yes` | string |  |
| [`response/public-key`](#field-response-public-key) | `yes` | string |  |
| [`control`](#field-control) | `yes` | string |  |
| [`evidence`](#field-evidence) | `yes` | array |  |
| [`adc/consent`](#field-adc-consent) | `no` | object | Private original M and complete M_A set for registration only; the signed registration binds its canonical digest. It never carries the approved payload or its opening and does not establish local trust. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "family": {
      "const": "case-status-request"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "evidence": {
      "maxItems": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "family": {
      "const": "case-registration"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "evidence": {
      "items": {
        "properties": {
          "role": {
            "enum": [
              "anchor-record",
              "anchor-manifest",
              "anchor-receipt",
              "anchor-certificate",
              "profile",
              "anchor-status",
              "anchor-closure",
              "anchor-source"
            ]
          }
        }
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "family": {
      "const": "case-request"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "evidence": {
      "items": {
        "properties": {
          "role": {
            "enum": [
              "profile",
              "successor-certificate",
              "successor-acceptance-status"
            ]
          }
        }
      }
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "family": {
      "const": "case-registration"
    }
  },
  "required": [
    "family"
  ]
}
```

Then:

```json
{
  "properties": {
    "evidence": {
      "contains": {
        "type": "object",
        "required": [
          "role"
        ],
        "properties": {
          "role": {
            "const": "anchor-source"
          }
        }
      }
    }
  }
}
```

### Rule 5

When:

```json
{
  "required": [
    "adc/consent"
  ]
}
```

Then:

```json
{
  "properties": {
    "family": {
      "const": "case-registration"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-command.v2`

<a id="field-family"></a>
## `family`

- Required: `yes`
- Shape: enum: `case-registration`, `case-request`, `case-status-request`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-exchange"></a>
## `exchange`

- Required: `yes`
- Shape: string

<a id="field-response-public-key"></a>
## `response/public-key`

- Required: `yes`
- Shape: string

<a id="field-control"></a>
## `control`

- Required: `yes`
- Shape: string

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array

<a id="field-adc-consent"></a>
## `adc/consent`

- Required: `no`
- Shape: object

Private original M and complete M_A set for registration only; the signed registration binds its canonical digest. It never carries the approved payload or its opening and does not establish local trust.
