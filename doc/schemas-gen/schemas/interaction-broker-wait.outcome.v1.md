# Interaction Broker Wait Outcome v1

Source schema: [`doc/schemas/interaction-broker-wait.outcome.v1.schema.json`](../../schemas/interaction-broker-wait.outcome.v1.schema.json)

Domain result/projection for a satisfied or terminal wait condition. Async lifecycle state remains deferred-operation-status.v1.

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
| [`schema`](#field-schema) | `yes` | const: `interaction-broker-wait.outcome.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`wait/ref`](#field-wait-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`condition/status`](#field-condition-status) | `yes` | enum: `satisfied`, `timed-out`, `cancelled`, `failed`, `maybe-hung`, `waiting-for-input`, `no-progress`, `probe-failed` |  |
| [`observed`](#field-observed) | `no` | object | Bounded provider observation. Runtime validation also applies a serialized byte cap before projection into deferred-operation-status.v1. |
| [`duration_ms`](#field-duration-ms) | `yes` | integer |  |
| [`diagnostics`](#field-diagnostics) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `interaction-broker-wait.outcome.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-wait-ref"></a>
## `wait/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-condition-status"></a>
## `condition/status`

- Required: `yes`
- Shape: enum: `satisfied`, `timed-out`, `cancelled`, `failed`, `maybe-hung`, `waiting-for-input`, `no-progress`, `probe-failed`

<a id="field-observed"></a>
## `observed`

- Required: `no`
- Shape: object

Bounded provider observation. Runtime validation also applies a serialized byte cap before projection into deferred-operation-status.v1.

<a id="field-duration-ms"></a>
## `duration_ms`

- Required: `yes`
- Shape: integer

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
