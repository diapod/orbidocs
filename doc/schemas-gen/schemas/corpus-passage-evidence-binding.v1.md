# Corpus Passage Evidence Binding v1

Source schema: [`doc/schemas/corpus-passage-evidence-binding.v1.schema.json`](../../schemas/corpus-passage-evidence-binding.v1.schema.json)

Corpus lineage fact binding one Agent passage to the evidence manifest its prompt was assembled from (P094-023a): the passage, its Agent and Flow bindings, the passage input digest that covers the manifest reference in the request metadata, the query and Room, the manifest by ref and digest, and the digest of the materialized content. It is recorded, create-only, before inference; it does not mean the inference completed.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`agent/input-manifest-ref`](#field-agent-input-manifest-ref) | `yes` | string | Canonical Agent-owned passage input commitment; this Corpus fact adds only domain relations, never a second input list. |
| [`schema`](#field-schema) | `yes` | const: `corpus-passage-evidence-binding.v1` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`agent-flow-binding/ref`](#field-agent-flow-binding-ref) | `yes` | string |  |
| [`inference-flow-binding/ref`](#field-inference-flow-binding-ref) | `yes` | string |  |
| [`input/digest`](#field-input-digest) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`evidence/manifest-ref`](#field-evidence-manifest-ref) | `yes` | string |  |
| [`evidence/manifest-digest`](#field-evidence-manifest-digest) | `yes` | string |  |
| [`materialized/digest`](#field-materialized-digest) | `yes` | string |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
## Field Semantics

<a id="field-agent-input-manifest-ref"></a>
## `agent/input-manifest-ref`

- Required: `yes`
- Shape: string

Canonical Agent-owned passage input commitment; this Corpus fact adds only domain relations, never a second input list.

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-passage-evidence-binding.v1`

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: string

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-agent-flow-binding-ref"></a>
## `agent-flow-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-inference-flow-binding-ref"></a>
## `inference-flow-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-input-digest"></a>
## `input/digest`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-evidence-manifest-ref"></a>
## `evidence/manifest-ref`

- Required: `yes`
- Shape: string

<a id="field-evidence-manifest-digest"></a>
## `evidence/manifest-digest`

- Required: `yes`
- Shape: string

<a id="field-materialized-digest"></a>
## `materialized/digest`

- Required: `yes`
- Shape: string

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string
