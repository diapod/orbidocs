# Inquirium Local Model Acceptance Report v2

Source schema: [`doc/schemas/inquirium.local-model-acceptance-report.v2.schema.json`](../../schemas/inquirium.local-model-acceptance-report.v2.schema.json)

Provider-neutral, metadata-only evidence for one real managed local-model package and independently probed runtime capabilities.

## Governing Basis

- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/066-inquirium-assistant-channel.md`](../../project/40-proposals/066-inquirium-assistant-channel.md)

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.local-model-acceptance-report.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | enum: `macos-arm64-metal`, `linux-x86_64-cpu` |  |
| [`runtime`](#field-runtime) | `yes` | object |  |
| [`model`](#field-model) | `yes` | object |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`capabilities`](#field-capabilities) | `yes` | object |  |
| [`measurements`](#field-measurements) | `yes` | object |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
| [`generations`](#field-generations) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`label`](#def-label) | string |  |
| [`capabilityFact`](#def-capabilityfact) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.local-model-acceptance-report.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: enum: `macos-arm64-metal`, `linux-x86_64-cpu`

<a id="field-runtime"></a>
## `runtime`

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

<a id="field-capabilities"></a>
## `capabilities`

- Required: `yes`
- Shape: object

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

<a id="def-label"></a>
## `$defs.label`

- Shape: string

<a id="def-capabilityfact"></a>
## `$defs.capabilityFact`

- Shape: object
