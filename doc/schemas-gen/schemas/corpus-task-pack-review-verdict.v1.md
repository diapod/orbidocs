# Corpus Task-pack Review Verdict v1

Source schema: [`doc/schemas/corpus-task-pack-review-verdict.v1.schema.json`](../../schemas/corpus-task-pack-review-verdict.v1.schema.json)

What a reviewer passage produces about one task-pack candidate (P094-023b): a verdict and bounded findings. It is the model's output, never a signed fact: the host's Corpus adapter derives the signed review from it, with the reviewer, node, turn, proposal and evidence taken from admitted facts.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-review-verdict.v1` |  |
| [`verdict`](#field-verdict) | `yes` | enum: `accept`, `reject`, `request-regeneration` |  |
| [`findings`](#field-findings) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-review-verdict.v1`

<a id="field-verdict"></a>
## `verdict`

- Required: `yes`
- Shape: enum: `accept`, `reject`, `request-regeneration`

<a id="field-findings"></a>
## `findings`

- Required: `yes`
- Shape: array
