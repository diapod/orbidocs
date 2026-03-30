# Ledger Hold v1

Source schema: [`doc/schemas/ledger-hold.v1.schema.json`](../../schemas/ledger-hold.v1.schema.json)

Machine-readable schema for one supervised escrow hold on the host-ledger settlement rail.

## Governing Basis

- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

## Project Lineage

### Requirements

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
| [`hold/id`](#field-hold-id) | `yes` | string | Stable identifier of the escrow hold. |
| [`contract/id`](#field-contract-id) | `yes` | string | Procurement contract whose settlement path is anchored by this hold. |
| [`question/id`](#field-question-id) | `no` | string | Optional question lifecycle identifier for audit joins. |
| [`payer/account-id`](#field-payer-account-id) | `yes` | string | Ledger account from which value is reserved. |
| [`payee/account-id`](#field-payee-account-id) | `yes` | string | Ledger account eligible to receive release transfers from this hold. |
| [`escrow/node-id`](#field-escrow-node-id) | `yes` | string | Supervisory node responsible for maintaining the hold state machine. |
| [`escrow-policy/ref`](#field-escrow-policy-ref) | `no` | string | Escrow policy governing dispute, confirmation, and release behavior for this hold. |
| [`amount`](#field-amount) | `yes` | integer | Reserved amount in internal minor units. For `ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`unit`](#field-unit) | `yes` | const: `ORC` | Internal settlement unit carried by the hold in MVP. `ORC` uses fixed decimal scale `2`. |
| [`status`](#field-status) | `yes` | enum: `active`, `disputed`, `released`, `partially-released`, `refunded`, `expired` | Operational state of the hold. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the hold was created. |
| [`work-by`](#field-work-by) | `yes` | string | Deadline by which the responder is expected to deliver the work. |
| [`accept-by`](#field-accept-by) | `yes` | string | Deadline by which the payer should acknowledge the delivered work. |
| [`dispute-by`](#field-dispute-by) | `yes` | string | Last moment for opening a valid dispute under the contract policy. |
| [`auto-release-after`](#field-auto-release-after) | `yes` | string | Moment when the hold may be released automatically if prior conditions are satisfied and no dispute is open. |
| [`resolved-at`](#field-resolved-at) | `no` | string | Timestamp when the hold reached a terminal or review-complete state. |
| [`released/amount`](#field-released-amount) | `no` | integer | Amount already released from the hold, expressed in ORC minor units with fixed scale `2`. |
| [`refunded/amount`](#field-refunded-amount) | `no` | integer | Amount already refunded from the hold, expressed in ORC minor units with fixed scale `2`. |
| [`dispute/case-ref`](#field-dispute-case-ref) | `no` | string | Formal dispute or arbiter case opened against the hold, if any. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "disputed"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "dispute/case-ref"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "released",
        "partially-released",
        "refunded",
        "expired"
      ]
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "resolved-at"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "released",
        "partially-released"
      ]
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "released/amount"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "status": {
      "const": "refunded"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "refunded/amount"
  ]
}
```

### Rule 5

When:

```json
{
  "required": [
    "escrow/node-id"
  ]
}
```

Then:

```json
{
  "required": [
    "escrow-policy/ref"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-hold-id"></a>
## `hold/id`

- Required: `yes`
- Shape: string

Stable identifier of the escrow hold.

<a id="field-contract-id"></a>
## `contract/id`

- Required: `yes`
- Shape: string

Procurement contract whose settlement path is anchored by this hold.

<a id="field-question-id"></a>
## `question/id`

- Required: `no`
- Shape: string

Optional question lifecycle identifier for audit joins.

<a id="field-payer-account-id"></a>
## `payer/account-id`

- Required: `yes`
- Shape: string

Ledger account from which value is reserved.

<a id="field-payee-account-id"></a>
## `payee/account-id`

- Required: `yes`
- Shape: string

Ledger account eligible to receive release transfers from this hold.

<a id="field-escrow-node-id"></a>
## `escrow/node-id`

- Required: `yes`
- Shape: string

Supervisory node responsible for maintaining the hold state machine.

<a id="field-escrow-policy-ref"></a>
## `escrow-policy/ref`

- Required: `no`
- Shape: string

Escrow policy governing dispute, confirmation, and release behavior for this hold.

<a id="field-amount"></a>
## `amount`

- Required: `yes`
- Shape: integer

Reserved amount in internal minor units. For `ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-unit"></a>
## `unit`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit carried by the hold in MVP. `ORC` uses fixed decimal scale `2`.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `active`, `disputed`, `released`, `partially-released`, `refunded`, `expired`

Operational state of the hold.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the hold was created.

<a id="field-work-by"></a>
## `work-by`

- Required: `yes`
- Shape: string

Deadline by which the responder is expected to deliver the work.

<a id="field-accept-by"></a>
## `accept-by`

- Required: `yes`
- Shape: string

Deadline by which the payer should acknowledge the delivered work.

<a id="field-dispute-by"></a>
## `dispute-by`

- Required: `yes`
- Shape: string

Last moment for opening a valid dispute under the contract policy.

<a id="field-auto-release-after"></a>
## `auto-release-after`

- Required: `yes`
- Shape: string

Moment when the hold may be released automatically if prior conditions are satisfied and no dispute is open.

<a id="field-resolved-at"></a>
## `resolved-at`

- Required: `no`
- Shape: string

Timestamp when the hold reached a terminal or review-complete state.

<a id="field-released-amount"></a>
## `released/amount`

- Required: `no`
- Shape: integer

Amount already released from the hold, expressed in ORC minor units with fixed scale `2`.

<a id="field-refunded-amount"></a>
## `refunded/amount`

- Required: `no`
- Shape: integer

Amount already refunded from the hold, expressed in ORC minor units with fixed scale `2`.

<a id="field-dispute-case-ref"></a>
## `dispute/case-ref`

- Required: `no`
- Shape: string

Formal dispute or arbiter case opened against the hold, if any.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
