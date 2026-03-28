# Ledger Transfer v1

Source schema: [`doc/schemas/ledger-transfer.v1.schema.json`](../../schemas/ledger-transfer.v1.schema.json)

Machine-readable schema for one append-only internal transfer recorded by the host-ledger settlement rail.

## Governing Basis

- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`transfer/id`](#field-transfer-id) | `yes` | string | Stable identifier of the append-only transfer fact. |
| [`kind`](#field-kind) | `yes` | enum: `top-up-credit`, `escrow-hold`, `release`, `partial-release`, `refund`, `payout-debit`, `adjustment` | Transfer class on the supervised ledger. |
| [`from/account-id`](#field-from-account-id) | `yes` | string | Debited ledger account identifier. |
| [`to/account-id`](#field-to-account-id) | `yes` | string | Credited ledger account identifier. |
| [`amount`](#field-amount) | `yes` | integer | Transferred amount in internal minor units. |
| [`unit`](#field-unit) | `yes` | const: `ORC` | Internal settlement unit carried by the transfer in MVP. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the transfer fact was recorded. |
| [`hold/id`](#field-hold-id) | `no` | string | Escrow hold to which the transfer belongs, when applicable. |
| [`contract/id`](#field-contract-id) | `no` | string | Procurement contract driving the transfer, when applicable. |
| [`gateway-receipt/id`](#field-gateway-receipt-id) | `no` | string | Gateway receipt that justified the transfer, when applicable. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "kind": {
      "enum": [
        "escrow-hold",
        "release",
        "partial-release",
        "refund"
      ]
    }
  },
  "required": [
    "kind"
  ]
}
```

Then:

```json
{
  "required": [
    "hold/id",
    "contract/id"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "kind": {
      "enum": [
        "top-up-credit",
        "payout-debit"
      ]
    }
  },
  "required": [
    "kind"
  ]
}
```

Then:

```json
{
  "required": [
    "gateway-receipt/id"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-transfer-id"></a>
## `transfer/id`

- Required: `yes`
- Shape: string

Stable identifier of the append-only transfer fact.

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `top-up-credit`, `escrow-hold`, `release`, `partial-release`, `refund`, `payout-debit`, `adjustment`

Transfer class on the supervised ledger.

<a id="field-from-account-id"></a>
## `from/account-id`

- Required: `yes`
- Shape: string

Debited ledger account identifier.

<a id="field-to-account-id"></a>
## `to/account-id`

- Required: `yes`
- Shape: string

Credited ledger account identifier.

<a id="field-amount"></a>
## `amount`

- Required: `yes`
- Shape: integer

Transferred amount in internal minor units.

<a id="field-unit"></a>
## `unit`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit carried by the transfer in MVP.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the transfer fact was recorded.

<a id="field-hold-id"></a>
## `hold/id`

- Required: `no`
- Shape: string

Escrow hold to which the transfer belongs, when applicable.

<a id="field-contract-id"></a>
## `contract/id`

- Required: `no`
- Shape: string

Procurement contract driving the transfer, when applicable.

<a id="field-gateway-receipt-id"></a>
## `gateway-receipt/id`

- Required: `no`
- Shape: string

Gateway receipt that justified the transfer, when applicable.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
