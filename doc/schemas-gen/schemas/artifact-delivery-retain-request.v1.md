# Artifact Delivery Retain Request v1

Source schema: [`doc/schemas/artifact-delivery-retain-request.v1.schema.json`](../../schemas/artifact-delivery-retain-request.v1.schema.json)

Authenticated host-local request to retain one content-bound artifact without granting delivery, publication, or read authority.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-retain-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`owner/component-id`](#field-owner-component-id) | `yes` | string |  |
| [`artifact`](#field-artifact) | `yes` | object |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-retain-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-owner-component-id"></a>
## `owner/component-id`

- Required: `yes`
- Shape: string

<a id="field-artifact"></a>
## `artifact`

- Required: `yes`
- Shape: object

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
