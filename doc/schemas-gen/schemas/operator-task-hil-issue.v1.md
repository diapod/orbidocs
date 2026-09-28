# Operator Task HIL Issue v1

Source schema: [`doc/schemas/operator-task-hil-issue.v1.schema.json`](../../schemas/operator-task-hil-issue.v1.schema.json)

Request to issue, or find, the HIL requests of one admitted run, for the binding revision it was admitted under. Each request is issued once; only an undelivered request passes the attention gate, so reading requests never prompts the operator again. A concluded run issues no new request.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-issue.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-issue.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: unspecified
