# Signal Marker v1

Source schema: [`doc/schemas/signal-marker.v1.schema.json`](../../schemas/signal-marker.v1.schema.json)

Machine-readable schema for visible signal markers that disclose whether a user-facing artifact preserves raw signal or presents a transformed variant.

## Governing Basis

- [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](../../normative/40-constitution/pl/CONSTITUTION.pl.md)
- [`doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md`](../../normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`marker_id`](#field-marker-id) | `yes` | string | Stable identifier of this visible signal marker. |
| [`applies_to_ref`](#field-applies-to-ref) | `yes` | string | Stable reference to the message, segment, bundle, or other artifact annotated by this marker. |
| [`mode`](#field-mode) | `yes` | enum: `raw`, `structured`, `transformed`, `redacted` | User-visible signal mode presented at the interface boundary. |
| [`actor`](#field-actor) | `yes` | enum: `ai`, `human`, `hybrid` | Who materially shaped the visible output variant. |
| [`requested_by`](#field-requested-by) | `no` | enum: `user`, `user_policy`, `safety_policy`, `exception` |  |
| [`basis_ref`](#field-basis-ref) | `no` | string | Reference to the prompt, policy, rule, exception, or other basis authorizing the visible signal mode. |
| [`operations`](#field-operations) | `no` | array |  |
| [`visible_to_user`](#field-visible-to-user) | `yes` | boolean | Whether the marker is intentionally surfaced in the same interface as the annotated artifact. |
| [`transform_ref`](#field-transform-ref) | `no` | string | Optional reference to a SignalTransformEvent that explains how the output variant was produced. |
| [`created_at`](#field-created-at) | `no` | string |  |
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
    "mode": {
      "const": "raw"
    }
  },
  "required": [
    "mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "operations": {
      "maxItems": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "mode": {
      "enum": [
        "structured",
        "transformed",
        "redacted"
      ]
    }
  },
  "required": [
    "mode"
  ]
}
```

Then:

```json
{
  "required": [
    "requested_by",
    "basis_ref",
    "operations"
  ],
  "properties": {
    "operations": {
      "minItems": 1
    },
    "visible_to_user": {
      "const": true
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

<a id="field-marker-id"></a>
## `marker_id`

- Required: `yes`
- Shape: string

Stable identifier of this visible signal marker.

<a id="field-applies-to-ref"></a>
## `applies_to_ref`

- Required: `yes`
- Shape: string

Stable reference to the message, segment, bundle, or other artifact annotated by this marker.

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `raw`, `structured`, `transformed`, `redacted`

User-visible signal mode presented at the interface boundary.

<a id="field-actor"></a>
## `actor`

- Required: `yes`
- Shape: enum: `ai`, `human`, `hybrid`

Who materially shaped the visible output variant.

<a id="field-requested-by"></a>
## `requested_by`

- Required: `no`
- Shape: enum: `user`, `user_policy`, `safety_policy`, `exception`

<a id="field-basis-ref"></a>
## `basis_ref`

- Required: `no`
- Shape: string

Reference to the prompt, policy, rule, exception, or other basis authorizing the visible signal mode.

<a id="field-operations"></a>
## `operations`

- Required: `no`
- Shape: array

<a id="field-visible-to-user"></a>
## `visible_to_user`

- Required: `yes`
- Shape: boolean

Whether the marker is intentionally surfaced in the same interface as the annotated artifact.

<a id="field-transform-ref"></a>
## `transform_ref`

- Required: `no`
- Shape: string

Optional reference to a SignalTransformEvent that explains how the output variant was produced.

<a id="field-created-at"></a>
## `created_at`

- Required: `no`
- Shape: string

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-operation"></a>
## `$defs.operation`

- Shape: enum: `structure_extraction`, `summarization`, `translation`, `tone_shift`, `formality_shift`, `style_polish`, `safety_redaction`, `privacy_redaction`
