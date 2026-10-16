# Sensorium-biosignal-window.v1

Source schema: [`doc/schemas/sensorium-biosignal-window.v1.schema.json`](../../schemas/sensorium-biosignal-window.v1.schema.json)

Transient synthetic window, grouped by independent preset. Min/max summarize present samples in the retained monotonic window; they are neither contact quality nor a feature recipe. Evictions count source blocks, not SDK losses. No physical sensing latency or continuity is inferred.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-biosignal-window.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`evidence/class`](#field-evidence-class) | `yes` | const: `synthetic` |  |
| [`quality`](#field-quality) | `yes` | const: `unknown` |  |
| [`position`](#field-position) | `yes` | string |  |
| [`retained/bytes`](#field-retained-bytes) | `yes` | integer |  |
| [`retained/high-water-bytes`](#field-retained-high-water-bytes) | `yes` | integer |  |
| [`evicted/blocks`](#field-evicted-blocks) | `yes` | integer |  |
| [`streams`](#field-streams) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-biosignal-window.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-evidence-class"></a>
## `evidence/class`

- Required: `yes`
- Shape: const: `synthetic`

<a id="field-quality"></a>
## `quality`

- Required: `yes`
- Shape: const: `unknown`

<a id="field-position"></a>
## `position`

- Required: `yes`
- Shape: string

<a id="field-retained-bytes"></a>
## `retained/bytes`

- Required: `yes`
- Shape: integer

<a id="field-retained-high-water-bytes"></a>
## `retained/high-water-bytes`

- Required: `yes`
- Shape: integer

<a id="field-evicted-blocks"></a>
## `evicted/blocks`

- Required: `yes`
- Shape: integer

<a id="field-streams"></a>
## `streams`

- Required: `yes`
- Shape: array
