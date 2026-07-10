# Execution Receipt v1

Source schema: [`doc/schemas/execution-receipt.v1.schema.json`](../../schemas/execution-receipt.v1.schema.json)

Immutable host-observed transition receipt linking causal context to domain-owned effect and outcome refs.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `execution-receipt.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`receipt/id`](#field-receipt-id) | `yes` | string |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`transition/from`](#field-transition-from) | `yes` | ref: `#/$defs/transition` |  |
| [`transition/to`](#field-transition-to) | `yes` | ref: `#/$defs/transition` |  |
| [`attempt/no`](#field-attempt-no) | `yes` | integer |  |
| [`recorded/by`](#field-recorded-by) | `yes` | ref: `#/$defs/ref` |  |
| [`recorded/at`](#field-recorded-at) | `yes` | string |  |
| [`policy/decision-ref`](#field-policy-decision-ref) | `no` | ref: `#/$defs/ref` |  |
| [`effect/refs`](#field-effect-refs) | `no` | array |  |
| [`outcome/refs`](#field-outcome-refs) | `no` | array |  |
| [`previous/receipt-ref`](#field-previous-receipt-ref) | `no` | string |  |
| [`diagnostics`](#field-diagnostics) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`transition`](#def-transition) | enum: `proposed`, `accepted`, `rejected`, `deferred`, `running`, `completed`, `failed`, `cancelled`, `timed-out`, `superseded` |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `execution-receipt.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-receipt-id"></a>
## `receipt/id`

- Required: `yes`
- Shape: string

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-transition-from"></a>
## `transition/from`

- Required: `yes`
- Shape: ref: `#/$defs/transition`

<a id="field-transition-to"></a>
## `transition/to`

- Required: `yes`
- Shape: ref: `#/$defs/transition`

<a id="field-attempt-no"></a>
## `attempt/no`

- Required: `yes`
- Shape: integer

<a id="field-recorded-by"></a>
## `recorded/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-recorded-at"></a>
## `recorded/at`

- Required: `yes`
- Shape: string

<a id="field-policy-decision-ref"></a>
## `policy/decision-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-effect-refs"></a>
## `effect/refs`

- Required: `no`
- Shape: array

<a id="field-outcome-refs"></a>
## `outcome/refs`

- Required: `no`
- Shape: array

<a id="field-previous-receipt-ref"></a>
## `previous/receipt-ref`

- Required: `no`
- Shape: string

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-transition"></a>
## `$defs.transition`

- Shape: enum: `proposed`, `accepted`, `rejected`, `deferred`, `running`, `completed`, `failed`, `cancelled`, `timed-out`, `superseded`

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
