# Agent.binding.v3

Source schema: [`doc/schemas/agent.binding.v3.schema.json`](../../schemas/agent.binding.v3.schema.json)

Closed P026-012b contract. Authority dependencies grant nothing and do not establish inference ancestry.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer.md`](../../project/40-proposals/026-assessment-agent-consumer.md)
- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.binding.v3` |  |
| [`binding/id`](#field-binding-id) | `yes` | string |  |
| [`agent/ref`](#field-agent-ref) | `yes` | string |  |
| [`consumer/ref`](#field-consumer-ref) | `yes` | string |  |
| [`session-source/ref`](#field-session-source-ref) | `yes` | string |  |
| [`participant/ref`](#field-participant-ref) | `yes` | string |  |
| [`consumer-policy/ref`](#field-consumer-policy-ref) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`at`](#field-at) | `yes` | string |  |
| [`by`](#field-by) | `yes` | string |  |
| [`consumer/kind`](#field-consumer-kind) | `yes` | const: `local-module` |  |
| [`output-sink/kind`](#field-output-sink-kind) | `yes` | const: `module-private-result` |  |
| [`grants`](#field-grants) | `yes` | array |  |
| [`budget`](#field-budget) | `yes` | object |  |
| [`memory-policy`](#field-memory-policy) | `yes` | object |  |
| [`observation-bindings`](#field-observation-bindings) | `yes` | array |  |
| [`consumer-policy/digest`](#field-consumer-policy-digest) | `yes` | string |  |
| [`authority-evidence/refs`](#field-authority-evidence-refs) | `yes` | array |  |
| [`human-in-loop`](#field-human-in-loop) | `yes` | const: `before_effects` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.binding.v3`

<a id="field-binding-id"></a>
## `binding/id`

- Required: `yes`
- Shape: string

<a id="field-agent-ref"></a>
## `agent/ref`

- Required: `yes`
- Shape: string

<a id="field-consumer-ref"></a>
## `consumer/ref`

- Required: `yes`
- Shape: string

<a id="field-session-source-ref"></a>
## `session-source/ref`

- Required: `yes`
- Shape: string

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: string

<a id="field-consumer-policy-ref"></a>
## `consumer-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: string

<a id="field-by"></a>
## `by`

- Required: `yes`
- Shape: string

<a id="field-consumer-kind"></a>
## `consumer/kind`

- Required: `yes`
- Shape: const: `local-module`

<a id="field-output-sink-kind"></a>
## `output-sink/kind`

- Required: `yes`
- Shape: const: `module-private-result`

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

<a id="field-memory-policy"></a>
## `memory-policy`

- Required: `yes`
- Shape: object

<a id="field-observation-bindings"></a>
## `observation-bindings`

- Required: `yes`
- Shape: array

<a id="field-consumer-policy-digest"></a>
## `consumer-policy/digest`

- Required: `yes`
- Shape: string

<a id="field-authority-evidence-refs"></a>
## `authority-evidence/refs`

- Required: `yes`
- Shape: array

<a id="field-human-in-loop"></a>
## `human-in-loop`

- Required: `yes`
- Shape: const: `before_effects`
