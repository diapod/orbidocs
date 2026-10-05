# Operator Task Verified Recipe v1

Source schema: [`doc/schemas/operator-task-verified-recipe.v1.schema.json`](../../schemas/operator-task-verified-recipe.v1.schema.json)

A bounded mechanical projection of one exact locally verified execution, its candidate and patch bytes, and retained signed Solver/Reviewer/Chair history. It is not another inference, permission to run the recipe, or a universal Corpus outcome format. The owner verifies all content addresses, signatures, source relationships and confirmed disposal before publication; the complete JCS document must fit the 65536-byte answer limit, with no truncation. Inference assertions name the exact retained Agent V2 products used in the publication's provenance composition.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-verified-recipe.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`source`](#field-source) | `yes` | ref: `#/$defs/source` |  |
| [`candidate`](#field-candidate) | `yes` | ref: `operator-task-experiment-candidate.v1.schema.json` |  |
| [`patches`](#field-patches) | `yes` | array |  |
| [`verified`](#field-verified) | `yes` | object |  |
| [`history`](#field-history) | `yes` | array |  |
| [`inputs/assertions`](#field-inputs-assertions) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`source`](#def-source) | object |  |
| [`proposal`](#def-proposal) | object |  |
| [`review`](#def-review) | object |  |
| [`decision`](#def-decision) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-verified-recipe.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `#/$defs/source`

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: ref: `operator-task-experiment-candidate.v1.schema.json`

<a id="field-patches"></a>
## `patches`

- Required: `yes`
- Shape: array

<a id="field-verified"></a>
## `verified`

- Required: `yes`
- Shape: object

<a id="field-history"></a>
## `history`

- Required: `yes`
- Shape: array

<a id="field-inputs-assertions"></a>
## `inputs/assertions`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-source"></a>
## `$defs.source`

- Shape: object

<a id="def-proposal"></a>
## `$defs.proposal`

- Shape: object

<a id="def-review"></a>
## `$defs.review`

- Shape: object

<a id="def-decision"></a>
## `$defs.decision`

- Shape: object
