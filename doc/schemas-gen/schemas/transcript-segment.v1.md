# Transcript Segment v1

Source schema: [`doc/schemas/transcript-segment.v1.schema.json`](../../schemas/transcript-segment.v1.schema.json)

Machine-readable schema for transcript segments that preserve room/message provenance and human-origin semantics.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`segment_id`](#field-segment-id) | `yes` | string |  |
| [`question_id`](#field-question-id) | `yes` | string |  |
| [`channel_id`](#field-channel-id) | `yes` | string |  |
| [`message_id`](#field-message-id) | `yes` | string |  |
| [`speaker_ref`](#field-speaker-ref) | `yes` | string | Semantic speaker at the room boundary. |
| [`gateway_node_ref`](#field-gateway-node-ref) | `yes` | string | Node that injected the message into the room or relay path. |
| [`origin_class`](#field-origin-class) | `yes` | enum: `node-generated`, `node-mediated-human`, `human-live` |  |
| [`operator_presence_mode`](#field-operator-presence-mode) | `yes` | enum: `none`, `mediated`, `direct-live` |  |
| [`human_origin`](#field-human-origin) | `yes` | boolean |  |
| [`ts`](#field-ts) | `yes` | string | ISO-8601 UTC timestamp. |
| [`content`](#field-content) | `yes` | unspecified | Either plain text or a structured content object. Structured objects should expose a stable textual projection. |
| [`visibility_scope`](#field-visibility-scope) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`consent_basis`](#field-consent-basis) | `yes` | enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception` |  |
| [`provenance_refs`](#field-provenance-refs) | `yes` | array |  |
| [`redaction_markers`](#field-redaction-markers) | `no` | array | Describes removals or transformations rather than silently rewriting content history. |
| [`content_hash`](#field-content-hash) | `no` | string |  |
| [`language`](#field-language) | `no` | string |  |
| [`reply_to`](#field-reply-to) | `no` | string |  |
| [`attachments`](#field-attachments) | `no` | array |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "origin_class": {
      "const": "node-generated"
    }
  },
  "required": [
    "origin_class"
  ]
}
```

Then:

```json
{
  "properties": {
    "human_origin": {
      "const": false
    },
    "operator_presence_mode": {
      "const": "none"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "origin_class": {
      "const": "node-mediated-human"
    }
  },
  "required": [
    "origin_class"
  ]
}
```

Then:

```json
{
  "properties": {
    "human_origin": {
      "const": true
    },
    "operator_presence_mode": {
      "const": "mediated"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "origin_class": {
      "const": "human-live"
    }
  },
  "required": [
    "origin_class"
  ]
}
```

Then:

```json
{
  "properties": {
    "human_origin": {
      "const": true
    },
    "operator_presence_mode": {
      "const": "direct-live"
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

<a id="field-segment-id"></a>
## `segment_id`

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

<a id="field-message-id"></a>
## `message_id`

- Required: `yes`
- Shape: string

<a id="field-speaker-ref"></a>
## `speaker_ref`

- Required: `yes`
- Shape: string

Semantic speaker at the room boundary.

<a id="field-gateway-node-ref"></a>
## `gateway_node_ref`

- Required: `yes`
- Shape: string

Node that injected the message into the room or relay path.

<a id="field-origin-class"></a>
## `origin_class`

- Required: `yes`
- Shape: enum: `node-generated`, `node-mediated-human`, `human-live`

<a id="field-operator-presence-mode"></a>
## `operator_presence_mode`

- Required: `yes`
- Shape: enum: `none`, `mediated`, `direct-live`

<a id="field-human-origin"></a>
## `human_origin`

- Required: `yes`
- Shape: boolean

<a id="field-ts"></a>
## `ts`

- Required: `yes`
- Shape: string

ISO-8601 UTC timestamp.

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: unspecified

Either plain text or a structured content object. Structured objects should expose a stable textual projection.

<a id="field-visibility-scope"></a>
## `visibility_scope`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-consent-basis"></a>
## `consent_basis`

- Required: `yes`
- Shape: enum: `not-required`, `operator-consultation`, `explicit-consent`, `federation-policy`, `public-scope`, `emergency-exception`

<a id="field-provenance-refs"></a>
## `provenance_refs`

- Required: `yes`
- Shape: array

<a id="field-redaction-markers"></a>
## `redaction_markers`

- Required: `no`
- Shape: array

Describes removals or transformations rather than silently rewriting content history.

<a id="field-content-hash"></a>
## `content_hash`

- Required: `no`
- Shape: string

<a id="field-language"></a>
## `language`

- Required: `no`
- Shape: string

<a id="field-reply-to"></a>
## `reply_to`

- Required: `no`
- Shape: string

<a id="field-attachments"></a>
## `attachments`

- Required: `no`
- Shape: array

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
