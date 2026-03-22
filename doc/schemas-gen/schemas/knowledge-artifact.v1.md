# Knowledge Artifact v1

Source schema: [`doc/schemas/knowledge-artifact.v1.schema.json`](../../schemas/knowledge-artifact.v1.schema.json)

Machine-readable schema for local or portable knowledge artifacts promoted from learning outcomes.

## Governing Basis

- [`doc/project/30-stories/story-002.md`](../../project/30-stories/story-002.md)
- [`doc/project/50-requirements/requirements-002.md`](../../project/50-requirements/requirements-002.md)
- [`doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`](../../project/40-proposals/012-learning-outcomes-and-archival-contracts.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-002.md`](../../project/50-requirements/requirements-002.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)
- [`doc/project/50-requirements/requirements-005.md`](../../project/50-requirements/requirements-005.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-002.md`](../../project/30-stories/story-002.md)
- [`doc/project/30-stories/story-003.md`](../../project/30-stories/story-003.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`knowledge-artifact/id`](#field-knowledge-artifact-id) | `yes` | string | Stable identifier of the promoted artifact. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier from which the artifact ultimately derives. |
| [`source/learning-outcome-id`](#field-source-learning-outcome-id) | `yes` | string | LearningOutcome identifier that justified the promotion. |
| [`artifact/class`](#field-artifact-class) | `yes` | enum: `trusted-local-retrieval`, `review-only`, `corpus-candidate`, `training-candidate` | Semantic class of the promoted artifact. |
| [`target/kind`](#field-target-kind) | `yes` | enum: `vector-memory`, `indexed-file`, `corpus-entry`, `training-queue` | Primary downstream target represented by the artifact. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp of promotion into the target layer. |
| [`content/ref`](#field-content-ref) | `yes` | string | Stable content or storage reference used by the target layer. |
| [`provenance/refs`](#field-provenance-refs) | `yes` | array | References that link the artifact back to room outputs, summaries, or other source material. |
| [`trust/status`](#field-trust-status) | `yes` | enum: `confirmed`, `corrected`, `unresolved` | Inherited trust class from the source learning outcome. |
| [`training/eligible`](#field-training-eligible) | `no` | boolean | Whether this artifact is currently eligible for later training jobs. |
| [`human-linked/input`](#field-human-linked-input) | `no` | boolean | Whether the artifact preserves accepted human-linked influence in its provenance. |
| [`domain/tags`](#field-domain-tags) | `no` | array | Optional local or federation domain tags assigned during promotion. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional policy metadata that does not change the core promotion semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "trust/status": {
      "const": "unresolved"
    }
  },
  "required": [
    "trust/status"
  ]
}
```

Then:

```json
{
  "properties": {
    "artifact/class": {
      "const": "review-only"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "artifact/class": {
      "const": "training-candidate"
    }
  },
  "required": [
    "artifact/class"
  ]
}
```

Then:

```json
{
  "properties": {
    "target/kind": {
      "const": "training-queue"
    },
    "training/eligible": {
      "const": true
    }
  },
  "required": [
    "training/eligible"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "artifact/class": {
      "const": "trusted-local-retrieval"
    }
  },
  "required": [
    "artifact/class"
  ]
}
```

Then:

```json
{
  "properties": {
    "target/kind": {
      "enum": [
        "vector-memory",
        "indexed-file"
      ]
    },
    "trust/status": {
      "enum": [
        "confirmed",
        "corrected"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-knowledge-artifact-id"></a>
## `knowledge-artifact/id`

- Required: `yes`
- Shape: string

Stable identifier of the promoted artifact.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier from which the artifact ultimately derives.

<a id="field-source-learning-outcome-id"></a>
## `source/learning-outcome-id`

- Required: `yes`
- Shape: string

LearningOutcome identifier that justified the promotion.

<a id="field-artifact-class"></a>
## `artifact/class`

- Required: `yes`
- Shape: enum: `trusted-local-retrieval`, `review-only`, `corpus-candidate`, `training-candidate`

Semantic class of the promoted artifact.

<a id="field-target-kind"></a>
## `target/kind`

- Required: `yes`
- Shape: enum: `vector-memory`, `indexed-file`, `corpus-entry`, `training-queue`

Primary downstream target represented by the artifact.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp of promotion into the target layer.

<a id="field-content-ref"></a>
## `content/ref`

- Required: `yes`
- Shape: string

Stable content or storage reference used by the target layer.

<a id="field-provenance-refs"></a>
## `provenance/refs`

- Required: `yes`
- Shape: array

References that link the artifact back to room outputs, summaries, or other source material.

<a id="field-trust-status"></a>
## `trust/status`

- Required: `yes`
- Shape: enum: `confirmed`, `corrected`, `unresolved`

Inherited trust class from the source learning outcome.

<a id="field-training-eligible"></a>
## `training/eligible`

- Required: `no`
- Shape: boolean

Whether this artifact is currently eligible for later training jobs.

<a id="field-human-linked-input"></a>
## `human-linked/input`

- Required: `no`
- Shape: boolean

Whether the artifact preserves accepted human-linked influence in its provenance.

<a id="field-domain-tags"></a>
## `domain/tags`

- Required: `no`
- Shape: array

Optional local or federation domain tags assigned during promotion.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional policy metadata that does not change the core promotion semantics.
