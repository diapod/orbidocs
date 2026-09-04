# External Agent Runtime Product V2

Source schema: [`doc/schemas/agent.external-runtime.product.v2.schema.json`](../../schemas/agent.external-runtime.product.v2.schema.json)

Compatible successor binding one V1 external-runtime product to provider-neutral realized inference execution provenance.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.product.v2` |  |
| [`product`](#field-product) | `yes` | ref: `agent.external-runtime.product.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.product.v2`

<a id="field-product"></a>
## `product`

- Required: `yes`
- Shape: ref: `agent.external-runtime.product.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
