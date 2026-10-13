# Sensorium-biosignal-capture.v1

Source schema: [`doc/schemas/sensorium-biosignal-capture.v1.schema.json`](../../schemas/sensorium-biosignal-capture.v1.schema.json)

Reserved optional retained capture contract. Requires independent capture admission, quota, retention and Artifact Delivery policy; transient sample reads never imply recording. First slice exposes no capture route. Partial/final state must reflect actual completeness; no values embedded.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-biosignal-capture.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capture/ref`](#field-capture-ref) | `yes` | object |  |
| [`instance/ref`](#field-instance-ref) | `yes` | object |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`session/epoch`](#field-session-epoch) | `yes` | string |  |
| [`source/generation`](#field-source-generation) | `yes` | integer |  |
| [`capture/state`](#field-capture-state) | `yes` | enum: `partial`, `final`, `tombstoned` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`artifacts`](#field-artifacts) | `yes` | array |  |
| [`capture-authority/ref`](#field-capture-authority-ref) | `yes` | object |  |
| [`retention/expires-at-unix-s`](#field-retention-expires-at-unix-s) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-biosignal-capture.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capture-ref"></a>
## `capture/ref`

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

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: string

<a id="field-source-generation"></a>
## `source/generation`

- Required: `yes`
- Shape: integer

<a id="field-capture-state"></a>
## `capture/state`

- Required: `yes`
- Shape: enum: `partial`, `final`, `tombstoned`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-artifacts"></a>
## `artifacts`

- Required: `yes`
- Shape: array

<a id="field-capture-authority-ref"></a>
## `capture-authority/ref`

- Required: `yes`
- Shape: object

<a id="field-retention-expires-at-unix-s"></a>
## `retention/expires-at-unix-s`

- Required: `yes`
- Shape: integer
