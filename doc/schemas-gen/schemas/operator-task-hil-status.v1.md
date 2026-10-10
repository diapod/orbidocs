# Operator Task HIL Status v1

Source schema: [`doc/schemas/operator-task-hil-status.v1.schema.json`](../../schemas/operator-task-hil-status.v1.schema.json)

The requests of one run: pending, decided by a human, expired, or superseded by an exact delegated confirmation for an already admitted step. Supersession is not a human answer. The attention gate never approves.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | unspecified |  |
| [`requests`](#field-requests) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-requests"></a>
## `requests`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
