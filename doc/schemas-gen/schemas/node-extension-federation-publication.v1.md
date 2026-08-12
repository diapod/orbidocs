# Node Extension Federation Publication V1

Source schema: [`doc/schemas/node-extension-federation-publication.v1.schema.json`](../../schemas/node-extension-federation-publication.v1.schema.json)

Self-contained carrier for independently signed node posture and exact federated envelope declaration.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `node-extension-federation-publication.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`posture`](#field-posture) | `yes` | ref: `node-extension-posture.v1.schema.json` |  |
| [`declaration`](#field-declaration) | `yes` | ref: `federated-envelope-declaration.v2.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `node-extension-federation-publication.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-posture"></a>
## `posture`

- Required: `yes`
- Shape: ref: `node-extension-posture.v1.schema.json`

<a id="field-declaration"></a>
## `declaration`

- Required: `yes`
- Shape: ref: `federated-envelope-declaration.v2.schema.json`
