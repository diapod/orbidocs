# Sensorium Workbench Instance v1

Source schema: [`doc/schemas/sensorium-workbench-instance.v1.schema.json`](../../schemas/sensorium-workbench-instance.v1.schema.json)

The microVM instance of one run, allocated from a configured Workbench root (P094-021c). Its root ref is the content address of the workspace, the configured root and the instance key, so a Workbench restart re-binds the live VM. `allocating` means the host holds the allocation but the VM has not started; `unbound` means a restart could not re-bind it; either can still be torn down. A `closed` instance is never allocated again under its key.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-instance.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`root/ref`](#field-root-ref) | `yes` | string |  |
| [`template/root-ref`](#field-template-root-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`profile/root-ref`](#field-profile-root-ref) | `no` | ref: `#/$defs/ref` | Immutable portable root mapping selected by the host binding at allocation; absent means template/root-ref. |
| [`instance/key`](#field-instance-key) | `yes` | string |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`image/manifest-digest`](#field-image-manifest-digest) | `no` | string \| null |  |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | enum: `allocating`, `ready`, `unbound`, `closed` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-instance.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-root-ref"></a>
## `root/ref`

- Required: `yes`
- Shape: string

<a id="field-template-root-ref"></a>
## `template/root-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-profile-root-ref"></a>
## `profile/root-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

Immutable portable root mapping selected by the host binding at allocation; absent means template/root-ref.

<a id="field-instance-key"></a>
## `instance/key`

- Required: `yes`
- Shape: string

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-image-manifest-digest"></a>
## `image/manifest-digest`

- Required: `no`
- Shape: string | null

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: enum: `allocating`, `ready`, `unbound`, `closed`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
