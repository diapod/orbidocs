# Package Capability Invocation v1

Source schema: [`doc/schemas/package-capability-invocation.v1.schema.json`](../../schemas/package-capability-invocation.v1.schema.json)

One append-only fact of the host invocation journal (P093 §9, R13). The `started` fact freezes the recovery context: recovery reads it, never the current overlay. Later facts name the same key `(caller, invocation/id)` and the new `event`.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-invocation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`caller`](#field-caller) | `yes` | object |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `#/$defs/invocation-id` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `#/$defs/capability-id` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`deadline`](#field-deadline) | `yes` | ref: `#/$defs/timestamp` |  |
| [`protected-until`](#field-protected-until) | `yes` | ref: `#/$defs/timestamp` |  |
| [`recovery/context`](#field-recovery-context) | `yes` | object |  |
| [`event`](#field-event) | `yes` | enum: `started`, `completed`, `aborted`, `compensated`, `unknown` |  |
| [`result/status`](#field-result-status) | `no` | enum: `retained`, `unavailable` |  |
| [`output/digest`](#field-output-digest) | `no` | ref: `#/$defs/digest` |  |
| [`cause`](#field-cause) | `no` | enum: `no-outcome`, `output-contract-violation`, `pending-disposal` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | ref: `#/$defs/timestamp` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capability-id`](#def-capability-id) | string | A package capability identifier (P093 §2); the host parses it with the one grammar. |
| [`digest`](#def-digest) | string |  |
| [`invocation-id`](#def-invocation-id) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "event": {
      "const": "completed"
    }
  },
  "required": [
    "event"
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
    "event": {
      "const": "unknown"
    }
  },
  "required": [
    "event"
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
- Shape: const: `package-capability-invocation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-caller"></a>
## `caller`

- Required: `yes`
- Shape: object

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `yes`
- Shape: ref: `#/$defs/invocation-id`

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `#/$defs/capability-id`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-deadline"></a>
## `deadline`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-protected-until"></a>
## `protected-until`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-recovery-context"></a>
## `recovery/context`

- Required: `yes`
- Shape: object

<a id="field-event"></a>
## `event`

- Required: `yes`
- Shape: enum: `started`, `completed`, `aborted`, `compensated`, `unknown`

<a id="field-result-status"></a>
## `result/status`

- Required: `no`
- Shape: enum: `retained`, `unavailable`

<a id="field-output-digest"></a>
## `output/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-cause"></a>
## `cause`

- Required: `no`
- Shape: enum: `no-outcome`, `output-contract-violation`, `pending-disposal`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

## Definition Semantics

<a id="def-capability-id"></a>
## `$defs.capability-id`

- Shape: string

A package capability identifier (P093 §2); the host parses it with the one grammar.

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-invocation-id"></a>
## `$defs.invocation-id`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
