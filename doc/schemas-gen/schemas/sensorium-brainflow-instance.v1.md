# Sensorium-brainflow-instance.v1

Source schema: [`doc/schemas/sensorium-brainflow-instance.v1.schema.json`](../../schemas/sensorium-brainflow-instance.v1.schema.json)

Durable instance intent, separate from admitted, resolved and active views. Opaque host-private binding refs contain no selectors. Desired running state alone does not launch or authorize acquisition; every launch requires current host admission and independently allocated identity/home/auth. This admitted intent view references a separate source declaration artifact; declaration/ref is not a self-digest. Synthetic uses a null physical binding. Desired eligibility is disabled/enabled; explicit operator stop and current acquisition authority remain separate facts.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-instance.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`instance/ref`](#field-instance-ref) | `yes` | object |  |
| [`declaration/ref`](#field-declaration-ref) | `yes` | object |  |
| [`package/ref`](#field-package-ref) | `yes` | object |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`mode/id`](#field-mode-id) | `yes` | enum: `synthetic`, `p21`, `p51` |  |
| [`desired/state`](#field-desired-state) | `yes` | enum: `disabled`, `enabled` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | unspecified |  |
| [`budgets/ref`](#field-budgets-ref) | `yes` | object |  |
| [`restart/policy`](#field-restart-policy) | `yes` | const: `manual` |  |
| [`capture/desired`](#field-capture-desired) | `yes` | const: `off` |  |
| [`publication/desired`](#field-publication-desired) | `yes` | const: `off` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-instance.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-instance-ref"></a>
## `instance/ref`

- Required: `yes`
- Shape: object

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `yes`
- Shape: object

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: object

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-mode-id"></a>
## `mode/id`

- Required: `yes`
- Shape: enum: `synthetic`, `p21`, `p51`

<a id="field-desired-state"></a>
## `desired/state`

- Required: `yes`
- Shape: enum: `disabled`, `enabled`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-budgets-ref"></a>
## `budgets/ref`

- Required: `yes`
- Shape: object

<a id="field-restart-policy"></a>
## `restart/policy`

- Required: `yes`
- Shape: const: `manual`

<a id="field-capture-desired"></a>
## `capture/desired`

- Required: `yes`
- Shape: const: `off`

<a id="field-publication-desired"></a>
## `publication/desired`

- Required: `yes`
- Shape: const: `off`
