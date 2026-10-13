# Sensorium-brainflow-device-binding.v1

Source schema: [`doc/schemas/sensorium-brainflow-device-binding.v1.schema.json`](../../schemas/sensorium-brainflow-device-binding.v1.schema.json)

HOST-PRIVATE only: selector never appears in status, plan, telemetry, reports or publication descriptors. A confirmed selector does not prove serial identity. Ambiguity, absent/currently busy device and claim conflict are distinct refusals. This shape grants no discovery or acquisition authority.

## Governing Basis

- [`doc/project/40-proposals/096-sensorium-brainflow-connector.md`](../../project/40-proposals/096-sensorium-brainflow-connector.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-device-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | object |  |
| [`instance/ref`](#field-instance-ref) | `yes` | object |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`selector/kind`](#field-selector-kind) | `yes` | const: `advertised-name` |  |
| [`selector/value`](#field-selector-value) | `yes` | string |  |
| [`identity/assurance`](#field-identity-assurance) | `yes` | const: `operator-confirmed-selector` |  |
| [`resolution/state`](#field-resolution-state) | `yes` | enum: `operator-confirmed`, `resolved`, `ambiguous`, `unavailable` |  |
| [`claim/alias`](#field-claim-alias) | `yes` | string |  |
| [`expires/at-unix-s`](#field-expires-at-unix-s) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-device-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: object

<a id="field-instance-ref"></a>
## `instance/ref`

- Required: `yes`
- Shape: object

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-selector-kind"></a>
## `selector/kind`

- Required: `yes`
- Shape: const: `advertised-name`

<a id="field-selector-value"></a>
## `selector/value`

- Required: `yes`
- Shape: string

<a id="field-identity-assurance"></a>
## `identity/assurance`

- Required: `yes`
- Shape: const: `operator-confirmed-selector`

<a id="field-resolution-state"></a>
## `resolution/state`

- Required: `yes`
- Shape: enum: `operator-confirmed`, `resolved`, `ambiguous`, `unavailable`

<a id="field-claim-alias"></a>
## `claim/alias`

- Required: `yes`
- Shape: string

<a id="field-expires-at-unix-s"></a>
## `expires/at-unix-s`

- Required: `yes`
- Shape: integer
