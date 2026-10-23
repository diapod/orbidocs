# Agora-matrix-recovery-attention.v1

Source schema: [`doc/schemas/agora-matrix-recovery-attention.v1.schema.json`](../../schemas/agora-matrix-recovery-attention.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `agora-matrix-recovery-attention.v1` |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`after`](#field-after) | `yes` | integer \| null |  |
| [`next_cursor`](#field-next-cursor) | `yes` | integer \| null |  |
| [`has_more`](#field-has-more) | `yes` | boolean |  |
| [`facts`](#field-facts) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-matrix-recovery-attention.v1`

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-after"></a>
## `after`

- Required: `yes`
- Shape: integer | null

<a id="field-next-cursor"></a>
## `next_cursor`

- Required: `yes`
- Shape: integer | null

<a id="field-has-more"></a>
## `has_more`

- Required: `yes`
- Shape: boolean

<a id="field-facts"></a>
## `facts`

- Required: `yes`
- Shape: array
