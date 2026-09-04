# Agent Inference Passage Trace v2

Source schema: [`doc/schemas/agent.inference-passage-trace.v2.schema.json`](../../schemas/agent.inference-passage-trace.v2.schema.json)

Compatible terminal trace successor preserving product-bound or product-free refusal provenance; admission posture remains a separate contract.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-trace.v2` |  |
| [`trace`](#field-trace) | `yes` | unspecified |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-trace.v2`

<a id="field-trace"></a>
## `trace`

- Required: `yes`
- Shape: unspecified

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
