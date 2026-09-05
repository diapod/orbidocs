# Service Order Result v2

Source schema: [`doc/schemas/service-order-result.v2.schema.json`](../../schemas/service-order-result.v2.schema.json)

Compatible terminal-result envelope. The exact V1 result and provider-owned inference descriptor are content-bound. Transport authenticity and buyer correlation/policy remain independent admission gates. External descriptor refs must be resolved and verified before acceptance.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-order.result.v2` |  |
| [`result`](#field-result) | `yes` | ref: `service-order-result.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-order.result.v2`

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: ref: `service-order-result.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
