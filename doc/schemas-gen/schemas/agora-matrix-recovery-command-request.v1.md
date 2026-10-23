# Agora-matrix-recovery-command-request.v1

Source schema: [`doc/schemas/agora-matrix-recovery-command-request.v1.schema.json`](../../schemas/agora-matrix-recovery-command-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`task_ref`](#field-task-ref) | `yes` | integer |  |
| [`expected_revision`](#field-expected-revision) | `yes` | integer |  |
| [`request/id`](#field-request-id) | `no` | unspecified |  |
| [`source/id`](#field-source-id) | `no` | string \| null |  |
| [`operator_ref`](#field-operator-ref) | `no` | string |  |
| [`reason`](#field-reason) | `no` | string \| null |  |
## Field Semantics

<a id="field-task-ref"></a>
## `task_ref`

- Required: `yes`
- Shape: integer

<a id="field-expected-revision"></a>
## `expected_revision`

- Required: `yes`
- Shape: integer

<a id="field-request-id"></a>
## `request/id`

- Required: `no`
- Shape: unspecified

<a id="field-source-id"></a>
## `source/id`

- Required: `no`
- Shape: string | null

<a id="field-operator-ref"></a>
## `operator_ref`

- Required: `no`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string | null
