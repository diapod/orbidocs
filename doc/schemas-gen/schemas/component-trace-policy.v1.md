# Component Trace Policy V1

Source schema: [`doc/schemas/component-trace-policy.v1.schema.json`](../../schemas/component-trace-policy.v1.schema.json)

Bounded effective capture policy for one node process.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-policy.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`policy/digest`](#field-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`profile`](#field-profile) | `yes` | enum: `production`, `development`, `test`, `acceptance`, `operator-debug` | Runtime posture selecting the disabled baseline or an explicit bounded capture context. |
| [`selectors`](#field-selectors) | `yes` | ref: `#/$defs/selectors` |  |
| [`capture/interest`](#field-capture-interest) | `yes` | enum: `none`, `metadata`, `digest`, `redacted`, `content` | Maximum observation detail requested before boundary and secret-policy intersection. |
| [`capture/content`](#field-capture-content) | `yes` | enum: `none`, `inline`, `artifact` |  |
| [`digest/permitted`](#field-digest-permitted) | `yes` | boolean |  |
| [`record/max-bytes`](#field-record-max-bytes) | `yes` | integer |  |
| [`session/max-bytes`](#field-session-max-bytes) | `yes` | integer |  |
| [`session/ttl-seconds`](#field-session-ttl-seconds) | `yes` | integer |  |
| [`hard-secret/classes`](#field-hard-secret-classes) | `yes` | array |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `no` | ref: `#/$defs/ref` |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`reason`](#field-reason) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`selectors`](#def-selectors) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "profile": {
      "const": "production"
    }
  },
  "required": [
    "profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "capture/interest": {
      "const": "none"
    },
    "capture/content": {
      "const": "none"
    },
    "digest/permitted": {
      "const": false
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "operator/binding-ref"
        ]
      },
      {
        "required": [
          "expires/at"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "profile": {
      "const": "operator-debug"
    }
  },
  "required": [
    "profile"
  ]
}
```

Then:

```json
{
  "required": [
    "operator/binding-ref",
    "expires/at"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-policy.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: enum: `production`, `development`, `test`, `acceptance`, `operator-debug`

Runtime posture selecting the disabled baseline or an explicit bounded capture context.

<a id="field-selectors"></a>
## `selectors`

- Required: `yes`
- Shape: ref: `#/$defs/selectors`

<a id="field-capture-interest"></a>
## `capture/interest`

- Required: `yes`
- Shape: enum: `none`, `metadata`, `digest`, `redacted`, `content`

Maximum observation detail requested before boundary and secret-policy intersection.

<a id="field-capture-content"></a>
## `capture/content`

- Required: `yes`
- Shape: enum: `none`, `inline`, `artifact`

<a id="field-digest-permitted"></a>
## `digest/permitted`

- Required: `yes`
- Shape: boolean

<a id="field-record-max-bytes"></a>
## `record/max-bytes`

- Required: `yes`
- Shape: integer

<a id="field-session-max-bytes"></a>
## `session/max-bytes`

- Required: `yes`
- Shape: integer

<a id="field-session-ttl-seconds"></a>
## `session/ttl-seconds`

- Required: `yes`
- Shape: integer

<a id="field-hard-secret-classes"></a>
## `hard-secret/classes`

- Required: `yes`
- Shape: array

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-selectors"></a>
## `$defs.selectors`

- Shape: object
