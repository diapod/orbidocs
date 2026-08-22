# Component Trace Record V1

Source schema: [`doc/schemas/component-trace-record.v1.schema.json`](../../schemas/component-trace-record.v1.schema.json)

One independently parseable discriminated JSONL recording line.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-record.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recording/sequence`](#field-recording-sequence) | `yes` | integer |  |
| [`record/kind`](#field-record-kind) | `yes` | enum: `observation`, `gap`, `session`, `policy-transition`, `context-snapshot`, `recovery`, `recorder-diagnostic` |  |
| [`record/value`](#field-record-value) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`policy-transition`](#def-policy-transition) | object |  |
| [`context-snapshot`](#def-context-snapshot) | object |  |
| [`diagnostic`](#def-diagnostic) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "record/kind": {
      "const": "observation"
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "component-communication-observation.v1.schema.json"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "record/kind": {
      "const": "gap"
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "component-trace-gap.v1.schema.json"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "record/kind": {
      "const": "session"
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "component-trace-session.v1.schema.json"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "record/kind": {
      "const": "policy-transition"
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "#/$defs/policy-transition"
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "record/kind": {
      "const": "context-snapshot"
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "#/$defs/context-snapshot"
    }
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "record/kind": {
      "enum": [
        "recovery",
        "recorder-diagnostic"
      ]
    }
  },
  "required": [
    "record/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "record/value": {
      "$ref": "#/$defs/diagnostic"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-record.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recording-sequence"></a>
## `recording/sequence`

- Required: `yes`
- Shape: integer

<a id="field-record-kind"></a>
## `record/kind`

- Required: `yes`
- Shape: enum: `observation`, `gap`, `session`, `policy-transition`, `context-snapshot`, `recovery`, `recorder-diagnostic`

<a id="field-record-value"></a>
## `record/value`

- Required: `yes`
- Shape: unspecified

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

<a id="def-policy-transition"></a>
## `$defs.policy-transition`

- Shape: object

<a id="def-context-snapshot"></a>
## `$defs.context-snapshot`

- Shape: object

<a id="def-diagnostic"></a>
## `$defs.diagnostic`

- Shape: object
