# Agent Inference Flow Binding v1

Source schema: [`doc/schemas/agent.inference-flow-binding.v1.schema.json`](../../schemas/agent.inference-flow-binding.v1.schema.json)

A host-admitted closed vocabulary binding one JSON-e Flow to one Agent and its existing Agent binding.

## Governing Basis

- [`doc/project/40-proposals/049-json-e-flow-middleware.md`](../../project/40-proposals/049-json-e-flow-middleware.md)
- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
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
| [`schema`](#field-schema) | `yes` | const: `agent.inference-flow-binding.v1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/digest`](#field-binding-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`flow/ref`](#field-flow-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`flow/digest`](#field-flow-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`max/passages`](#field-max-passages) | `yes` | integer |  |
| [`prompt-policy/refs`](#field-prompt-policy-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`output-schema/refs`](#field-output-schema-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`repair-profile/refs`](#field-repair-profile-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`model-profile/refs`](#field-model-profile-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`runtime/refs`](#field-runtime-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`visibility/ceiling`](#field-visibility-ceiling) | `yes` | ref: `#/$defs/visibility` |  |
| [`classification/ceiling`](#field-classification-ceiling) | `yes` | enum: `Personal`, `Community`, `Public` |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`created/by`](#field-created-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`visibility`](#def-visibility) | enum: `private`, `operator`, `shared` |  |
| [`ref-set`](#def-ref-set) | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-flow-binding.v1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-digest"></a>
## `binding/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-flow-ref"></a>
## `flow/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-flow-digest"></a>
## `flow/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-max-passages"></a>
## `max/passages`

- Required: `yes`
- Shape: integer

<a id="field-prompt-policy-refs"></a>
## `prompt-policy/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-output-schema-refs"></a>
## `output-schema/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-repair-profile-refs"></a>
## `repair-profile/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-model-profile-refs"></a>
## `model-profile/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-runtime-refs"></a>
## `runtime/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-visibility-ceiling"></a>
## `visibility/ceiling`

- Required: `yes`
- Shape: ref: `#/$defs/visibility`

<a id="field-classification-ceiling"></a>
## `classification/ceiling`

- Required: `yes`
- Shape: enum: `Personal`, `Community`, `Public`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-created-by"></a>
## `created/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-visibility"></a>
## `$defs.visibility`

- Shape: enum: `private`, `operator`, `shared`

<a id="def-ref-set"></a>
## `$defs.ref-set`

- Shape: array
