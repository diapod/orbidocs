# Component Communication Observation V1

Source schema: [`doc/schemas/component-communication-observation.v1.schema.json`](../../schemas/component-communication-observation.v1.schema.json)

Host-stamped observation of one registered communication boundary stage.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-communication-observation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`observation/id`](#field-observation-id) | `yes` | ref: `#/$defs/ref` |  |
| [`observation/generation`](#field-observation-generation) | `yes` | ref: `#/$defs/ref` |  |
| [`observation/cursor`](#field-observation-cursor) | `yes` | integer |  |
| [`occurred/at`](#field-occurred-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`observed/at`](#field-observed-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`node/ref`](#field-node-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`boundary/id`](#field-boundary-id) | `yes` | ref: `#/$defs/ref` |  |
| [`boundary/kind`](#field-boundary-kind) | `yes` | enum: `channel-json`, `host-capability`, `middleware-passage`, `peer-session`, `room-carrier`, `http-boundary`, `component-private` |  |
| [`stage`](#field-stage) | `yes` | ref: `#/$defs/stage` |  |
| [`evidence`](#field-evidence) | `yes` | ref: `#/$defs/evidence` |  |
| [`source`](#field-source) | `yes` | ref: `#/$defs/endpoint` |  |
| [`target`](#field-target) | `yes` | ref: `#/$defs/endpoint` |  |
| [`message/ref`](#field-message-ref) | `no` | ref: `#/$defs/ref` |  |
| [`operation`](#field-operation) | `yes` | string |  |
| [`transport/session-ref`](#field-transport-session-ref) | `no` | ref: `#/$defs/ref` |  |
| [`transport/sequence`](#field-transport-sequence) | `no` | integer |  |
| [`causal/context-ref`](#field-causal-context-ref) | `no` | ref: `#/$defs/ref` |  |
| [`causal/context-digest`](#field-causal-context-digest) | `no` | ref: `#/$defs/digest` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`payload`](#field-payload) | `yes` | ref: `#/$defs/payload` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`stage`](#def-stage) | enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled` |  |
| [`endpoint`](#def-endpoint) | object |  |
| [`evidence`](#def-evidence) | unspecified |  |
| [`adapter`](#def-adapter) | enum: `channel-json-session`, `middleware-passage`, `host-capability-dispatch`, `peer-session`, `room-carrier`, `http-boundary`, `component-report` |  |
| [`capture`](#def-capture) | object |  |
| [`payload`](#def-payload) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "transport/sequence"
  ]
}
```

Then:

```json
{
  "required": [
    "transport/session-ref"
  ]
}
```

### Rule 2

When:

```json
{
  "required": [
    "causal/context-ref"
  ]
}
```

Then:

```json
{
  "required": [
    "causal/context-digest"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-communication-observation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-observation-id"></a>
## `observation/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-observation-generation"></a>
## `observation/generation`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-observation-cursor"></a>
## `observation/cursor`

- Required: `yes`
- Shape: integer

<a id="field-occurred-at"></a>
## `occurred/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-boundary-id"></a>
## `boundary/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-boundary-kind"></a>
## `boundary/kind`

- Required: `yes`
- Shape: enum: `channel-json`, `host-capability`, `middleware-passage`, `peer-session`, `room-carrier`, `http-boundary`, `component-private`

<a id="field-stage"></a>
## `stage`

- Required: `yes`
- Shape: ref: `#/$defs/stage`

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: ref: `#/$defs/evidence`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `#/$defs/endpoint`

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: ref: `#/$defs/endpoint`

<a id="field-message-ref"></a>
## `message/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: string

<a id="field-transport-session-ref"></a>
## `transport/session-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-transport-sequence"></a>
## `transport/sequence`

- Required: `no`
- Shape: integer

<a id="field-causal-context-ref"></a>
## `causal/context-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-causal-context-digest"></a>
## `causal/context-digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: ref: `#/$defs/payload`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-stage"></a>
## `$defs.stage`

- Shape: enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled`

<a id="def-endpoint"></a>
## `$defs.endpoint`

- Shape: object

<a id="def-evidence"></a>
## `$defs.evidence`

- Shape: unspecified

<a id="def-adapter"></a>
## `$defs.adapter`

- Shape: enum: `channel-json-session`, `middleware-passage`, `host-capability-dispatch`, `peer-session`, `room-carrier`, `http-boundary`, `component-report`

<a id="def-capture"></a>
## `$defs.capture`

- Shape: object

<a id="def-payload"></a>
## `$defs.payload`

- Shape: object
