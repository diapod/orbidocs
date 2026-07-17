# Sensorium Interface Invoke Receipt v1

Source schema: [`doc/schemas/sensorium-interface-invoke-receipt.v1.schema.json`](../../schemas/sensorium-interface-invoke-receipt.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-invoke-receipt.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`interface/id`](#field-interface-id) | `yes` | string |  |
| [`caller/ref`](#field-caller-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`grant/id`](#field-grant-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`lease/id`](#field-lease-id) | `no` | string |  |
| [`lease/epoch`](#field-lease-epoch) | `no` | integer |  |
| [`method/name`](#field-method-name) | `yes` | string |  |
| [`input/schema-ref`](#field-input-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`payload/digest`](#field-payload-digest) | `yes` | string |  |
| [`accepted/sequence`](#field-accepted-sequence) | `no` | integer |  |
| [`outcome`](#field-outcome) | `yes` | enum: `applied`, `refused`, `failed`, `unknown` |  |
| [`evidence/class`](#field-evidence-class) | `yes` | enum: `host-admission`, `provider-ack`, `operation-status`, `state-readback`, `none` |  |
| [`evidence/ref`](#field-evidence-ref) | `no` | ref: `#/$defs/ref` |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`completed/at`](#field-completed-at) | `yes` | string |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

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
    "evidence/class": {
      "const": "host-admission"
    }
  },
  "required": [
    "reason"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "const": "unknown"
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
    "evidence/class": {
      "const": "none"
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
    "evidence/class": {
      "enum": [
        "provider-ack",
        "operation-status"
      ]
    }
  },
  "required": [
    "reason"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "outcome": {
      "const": "applied"
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
    "evidence/class": {
      "enum": [
        "provider-ack",
        "operation-status",
        "state-readback"
      ]
    }
  },
  "required": [
    "accepted/sequence"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-invoke-receipt.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

<a id="field-caller-ref"></a>
## `caller/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-grant-id"></a>
## `grant/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-lease-id"></a>
## `lease/id`

- Required: `no`
- Shape: string

<a id="field-lease-epoch"></a>
## `lease/epoch`

- Required: `no`
- Shape: integer

<a id="field-method-name"></a>
## `method/name`

- Required: `yes`
- Shape: string

<a id="field-input-schema-ref"></a>
## `input/schema-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-payload-digest"></a>
## `payload/digest`

- Required: `yes`
- Shape: string

<a id="field-accepted-sequence"></a>
## `accepted/sequence`

- Required: `no`
- Shape: integer

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `applied`, `refused`, `failed`, `unknown`

<a id="field-evidence-class"></a>
## `evidence/class`

- Required: `yes`
- Shape: enum: `host-admission`, `provider-ack`, `operation-status`, `state-readback`, `none`

<a id="field-evidence-ref"></a>
## `evidence/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-completed-at"></a>
## `completed/at`

- Required: `yes`
- Shape: string

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
