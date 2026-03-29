# Gateway Policy v1

Source schema: [`doc/schemas/gateway-policy.v1.schema.json`](../../schemas/gateway-policy.v1.schema.json)

Machine-readable schema for one trusted gateway policy binding a servicing node to an accountable organization in the host-ledger settlement rail.

## Governing Basis

- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
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
| [`policy/id`](#field-policy-id) | `yes` | string | Stable identifier of the gateway policy. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the gateway policy became auditable. |
| [`federation/id`](#field-federation-id) | `yes` | string | Federation scope in which the gateway policy applies. |
| [`gateway/node-id`](#field-gateway-node-id) | `yes` | string | Node currently serving the trusted gateway role under this policy. |
| [`operator/org-ref`](#field-operator-org-ref) | `yes` | string | Accountable organization operating the gateway policy. |
| [`settlement/unit`](#field-settlement-unit) | `yes` | const: `ORC` | Internal settlement unit handled by this gateway policy in MVP. |
| [`supported/directions`](#field-supported-directions) | `yes` | array | Permitted directions for fiat-to-credit or credit-to-fiat boundary crossings. |
| [`kyc/mode`](#field-kyc-mode) | `no` | enum: `none`, `provider-managed`, `manual-review` | High-level compliance posture applied to payout or top-up flows. |
| [`payout/manual-review`](#field-payout-manual-review) | `no` | boolean | Whether outbound settlement may require manual review under this policy. |
| [`external/providers`](#field-external-providers) | `no` | array | Named external payment providers or rails admitted under this policy. |
| [`fee/ingress-rate`](#field-fee-ingress-rate) | `yes` | number | Fixed ingress fee rate applied on gross external top-up amount in MVP. |
| [`fee/ingress-destination-account-id`](#field-fee-ingress-destination-account-id) | `yes` | string | Ledger account that receives ingress fee credits, typically the `community-pool`. |
| [`fee/ingress-min-internal-amount`](#field-fee-ingress-min-internal-amount) | `yes` | integer | Minimum internal-equivalent amount below which ingress fee is not applied. |
| [`fee/egress-rate`](#field-fee-egress-rate) | `yes` | number \| null | Optional payout-side fee rate. MVP keeps this `null` until outbound payout stabilizes. |
| [`status`](#field-status) | `yes` | enum: `active`, `suspended`, `retired` | Administrative lifecycle state of the gateway policy. |
| [`suspended-at`](#field-suspended-at) | `no` | string | Timestamp when the gateway policy was suspended, if applicable. |
| [`retired-at`](#field-retired-at) | `no` | string | Timestamp when the gateway policy was retired, if applicable. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "suspended"
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
    "suspended-at"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "retired"
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
    "retired-at"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

Stable identifier of the gateway policy.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the gateway policy became auditable.

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

Federation scope in which the gateway policy applies.

<a id="field-gateway-node-id"></a>
## `gateway/node-id`

- Required: `yes`
- Shape: string

Node currently serving the trusted gateway role under this policy.

<a id="field-operator-org-ref"></a>
## `operator/org-ref`

- Required: `yes`
- Shape: string

Accountable organization operating the gateway policy.

<a id="field-settlement-unit"></a>
## `settlement/unit`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit handled by this gateway policy in MVP.

<a id="field-supported-directions"></a>
## `supported/directions`

- Required: `yes`
- Shape: array

Permitted directions for fiat-to-credit or credit-to-fiat boundary crossings.

<a id="field-kyc-mode"></a>
## `kyc/mode`

- Required: `no`
- Shape: enum: `none`, `provider-managed`, `manual-review`

High-level compliance posture applied to payout or top-up flows.

<a id="field-payout-manual-review"></a>
## `payout/manual-review`

- Required: `no`
- Shape: boolean

Whether outbound settlement may require manual review under this policy.

<a id="field-external-providers"></a>
## `external/providers`

- Required: `no`
- Shape: array

Named external payment providers or rails admitted under this policy.

<a id="field-fee-ingress-rate"></a>
## `fee/ingress-rate`

- Required: `yes`
- Shape: number

Fixed ingress fee rate applied on gross external top-up amount in MVP.

<a id="field-fee-ingress-destination-account-id"></a>
## `fee/ingress-destination-account-id`

- Required: `yes`
- Shape: string

Ledger account that receives ingress fee credits, typically the `community-pool`.

<a id="field-fee-ingress-min-internal-amount"></a>
## `fee/ingress-min-internal-amount`

- Required: `yes`
- Shape: integer

Minimum internal-equivalent amount below which ingress fee is not applied.

<a id="field-fee-egress-rate"></a>
## `fee/egress-rate`

- Required: `yes`
- Shape: number | null

Optional payout-side fee rate. MVP keeps this `null` until outbound payout stabilizes.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `active`, `suspended`, `retired`

Administrative lifecycle state of the gateway policy.

<a id="field-suspended-at"></a>
## `suspended-at`

- Required: `no`
- Shape: string

Timestamp when the gateway policy was suspended, if applicable.

<a id="field-retired-at"></a>
## `retired-at`

- Required: `no`
- Shape: string

Timestamp when the gateway policy was retired, if applicable.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
