# Service Offer v1

Source schema: [`doc/schemas/service-offer.v1.schema.json`](../../schemas/service-offer.v1.schema.json)

Machine-readable schema for one standing exchange-facing service offer published by a provider-side subject. This artifact is catalog-facing and distinct from transport-facing node advertisements. Host-side pricing remains computable through explicit unit semantics rather than through parsing human-readable labels.

## Governing Basis

- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [`doc/project/50-requirements/requirements-012-service-offers-orders.md`](../../project/50-requirements/requirements-012-service-offers-orders.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-012-service-offers-orders.md`](../../project/50-requirements/requirements-012-service-offers-orders.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`signature`](#field-signature) | `yes` | ref: `service-offer-common.v1.schema.json#/$defs/signature` |  |
## Field Semantics

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `service-offer-common.v1.schema.json#/$defs/signature`
