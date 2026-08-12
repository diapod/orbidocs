# Node Extension Posture Evaluation V1

Source schema: [`doc/schemas/node-extension-posture-evaluation.v1.schema.json`](../../schemas/node-extension-posture-evaluation.v1.schema.json)

Prompt-free receiver projection of one admitted peer extension-posture comparison.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `node-extension-posture-evaluation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`node/id`](#field-node-id) | `yes` | string |  |
| [`posture/ref`](#field-posture-ref) | `yes` | string |  |
| [`posture/digest`](#field-posture-digest) | `yes` | string |  |
| [`declaration/ref`](#field-declaration-ref) | `yes` | string |  |
| [`declaration/digest`](#field-declaration-digest) | `yes` | string |  |
| [`peer/profile-digest`](#field-peer-profile-digest) | `yes` | string |  |
| [`local/effective-profile-digest`](#field-local-effective-profile-digest) | `yes` | string |  |
| [`effective/entry-refs`](#field-effective-entry-refs) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `node-extension-posture-evaluation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

<a id="field-posture-ref"></a>
## `posture/ref`

- Required: `yes`
- Shape: string

<a id="field-posture-digest"></a>
## `posture/digest`

- Required: `yes`
- Shape: string

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `yes`
- Shape: string

<a id="field-declaration-digest"></a>
## `declaration/digest`

- Required: `yes`
- Shape: string

<a id="field-peer-profile-digest"></a>
## `peer/profile-digest`

- Required: `yes`
- Shape: string

<a id="field-local-effective-profile-digest"></a>
## `local/effective-profile-digest`

- Required: `yes`
- Shape: string

<a id="field-effective-entry-refs"></a>
## `effective/entry-refs`

- Required: `yes`
- Shape: array
