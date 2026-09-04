# Inquirium Result Provenance V1

Source schema: [`doc/schemas/inquirium.result-provenance.v1.schema.json`](../../schemas/inquirium.result-provenance.v1.schema.json)

Immutable content-bound sidecar associating one existing Inquirium result with provider-neutral realized inference execution provenance.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.result-provenance.v1` |  |
| [`result/ref`](#field-result-ref) | `yes` | string |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.result-provenance.v1`

<a id="field-result-ref"></a>
## `result/ref`

- Required: `yes`
- Shape: string

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
