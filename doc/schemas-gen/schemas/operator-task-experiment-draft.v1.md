# Operator Task Experiment Draft v1

Source schema: [`doc/schemas/operator-task-experiment-draft.v1.schema.json`](../../schemas/operator-task-experiment-draft.v1.schema.json)

Inert Solver-authored publication input, not a plan. The host reads it only from the exact retained Agent product. Each attachment names exactly one patch step; that step must name draft-patch:<step/id> and the same patch-policy/ref. The host validates all material and derives content addresses before publication. Total decoded written content is at most 1 MiB, across all attachments; enclosing product and evidence budgets also apply. Independent review, plan policy admission and HIL remain mandatory.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-experiment-draft.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`candidate`](#field-candidate) | `yes` | ref: `operator-task-experiment-candidate.v1.schema.json` |  |
| [`patches`](#field-patches) | `yes` | array | Ordered attachments. Semantic admission rejects duplicate or missing step ids, unconsumed local refs and ref/policy substitution. Empty for observation-only drafts. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`text-patch`](#def-text-patch) | object | Write-only authoring representation, converted to the unchanged operator-task-patch.v1. No content selection or normalization; use patch for binary files or deletion. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-experiment-draft.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: ref: `operator-task-experiment-candidate.v1.schema.json`

<a id="field-patches"></a>
## `patches`

- Required: `yes`
- Shape: array

Ordered attachments. Semantic admission rejects duplicate or missing step ids, unconsumed local refs and ref/policy substitution. Empty for observation-only drafts.

## Definition Semantics

<a id="def-text-patch"></a>
## `$defs.text-patch`

- Shape: object

Write-only authoring representation, converted to the unchanged operator-task-patch.v1. No content selection or normalization; use patch for binary files or deletion.
