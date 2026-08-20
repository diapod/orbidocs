# Operator Experiment Package V1

Source schema: [`doc/schemas/operator-experiment-package.v1.schema.json`](../../schemas/operator-experiment-package.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-experiment-package.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`middleware-package/ref`](#field-middleware-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`middleware-package/digest`](#field-middleware-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`hooks`](#field-hooks) | `yes` | array | Hook registrations identify producers only. Generic scalar/profile decisions use nse-policy-table.v1; Corpus target-free turn ordering uses the separate nse-select-turn-order-table.v1 contract. |
| [`semantic-entries`](#field-semantic-entries) | `no` | array |  |
| [`inference-flows`](#field-inference-flows) | `no` | array |  |
| [`compatibility`](#field-compatibility) | `no` | ref: `#/$defs/compatibility` |  |
| [`required-capability/ids`](#field-required-capability-ids) | `yes` | ref: `#/$defs/refs` |  |
| [`resource-envelope/refs`](#field-resource-envelope-refs) | `no` | ref: `#/$defs/refs` |  |
| [`derived-capability/refs`](#field-derived-capability-refs) | `no` | ref: `#/$defs/refs` |  |
| [`refusal-corpus/ref`](#field-refusal-corpus-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`refusal-corpus/digest`](#field-refusal-corpus-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`rollback/ref`](#field-rollback-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operational/class`](#field-operational-class) | `yes` | enum: `research`, `experimental`, `test`, `production`, `critical` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`refs`](#def-refs) | array |  |
| [`compatibility`](#def-compatibility) | object |  |
| [`hook`](#def-hook) | object |  |
| [`semantic-entry`](#def-semantic-entry) | object |  |
| [`inference-flow`](#def-inference-flow) | object |  |
| [`semantic-digest`](#def-semantic-digest) | string |  |
| [`profile-refs`](#def-profile-refs) | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-experiment-package.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-middleware-package-ref"></a>
## `middleware-package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-middleware-package-digest"></a>
## `middleware-package/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-hooks"></a>
## `hooks`

- Required: `yes`
- Shape: array

Hook registrations identify producers only. Generic scalar/profile decisions use nse-policy-table.v1; Corpus target-free turn ordering uses the separate nse-select-turn-order-table.v1 contract.

<a id="field-semantic-entries"></a>
## `semantic-entries`

- Required: `no`
- Shape: array

<a id="field-inference-flows"></a>
## `inference-flows`

- Required: `no`
- Shape: array

<a id="field-compatibility"></a>
## `compatibility`

- Required: `no`
- Shape: ref: `#/$defs/compatibility`

<a id="field-required-capability-ids"></a>
## `required-capability/ids`

- Required: `yes`
- Shape: ref: `#/$defs/refs`

<a id="field-resource-envelope-refs"></a>
## `resource-envelope/refs`

- Required: `no`
- Shape: ref: `#/$defs/refs`

<a id="field-derived-capability-refs"></a>
## `derived-capability/refs`

- Required: `no`
- Shape: ref: `#/$defs/refs`

<a id="field-refusal-corpus-ref"></a>
## `refusal-corpus/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-refusal-corpus-digest"></a>
## `refusal-corpus/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-rollback-ref"></a>
## `rollback/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operational-class"></a>
## `operational/class`

- Required: `yes`
- Shape: enum: `research`, `experimental`, `test`, `production`, `critical`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-refs"></a>
## `$defs.refs`

- Shape: array

<a id="def-compatibility"></a>
## `$defs.compatibility`

- Shape: object

<a id="def-hook"></a>
## `$defs.hook`

- Shape: object

<a id="def-semantic-entry"></a>
## `$defs.semantic-entry`

- Shape: object

<a id="def-inference-flow"></a>
## `$defs.inference-flow`

- Shape: object

<a id="def-semantic-digest"></a>
## `$defs.semantic-digest`

- Shape: string

<a id="def-profile-refs"></a>
## `$defs.profile-refs`

- Shape: array
