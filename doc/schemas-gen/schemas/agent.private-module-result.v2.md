# Agent.private-module-result.v2

Source schema: [`doc/schemas/agent.private-module-result.v2.schema.json`](../../schemas/agent.private-module-result.v2.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.private-module-result.v2` |  |
| [`agent/ref`](#field-agent-ref) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`passage/ref`](#field-passage-ref) | `yes` | string |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`context/authority-dependencies`](#field-context-authority-dependencies) | `yes` | array |  |
| [`response`](#field-response) | `yes` | object |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.private-module-result.v2`

<a id="field-agent-ref"></a>
## `agent/ref`

- Required: `yes`
- Shape: string

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: string

<a id="field-manifest-ref"></a>
## `manifest/ref`

- Required: `yes`
- Shape: string

<a id="field-context-authority-dependencies"></a>
## `context/authority-dependencies`

- Required: `yes`
- Shape: array

<a id="field-response"></a>
## `response`

- Required: `yes`
- Shape: object

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string
