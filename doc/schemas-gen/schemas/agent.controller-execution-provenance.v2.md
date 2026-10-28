# Agent.controller-execution-provenance.v2

Source schema: [`doc/schemas/agent.controller-execution-provenance.v2.schema.json`](../../schemas/agent.controller-execution-provenance.v2.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.controller-execution-provenance.v2` |  |
| [`provenance/ref`](#field-provenance-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`execution-binding/ref`](#field-execution-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`step/no`](#field-step-no) | `yes` | integer |  |
| [`request/ref`](#field-request-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`product/ref`](#field-product-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `yes` | string |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
| [`supplied/input-manifest`](#field-supplied-input-manifest) | `no` | ref: `agent.supplied-input-manifest.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.controller-execution-provenance.v2`

<a id="field-provenance-ref"></a>
## `provenance/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-execution-binding-ref"></a>
## `execution-binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-step-no"></a>
## `step/no`

- Required: `yes`
- Shape: integer

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `yes`
- Shape: string

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`

<a id="field-supplied-input-manifest"></a>
## `supplied/input-manifest`

- Required: `no`
- Shape: ref: `agent.supplied-input-manifest.v1.schema.json`
