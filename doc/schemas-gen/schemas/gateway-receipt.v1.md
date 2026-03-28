# Gateway Receipt v1

Source schema: [`doc/schemas/gateway-receipt.v1.schema.json`](../../schemas/gateway-receipt.v1.schema.json)

Machine-readable schema for a fiat-to-credit or credit-to-fiat crossing performed by a trusted prepaid gateway node.

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
| [`receipt/id`](#field-receipt-id) | `yes` | string | Stable identifier of the gateway receipt. |
| [`gateway/node-id`](#field-gateway-node-id) | `yes` | string | Trusted gateway node that performed the external settlement crossing. |
| [`direction`](#field-direction) | `yes` | enum: `inbound`, `outbound` | Direction of value crossing the protocol boundary. `inbound` credits a local account, `outbound` debits it for payout. |
| [`external/amount`](#field-external-amount) | `yes` | number | Amount observed on the external payment rail. |
| [`external/currency`](#field-external-currency) | `yes` | string | External settlement currency or tender symbol. |
| [`internal/amount`](#field-internal-amount) | `yes` | integer | Credited or debited amount in internal minor units. |
| [`internal/currency`](#field-internal-currency) | `yes` | const: `ORC` | Internal settlement unit used by the supervised ledger in MVP. |
| [`account/id`](#field-account-id) | `yes` | string | Local supervised account affected by the gateway event. |
| [`ts`](#field-ts) | `yes` | string | Timestamp when the gateway event was committed for audit. |
| [`external/payment-ref`](#field-external-payment-ref) | `yes` | string | Gateway-side payment reference such as a PSP transaction id or bank transfer reference. |
| [`gateway-policy/ref`](#field-gateway-policy-ref) | `no` | string | Gateway policy under which this boundary crossing was executed. |
| [`external/provider`](#field-external-provider) | `no` | string | Payment service provider or banking rail label used by the gateway. |
| [`exchange-policy/ref`](#field-exchange-policy-ref) | `no` | string | Optional reference to the gateway-side pricing or exchange policy in force for this event. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "direction": {
      "const": "outbound"
    }
  },
  "required": [
    "direction"
  ]
}
```

Then:

```json
{
  "required": [
    "gateway-policy/ref"
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

Stable identifier of the gateway receipt.

<a id="field-gateway-node-id"></a>
## `gateway/node-id`

- Required: `yes`
- Shape: string

Trusted gateway node that performed the external settlement crossing.

<a id="field-direction"></a>
## `direction`

- Required: `yes`
- Shape: enum: `inbound`, `outbound`

Direction of value crossing the protocol boundary. `inbound` credits a local account, `outbound` debits it for payout.

<a id="field-external-amount"></a>
## `external/amount`

- Required: `yes`
- Shape: number

Amount observed on the external payment rail.

<a id="field-external-currency"></a>
## `external/currency`

- Required: `yes`
- Shape: string

External settlement currency or tender symbol.

<a id="field-internal-amount"></a>
## `internal/amount`

- Required: `yes`
- Shape: integer

Credited or debited amount in internal minor units.

<a id="field-internal-currency"></a>
## `internal/currency`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit used by the supervised ledger in MVP.

<a id="field-account-id"></a>
## `account/id`

- Required: `yes`
- Shape: string

Local supervised account affected by the gateway event.

<a id="field-ts"></a>
## `ts`

- Required: `yes`
- Shape: string

Timestamp when the gateway event was committed for audit.

<a id="field-external-payment-ref"></a>
## `external/payment-ref`

- Required: `yes`
- Shape: string

Gateway-side payment reference such as a PSP transaction id or bank transfer reference.

<a id="field-gateway-policy-ref"></a>
## `gateway-policy/ref`

- Required: `no`
- Shape: string

Gateway policy under which this boundary crossing was executed.

<a id="field-external-provider"></a>
## `external/provider`

- Required: `no`
- Shape: string

Payment service provider or banking rail label used by the gateway.

<a id="field-exchange-policy-ref"></a>
## `exchange-policy/ref`

- Required: `no`
- Shape: string

Optional reference to the gateway-side pricing or exchange policy in force for this event.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
