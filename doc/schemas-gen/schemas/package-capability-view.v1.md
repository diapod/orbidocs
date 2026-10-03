# Package Capability View V1

Source schema: [`doc/schemas/package-capability-view.v1.schema.json`](../../schemas/package-capability-view.v1.schema.json)

Host-derived, bounded local operator metadata. Never caller authority; no prompts, inputs or outputs.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-view.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | string |  |
| [`package/digest`](#field-package-digest) | `yes` | string |  |
| [`supplies`](#field-supplies) | `yes` | array |  |
| [`activation`](#field-activation) | `yes` | unspecified |  |
| [`diagnostic`](#field-diagnostic) | `yes` | unspecified |  |
| [`uses`](#field-uses) | `yes` | array |  |
| [`uses/omitted`](#field-uses-omitted) | `yes` | integer |  |
| [`invocations`](#field-invocations) | `yes` | array |  |
| [`invocations/omitted`](#field-invocations-omitted) | `yes` | integer |  |
| [`journal/started`](#field-journal-started) | `yes` | integer |  |
| [`journal/unknown`](#field-journal-unknown) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-view.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: string

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: string

<a id="field-supplies"></a>
## `supplies`

- Required: `yes`
- Shape: array

<a id="field-activation"></a>
## `activation`

- Required: `yes`
- Shape: unspecified

<a id="field-diagnostic"></a>
## `diagnostic`

- Required: `yes`
- Shape: unspecified

<a id="field-uses"></a>
## `uses`

- Required: `yes`
- Shape: array

<a id="field-uses-omitted"></a>
## `uses/omitted`

- Required: `yes`
- Shape: integer

<a id="field-invocations"></a>
## `invocations`

- Required: `yes`
- Shape: array

<a id="field-invocations-omitted"></a>
## `invocations/omitted`

- Required: `yes`
- Shape: integer

<a id="field-journal-started"></a>
## `journal/started`

- Required: `yes`
- Shape: integer

<a id="field-journal-unknown"></a>
## `journal/unknown`

- Required: `yes`
- Shape: integer
