# Corpus Entry v1

Source schema: [`doc/schemas/corpus-entry.v1.schema.json`](../../schemas/corpus-entry.v1.schema.json)

Machine-readable schema for curated corpus entries derived from accepted bundles or promoted knowledge artifacts.

## Governing Basis

- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)
- [`doc/project/50-requirements/requirements-002.md`](../../project/50-requirements/requirements-002.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)

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
| [`entry/id`](#field-entry-id) | `yes` | string | Stable identifier of the curated corpus entry. |
| [`source/type`](#field-source-type) | `yes` | enum: `transcript-bundle`, `knowledge-artifact`, `archival-package` | Primary source class from which the corpus entry was assembled. |
| [`source/id`](#field-source-id) | `yes` | string | Identifier of the primary source artifact. |
| [`content/ref`](#field-content-ref) | `yes` | string | Stable reference to the curated content body. |
| [`domain/tags`](#field-domain-tags) | `yes` | array | Domain and topic tags assigned by curation. |
| [`quality/grade`](#field-quality-grade) | `yes` | enum: `low`, `medium`, `high` | Curation quality assessment of the entry. |
| [`risk/grade`](#field-risk-grade) | `yes` | enum: `low`, `moderate`, `high` | Risk classification relevant to later publication or training use. |
| [`training/eligibility`](#field-training-eligibility) | `yes` | enum: `blocked`, `needs-review`, `approved` | Training eligibility state assigned to the corpus entry. |
| [`provenance/manifest`](#field-provenance-manifest) | `yes` | string | Reference to provenance manifest sufficient to reconstruct source lineage. |
| [`contains-human-origin`](#field-contains-human-origin) | `no` | boolean | Whether the curated entry preserves human-originated source material. |
| [`language`](#field-language) | `no` | string | Primary language of the curated content. |
| [`creator/refs`](#field-creator-refs) | `no` | array | Curator, secretary, or contributor references that should survive attribution-sensitive flows. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core corpus-entry semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "risk/grade": {
      "const": "high"
    }
  },
  "required": [
    "risk/grade"
  ]
}
```

Then:

```json
{
  "properties": {
    "training/eligibility": {
      "enum": [
        "blocked",
        "needs-review"
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

<a id="field-entry-id"></a>
## `entry/id`

- Required: `yes`
- Shape: string

Stable identifier of the curated corpus entry.

<a id="field-source-type"></a>
## `source/type`

- Required: `yes`
- Shape: enum: `transcript-bundle`, `knowledge-artifact`, `archival-package`

Primary source class from which the corpus entry was assembled.

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

Identifier of the primary source artifact.

<a id="field-content-ref"></a>
## `content/ref`

- Required: `yes`
- Shape: string

Stable reference to the curated content body.

<a id="field-domain-tags"></a>
## `domain/tags`

- Required: `yes`
- Shape: array

Domain and topic tags assigned by curation.

<a id="field-quality-grade"></a>
## `quality/grade`

- Required: `yes`
- Shape: enum: `low`, `medium`, `high`

Curation quality assessment of the entry.

<a id="field-risk-grade"></a>
## `risk/grade`

- Required: `yes`
- Shape: enum: `low`, `moderate`, `high`

Risk classification relevant to later publication or training use.

<a id="field-training-eligibility"></a>
## `training/eligibility`

- Required: `yes`
- Shape: enum: `blocked`, `needs-review`, `approved`

Training eligibility state assigned to the corpus entry.

<a id="field-provenance-manifest"></a>
## `provenance/manifest`

- Required: `yes`
- Shape: string

Reference to provenance manifest sufficient to reconstruct source lineage.

<a id="field-contains-human-origin"></a>
## `contains-human-origin`

- Required: `no`
- Shape: boolean

Whether the curated entry preserves human-originated source material.

<a id="field-language"></a>
## `language`

- Required: `no`
- Shape: string

Primary language of the curated content.

<a id="field-creator-refs"></a>
## `creator/refs`

- Required: `no`
- Shape: array

Curator, secretary, or contributor references that should survive attribution-sensitive flows.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core corpus-entry semantics.
