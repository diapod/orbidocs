# Agent Outcome v2

Source schema: [`doc/schemas/agent.outcome.v2.schema.json`](../../schemas/agent.outcome.v2.schema.json)

Compatible successor preserving the exact selected Agent product digest and provider-neutral execution provenance.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.outcome.v2` |  |
| [`outcome`](#field-outcome) | `yes` | ref: `agent.outcome.v1.schema.json` |  |
| [`execution-binding/ref`](#field-execution-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.outcome.v2`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: ref: `agent.outcome.v1.schema.json`

<a id="field-execution-binding-ref"></a>
## `execution-binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
