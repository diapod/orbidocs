# Component Communication Report V1

Source schema: [`doc/schemas/component-communication-report.v1.schema.json`](../../schemas/component-communication-report.v1.schema.json)

Bounded component claim submitted through authenticated middleware.trace.report.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-communication-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`report/id`](#field-report-id) | `yes` | ref: `#/$defs/ref` |  |
| [`report/sequence`](#field-report-sequence) | `no` | integer |  |
| [`boundary/id`](#field-boundary-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source`](#field-source) | `yes` | ref: `#/$defs/endpoint` |  |
| [`target`](#field-target) | `yes` | ref: `#/$defs/endpoint` |  |
| [`stage`](#field-stage) | `yes` | enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled` |  |
| [`operation`](#field-operation) | `yes` | string |  |
| [`message/ref`](#field-message-ref) | `no` | ref: `#/$defs/ref` |  |
| [`causal/context-ref`](#field-causal-context-ref) | `no` | ref: `#/$defs/ref` |  |
| [`causal/context-digest`](#field-causal-context-digest) | `no` | ref: `#/$defs/digest` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`occurred/at`](#field-occurred-at) | `yes` | string |  |
| [`payload`](#field-payload) | `yes` | ref: `#/$defs/payload` |  |
| [`reason/code`](#field-reason-code) | `no` | string |  |
| [`retryable`](#field-retryable) | `no` | boolean |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`endpoint`](#def-endpoint) | object |  |
| [`payload`](#def-payload) | object |  |

## Conditional Rules

### Rule 1

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

### Rule 2

When:

```json
{
  "required": [
    "reason/code"
  ]
}
```

Then:

```json
{
  "required": [
    "retryable"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-communication-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-report-id"></a>
## `report/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-report-sequence"></a>
## `report/sequence`

- Required: `no`
- Shape: integer

<a id="field-boundary-id"></a>
## `boundary/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `#/$defs/endpoint`

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: ref: `#/$defs/endpoint`

<a id="field-stage"></a>
## `stage`

- Required: `yes`
- Shape: enum: `egress-admitted`, `egress-failed`, `ingress-admitted`, `ingress-refused`, `completed`, `timed-out`, `canceled`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: string

<a id="field-message-ref"></a>
## `message/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

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

<a id="field-occurred-at"></a>
## `occurred/at`

- Required: `yes`
- Shape: string

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: ref: `#/$defs/payload`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `no`
- Shape: string

<a id="field-retryable"></a>
## `retryable`

- Required: `no`
- Shape: boolean

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-endpoint"></a>
## `$defs.endpoint`

- Shape: object

<a id="def-payload"></a>
## `$defs.payload`

- Shape: object
