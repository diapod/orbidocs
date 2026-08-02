# Operator Resource Envelope Revocation v1

Source schema: [`doc/schemas/operator-resource-envelope-revocation.v1.schema.json`](../../schemas/operator-resource-envelope-revocation.v1.schema.json)

Signed immutable operator fact revoking one active resource-envelope revision.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-resource-envelope-revocation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`revocation/id`](#field-revocation-id) | `yes` | string |  |
| [`envelope/ref`](#field-envelope-ref) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`reason`](#field-reason) | `yes` | string |  |
| [`occurred-at`](#field-occurred-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-resource-envelope-revocation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-revocation-id"></a>
## `revocation/id`

- Required: `yes`
- Shape: string

<a id="field-envelope-ref"></a>
## `envelope/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

<a id="field-occurred-at"></a>
## `occurred-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
