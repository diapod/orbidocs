# Operator Task Binding Inspection v1

Source schema: [`doc/schemas/operator-task-binding-inspection.v1.schema.json`](../../schemas/operator-task-binding-inspection.v1.schema.json)

Operator drill-down of one local task-pack binding (P094-012), projected on read from the binding, its accepted profile, readiness and run facts. It leads with the decisive readiness blocker and its next action, shows each narrowing axis with its effective value and the layer that decided it, and names drill-down refs. Values are enum names, numbers as text, or refs and digests; never local paths, command output or raw stores. Readiness itself stays the operator-task-readiness.v1 contract.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-inspection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | unspecified |  |
| [`binding/state`](#field-binding-state) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/bindingState` |  |
| [`binding/revision`](#field-binding-revision) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`evaluated-at`](#field-evaluated-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`workspace`](#field-workspace) | `yes` | object |  |
| [`image-variant/ref`](#field-image-variant-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`inference`](#field-inference) | `no` | object |  |
| [`runnable`](#field-runnable) | `yes` | boolean |  |
| [`decisive-blocker`](#field-decisive-blocker) | `no` | object |  |
| [`effective`](#field-effective) | `yes` | array |  |
| [`publication`](#field-publication) | `yes` | object |  |
| [`runs`](#field-runs) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-inspection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-binding-state"></a>
## `binding/state`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/bindingState`

<a id="field-binding-revision"></a>
## `binding/revision`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-ref"></a>
## `task-profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-evaluated-at"></a>
## `evaluated-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-workspace"></a>
## `workspace`

- Required: `yes`
- Shape: object

<a id="field-image-variant-ref"></a>
## `image-variant/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-inference"></a>
## `inference`

- Required: `no`
- Shape: object

<a id="field-runnable"></a>
## `runnable`

- Required: `yes`
- Shape: boolean

<a id="field-decisive-blocker"></a>
## `decisive-blocker`

- Required: `no`
- Shape: object

<a id="field-effective"></a>
## `effective`

- Required: `yes`
- Shape: array

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: object

<a id="field-runs"></a>
## `runs`

- Required: `yes`
- Shape: array
