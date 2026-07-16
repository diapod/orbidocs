# Sensorium Interface Subscribe Request v1

Source schema: [`doc/schemas/sensorium-interface-subscribe-request.v1.schema.json`](../../schemas/sensorium-interface-subscribe-request.v1.schema.json)

Request to create a caller-bound, bounded Sensorium Interface lease.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-subscribe-request.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`interface/id`](#field-interface-id) | `yes` | string | Interface resource to subscribe to. |
| [`cursor/after`](#field-cursor-after) | `no` | string | Optional resume point bound to this interface and source generation. |
| [`lease/requested-seconds`](#field-lease-requested-seconds) | `yes` | integer | Requested lease duration before descriptor, grant, and host narrowing. |
| [`batch`](#field-batch) | `yes` | object | Default read-next bounds retained by the lease. |
| [`deadline/at`](#field-deadline-at) | `yes` | string | Absolute deadline for subscription admission. |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` | P081 context for traceability; never authority. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-subscribe-request.v1`

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

Interface resource to subscribe to.

<a id="field-cursor-after"></a>
## `cursor/after`

- Required: `no`
- Shape: string

Optional resume point bound to this interface and source generation.

<a id="field-lease-requested-seconds"></a>
## `lease/requested-seconds`

- Required: `yes`
- Shape: integer

Requested lease duration before descriptor, grant, and host narrowing.

<a id="field-batch"></a>
## `batch`

- Required: `yes`
- Shape: object

Default read-next bounds retained by the lease.

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

Absolute deadline for subscription admission.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

P081 context for traceability; never authority.
