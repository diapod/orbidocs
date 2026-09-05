# Service-order.result.prepare.request.v1

Source schema: [`doc/schemas/service-order.result.prepare.request.v1.schema.json`](../../schemas/service-order.result.prepare.request.v1.schema.json)

Data-only producer binding. Source authority remains independent; missing evidence never implies local execution.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-order.result.prepare.request.v1` |  |
| [`result`](#field-result) | `yes` | ref: `service-order-result.v1.schema.json` |  |
| [`source`](#field-source) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-order.result.prepare.request.v1`

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: ref: `service-order-result.v1.schema.json`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: unspecified
