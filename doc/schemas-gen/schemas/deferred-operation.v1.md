# Deferred Operation v1

Source schema: [`doc/schemas/deferred-operation.v1.schema.json`](../../schemas/deferred-operation.v1.schema.json)

Initial 202 Accepted control payload for an explicitly opted-in deferred operation. This is not domain data; it tells the caller that processing is suspended and may be resumed by polling or a stored continuation.

## Governing Basis

- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `deferred-operation.v1` | Schema tag for the initial deferred operation payload. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`status`](#field-status) | `yes` | const: `deferred` | Initial control status. Callers MUST suspend downstream domain processing instead of treating this payload as ordinary output. |
| [`operation/id`](#field-operation-id) | `yes` | string | Stable id for the deferred operation. Implementations SHOULD derive it deterministically from the operation kind and an idempotency seed when duplicate suppression matters. |
| [`operation/kind`](#field-operation-kind) | `yes` | string | Operation class that owns the continuation semantics, e.g. sensorium.directive.invoke or json-e-flow.step. |
| [`created_at`](#field-created-at) | `yes` | string | RFC 3339 timestamp at which the host accepted the deferred operation. |
| [`retry_after_seconds`](#field-retry-after-seconds) | `yes` | integer | Host-clamped lower bound before the caller or scheduler should poll/resume the operation. It maps to HTTP Retry-After for HTTP surfaces. |
| [`expires_at`](#field-expires-at) | `yes` | string | Host-clamped absolute deadline after which the operation MUST be treated as expired if no terminal result exists. |
| [`status_href`](#field-status-href) | `no` | string | Optional local status endpoint for polling. Omitted when the caller must resume through a stored continuation rather than HTTP polling. |
| [`cancel_href`](#field-cancel-href) | `no` | string | Optional local cancel endpoint. Absence means cancellation is unsupported for this operation kind. |
| [`cancel/unavailable-reason`](#field-cancel-unavailable-reason) | `no` | string | Reason cancellation is not available for this operation. Exactly one of cancel_href or cancel/unavailable-reason MUST be present. |
| [`correlation/id`](#field-correlation-id) | `no` | string | Optional correlation id from the parent flow or workflow. |
| [`audit/outcome-ref`](#field-audit-outcome-ref) | `no` | string | Optional reference to the host/runtime audit outcome that recorded acceptance of this deferred operation. |
| [`continuation`](#field-continuation) | `no` | object | Explicit serializable continuation context. It is a host/runtime value, not a captured language stack. |
| [`diagnostics`](#field-diagnostics) | `no` | array | Optional diagnostics for operator and caller visibility. |
| [`extensions`](#field-extensions) | `no` | object | Open extension map for experimental or deployment-local metadata. Stable protocol fields MUST be promoted to first-class schema properties. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `deferred-operation.v1`

Schema tag for the initial deferred operation payload.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `deferred`

Initial control status. Callers MUST suspend downstream domain processing instead of treating this payload as ordinary output.

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

Stable id for the deferred operation. Implementations SHOULD derive it deterministically from the operation kind and an idempotency seed when duplicate suppression matters.

<a id="field-operation-kind"></a>
## `operation/kind`

- Required: `yes`
- Shape: string

Operation class that owns the continuation semantics, e.g. sensorium.directive.invoke or json-e-flow.step.

<a id="field-created-at"></a>
## `created_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which the host accepted the deferred operation.

<a id="field-retry-after-seconds"></a>
## `retry_after_seconds`

- Required: `yes`
- Shape: integer

Host-clamped lower bound before the caller or scheduler should poll/resume the operation. It maps to HTTP Retry-After for HTTP surfaces.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

Host-clamped absolute deadline after which the operation MUST be treated as expired if no terminal result exists.

<a id="field-status-href"></a>
## `status_href`

- Required: `no`
- Shape: string

Optional local status endpoint for polling. Omitted when the caller must resume through a stored continuation rather than HTTP polling.

<a id="field-cancel-href"></a>
## `cancel_href`

- Required: `no`
- Shape: string

Optional local cancel endpoint. Absence means cancellation is unsupported for this operation kind.

<a id="field-cancel-unavailable-reason"></a>
## `cancel/unavailable-reason`

- Required: `no`
- Shape: string

Reason cancellation is not available for this operation. Exactly one of cancel_href or cancel/unavailable-reason MUST be present.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

Optional correlation id from the parent flow or workflow.

<a id="field-audit-outcome-ref"></a>
## `audit/outcome-ref`

- Required: `no`
- Shape: string

Optional reference to the host/runtime audit outcome that recorded acceptance of this deferred operation.

<a id="field-continuation"></a>
## `continuation`

- Required: `no`
- Shape: object

Explicit serializable continuation context. It is a host/runtime value, not a captured language stack.

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
