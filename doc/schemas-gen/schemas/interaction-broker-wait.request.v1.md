# Interaction Broker Wait Request v1

Source schema: [`doc/schemas/interaction-broker-wait.request.v1.schema.json`](../../schemas/interaction-broker-wait.request.v1.schema.json)

Declarative bounded wait over one primary observation source.

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
| [`schema`](#field-schema) | `yes` | const: `interaction-broker-wait.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`wait/ref`](#field-wait-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `#/$defs/ref` |  |
| [`scope`](#field-scope) | `yes` | object |  |
| [`condition`](#field-condition) | `yes` | ref: `#/$defs/waitCondition` |  |
| [`deadline_ms`](#field-deadline-ms) | `yes` | integer |  |
| [`on_timeout`](#field-on-timeout) | `yes` | enum: `return-not-kill`, `cancel-if-cancelable` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
| [`sha256Ref`](#def-sha256ref) | string |  |
| [`deferredOperationId`](#def-deferredoperationid) | string |  |
| [`observationSource`](#def-observationsource) | unspecified |  |
| [`waitCondition`](#def-waitcondition) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `interaction-broker-wait.request.v1`

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

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

<a id="field-condition"></a>
## `condition`

- Required: `yes`
- Shape: ref: `#/$defs/waitCondition`

<a id="field-deadline-ms"></a>
## `deadline_ms`

- Required: `yes`
- Shape: integer

<a id="field-on-timeout"></a>
## `on_timeout`

- Required: `yes`
- Shape: enum: `return-not-kill`, `cancel-if-cancelable`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string

<a id="def-sha256ref"></a>
## `$defs.sha256Ref`

- Shape: string

<a id="def-deferredoperationid"></a>
## `$defs.deferredOperationId`

- Shape: string

<a id="def-observationsource"></a>
## `$defs.observationSource`

- Shape: unspecified

<a id="def-waitcondition"></a>
## `$defs.waitCondition`

- Shape: unspecified
