# Sensorium Interface Actuation Status v1

Source schema: [`doc/schemas/sensorium-interface-actuation-status.v1.schema.json`](../../schemas/sensorium-interface-actuation-status.v1.schema.json)

Grant-gated, caller-relative status for one actuation interface.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-actuation-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`coordination/mode`](#field-coordination-mode) | `yes` | enum: `shared`, `exclusive-lease` |  |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | enum: `published`, `suspended`, `withdrawn`, `expired` |  |
| [`health/status`](#field-health-status) | `yes` | enum: `ready`, `degraded` |  |
| [`health/reason`](#field-health-reason) | `no` | string |  |
| [`control/state`](#field-control-state) | `yes` | enum: `not-applicable`, `free`, `held-by-caller`, `held` |  |
| [`claim/state`](#field-claim-state) | `yes` | enum: `not-applicable`, `absent`, `queued`, `held` |  |
| [`claim/id`](#field-claim-id) | `no` | ref: `#/$defs/claim_ref` |  |
| [`queue/position`](#field-queue-position) | `no` | integer |  |
| [`lease`](#field-lease) | `no` | ref: `sensorium-interface-control-lease.v1.schema.json` |  |
| [`status/at`](#field-status-at) | `yes` | string |  |

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
    "health/status": {
      "const": "degraded"
    }
  },
  "required": [
    "health/status"
  ]
}
```

Then:

```json
{
  "required": [
    "health/reason"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "coordination/mode": {
      "const": "shared"
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
  "properties": {
    "control/state": {
      "const": "not-applicable"
    },
    "claim/state": {
      "const": "not-applicable"
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "claim/id"
        ]
      },
      {
        "required": [
          "queue/position"
        ]
      },
      {
        "required": [
          "lease"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-actuation-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-coordination-mode"></a>
## `coordination/mode`

- Required: `yes`
- Shape: enum: `shared`, `exclusive-lease`

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: enum: `published`, `suspended`, `withdrawn`, `expired`

<a id="field-health-status"></a>
## `health/status`

- Required: `yes`
- Shape: enum: `ready`, `degraded`

<a id="field-health-reason"></a>
## `health/reason`

- Required: `no`
- Shape: string

<a id="field-control-state"></a>
## `control/state`

- Required: `yes`
- Shape: enum: `not-applicable`, `free`, `held-by-caller`, `held`

<a id="field-claim-state"></a>
## `claim/state`

- Required: `yes`
- Shape: enum: `not-applicable`, `absent`, `queued`, `held`

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

<a id="field-status-at"></a>
## `status/at`

- Required: `yes`
- Shape: string

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
