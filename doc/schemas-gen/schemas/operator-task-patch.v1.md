# Operator Task Patch v1

Source schema: [`doc/schemas/operator-task-patch.v1.schema.json`](../../schemas/operator-task-patch.v1.schema.json)

Closed, content-addressed patch a plan's `patch` step applies: the complete resulting content of each written file, or its deletion, below logical roots, for exactly one patch policy. The host stores it before plan validation as `artifact:sha256:<base64url>`, the SHA-256 over its JCS v1 canonical JSON, and admits every file against the kept policy before any operator question is asked, so a HIL request shows the exact targets and content digests. A write carries the whole resulting file, which the policy's line shape judges; a patch never carries diffs, commands or paths outside the policy's targets.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-patch.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`patch-policy/ref`](#field-patch-policy-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` | The patch policy this patch is written for; a plan step applies it only under that exact policy. |
| [`files`](#field-files) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`file`](#def-file) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-patch.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-patch-policy-ref"></a>
## `patch-policy/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

The patch policy this patch is written for; a plan step applies it only under that exact policy.

<a id="field-files"></a>
## `files`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-file"></a>
## `$defs.file`

- Shape: object
