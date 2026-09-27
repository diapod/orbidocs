# Operator Task Pack Conformance Run v1

Source schema: [`doc/schemas/operator-task-pack-conformance-run.v1.schema.json`](../../schemas/operator-task-pack-conformance-run.v1.schema.json)

Request to recompute the pack facts of every task profile an installed P085 package binds and, when they pass, to run the package's host-owned P085 conformance. The asset bundle is read from one host-admitted P085 import root; each entry names the asset ref the profile uses and its relative path there. The host digests every asset itself; the request carries no digests and no absolute paths.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-pack-conformance-run.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`assets`](#field-assets) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-pack-conformance-run.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-assets"></a>
## `assets`

- Required: `yes`
- Shape: object
