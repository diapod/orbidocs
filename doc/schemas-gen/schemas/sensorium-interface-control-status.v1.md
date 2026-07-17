# Sensorium Interface Control Status v1

Source schema: [`doc/schemas/sensorium-interface-control-status.v1.schema.json`](../../schemas/sensorium-interface-control-status.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-control-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`caller/ref`](#field-caller-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `acquired`, `queued`, `cancelled`, `renewed`, `released`, `handed-off`, `refused`, `expired`, `preempted` |  |
| [`claim/id`](#field-claim-id) | `no` | ref: `#/$defs/claim_ref` |  |
| [`queue/position`](#field-queue-position) | `no` | integer |  |
| [`lease`](#field-lease) | `no` | ref: `sensorium-interface-control-lease.v1.schema.json` |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`status/at`](#field-status-at) | `yes` | string |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`interface_ref`](#def-interface-ref) | string |  |
| [`claim_ref`](#def-claim-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "acquired",
        "renewed",
        "handed-off"
      ]
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
  "required": [
    "lease"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "const": "queued"
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
  "required": [
    "claim/id",
    "queue/position"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "refused",
        "expired",
        "preempted"
      ]
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
  "required": [
    "reason"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-control-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-caller-ref"></a>
## `caller/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `acquired`, `queued`, `cancelled`, `renewed`, `released`, `handed-off`, `refused`, `expired`, `preempted`

<a id="field-claim-id"></a>
## `claim/id`

- Required: `no`
- Shape: ref: `#/$defs/claim_ref`

<a id="field-queue-position"></a>
## `queue/position`

- Required: `no`
- Shape: integer

<a id="field-lease"></a>
## `lease`

- Required: `no`
- Shape: ref: `sensorium-interface-control-lease.v1.schema.json`

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-status-at"></a>
## `status/at`

- Required: `yes`
- Shape: string

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-interface-ref"></a>
## `$defs.interface_ref`

- Shape: string

<a id="def-claim-ref"></a>
## `$defs.claim_ref`

- Shape: string
