# Operator Extension Durable Activation V1

Source schema: [`doc/schemas/operator-extension-activation.v1.schema.json`](../../schemas/operator-extension-activation.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-activation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`activation/ref`](#field-activation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | const: `durable` |  |
| [`operational/class`](#field-operational-class) | `yes` | ref: `#/$defs/class` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`conformance/report-ref`](#field-conformance-report-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`conformance/report-digest`](#field-conformance-report-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`producers`](#field-producers) | `yes` | array |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`class`](#def-class) | enum: `research`, `experimental`, `test`, `production`, `critical` |  |
| [`signature`](#def-signature) | object |  |
| [`producer`](#def-producer) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-activation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-activation-ref"></a>
## `activation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: const: `durable`

<a id="field-operational-class"></a>
## `operational/class`

- Required: `yes`
- Shape: ref: `#/$defs/class`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-conformance-report-ref"></a>
## `conformance/report-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-conformance-report-digest"></a>
## `conformance/report-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-producers"></a>
## `producers`

- Required: `yes`
- Shape: array

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-class"></a>
## `$defs.class`

- Shape: enum: `research`, `experimental`, `test`, `production`, `critical`

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-producer"></a>
## `$defs.producer`

- Shape: object
