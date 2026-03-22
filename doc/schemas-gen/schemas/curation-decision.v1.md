# Curation Decision v1

Source schema: [`doc/schemas/curation-decision.v1.schema.json`](../../schemas/curation-decision.v1.schema.json)

Machine-readable schema for curator decisions applied to transcript bundles or other archive-eligible source artifacts.

## Governing Basis

- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`](../../project/40-proposals/008-transcription-monitors-and-public-vaults.md)

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
| [`decision/id`](#field-decision-id) | `yes` | string | Stable identifier of the curation decision. |
| [`subject/type`](#field-subject-type) | `yes` | enum: `transcript-bundle`, `archival-package`, `knowledge-artifact` | Semantic class of the curated subject. |
| [`subject/id`](#field-subject-id) | `yes` | string | Identifier of the subject under review. |
| [`status`](#field-status) | `yes` | enum: `accepted`, `accepted-redacted`, `quarantined`, `rejected` | Result of curation review. |
| [`decided-at`](#field-decided-at) | `yes` | string | Timestamp at which the decision was taken. |
| [`curator/ref`](#field-curator-ref) | `yes` | string | Curator or policy actor responsible for the decision. |
| [`reason/codes`](#field-reason-codes) | `yes` | array | Short machine-readable reason codes that justify the decision. |
| [`redaction/status`](#field-redaction-status) | `no` | enum: `none`, `partial`, `full-derived` | Export posture approved or required by the decision. |
| [`consent/basis`](#field-consent-basis) | `no` | enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception` | Policy or consent basis that permits curation or later publication. |
| [`training/eligibility`](#field-training-eligibility) | `no` | enum: `blocked`, `needs-review`, `approved` | Training eligibility state resulting from curation. |
| [`provenance/refs`](#field-provenance-refs) | `no` | array | Supporting references used during review. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core curation semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "accepted-redacted"
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
    "redaction/status"
  ],
  "properties": {
    "redaction/status": {
      "enum": [
        "partial",
        "full-derived"
      ]
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "quarantined",
        "rejected"
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
  "properties": {
    "training/eligibility": {
      "const": "blocked"
    }
  },
  "required": [
    "training/eligibility"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-decision-id"></a>
## `decision/id`

- Required: `yes`
- Shape: string

Stable identifier of the curation decision.

<a id="field-subject-type"></a>
## `subject/type`

- Required: `yes`
- Shape: enum: `transcript-bundle`, `archival-package`, `knowledge-artifact`

Semantic class of the curated subject.

<a id="field-subject-id"></a>
## `subject/id`

- Required: `yes`
- Shape: string

Identifier of the subject under review.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `accepted-redacted`, `quarantined`, `rejected`

Result of curation review.

<a id="field-decided-at"></a>
## `decided-at`

- Required: `yes`
- Shape: string

Timestamp at which the decision was taken.

<a id="field-curator-ref"></a>
## `curator/ref`

- Required: `yes`
- Shape: string

Curator or policy actor responsible for the decision.

<a id="field-reason-codes"></a>
## `reason/codes`

- Required: `yes`
- Shape: array

Short machine-readable reason codes that justify the decision.

<a id="field-redaction-status"></a>
## `redaction/status`

- Required: `no`
- Shape: enum: `none`, `partial`, `full-derived`

Export posture approved or required by the decision.

<a id="field-consent-basis"></a>
## `consent/basis`

- Required: `no`
- Shape: enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception`

Policy or consent basis that permits curation or later publication.

<a id="field-training-eligibility"></a>
## `training/eligibility`

- Required: `no`
- Shape: enum: `blocked`, `needs-review`, `approved`

Training eligibility state resulting from curation.

<a id="field-provenance-refs"></a>
## `provenance/refs`

- Required: `no`
- Shape: array

Supporting references used during review.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core curation semantics.
