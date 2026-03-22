# Adapter Artifact v1

Source schema: [`doc/schemas/adapter-artifact.v1.schema.json`](../../schemas/adapter-artifact.v1.schema.json)

Machine-readable schema for adapter-first specialization artifacts and their deployment-facing provenance.

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
| [`adapter/id`](#field-adapter-id) | `yes` | string | Stable identifier of the adapter artifact. |
| [`job/id`](#field-job-id) | `yes` | string | TrainingJob identifier that produced the adapter. |
| [`base-model/ref`](#field-base-model-ref) | `yes` | string | Immutable base model on top of which the adapter applies. |
| [`adapter/hash`](#field-adapter-hash) | `yes` | string | Hash or equivalent immutable content identifier of the adapter payload. |
| [`eval-report/ref`](#field-eval-report-ref) | `yes` | string | Reference to evaluation results that justify deployment or rejection. |
| [`deployment/scope`](#field-deployment-scope) | `yes` | enum: `private`, `federation-local`, `public` | Intended deployment visibility of the adapter artifact. |
| [`rollback/ref`](#field-rollback-ref) | `yes` | string | Reference to rollback path, previous adapter, or disable artifact. |
| [`creator/refs`](#field-creator-refs) | `yes` | array | Creators or contributors that should remain attributable in downstream use. |
| [`status`](#field-status) | `no` | enum: `validated`, `deployed`, `rejected`, `revoked` | Current artifact lifecycle status. |
| [`model-card/ref`](#field-model-card-ref) | `no` | string | Reference to model card or equivalent manifest describing intended use and risks. |
| [`created-at`](#field-created-at) | `no` | string | Artifact creation timestamp. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core adapter semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "deployed",
        "validated"
      ]
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
    "model-card/ref",
    "created-at"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-adapter-id"></a>
## `adapter/id`

- Required: `yes`
- Shape: string

Stable identifier of the adapter artifact.

<a id="field-job-id"></a>
## `job/id`

- Required: `yes`
- Shape: string

TrainingJob identifier that produced the adapter.

<a id="field-base-model-ref"></a>
## `base-model/ref`

- Required: `yes`
- Shape: string

Immutable base model on top of which the adapter applies.

<a id="field-adapter-hash"></a>
## `adapter/hash`

- Required: `yes`
- Shape: string

Hash or equivalent immutable content identifier of the adapter payload.

<a id="field-eval-report-ref"></a>
## `eval-report/ref`

- Required: `yes`
- Shape: string

Reference to evaluation results that justify deployment or rejection.

<a id="field-deployment-scope"></a>
## `deployment/scope`

- Required: `yes`
- Shape: enum: `private`, `federation-local`, `public`

Intended deployment visibility of the adapter artifact.

<a id="field-rollback-ref"></a>
## `rollback/ref`

- Required: `yes`
- Shape: string

Reference to rollback path, previous adapter, or disable artifact.

<a id="field-creator-refs"></a>
## `creator/refs`

- Required: `yes`
- Shape: array

Creators or contributors that should remain attributable in downstream use.

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: enum: `validated`, `deployed`, `rejected`, `revoked`

Current artifact lifecycle status.

<a id="field-model-card-ref"></a>
## `model-card/ref`

- Required: `no`
- Shape: string

Reference to model card or equivalent manifest describing intended use and risks.

<a id="field-created-at"></a>
## `created-at`

- Required: `no`
- Shape: string

Artifact creation timestamp.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core adapter semantics.
