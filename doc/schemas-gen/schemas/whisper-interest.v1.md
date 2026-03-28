# Whisper Interest v1

Source schema: [`doc/schemas/whisper-interest.v1.schema.json`](../../schemas/whisper-interest.v1.schema.json)

Machine-readable schema for bounded local-interest registration in response to a whisper signal.

## Governing Basis

- [`doc/project/20-memos/orbiplex-whisper.md`](../../project/20-memos/orbiplex-whisper.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`interest/id`](#field-interest-id) | `yes` | string | Stable identifier of the local interest registration. |
| [`signal/id`](#field-signal-id) | `yes` | string | Whisper signal that triggered local interest. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp of interest registration. |
| [`interested/node-id`](#field-interested-node-id) | `yes` | string | Node registering local relevance. |
| [`interest/kind`](#field-interest-kind) | `yes` | enum: `local-relevance`, `correlation-willing`, `bootstrap-willing` | Level of willingness to participate in further correlation. |
| [`disclosure/readiness`](#field-disclosure-readiness) | `yes` | enum: `none`, `conditional`, `room-only` | Maximum disclosure willingness at the current stage. |
| [`local/user-notified`](#field-local-user-notified) | `yes` | boolean | Whether the local user or operator has already been notified of the relevant rumor. |
| [`matching/facets`](#field-matching-facets) | `no` | array | Optional local facets that justify relevance without forcing case disclosure. |
| [`trust/tier`](#field-trust-tier) | `no` | enum: `unknown`, `member`, `validated`, `high-trust` | Trust tier visible at thresholding time. |
| [`expires-at`](#field-expires-at) | `no` | string | Optional expiry after which this interest should no longer be counted. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "interest/kind": {
      "const": "bootstrap-willing"
    }
  },
  "required": [
    "interest/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "disclosure/readiness": {
      "enum": [
        "conditional",
        "room-only"
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

<a id="field-interest-id"></a>
## `interest/id`

- Required: `yes`
- Shape: string

Stable identifier of the local interest registration.

<a id="field-signal-id"></a>
## `signal/id`

- Required: `yes`
- Shape: string

Whisper signal that triggered local interest.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp of interest registration.

<a id="field-interested-node-id"></a>
## `interested/node-id`

- Required: `yes`
- Shape: string

Node registering local relevance.

<a id="field-interest-kind"></a>
## `interest/kind`

- Required: `yes`
- Shape: enum: `local-relevance`, `correlation-willing`, `bootstrap-willing`

Level of willingness to participate in further correlation.

<a id="field-disclosure-readiness"></a>
## `disclosure/readiness`

- Required: `yes`
- Shape: enum: `none`, `conditional`, `room-only`

Maximum disclosure willingness at the current stage.

<a id="field-local-user-notified"></a>
## `local/user-notified`

- Required: `yes`
- Shape: boolean

Whether the local user or operator has already been notified of the relevant rumor.

<a id="field-matching-facets"></a>
## `matching/facets`

- Required: `no`
- Shape: array

Optional local facets that justify relevance without forcing case disclosure.

<a id="field-trust-tier"></a>
## `trust/tier`

- Required: `no`
- Shape: enum: `unknown`, `member`, `validated`, `high-trust`

Trust tier visible at thresholding time.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

Optional expiry after which this interest should no longer be counted.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
