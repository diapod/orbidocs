# Operator Task Conformance Report v1

Source schema: [`doc/schemas/operator-task-conformance-report.v1.schema.json`](../../schemas/operator-task-conformance-report.v1.schema.json)

Conformance of one exact task profile against its package, schema set, action-semantics map, refusal corpus, fixtures, and runtime. A revised action-semantics map makes the report non-current.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-conformance-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`report/ref`](#field-report-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`package/digest`](#field-package-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`implementation/digest`](#field-implementation-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`schema-set/digest`](#field-schema-set-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`action-semantics/digest`](#field-action-semantics-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`refusal-corpus/digest`](#field-refusal-corpus-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`fixture-set/digest`](#field-fixture-set-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`evaluated-at`](#field-evaluated-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`results`](#field-results) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-conformance-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-report-ref"></a>
## `report/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-implementation-digest"></a>
## `implementation/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-schema-set-digest"></a>
## `schema-set/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-action-semantics-digest"></a>
## `action-semantics/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-refusal-corpus-digest"></a>
## `refusal-corpus/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-fixture-set-digest"></a>
## `fixture-set/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-evaluated-at"></a>
## `evaluated-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-results"></a>
## `results`

- Required: `yes`
- Shape: object
