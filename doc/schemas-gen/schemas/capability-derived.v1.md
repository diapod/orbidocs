# Capability Derived V1

Source schema: [`doc/schemas/capability-derived.v1.schema.json`](../../schemas/capability-derived.v1.schema.json)

Signed local intersection of current base grants. It creates no route, advertisement, passport, or effect authority.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-derived.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`declaration/ref`](#field-declaration-ref) | `yes` | string |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`components`](#field-components) | `yes` | array |  |
| [`restrictions`](#field-restrictions) | `yes` | object |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`ref-list`](#def-ref-list) | array |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-derived.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `yes`
- Shape: string

<a id="field-revision-no"></a>
## `revision/no`

- Required: `yes`
- Shape: integer

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-components"></a>
## `components`

- Required: `yes`
- Shape: array

<a id="field-restrictions"></a>
## `restrictions`

- Required: `yes`
- Shape: object

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-ref-list"></a>
## `$defs.ref-list`

- Shape: array

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
