# Operator Task Local Binding v1

Source schema: [`doc/schemas/operator-task-local-binding.v1.schema.json`](../../schemas/operator-task-local-binding.v1.schema.json)

Host-owned local choices for one task profile and a host mutation revision that fences stale requests across pause/resume cycles. No activation generation or restated portable fact. Legacy documents without binding/revision retain their original digest until the first change; new bindings start at revision 1 and every effective change increments it.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-local-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`binding/state`](#field-binding-state) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/bindingState` |  |
| [`binding/revision`](#field-binding-revision) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/counter` | Host-owned monotone mutation counter, included in local-binding/digest. It is never supplied in a change request; omitted only in legacy stored documents. No-op retries do not increment it. |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`workspace`](#field-workspace) | `yes` | object |  |
| [`image-variant/ref`](#field-image-variant-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`inference`](#field-inference) | `no` | object |  |
| [`deliberation`](#field-deliberation) | `no` | object |  |
| [`publication`](#field-publication) | `yes` | object |  |
| [`safety`](#field-safety) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-local-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-binding-state"></a>
## `binding/state`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/bindingState`

<a id="field-binding-revision"></a>
## `binding/revision`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

Host-owned monotone mutation counter, included in local-binding/digest. It is never supplied in a change request; omitted only in legacy stored documents. No-op retries do not increment it.

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

<a id="field-deliberation"></a>
## `deliberation`

- Required: `no`
- Shape: object

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: object

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: object
