# Sensorium-biosignal-stream-descriptor.v1

Source schema: [`doc/schemas/sensorium-biosignal-stream-descriptor.v1.schema.json`](../../schemas/sensorium-biosignal-stream-descriptor.v1.schema.json)

Backend-neutral stream layout. Signal rows must be unique, in range and disjoint from source time, package number and marker rows. Metadata describes layout, not observed activation. Unknown units and counter semantics are explicit until qualified by a profile.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-biosignal-stream-descriptor.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`stream/id`](#field-stream-id) | `yes` | string |  |
| [`backend/preset`](#field-backend-preset) | `yes` | string |  |
| [`source/rows`](#field-source-rows) | `yes` | integer |  |
| [`channels`](#field-channels) | `yes` | array |  |
| [`rate/nominal`](#field-rate-nominal) | `yes` | object |  |
| [`source-time/row`](#field-source-time-row) | `yes` | integer |  |
| [`package-num/row`](#field-package-num-row) | `yes` | integer |  |
| [`marker/row`](#field-marker-row) | `yes` | integer |  |
| [`package-num/semantics`](#field-package-num-semantics) | `yes` | enum: `unknown`, `per-sample`, `repeated-packet` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-biosignal-stream-descriptor.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-stream-id"></a>
## `stream/id`

- Required: `yes`
- Shape: string

<a id="field-backend-preset"></a>
## `backend/preset`

- Required: `yes`
- Shape: string

<a id="field-source-rows"></a>
## `source/rows`

- Required: `yes`
- Shape: integer

<a id="field-channels"></a>
## `channels`

- Required: `yes`
- Shape: array

<a id="field-rate-nominal"></a>
## `rate/nominal`

- Required: `yes`
- Shape: object

<a id="field-source-time-row"></a>
## `source-time/row`

- Required: `yes`
- Shape: integer

<a id="field-package-num-row"></a>
## `package-num/row`

- Required: `yes`
- Shape: integer

<a id="field-marker-row"></a>
## `marker/row`

- Required: `yes`
- Shape: integer

<a id="field-package-num-semantics"></a>
## `package-num/semantics`

- Required: `yes`
- Shape: enum: `unknown`, `per-sample`, `repeated-packet`
