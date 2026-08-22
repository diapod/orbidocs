# Component Trace Session V1

Source schema: [`doc/schemas/component-trace-session.v1.schema.json`](../../schemas/component-trace-session.v1.schema.json)

Host capture-session lifecycle and bounded counters.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-session.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`session/ref`](#field-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`node/ref`](#field-node-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`observation/generation`](#field-observation-generation) | `yes` | ref: `#/$defs/ref` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`policy/digest`](#field-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`status`](#field-status) | `yes` | enum: `disabled`, `active`, `stopping`, `closed`, `expired`, `revoked`, `interrupted`, `failed` |  |
| [`started/at`](#field-started-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`expires/at`](#field-expires-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`start/cursor`](#field-start-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`start/resume-token`](#field-start-resume-token) | `yes` | string |  |
| [`final/cursor`](#field-final-cursor) | `no` | ref: `#/$defs/cursor` |  |
| [`final/resume-token`](#field-final-resume-token) | `no` | string |  |
| [`observations/accepted`](#field-observations-accepted) | `yes` | ref: `#/$defs/cursor` |  |
| [`observations/dropped`](#field-observations-dropped) | `yes` | ref: `#/$defs/cursor` |  |
| [`gaps/emitted`](#field-gaps-emitted) | `yes` | ref: `#/$defs/cursor` |  |
| [`terminal/reason-code`](#field-terminal-reason-code) | `no` | ref: `#/$defs/ref` |  |
| [`links`](#field-links) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`cursor`](#def-cursor) | integer |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "final/cursor"
  ]
}
```

Then:

```json
{
  "required": [
    "final/resume-token"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "disabled",
        "active",
        "stopping"
      ]
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "terminal/reason-code"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-session.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-session-ref"></a>
## `session/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-observation-generation"></a>
## `observation/generation`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `disabled`, `active`, `stopping`, `closed`, `expired`, `revoked`, `interrupted`, `failed`

<a id="field-started-at"></a>
## `started/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-start-cursor"></a>
## `start/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-start-resume-token"></a>
## `start/resume-token`

- Required: `yes`
- Shape: string

<a id="field-final-cursor"></a>
## `final/cursor`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-final-resume-token"></a>
## `final/resume-token`

- Required: `no`
- Shape: string

<a id="field-observations-accepted"></a>
## `observations/accepted`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-observations-dropped"></a>
## `observations/dropped`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-gaps-emitted"></a>
## `gaps/emitted`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-terminal-reason-code"></a>
## `terminal/reason-code`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-links"></a>
## `links`

- Required: `yes`
- Shape: object

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

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: integer
