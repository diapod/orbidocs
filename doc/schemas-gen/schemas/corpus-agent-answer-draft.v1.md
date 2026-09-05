# Corpus Agent Answer Draft v1

Source schema: [`doc/schemas/corpus-agent-answer-draft.v1.schema.json`](../../schemas/corpus-agent-answer-draft.v1.schema.json)

Inert admitted Agent draft. Publication requires separate host authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-agent-answer-draft.v1` |  |
| [`draft/ref`](#field-draft-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`agent/ref`](#field-agent-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`participant/ref`](#field-participant-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`outcome/ref`](#field-outcome-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`product/ref`](#field-product-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`membership-attestation/ref`](#field-membership-attestation-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`accepted-by`](#field-accepted-by) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`room-event/high-water`](#field-room-event-high-water) | `yes` | integer |  |
| [`publication/authorized`](#field-publication-authorized) | `yes` | const: `False` |  |
| [`accepted-at`](#field-accepted-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-agent-answer-draft.v1`

<a id="field-draft-ref"></a>
## `draft/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-agent-ref"></a>
## `agent/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-outcome-ref"></a>
## `outcome/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-membership-attestation-ref"></a>
## `membership-attestation/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-accepted-by"></a>
## `accepted-by`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-room-event-high-water"></a>
## `room-event/high-water`

- Required: `yes`
- Shape: integer

<a id="field-publication-authorized"></a>
## `publication/authorized`

- Required: `yes`
- Shape: const: `False`

<a id="field-accepted-at"></a>
## `accepted-at`

- Required: `yes`
- Shape: string
