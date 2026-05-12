# Artifact Delivery Recovery v1

Source schema: [`doc/schemas/artifact-delivery-recovery.v1.schema.json`](../../schemas/artifact-delivery-recovery.v1.schema.json)

Operator response returned after one Artifact Delivery recovery pass.

## Governing Basis

- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-recovery.v1` |  |
| [`status`](#field-status) | `yes` | const: `ok` |  |
| [`recovered/count`](#field-recovered-count) | `yes` | integer |  |
| [`deliveries`](#field-deliveries) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-recovery.v1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `ok`

<a id="field-recovered-count"></a>
## `recovered/count`

- Required: `yes`
- Shape: integer

<a id="field-deliveries"></a>
## `deliveries`

- Required: `yes`
- Shape: array
