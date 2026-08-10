# Operator Extension Inspection V1

Source schema: [`doc/schemas/operator-extension-inspection.v1.schema.json`](../../schemas/operator-extension-inspection.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-inspection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`safe-mode/active`](#field-safe-mode-active) | `yes` | boolean |  |
| [`packages`](#field-packages) | `yes` | array |  |
| [`policies`](#field-policies) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`optional-ref`](#def-optional-ref) | unspecified |  |
| [`producer`](#def-producer) | object |  |
| [`policy-status`](#def-policy-status) | object |  |
| [`package-status`](#def-package-status) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-inspection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-safe-mode-active"></a>
## `safe-mode/active`

- Required: `yes`
- Shape: boolean

<a id="field-packages"></a>
## `packages`

- Required: `yes`
- Shape: array

<a id="field-policies"></a>
## `policies`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-optional-ref"></a>
## `$defs.optional-ref`

- Shape: unspecified

<a id="def-producer"></a>
## `$defs.producer`

- Shape: object

<a id="def-policy-status"></a>
## `$defs.policy-status`

- Shape: object

<a id="def-package-status"></a>
## `$defs.package-status`

- Shape: object
