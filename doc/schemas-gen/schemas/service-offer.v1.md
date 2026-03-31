# Service Offer v1

Source schema: [`doc/schemas/service-offer.v1.schema.json`](../../schemas/service-offer.v1.schema.json)

Machine-readable schema for one standing exchange-facing service offer published by a provider-side subject. This artifact is catalog-facing and distinct from transport-facing node advertisements. Host-side pricing remains computable through explicit unit semantics rather than through parsing human-readable labels.

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
| [`offer/id`](#field-offer-id) | `yes` | string | Stable identifier of this standing service offer. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the offer record became auditable. |
| [`published-at`](#field-published-at) | `yes` | string | Timestamp when the offer was last published to the exchange-visible channel. |
| [`expires-at`](#field-expires-at) | `yes` | string | Timestamp after which the offer should be treated as stale. |
| [`sequence/no`](#field-sequence-no) | `yes` | integer | Monotonic per-offer sequence number. Higher values supersede lower ones for the same standing offer identity. |
| [`provider/node-id`](#field-provider-node-id) | `yes` | string | Serving node hosting this offer. |
| [`provider/participant-id`](#field-provider-participant-id) | `yes` | string | Provider-side accountable subject publishing this offer. |
| [`service/type`](#field-service-type) | `yes` | string | Marketplace-visible service category such as `text/redaction`, `research/topical`, or `image/generation`. |
| [`service/description`](#field-service-description) | `yes` | string | Human-readable summary of the offered service. |
| [`pricing/amount`](#field-pricing-amount) | `yes` | integer | Price in minor units for one billable unit of service. When `pricing/currency = ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`pricing/currency`](#field-pricing-currency) | `yes` | string | Settlement unit or currency symbol, with `ORC` as the current hard-MVP marketplace unit. |
| [`pricing/unit`](#field-pricing-unit) | `yes` | string | Human-readable billable unit label, for example `1 summary item`, `1800 input characters`, or `1 illustration`. |
| [`pricing/unit-kind`](#field-pricing-unit-kind) | `yes` | enum: `per-item`, `per-character-block`, `per-request`, `flat` | Host-computable pricing kind. The host computes total price and hold from explicit order units multiplied by `pricing/amount`; `pricing/unit` remains descriptive only. |
| [`delivery/max-duration-sec`](#field-delivery-max-duration-sec) | `yes` | integer | Maximum provider-side promised duration for one accepted order under this standing offer. |
| [`queue/auto-accept`](#field-queue-auto-accept) | `yes` | boolean | Whether the provider declares automatic acceptance up to the published queue posture. |
| [`queue/max-depth`](#field-queue-max-depth) | `yes` | integer | Maximum queue depth at which the provider still considers the service admissible. |
| [`queue/current-depth`](#field-queue-current-depth) | `no` | integer | Current queue depth when the offer was published or refreshed. |
| [`constraints/input`](#field-constraints-input) | `no` | object | Optional input-side bounded constraints declared by the provider. |
| [`constraints/output`](#field-constraints-output) | `no` | object | Optional output-side bounded constraints declared by the provider. |
| [`hybrid`](#field-hybrid) | `yes` | boolean | Whether this service involves human intervention beyond pure automated model execution. |
| [`model-first`](#field-model-first) | `no` | boolean | Whether model-backed processing is intended to happen before human intervention when `hybrid` is true. |
| [`confirmation/mode`](#field-confirmation-mode) | `no` | enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only` | Provider-declared preferred confirmation mode intended to map directly into procurement contract confirmation semantics. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional marketplace-local or federation-local annotations that do not redefine the core standing-offer semantics. |
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
    "hybrid": {
      "const": false
    }
  },
  "required": [
    "hybrid"
  ]
}
```

Then:

```json
{
  "properties": {
    "model-first": {
      "const": false
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-offer-id"></a>
## `offer/id`

- Required: `yes`
- Shape: string

Stable identifier of this standing service offer.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the offer record became auditable.

<a id="field-published-at"></a>
## `published-at`

- Required: `yes`
- Shape: string

Timestamp when the offer was last published to the exchange-visible channel.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

Timestamp after which the offer should be treated as stale.

<a id="field-sequence-no"></a>
## `sequence/no`

- Required: `yes`
- Shape: integer

Monotonic per-offer sequence number. Higher values supersede lower ones for the same standing offer identity.

<a id="field-provider-node-id"></a>
## `provider/node-id`

- Required: `yes`
- Shape: string

Serving node hosting this offer.

<a id="field-provider-participant-id"></a>
## `provider/participant-id`

- Required: `yes`
- Shape: string

Provider-side accountable subject publishing this offer.

<a id="field-service-type"></a>
## `service/type`

- Required: `yes`
- Shape: string

Marketplace-visible service category such as `text/redaction`, `research/topical`, or `image/generation`.

<a id="field-service-description"></a>
## `service/description`

- Required: `yes`
- Shape: string

Human-readable summary of the offered service.

<a id="field-pricing-amount"></a>
## `pricing/amount`

- Required: `yes`
- Shape: integer

Price in minor units for one billable unit of service. When `pricing/currency = ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-pricing-currency"></a>
## `pricing/currency`

- Required: `yes`
- Shape: string

Settlement unit or currency symbol, with `ORC` as the current hard-MVP marketplace unit.

<a id="field-pricing-unit"></a>
## `pricing/unit`

- Required: `yes`
- Shape: string

Human-readable billable unit label, for example `1 summary item`, `1800 input characters`, or `1 illustration`.

<a id="field-pricing-unit-kind"></a>
## `pricing/unit-kind`

- Required: `yes`
- Shape: enum: `per-item`, `per-character-block`, `per-request`, `flat`

Host-computable pricing kind. The host computes total price and hold from explicit order units multiplied by `pricing/amount`; `pricing/unit` remains descriptive only.

<a id="field-delivery-max-duration-sec"></a>
## `delivery/max-duration-sec`

- Required: `yes`
- Shape: integer

Maximum provider-side promised duration for one accepted order under this standing offer.

<a id="field-queue-auto-accept"></a>
## `queue/auto-accept`

- Required: `yes`
- Shape: boolean

Whether the provider declares automatic acceptance up to the published queue posture.

<a id="field-queue-max-depth"></a>
## `queue/max-depth`

- Required: `yes`
- Shape: integer

Maximum queue depth at which the provider still considers the service admissible.

<a id="field-queue-current-depth"></a>
## `queue/current-depth`

- Required: `no`
- Shape: integer

Current queue depth when the offer was published or refreshed.

<a id="field-constraints-input"></a>
## `constraints/input`

- Required: `no`
- Shape: object

Optional input-side bounded constraints declared by the provider.

<a id="field-constraints-output"></a>
## `constraints/output`

- Required: `no`
- Shape: object

Optional output-side bounded constraints declared by the provider.

<a id="field-hybrid"></a>
## `hybrid`

- Required: `yes`
- Shape: boolean

Whether this service involves human intervention beyond pure automated model execution.

<a id="field-model-first"></a>
## `model-first`

- Required: `no`
- Shape: boolean

Whether model-backed processing is intended to happen before human intervention when `hybrid` is true.

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `no`
- Shape: enum: `arbiter-confirmed`, `self-confirmed`, `manual-review-only`

Provider-declared preferred confirmation mode intended to map directly into procurement contract confirmation semantics.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional marketplace-local or federation-local annotations that do not redefine the core standing-offer semantics.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
