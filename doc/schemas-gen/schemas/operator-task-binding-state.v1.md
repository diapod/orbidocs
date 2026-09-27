# Operator Task Binding State v1

Source schema: [`doc/schemas/operator-task-binding-state.v1.schema.json`](../../schemas/operator-task-binding-state.v1.schema.json)

Request to pause or resume one local binding under a current operator binding. Pausing is reversible and needs no reactivation; revocation stays a P085 operation. The host verifies the operator binding and the expected revision when it commits the change. A request whose outcome already holds changes and records nothing. A pause that must not depend on a current operator binding uses `operator-task-binding-emergency-pause.v1` instead; this request never falls back to it.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-state.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`local-binding/expected-digest`](#field-local-binding-expected-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` | The `local-binding/digest` of the revision this change was prepared against, as readiness or a profile-change review reported it. The host compares it with the stored binding when it commits the change and refuses a mismatch with `local-binding/revision-stale`. |
| [`binding/state`](#field-binding-state) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/bindingState` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-state.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-local-binding-expected-digest"></a>
## `local-binding/expected-digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

The `local-binding/digest` of the revision this change was prepared against, as readiness or a profile-change review reported it. The host compares it with the stored binding when it commits the change and refuses a mismatch with `local-binding/revision-stale`.

<a id="field-binding-state"></a>
## `binding/state`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/bindingState`
