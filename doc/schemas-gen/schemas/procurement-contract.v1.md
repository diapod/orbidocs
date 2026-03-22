# Procurement Contract v1

Source schema: [`doc/schemas/procurement-contract.v1.schema.json`](../../schemas/procurement-contract.v1.schema.json)

Machine-readable schema for a selected responder contract linked to a procurement question lifecycle.

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
| [`contract/id`](#field-contract-id) | `yes` | string | Stable identifier of the procurement contract. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier to which the contract belongs. |
| [`room/id`](#field-room-id) | `yes` | string | Room or execution channel bound to the selected responder path. |
| [`selected-offer/id`](#field-selected-offer-id) | `yes` | string | Identifier of the offer chosen for contract formation. |
| [`created-at`](#field-created-at) | `yes` | string | Contract creation timestamp. |
| [`asker/node-id`](#field-asker-node-id) | `yes` | string | Node acting for the asking side of the contract. |
| [`asker/pod-user-id`](#field-asker-pod-user-id) | `no` | string | Hosted-user identity when the contract was created on behalf of a pod-backed client. |
| [`responder/node-id`](#field-responder-node-id) | `yes` | string | Node selected to fulfill the answer contract. |
| [`payment/amount`](#field-payment-amount) | `yes` | integer | Agreed payment amount in minor units. |
| [`payment/currency`](#field-payment-currency) | `yes` | string | Currency or settlement unit symbol for the contract payment. |
| [`settlement/rail`](#field-settlement-rail) | `no` | enum: `external-invoice`, `host-ledger`, `manual-transfer`, `none` | Settlement rail chosen outside the protocol core. |
| [`deadline-at`](#field-deadline-at) | `yes` | string | Deadline by which the responder must deliver or the contract expires. |
| [`acceptance/answer-format`](#field-acceptance-answer-format) | `yes` | enum: `plain-text`, `markdown`, `json`, `edn`, `mixed` | Expected answer format used for acceptance checks. |
| [`acceptance/min-length`](#field-acceptance-min-length) | `yes` | integer | Minimum accepted answer length. |
| [`acceptance/max-length`](#field-acceptance-max-length) | `yes` | integer | Maximum accepted answer length. |
| [`acceptance/arbiter-set`](#field-acceptance-arbiter-set) | `no` | array | Arbiter identities required when arbiter confirmation is part of the contract. |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | enum: `arbiter-confirmed`, `self-confirmed`, `no-confirmation` | Confirmation mode required before settlement. |
| [`status`](#field-status) | `yes` | enum: `pending`, `settled`, `rejected`, `expired`, `canceled` | Current lifecycle status of the contract. |
| [`transport/encryption-mode`](#field-transport-encryption-mode) | `no` | enum: `none`, `recipient-key`, `federation-policy` | Expected transport-level privacy mode for the narrowed execution path. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "confirmation/mode": {
      "const": "arbiter-confirmed"
    }
  },
  "required": [
    "confirmation/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "acceptance/arbiter-set"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "confirmation/mode": {
      "const": "no-confirmation"
    }
  },
  "required": [
    "confirmation/mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "payment/amount": {
      "const": 0
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

<a id="field-contract-id"></a>
## `contract/id`

- Required: `yes`
- Shape: string

Stable identifier of the procurement contract.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier to which the contract belongs.

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

Room or execution channel bound to the selected responder path.

<a id="field-selected-offer-id"></a>
## `selected-offer/id`

- Required: `yes`
- Shape: string

Identifier of the offer chosen for contract formation.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Contract creation timestamp.

<a id="field-asker-node-id"></a>
## `asker/node-id`

- Required: `yes`
- Shape: string

Node acting for the asking side of the contract.

<a id="field-asker-pod-user-id"></a>
## `asker/pod-user-id`

- Required: `no`
- Shape: string

Hosted-user identity when the contract was created on behalf of a pod-backed client.

<a id="field-responder-node-id"></a>
## `responder/node-id`

- Required: `yes`
- Shape: string

Node selected to fulfill the answer contract.

<a id="field-payment-amount"></a>
## `payment/amount`

- Required: `yes`
- Shape: integer

Agreed payment amount in minor units.

<a id="field-payment-currency"></a>
## `payment/currency`

- Required: `yes`
- Shape: string

Currency or settlement unit symbol for the contract payment.

<a id="field-settlement-rail"></a>
## `settlement/rail`

- Required: `no`
- Shape: enum: `external-invoice`, `host-ledger`, `manual-transfer`, `none`

Settlement rail chosen outside the protocol core.

<a id="field-deadline-at"></a>
## `deadline-at`

- Required: `yes`
- Shape: string

Deadline by which the responder must deliver or the contract expires.

<a id="field-acceptance-answer-format"></a>
## `acceptance/answer-format`

- Required: `yes`
- Shape: enum: `plain-text`, `markdown`, `json`, `edn`, `mixed`

Expected answer format used for acceptance checks.

<a id="field-acceptance-min-length"></a>
## `acceptance/min-length`

- Required: `yes`
- Shape: integer

Minimum accepted answer length.

<a id="field-acceptance-max-length"></a>
## `acceptance/max-length`

- Required: `yes`
- Shape: integer

Maximum accepted answer length.

<a id="field-acceptance-arbiter-set"></a>
## `acceptance/arbiter-set`

- Required: `no`
- Shape: array

Arbiter identities required when arbiter confirmation is part of the contract.

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `yes`
- Shape: enum: `arbiter-confirmed`, `self-confirmed`, `no-confirmation`

Confirmation mode required before settlement.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `pending`, `settled`, `rejected`, `expired`, `canceled`

Current lifecycle status of the contract.

<a id="field-transport-encryption-mode"></a>
## `transport/encryption-mode`

- Required: `no`
- Shape: enum: `none`, `recipient-key`, `federation-policy`

Expected transport-level privacy mode for the narrowed execution path.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
