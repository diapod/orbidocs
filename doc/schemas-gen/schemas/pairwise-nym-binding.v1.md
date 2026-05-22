# Pairwise Nym Binding v1

Source schema: [`doc/schemas/pairwise-nym-binding.v1.schema.json`](../../schemas/pairwise-nym-binding.v1.schema.json)

Current sealed projection of pairwise nym continuity reduced from pairwise-nym-binding-fact.v1 events.

## Governing Basis

- [`doc/project/40-proposals/065-local-relationship-layer.md`](../../project/40-proposals/065-local-relationship-layer.md)
- [`doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)

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

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `pairwise-nym-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`contact/ref`](#field-contact-ref) | `yes` | string |  |
| [`context/kind`](#field-context-kind) | `yes` | ref: `pairwise-nym-binding-fact.v1.schema.json#/$defs/context_kind` |  |
| [`context/ref`](#field-context-ref) | `no` | string |  |
| [`nym/current`](#field-nym-current) | `yes` | string \| null |  |
| [`nym/history`](#field-nym-history) | `yes` | array |  |
| [`as-of-tx/id`](#field-as-of-tx-id) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`history_entry`](#def-history-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `pairwise-nym-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-contact-ref"></a>
## `contact/ref`

- Required: `yes`
- Shape: string

<a id="field-context-kind"></a>
## `context/kind`

- Required: `yes`
- Shape: ref: `pairwise-nym-binding-fact.v1.schema.json#/$defs/context_kind`

<a id="field-context-ref"></a>
## `context/ref`

- Required: `no`
- Shape: string

<a id="field-nym-current"></a>
## `nym/current`

- Required: `yes`
- Shape: string | null

<a id="field-nym-history"></a>
## `nym/history`

- Required: `yes`
- Shape: array

<a id="field-as-of-tx-id"></a>
## `as-of-tx/id`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-history-entry"></a>
## `$defs.history_entry`

- Shape: object
