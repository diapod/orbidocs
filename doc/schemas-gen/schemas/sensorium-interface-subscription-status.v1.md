# Sensorium Interface Subscription Status v1

Source schema: [`doc/schemas/sensorium-interface-subscription-status.v1.schema.json`](../../schemas/sensorium-interface-subscription-status.v1.schema.json)

Durable host projection of one caller-bound Sensorium Interface lease.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-subscription-status.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`subscription/id`](#field-subscription-id) | `yes` | string | Stable identifier of this lease. |
| [`interface/id`](#field-interface-id) | `yes` | string | Interface resource bound to this lease. |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | enum: `requested`, `active`, `closing`, `closed` | Host-enforced lease lifecycle. |
| [`health/status`](#field-health-status) | `yes` | enum: `ready`, `degraded` | Current ability to serve read-next operations. |
| [`health/reason`](#field-health-reason) | `no` | string | Required bounded diagnostic when health is degraded. |
| [`lease/expires-at`](#field-lease-expires-at) | `yes` | string | Hard expiry of the current lease grant. |
| [`cursor/current`](#field-cursor-current) | `no` | string | Last batch-level progress token committed for this lease. |
| [`terminal/reason`](#field-terminal-reason) | `no` | string | Immutable closure reason required for a closed lease. |
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

### Rule 2

When:

```json
{
  "properties": {
    "lifecycle/status": {
      "const": "closed"
    }
  },
  "required": [
    "lifecycle/status"
  ]
}
```

Then:

```json
{
  "required": [
    "terminal/reason"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-subscription-status.v1`

Contract discriminator.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Contract version.

<a id="field-subscription-id"></a>
## `subscription/id`

- Required: `yes`
- Shape: string

Stable identifier of this lease.

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

Interface resource bound to this lease.

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: enum: `requested`, `active`, `closing`, `closed`

Host-enforced lease lifecycle.

<a id="field-health-status"></a>
## `health/status`

- Required: `yes`
- Shape: enum: `ready`, `degraded`

Current ability to serve read-next operations.

<a id="field-health-reason"></a>
## `health/reason`

- Required: `no`
- Shape: string

Required bounded diagnostic when health is degraded.

<a id="field-lease-expires-at"></a>
## `lease/expires-at`

- Required: `yes`
- Shape: string

Hard expiry of the current lease grant.

<a id="field-cursor-current"></a>
## `cursor/current`

- Required: `no`
- Shape: string

Last batch-level progress token committed for this lease.

<a id="field-terminal-reason"></a>
## `terminal/reason`

- Required: `no`
- Shape: string

Immutable closure reason required for a closed lease.

<a id="field-status-at"></a>
## `status/at`

- Required: `yes`
- Shape: string

Time this status projection was recorded.
