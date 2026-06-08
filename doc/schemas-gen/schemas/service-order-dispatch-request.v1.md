# Service Order Dispatch Request v1

Source schema: [`doc/schemas/service-order-dispatch-request.v1.schema.json`](../../schemas/service-order-dispatch-request.v1.schema.json)

Terminal-provider dispatch artifact sent by Arca to Dator through Artifact Delivery. The artifact carries a P021 service-order.v1 payload plus execution, correlation, reply-routing, and deadline fields. It is a domain artifact, not an AD transport envelope.

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
| [`schema`](#field-schema) | `yes` | const: `service-order.dispatch.request.v1` |  |
| [`request_id`](#field-request-id) | `yes` | string | Buyer-scoped idempotency key for this provider dispatch. |
| [`order`](#field-order) | `yes` | ref: `service-order.v1.schema.json` |  |
| [`dispatch_payload`](#field-dispatch-payload) | `yes` | object | Existing Dator service_dispatch_execute payload shape used by provider-side execution. |
| [`service_type`](#field-service-type) | `yes` | string |  |
| [`request/input`](#field-request-input) | `yes` | object |  |
| [`workflow/run-id`](#field-workflow-run-id) | `yes` | string |  |
| [`workflow/phase-id`](#field-workflow-phase-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`reply/target`](#field-reply-target) | `yes` | ref: `#/$defs/replyTarget` | Privacy-aware AD recipient selector that Dator must use when sending service-order.result.v1 back to Arca. |
| [`reply/delivery_plan`](#field-reply-delivery-plan) | `no` | ref: `#/$defs/deliveryPlan` | Optional privacy-aware AD delivery plan for the service-order.result.v1 reply. When present, Dator must use this complete plan instead of deriving a single-stage plan from reply/target. |
| [`delivery_deadline`](#field-delivery-deadline) | `yes` | string |  |
| [`constraints`](#field-constraints) | `no` | object |  |
| [`order/payment-ref`](#field-order-payment-ref) | `no` | string |  |
| [`settlement/refs`](#field-settlement-refs) | `no` | array |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`replyTarget`](#def-replytarget) | unspecified |  |
| [`deliveryPlan`](#def-deliveryplan) | object |  |
| [`deliverySelector`](#def-deliveryselector) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-order.dispatch.request.v1`

<a id="field-request-id"></a>
## `request_id`

- Required: `yes`
- Shape: string

Buyer-scoped idempotency key for this provider dispatch.

<a id="field-order"></a>
## `order`

- Required: `yes`
- Shape: ref: `service-order.v1.schema.json`

<a id="field-dispatch-payload"></a>
## `dispatch_payload`

- Required: `yes`
- Shape: object

Existing Dator service_dispatch_execute payload shape used by provider-side execution.

<a id="field-service-type"></a>
## `service_type`

- Required: `yes`
- Shape: string

<a id="field-request-input"></a>
## `request/input`

- Required: `yes`
- Shape: object

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

<a id="field-reply-target"></a>
## `reply/target`

- Required: `yes`
- Shape: ref: `#/$defs/replyTarget`

Privacy-aware AD recipient selector that Dator must use when sending service-order.result.v1 back to Arca.

<a id="field-reply-delivery-plan"></a>
## `reply/delivery_plan`

- Required: `no`
- Shape: ref: `#/$defs/deliveryPlan`

Optional privacy-aware AD delivery plan for the service-order.result.v1 reply. When present, Dator must use this complete plan instead of deriving a single-stage plan from reply/target.

<a id="field-delivery-deadline"></a>
## `delivery_deadline`

- Required: `yes`
- Shape: string

<a id="field-constraints"></a>
## `constraints`

- Required: `no`
- Shape: object

<a id="field-order-payment-ref"></a>
## `order/payment-ref`

- Required: `no`
- Shape: string

<a id="field-settlement-refs"></a>
## `settlement/refs`

- Required: `no`
- Shape: array

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-replytarget"></a>
## `$defs.replyTarget`

- Shape: unspecified

<a id="def-deliveryplan"></a>
## `$defs.deliveryPlan`

- Shape: object

<a id="def-deliveryselector"></a>
## `$defs.deliverySelector`

- Shape: unspecified
