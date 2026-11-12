# Weak-signal-review.v1

Source schema: [`doc/schemas/weak-signal-review.v1.schema.json`](../../schemas/weak-signal-review.v1.schema.json)

Immutable local review with exact admitted material inventory and private claim bindings. A review grants no publication authority. Owner checks bytes, current custody and lineage; summary contains no raw refs or horizons.

## Governing Basis

- [`doc/project/40-proposals/078-weak-signal-harvester.md`](../../project/40-proposals/078-weak-signal-harvester.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

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
| [`schema`](#field-schema) | `yes` | const: `weak-signal-review.v1` |  |
| [`review/id`](#field-review-id) | `yes` | string |  |
| [`reviewed/by`](#field-reviewed-by) | `yes` | const: `operator:local-control` |  |
| [`reviewed/at`](#field-reviewed-at) | `yes` | string |  |
| [`review/revision`](#field-review-revision) | `yes` | integer |  |
| [`review/request`](#field-review-request) | `yes` | ref: `#/$defs/request` |  |
| [`material/findings`](#field-material-findings) | `yes` | array |  |
| [`custody/claims`](#field-custody-claims) | `yes` | array |  |
| [`origin`](#field-origin) | `yes` | ref: `whisper-origin.v1.schema.json` |  |
| [`execution/receipt`](#field-execution-receipt) | `yes` | ref: `execution-receipt.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`request`](#def-request) | object |  |
| [`custody-claim`](#def-custody-claim) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `weak-signal-review.v1`

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

<a id="field-review-revision"></a>
## `review/revision`

- Required: `yes`
- Shape: integer

<a id="field-review-request"></a>
## `review/request`

- Required: `yes`
- Shape: ref: `#/$defs/request`

<a id="field-material-findings"></a>
## `material/findings`

- Required: `yes`
- Shape: array

<a id="field-custody-claims"></a>
## `custody/claims`

- Required: `yes`
- Shape: array

<a id="field-origin"></a>
## `origin`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json`

<a id="field-execution-receipt"></a>
## `execution/receipt`

- Required: `yes`
- Shape: ref: `execution-receipt.v1.schema.json`

## Definition Semantics

<a id="def-request"></a>
## `$defs.request`

- Shape: object

<a id="def-custody-claim"></a>
## `$defs.custody-claim`

- Shape: object
