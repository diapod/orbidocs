# Procurement Receipt v1

Source schema: [`doc/schemas/procurement-receipt.v1.schema.json`](../../schemas/procurement-receipt.v1.schema.json)

Machine-readable schema for the auditable outcome of a procurement contract.

## Governing Basis

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)
- [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)
- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)
- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`receipt/id`](#field-receipt-id) | `yes` | string | Stable identifier of the outcome receipt. |
| [`contract/id`](#field-contract-id) | `yes` | string | Procurement contract to which this receipt belongs. |
| [`question/id`](#field-question-id) | `yes` | string | Question lifecycle identifier for audit joins. |
| [`created-at`](#field-created-at) | `yes` | string | Receipt creation timestamp. |
| [`payer/participant-id`](#field-payer-participant-id) | `yes` | string | Participation-role identity on the payer/asker side whose acceptance or refusal is being recorded. |
| [`payee/participant-id`](#field-payee-participant-id) | `yes` | string | Participation-role identity on the payee/responder side whose acknowledgement or outcome is being recorded. |
| [`settled-at`](#field-settled-at) | `no` | string | Timestamp at which settlement or equivalent terminal confirmation completed. |
| [`outcome`](#field-outcome) | `yes` | enum: `settled`, `rejected`, `expired`, `canceled` | Terminal contract outcome recorded by the local node. |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only` | Confirmation mode actually used for the recorded outcome. |
| [`answer/accepted`](#field-answer-accepted) | `no` | boolean | Whether the received answer or summary satisfied the contract criteria. |
| [`payer/signature`](#field-payer-signature) | `no` | string | Signature or reference proving payer-side acceptance of the recorded outcome. |
| [`payee/signature`](#field-payee-signature) | `no` | string | Signature or reference proving payee-side acknowledgement of the recorded outcome. |
| [`arbiter/signatures`](#field-arbiter-signatures) | `no` | array | Arbiter confirmations when the contract required arbiter approval. |
| [`settlement/rail`](#field-settlement-rail) | `no` | enum: `external-invoice`, `host-ledger`, `manual-transfer`, `none` | Settlement rail used outside the protocol core. |
| [`settlement/ref`](#field-settlement-ref) | `no` | string | External settlement reference such as an invoice id, ledger entry id, or transfer reference. |
| [`settlement/hold-ref`](#field-settlement-hold-ref) | `no` | string | Host-ledger hold reference from which release or refund was resolved. |
| [`settlement/transfer-refs`](#field-settlement-transfer-refs) | `no` | array | One or more host-ledger transfer references that completed release, partial release, refund, or payout bookkeeping for the contract. |
| [`rejection/reason`](#field-rejection-reason) | `no` | string | Human- or machine-readable reason when the answer or contract outcome was not accepted. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "settled"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "settled-at",
    "answer/accepted",
    "payer/signature",
    "payee/signature"
  ],
  "properties": {
    "answer/accepted": {
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
    "arbiter/signatures"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "rejected",
        "expired",
        "canceled"
      ]
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "rejection/reason"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "settlement/rail": {
      "const": "host-ledger"
    }
  },
  "required": [
    "settlement/rail"
  ]
}
```

Then:

```json
{
  "required": [
    "settlement/ref",
    "settlement/hold-ref",
    "settlement/transfer-refs"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-receipt-id"></a>
## `receipt/id`

- Required: `yes`
- Shape: string

Stable identifier of the outcome receipt.

<a id="field-contract-id"></a>
## `contract/id`

- Required: `yes`
- Shape: string

Procurement contract to which this receipt belongs.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Question lifecycle identifier for audit joins.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Receipt creation timestamp.

<a id="field-payer-participant-id"></a>
## `payer/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity on the payer/asker side whose acceptance or refusal is being recorded.

<a id="field-payee-participant-id"></a>
## `payee/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity on the payee/responder side whose acknowledgement or outcome is being recorded.

<a id="field-settled-at"></a>
## `settled-at`

- Required: `no`
- Shape: string

Timestamp at which settlement or equivalent terminal confirmation completed.

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `settled`, `rejected`, `expired`, `canceled`

Terminal contract outcome recorded by the local node.

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `yes`
- Shape: enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only`

Confirmation mode actually used for the recorded outcome.

<a id="field-answer-accepted"></a>
## `answer/accepted`

- Required: `no`
- Shape: boolean

Whether the received answer or summary satisfied the contract criteria.

<a id="field-payer-signature"></a>
## `payer/signature`

- Required: `no`
- Shape: string

Signature or reference proving payer-side acceptance of the recorded outcome.

<a id="field-payee-signature"></a>
## `payee/signature`

- Required: `no`
- Shape: string

Signature or reference proving payee-side acknowledgement of the recorded outcome.

<a id="field-arbiter-signatures"></a>
## `arbiter/signatures`

- Required: `no`
- Shape: array

Arbiter confirmations when the contract required arbiter approval.

<a id="field-settlement-rail"></a>
## `settlement/rail`

- Required: `no`
- Shape: enum: `external-invoice`, `host-ledger`, `manual-transfer`, `none`

Settlement rail used outside the protocol core.

<a id="field-settlement-ref"></a>
## `settlement/ref`

- Required: `no`
- Shape: string

External settlement reference such as an invoice id, ledger entry id, or transfer reference.

<a id="field-settlement-hold-ref"></a>
## `settlement/hold-ref`

- Required: `no`
- Shape: string

Host-ledger hold reference from which release or refund was resolved.

<a id="field-settlement-transfer-refs"></a>
## `settlement/transfer-refs`

- Required: `no`
- Shape: array

One or more host-ledger transfer references that completed release, partial release, refund, or payout bookkeeping for the contract.

<a id="field-rejection-reason"></a>
## `rejection/reason`

- Required: `no`
- Shape: string

Human- or machine-readable reason when the answer or contract outcome was not accepted.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
