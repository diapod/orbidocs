# Eval Report v1

Source schema: [`doc/schemas/eval-report.v1.schema.json`](../../schemas/eval-report.v1.schema.json)

Machine-readable schema for adapter evaluation outputs that gate validation, deployment, or rejection.

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
| [`eval-report/id`](#field-eval-report-id) | `yes` | string | Stable identifier of the evaluation report. |
| [`subject/kind`](#field-subject-kind) | `yes` | enum: `training-job`, `adapter-artifact` | Evaluated subject class. |
| [`subject/ref`](#field-subject-ref) | `yes` | string | Reference to the evaluated job or adapter. |
| [`base-model/ref`](#field-base-model-ref) | `yes` | string | Immutable base model against which the evaluated artifact must remain interpretable. |
| [`adapter/hash`](#field-adapter-hash) | `no` | string | Immutable adapter hash when the evaluated subject is an adapter artifact. |
| [`generated-at`](#field-generated-at) | `yes` | string | Evaluation completion timestamp. |
| [`verdict`](#field-verdict) | `yes` | enum: `pass`, `conditional-pass`, `fail` | High-level evaluation verdict. |
| [`summary`](#field-summary) | `yes` | string | Human-readable summary of the evaluation outcome. |
| [`evaluator/refs`](#field-evaluator-refs) | `yes` | array | People, nodes, or policy engines that produced or signed the report. |
| [`policy/profile`](#field-policy-profile) | `no` | string | Evaluation policy profile used for this report. |
| [`known-issues`](#field-known-issues) | `no` | array | Residual issues kept visible even when the verdict is not a hard fail. |
| [`suites`](#field-suites) | `yes` | array | Evaluation suites covering quality, regression, and risk gates. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core evaluation semantics. |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "properties": {
    "suites": {
      "contains": {
        "type": "object",
        "properties": {
          "suite/class": {
            "const": "quality"
          }
        },
        "required": [
          "suite/class"
        ]
      }
    }
  }
}
```

### Rule 2

Constraint:

```json
{
  "properties": {
    "suites": {
      "contains": {
        "type": "object",
        "properties": {
          "suite/class": {
            "const": "regression"
          }
        },
        "required": [
          "suite/class"
        ]
      }
    }
  }
}
```

### Rule 3

Constraint:

```json
{
  "properties": {
    "suites": {
      "contains": {
        "type": "object",
        "properties": {
          "suite/class": {
            "const": "risk"
          }
        },
        "required": [
          "suite/class"
        ]
      }
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "subject/kind": {
      "const": "adapter-artifact"
    }
  },
  "required": [
    "subject/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "adapter/hash"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-eval-report-id"></a>
## `eval-report/id`

- Required: `yes`
- Shape: string

Stable identifier of the evaluation report.

<a id="field-subject-kind"></a>
## `subject/kind`

- Required: `yes`
- Shape: enum: `training-job`, `adapter-artifact`

Evaluated subject class.

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: string

Reference to the evaluated job or adapter.

<a id="field-base-model-ref"></a>
## `base-model/ref`

- Required: `yes`
- Shape: string

Immutable base model against which the evaluated artifact must remain interpretable.

<a id="field-adapter-hash"></a>
## `adapter/hash`

- Required: `no`
- Shape: string

Immutable adapter hash when the evaluated subject is an adapter artifact.

<a id="field-generated-at"></a>
## `generated-at`

- Required: `yes`
- Shape: string

Evaluation completion timestamp.

<a id="field-verdict"></a>
## `verdict`

- Required: `yes`
- Shape: enum: `pass`, `conditional-pass`, `fail`

High-level evaluation verdict.

<a id="field-summary"></a>
## `summary`

- Required: `yes`
- Shape: string

Human-readable summary of the evaluation outcome.

<a id="field-evaluator-refs"></a>
## `evaluator/refs`

- Required: `yes`
- Shape: array

People, nodes, or policy engines that produced or signed the report.

<a id="field-policy-profile"></a>
## `policy/profile`

- Required: `no`
- Shape: string

Evaluation policy profile used for this report.

<a id="field-known-issues"></a>
## `known-issues`

- Required: `no`
- Shape: array

Residual issues kept visible even when the verdict is not a hard fail.

<a id="field-suites"></a>
## `suites`

- Required: `yes`
- Shape: array

Evaluation suites covering quality, regression, and risk gates.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core evaluation semantics.
