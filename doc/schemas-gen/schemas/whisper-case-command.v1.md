# Whisper-case-command.v1

Source schema: [`doc/schemas/whisper-case-command.v1.schema.json`](../../schemas/whisper-case-command.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-command.v1` |  |
| [`family`](#field-family) | `yes` | enum: `case-registration`, `case-request`, `case-status-request` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`exchange`](#field-exchange) | `yes` | string |  |
| [`response/public-key`](#field-response-public-key) | `yes` | string |  |
| [`control`](#field-control) | `yes` | string |  |
| [`evidence`](#field-evidence) | `yes` | array |  |

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
              "anchor-closure"
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

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-command.v1`

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
