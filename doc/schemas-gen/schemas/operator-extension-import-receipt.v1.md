# Operator Extension Import Receipt V1

Source schema: [`doc/schemas/operator-extension-import-receipt.v1.schema.json`](../../schemas/operator-extension-import-receipt.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-import-receipt.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`signer/key-public`](#field-signer-key-public) | `yes` | string |  |
| [`container/mode`](#field-container-mode) | `yes` | const: `loose-file-import` |  |
| [`distribution/eligible`](#field-distribution-eligible) | `yes` | const: `False` |  |
| [`activated`](#field-activated) | `yes` | const: `False` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-import-receipt.v1`

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

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-signer-key-public"></a>
## `signer/key-public`

- Required: `yes`
- Shape: string

<a id="field-container-mode"></a>
## `container/mode`

- Required: `yes`
- Shape: const: `loose-file-import`

<a id="field-distribution-eligible"></a>
## `distribution/eligible`

- Required: `yes`
- Shape: const: `False`

<a id="field-activated"></a>
## `activated`

- Required: `yes`
- Shape: const: `False`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
