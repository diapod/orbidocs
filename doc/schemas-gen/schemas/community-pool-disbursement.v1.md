# Community Pool Disbursement v1

Source schema: [`doc/schemas/community-pool-disbursement.v1.schema.json`](../../schemas/community-pool-disbursement.v1.schema.json)

Machine-readable schema for one council-approved community-pool outflow. The signed surface uses `orbiplex-community-pool-disbursement-v1\x00 || deterministic_cbor(payload_without_signature)`.

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`disbursement/id`](#field-disbursement-id) | `yes` | string |  |
| [`pool/account-id`](#field-pool-account-id) | `yes` | string | Ledger account id of the source community-pool. |
| [`destination/account-id`](#field-destination-account-id) | `yes` | string | Ledger account id receiving the disbursement. |
| [`amount`](#field-amount) | `yes` | integer | Transferred amount in internal minor units. |
| [`unit`](#field-unit) | `yes` | const: `ORC` |  |
| [`purpose`](#field-purpose) | `yes` | enum: `ubc-subsidy`, `infrastructure-support`, `emergency-relief` |  |
| [`basis/refs`](#field-basis-refs) | `yes` | array |  |
| [`approved-by/id`](#field-approved-by-id) | `yes` | string |  |
| [`approved-at`](#field-approved-at) | `yes` | string |  |
| [`ledger-transfer/id`](#field-ledger-transfer-id) | `yes` | string | The append-only internal transfer that executed the outflow. |
| [`notes`](#field-notes) | `no` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-disbursement-id"></a>
## `disbursement/id`

- Required: `yes`
- Shape: string

<a id="field-pool-account-id"></a>
## `pool/account-id`

- Required: `yes`
- Shape: string

Ledger account id of the source community-pool.

<a id="field-destination-account-id"></a>
## `destination/account-id`

- Required: `yes`
- Shape: string

Ledger account id receiving the disbursement.

<a id="field-amount"></a>
## `amount`

- Required: `yes`
- Shape: integer

Transferred amount in internal minor units.

<a id="field-unit"></a>
## `unit`

- Required: `yes`
- Shape: const: `ORC`

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: enum: `ubc-subsidy`, `infrastructure-support`, `emergency-relief`

<a id="field-basis-refs"></a>
## `basis/refs`

- Required: `yes`
- Shape: array

<a id="field-approved-by-id"></a>
## `approved-by/id`

- Required: `yes`
- Shape: string

<a id="field-approved-at"></a>
## `approved-at`

- Required: `yes`
- Shape: string

<a id="field-ledger-transfer-id"></a>
## `ledger-transfer/id`

- Required: `yes`
- Shape: string

The append-only internal transfer that executed the outflow.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
