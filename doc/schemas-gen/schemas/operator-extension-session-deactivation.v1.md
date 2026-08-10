# Operator Extension Session Deactivation V1

Source schema: [`doc/schemas/operator-extension-session-deactivation.v1.schema.json`](../../schemas/operator-extension-session-deactivation.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-session-deactivation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`activation/ref`](#field-activation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`reason`](#field-reason) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-session-deactivation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-activation-ref"></a>
## `activation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
