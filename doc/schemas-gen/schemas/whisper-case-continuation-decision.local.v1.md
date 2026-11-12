# Whisper-case-continuation-decision.local.v1

Source schema: [`doc/schemas/whisper-case-continuation-decision.local.v1.schema.json`](../../schemas/whisper-case-continuation-decision.local.v1.schema.json)

Recipient-owned point-in-time decision for continue-case only. History/authenticity are independently verified inputs; case and source currency remain separate. The effect owner rechecks time and fencing.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-continuation-decision.local.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`successor`](#field-successor) | `yes` | string |  |
| [`reader`](#field-reader) | `yes` | string |  |
| [`succession/digest`](#field-succession-digest) | `yes` | string |  |
| [`acceptance/digest`](#field-acceptance-digest) | `yes` | string |  |
| [`inputs/digest`](#field-inputs-digest) | `yes` | string |  |
| [`evaluated/at`](#field-evaluated-at) | `yes` | string |  |
| [`case/usable-until`](#field-case-usable-until) | `yes` | string |  |
| [`case/currency`](#field-case-currency) | `yes` | unspecified |  |
| [`source/currency`](#field-source-currency) | `yes` | unspecified |  |
| [`result`](#field-result) | `yes` | enum: `allowed`, `refused` |  |
| [`signature/work`](#field-signature-work) | `yes` | integer |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`anchor/witness`](#field-anchor-witness) | `yes` | unspecified |  |
| [`registration/basis`](#field-registration-basis) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "result": {
      "const": "allowed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "case/currency": {
      "properties": {
        "outcome": {
          "const": "current"
        }
      }
    },
    "source/currency": {
      "properties": {
        "state": {
          "const": "usable"
        }
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "case/currency": {
      "properties": {
        "outcome": {
          "const": "current"
        }
      }
    },
    "source/currency": {
      "properties": {
        "state": {
          "const": "usable"
        }
      }
    }
  }
}
```

Then:

```json
{
  "properties": {
    "result": {
      "const": "allowed"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-continuation-decision.local.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-successor"></a>
## `successor`

- Required: `yes`
- Shape: string

<a id="field-reader"></a>
## `reader`

- Required: `yes`
- Shape: string

<a id="field-succession-digest"></a>
## `succession/digest`

- Required: `yes`
- Shape: string

<a id="field-acceptance-digest"></a>
## `acceptance/digest`

- Required: `yes`
- Shape: string

<a id="field-inputs-digest"></a>
## `inputs/digest`

- Required: `yes`
- Shape: string

<a id="field-evaluated-at"></a>
## `evaluated/at`

- Required: `yes`
- Shape: string

<a id="field-case-usable-until"></a>
## `case/usable-until`

- Required: `yes`
- Shape: string

<a id="field-case-currency"></a>
## `case/currency`

- Required: `yes`
- Shape: unspecified

<a id="field-source-currency"></a>
## `source/currency`

- Required: `yes`
- Shape: unspecified

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: enum: `allowed`, `refused`

<a id="field-signature-work"></a>
## `signature/work`

- Required: `yes`
- Shape: integer

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-anchor-witness"></a>
## `anchor/witness`

- Required: `yes`
- Shape: unspecified

<a id="field-registration-basis"></a>
## `registration/basis`

- Required: `yes`
- Shape: unspecified
