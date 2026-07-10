# Middleware Channel Call Result v1

Source schema: [`doc/schemas/middleware-channel-call-result.v1.schema.json`](../../schemas/middleware-channel-call-result.v1.schema.json)

Redacted host-capability result with explicit retry and policy failure semantics.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-call-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `succeeded`, `refused`, `failed` |  |
| [`result/schema`](#field-result-schema) | `yes` | string \| null |  |
| [`result`](#field-result) | `yes` | any |  |
| [`failure`](#field-failure) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`failure`](#def-failure) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "succeeded"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "result/schema": {
      "type": "string"
    },
    "result": {
      "not": {
        "type": "null"
      }
    },
    "failure": {
      "type": "null"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "const": "refused"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "result/schema": {
      "type": "null"
    },
    "result": {
      "type": "null"
    },
    "failure": {
      "allOf": [
        {
          "$ref": "#/$defs/failure"
        },
        {
          "properties": {
            "class": {
              "const": "policy-denied"
            }
          }
        }
      ]
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "const": "failed"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "result/schema": {
      "type": "null"
    },
    "result": {
      "type": "null"
    },
    "failure": {
      "allOf": [
        {
          "$ref": "#/$defs/failure"
        },
        {
          "properties": {
            "class": {
              "enum": [
                "retryable",
                "terminal"
              ]
            }
          }
        }
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-call-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `succeeded`, `refused`, `failed`

<a id="field-result-schema"></a>
## `result/schema`

- Required: `yes`
- Shape: string | null

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: any

<a id="field-failure"></a>
## `failure`

- Required: `yes`
- Shape: unspecified

## Definition Semantics

<a id="def-failure"></a>
## `$defs.failure`

- Shape: object
