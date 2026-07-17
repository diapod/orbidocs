# Sensorium Interface Invoke Request v1

Source schema: [`doc/schemas/sensorium-interface-invoke-request.v1.schema.json`](../../schemas/sensorium-interface-invoke-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-invoke-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`interface/id`](#field-interface-id) | `yes` | string |  |
| [`caller/ref`](#field-caller-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`grant/id`](#field-grant-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`coordination/mode`](#field-coordination-mode) | `yes` | enum: `shared`, `exclusive-lease` |  |
| [`lease/id`](#field-lease-id) | `no` | string |  |
| [`lease/epoch`](#field-lease-epoch) | `no` | integer |  |
| [`caller/sequence`](#field-caller-sequence) | `no` | integer |  |
| [`method/name`](#field-method-name) | `yes` | string |  |
| [`input/schema-ref`](#field-input-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`payload`](#field-payload) | `yes` | unspecified |  |
| [`deadline/at`](#field-deadline-at) | `yes` | string |  |
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
    "coordination/mode": {
      "const": "exclusive-lease"
    }
  },
  "required": [
    "coordination/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "lease/id",
    "lease/epoch",
    "caller/sequence"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-invoke-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

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

<a id="field-coordination-mode"></a>
## `coordination/mode`

- Required: `yes`
- Shape: enum: `shared`, `exclusive-lease`

<a id="field-lease-id"></a>
## `lease/id`

- Required: `no`
- Shape: string

<a id="field-lease-epoch"></a>
## `lease/epoch`

- Required: `no`
- Shape: integer

<a id="field-caller-sequence"></a>
## `caller/sequence`

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

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: unspecified

<a id="field-deadline-at"></a>
## `deadline/at`

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
