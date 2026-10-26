# Assessment-agent-request.v1

Source schema: [`doc/schemas/assessment-agent-request.v1.schema.json`](../../schemas/assessment-agent-request.v1.schema.json)

Closed P026-012b contract. Authority dependencies grant nothing and do not establish inference ancestry.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer.md`](../../project/40-proposals/026-assessment-agent-consumer.md)
- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`source/approval-ref`](#field-source-approval-ref) | `yes` | string |  |
| [`subject`](#field-subject) | `yes` | object |  |
| [`runtime/ref`](#field-runtime-ref) | `no` | string |  |
## Field Semantics

<a id="field-source-approval-ref"></a>
## `source/approval-ref`

- Required: `yes`
- Shape: string

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: object

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `no`
- Shape: string
