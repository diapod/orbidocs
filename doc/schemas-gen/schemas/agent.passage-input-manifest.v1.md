# Agent Passage Input Manifest v1

Source schema: [`doc/schemas/agent.passage-input-manifest.v1.schema.json`](../../schemas/agent.passage-input-manifest.v1.schema.json)

Host-owned exact input commitment for one inference-Flow passage. Source assertions share the controller input vocabulary without reinterpreting a passage as a controller step. Request digest and instruction hash bind the admitted request and assembly; ordered supplements bind materialized source bytes. This fact grants no source access and does not prove inference completion or model attention.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.passage-input-manifest.v1` |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`input/digest`](#field-input-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`instruction/hash`](#field-instruction-hash) | `yes` | string |  |
| [`context/ancestry-complete`](#field-context-ancestry-complete) | `yes` | boolean |  |
| [`inputs`](#field-inputs) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`input`](#def-input) | object | Passage source assertion. A referenced carrier grants no resolution authority: the host must resolve and verify exact bytes through its admitted bounded resolver. Controller inputs retain their separate inline-only contract. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.passage-input-manifest.v1`

<a id="field-manifest-ref"></a>
## `manifest/ref`

- Required: `yes`
- Shape: string

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-input-digest"></a>
## `input/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-instruction-hash"></a>
## `instruction/hash`

- Required: `yes`
- Shape: string

<a id="field-context-ancestry-complete"></a>
## `context/ancestry-complete`

- Required: `yes`
- Shape: boolean

<a id="field-inputs"></a>
## `inputs`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-input"></a>
## `$defs.input`

- Shape: object

Passage source assertion. A referenced carrier grants no resolution authority: the host must resolve and verify exact bytes through its admitted bounded resolver. Controller inputs retain their separate inline-only contract.
