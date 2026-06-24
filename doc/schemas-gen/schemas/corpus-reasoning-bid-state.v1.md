# Corpus Reasoning Bid State v1

Source schema: [`doc/schemas/corpus-reasoning-bid-state.v1.schema.json`](../../schemas/corpus-reasoning-bid-state.v1.schema.json)

Requester-owned read model for Corpus procurement candidates. This projection is operator-visible state, not an authority or provider wire artifact.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`owner/node-id`](#field-owner-node-id) | `yes` | string |  |
| [`updated-at`](#field-updated-at) | `yes` | string |  |
| [`candidates`](#field-candidates) | `yes` | array |  |
| [`selected/bid-id`](#field-selected-bid-id) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`candidate_state`](#def-candidate-state) | object |  |
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-owner-node-id"></a>
## `owner/node-id`

- Required: `yes`
- Shape: string

<a id="field-updated-at"></a>
## `updated-at`

- Required: `yes`
- Shape: string

<a id="field-candidates"></a>
## `candidates`

- Required: `yes`
- Shape: array

<a id="field-selected-bid-id"></a>
## `selected/bid-id`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `#/$defs/extensions`

## Definition Semantics

<a id="def-candidate-state"></a>
## `$defs.candidate_state`

- Shape: object

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
