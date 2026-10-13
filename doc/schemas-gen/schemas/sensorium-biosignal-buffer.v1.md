# Sensorium Biosignal Buffer v1

Source schema: [`doc/schemas/sensorium-biosignal-buffer.v1.schema.json`](../../schemas/sensorium-biosignal-buffer.v1.schema.json)

Draft nested tensor contract for the first P096 slice. Only f64le is implemented. JSON shape validity does not prove byte lengths, canonical base64 pad bits, finite present values, positive zero for missing values, or zero unused mask bits; the host performs those semantic checks before hashing or admission. This shape supplies no authority or source identity. Workers MUST normalize every negative zero, including present values, to positive zero. Hosts reject present negative zero. nonfinite/count is worker-declared diagnostic provenance: the host validates that it does not exceed mask missingness but cannot recover erased NaN/Inf bits. This buffer is a nested element of sensorium-biosignal-sample-block.v1, not a complete stream or sample block.

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
| [`dtype`](#field-dtype) | `yes` | const: `f64le` |  |
| [`shape`](#field-shape) | `yes` | array |  |
| [`layout`](#field-layout) | `yes` | const: `channels-by-samples` |  |
| [`values/b64u`](#field-values-b64u) | `yes` | string |  |
| [`missing/b64u`](#field-missing-b64u) | `yes` | string |  |
| [`nonfinite/count`](#field-nonfinite-count) | `yes` | integer |  |
## Field Semantics

<a id="field-dtype"></a>
## `dtype`

- Required: `yes`
- Shape: const: `f64le`

<a id="field-shape"></a>
## `shape`

- Required: `yes`
- Shape: array

<a id="field-layout"></a>
## `layout`

- Required: `yes`
- Shape: const: `channels-by-samples`

<a id="field-values-b64u"></a>
## `values/b64u`

- Required: `yes`
- Shape: string

<a id="field-missing-b64u"></a>
## `missing/b64u`

- Required: `yes`
- Shape: string

<a id="field-nonfinite-count"></a>
## `nonfinite/count`

- Required: `yes`
- Shape: integer
