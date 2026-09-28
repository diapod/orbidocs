# Operator Task HIL Status v1

Source schema: [`doc/schemas/operator-task-hil-status.v1.schema.json`](../../schemas/operator-task-hil-status.v1.schema.json)

The HIL requests of one plan and where each stands: `pending` with the delivery outcome when this call completed initial or interrupted delivery (`delivery` is absent when completion was already recorded), `decided` with the recorded decision, or `expired`. The attention gate never approves.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`requests`](#field-requests) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-requests"></a>
## `requests`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
