# Operator Extension Transition V1

Source schema: [`doc/schemas/operator-extension-transition.v1.schema.json`](../../schemas/operator-extension-transition.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-transition.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`transition/ref`](#field-transition-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`activation/ref`](#field-activation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`kind`](#field-kind) | `yes` | enum: `activate`, `revoke`, `rollback`, `safe-mode` |  |
| [`state`](#field-state) | `yes` | enum: `planned`, `committed`, `finalized`, `failed` |  |
| [`expected/generation`](#field-expected-generation) | `yes` | integer |  |
| [`target/generation`](#field-target-generation) | `yes` | integer |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-transition.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-transition-ref"></a>
## `transition/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-activation-ref"></a>
## `activation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `activate`, `revoke`, `rollback`, `safe-mode`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `planned`, `committed`, `finalized`, `failed`

<a id="field-expected-generation"></a>
## `expected/generation`

- Required: `yes`
- Shape: integer

<a id="field-target-generation"></a>
## `target/generation`

- Required: `yes`
- Shape: integer

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
