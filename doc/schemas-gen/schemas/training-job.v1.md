# Training Job v1

Source schema: [`doc/schemas/training-job.v1.schema.json`](../../schemas/training-job.v1.schema.json)

Machine-readable schema for adapter-first specialization jobs built from approved corpus entries.

## Governing Basis

- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)

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
| [`job/id`](#field-job-id) | `yes` | string | Stable identifier of the specialization job. |
| [`base-model/ref`](#field-base-model-ref) | `yes` | string | Reference to the immutable base model on which specialization is built. |
| [`method`](#field-method) | `yes` | enum: `lora`, `qlora` | Adapter-first specialization method. |
| [`dataset/refs`](#field-dataset-refs) | `yes` | array | Corpus or dataset references used by the job. |
| [`policy/profile`](#field-policy-profile) | `yes` | string | Training policy profile applied to this job. |
| [`started-at`](#field-started-at) | `yes` | string | Job start timestamp. |
| [`ended-at`](#field-ended-at) | `no` | string | Job completion timestamp. |
| [`operator/ref`](#field-operator-ref) | `yes` | string | Human or policy actor responsible for starting the job. |
| [`status`](#field-status) | `no` | enum: `running`, `completed`, `failed`, `canceled` | Current or terminal job status. |
| [`eval-report/ref`](#field-eval-report-ref) | `no` | string | Reference to evaluation output when the job completes. |
| [`creator/refs`](#field-creator-refs) | `no` | array | Creator or contributor references that should survive into attribution-sensitive adapter artifacts. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core training-job semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "completed"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "ended-at",
    "eval-report/ref"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "ended-at": {
      "type": "string"
    }
  },
  "required": [
    "ended-at"
  ]
}
```

Then:

```json
{
  "required": [
    "status"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-job-id"></a>
## `job/id`

- Required: `yes`
- Shape: string

Stable identifier of the specialization job.

<a id="field-base-model-ref"></a>
## `base-model/ref`

- Required: `yes`
- Shape: string

Reference to the immutable base model on which specialization is built.

<a id="field-method"></a>
## `method`

- Required: `yes`
- Shape: enum: `lora`, `qlora`

Adapter-first specialization method.

<a id="field-dataset-refs"></a>
## `dataset/refs`

- Required: `yes`
- Shape: array

Corpus or dataset references used by the job.

<a id="field-policy-profile"></a>
## `policy/profile`

- Required: `yes`
- Shape: string

Training policy profile applied to this job.

<a id="field-started-at"></a>
## `started-at`

- Required: `yes`
- Shape: string

Job start timestamp.

<a id="field-ended-at"></a>
## `ended-at`

- Required: `no`
- Shape: string

Job completion timestamp.

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: string

Human or policy actor responsible for starting the job.

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: enum: `running`, `completed`, `failed`, `canceled`

Current or terminal job status.

<a id="field-eval-report-ref"></a>
## `eval-report/ref`

- Required: `no`
- Shape: string

Reference to evaluation output when the job completes.

<a id="field-creator-refs"></a>
## `creator/refs`

- Required: `no`
- Shape: array

Creator or contributor references that should survive into attribution-sensitive adapter artifacts.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core training-job semantics.
