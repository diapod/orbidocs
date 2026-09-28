# Operator Task Patch Receipt v1

Source schema: [`doc/schemas/operator-task-patch-receipt.v1.schema.json`](../../schemas/operator-task-patch-receipt.v1.schema.json)

The content address under which the host stored one `operator-task-patch.v1`. A candidate's `patch` step names the patch by this ref only.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-patch-receipt.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`patch/ref`](#field-patch-ref) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-patch-receipt.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-patch-ref"></a>
## `patch/ref`

- Required: `yes`
- Shape: unspecified
