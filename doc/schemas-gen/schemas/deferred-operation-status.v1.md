# Deferred Operation Status v1

Source schema: [`doc/schemas/deferred-operation-status.v1.schema.json`](../../schemas/deferred-operation-status.v1.schema.json)

Status payload for an operation previously accepted as deferred-operation.v1. Pending and running statuses keep the caller suspended; terminal statuses either resume with result or end the continuation.

## Governing Basis

- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `deferred-operation-status.v1` | Schema tag for deferred operation status payloads. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`status`](#field-status) | `yes` | enum: `pending`, `running`, `completed`, `failed`, `timed-out`, `cancelled`, `expired`, `unknown` | Lifecycle status. pending/running suspend processing; completed resumes with result; failed/timed-out/cancelled/expired/unknown are terminal failures unless the parent runtime has an explicit retry policy. |
| [`operation/id`](#field-operation-id) | `yes` | string | Id from the initial deferred-operation.v1 payload. |
| [`operation/kind`](#field-operation-kind) | `yes` | string | Operation class that owns the continuation semantics. |
| [`updated_at`](#field-updated-at) | `yes` | string | RFC 3339 timestamp at which this status was produced. |
| [`retry_after_seconds`](#field-retry-after-seconds) | `no` | integer | Host-clamped lower bound before the next poll/resume attempt. Required by convention for pending/running statuses that are not immediately resumable. |
| [`expires_at`](#field-expires-at) | `no` | string | Current absolute expiry deadline, if still applicable. |
| [`causal/context`](#field-causal-context) | `no` | ref: `causal-context.v1.schema.json` | Optional canonical P081 causal context preserved on status and continuation responses. |
| [`result`](#field-result) | `no` | unspecified | Domain result only for completed status. It MUST be validated by the owning operation kind before downstream use. |
| [`diagnostics`](#field-diagnostics) | `no` | array | Optional diagnostics for operator and caller visibility. |
| [`extensions`](#field-extensions) | `no` | object | Open extension map for experimental or deployment-local metadata. Stable protocol fields MUST be promoted to first-class schema properties. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "completed"
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
    "result"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `deferred-operation-status.v1`

Schema tag for deferred operation status payloads.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `pending`, `running`, `completed`, `failed`, `timed-out`, `cancelled`, `expired`, `unknown`

Lifecycle status. pending/running suspend processing; completed resumes with result; failed/timed-out/cancelled/expired/unknown are terminal failures unless the parent runtime has an explicit retry policy.

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

Id from the initial deferred-operation.v1 payload.

<a id="field-operation-kind"></a>
## `operation/kind`

- Required: `yes`
- Shape: string

Operation class that owns the continuation semantics.

<a id="field-updated-at"></a>
## `updated_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which this status was produced.

<a id="field-retry-after-seconds"></a>
## `retry_after_seconds`

- Required: `no`
- Shape: integer

Host-clamped lower bound before the next poll/resume attempt. Required by convention for pending/running statuses that are not immediately resumable.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `no`
- Shape: string

Current absolute expiry deadline, if still applicable.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `no`
- Shape: ref: `causal-context.v1.schema.json`

Optional canonical P081 causal context preserved on status and continuation responses.

<a id="field-result"></a>
## `result`

- Required: `no`
- Shape: unspecified

Domain result only for completed status. It MUST be validated by the owning operation kind before downstream use.

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

Optional diagnostics for operator and caller visibility.

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: object

Open extension map for experimental or deployment-local metadata. Stable protocol fields MUST be promoted to first-class schema properties.
