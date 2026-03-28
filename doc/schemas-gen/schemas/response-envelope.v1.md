# Response Envelope v1

Source schema: [`doc/schemas/response-envelope.v1.schema.json`](../../schemas/response-envelope.v1.schema.json)

Machine-readable schema for the final answer returned from swarm procurement or collaborative answer flow. This artifact remains participant-scoped in v1 and does not define a nym-authored alternative path.

## Governing Basis

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`](../../project/40-proposals/004-human-origin-flags-and-operator-participation.md)
- [`doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`](../../project/40-proposals/008-transcription-monitors-and-public-vaults.md)
- [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`response/id`](#field-response-id) | `yes` | string | Stable identifier of the returned response boundary object. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier from which the response originated. |
| [`room/id`](#field-room-id) | `no` | string | Room or execution path that produced the final answer or accepted summary. |
| [`contract/id`](#field-contract-id) | `no` | string | Linked procurement contract when payment or narrowed execution applied. |
| [`receipt/id`](#field-receipt-id) | `no` | string | Linked procurement receipt when settlement or explicit rejection was recorded. |
| [`accepted-summary/id`](#field-accepted-summary-id) | `no` | string | Accepted summary identifier when the final answer is derived from room convergence. |
| [`created-at`](#field-created-at) | `yes` | string | Response publication timestamp. |
| [`source/node-id`](#field-source-node-id) | `yes` | string | Primary remote responder or gateway node at the protocol boundary. This is the routing or hosting identity, not the authored participation identity. |
| [`source/participant-id`](#field-source-participant-id) | `yes` | string | Participation-role identity that authored, endorsed, or stood behind the returned answer payload. In v1 this remains the accountable authored identity rather than being replaced by a pseudonymous nym path. |
| [`gateway/node-id`](#field-gateway-node-id) | `no` | string | Gateway node when the result was delivered through a delegated host or other relay role. |
| [`answer/content`](#field-answer-content) | `yes` | unspecified | Returned answer payload in textual or structured form. |
| [`answer/format`](#field-answer-format) | `yes` | enum: `plain-text`, `markdown`, `json`, `edn`, `mixed` | Representation format of the returned answer payload. |
| [`confidence/signal`](#field-confidence-signal) | `yes` | number | Composite confidence signal shown to the consumer of the response. |
| [`uncertainty/signal`](#field-uncertainty-signal) | `no` | number | Optional uncertainty signal paired with or derived from confidence. |
| [`human-linked-participation`](#field-human-linked-participation) | `yes` | boolean | Whether human-linked input materially influenced the final result. |
| [`provenance/origin-classes`](#field-provenance-origin-classes) | `yes` | array | Origin classes materially present in the answer path. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "contract/id"
  ]
}
```

Then:

```json
{
  "required": [
    "receipt/id"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "human-linked-participation": {
      "const": true
    }
  },
  "required": [
    "human-linked-participation"
  ]
}
```

Then:

```json
{
  "properties": {
    "provenance/origin-classes": {
      "contains": {
        "enum": [
          "node-mediated-human",
          "human-live"
        ]
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "human-linked-participation": {
      "const": false
    }
  },
  "required": [
    "human-linked-participation"
  ]
}
```

Then:

```json
{
  "properties": {
    "provenance/origin-classes": {
      "items": {
        "const": "node-generated"
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

<a id="field-response-id"></a>
## `response/id`

- Required: `yes`
- Shape: string

Stable identifier of the returned response boundary object.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier from which the response originated.

<a id="field-room-id"></a>
## `room/id`

- Required: `no`
- Shape: string

Room or execution path that produced the final answer or accepted summary.

<a id="field-contract-id"></a>
## `contract/id`

- Required: `no`
- Shape: string

Linked procurement contract when payment or narrowed execution applied.

<a id="field-receipt-id"></a>
## `receipt/id`

- Required: `no`
- Shape: string

Linked procurement receipt when settlement or explicit rejection was recorded.

<a id="field-accepted-summary-id"></a>
## `accepted-summary/id`

- Required: `no`
- Shape: string

Accepted summary identifier when the final answer is derived from room convergence.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Response publication timestamp.

<a id="field-source-node-id"></a>
## `source/node-id`

- Required: `yes`
- Shape: string

Primary remote responder or gateway node at the protocol boundary. This is the routing or hosting identity, not the authored participation identity.

<a id="field-source-participant-id"></a>
## `source/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity that authored, endorsed, or stood behind the returned answer payload. In v1 this remains the accountable authored identity rather than being replaced by a pseudonymous nym path.

<a id="field-gateway-node-id"></a>
## `gateway/node-id`

- Required: `no`
- Shape: string

Gateway node when the result was delivered through a delegated host or other relay role.

<a id="field-answer-content"></a>
## `answer/content`

- Required: `yes`
- Shape: unspecified

Returned answer payload in textual or structured form.

<a id="field-answer-format"></a>
## `answer/format`

- Required: `yes`
- Shape: enum: `plain-text`, `markdown`, `json`, `edn`, `mixed`

Representation format of the returned answer payload.

<a id="field-confidence-signal"></a>
## `confidence/signal`

- Required: `yes`
- Shape: number

Composite confidence signal shown to the consumer of the response.

<a id="field-uncertainty-signal"></a>
## `uncertainty/signal`

- Required: `no`
- Shape: number

Optional uncertainty signal paired with or derived from confidence.

<a id="field-human-linked-participation"></a>
## `human-linked-participation`

- Required: `yes`
- Shape: boolean

Whether human-linked input materially influenced the final result.

<a id="field-provenance-origin-classes"></a>
## `provenance/origin-classes`

- Required: `yes`
- Shape: array

Origin classes materially present in the answer path.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
