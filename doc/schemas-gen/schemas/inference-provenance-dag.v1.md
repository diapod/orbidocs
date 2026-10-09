# Bounded Inference Provenance DAG v1

Source schema: [`doc/schemas/inference-provenance-dag.v1.schema.json`](../../schemas/inference-provenance-dag.v1.schema.json)

The exact reachable graph, keyed by SHA-256 of canonical node bytes. Semantic admission verifies root, all edges, hashes, source summaries, reachability, cycles, depth, total edges and canonical byte budget; syntax is not admission or access authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-provenance-dag.v1` |  |
| [`root/digest`](#field-root-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`nodes`](#field-nodes) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`node`](#def-node) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-provenance-dag.v1`

<a id="field-root-digest"></a>
## `root/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-node"></a>
## `$defs.node`

- Shape: object
