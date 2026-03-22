# Ubc Settlement v1

Source schema: [`doc/schemas/ubc-settlement.v1.schema.json`](../../schemas/ubc-settlement.v1.schema.json)

Machine-readable schema for periodic settlement records of Universal Basic Compute funding, allocation, and optional FIP bridge usage.

## Governing Basis

- [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](../../normative/40-constitution/pl/CONSTITUTION.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)
- [`doc/normative/50-constitutional-ops/pl/SWARM-ECONOMY-SUFFICIENCY.pl.md`](../../normative/50-constitutional-ops/pl/SWARM-ECONOMY-SUFFICIENCY.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`settlement_id`](#field-settlement-id) | `yes` | string | Stable identifier of this settlement record. |
| [`federation_id`](#field-federation-id) | `yes` | string | Federation whose funding floor and usage are being settled. |
| [`period_start`](#field-period-start) | `yes` | string |  |
| [`period_end`](#field-period-end) | `yes` | string |  |
| [`compute_unit`](#field-compute-unit) | `yes` | string | Unit of account used for compute funding and usage in this settlement window. |
| [`beneficiary_count`](#field-beneficiary-count) | `yes` | integer | Number of persons whose UBC floor was funded in the settlement period. |
| [`total_allocated_compute`](#field-total-allocated-compute) | `yes` | number | Total compute budget allocated to the UBC floor in the settlement period. |
| [`funding_sources`](#field-funding-sources) | `yes` | array |  |
| [`emergency_usage`](#field-emergency-usage) | `yes` | number |  |
| [`communication_usage`](#field-communication-usage) | `yes` | number |  |
| [`care_usage`](#field-care-usage) | `yes` | number |  |
| [`bridge_usage`](#field-bridge-usage) | `no` | array |  |
| [`policy_ref`](#field-policy-ref) | `yes` | string | Reference to the governing funding or sufficiency policy used for this settlement. |
| [`created_at`](#field-created-at) | `yes` | string |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`fundingSource`](#def-fundingsource) | object |  |
| [`bridgeUsage`](#def-bridgeusage) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-settlement-id"></a>
## `settlement_id`

- Required: `yes`
- Shape: string

Stable identifier of this settlement record.

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

Federation whose funding floor and usage are being settled.

<a id="field-period-start"></a>
## `period_start`

- Required: `yes`
- Shape: string

<a id="field-period-end"></a>
## `period_end`

- Required: `yes`
- Shape: string

<a id="field-compute-unit"></a>
## `compute_unit`

- Required: `yes`
- Shape: string

Unit of account used for compute funding and usage in this settlement window.

<a id="field-beneficiary-count"></a>
## `beneficiary_count`

- Required: `yes`
- Shape: integer

Number of persons whose UBC floor was funded in the settlement period.

<a id="field-total-allocated-compute"></a>
## `total_allocated_compute`

- Required: `yes`
- Shape: number

Total compute budget allocated to the UBC floor in the settlement period.

<a id="field-funding-sources"></a>
## `funding_sources`

- Required: `yes`
- Shape: array

<a id="field-emergency-usage"></a>
## `emergency_usage`

- Required: `yes`
- Shape: number

<a id="field-communication-usage"></a>
## `communication_usage`

- Required: `yes`
- Shape: number

<a id="field-care-usage"></a>
## `care_usage`

- Required: `yes`
- Shape: number

<a id="field-bridge-usage"></a>
## `bridge_usage`

- Required: `no`
- Shape: array

<a id="field-policy-ref"></a>
## `policy_ref`

- Required: `yes`
- Shape: string

Reference to the governing funding or sufficiency policy used for this settlement.

<a id="field-created-at"></a>
## `created_at`

- Required: `yes`
- Shape: string

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-fundingsource"></a>
## `$defs.fundingSource`

- Shape: object

<a id="def-bridgeusage"></a>
## `$defs.bridgeUsage`

- Shape: object
