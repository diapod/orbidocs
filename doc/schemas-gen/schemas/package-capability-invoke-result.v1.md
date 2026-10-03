# Package Capability Invoke Result v1

Source schema: [`doc/schemas/package-capability-invoke-result.v1.schema.json`](../../schemas/package-capability-invoke-result.v1.schema.json)

The answer to one invocation (P093 R13). `refused` happens before the admission point and records nothing; every other outcome is the journal's record, and `started` is a read of an in-flight invocation, never permission to dispatch it again. `output/digest` is present only for output the host validated.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`diagnostic`](#field-diagnostic) | `no` | ref: `package-capability-diagnostic.v1.schema.json` |  |
| [`schema`](#field-schema) | `yes` | const: `package-capability-invoke-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `#/$defs/invocation-id` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `refused`, `started`, `completed`, `aborted`, `compensated`, `unknown` |  |
| [`refusal/code`](#field-refusal-code) | `no` | enum: `package-capability/stale-request`, `package-capability/out-of-scope`, `package-capability/unknown-capability`, `package-capability/scope-commitment-mismatch`, `package-capability/contract-mismatch`, `package-capability/caller-evidence-invalid`, `package-capability/grant-missing`, `package-capability/grant-invalid`, `package-capability/grant-revoked-or-expired`, `package-capability/grant-holder-mismatch`, `package-capability/grant-binding-stale`, `package-capability/grant-voided-by-tombstone`, `package-capability/invocation-id-conflict`, `package-capability/invalid-input`, `package-capability/activation-stale`, `package-capability/provider-unavailable`, `package-capability/capacity-exhausted`, `package-capability/deadline-exceeded` |  |
| [`retryable`](#field-retryable) | `no` | boolean |  |
| [`request/digest`](#field-request-digest) | `no` | ref: `#/$defs/digest` |  |
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
  "required": [
    "diagnostic"
  ]
}
```

Then:

```json
{
  "properties": {
    "outcome": {
      "const": "refused"
    }
  },
  "required": [
    "outcome"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "const": "refused"
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
    "refusal/code",
    "retryable"
  ],
  "allOf": [
    {
      "not": {
        "anyOf": [
          {
            "required": [
              "result/status"
            ]
          },
          {
            "required": [
              "output"
            ]
          },
          {
            "required": [
              "output/digest"
            ]
          },
          {
            "required": [
              "cause"
            ]
          },
          {
            "required": [
              "request/digest"
            ]
          }
        ]
      }
    }
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "const": "completed"
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

### Rule 4

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

### Rule 5

When:

```json
{
  "properties": {
    "outcome": {
      "const": "unknown"
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
    "cause"
  ]
}
```

## Field Semantics

<a id="field-diagnostic"></a>
## `diagnostic`

- Required: `no`
- Shape: ref: `package-capability-diagnostic.v1.schema.json`

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-invoke-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `yes`
- Shape: ref: `#/$defs/invocation-id`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `refused`, `started`, `completed`, `aborted`, `compensated`, `unknown`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `no`
- Shape: enum: `package-capability/stale-request`, `package-capability/out-of-scope`, `package-capability/unknown-capability`, `package-capability/scope-commitment-mismatch`, `package-capability/contract-mismatch`, `package-capability/caller-evidence-invalid`, `package-capability/grant-missing`, `package-capability/grant-invalid`, `package-capability/grant-revoked-or-expired`, `package-capability/grant-holder-mismatch`, `package-capability/grant-binding-stale`, `package-capability/grant-voided-by-tombstone`, `package-capability/invocation-id-conflict`, `package-capability/invalid-input`, `package-capability/activation-stale`, `package-capability/provider-unavailable`, `package-capability/capacity-exhausted`, `package-capability/deadline-exceeded`

<a id="field-retryable"></a>
## `retryable`

- Required: `no`
- Shape: boolean

<a id="field-request-digest"></a>
## `request/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

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
