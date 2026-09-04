# Agent Outcome v1

Source schema: [`doc/schemas/agent.outcome.v1.schema.json`](../../schemas/agent.outcome.v1.schema.json)

Content-addressed terminal Agent draft produced for its bound domain consumer; it grants neither publication nor effect authority.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.outcome.v1` |  |
| [`outcome/ref`](#field-outcome-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`state`](#field-state) | `yes` | const: `completed` |  |
| [`product/kind`](#field-product-kind) | `yes` | enum: `flow-result`, `assistant-response-draft`, `collaborative-answer-draft`, `collaborative-turn-draft` |  |
| [`product/ref`](#field-product-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`budget_spent`](#field-budget-spent) | `yes` | ref: `agent.inference-passage-product.v1.schema.json#/$defs/budget` |  |
| [`trace/ref`](#field-trace-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`at`](#field-at) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.outcome.v1`

<a id="field-outcome-ref"></a>
## `outcome/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: const: `completed`

<a id="field-product-kind"></a>
## `product/kind`

- Required: `yes`
- Shape: enum: `flow-result`, `assistant-response-draft`, `collaborative-answer-draft`, `collaborative-turn-draft`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-budget-spent"></a>
## `budget_spent`

- Required: `yes`
- Shape: ref: `agent.inference-passage-product.v1.schema.json#/$defs/budget`

<a id="field-trace-ref"></a>
## `trace/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`
