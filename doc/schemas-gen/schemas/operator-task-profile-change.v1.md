# Operator Task Profile Change v1

Source schema: [`doc/schemas/operator-task-profile-change.v1.schema.json`](../../schemas/operator-task-profile-change.v1.schema.json)

Request to review, and optionally accept, the task profile an upgraded package now pins for one binding. The host admits the supplied profile only at the package's registered digest and diffs it against the binding's accepted profile; acceptance is one action and refuses when the binding's local choices would exceed the new ceilings. A review (`accept: false`) is a read and carries no authority. An acceptance names the operator binding and the expected revision, which the host verifies when it commits the change, not when it computed the diff.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-profile-change.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`local-binding/expected-digest`](#field-local-binding-expected-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` | The `local-binding/digest` of the revision this change was prepared against, as readiness or a profile-change review reported it. The host compares it with the stored binding when it commits the change and refuses a mismatch with `local-binding/revision-stale`. |
| [`task-profile`](#field-task-profile) | `yes` | ref: `operator-task-profile.v1.schema.json` |  |
| [`accept`](#field-accept) | `yes` | boolean |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "accept": {
      "const": true
    }
  },
  "required": [
    "accept"
  ]
}
```

Then:

```json
{
  "required": [
    "operator/binding-ref",
    "local-binding/expected-digest"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-profile-change.v1`

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

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-local-binding-expected-digest"></a>
## `local-binding/expected-digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

The `local-binding/digest` of the revision this change was prepared against, as readiness or a profile-change review reported it. The host compares it with the stored binding when it commits the change and refuses a mismatch with `local-binding/revision-stale`.

<a id="field-task-profile"></a>
## `task-profile`

- Required: `yes`
- Shape: ref: `operator-task-profile.v1.schema.json`

<a id="field-accept"></a>
## `accept`

- Required: `yes`
- Shape: boolean
