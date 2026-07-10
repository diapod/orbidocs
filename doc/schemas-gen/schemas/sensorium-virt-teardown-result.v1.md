# Sensorium Virt Teardown Result v1

Source schema: [`doc/schemas/sensorium-virt-teardown-result.v1.schema.json`](../../schemas/sensorium-virt-teardown-result.v1.schema.json)

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
| [`status`](#field-status) | `yes` | const: `ok` |  |
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-teardown-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | string |  |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | const: `closed` |  |
| [`cleanup/status`](#field-cleanup-status) | `yes` | const: `completed` |  |
| [`outcome`](#field-outcome) | `yes` | ref: `sensorium-workbench-outcome.v1.schema.json` |  |
| [`diagnostics`](#field-diagnostics) | `yes` | array |  |
## Field Semantics

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `ok`

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-teardown-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: string

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: const: `closed`

<a id="field-cleanup-status"></a>
## `cleanup/status`

- Required: `yes`
- Shape: const: `completed`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: ref: `sensorium-workbench-outcome.v1.schema.json`

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `yes`
- Shape: array
