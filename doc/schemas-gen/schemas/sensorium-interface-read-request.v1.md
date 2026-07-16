# Sensorium Interface Read Request v1

Source schema: [`doc/schemas/sensorium-interface-read-request.v1.schema.json`](../../schemas/sensorium-interface-read-request.v1.schema.json)

Bounded one-shot or subscription read-next request.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-read-request.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`interface/id`](#field-interface-id) | `yes` | string | Interface resource to read. |
| [`delivery/kind`](#field-delivery-kind) | `yes` | enum: `one-shot`, `subscription` | Selects direct read or caller-bound leased read-next semantics. |
| [`subscription/id`](#field-subscription-id) | `no` | string | Required caller-bound lease for subscription delivery. |
| [`cursor/after`](#field-cursor-after) | `no` | string | Opaque interface- and source-generation-bound progress token. |
| [`batch`](#field-batch) | `yes` | ref: `#/$defs/BatchLimits` | Caller-requested bounds narrowed by descriptor and host ceilings. |
| [`deadline/at`](#field-deadline-at) | `yes` | string | Absolute deadline by which admission and bounded observation must complete. |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` | P081 context for traceability; never authority. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`BatchLimits`](#def-batchlimits) | object | Independent frame-count, byte, and wait ceilings for one batch. |

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
    "subscription/id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-read-request.v1`

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

Interface resource to read.

<a id="field-delivery-kind"></a>
## `delivery/kind`

- Required: `yes`
- Shape: enum: `one-shot`, `subscription`

Selects direct read or caller-bound leased read-next semantics.

<a id="field-subscription-id"></a>
## `subscription/id`

- Required: `no`
- Shape: string

Required caller-bound lease for subscription delivery.

<a id="field-cursor-after"></a>
## `cursor/after`

- Required: `no`
- Shape: string

Opaque interface- and source-generation-bound progress token.

<a id="field-batch"></a>
## `batch`

- Required: `yes`
- Shape: ref: `#/$defs/BatchLimits`

Caller-requested bounds narrowed by descriptor and host ceilings.

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

Absolute deadline by which admission and bounded observation must complete.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

P081 context for traceability; never authority.

## Definition Semantics

<a id="def-batchlimits"></a>
## `$defs.BatchLimits`

- Shape: object

Independent frame-count, byte, and wait ceilings for one batch.
