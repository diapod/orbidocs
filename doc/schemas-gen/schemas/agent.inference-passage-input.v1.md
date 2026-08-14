# Agent Inference Passage Input v1

Source schema: [`doc/schemas/agent.inference-passage-input.v1.schema.json`](../../schemas/agent.inference-passage-input.v1.schema.json)

One host-admitted passage input containing only policy refs, lineage, classification, and digests. Prompt or privileged instruction text has no field.

## Governing Basis

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
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-input.v1` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`passage/no`](#field-passage-no) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | ref: `#/$defs/kind` |  |
| [`parent-product/refs`](#field-parent-product-refs) | `yes` | ref: `#/$defs/parents` |  |
| [`input/digest`](#field-input-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`instruction/hash`](#field-instruction-hash) | `yes` | ref: `#/$defs/instruction-hash` |  |
| [`prompt-policy/ref`](#field-prompt-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`output-schema/ref`](#field-output-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`repair-profile/ref`](#field-repair-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`model-profile/ref`](#field-model-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`visibility`](#field-visibility) | `yes` | ref: `#/$defs/visibility` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`admitted/at`](#field-admitted-at) | `yes` | string |  |
| [`admitted/by`](#field-admitted-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`instruction-hash`](#def-instruction-hash) | string |  |
| [`kind`](#def-kind) | enum: `draft`, `critique`, `revision`, `final` |  |
| [`visibility`](#def-visibility) | enum: `private`, `operator`, `shared` |  |
| [`parents`](#def-parents) | array |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "kind": {
      "const": "draft"
    }
  },
  "required": [
    "kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "parent-product/refs": {
      "maxItems": 0
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-input.v1`

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-passage-no"></a>
## `passage/no`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: ref: `#/$defs/kind`

<a id="field-parent-product-refs"></a>
## `parent-product/refs`

- Required: `yes`
- Shape: ref: `#/$defs/parents`

<a id="field-input-digest"></a>
## `input/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-instruction-hash"></a>
## `instruction/hash`

- Required: `yes`
- Shape: ref: `#/$defs/instruction-hash`

<a id="field-prompt-policy-ref"></a>
## `prompt-policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-output-schema-ref"></a>
## `output-schema/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-repair-profile-ref"></a>
## `repair-profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-model-profile-ref"></a>
## `model-profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-visibility"></a>
## `visibility`

- Required: `yes`
- Shape: ref: `#/$defs/visibility`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-idempotency-key"></a>
## `idempotency/key`

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

<a id="def-instruction-hash"></a>
## `$defs.instruction-hash`

- Shape: string

<a id="def-kind"></a>
## `$defs.kind`

- Shape: enum: `draft`, `critique`, `revision`, `final`

<a id="def-visibility"></a>
## `$defs.visibility`

- Shape: enum: `private`, `operator`, `shared`

<a id="def-parents"></a>
## `$defs.parents`

- Shape: array
