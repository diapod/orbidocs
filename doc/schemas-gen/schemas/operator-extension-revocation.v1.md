# Operator Extension Revocation V1

Source schema: [`doc/schemas/operator-extension-revocation.v1.schema.json`](../../schemas/operator-extension-revocation.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-revocation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`revocation/ref`](#field-revocation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`expected/generation`](#field-expected-generation) | `yes` | integer |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`reason`](#field-reason) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-revocation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-revocation-ref"></a>
## `revocation/ref`

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

<a id="field-expected-generation"></a>
## `expected/generation`

- Required: `yes`
- Shape: integer

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

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

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
