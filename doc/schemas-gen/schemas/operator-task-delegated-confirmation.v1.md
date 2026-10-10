# Operator-task-delegated-confirmation.v1

Source schema: [`doc/schemas/operator-task-delegated-confirmation.v1.schema.json`](../../schemas/operator-task-delegated-confirmation.v1.schema.json)

A delegated confirmation, not independent human HIL. Exact subject bytes and actual local executor are retained before the owner's effect; replay rechecks current authority.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-delegated-confirmation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`confirmation/ref`](#field-confirmation-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`mandate/ref`](#field-mandate-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`action`](#field-action) | `yes` | enum: `model-turn`, `communication`, `chair-admit-reviewed`, `experiment-plan`, `experiment-step` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`subject/digest`](#field-subject-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`answered/by`](#field-answered-by) | `yes` | const: `local-executor:task-pack-delegate` |  |
| [`authorized/by`](#field-authorized-by) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`confirmed-at`](#field-confirmed-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | const: `delegated` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-delegated-confirmation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-confirmation-ref"></a>
## `confirmation/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-mandate-ref"></a>
## `mandate/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `model-turn`, `communication`, `chair-admit-reviewed`, `experiment-plan`, `experiment-step`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-subject-digest"></a>
## `subject/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-answered-by"></a>
## `answered/by`

- Required: `yes`
- Shape: const: `local-executor:task-pack-delegate`

<a id="field-authorized-by"></a>
## `authorized/by`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-confirmed-at"></a>
## `confirmed-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `yes`
- Shape: const: `delegated`
