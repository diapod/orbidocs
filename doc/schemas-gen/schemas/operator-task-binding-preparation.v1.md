# Operator Task Binding Preparation v1

Source schema: [`doc/schemas/operator-task-binding-preparation.v1.schema.json`](../../schemas/operator-task-binding-preparation.v1.schema.json)

Read-only bounded owner inventory for binding clients. Profiles are exact retained package material; choices confer neither activation, readiness nor execution authority. Commit still uses operator-task-binding-create.v1 and rechecks its owners.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`package/states`](#field-package-states) | `yes` | object | Recorded lifecycle for the displayed packages. Activation-recorded does not assert current authority or readiness; expiry and use fences remain owner-checked. |
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-preparation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`packages`](#field-packages) | `yes` | array |  |
| [`profiles`](#field-profiles) | `yes` | array |  |
| [`workspaces`](#field-workspaces) | `yes` | array |  |
## Field Semantics

<a id="field-package-states"></a>
## `package/states`

- Required: `yes`
- Shape: object

Recorded lifecycle for the displayed packages. Activation-recorded does not assert current authority or readiness; expiry and use fences remain owner-checked.

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-preparation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-packages"></a>
## `packages`

- Required: `yes`
- Shape: array

<a id="field-profiles"></a>
## `profiles`

- Required: `yes`
- Shape: array

<a id="field-workspaces"></a>
## `workspaces`

- Required: `yes`
- Shape: array
