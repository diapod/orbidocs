# Agent.product.read.request.v3

Source schema: [`doc/schemas/agent.product.read.request.v3.schema.json`](../../schemas/agent.product.read.request.v3.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.product.read.request.v3` |  |
| [`product/ref`](#field-product-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.product.read.request.v3`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: string
