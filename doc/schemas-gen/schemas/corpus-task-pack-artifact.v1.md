# Corpus Task-pack Artifact v1

Source schema: [`doc/schemas/corpus-task-pack-artifact.v1.schema.json`](../../schemas/corpus-task-pack-artifact.v1.schema.json)

One artifact a published task-pack execution record of the query names (its candidate, result or step evidence), read by its content address under the same right as the records.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-artifact.v1` |  |
| [`artifact/ref`](#field-artifact-ref) | `yes` | string |  |
| [`document`](#field-document) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-artifact.v1`

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `yes`
- Shape: string

<a id="field-document"></a>
## `document`

- Required: `yes`
- Shape: object
