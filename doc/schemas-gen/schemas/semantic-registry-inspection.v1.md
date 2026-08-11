# Semantic Registry Inspection v1

Source schema: [`doc/schemas/semantic-registry-inspection.v1.schema.json`](../../schemas/semantic-registry-inspection.v1.schema.json)

Bounded prompt-free read model for one domain-owned registry.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `semantic-registry-inspection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`domain`](#field-domain) | `yes` | ref: `#/$defs/id` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`entries`](#field-entries) | `yes` | array |  |
| [`effective/refs`](#field-effective-refs) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `semantic-registry-inspection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-domain"></a>
## `domain`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

<a id="field-effective-refs"></a>
## `effective/refs`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
