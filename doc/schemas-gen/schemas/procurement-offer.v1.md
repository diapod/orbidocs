# Procurement Offer v1

Source schema: [`doc/schemas/procurement-offer.v1.schema.json`](../../schemas/procurement-offer.v1.schema.json)

Machine-readable schema for responder offers attached to a published procurement-capable question.

## Governing Basis

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)
- [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`offer/id`](#field-offer-id) | `yes` | string | Stable identifier of the offer instance. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier to which the offer responds. |
| [`created-at`](#field-created-at) | `yes` | string | Offer creation timestamp. |
| [`expires-at`](#field-expires-at) | `no` | string | Optional offer-expiry timestamp before which the asker must decide. |
| [`responder/node-id`](#field-responder-node-id) | `yes` | string | Responding node that would host, route, or execute the answer path. |
| [`responder/participant-id`](#field-responder-participant-id) | `yes` | string | Participation-role identity that stands behind the offer and would own the responder-side participation semantics. |
| [`responder/federation-id`](#field-responder-federation-id) | `no` | string | Federation identity of the responder when relevant to routing or trust. |
| [`responder/public-key-ref`](#field-responder-public-key-ref) | `no` | string | Reference to the responder's encryption or signature key material. |
| [`price/amount`](#field-price-amount) | `yes` | integer | Proposed price in minor units. When `price/currency = ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`price/currency`](#field-price-currency) | `yes` | string | Currency or settlement unit symbol for the proposed price. |
| [`deadline-at`](#field-deadline-at) | `yes` | string | Latest timestamp by which the responder expects to deliver or conclude. |
| [`answer/min-length`](#field-answer-min-length) | `yes` | integer | Lower answer-length bound the responder is willing to contract against. |
| [`answer/max-length`](#field-answer-max-length) | `yes` | integer | Upper answer-length bound the responder is willing to contract against. |
| [`answer/format`](#field-answer-format) | `no` | enum: `plain-text`, `markdown`, `json`, `edn`, `mixed` | Preferred answer representation. |
| [`execution/mode`](#field-execution-mode) | `yes` | enum: `room-collaboration`, `single-responder` | Whether the responder expects collaborative discussion or a narrowed single-responder path. |
| [`specialization/tags`](#field-specialization-tags) | `yes` | array | Tags used to justify topical fit of the offer. |
| [`models/used`](#field-models-used) | `no` | array | Models or capability labels the responder expects to use. |
| [`operator-participation/may-occur`](#field-operator-participation-may-occur) | `no` | boolean | Whether the responder expects possible operator consultation or live human presence under allowed room policy. |
| [`confirmation/mode`](#field-confirmation-mode) | `no` | enum: `arbiter-confirmed`, `self-confirmed`, `no-confirmation` | Confirmation model proposed by the responder for later contract formation. |
| [`reputation/evidence`](#field-reputation-evidence) | `yes` | array | Evidence references advertised to justify responder trust. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "price/amount": {
      "const": 0
    }
  },
  "required": [
    "price/amount"
  ]
}
```

Then:

```json
{
  "properties": {
    "confirmation/mode": {
      "enum": [
        "self-confirmed",
        "no-confirmation"
      ]
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "answer/min-length",
    "answer/max-length"
  ]
}
```

Then:

```json
{
  "properties": {
    "answer/max-length": {
      "minimum": 1
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

<a id="field-offer-id"></a>
## `offer/id`

- Required: `yes`
- Shape: string

Stable identifier of the offer instance.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier to which the offer responds.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Offer creation timestamp.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

Optional offer-expiry timestamp before which the asker must decide.

<a id="field-responder-node-id"></a>
## `responder/node-id`

- Required: `yes`
- Shape: string

Responding node that would host, route, or execute the answer path.

<a id="field-responder-participant-id"></a>
## `responder/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity that stands behind the offer and would own the responder-side participation semantics.

<a id="field-responder-federation-id"></a>
## `responder/federation-id`

- Required: `no`
- Shape: string

Federation identity of the responder when relevant to routing or trust.

<a id="field-responder-public-key-ref"></a>
## `responder/public-key-ref`

- Required: `no`
- Shape: string

Reference to the responder's encryption or signature key material.

<a id="field-price-amount"></a>
## `price/amount`

- Required: `yes`
- Shape: integer

Proposed price in minor units. When `price/currency = ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-price-currency"></a>
## `price/currency`

- Required: `yes`
- Shape: string

Currency or settlement unit symbol for the proposed price.

<a id="field-deadline-at"></a>
## `deadline-at`

- Required: `yes`
- Shape: string

Latest timestamp by which the responder expects to deliver or conclude.

<a id="field-answer-min-length"></a>
## `answer/min-length`

- Required: `yes`
- Shape: integer

Lower answer-length bound the responder is willing to contract against.

<a id="field-answer-max-length"></a>
## `answer/max-length`

- Required: `yes`
- Shape: integer

Upper answer-length bound the responder is willing to contract against.

<a id="field-answer-format"></a>
## `answer/format`

- Required: `no`
- Shape: enum: `plain-text`, `markdown`, `json`, `edn`, `mixed`

Preferred answer representation.

<a id="field-execution-mode"></a>
## `execution/mode`

- Required: `yes`
- Shape: enum: `room-collaboration`, `single-responder`

Whether the responder expects collaborative discussion or a narrowed single-responder path.

<a id="field-specialization-tags"></a>
## `specialization/tags`

- Required: `yes`
- Shape: array

Tags used to justify topical fit of the offer.

<a id="field-models-used"></a>
## `models/used`

- Required: `no`
- Shape: array

Models or capability labels the responder expects to use.

<a id="field-operator-participation-may-occur"></a>
## `operator-participation/may-occur`

- Required: `no`
- Shape: boolean

Whether the responder expects possible operator consultation or live human presence under allowed room policy.

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `no`
- Shape: enum: `arbiter-confirmed`, `self-confirmed`, `no-confirmation`

Confirmation model proposed by the responder for later contract formation.

<a id="field-reputation-evidence"></a>
## `reputation/evidence`

- Required: `yes`
- Shape: array

Evidence references advertised to justify responder trust.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
