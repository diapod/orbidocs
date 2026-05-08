# Artifact Delivery Status v1

Source schema: [`doc/schemas/artifact-delivery-status.v1.schema.json`](../../schemas/artifact-delivery-status.v1.schema.json)

Operator/host status payload for a single Artifact Delivery run. This is not an MVP cross-component host capability.

## Governing Basis

- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-status.v1` |  |
| [`delivery/id`](#field-delivery-id) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent` |  |
| [`dispatch/plan`](#field-dispatch-plan) | `no` | object |  |
| [`stage/outcomes`](#field-stage-outcomes) | `no` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-status.v1`

<a id="field-delivery-id"></a>
## `delivery/id`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`

<a id="field-dispatch-plan"></a>
## `dispatch/plan`

- Required: `no`
- Shape: object

<a id="field-stage-outcomes"></a>
## `stage/outcomes`

- Required: `no`
- Shape: array
