# Artifact Location Advice v1

Source schema: [`doc/schemas/artifact-location-advice.v1.schema.json`](../../schemas/artifact-location-advice.v1.schema.json)

Bounded, non-authoritative location hints for exact or related artifact targets. Advice never creates a source, grants credentials, changes the primary INAC payload location, or authorizes recursive resolution.

## Governing Basis

- [`doc/project/40-proposals/088-pull-based-artifact-acquisition.md`](../../project/40-proposals/088-pull-based-artifact-acquisition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-location-advice.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`advice/items`](#field-advice-items) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`target`](#def-target) | object |  |
| [`selector`](#def-selector) | object |  |
| [`location`](#def-location) | object |  |
| [`item`](#def-item) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-location-advice.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-advice-items"></a>
## `advice/items`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-target"></a>
## `$defs.target`

- Shape: object

<a id="def-selector"></a>
## `$defs.selector`

- Shape: object

<a id="def-location"></a>
## `$defs.location`

- Shape: object

<a id="def-item"></a>
## `$defs.item`

- Shape: object
