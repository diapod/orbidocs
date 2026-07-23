# Inquirium Local Model Acceptance Report v1

Source schema: [`doc/schemas/inquirium.local-model-acceptance-report.v1.schema.json`](../../schemas/inquirium.local-model-acceptance-report.v1.schema.json)

Closed metadata-only evidence that one real local model package passed lifecycle and inference acceptance.

## Governing Basis

- [`doc/project/60-solutions/046-inquirium.md`](../../project/60-solutions/046-inquirium.md)
- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.local-model-acceptance-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | enum: `macos-arm64-metal`, `linux-x86_64-cpu` |  |
| [`llama-server`](#field-llama-server) | `yes` | object |  |
| [`model`](#field-model) | `yes` | object |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`measurements`](#field-measurements) | `yes` | object |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
| [`generations`](#field-generations) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.local-model-acceptance-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: enum: `macos-arm64-metal`, `linux-x86_64-cpu`

<a id="field-llama-server"></a>
## `llama-server`

- Required: `yes`
- Shape: object

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: object

<a id="field-checks"></a>
## `checks`

- Required: `yes`
- Shape: array

<a id="field-measurements"></a>
## `measurements`

- Required: `yes`
- Shape: object

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object

<a id="field-generations"></a>
## `generations`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
