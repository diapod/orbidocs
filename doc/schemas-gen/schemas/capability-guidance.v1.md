# Local Capability Guidance v1

Source schema: [`doc/schemas/capability-guidance.v1.schema.json`](../../schemas/capability-guidance.v1.schema.json)

Optional lower-trust documentation from an operator-admitted signed local provider, bound to one exact capability contract. Notes describe use, not executable instructions. The host validates structure and provenance, not semantic intent; schema, grants and host policy retain authority.

## Governing Basis

- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-guidance.v1` |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`provider/id`](#field-provider-id) | `yes` | string |  |
| [`contract/ref`](#field-contract-ref) | `yes` | string |  |
| [`contract/digest`](#field-contract-digest) | `yes` | string |  |
| [`description`](#field-description) | `yes` | string |  |
| [`lang`](#field-lang) | `yes` | string |  |
| [`usage/when`](#field-usage-when) | `no` | string |  |
| [`usage/avoid`](#field-usage-avoid) | `no` | string |  |
| [`usage/notes`](#field-usage-notes) | `no` | string |  |
| [`usage/ref`](#field-usage-ref) | `no` | string |  |
| [`examples`](#field-examples) | `no` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-guidance.v1`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-provider-id"></a>
## `provider/id`

- Required: `yes`
- Shape: string

<a id="field-contract-ref"></a>
## `contract/ref`

- Required: `yes`
- Shape: string

<a id="field-contract-digest"></a>
## `contract/digest`

- Required: `yes`
- Shape: string

<a id="field-description"></a>
## `description`

- Required: `yes`
- Shape: string

<a id="field-lang"></a>
## `lang`

- Required: `yes`
- Shape: string

<a id="field-usage-when"></a>
## `usage/when`

- Required: `no`
- Shape: string

<a id="field-usage-avoid"></a>
## `usage/avoid`

- Required: `no`
- Shape: string

<a id="field-usage-notes"></a>
## `usage/notes`

- Required: `no`
- Shape: string

<a id="field-usage-ref"></a>
## `usage/ref`

- Required: `no`
- Shape: string

<a id="field-examples"></a>
## `examples`

- Required: `no`
- Shape: array
