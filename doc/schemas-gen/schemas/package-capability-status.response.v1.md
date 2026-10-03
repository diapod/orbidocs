# Package Capability Status Response v1

Source schema: [`doc/schemas/package-capability-status.response.v1.schema.json`](../../schemas/package-capability-status.response.v1.schema.json)

The journal's record of one invocation, or `not-found`, which is no proof that nothing ran (P093 §13).

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-status.response.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `#/$defs/invocation-id` |  |
| [`state`](#field-state) | `yes` | enum: `started`, `completed`, `aborted`, `compensated`, `unknown`, `not-found` |  |
| [`result/status`](#field-result-status) | `no` | enum: `retained`, `unavailable` |  |
| [`output`](#field-output) | `no` | unspecified |  |
| [`output/digest`](#field-output-digest) | `no` | ref: `#/$defs/digest` |  |
| [`cause`](#field-cause) | `no` | enum: `no-outcome`, `output-contract-violation`, `pending-disposal` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`invocation-id`](#def-invocation-id) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "const": "completed"
    }
  },
  "required": [
    "state"
  ]
}
```

Then:

```json
{
  "required": [
    "result/status"
  ],
  "allOf": [
    {
      "not": {
        "anyOf": [
          {
            "required": [
              "cause"
            ]
          }
        ]
      }
    }
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "result/status": {
      "const": "retained"
    }
  },
  "required": [
    "result/status"
  ]
}
```

Then:

```json
{
  "required": [
    "output",
    "output/digest"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "state": {
      "const": "unknown"
    }
  },
  "required": [
    "state"
  ]
}
```

Then:

```json
{
  "required": [
    "cause"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-status.response.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `yes`
- Shape: ref: `#/$defs/invocation-id`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `started`, `completed`, `aborted`, `compensated`, `unknown`, `not-found`

<a id="field-result-status"></a>
## `result/status`

- Required: `no`
- Shape: enum: `retained`, `unavailable`

<a id="field-output"></a>
## `output`

- Required: `no`
- Shape: unspecified

<a id="field-output-digest"></a>
## `output/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-cause"></a>
## `cause`

- Required: `no`
- Shape: enum: `no-outcome`, `output-contract-violation`, `pending-disposal`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-invocation-id"></a>
## `$defs.invocation-id`

- Shape: string
