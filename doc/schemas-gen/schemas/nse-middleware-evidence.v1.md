# NSE Middleware Evidence V1

Source schema: [`doc/schemas/nse-middleware-evidence.v1.schema.json`](../../schemas/nse-middleware-evidence.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-middleware-evidence.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | string |  |
| [`hook/v`](#field-hook-v) | `yes` | integer |  |
| [`module/ref`](#field-module-ref) | `yes` | string |  |
| [`package/digest`](#field-package-digest) | `yes` | string |  |
| [`grant/refs`](#field-grant-refs) | `yes` | array |  |
| [`input/schema`](#field-input-schema) | `yes` | string |  |
| [`output/schema`](#field-output-schema) | `yes` | const: `nse-middleware-evidence.v1` |  |
| [`timeout/ms`](#field-timeout-ms) | `yes` | integer |  |
| [`input/max-bytes`](#field-input-max-bytes) | `yes` | integer |  |
| [`output/max-bytes`](#field-output-max-bytes) | `yes` | integer |  |
| [`causal/ref`](#field-causal-ref) | `yes` | string |  |
| [`offer/fields`](#field-offer-fields) | `yes` | array |  |
| [`evidence`](#field-evidence) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`target`](#def-target) | enum: `candidate-provider`, `candidate-transport-kind`, `candidate-location`, `candidate-parameter-count`, `candidate-runtime-ref`, `candidate-capability` |  |
| [`value`](#def-value) | unspecified |  |
| [`candidate_ref`](#def-candidate-ref) | string |  |
| [`evidence_item`](#def-evidence-item) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-middleware-evidence.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invocation-ref"></a>
## `invocation/ref`

- Required: `yes`
- Shape: string

<a id="field-hook-id"></a>
## `hook/id`

- Required: `yes`
- Shape: string

<a id="field-hook-v"></a>
## `hook/v`

- Required: `yes`
- Shape: integer

<a id="field-module-ref"></a>
## `module/ref`

- Required: `yes`
- Shape: string

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: string

<a id="field-grant-refs"></a>
## `grant/refs`

- Required: `yes`
- Shape: array

<a id="field-input-schema"></a>
## `input/schema`

- Required: `yes`
- Shape: string

<a id="field-output-schema"></a>
## `output/schema`

- Required: `yes`
- Shape: const: `nse-middleware-evidence.v1`

<a id="field-timeout-ms"></a>
## `timeout/ms`

- Required: `yes`
- Shape: integer

<a id="field-input-max-bytes"></a>
## `input/max-bytes`

- Required: `yes`
- Shape: integer

<a id="field-output-max-bytes"></a>
## `output/max-bytes`

- Required: `yes`
- Shape: integer

<a id="field-causal-ref"></a>
## `causal/ref`

- Required: `yes`
- Shape: string

<a id="field-offer-fields"></a>
## `offer/fields`

- Required: `yes`
- Shape: array

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-target"></a>
## `$defs.target`

- Shape: enum: `candidate-provider`, `candidate-transport-kind`, `candidate-location`, `candidate-parameter-count`, `candidate-runtime-ref`, `candidate-capability`

<a id="def-value"></a>
## `$defs.value`

- Shape: unspecified

<a id="def-candidate-ref"></a>
## `$defs.candidate_ref`

- Shape: string

<a id="def-evidence-item"></a>
## `$defs.evidence_item`

- Shape: unspecified
