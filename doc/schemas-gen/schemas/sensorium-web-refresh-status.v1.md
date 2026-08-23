# Sensorium Web Refresh Status v1

Source schema: [`doc/schemas/sensorium-web-refresh-status.v1.schema.json`](../../schemas/sensorium-web-refresh-status.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-refresh-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`operation/id`](#field-operation-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source/ref`](#field-source-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`status`](#field-status) | `yes` | enum: `pending`, `running`, `terminal` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `pending`, `changed`, `no-change`, `refused`, `failed`, `unknown`, `cancelled` |  |
| [`attempt`](#field-attempt) | `yes` | integer |  |
| [`started/at`](#field-started-at) | `yes` | string |  |
| [`completed/at`](#field-completed-at) | `no` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`snapshot/id`](#field-snapshot-id) | `no` | ref: `#/$defs/ref` |  |
| [`snapshot/digest`](#field-snapshot-digest) | `no` | ref: `#/$defs/digest` |  |
| [`observation/id`](#field-observation-id) | `no` | ref: `#/$defs/ref` |  |
| [`failure/code`](#field-failure-code) | `no` | enum: `source-not-found`, `source-superseded`, `refresh-in-progress`, `cache-evidence-missing`, `cache-binding-mismatch`, `broker-unavailable`, `fetch-not-completed`, `extraction-refused`, `observation-rejected`, `storage-failed`, `interrupted`, `cancelled` |  |
| [`retry/class`](#field-retry-class) | `no` | enum: `terminal`, `retryable`, `policy-dependent` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "terminal"
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
  "required": [
    "completed/at"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "changed",
        "no-change"
      ]
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "snapshot/id",
    "snapshot/digest",
    "observation/id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-refresh-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `pending`, `running`, `terminal`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `pending`, `changed`, `no-change`, `refused`, `failed`, `unknown`, `cancelled`

<a id="field-attempt"></a>
## `attempt`

- Required: `yes`
- Shape: integer

<a id="field-started-at"></a>
## `started/at`

- Required: `yes`
- Shape: string

<a id="field-completed-at"></a>
## `completed/at`

- Required: `no`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-snapshot-id"></a>
## `snapshot/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-snapshot-digest"></a>
## `snapshot/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-observation-id"></a>
## `observation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-failure-code"></a>
## `failure/code`

- Required: `no`
- Shape: enum: `source-not-found`, `source-superseded`, `refresh-in-progress`, `cache-evidence-missing`, `cache-binding-mismatch`, `broker-unavailable`, `fetch-not-completed`, `extraction-refused`, `observation-rejected`, `storage-failed`, `interrupted`, `cancelled`

<a id="field-retry-class"></a>
## `retry/class`

- Required: `no`
- Shape: enum: `terminal`, `retryable`, `policy-dependent`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
