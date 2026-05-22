# Pairwise Nym Binding Fact v1

Source schema: [`doc/schemas/pairwise-nym-binding-fact.v1.schema.json`](../../schemas/pairwise-nym-binding-fact.v1.schema.json)

Append-only local event recording observed pairwise nym continuity for one contact and context.

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
| [`schema`](#field-schema) | `yes` | const: `pairwise-nym-binding-fact.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`contact/ref`](#field-contact-ref) | `yes` | string |  |
| [`context/kind`](#field-context-kind) | `yes` | ref: `#/$defs/context_kind` |  |
| [`context/ref`](#field-context-ref) | `no` | string |  |
| [`event/kind`](#field-event-kind) | `yes` | enum: `observed`, `rotated-into`, `retired` |  |
| [`nym/value`](#field-nym-value) | `yes` | string |  |
| [`prior/nym`](#field-prior-nym) | `no` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`detected/by`](#field-detected-by) | `yes` | string |  |
| [`evidence/ref`](#field-evidence-ref) | `no` | string |  |
| [`tx/id`](#field-tx-id) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`context_kind`](#def-context-kind) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `pairwise-nym-binding-fact.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-fact-id"></a>
## `fact/id`

- Required: `yes`
- Shape: string

<a id="field-contact-ref"></a>
## `contact/ref`

- Required: `yes`
- Shape: string

<a id="field-context-kind"></a>
## `context/kind`

- Required: `yes`
- Shape: ref: `#/$defs/context_kind`

<a id="field-context-ref"></a>
## `context/ref`

- Required: `no`
- Shape: string

<a id="field-event-kind"></a>
## `event/kind`

- Required: `yes`
- Shape: enum: `observed`, `rotated-into`, `retired`

<a id="field-nym-value"></a>
## `nym/value`

- Required: `yes`
- Shape: string

<a id="field-prior-nym"></a>
## `prior/nym`

- Required: `no`
- Shape: string

<a id="field-event-at"></a>
## `event/at`

- Required: `yes`
- Shape: string

<a id="field-detected-by"></a>
## `detected/by`

- Required: `yes`
- Shape: string

<a id="field-evidence-ref"></a>
## `evidence/ref`

- Required: `no`
- Shape: string

<a id="field-tx-id"></a>
## `tx/id`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-context-kind"></a>
## `$defs.context_kind`

- Shape: string
