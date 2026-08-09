# Operator Extension Loose Import V1

Source schema: [`doc/schemas/operator-extension-loose-import.v1.schema.json`](../../schemas/operator-extension-loose-import.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-loose-import.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`root/id`](#field-root-id) | `yes` | string |  |
| [`relative/path`](#field-relative-path) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-loose-import.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-root-id"></a>
## `root/id`

- Required: `yes`
- Shape: string

<a id="field-relative-path"></a>
## `relative/path`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
