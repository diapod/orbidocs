# NSE Hook Decision Proposal v1

Source schema: [`doc/schemas/nse-hook-decision.v1.schema.json`](../../schemas/nse-hook-decision.v1.schema.json)

Raw producer proposal bound to one exact NSE offer. Admission remains host-owned.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-hook-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | const: `select-llm-model` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`producer/ref`](#field-producer-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`producer/digest`](#field-producer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`outcome`](#field-outcome) | `yes` | object |  |
| [`annotations`](#field-annotations) | `no` | ref: `#/$defs/annotations` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`text`](#def-text) | string |  |
| [`reason`](#def-reason) | object |  |
| [`use-runtime`](#def-use-runtime) | object |  |
| [`annotations`](#def-annotations) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-hook-decision.v1`

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
- Shape: const: `select-llm-model`

<a id="field-hook-v"></a>
## `hook/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-producer-ref"></a>
## `producer/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-producer-digest"></a>
## `producer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: object

<a id="field-annotations"></a>
## `annotations`

- Required: `no`
- Shape: ref: `#/$defs/annotations`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-text"></a>
## `$defs.text`

- Shape: string

<a id="def-reason"></a>
## `$defs.reason`

- Shape: object

<a id="def-use-runtime"></a>
## `$defs.use-runtime`

- Shape: object

<a id="def-annotations"></a>
## `$defs.annotations`

- Shape: object
