# Memarium Host API v1

Source schema: [`doc/schemas/memarium-host-api.v1.schema.json`](../../schemas/memarium-host-api.v1.schema.json)

Stable wire contract for daemon-level memarium.* host capability request and response envelopes. Operations are selected by the endpoint plus the `op` field; clients MUST parse `status` programmatically and MUST NOT parse free-form `reason`.

## Governing Basis

- [`doc/project/40-proposals/036-memarium.md`](../../project/40-proposals/036-memarium.md)
- [`doc/project/40-proposals/047-classification-label-propagation.md`](../../project/40-proposals/047-classification-label-propagation.md)
- [`doc/project/60-solutions/memarium.md`](../../project/60-solutions/memarium.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`OperationEnvelope`](#def-operationenvelope) | object |  |
| [`OkResponse`](#def-okresponse) | object |  |
| [`ErrorResponse`](#def-errorresponse) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-operationenvelope"></a>
## `$defs.OperationEnvelope`

- Shape: object

<a id="def-okresponse"></a>
## `$defs.OkResponse`

- Shape: object

<a id="def-errorresponse"></a>
## `$defs.ErrorResponse`

- Shape: object
