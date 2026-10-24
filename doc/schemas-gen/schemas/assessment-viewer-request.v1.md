# Assessment-viewer-request.v1

Source schema: [`doc/schemas/assessment-viewer-request.v1.schema.json`](../../schemas/assessment-viewer-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/026-assessment-viewer-grants.md`](../../project/40-proposals/026-assessment-viewer-grants.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`executor/ref`](#field-executor-ref) | `yes` | string |  |
| [`subjects`](#field-subjects) | `yes` | array |  |
| [`ttl/seconds`](#field-ttl-seconds) | `no` | integer |  |
## Field Semantics

<a id="field-executor-ref"></a>
## `executor/ref`

- Required: `yes`
- Shape: string

<a id="field-subjects"></a>
## `subjects`

- Required: `yes`
- Shape: array

<a id="field-ttl-seconds"></a>
## `ttl/seconds`

- Required: `no`
- Shape: integer
