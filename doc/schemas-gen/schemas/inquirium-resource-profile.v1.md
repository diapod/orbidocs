# Inquirium Resource Profile v1

Source schema: [`doc/schemas/inquirium-resource-profile.v1.schema.json`](../../schemas/inquirium-resource-profile.v1.schema.json)

Closed sparse overlay over the distribution-owned Inquirium operational resource profile. Missing limits inherit; they never mean unbounded. Schema admission declares an axis but does not by itself prove that the current runtime enforces it; enforcement support is operation-specific and must be reported separately.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium-resource-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | string |  |
| [`limits`](#field-limits) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`limit`](#def-limit) | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium-resource-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: string

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-limit"></a>
## `$defs.limit`

- Shape: integer
