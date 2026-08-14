# Federated Inquirium Resource Profile v1

Source schema: [`doc/schemas/inquirium-federated-resource-profile.v1.schema.json`](../../schemas/inquirium-federated-resource-profile.v1.schema.json)

Complete peer resource profile bound by a node-signed federation declaration to one operation, experiment class, and runtime candidate. Sparse profiles are forbidden at this boundary.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium-federated-resource-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`peer/node-id`](#field-peer-node-id) | `yes` | string |  |
| [`envelope/ref`](#field-envelope-ref) | `yes` | string |  |
| [`operation`](#field-operation) | `yes` | enum: `generate`, `embed`, `batch.embed`, `classify`, `rerank`, `summarize`, `transform`, `image.generate`, `image.edit`, `train.adapt` |  |
| [`experiment/class`](#field-experiment-class) | `yes` | enum: `production`, `research`, `experimental`, `critical` |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | string |  |
| [`profile`](#field-profile) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium-federated-resource-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-peer-node-id"></a>
## `peer/node-id`

- Required: `yes`
- Shape: string

<a id="field-envelope-ref"></a>
## `envelope/ref`

- Required: `yes`
- Shape: string

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `generate`, `embed`, `batch.embed`, `classify`, `rerank`, `summarize`, `transform`, `image.generate`, `image.edit`, `train.adapt`

<a id="field-experiment-class"></a>
## `experiment/class`

- Required: `yes`
- Shape: enum: `production`, `research`, `experimental`, `critical`

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `yes`
- Shape: string

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: unspecified
