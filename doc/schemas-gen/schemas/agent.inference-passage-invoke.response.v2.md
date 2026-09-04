# Agent Inference Passage Invoke Response v2

Source schema: [`doc/schemas/agent.inference-passage-invoke.response.v2.schema.json`](../../schemas/agent.inference-passage-invoke.response.v2.schema.json)

Successful Agent passage invocation response preserving the exact product and its provider-neutral execution provenance. Refusals use the capability refusal envelope.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-invoke.response.v2` |  |
| [`status`](#field-status) | `yes` | const: `completed` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`product`](#field-product) | `yes` | ref: `agent.inference-passage-product.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-invoke.response.v2`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `completed`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-product"></a>
## `product`

- Required: `yes`
- Shape: ref: `agent.inference-passage-product.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
