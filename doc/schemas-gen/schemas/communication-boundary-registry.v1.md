# Communication Boundary Registry V1

Source schema: [`doc/schemas/communication-boundary-registry.v1.schema.json`](../../schemas/communication-boundary-registry.v1.schema.json)

Static startup inventory of observable communication boundaries.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `communication-boundary-registry.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`registry/revision`](#field-registry-revision) | `yes` | ref: `#/$defs/ref` |  |
| [`boundaries`](#field-boundaries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`stage`](#def-stage) | enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled` |  |
| [`endpoint-kind`](#def-endpoint-kind) | enum: `host`, `component`, `middleware-module`, `peer-node`, `room-participant`, `network-service`, `operator` |  |
| [`endpoint-kinds`](#def-endpoint-kinds) | array |  |
| [`stages`](#def-stages) | array |  |
| [`reporting`](#def-reporting) | object |  |
| [`boundary`](#def-boundary) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `communication-boundary-registry.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-registry-revision"></a>
## `registry/revision`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-boundaries"></a>
## `boundaries`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-stage"></a>
## `$defs.stage`

- Shape: enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled`

<a id="def-endpoint-kind"></a>
## `$defs.endpoint-kind`

- Shape: enum: `host`, `component`, `middleware-module`, `peer-node`, `room-participant`, `network-service`, `operator`

<a id="def-endpoint-kinds"></a>
## `$defs.endpoint-kinds`

- Shape: array

<a id="def-stages"></a>
## `$defs.stages`

- Shape: array

<a id="def-reporting"></a>
## `$defs.reporting`

- Shape: object

<a id="def-boundary"></a>
## `$defs.boundary`

- Shape: object
