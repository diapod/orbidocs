# Learning Outcome v1

Source schema: [`doc/schemas/learning-outcome.v1.schema.json`](../../schemas/learning-outcome.v1.schema.json)

Machine-readable schema for durable correction outcomes produced inside a question-bound answer-room flow.

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
| [`learning-outcome/id`](#field-learning-outcome-id) | `yes` | string | Stable identifier of the correction or confirmation outcome. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier that roots the learning event. |
| [`room/id`](#field-room-id) | `yes` | string | Answer-room or tightly linked review path where the outcome emerged. |
| [`subject/ref`](#field-subject-ref) | `yes` | string | Reference to the disputed or reviewed answer artifact. |
| [`outcome/status`](#field-outcome-status) | `yes` | enum: `confirmed`, `corrected`, `unresolved` | Epistemic result of the correction path. |
| [`decided-at`](#field-decided-at) | `yes` | string | Timestamp at which the outcome was frozen. |
| [`decider/ref`](#field-decider-ref) | `yes` | string | Node, secretary, or policy actor that froze the outcome. |
| [`supporting/refs`](#field-supporting-refs) | `yes` | array | Evidence, summary, transcript, or response references that support the outcome. |
| [`provenance/refs`](#field-provenance-refs) | `yes` | array | Trace references sufficient to rebuild the causal chain of the outcome. |
| [`summary/ref`](#field-summary-ref) | `no` | string | Accepted room summary reference when the outcome is expressed through a summary artifact. |
| [`response-envelope/ref`](#field-response-envelope-ref) | `no` | string | Corrected or accepted response-envelope reference when a final answer artifact exists. |
| [`reason/codes`](#field-reason-codes) | `no` | array | Short machine-readable reason tags used by local policy and later audit. |
| [`human-linked/input`](#field-human-linked-input) | `yes` | boolean | Whether the accepted or unresolved outcome depended on human-originated input. |
| [`policy/profile`](#field-policy-profile) | `no` | string | Optional local or federation policy profile that governed the correction path. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core outcome semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome/status": {
      "const": "corrected"
    }
  },
  "required": [
    "outcome/status"
  ]
}
```

Then:

```json
{
  "anyOf": [
    {
      "required": [
        "summary/ref"
      ]
    },
    {
      "required": [
        "response-envelope/ref"
      ]
    }
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-learning-outcome-id"></a>
## `learning-outcome/id`

- Required: `yes`
- Shape: string

Stable identifier of the correction or confirmation outcome.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier that roots the learning event.

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

Answer-room or tightly linked review path where the outcome emerged.

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: string

Reference to the disputed or reviewed answer artifact.

<a id="field-outcome-status"></a>
## `outcome/status`

- Required: `yes`
- Shape: enum: `confirmed`, `corrected`, `unresolved`

Epistemic result of the correction path.

<a id="field-decided-at"></a>
## `decided-at`

- Required: `yes`
- Shape: string

Timestamp at which the outcome was frozen.

<a id="field-decider-ref"></a>
## `decider/ref`

- Required: `yes`
- Shape: string

Node, secretary, or policy actor that froze the outcome.

<a id="field-supporting-refs"></a>
## `supporting/refs`

- Required: `yes`
- Shape: array

Evidence, summary, transcript, or response references that support the outcome.

<a id="field-provenance-refs"></a>
## `provenance/refs`

- Required: `yes`
- Shape: array

Trace references sufficient to rebuild the causal chain of the outcome.

<a id="field-summary-ref"></a>
## `summary/ref`

- Required: `no`
- Shape: string

Accepted room summary reference when the outcome is expressed through a summary artifact.

<a id="field-response-envelope-ref"></a>
## `response-envelope/ref`

- Required: `no`
- Shape: string

Corrected or accepted response-envelope reference when a final answer artifact exists.

<a id="field-reason-codes"></a>
## `reason/codes`

- Required: `no`
- Shape: array

Short machine-readable reason tags used by local policy and later audit.

<a id="field-human-linked-input"></a>
## `human-linked/input`

- Required: `yes`
- Shape: boolean

Whether the accepted or unresolved outcome depended on human-originated input.

<a id="field-policy-profile"></a>
## `policy/profile`

- Required: `no`
- Shape: string

Optional local or federation policy profile that governed the correction path.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core outcome semantics.
