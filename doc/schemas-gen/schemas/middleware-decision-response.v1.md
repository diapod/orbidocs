# Middleware Decision Response v1

Source schema: [`doc/schemas/middleware-decision-response.v1.schema.json`](../../schemas/middleware-decision-response.v1.schema.json)

Host-facing decision returned by middleware chain handlers.

## Governing Basis

- [`doc/project/40-proposals/068-api-surface-projection.md`](../../project/40-proposals/068-api-surface-projection.md)

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
| [`decision`](#field-decision) | `yes` | enum: `allow`, `annotate`, `rewrite`, `route`, `return`, `drop`, `defer`, `reject` |  |
| [`reason`](#field-reason) | `yes` | string |  |
| [`annotations`](#field-annotations) | `no` | object |  |
| [`patch_strategy`](#field-patch-strategy) | `no` | string \| null |  |
| [`patch`](#field-patch) | `no` | any |  |
| [`route`](#field-route) | `no` | object \| null |  |
| [`next_step`](#field-next-step) | `no` | string \| null |  |
| [`diagnostics`](#field-diagnostics) | `no` | object |  |
## Field Semantics

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `allow`, `annotate`, `rewrite`, `route`, `return`, `drop`, `defer`, `reject`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

<a id="field-annotations"></a>
## `annotations`

- Required: `no`
- Shape: object

<a id="field-patch-strategy"></a>
## `patch_strategy`

- Required: `no`
- Shape: string | null

<a id="field-patch"></a>
## `patch`

- Required: `no`
- Shape: any

<a id="field-route"></a>
## `route`

- Required: `no`
- Shape: object | null

<a id="field-next-step"></a>
## `next_step`

- Required: `no`
- Shape: string | null

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: object
