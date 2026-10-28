# Assessment-agent-run.v1

Source schema: [`doc/schemas/assessment-agent-run.v1.schema.json`](../../schemas/assessment-agent-run.v1.schema.json)

Closed P026-012b contract. Authority dependencies grant nothing and do not establish inference ancestry.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer.md`](../../project/40-proposals/026-assessment-agent-consumer.md)
- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`agent/ref`](#field-agent-ref) | `yes` | string |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
| [`expected-step`](#field-expected-step) | `yes` | integer |  |
## Field Semantics

<a id="field-agent-ref"></a>
## `agent/ref`

- Required: `yes`
- Shape: string

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string

<a id="field-expected-step"></a>
## `expected-step`

- Required: `yes`
- Shape: integer
