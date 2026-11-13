# Agora-matrix-homeserver-admission.v1

Source schema: [`doc/schemas/agora-matrix-homeserver-admission.v1.schema.json`](../../schemas/agora-matrix-homeserver-admission.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `agora-matrix-homeserver-admission.v1` |  |
| [`matrix/homeserver`](#field-matrix-homeserver) | `yes` | string |  |
| [`matrix/room-version`](#field-matrix-room-version) | `yes` | const: `10` |  |
| [`admitted/from`](#field-admitted-from) | `yes` | string |  |
| [`admitted/until`](#field-admitted-until) | `yes` | string |  |
| [`server/keys`](#field-server-keys) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-matrix-homeserver-admission.v1`

<a id="field-matrix-homeserver"></a>
## `matrix/homeserver`

- Required: `yes`
- Shape: string

<a id="field-matrix-room-version"></a>
## `matrix/room-version`

- Required: `yes`
- Shape: const: `10`

<a id="field-admitted-from"></a>
## `admitted/from`

- Required: `yes`
- Shape: string

<a id="field-admitted-until"></a>
## `admitted/until`

- Required: `yes`
- Shape: string

<a id="field-server-keys"></a>
## `server/keys`

- Required: `yes`
- Shape: array
