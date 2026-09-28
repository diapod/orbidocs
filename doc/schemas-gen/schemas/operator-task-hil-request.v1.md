# Operator Task HIL Request v1

Source schema: [`doc/schemas/operator-task-hil-request.v1.schema.json`](../../schemas/operator-task-hil-request.v1.schema.json)

Host-issued request for an operator decision on one step of one stored experiment plan that requires HIL. It carries the decision material: the stamped step with its derived effect class and source, the exact files and content digests of a patch, and the rollback that would apply. Model prose is never part of it. Its ref is the content address of the plan ref and step id, so one step has exactly one request; delivery passes the P085 attention gate, which may deliver, group, defer or deny it but never approves. The request expires; an expired request cannot be approved.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/ref`](#field-request-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`step`](#field-step) | `yes` | unspecified | The plan step exactly as the plan stamps it; only a step that requires HIL has a request. |
| [`patch/files`](#field-patch-files) | `no` | array | For a `patch` step: every file of the patch, with the digest and size of the complete resulting content of each written file. |
| [`rollback/mode`](#field-rollback-mode) | `yes` | enum: `recreate-prepared-system`, `exact-rollback-profile` |  |
| [`requested-at`](#field-requested-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`expires-at`](#field-expires-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`patchFile`](#def-patchfile) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-step"></a>
## `step`

- Required: `yes`
- Shape: unspecified

The plan step exactly as the plan stamps it; only a step that requires HIL has a request.

<a id="field-patch-files"></a>
## `patch/files`

- Required: `no`
- Shape: array

For a `patch` step: every file of the patch, with the digest and size of the complete resulting content of each written file.

<a id="field-rollback-mode"></a>
## `rollback/mode`

- Required: `yes`
- Shape: enum: `recreate-prepared-system`, `exact-rollback-profile`

<a id="field-requested-at"></a>
## `requested-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

## Definition Semantics

<a id="def-patchfile"></a>
## `$defs.patchFile`

- Shape: object
