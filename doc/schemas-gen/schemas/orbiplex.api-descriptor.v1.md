# Orbiplex API Descriptor

Source schema: [`doc/schemas/orbiplex.api-descriptor.v1.schema.json`](../../schemas/orbiplex.api-descriptor.v1.schema.json)

Descriptor contributed by a daemon route registry or middleware component for aggregated OpenAPI projection. It is descriptive, not authoritative.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `orbiplex.api-descriptor.v1` |  |
| [`component/id`](#field-component-id) | `yes` | string |  |
| [`base/path`](#field-base-path) | `no` | ref: `#/$defs/pathTemplate` |  |
| [`endpoints`](#field-endpoints) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`endpoint`](#def-endpoint) | object |  |
| [`pathParam`](#def-pathparam) | object |  |
| [`schemaBinding`](#def-schemabinding) | object |  |
| [`pathTemplate`](#def-pathtemplate) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `orbiplex.api-descriptor.v1`

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: string

<a id="field-base-path"></a>
## `base/path`

- Required: `no`
- Shape: ref: `#/$defs/pathTemplate`

<a id="field-endpoints"></a>
## `endpoints`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-endpoint"></a>
## `$defs.endpoint`

- Shape: object

<a id="def-pathparam"></a>
## `$defs.pathParam`

- Shape: object

<a id="def-schemabinding"></a>
## `$defs.schemaBinding`

- Shape: object

<a id="def-pathtemplate"></a>
## `$defs.pathTemplate`

- Shape: string
