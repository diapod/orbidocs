# Orbiplex Acceptance Topology v1

Source schema: [`doc/schemas/orbiplex-acceptance-topology.v1.schema.json`](../../schemas/orbiplex-acceptance-topology.v1.schema.json)

Reusable infrastructure-only mapping from stable acceptance slots to SSH-controllable physical hosts.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `orbiplex-acceptance-topology.v1` |  |
| [`topology/ref`](#field-topology-ref) | `yes` | string |  |
| [`topology/revision`](#field-topology-revision) | `yes` | integer |  |
| [`topology/host-posture`](#field-topology-host-posture) | `no` | enum: `distinct-physical-hosts`, `shared-physical-hosts` |  |
| [`nodes`](#field-nodes) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`host`](#def-host) | string |  |
| [`token`](#def-token) | string |  |
| [`node`](#def-node) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `orbiplex-acceptance-topology.v1`

<a id="field-topology-ref"></a>
## `topology/ref`

- Required: `yes`
- Shape: string

<a id="field-topology-revision"></a>
## `topology/revision`

- Required: `yes`
- Shape: integer

<a id="field-topology-host-posture"></a>
## `topology/host-posture`

- Required: `no`
- Shape: enum: `distinct-physical-hosts`, `shared-physical-hosts`

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-host"></a>
## `$defs.host`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-node"></a>
## `$defs.node`

- Shape: object
