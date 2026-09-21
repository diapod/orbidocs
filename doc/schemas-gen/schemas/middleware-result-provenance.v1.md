# Middleware Result Provenance V1

Source schema: [`doc/schemas/middleware-result-provenance.v1.schema.json`](../../schemas/middleware-result-provenance.v1.schema.json)

Host-owned immutable sidecar binding exact canonical middleware result bytes to inference ancestry. Templates cannot create completeness or authority. The consuming boundary verifies the JCS result digest and descriptor subject; external descriptor resolution is not admitted by this profile.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-result-provenance.v1` |  |
| [`result/ref`](#field-result-ref) | `yes` | string |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-result-provenance.v1`

<a id="field-result-ref"></a>
## `result/ref`

- Required: `yes`
- Shape: string

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
