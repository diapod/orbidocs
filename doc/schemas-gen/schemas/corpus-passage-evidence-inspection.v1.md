# Corpus Passage Evidence Inspection v1

Source schema: [`doc/schemas/corpus-passage-evidence-inspection.v1.schema.json`](../../schemas/corpus-passage-evidence-inspection.v1.schema.json)

The operator's view of one passage's evidence: its binding fact and the manifest it names.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-passage-evidence-inspection.v1` |  |
| [`binding`](#field-binding) | `yes` | ref: `corpus-passage-evidence-binding.v1.schema.json` |  |
| [`manifest`](#field-manifest) | `yes` | ref: `corpus-passage-evidence-manifest.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-passage-evidence-inspection.v1`

<a id="field-binding"></a>
## `binding`

- Required: `yes`
- Shape: ref: `corpus-passage-evidence-binding.v1.schema.json`

<a id="field-manifest"></a>
## `manifest`

- Required: `yes`
- Shape: ref: `corpus-passage-evidence-manifest.v1.schema.json`
