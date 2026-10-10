# Operator-task-delegation-preview.v1

Source schema: [`doc/schemas/operator-task-delegation-preview.v1.schema.json`](../../schemas/operator-task-delegation-preview.v1.schema.json)

Host-retained exact approval document and its expiry. Commitment covers document and preview deadline.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-delegation-preview.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`preview/ref`](#field-preview-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`preview/digest`](#field-preview-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`document`](#field-document) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-delegation-preview.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-document"></a>
## `document`

- Required: `yes`
- Shape: unspecified
