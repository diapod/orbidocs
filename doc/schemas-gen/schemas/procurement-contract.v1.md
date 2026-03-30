# Procurement Contract v1

Source schema: [`doc/schemas/procurement-contract.v1.schema.json`](../../schemas/procurement-contract.v1.schema.json)

Machine-readable schema for a selected responder contract linked to a procurement question lifecycle.

## Governing Basis

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)
- [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)
- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001.md`](../../project/50-requirements/requirements-001.md)
- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

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
| [`source/marketplace-refs`](#field-source-marketplace-refs) | `no` | object | Optional marketplace refs preserved when the contract is opened through the service-order bridge. |
| [`created-at`](#field-created-at) | `yes` | string | Contract creation timestamp. |
| [`asker/node-id`](#field-asker-node-id) | `yes` | string | Node acting for the asking side of the contract as the routing or hosting identity. |
| [`asker/participant-id`](#field-asker-participant-id) | `yes` | string | Participation-role identity on whose behalf the asking side entered the contract. |
| [`asker/pod-user-id`](#field-asker-pod-user-id) | `no` | string | Hosted-user identity when the contract was created on behalf of a later pod-backed client flow. This is additive to, not a replacement for, `asker/participant-id`. |
| [`responder/node-id`](#field-responder-node-id) | `yes` | string | Node selected to fulfill the answer contract as the routing or hosting identity. |
| [`responder/participant-id`](#field-responder-participant-id) | `yes` | string | Participation-role identity selected to fulfill or lead the responder side of the contract. |
| [`payment/amount`](#field-payment-amount) | `yes` | integer | Agreed payment amount in minor units. When `payment/currency = ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`payment/currency`](#field-payment-currency) | `yes` | string | Currency or settlement unit symbol for the contract payment. |
| [`payer/account-ref`](#field-payer-account-ref) | `no` | string | Optional payer-side canonical settlement owner reference. The role lives in the identifier prefix, so no separate `payer/kind` field is used. This becomes required for the `host-ledger` rail. |
| [`payee/account-ref`](#field-payee-account-ref) | `no` | string | Optional payee-side canonical settlement owner reference. The role lives in the identifier prefix, so no separate `payee/kind` field is used. This becomes required for the `host-ledger` rail. |
| [`settlement/rail`](#field-settlement-rail) | `no` | enum: `external-invoice`, `host-ledger`, `manual-transfer`, `none` | Settlement rail chosen outside the protocol core. |
| [`deadline-at`](#field-deadline-at) | `yes` | string | Deadline by which the responder must deliver or the contract expires. |
| [`escrow/node-id`](#field-escrow-node-id) | `no` | string | Supervisory node responsible for the host-ledger escrow path. |
| [`escrow/hold-ref`](#field-escrow-hold-ref) | `no` | string | Reference to the host-ledger hold created for this contract. |
| [`escrow-policy/ref`](#field-escrow-policy-ref) | `no` | string | Escrow policy in force for this host-ledger contract. |
| [`deadlines/work-by`](#field-deadlines-work-by) | `no` | string | Responder delivery deadline in the host-ledger timeout cascade. This SHOULD align with `deadline-at`. |
| [`deadlines/accept-by`](#field-deadlines-accept-by) | `no` | string | Deadline by which the payer should acknowledge delivered work. |
| [`deadlines/dispute-by`](#field-deadlines-dispute-by) | `no` | string | Last moment for opening a formal dispute under the contract policy. |
| [`deadlines/auto-release`](#field-deadlines-auto-release) | `no` | string | Moment when escrow may auto-release if contract conditions are satisfied and no dispute is open. |
| [`acceptance/answer-format`](#field-acceptance-answer-format) | `yes` | enum: `plain-text`, `markdown`, `json`, `edn`, `mixed` | Expected answer format used for acceptance checks. |
| [`acceptance/min-length`](#field-acceptance-min-length) | `yes` | integer | Minimum accepted answer length. |
| [`acceptance/max-length`](#field-acceptance-max-length) | `yes` | integer | Maximum accepted answer length. |
| [`acceptance/arbiter-set`](#field-acceptance-arbiter-set) | `no` | array | Arbiter identities required when arbiter confirmation is part of the contract. |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only` | Confirmation mode required before settlement. |
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
    "payer/account-ref",
    "payee/account-ref",
    "escrow/node-id",
    "escrow/hold-ref",
    "escrow-policy/ref",
    "deadlines/work-by",
    "deadlines/accept-by",
    "deadlines/dispute-by",
    "deadlines/auto-release"
  ],
  "properties": {
    "payment/currency": {
      "const": "ORC"
    }
  }
}
```

### Rule 3

When:

```json
{
  "anyOf": [
    {
      "required": [
        "deadlines/work-by"
      ]
    },
    {
      "required": [
        "deadlines/accept-by"
      ]
    },
    {
      "required": [
        "deadlines/dispute-by"
      ]
    },
    {
      "required": [
        "deadlines/auto-release"
      ]
    }
  ]
}
```

Then:

```json
{
  "required": [
    "deadlines/work-by",
    "deadlines/accept-by",
    "deadlines/dispute-by",
    "deadlines/auto-release"
  ]
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

<a id="field-source-marketplace-refs"></a>
## `source/marketplace-refs`

- Required: `no`
- Shape: object

Optional marketplace refs preserved when the contract is opened through the service-order bridge.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Contract creation timestamp.

<a id="field-asker-node-id"></a>
## `asker/node-id`

- Required: `yes`
- Shape: string

Node acting for the asking side of the contract as the routing or hosting identity.

<a id="field-asker-participant-id"></a>
## `asker/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity on whose behalf the asking side entered the contract.

<a id="field-asker-pod-user-id"></a>
## `asker/pod-user-id`

- Required: `no`
- Shape: string

Hosted-user identity when the contract was created on behalf of a later pod-backed client flow. This is additive to, not a replacement for, `asker/participant-id`.

<a id="field-responder-node-id"></a>
## `responder/node-id`

- Required: `yes`
- Shape: string

Node selected to fulfill the answer contract as the routing or hosting identity.

<a id="field-responder-participant-id"></a>
## `responder/participant-id`

- Required: `yes`
- Shape: string

Participation-role identity selected to fulfill or lead the responder side of the contract.

<a id="field-payment-amount"></a>
## `payment/amount`

- Required: `yes`
- Shape: integer

Agreed payment amount in minor units. When `payment/currency = ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-payment-currency"></a>
## `payment/currency`

- Required: `yes`
- Shape: string

Currency or settlement unit symbol for the contract payment.

<a id="field-payer-account-ref"></a>
## `payer/account-ref`

- Required: `no`
- Shape: string

Optional payer-side canonical settlement owner reference. The role lives in the identifier prefix, so no separate `payer/kind` field is used. This becomes required for the `host-ledger` rail.

<a id="field-payee-account-ref"></a>
## `payee/account-ref`

- Required: `no`
- Shape: string

Optional payee-side canonical settlement owner reference. The role lives in the identifier prefix, so no separate `payee/kind` field is used. This becomes required for the `host-ledger` rail.

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

<a id="field-escrow-node-id"></a>
## `escrow/node-id`

- Required: `no`
- Shape: string

Supervisory node responsible for the host-ledger escrow path.

<a id="field-escrow-hold-ref"></a>
## `escrow/hold-ref`

- Required: `no`
- Shape: string

Reference to the host-ledger hold created for this contract.

<a id="field-escrow-policy-ref"></a>
## `escrow-policy/ref`

- Required: `no`
- Shape: string

Escrow policy in force for this host-ledger contract.

<a id="field-deadlines-work-by"></a>
## `deadlines/work-by`

- Required: `no`
- Shape: string

Responder delivery deadline in the host-ledger timeout cascade. This SHOULD align with `deadline-at`.

<a id="field-deadlines-accept-by"></a>
## `deadlines/accept-by`

- Required: `no`
- Shape: string

Deadline by which the payer should acknowledge delivered work.

<a id="field-deadlines-dispute-by"></a>
## `deadlines/dispute-by`

- Required: `no`
- Shape: string

Last moment for opening a formal dispute under the contract policy.

<a id="field-deadlines-auto-release"></a>
## `deadlines/auto-release`

- Required: `no`
- Shape: string

Moment when escrow may auto-release if contract conditions are satisfied and no dispute is open.

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
- Shape: enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only`

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
