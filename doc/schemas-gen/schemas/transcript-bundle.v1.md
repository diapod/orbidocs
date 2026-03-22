# TranscriptBundle v1

Source schema: [`doc/schemas/transcript-bundle.v1.schema.json`](../../schemas/transcript-bundle.v1.schema.json)

Machine-readable schema for transcript bundles that preserve archival scope, integrity, and human-origin aggregate flags.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`bundle_id`](#field-bundle-id) | `yes` | string |  |
| [`question_id`](#field-question-id) | `yes` | string |  |
| [`channel_id`](#field-channel-id) | `yes` | string |  |
| [`source_scope`](#field-source-scope) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`created_at`](#field-created-at) | `yes` | string |  |
| [`source_nodes`](#field-source-nodes) | `yes` | array |  |
| [`segments`](#field-segments) | `yes` | array |  |
| [`contains_human_origin`](#field-contains-human-origin) | `yes` | boolean |  |
| [`contains_direct_human_live`](#field-contains-direct-human-live) | `yes` | boolean |  |
| [`consent_basis`](#field-consent-basis) | `yes` | enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception` | Archival/publication basis for the bundle as a whole. |
| [`redaction_status`](#field-redaction-status) | `yes` | enum: `none`, `partial`, `full-derived` |  |
| [`integrity_proof`](#field-integrity-proof) | `yes` | ref: `#/$defs/integrityProof` |  |
| [`room_policy_profile`](#field-room-policy-profile) | `no` | enum: `none`, `mediated-only`, `direct-live-allowed` |  |
| [`summary_refs`](#field-summary-refs) | `no` | array |  |
| [`source_transport`](#field-source-transport) | `no` | string |  |
| [`retention_profile`](#field-retention-profile) | `no` | string |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`transcriptSegmentRef`](#def-transcriptsegmentref) | object |  |
| [`integrityProof`](#def-integrityproof) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "contains_direct_human_live": {
      "const": true
    }
  },
  "required": [
    "contains_direct_human_live"
  ]
}
```

Then:

```json
{
  "properties": {
    "contains_human_origin": {
      "const": true
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "room_policy_profile": {
      "const": "none"
    }
  },
  "required": [
    "room_policy_profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "contains_human_origin": {
      "const": false
    },
    "contains_direct_human_live": {
      "const": false
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

<a id="field-bundle-id"></a>
## `bundle_id`

- Required: `yes`
- Shape: string

<a id="field-question-id"></a>
## `question_id`

- Required: `yes`
- Shape: string

<a id="field-channel-id"></a>
## `channel_id`

- Required: `yes`
- Shape: string

<a id="field-source-scope"></a>
## `source_scope`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-created-at"></a>
## `created_at`

- Required: `yes`
- Shape: string

<a id="field-source-nodes"></a>
## `source_nodes`

- Required: `yes`
- Shape: array

<a id="field-segments"></a>
## `segments`

- Required: `yes`
- Shape: array

<a id="field-contains-human-origin"></a>
## `contains_human_origin`

- Required: `yes`
- Shape: boolean

<a id="field-contains-direct-human-live"></a>
## `contains_direct_human_live`

- Required: `yes`
- Shape: boolean

<a id="field-consent-basis"></a>
## `consent_basis`

- Required: `yes`
- Shape: enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception`

Archival/publication basis for the bundle as a whole.

<a id="field-redaction-status"></a>
## `redaction_status`

- Required: `yes`
- Shape: enum: `none`, `partial`, `full-derived`

<a id="field-integrity-proof"></a>
## `integrity_proof`

- Required: `yes`
- Shape: ref: `#/$defs/integrityProof`

<a id="field-room-policy-profile"></a>
## `room_policy_profile`

- Required: `no`
- Shape: enum: `none`, `mediated-only`, `direct-live-allowed`

<a id="field-summary-refs"></a>
## `summary_refs`

- Required: `no`
- Shape: array

<a id="field-source-transport"></a>
## `source_transport`

- Required: `no`
- Shape: string

<a id="field-retention-profile"></a>
## `retention_profile`

- Required: `no`
- Shape: string

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-transcriptsegmentref"></a>
## `$defs.transcriptSegmentRef`

- Shape: object

<a id="def-integrityproof"></a>
## `$defs.integrityProof`

- Shape: object
