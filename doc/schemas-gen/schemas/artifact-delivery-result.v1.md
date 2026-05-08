# Artifact Delivery Result v1

Source schema: [`doc/schemas/artifact-delivery-result.v1.schema.json`](../../schemas/artifact-delivery-result.v1.schema.json)

Response returned by the Artifact Delivery host capability after accepting or completing a delivery request.

## Governing Basis

- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-result.v1` |  |
| [`delivery/id`](#field-delivery-id) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent` |  |
| [`failure/class`](#field-failure-class) | `no` | ref: `#/$defs/failureClass` |  |
| [`diagnostic`](#field-diagnostic) | `no` | object \| array \| string \| number \| boolean \| null |  |
| [`stage/results`](#field-stage-results) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`failureClass`](#def-failureclass) | enum: `envelope-malformed`, `envelope-invalid`, `route-unresolved`, `admission-conflict`, `kind-not-supported`, `outbound-denied`, `adapter-transient`, `adapter-permanent`, `stage-timeout`, `admission-timeout`, `ledger-error` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-result.v1`

<a id="field-delivery-id"></a>
## `delivery/id`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`

<a id="field-failure-class"></a>
## `failure/class`

- Required: `no`
- Shape: ref: `#/$defs/failureClass`

<a id="field-diagnostic"></a>
## `diagnostic`

- Required: `no`
- Shape: object | array | string | number | boolean | null

<a id="field-stage-results"></a>
## `stage/results`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-failureclass"></a>
## `$defs.failureClass`

- Shape: enum: `envelope-malformed`, `envelope-invalid`, `route-unresolved`, `admission-conflict`, `kind-not-supported`, `outbound-denied`, `adapter-transient`, `adapter-permanent`, `stage-timeout`, `admission-timeout`, `ledger-error`
