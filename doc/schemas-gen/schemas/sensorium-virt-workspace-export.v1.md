# Sensorium Virt Workspace Export v1

Source schema: [`doc/schemas/sensorium-virt-workspace-export.v1.schema.json`](../../schemas/sensorium-virt-workspace-export.v1.schema.json)

Bounded content bundle exported explicitly from a managed Sensorium Virt workspace.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-workspace-export.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend`](#field-backend) | `yes` | enum: `fixture-virtual-workspace`, `container`, `microvm` |  |
| [`executor/kind`](#field-executor-kind) | `yes` | enum: `fixture-copy.v1`, `container`, `microvm` |  |
| [`files`](#field-files) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-workspace-export.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend"></a>
## `backend`

- Required: `yes`
- Shape: enum: `fixture-virtual-workspace`, `container`, `microvm`

<a id="field-executor-kind"></a>
## `executor/kind`

- Required: `yes`
- Shape: enum: `fixture-copy.v1`, `container`, `microvm`

<a id="field-files"></a>
## `files`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
