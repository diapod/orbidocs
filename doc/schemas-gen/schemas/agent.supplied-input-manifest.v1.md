# Agent Supplied Input Manifest v1

Source schema: [`doc/schemas/agent.supplied-input-manifest.v1.schema.json`](../../schemas/agent.supplied-input-manifest.v1.schema.json)

Host-authored ordered commitment to exact input material at the Agent execution edge. This is not a citation list, provider-side token trace, model-attention claim or source-access grant.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.supplied-input-manifest.v1` |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`step/no`](#field-step-no) | `yes` | integer |  |
| [`request/ref`](#field-request-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`context/ancestry-complete`](#field-context-ancestry-complete) | `yes` | boolean |  |
| [`inputs`](#field-inputs) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`source`](#def-source) | object |  |
| [`input`](#def-input) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.supplied-input-manifest.v1`

<a id="field-manifest-ref"></a>
## `manifest/ref`

- Required: `yes`
- Shape: string

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

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

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-context-ancestry-complete"></a>
## `context/ancestry-complete`

- Required: `yes`
- Shape: boolean

<a id="field-inputs"></a>
## `inputs`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-source"></a>
## `$defs.source`

- Shape: object

<a id="def-input"></a>
## `$defs.input`

- Shape: object
