# Service Order Result v1

Source schema: [`doc/schemas/service-order-result.v1.schema.json`](../../schemas/service-order-result.v1.schema.json)

Terminal service-order result artifact sent by Dator to Arca through Artifact Delivery. This artifact reports only completed, failed, or rejected outcomes; non-terminal provider progress belongs to a separate future event schema.

## Governing Basis

- [`doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-order.result.v1` |  |
| [`request_id`](#field-request-id) | `yes` | string |  |
| [`workflow/run-id`](#field-workflow-run-id) | `yes` | string |  |
| [`workflow/phase-id`](#field-workflow-phase-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`service_type`](#field-service-type) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `completed`, `failed`, `rejected` |  |
| [`output`](#field-output) | `no` | object \| array \| string \| number \| boolean \| null | Provider output for completed results. Large output may be represented by result/artifact-digest plus AD object-store indirect payload. |
| [`error`](#field-error) | `no` | ref: `#/$defs/error` |  |
| [`provider/node-id`](#field-provider-node-id) | `yes` | string |  |
| [`provider/participant-id`](#field-provider-participant-id) | `yes` | string |  |
| [`provider/metadata`](#field-provider-metadata) | `no` | object |  |
| [`settlement/refs`](#field-settlement-refs) | `no` | array |  |
| [`receipt/ref`](#field-receipt-ref) | `no` | string |  |
| [`hold/ref`](#field-hold-ref) | `no` | string |  |
| [`result/artifact-digest`](#field-result-artifact-digest) | `no` | string |  |
| [`responded_at`](#field-responded-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`error`](#def-error) | object |  |

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
    "output"
  ],
  "not": {
    "required": [
      "error"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "failed",
        "rejected"
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
  "required": [
    "error"
  ],
  "not": {
    "required": [
      "output"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-order.result.v1`

<a id="field-request-id"></a>
## `request_id`

- Required: `yes`
- Shape: string

<a id="field-workflow-run-id"></a>
## `workflow/run-id`

- Required: `yes`
- Shape: string

<a id="field-workflow-phase-id"></a>
## `workflow/phase-id`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `yes`
- Shape: string

<a id="field-service-type"></a>
## `service_type`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `completed`, `failed`, `rejected`

<a id="field-output"></a>
## `output`

- Required: `no`
- Shape: object | array | string | number | boolean | null

Provider output for completed results. Large output may be represented by result/artifact-digest plus AD object-store indirect payload.

<a id="field-error"></a>
## `error`

- Required: `no`
- Shape: ref: `#/$defs/error`

<a id="field-provider-node-id"></a>
## `provider/node-id`

- Required: `yes`
- Shape: string

<a id="field-provider-participant-id"></a>
## `provider/participant-id`

- Required: `yes`
- Shape: string

<a id="field-provider-metadata"></a>
## `provider/metadata`

- Required: `no`
- Shape: object

<a id="field-settlement-refs"></a>
## `settlement/refs`

- Required: `no`
- Shape: array

<a id="field-receipt-ref"></a>
## `receipt/ref`

- Required: `no`
- Shape: string

<a id="field-hold-ref"></a>
## `hold/ref`

- Required: `no`
- Shape: string

<a id="field-result-artifact-digest"></a>
## `result/artifact-digest`

- Required: `no`
- Shape: string

<a id="field-responded-at"></a>
## `responded_at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-error"></a>
## `$defs.error`

- Shape: object
