# Agent Inference Passage Invoke v1

Source schema: [`doc/schemas/agent.inference-passage-invoke.v1.schema.json`](../../schemas/agent.inference-passage-invoke.v1.schema.json)

Claims one host-local execution slot for an admitted passage, invokes host-scoped Inquirium, and transactionally commits or compensates the host-derived content-addressed product. Concurrent host-local replay cannot invoke the same passage twice; provider-native idempotency remains required beyond the host boundary. The caller cannot supply product metadata.

## Governing Basis

- [`doc/project/40-proposals/049-json-e-flow.md`](../../project/40-proposals/049-json-e-flow.md)
- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-passage-invoke.v1` |  |
| [`input`](#field-input) | `yes` | ref: `agent.inference-passage-input.v1.schema.json` |  |
| [`request`](#field-request) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-passage-invoke.v1`

<a id="field-input"></a>
## `input`

- Required: `yes`
- Shape: ref: `agent.inference-passage-input.v1.schema.json`

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: object
