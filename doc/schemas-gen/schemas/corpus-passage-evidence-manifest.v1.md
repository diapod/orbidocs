# Corpus Passage Evidence Manifest v1

Source schema: [`doc/schemas/corpus-passage-evidence-manifest.v1.schema.json`](../../schemas/corpus-passage-evidence-manifest.v1.schema.json)

Immutable, host-made manifest of the evidence one Agent passage reads (P094-023a): the query, Room and reading Room subject, the passage's Corpus inference-Flow binding, each item by exact ref and digest with the execution that names it, its step and source instance, whether it was included, and the projection that rendered them. The rendered content is kept by content address. Required items are always included; an optional item left out names why; nothing is cut. The manifest carries no timestamp, so equal evidence has one address.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-passage-evidence-manifest.v1` |  |
| [`manifest/ref`](#field-manifest-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`reader`](#field-reader) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`inference-flow-binding/ref`](#field-inference-flow-binding-ref) | `yes` | string |  |
| [`projection`](#field-projection) | `yes` | object |  |
| [`bytes/max`](#field-bytes-max) | `yes` | integer |  |
| [`items`](#field-items) | `yes` | array |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`content/ref`](#field-content-ref) | `yes` | string |  |
| [`content/digest`](#field-content-digest) | `yes` | string |  |
| [`content/size-bytes`](#field-content-size-bytes) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-passage-evidence-manifest.v1`

<a id="field-manifest-ref"></a>
## `manifest/ref`

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

<a id="field-reader"></a>
## `reader`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-inference-flow-binding-ref"></a>
## `inference-flow-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-projection"></a>
## `projection`

- Required: `yes`
- Shape: object

<a id="field-bytes-max"></a>
## `bytes/max`

- Required: `yes`
- Shape: integer

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-content-ref"></a>
## `content/ref`

- Required: `yes`
- Shape: string

<a id="field-content-digest"></a>
## `content/digest`

- Required: `yes`
- Shape: string

<a id="field-content-size-bytes"></a>
## `content/size-bytes`

- Required: `yes`
- Shape: integer
