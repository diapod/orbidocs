# Sensorium Interface Subscription Command v1

Source schema: [`doc/schemas/sensorium-interface-subscription-command.v1.schema.json`](../../schemas/sensorium-interface-subscription-command.v1.schema.json)

Caller-bound renewal or explicit closure of a Sensorium Interface lease.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-subscription-command.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`subscription/id`](#field-subscription-id) | `yes` | string | Caller-bound lease to mutate. |
| [`action`](#field-action) | `yes` | enum: `renew`, `close` | Requested lifecycle transition. |
| [`lease/requested-seconds`](#field-lease-requested-seconds) | `no` | integer | New bounded duration required only for renewal. |
| [`deadline/at`](#field-deadline-at) | `yes` | string | Absolute deadline for command admission. |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` | P081 context for traceability; never authority. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "action": {
      "const": "renew"
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "lease/requested-seconds"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-subscription-command.v1`

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

Caller-bound lease to mutate.

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `renew`, `close`

Requested lifecycle transition.

<a id="field-lease-requested-seconds"></a>
## `lease/requested-seconds`

- Required: `no`
- Shape: integer

New bounded duration required only for renewal.

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

Absolute deadline for command admission.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

P081 context for traceability; never authority.
