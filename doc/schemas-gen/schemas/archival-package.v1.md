# Archival Package v1

Source schema: [`doc/schemas/archival-package.v1.schema.json`](../../schemas/archival-package.v1.schema.json)

Machine-readable schema for packaging durable artifacts for archivist or vault handoff.

## Governing Basis

- [`doc/project/30-stories/story-003.md`](../../project/30-stories/story-003.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`](../../project/40-proposals/008-transcription-monitors-and-public-vaults.md)
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
| [`package/id`](#field-package-id) | `yes` | string | Stable package identifier used at archival handoff boundaries. |
| [`artifact/id`](#field-artifact-id) | `yes` | string | Identifier of the packaged artifact. |
| [`artifact/type`](#field-artifact-type) | `yes` | enum: `transcript-bundle`, `room-summary`, `response-envelope`, `knowledge-artifact`, `corpus-entry` | Primary semantic class of the packaged artifact. |
| [`source/question-id`](#field-source-question-id) | `yes` | string | Question lifecycle identifier that roots the packaged artifact. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp of archival package creation. |
| [`publication/scope`](#field-publication-scope) | `yes` | enum: `private-retained`, `federation-vault`, `public-vault` | Declared publication class of the archival handoff. |
| [`archival/basis`](#field-archival-basis) | `yes` | enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception` | Policy or consent basis for archival export. |
| [`redaction/status`](#field-redaction-status) | `yes` | enum: `none`, `partial`, `full-derived` | Redaction posture of the exported artifact. |
| [`payload/ref`](#field-payload-ref) | `yes` | string | Stable content, blob, or manifest reference for the packaged payload. |
| [`provenance/refs`](#field-provenance-refs) | `yes` | array | Trace references that bind the package to its source discussion or promotion history. |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` | Classification label preserved across archival/export boundaries. Export adapters MAY normalize `effective_tier` for the current export surface, but MUST preserve `source_tier`, `provenance`, and `declassify_trail` without rewriting them. |
| [`publication/timing-profile`](#field-publication-timing-profile) | `no` | enum: `live-mirror`, `delayed-bundle`, `curator-gated` | Timing profile for publication beyond storage success. |
| [`retention/max-duration-sec`](#field-retention-max-duration-sec) | `no` | integer | Maximum intended storage duration in seconds when retention is bounded. |
| [`retention/max-idle-ttl-sec`](#field-retention-max-idle-ttl-sec) | `no` | integer | Maximum idle time without retrieval before the package may expire. |
| [`integrity/proof`](#field-integrity-proof) | `yes` | ref: `#/$defs/integrityProof` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core archival semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`integrityProof`](#def-integrityproof) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "publication/scope": {
      "const": "public-vault"
    }
  },
  "required": [
    "publication/scope"
  ]
}
```

Then:

```json
{
  "required": [
    "publication/timing-profile"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-package-id"></a>
## `package/id`

- Required: `yes`
- Shape: string

Stable package identifier used at archival handoff boundaries.

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `yes`
- Shape: string

Identifier of the packaged artifact.

<a id="field-artifact-type"></a>
## `artifact/type`

- Required: `yes`
- Shape: enum: `transcript-bundle`, `room-summary`, `response-envelope`, `knowledge-artifact`, `corpus-entry`

Primary semantic class of the packaged artifact.

<a id="field-source-question-id"></a>
## `source/question-id`

- Required: `yes`
- Shape: string

Question lifecycle identifier that roots the packaged artifact.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp of archival package creation.

<a id="field-publication-scope"></a>
## `publication/scope`

- Required: `yes`
- Shape: enum: `private-retained`, `federation-vault`, `public-vault`

Declared publication class of the archival handoff.

<a id="field-archival-basis"></a>
## `archival/basis`

- Required: `yes`
- Shape: enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception`

Policy or consent basis for archival export.

<a id="field-redaction-status"></a>
## `redaction/status`

- Required: `yes`
- Shape: enum: `none`, `partial`, `full-derived`

Redaction posture of the exported artifact.

<a id="field-payload-ref"></a>
## `payload/ref`

- Required: `yes`
- Shape: string

Stable content, blob, or manifest reference for the packaged payload.

<a id="field-provenance-refs"></a>
## `provenance/refs`

- Required: `yes`
- Shape: array

Trace references that bind the package to its source discussion or promotion history.

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

Classification label preserved across archival/export boundaries. Export adapters MAY normalize `effective_tier` for the current export surface, but MUST preserve `source_tier`, `provenance`, and `declassify_trail` without rewriting them.

<a id="field-publication-timing-profile"></a>
## `publication/timing-profile`

- Required: `no`
- Shape: enum: `live-mirror`, `delayed-bundle`, `curator-gated`

Timing profile for publication beyond storage success.

<a id="field-retention-max-duration-sec"></a>
## `retention/max-duration-sec`

- Required: `no`
- Shape: integer

Maximum intended storage duration in seconds when retention is bounded.

<a id="field-retention-max-idle-ttl-sec"></a>
## `retention/max-idle-ttl-sec`

- Required: `no`
- Shape: integer

Maximum idle time without retrieval before the package may expire.

<a id="field-integrity-proof"></a>
## `integrity/proof`

- Required: `yes`
- Shape: ref: `#/$defs/integrityProof`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core archival semantics.

## Definition Semantics

<a id="def-integrityproof"></a>
## `$defs.integrityProof`

- Shape: object
