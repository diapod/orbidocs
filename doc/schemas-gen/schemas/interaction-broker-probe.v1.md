# Interaction Broker Probe v1

Source schema: [`doc/schemas/interaction-broker-probe.v1.schema.json`](../../schemas/interaction-broker-probe.v1.schema.json)

Active bounded probe request against one registered observation source.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`](../../project/60-solutions/035-interaction-broker/035-interaction-broker.md)

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
| [`schema`](#field-schema) | `yes` | const: `interaction-broker-probe.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`probe/ref`](#field-probe-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `#/$defs/ref` |  |
| [`source`](#field-source) | `yes` | ref: `interaction-broker-wait.request.v1.schema.json#/$defs/observationSource` |  |
| [`condition`](#field-condition) | `yes` | ref: `interaction-broker-wait.request.v1.schema.json#/$defs/waitCondition` |  |
| [`timeout_ms`](#field-timeout-ms) | `yes` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `interaction-broker-probe.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-probe-ref"></a>
## `probe/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `interaction-broker-wait.request.v1.schema.json#/$defs/observationSource`

<a id="field-condition"></a>
## `condition`

- Required: `yes`
- Shape: ref: `interaction-broker-wait.request.v1.schema.json#/$defs/waitCondition`

<a id="field-timeout-ms"></a>
## `timeout_ms`

- Required: `yes`
- Shape: integer

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
