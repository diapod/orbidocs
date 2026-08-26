# Artifact Delivery Retain Result v1

Source schema: [`doc/schemas/artifact-delivery-retain-result.v1.schema.json`](../../schemas/artifact-delivery-retain-result.v1.schema.json)

Host-owned content and receipt binding returned after one artifact is durably retained.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-retain-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`outcome`](#field-outcome) | `yes` | const: `completed` |  |
| [`artifact/ref`](#field-artifact-ref) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | string |  |
| [`artifact/size-bytes`](#field-artifact-size-bytes) | `yes` | integer |  |
| [`execution/receipt`](#field-execution-receipt) | `yes` | ref: `execution-receipt.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-retain-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: const: `completed`

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: string

<a id="field-artifact-size-bytes"></a>
## `artifact/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-execution-receipt"></a>
## `execution/receipt`

- Required: `yes`
- Shape: ref: `execution-receipt.v1.schema.json`
