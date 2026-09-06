# Publish an Admitted Agent Draft With Signed Execution Evidence

Source schema: [`doc/schemas/corpus-agent-answer.publish.request.v2.schema.json`](../../schemas/corpus-agent-answer.publish.request.v2.schema.json)

Explicit V2 representation selection, bound into the publication idempotency digest. Requires retained draft evidence; cannot upgrade a historical V1 publication or confer publication authority on its producer.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-agent-answer.publish.request.v2` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`draft/ref`](#field-draft-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-agent-answer.publish.request.v2`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-draft-ref"></a>
## `draft/ref`

- Required: `yes`
- Shape: string
