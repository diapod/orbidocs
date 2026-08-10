# Operator Attention Budget V1

Source schema: [`doc/schemas/operator-attention-budget.v1.schema.json`](../../schemas/operator-attention-budget.v1.schema.json)

Signed local budget for bounded human-in-the-loop prompts. Exhaustion can only group, defer, deny, or surface security visibility.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-attention-budget.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`budget/ref`](#field-budget-ref) | `yes` | string |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`request/classes`](#field-request-classes) | `yes` | array |  |
| [`timezone`](#field-timezone) | `yes` | string |  |
| [`availability/windows`](#field-availability-windows) | `yes` | array |  |
| [`window/seconds`](#field-window-seconds) | `yes` | integer |  |
| [`prompts/max`](#field-prompts-max) | `yes` | integer |  |
| [`group/max-items`](#field-group-max-items) | `yes` | integer |  |
| [`repeat/min-seconds`](#field-repeat-min-seconds) | `yes` | integer |  |
| [`request/timeout-seconds`](#field-request-timeout-seconds) | `yes` | integer |  |
| [`outside-window`](#field-outside-window) | `yes` | enum: `defer`, `deny` |  |
| [`overflow`](#field-overflow) | `yes` | enum: `group`, `defer`, `deny` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-attention-budget.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-budget-ref"></a>
## `budget/ref`

- Required: `yes`
- Shape: string

<a id="field-revision-no"></a>
## `revision/no`

- Required: `yes`
- Shape: integer

<a id="field-request-classes"></a>
## `request/classes`

- Required: `yes`
- Shape: array

<a id="field-timezone"></a>
## `timezone`

- Required: `yes`
- Shape: string

<a id="field-availability-windows"></a>
## `availability/windows`

- Required: `yes`
- Shape: array

<a id="field-window-seconds"></a>
## `window/seconds`

- Required: `yes`
- Shape: integer

<a id="field-prompts-max"></a>
## `prompts/max`

- Required: `yes`
- Shape: integer

<a id="field-group-max-items"></a>
## `group/max-items`

- Required: `yes`
- Shape: integer

<a id="field-repeat-min-seconds"></a>
## `repeat/min-seconds`

- Required: `yes`
- Shape: integer

<a id="field-request-timeout-seconds"></a>
## `request/timeout-seconds`

- Required: `yes`
- Shape: integer

<a id="field-outside-window"></a>
## `outside-window`

- Required: `yes`
- Shape: enum: `defer`, `deny`

<a id="field-overflow"></a>
## `overflow`

- Required: `yes`
- Shape: enum: `group`, `defer`, `deny`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
