# Trace Event v1

Source schema: [`doc/schemas/trace-event.v1.schema.json`](../../schemas/trace-event.v1.schema.json)

Redacted P074 trace projection over an existing committed fact. The trace event is a read model, never a source of authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `trace-event.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`trace/event-id`](#field-trace-event-id) | `yes` | string |  |
| [`run/id`](#field-run-id) | `yes` | string |  |
| [`node/ref`](#field-node-ref) | `yes` | string |  |
| [`source/store`](#field-source-store) | `yes` | string |  |
| [`component/id`](#field-component-id) | `yes` | string |  |
| [`event/time`](#field-event-time) | `yes` | string |  |
| [`event/kind`](#field-event-kind) | `yes` | string |  |
| [`status`](#field-status) | `yes` | string |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |
| [`receipt/ref`](#field-receipt-ref) | `no` | string |  |
| [`effect/refs`](#field-effect-refs) | `no` | array |  |
| [`outcome/refs`](#field-outcome-refs) | `no` | array |  |
| [`detail/redacted`](#field-detail-redacted) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `trace-event.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-trace-event-id"></a>
## `trace/event-id`

- Required: `yes`
- Shape: string

<a id="field-run-id"></a>
## `run/id`

- Required: `yes`
- Shape: string

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: string

<a id="field-source-store"></a>
## `source/store`

- Required: `yes`
- Shape: string

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: string

<a id="field-event-time"></a>
## `event/time`

- Required: `yes`
- Shape: string

<a id="field-event-kind"></a>
## `event/kind`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: string

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

<a id="field-receipt-ref"></a>
## `receipt/ref`

- Required: `no`
- Shape: string

<a id="field-effect-refs"></a>
## `effect/refs`

- Required: `no`
- Shape: array

<a id="field-outcome-refs"></a>
## `outcome/refs`

- Required: `no`
- Shape: array

<a id="field-detail-redacted"></a>
## `detail/redacted`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
