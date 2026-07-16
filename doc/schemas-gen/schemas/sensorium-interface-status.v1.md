# Sensorium Interface Status v1

Source schema: [`doc/schemas/sensorium-interface-status.v1.schema.json`](../../schemas/sensorium-interface-status.v1.schema.json)

Current host projection of an interface publication lifecycle and health.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-status.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`interface/id`](#field-interface-id) | `yes` | string | Interface resource described by this status. |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | enum: `published`, `suspended`, `withdrawn`, `expired` | Host-enforced publication lifecycle. |
| [`health/status`](#field-health-status) | `yes` | enum: `ready`, `degraded` | Current ability to serve admitted operations. |
| [`health/reason`](#field-health-reason) | `no` | string | Required bounded diagnostic when health is degraded. |
| [`status/at`](#field-status-at) | `yes` | string | Time this status projection was recorded. |

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

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-status.v1`

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

Interface resource described by this status.

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: enum: `published`, `suspended`, `withdrawn`, `expired`

Host-enforced publication lifecycle.

<a id="field-health-status"></a>
## `health/status`

- Required: `yes`
- Shape: enum: `ready`, `degraded`

Current ability to serve admitted operations.

<a id="field-health-reason"></a>
## `health/reason`

- Required: `no`
- Shape: string

Required bounded diagnostic when health is degraded.

<a id="field-status-at"></a>
## `status/at`

- Required: `yes`
- Shape: string

Time this status projection was recorded.
