# Agent.product.read.request.v2

Source schema: [`doc/schemas/agent.product.read.request.v2.schema.json`](../../schemas/agent.product.read.request.v2.schema.json)

Module-private RAM result contract. No generic artifact access or replay regeneration authority.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer.md`](../../project/40-proposals/026-assessment-agent-consumer.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.product.read.request.v2` |  |
| [`product/ref`](#field-product-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.product.read.request.v2`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: string
