# Corpus Task-pack Review Verdict v1

Source schema: [`doc/schemas/corpus-task-pack-review-verdict.v1.schema.json`](../../schemas/corpus-task-pack-review-verdict.v1.schema.json)

What a reviewer passage produces about one task-pack candidate (P094-023b): a verdict and bounded findings. It is the model's output, never a signed fact: the host's Corpus adapter derives the signed review from it, with the reviewer, node, turn, proposal and evidence taken from admitted facts.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-review-verdict.v1` |  |
| [`verdict`](#field-verdict) | `yes` | enum: `accept`, `reject`, `request-regeneration` |  |
| [`reviewed/patches`](#field-reviewed-patches) | `yes` | ref: `#/$defs/patches` |  |
| [`findings`](#field-findings) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`patches`](#def-patches) | array | Structured coverage claims, not a host verdict on reasoning quality. Acceptance must cover every exact candidate patch/file; an observation has an empty array. The owner compares identities and resulting byte digests, and binds finding indices, before signing or publication. |
| [`file`](#def-file) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-review-verdict.v1`

<a id="field-verdict"></a>
## `verdict`

- Required: `yes`
- Shape: enum: `accept`, `reject`, `request-regeneration`

<a id="field-reviewed-patches"></a>
## `reviewed/patches`

- Required: `yes`
- Shape: ref: `#/$defs/patches`

<a id="field-findings"></a>
## `findings`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-patches"></a>
## `$defs.patches`

- Shape: array

Structured coverage claims, not a host verdict on reasoning quality. Acceptance must cover every exact candidate patch/file; an observation has an empty array. The owner compares identities and resulting byte digests, and binds finding indices, before signing or publication.

<a id="def-file"></a>
## `$defs.file`

- Shape: object
