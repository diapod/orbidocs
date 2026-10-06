# Operator Task Binding Sources v1

Source schema: [`doc/schemas/operator-task-binding-sources.v1.schema.json`](../../schemas/operator-task-binding-sources.v1.schema.json)

Scoped source explanation of one task-pack binding. Equal declarations preserve all contributors; unequal declarations refuse. No path or other owner's configuration is disclosed. Write admission describes the retained host target, not current operator authority or an activation claim.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`history/capacity`](#field-history-capacity) | `yes` | object | Read-only node-wide journal pressure, including pending outcome reservations. Not a write-success or task-run authority claim. Near-capacity begins at 80%; archival is not implemented in this scoped vertical. |
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-sources.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`owner/ref`](#field-owner-ref) | `yes` | const: `daemon:operator-task-packs` |  |
| [`scope/ref`](#field-scope-ref) | `yes` | const: `component:operator-task-packs` |  |
| [`source/set`](#field-source-set) | `yes` | object |  |
| [`source-set/revision`](#field-source-set-revision) | `yes` | ref: `configuration-common.v1.schema.json#/$defs/digest` |  |
| [`binding`](#field-binding) | `yes` | ref: `operator-task-local-binding.v1.schema.json` |  |
| [`write/admitted`](#field-write-admitted) | `yes` | boolean |  |
| [`descriptor`](#field-descriptor) | `yes` | ref: `config-setting-descriptor.v1.schema.json` |  |
| [`descriptor/digest`](#field-descriptor-digest) | `yes` | ref: `configuration-common.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-history-capacity"></a>
## `history/capacity`

- Required: `yes`
- Shape: object

Read-only node-wide journal pressure, including pending outcome reservations. Not a write-success or task-run authority claim. Near-capacity begins at 80%; archival is not implemented in this scoped vertical.

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-sources.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-owner-ref"></a>
## `owner/ref`

- Required: `yes`
- Shape: const: `daemon:operator-task-packs`

<a id="field-scope-ref"></a>
## `scope/ref`

- Required: `yes`
- Shape: const: `component:operator-task-packs`

<a id="field-source-set"></a>
## `source/set`

- Required: `yes`
- Shape: object

<a id="field-source-set-revision"></a>
## `source-set/revision`

- Required: `yes`
- Shape: ref: `configuration-common.v1.schema.json#/$defs/digest`

<a id="field-binding"></a>
## `binding`

- Required: `yes`
- Shape: ref: `operator-task-local-binding.v1.schema.json`

<a id="field-write-admitted"></a>
## `write/admitted`

- Required: `yes`
- Shape: boolean

<a id="field-descriptor"></a>
## `descriptor`

- Required: `yes`
- Shape: ref: `config-setting-descriptor.v1.schema.json`

<a id="field-descriptor-digest"></a>
## `descriptor/digest`

- Required: `yes`
- Shape: ref: `configuration-common.v1.schema.json#/$defs/digest`
