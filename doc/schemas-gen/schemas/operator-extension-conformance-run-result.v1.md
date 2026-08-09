# Operator Extension Conformance Run Result V1

Source schema: [`doc/schemas/operator-extension-conformance-run-result.v1.schema.json`](../../schemas/operator-extension-conformance-run-result.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-conformance-run-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`report/ref`](#field-report-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`report/digest`](#field-report-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-conformance-run-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-report-ref"></a>
## `report/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-report-digest"></a>
## `report/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
