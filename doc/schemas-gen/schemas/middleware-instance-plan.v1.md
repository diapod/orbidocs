# Middleware Instance Plan v1

Source schema: [`doc/schemas/middleware-instance-plan.v1.schema.json`](../../schemas/middleware-instance-plan.v1.schema.json)

Draft adapter-neutral, single-instance registration intent. The host validates authority, exact declared/package material, allocated identities, entrypoints, dependency DAG, limits and CAS; commits and applies the complete runtime snapshot. A plan grants no authority and contains no credentials or device selectors. Semantic checks remain required.

## Governing Basis

- [`doc/project/40-proposals/096-sensorium-brainflow-connector.md`](../../project/40-proposals/096-sensorium-brainflow-connector.md)
- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/091-file-backed-configuration-and-explainable-composition.md`](../../project/40-proposals/091-file-backed-configuration-and-explainable-composition.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)
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
| [`schema`](#field-schema) | `yes` | const: `middleware-instance-plan.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`instance/ref`](#field-instance-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`declaration/ref`](#field-declaration-ref) | `yes` | ref: `#/$defs/exactRef` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/exactRef` |  |
| [`executor`](#field-executor) | `yes` | object |  |
| [`module/id`](#field-module-id) | `yes` | string |  |
| [`component/id`](#field-component-id) | `yes` | string |  |
| [`home/binding`](#field-home-binding) | `yes` | ref: `#/$defs/ref` |  |
| [`channel-auth/binding`](#field-channel-auth-binding) | `yes` | ref: `#/$defs/ref` |  |
| [`dependencies`](#field-dependencies) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | object |  |
| [`exactRef`](#def-exactref) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-instance-plan.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-instance-ref"></a>
## `instance/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `yes`
- Shape: ref: `#/$defs/exactRef`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/exactRef`

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: object

<a id="field-module-id"></a>
## `module/id`

- Required: `yes`
- Shape: string

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: string

<a id="field-home-binding"></a>
## `home/binding`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-channel-auth-binding"></a>
## `channel-auth/binding`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-dependencies"></a>
## `dependencies`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: object

<a id="def-exactref"></a>
## `$defs.exactRef`

- Shape: object
