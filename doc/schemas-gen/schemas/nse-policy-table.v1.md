# NSE Policy Table v1

Source schema: [`doc/schemas/nse-policy-table.v1.schema.json`](../../schemas/nse-policy-table.v1.schema.json)

Deterministic closed ordered rule table for select-llm-model V1.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-policy-table.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`policy/name`](#field-policy-name) | `yes` | ref: `#/$defs/text` |  |
| [`hook/id`](#field-hook-id) | `yes` | const: `select-llm-model` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`rules`](#field-rules) | `yes` | array |  |
| [`default/decision`](#field-default-decision) | `yes` | ref: `#/$defs/default-decision` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`text`](#def-text) | string |  |
| [`field`](#def-field) | enum: `purpose`, `context/token-estimate`, `candidate/provider`, `candidate/transport-kind`, `candidate/location`, `candidate/parameter-count`, `candidate/runtime-ref`, `candidate/capability` |  |
| [`predicate`](#def-predicate) | object |  |
| [`rule-decision`](#def-rule-decision) | unspecified |  |
| [`default-decision`](#def-default-decision) | unspecified |  |
| [`select-runtime`](#def-select-runtime) | object |  |
| [`defer`](#def-defer) | object |  |
| [`reject`](#def-reject) | object |  |
| [`rule`](#def-rule) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-policy-table.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-policy-name"></a>
## `policy/name`

- Required: `yes`
- Shape: ref: `#/$defs/text`

<a id="field-hook-id"></a>
## `hook/id`

- Required: `yes`
- Shape: const: `select-llm-model`

<a id="field-hook-v"></a>
## `hook/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-rules"></a>
## `rules`

- Required: `yes`
- Shape: array

<a id="field-default-decision"></a>
## `default/decision`

- Required: `yes`
- Shape: ref: `#/$defs/default-decision`

## Definition Semantics

<a id="def-text"></a>
## `$defs.text`

- Shape: string

<a id="def-field"></a>
## `$defs.field`

- Shape: enum: `purpose`, `context/token-estimate`, `candidate/provider`, `candidate/transport-kind`, `candidate/location`, `candidate/parameter-count`, `candidate/runtime-ref`, `candidate/capability`

<a id="def-predicate"></a>
## `$defs.predicate`

- Shape: object

<a id="def-rule-decision"></a>
## `$defs.rule-decision`

- Shape: unspecified

<a id="def-default-decision"></a>
## `$defs.default-decision`

- Shape: unspecified

<a id="def-select-runtime"></a>
## `$defs.select-runtime`

- Shape: object

<a id="def-defer"></a>
## `$defs.defer`

- Shape: object

<a id="def-reject"></a>
## `$defs.reject`

- Shape: object

<a id="def-rule"></a>
## `$defs.rule`

- Shape: object
