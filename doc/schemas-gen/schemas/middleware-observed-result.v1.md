# Middleware Observed Result V1

Source schema: [`doc/schemas/middleware-observed-result.v1.schema.json`](../../schemas/middleware-observed-result.v1.schema.json)

Explicit result representation selected by the caller. The existing result remains unchanged inside result; its content-bound sidecar is mandatory and cannot be stripped on replay. This new carrier does not change any existing response V1 in place.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-observed-result.v1` |  |
| [`result`](#field-result) | `yes` | unspecified |  |
| [`result/provenance`](#field-result-provenance) | `yes` | ref: `middleware-result-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-observed-result.v1`

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: unspecified

<a id="field-result-provenance"></a>
## `result/provenance`

- Required: `yes`
- Shape: ref: `middleware-result-provenance.v1.schema.json`
