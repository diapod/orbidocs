# Weak Signal Web Review v1

Source schema: [`doc/schemas/weak-signal-web-review.v1.schema.json`](../../schemas/weak-signal-web-review.v1.schema.json)

Immutable local operator review bound to an admitted finding digest. Redacted text is operator-authored; this decision grants no publication authority.

## Governing Basis

- [`doc/project/40-proposals/078-weak-signal-harvester.md`](../../project/40-proposals/078-weak-signal-harvester.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `weak-signal-web-review.v1` |  |
| [`review/id`](#field-review-id) | `yes` | string |  |
| [`reviewed/by`](#field-reviewed-by) | `yes` | const: `operator:local-control` |  |
| [`reviewed/at`](#field-reviewed-at) | `yes` | string |  |
| [`review/request`](#field-review-request) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `weak-signal-web-review.v1`

<a id="field-review-id"></a>
## `review/id`

- Required: `yes`
- Shape: string

<a id="field-reviewed-by"></a>
## `reviewed/by`

- Required: `yes`
- Shape: const: `operator:local-control`

<a id="field-reviewed-at"></a>
## `reviewed/at`

- Required: `yes`
- Shape: string

<a id="field-review-request"></a>
## `review/request`

- Required: `yes`
- Shape: object
