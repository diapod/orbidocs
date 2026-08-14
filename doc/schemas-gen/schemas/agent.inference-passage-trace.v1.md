# Agent Inference Passage Trace v1

Source schema: [`doc/schemas/agent.inference-passage-trace.v1.schema.json`](../../schemas/agent.inference-passage-trace.v1.schema.json)

Prompt-free metadata trace for one passage transition. Prompt text, product content, private reasoning, protected source bytes, signatures, and secrets have no representation.

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
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-trace.v1` |  |
| [`trace/ref`](#field-trace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`passage/no`](#field-passage-no) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | enum: `draft`, `critique`, `revision`, `final` |  |
| [`state`](#field-state) | `yes` | enum: `admitted`, `committed`, `refused`, `selected` |  |
| [`input/digest`](#field-input-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`product/ref`](#field-product-ref) | `no` | ref: `#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `no` | ref: `#/$defs/digest` |  |
| [`parent-product/refs`](#field-parent-product-refs) | `yes` | array |  |
| [`prompt-policy/ref`](#field-prompt-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`output-schema/ref`](#field-output-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`repair-profile/ref`](#field-repair-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`model-profile/ref`](#field-model-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`model/snapshot`](#field-model-snapshot) | `no` | ref: `#/$defs/ref` |  |
| [`visibility`](#field-visibility) | `yes` | enum: `private`, `operator`, `shared` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`instruction/hash`](#field-instruction-hash) | `yes` | ref: `#/$defs/instruction-hash` |  |
| [`budget/used`](#field-budget-used) | `yes` | ref: `#/$defs/budget` |  |
| [`decision/code`](#field-decision-code) | `yes` | enum: `passage-admitted`, `passage-committed`, `terminal-product-selected`, `passage-request-refused`, `passage-invocation-refused`, `passage-response-refused`, `passage-artifact-refused`, `passage-commit-refused` |  |
| [`at`](#field-at) | `yes` | string |  |
| [`by`](#field-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`instruction-hash`](#def-instruction-hash) | string |  |
| [`budget`](#def-budget) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "enum": [
        "committed",
        "selected"
      ]
    }
  },
  "required": [
    "state"
  ]
}
```

Then:

```json
{
  "required": [
    "product/ref",
    "product/digest",
    "model/snapshot"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "state": {
      "enum": [
        "admitted",
        "refused"
      ]
    }
  },
  "required": [
    "state"
  ]
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "product/ref"
        ]
      },
      {
        "required": [
          "product/digest"
        ]
      },
      {
        "required": [
          "model/snapshot"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-trace.v1`

<a id="field-trace-ref"></a>
## `trace/ref`

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

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-passage-no"></a>
## `passage/no`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `draft`, `critique`, `revision`, `final`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `admitted`, `committed`, `refused`, `selected`

<a id="field-input-digest"></a>
## `input/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-parent-product-refs"></a>
## `parent-product/refs`

- Required: `yes`
- Shape: array

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

<a id="field-model-snapshot"></a>
## `model/snapshot`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-visibility"></a>
## `visibility`

- Required: `yes`
- Shape: enum: `private`, `operator`, `shared`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-instruction-hash"></a>
## `instruction/hash`

- Required: `yes`
- Shape: ref: `#/$defs/instruction-hash`

<a id="field-budget-used"></a>
## `budget/used`

- Required: `yes`
- Shape: ref: `#/$defs/budget`

<a id="field-decision-code"></a>
## `decision/code`

- Required: `yes`
- Shape: enum: `passage-admitted`, `passage-committed`, `terminal-product-selected`, `passage-request-refused`, `passage-invocation-refused`, `passage-response-refused`, `passage-artifact-refused`, `passage-commit-refused`

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: string

<a id="field-by"></a>
## `by`

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

<a id="def-budget"></a>
## `$defs.budget`

- Shape: object
