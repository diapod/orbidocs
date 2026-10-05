# Operator Task Recipe Draft v1

Source schema: [`doc/schemas/operator-task-recipe-draft.v1.schema.json`](../../schemas/operator-task-recipe-draft.v1.schema.json)

Read-only exact recipe preview. The digest is SHA-256 of recipe JCS v1 bytes, not approval, publication or execution authority.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-recipe-draft.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recipe/digest`](#field-recipe-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`recipe`](#field-recipe) | `yes` | ref: `operator-task-verified-recipe.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-recipe-draft.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recipe-digest"></a>
## `recipe/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-recipe"></a>
## `recipe`

- Required: `yes`
- Shape: ref: `operator-task-verified-recipe.v1.schema.json`
