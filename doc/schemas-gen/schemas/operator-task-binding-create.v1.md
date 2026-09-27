# Operator Task Binding Create v1

Source schema: [`doc/schemas/operator-task-binding-create.v1.schema.json`](../../schemas/operator-task-binding-create.v1.schema.json)

Request to bind one task profile an installed package pins. The operator supplies the profile document, which the host admits only at the package's registered digest, and only the choices the profile leaves open. Omitted safety values take the most restrictive admissible default, publication defaults to off, and the host fills the profile digest. A missing workspace, or a missing image variant when the profile admits several, is refused as incomplete; the request cannot carry digests, generations or portable facts. Creating a binding is an ordinary binding change: it names the operator binding under which it is made, and the host verifies that binding as current when it commits the change.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-create.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile`](#field-task-profile) | `yes` | ref: `operator-task-profile.v1.schema.json` |  |
| [`workspace`](#field-workspace) | `no` | object |  |
| [`inference`](#field-inference) | `no` | object |  |
| [`publication`](#field-publication) | `no` | object |  |
| [`safety`](#field-safety) | `no` | object |  |
| [`image-variant/ref`](#field-image-variant-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` | Required when the profile admits more than one image variant; forbidden to restate otherwise by the host's admission, not by shape. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-create.v1`

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

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile"></a>
## `task-profile`

- Required: `yes`
- Shape: ref: `operator-task-profile.v1.schema.json`

<a id="field-workspace"></a>
## `workspace`

- Required: `no`
- Shape: object

<a id="field-inference"></a>
## `inference`

- Required: `no`
- Shape: object

<a id="field-publication"></a>
## `publication`

- Required: `no`
- Shape: object

<a id="field-safety"></a>
## `safety`

- Required: `no`
- Shape: object

<a id="field-image-variant-ref"></a>
## `image-variant/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

Required when the profile admits more than one image variant; forbidden to restate otherwise by the host's admission, not by shape.
