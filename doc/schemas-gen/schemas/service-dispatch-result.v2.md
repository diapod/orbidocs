# Service-dispatch-result.v2

Source schema: [`doc/schemas/service-dispatch-result.v2.schema.json`](../../schemas/service-dispatch-result.v2.schema.json)

Data-only producer binding. Source authority remains independent; missing evidence never implies local execution.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-dispatch-result.v2` |  |
| [`result`](#field-result) | `yes` | object | Unchanged role dispatch response. Its admitted role contract is validated independently; this wrapper binds its canonical bytes. |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-dispatch-result.v2`

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: object

Unchanged role dispatch response. Its admitted role contract is validated independently; this wrapper binds its canonical bytes.

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
