# Sensorium Workbench Patch v1

Source schema: [`doc/schemas/sensorium-workbench-patch.v1.schema.json`](../../schemas/sensorium-workbench-patch.v1.schema.json)

Patch proposal artifact for a Workbench workspace. It may carry a human-readable unified diff or structured edit operations.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-patch.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`patch/ref`](#field-patch-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`patch/kind`](#field-patch-kind) | `yes` | enum: `unified-diff`, `structured-edits` |  |
| [`unified_diff`](#field-unified-diff) | `no` | string |  |
| [`edits`](#field-edits) | `no` | array |  |
| [`provenance`](#field-provenance) | `no` | object |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-patch.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-patch-ref"></a>
## `patch/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-patch-kind"></a>
## `patch/kind`

- Required: `yes`
- Shape: enum: `unified-diff`, `structured-edits`

<a id="field-unified-diff"></a>
## `unified_diff`

- Required: `no`
- Shape: string

<a id="field-edits"></a>
## `edits`

- Required: `no`
- Shape: array

<a id="field-provenance"></a>
## `provenance`

- Required: `no`
- Shape: object

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
