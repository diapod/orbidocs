# Agent.supplied-input-manifest.v3

Source schema: [`doc/schemas/agent.supplied-input-manifest.v3.schema.json`](../../schemas/agent.supplied-input-manifest.v3.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.supplied-input-manifest.v3` |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | string |  |
| [`passage/ref`](#field-passage-ref) | `yes` | string |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`context/authority-dependencies`](#field-context-authority-dependencies) | `yes` | array |  |
| [`inputs`](#field-inputs) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.supplied-input-manifest.v3`

<a id="field-manifest-ref"></a>
## `manifest/ref`

- Required: `yes`
- Shape: string

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: string

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-context-authority-dependencies"></a>
## `context/authority-dependencies`

- Required: `yes`
- Shape: array

<a id="field-inputs"></a>
## `inputs`

- Required: `yes`
- Shape: array
