# NSE Hook Offer v1

Source schema: [`doc/schemas/nse-hook-offer.v1.schema.json`](../../schemas/nse-hook-offer.v1.schema.json)

Exact host-built offer for one NSE invocation. V1 freezes the select-llm-model payload.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-hook-offer.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | const: `select-llm-model` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`hook/class`](#field-hook-class) | `yes` | const: `select` |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`causal/ref`](#field-causal-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/bounds`](#field-backend-bounds) | `yes` | object |  |
| [`payload`](#field-payload) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`text`](#def-text) | string |  |
| [`text-array`](#def-text-array) | array |  |
| [`candidate`](#def-candidate) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-hook-offer.v1`

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

<a id="field-hook-class"></a>
## `hook/class`

- Required: `yes`
- Shape: const: `select`

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-causal-ref"></a>
## `causal/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-bounds"></a>
## `backend/bounds`

- Required: `yes`
- Shape: object

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: object

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

<a id="def-text-array"></a>
## `$defs.text-array`

- Shape: array

<a id="def-candidate"></a>
## `$defs.candidate`

- Shape: object
