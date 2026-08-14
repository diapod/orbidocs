# Agent Inference Passage Product v1

Source schema: [`doc/schemas/agent.inference-passage-product.v1.schema.json`](../../schemas/agent.inference-passage-product.v1.schema.json)

A metadata-only structured intermediate or final product. Retained bytes are addressed through an artifact ref and digest, never carried inline.

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
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-product.v1` |  |
| [`product/ref`](#field-product-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`kind`](#field-kind) | `yes` | enum: `draft`, `critique`, `revision`, `final` |  |
| [`parent-product/refs`](#field-parent-product-refs) | `yes` | array |  |
| [`content/digest`](#field-content-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`content/size-bytes`](#field-content-size-bytes) | `yes` | integer |  |
| [`artifact/ref`](#field-artifact-ref) | `no` | ref: `#/$defs/ref` |  |
| [`retained`](#field-retained) | `yes` | boolean |  |
| [`output-schema/ref`](#field-output-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`model/snapshot`](#field-model-snapshot) | `yes` | ref: `#/$defs/ref` |  |
| [`budget/used`](#field-budget-used) | `yes` | ref: `#/$defs/budget` |  |
| [`visibility`](#field-visibility) | `yes` | enum: `private`, `operator`, `shared` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`committed/at`](#field-committed-at) | `yes` | string |  |
| [`committed/by`](#field-committed-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`budget`](#def-budget) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "retained": {
      "const": true
    }
  },
  "required": [
    "retained"
  ]
}
```

Then:

```json
{
  "required": [
    "artifact/ref"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-product.v1`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

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

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `draft`, `critique`, `revision`, `final`

<a id="field-parent-product-refs"></a>
## `parent-product/refs`

- Required: `yes`
- Shape: array

<a id="field-content-digest"></a>
## `content/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-content-size-bytes"></a>
## `content/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-retained"></a>
## `retained`

- Required: `yes`
- Shape: boolean

<a id="field-output-schema-ref"></a>
## `output-schema/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-model-snapshot"></a>
## `model/snapshot`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-budget-used"></a>
## `budget/used`

- Required: `yes`
- Shape: ref: `#/$defs/budget`

<a id="field-visibility"></a>
## `visibility`

- Required: `yes`
- Shape: enum: `private`, `operator`, `shared`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-committed-at"></a>
## `committed/at`

- Required: `yes`
- Shape: string

<a id="field-committed-by"></a>
## `committed/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-budget"></a>
## `$defs.budget`

- Shape: object
