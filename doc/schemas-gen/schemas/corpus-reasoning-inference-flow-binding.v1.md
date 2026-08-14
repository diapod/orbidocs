# Corpus Reasoning Inference Flow Binding v1

Source schema: [`doc/schemas/corpus-reasoning-inference-flow-binding.v1.schema.json`](../../schemas/corpus-reasoning-inference-flow-binding.v1.schema.json)

Corpus-owned authority binding one Agent inference Flow to one current Room role, locally accepted instruction overlay, turn, policy generation, and unpublished draft sink.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-reasoning-inference-flow-binding.v1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/digest`](#field-binding-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`participant`](#field-participant) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent-flow-binding/ref`](#field-agent-flow-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent-flow-binding/digest`](#field-agent-flow-binding-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`role-assignment/ref`](#field-role-assignment-ref) | `yes` | string |  |
| [`role-assignment/revision`](#field-role-assignment-revision) | `yes` | integer |  |
| [`role-assignment/digest`](#field-role-assignment-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`instruction-overlay/ref`](#field-instruction-overlay-ref) | `yes` | string |  |
| [`instruction-overlay/revision`](#field-instruction-overlay-revision) | `yes` | integer |  |
| [`instruction-overlay/digest`](#field-instruction-overlay-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`turn/no`](#field-turn-no) | `yes` | integer |  |
| [`room-policy/ref`](#field-room-policy-ref) | `yes` | string |  |
| [`room-policy/digest`](#field-room-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`prompt-policy/ref`](#field-prompt-policy-ref) | `yes` | string |  |
| [`classification/ceiling`](#field-classification-ceiling) | `yes` | enum: `Personal`, `Community`, `Public` |  |
| [`exposure`](#field-exposure) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`intermediate/visibility-ceiling`](#field-intermediate-visibility-ceiling) | `yes` | enum: `private`, `operator` |  |
| [`terminal/disposition`](#field-terminal-disposition) | `yes` | const: `unpublished-corpus-draft` |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`admitted/at`](#field-admitted-at) | `yes` | string |  |
| [`admitted/by`](#field-admitted-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-reasoning-inference-flow-binding.v1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-digest"></a>
## `binding/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-participant"></a>
## `participant`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-flow-binding-ref"></a>
## `agent-flow-binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-flow-binding-digest"></a>
## `agent-flow-binding/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-role-assignment-ref"></a>
## `role-assignment/ref`

- Required: `yes`
- Shape: string

<a id="field-role-assignment-revision"></a>
## `role-assignment/revision`

- Required: `yes`
- Shape: integer

<a id="field-role-assignment-digest"></a>
## `role-assignment/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-instruction-overlay-ref"></a>
## `instruction-overlay/ref`

- Required: `yes`
- Shape: string

<a id="field-instruction-overlay-revision"></a>
## `instruction-overlay/revision`

- Required: `yes`
- Shape: integer

<a id="field-instruction-overlay-digest"></a>
## `instruction-overlay/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-turn-no"></a>
## `turn/no`

- Required: `yes`
- Shape: integer

<a id="field-room-policy-ref"></a>
## `room-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-room-policy-digest"></a>
## `room-policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-prompt-policy-ref"></a>
## `prompt-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-classification-ceiling"></a>
## `classification/ceiling`

- Required: `yes`
- Shape: enum: `Personal`, `Community`, `Public`

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-intermediate-visibility-ceiling"></a>
## `intermediate/visibility-ceiling`

- Required: `yes`
- Shape: enum: `private`, `operator`

<a id="field-terminal-disposition"></a>
## `terminal/disposition`

- Required: `yes`
- Shape: const: `unpublished-corpus-draft`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-admitted-at"></a>
## `admitted/at`

- Required: `yes`
- Shape: string

<a id="field-admitted-by"></a>
## `admitted/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
