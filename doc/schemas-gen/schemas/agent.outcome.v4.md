# Agent.outcome.v4

Source schema: [`doc/schemas/agent.outcome.v4.schema.json`](../../schemas/agent.outcome.v4.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.outcome.v4` |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`passage/ref`](#field-passage-ref) | `yes` | string |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`product/ref`](#field-product-ref) | `yes` | string |  |
| [`product/digest`](#field-product-digest) | `yes` | string |  |
| [`context/authority-dependencies`](#field-context-authority-dependencies) | `yes` | array |  |
| [`lifecycle/epoch`](#field-lifecycle-epoch) | `yes` | integer |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.outcome.v4`

<a id="field-agent-id"></a>
## `agent/id`

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

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: string

<a id="field-product-digest"></a>
## `product/digest`

- Required: `yes`
- Shape: string

<a id="field-context-authority-dependencies"></a>
## `context/authority-dependencies`

- Required: `yes`
- Shape: array

<a id="field-lifecycle-epoch"></a>
## `lifecycle/epoch`

- Required: `yes`
- Shape: integer

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string
