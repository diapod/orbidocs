# Sensorium Interface Read Result v1

Source schema: [`doc/schemas/sensorium-interface-read-result.v1.schema.json`](../../schemas/sensorium-interface-read-result.v1.schema.json)

Bounded delivery batch and its single cursor-advancement unit.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-read-result.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`interface/id`](#field-interface-id) | `yes` | string | Interface resource that produced this batch. |
| [`delivery/kind`](#field-delivery-kind) | `yes` | enum: `one-shot`, `subscription` | Delivery binding echoed from the admitted request. |
| [`subscription/id`](#field-subscription-id) | `no` | string | Caller-bound lease that owns cursor progress for subscription delivery. |
| [`batch/outcome`](#field-batch-outcome) | `yes` | enum: `data`, `no-change`, `terminal` | Successful data, bounded timeout without change, or final subscription outcome. |
| [`cursor/next`](#field-cursor-next) | `no` | string | Opaque resume point after accepting the complete batch. |
| [`frames`](#field-frames) | `yes` | array | Ordered frames delivered atomically with cursor progress. |
| [`delivery/diagnostics`](#field-delivery-diagnostics) | `yes` | object | Bounded delivery-loss and coalescing evidence for this result. |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` | P081 batch context for traceability; never authority. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "delivery/kind": {
      "const": "subscription"
    }
  },
  "required": [
    "delivery/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "subscription/id",
    "cursor/next"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "batch/outcome": {
      "const": "no-change"
    }
  },
  "required": [
    "batch/outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "frames": {
      "maxItems": 0
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "batch/outcome": {
      "const": "data"
    }
  },
  "required": [
    "batch/outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "frames": {
      "minItems": 1
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "batch/outcome": {
      "const": "terminal"
    }
  },
  "required": [
    "batch/outcome"
  ]
}
```

Then:

```json
{
  "properties": {
    "delivery/kind": {
      "const": "subscription"
    },
    "frames": {
      "minItems": 1,
      "maxItems": 1,
      "items": {
        "allOf": [
          {
            "$ref": "sensorium-interface-frame.v1.schema.json"
          },
          {
            "properties": {
              "frame/kind": {
                "const": "end"
              }
            }
          }
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
- Shape: const: `sensorium-interface-read-result.v1`

Contract discriminator.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Contract version.

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

Interface resource that produced this batch.

<a id="field-delivery-kind"></a>
## `delivery/kind`

- Required: `yes`
- Shape: enum: `one-shot`, `subscription`

Delivery binding echoed from the admitted request.

<a id="field-subscription-id"></a>
## `subscription/id`

- Required: `no`
- Shape: string

Caller-bound lease that owns cursor progress for subscription delivery.

<a id="field-batch-outcome"></a>
## `batch/outcome`

- Required: `yes`
- Shape: enum: `data`, `no-change`, `terminal`

Successful data, bounded timeout without change, or final subscription outcome.

<a id="field-cursor-next"></a>
## `cursor/next`

- Required: `no`
- Shape: string

Opaque resume point after accepting the complete batch.

<a id="field-frames"></a>
## `frames`

- Required: `yes`
- Shape: array

Ordered frames delivered atomically with cursor progress.

<a id="field-delivery-diagnostics"></a>
## `delivery/diagnostics`

- Required: `yes`
- Shape: object

Bounded delivery-loss and coalescing evidence for this result.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

P081 batch context for traceability; never authority.
