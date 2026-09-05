# Corpus Agent Answer Draft v2

Source schema: [`doc/schemas/corpus-agent-answer-draft.v2.schema.json`](../../schemas/corpus-agent-answer-draft.v2.schema.json)

Exact inert draft and admitted Agent outcome with content-bound derived provenance. Neither source labels nor provenance grant publication authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-agent-answer-draft.v2` |  |
| [`draft`](#field-draft) | `yes` | ref: `corpus-agent-answer-draft.v1.schema.json` |  |
| [`owner/node-id`](#field-owner-node-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`source/outcome`](#field-source-outcome) | `yes` | unspecified |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-agent-answer-draft.v2`

<a id="field-draft"></a>
## `draft`

- Required: `yes`
- Shape: ref: `corpus-agent-answer-draft.v1.schema.json`

<a id="field-owner-node-id"></a>
## `owner/node-id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-source-outcome"></a>
## `source/outcome`

- Required: `yes`
- Shape: unspecified

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
