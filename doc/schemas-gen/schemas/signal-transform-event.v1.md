# SignalTransformEvent v1

Source schema: [`doc/schemas/signal-transform-event.v1.schema.json`](../../schemas/signal-transform-event.v1.schema.json)

Machine-readable schema for auditable records of transformations applied to user signal when the output is no longer raw.

## Governing Basis

- [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](../../normative/40-constitution/pl/CONSTITUTION.pl.md)
- [`doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md`](../../normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`transform_id`](#field-transform-id) | `yes` | string | Stable identifier of this transformation event. |
| [`source_ref`](#field-source-ref) | `yes` | string | Stable reference to the source message, segment, or artifact before transformation. |
| [`output_ref`](#field-output-ref) | `no` | string | Optional reference to the produced artifact after transformation. |
| [`marker_ref`](#field-marker-ref) | `no` | string | Optional reference to the visible SignalMarker attached to the output. |
| [`input_mode`](#field-input-mode) | `yes` | enum: `raw`, `structured`, `transformed`, `redacted` | Signal mode of the source artifact before the transformation step. |
| [`output_mode`](#field-output-mode) | `yes` | enum: `structured`, `transformed`, `redacted` | Signal mode of the produced artifact after the transformation step. |
| [`actor_type`](#field-actor-type) | `yes` | enum: `ai`, `human`, `hybrid` | Who materially performed the transformation. |
| [`requested_by`](#field-requested-by) | `yes` | enum: `user`, `user_policy`, `safety_policy`, `exception` |  |
| [`basis_ref`](#field-basis-ref) | `yes` | string | Reference to the prompt, policy, rule, exception, or other basis authorizing the transformation. |
| [`operations`](#field-operations) | `yes` | array |  |
| [`created_at`](#field-created-at) | `yes` | string |  |
| [`visibility_scope`](#field-visibility-scope) | `no` | enum: `user-visible`, `same-interface`, `audit-only` | How the fact of transformation is surfaced relative to the transformed artifact. |
| [`content_disclosure`](#field-content-disclosure) | `no` | enum: `full`, `partial`, `metadata-only` | How much of the transformed content is available to a given audit path. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`operation`](#def-operation) | enum: `structure_extraction`, `summarization`, `translation`, `tone_shift`, `formality_shift`, `style_polish`, `safety_redaction`, `privacy_redaction` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "output_mode": {
      "const": "redacted"
    }
  },
  "required": [
    "output_mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "operations": {
      "contains": {
        "enum": [
          "safety_redaction",
          "privacy_redaction"
        ]
      }
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

<a id="field-transform-id"></a>
## `transform_id`

- Required: `yes`
- Shape: string

Stable identifier of this transformation event.

<a id="field-source-ref"></a>
## `source_ref`

- Required: `yes`
- Shape: string

Stable reference to the source message, segment, or artifact before transformation.

<a id="field-output-ref"></a>
## `output_ref`

- Required: `no`
- Shape: string

Optional reference to the produced artifact after transformation.

<a id="field-marker-ref"></a>
## `marker_ref`

- Required: `no`
- Shape: string

Optional reference to the visible SignalMarker attached to the output.

<a id="field-input-mode"></a>
## `input_mode`

- Required: `yes`
- Shape: enum: `raw`, `structured`, `transformed`, `redacted`

Signal mode of the source artifact before the transformation step.

<a id="field-output-mode"></a>
## `output_mode`

- Required: `yes`
- Shape: enum: `structured`, `transformed`, `redacted`

Signal mode of the produced artifact after the transformation step.

<a id="field-actor-type"></a>
## `actor_type`

- Required: `yes`
- Shape: enum: `ai`, `human`, `hybrid`

Who materially performed the transformation.

<a id="field-requested-by"></a>
## `requested_by`

- Required: `yes`
- Shape: enum: `user`, `user_policy`, `safety_policy`, `exception`

<a id="field-basis-ref"></a>
## `basis_ref`

- Required: `yes`
- Shape: string

Reference to the prompt, policy, rule, exception, or other basis authorizing the transformation.

<a id="field-operations"></a>
## `operations`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created_at`

- Required: `yes`
- Shape: string

<a id="field-visibility-scope"></a>
## `visibility_scope`

- Required: `no`
- Shape: enum: `user-visible`, `same-interface`, `audit-only`

How the fact of transformation is surfaced relative to the transformed artifact.

<a id="field-content-disclosure"></a>
## `content_disclosure`

- Required: `no`
- Shape: enum: `full`, `partial`, `metadata-only`

How much of the transformed content is available to a given audit path.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-operation"></a>
## `$defs.operation`

- Shape: enum: `structure_extraction`, `summarization`, `translation`, `tone_shift`, `formality_shift`, `style_polish`, `safety_redaction`, `privacy_redaction`
