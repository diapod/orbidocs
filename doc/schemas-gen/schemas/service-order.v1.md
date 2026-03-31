# Service Order v1

Source schema: [`doc/schemas/service-order.v1.schema.json`](../../schemas/service-order.v1.schema.json)

Machine-readable schema for one buyer-facing purchase intent referencing a standing service offer. In hard MVP this artifact is bridged by the host into the current procurement substrate rather than bypassing it. The buyer computes `request/units` explicitly; the host must not infer economic meaning by parsing human-readable pricing labels.

## Governing Basis

- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [`doc/project/50-requirements/requirements-012.md`](../../project/50-requirements/requirements-012.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)
- [`doc/project/50-requirements/requirements-012.md`](../../project/50-requirements/requirements-012.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`order/id`](#field-order-id) | `yes` | string | Stable identifier of this buyer-side service order. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the order became auditable. |
| [`buyer/node-id`](#field-buyer-node-id) | `yes` | string | Node acting as the buyer-side orchestrator for this order. |
| [`buyer/subject-kind`](#field-buyer-subject-kind) | `yes` | enum: `participant`, `org` | Kind of accountable buyer subject that authorizes the order. |
| [`buyer/subject-id`](#field-buyer-subject-id) | `yes` | string | Identifier of the accountable buyer subject. |
| [`buyer/operator-participant-id`](#field-buyer-operator-participant-id) | `no` | string | Optional participant subject operating on behalf of the buyer subject, for example the custodian of an organization purchase. |
| [`provider/node-id`](#field-provider-node-id) | `yes` | string | Provider-side serving node expected to fulfill the order. |
| [`provider/participant-id`](#field-provider-participant-id) | `yes` | string | Provider-side accountable subject expected to stand behind the later procurement execution. |
| [`offer/id`](#field-offer-id) | `yes` | string | Standing service offer selected by the buyer. |
| [`offer/seq`](#field-offer-seq) | `yes` | integer | Standing-offer sequence observed by the buyer when the order was prepared. Hard MVP host bridge MUST reject stale mismatches against the active catalog. |
| [`service/type`](#field-service-type) | `yes` | string | Service category expected by the buyer. The host validates it against the referenced standing offer. |
| [`request/units`](#field-request-units) | `yes` | integer | Requested number of billable units under the referenced standing offer. The buyer computes this quantity explicitly from its own domain input. |
| [`request/input`](#field-request-input) | `yes` | object | Structured buyer-side request input carried into the host-owned bridge. |
| [`request/output-constraints`](#field-request-output-constraints) | `no` | object | Optional buyer-side output expectations narrower than or equal to the referenced standing offer. |
| [`pricing/max-amount`](#field-pricing-max-amount) | `yes` | integer | Maximum total price in minor units the buyer is willing to accept for this order. When `pricing/currency = ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`pricing/currency`](#field-pricing-currency) | `yes` | string | Settlement unit or currency symbol expected by the buyer. |
| [`delivery/requested-by`](#field-delivery-requested-by) | `no` | string | Optional stricter delivery expectation imposed by the buyer. The host must reject values that exceed offer bounds or policy. |
| [`workflow/run-id`](#field-workflow-run-id) | `no` | string | Optional buyer-side workflow run identifier, for example from `Arca`. |
| [`workflow/phase-id`](#field-workflow-phase-id) | `no` | string | Optional buyer-side workflow phase identifier, for example one phase within a recurring orchestration. |
| [`lineage/upstream-refs`](#field-lineage-upstream-refs) | `no` | array | Optional refs to upstream artifacts or prior workflow outputs that justify this purchase. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional buyer-local or federation-local annotations that do not redefine the core purchase semantics. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "buyer/subject-kind": {
      "const": "org"
    }
  },
  "required": [
    "buyer/subject-kind"
  ]
}
```

Then:

```json
{
  "required": [
    "buyer/operator-participant-id"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-order-id"></a>
## `order/id`

- Required: `yes`
- Shape: string

Stable identifier of this buyer-side service order.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the order became auditable.

<a id="field-buyer-node-id"></a>
## `buyer/node-id`

- Required: `yes`
- Shape: string

Node acting as the buyer-side orchestrator for this order.

<a id="field-buyer-subject-kind"></a>
## `buyer/subject-kind`

- Required: `yes`
- Shape: enum: `participant`, `org`

Kind of accountable buyer subject that authorizes the order.

<a id="field-buyer-subject-id"></a>
## `buyer/subject-id`

- Required: `yes`
- Shape: string

Identifier of the accountable buyer subject.

<a id="field-buyer-operator-participant-id"></a>
## `buyer/operator-participant-id`

- Required: `no`
- Shape: string

Optional participant subject operating on behalf of the buyer subject, for example the custodian of an organization purchase.

<a id="field-provider-node-id"></a>
## `provider/node-id`

- Required: `yes`
- Shape: string

Provider-side serving node expected to fulfill the order.

<a id="field-provider-participant-id"></a>
## `provider/participant-id`

- Required: `yes`
- Shape: string

Provider-side accountable subject expected to stand behind the later procurement execution.

<a id="field-offer-id"></a>
## `offer/id`

- Required: `yes`
- Shape: string

Standing service offer selected by the buyer.

<a id="field-offer-seq"></a>
## `offer/seq`

- Required: `yes`
- Shape: integer

Standing-offer sequence observed by the buyer when the order was prepared. Hard MVP host bridge MUST reject stale mismatches against the active catalog.

<a id="field-service-type"></a>
## `service/type`

- Required: `yes`
- Shape: string

Service category expected by the buyer. The host validates it against the referenced standing offer.

<a id="field-request-units"></a>
## `request/units`

- Required: `yes`
- Shape: integer

Requested number of billable units under the referenced standing offer. The buyer computes this quantity explicitly from its own domain input.

<a id="field-request-input"></a>
## `request/input`

- Required: `yes`
- Shape: object

Structured buyer-side request input carried into the host-owned bridge.

<a id="field-request-output-constraints"></a>
## `request/output-constraints`

- Required: `no`
- Shape: object

Optional buyer-side output expectations narrower than or equal to the referenced standing offer.

<a id="field-pricing-max-amount"></a>
## `pricing/max-amount`

- Required: `yes`
- Shape: integer

Maximum total price in minor units the buyer is willing to accept for this order. When `pricing/currency = ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-pricing-currency"></a>
## `pricing/currency`

- Required: `yes`
- Shape: string

Settlement unit or currency symbol expected by the buyer.

<a id="field-delivery-requested-by"></a>
## `delivery/requested-by`

- Required: `no`
- Shape: string

Optional stricter delivery expectation imposed by the buyer. The host must reject values that exceed offer bounds or policy.

<a id="field-workflow-run-id"></a>
## `workflow/run-id`

- Required: `no`
- Shape: string

Optional buyer-side workflow run identifier, for example from `Arca`.

<a id="field-workflow-phase-id"></a>
## `workflow/phase-id`

- Required: `no`
- Shape: string

Optional buyer-side workflow phase identifier, for example one phase within a recurring orchestration.

<a id="field-lineage-upstream-refs"></a>
## `lineage/upstream-refs`

- Required: `no`
- Shape: array

Optional refs to upstream artifacts or prior workflow outputs that justify this purchase.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional buyer-local or federation-local annotations that do not redefine the core purchase semantics.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
