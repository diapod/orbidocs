# Inquirium Candidate Plan v1

Source schema: [`doc/schemas/inquirium.candidate-plan.v1.schema.json`](../../schemas/inquirium.candidate-plan.v1.schema.json)

A bounded model-authored plan candidate. The value is inert until a host compiles and admits each effect.

## Governing Basis

- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.candidate-plan.v1` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`adapter.manifest/ref`](#field-adapter-manifest-ref) | `no` | ref: `#/$defs/ref` | Optional producer provenance for adapter-authored plans. Portable envelope-admitted plans omit this local implementation reference. |
| [`nodes`](#field-nodes) | `yes` | array |  |
| [`edges`](#field-edges) | `no` | array |  |
| [`budget`](#field-budget) | `yes` | ref: `#/$defs/budget` |  |
| [`cancellation`](#field-cancellation) | `no` | ref: `#/$defs/cancellation` |  |
| [`metadata`](#field-metadata) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`operation`](#def-operation) | enum: `generate`, `embed`, `batch_embed`, `classify`, `rerank`, `summarize`, `transform`, `image_generate`, `image_edit`, `train_adapt` |  |
| [`node`](#def-node) | unspecified |  |
| [`edge`](#def-edge) | object |  |
| [`budget`](#def-budget) | object |  |
| [`cancellation`](#def-cancellation) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.candidate-plan.v1`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-adapter-manifest-ref"></a>
## `adapter.manifest/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

Optional producer provenance for adapter-authored plans. Portable envelope-admitted plans omit this local implementation reference.

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: array

<a id="field-edges"></a>
## `edges`

- Required: `no`
- Shape: array

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: ref: `#/$defs/budget`

<a id="field-cancellation"></a>
## `cancellation`

- Required: `no`
- Shape: ref: `#/$defs/cancellation`

<a id="field-metadata"></a>
## `metadata`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-operation"></a>
## `$defs.operation`

- Shape: enum: `generate`, `embed`, `batch_embed`, `classify`, `rerank`, `summarize`, `transform`, `image_generate`, `image_edit`, `train_adapt`

<a id="def-node"></a>
## `$defs.node`

- Shape: unspecified

<a id="def-edge"></a>
## `$defs.edge`

- Shape: object

<a id="def-budget"></a>
## `$defs.budget`

- Shape: object

<a id="def-cancellation"></a>
## `$defs.cancellation`

- Shape: object
