# Corpus Task-pack Executions v1

Source schema: [`doc/schemas/corpus-task-pack-executions.v1.schema.json`](../../schemas/corpus-task-pack-executions.v1.schema.json)

The published task-pack execution records of one Corpus query, as a reader with the current right to read its Room receives them: a current member holding `observe` in an unexpired Room, or the host itself. The host's signature on each record proves origin; it grants no access.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-executions.v1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`executions`](#field-executions) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-executions.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-executions"></a>
## `executions`

- Required: `yes`
- Shape: array
