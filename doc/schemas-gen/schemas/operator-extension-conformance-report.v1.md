# Operator Extension Conformance Report V1

Source schema: [`doc/schemas/operator-extension-conformance-report.v1.schema.json`](../../schemas/operator-extension-conformance-report.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-conformance-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`report/ref`](#field-report-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`refusal-corpus/ref`](#field-refusal-corpus-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`refusal-corpus/digest`](#field-refusal-corpus-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`runtime/digest`](#field-runtime-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`positive/passed`](#field-positive-passed) | `yes` | integer |  |
| [`positive/total`](#field-positive-total) | `yes` | integer |  |
| [`refusal/status`](#field-refusal-status) | `yes` | enum: `passed`, `failed` |  |
| [`refusal/passed`](#field-refusal-passed) | `yes` | integer |  |
| [`refusal/total`](#field-refusal-total) | `yes` | integer |  |
| [`report/digest`](#field-report-digest) | `yes` | ref: `#/$defs/digest` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-conformance-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-report-ref"></a>
## `report/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-refusal-corpus-ref"></a>
## `refusal-corpus/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-refusal-corpus-digest"></a>
## `refusal-corpus/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-runtime-digest"></a>
## `runtime/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-positive-passed"></a>
## `positive/passed`

- Required: `yes`
- Shape: integer

<a id="field-positive-total"></a>
## `positive/total`

- Required: `yes`
- Shape: integer

<a id="field-refusal-status"></a>
## `refusal/status`

- Required: `yes`
- Shape: enum: `passed`, `failed`

<a id="field-refusal-passed"></a>
## `refusal/passed`

- Required: `yes`
- Shape: integer

<a id="field-refusal-total"></a>
## `refusal/total`

- Required: `yes`
- Shape: integer

<a id="field-report-digest"></a>
## `report/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
