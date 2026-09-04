# Agent Inference Terminal Selection v2

Source schema: [`doc/schemas/agent.inference-terminal-selection.v2.schema.json`](../../schemas/agent.inference-terminal-selection.v2.schema.json)

Compatible successor preserving the selected Agent product's exact provider-neutral execution provenance.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-terminal-selection.v2` |  |
| [`selection`](#field-selection) | `yes` | ref: `agent.inference-terminal-selection.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-terminal-selection.v2`

<a id="field-selection"></a>
## `selection`

- Required: `yes`
- Shape: ref: `agent.inference-terminal-selection.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
