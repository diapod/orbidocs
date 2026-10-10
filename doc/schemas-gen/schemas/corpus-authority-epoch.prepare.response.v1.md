# Communication Epoch Preparation Response v1

Source schema: [`doc/schemas/corpus-authority-epoch.prepare.response.v1.schema.json`](../../schemas/corpus-authority-epoch.prepare.response.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-authority-epoch.prepare.response.v1` |  |
| [`preview`](#field-preview) | `yes` | ref: `corpus-authority-epoch.preview.v1.schema.json` |  |
| [`preview/digest`](#field-preview-digest) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-authority-epoch.prepare.response.v1`

<a id="field-preview"></a>
## `preview`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.preview.v1.schema.json`

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest`
