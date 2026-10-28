# Agent.product.read.response.v3

Source schema: [`doc/schemas/agent.product.read.response.v3.schema.json`](../../schemas/agent.product.read.response.v3.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.product.read.response.v3` |  |
| [`product/ref`](#field-product-ref) | `yes` | string |  |
| [`content/base64`](#field-content-base64) | `yes` | string |  |
| [`content/bytes`](#field-content-bytes) | `yes` | integer |  |
| [`context/authority-dependencies`](#field-context-authority-dependencies) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.product.read.response.v3`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: string

<a id="field-content-base64"></a>
## `content/base64`

- Required: `yes`
- Shape: string

<a id="field-content-bytes"></a>
## `content/bytes`

- Required: `yes`
- Shape: integer

<a id="field-context-authority-dependencies"></a>
## `context/authority-dependencies`

- Required: `yes`
- Shape: array
