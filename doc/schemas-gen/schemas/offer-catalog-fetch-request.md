# Offer Catalog Fetch Request

Source schema: [`doc/schemas/offer-catalog-fetch-request.schema.json`](../../schemas/offer-catalog-fetch-request.schema.json)

Peer message payload carried by `offer-catalog.fetch.request`.

## Governing Basis

- [`doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`](../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md)
- [`doc/project/40-proposals/027-middleware-peer-message-dispatch.md`](../../project/40-proposals/027-middleware-peer-message-dispatch.md)
- [`doc/project/60-solutions/000-node/000-node.md`](../../project/60-solutions/000-node/000-node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`filter`](#field-filter) | `no` | object | Optional responder-side filter hint. |
| [`query_id`](#field-query-id) | `no` | string | Optional initiator-generated correlation id echoed back in the response. |
## Field Semantics

<a id="field-filter"></a>
## `filter`

- Required: `no`
- Shape: object

Optional responder-side filter hint.

<a id="field-query-id"></a>
## `query_id`

- Required: `no`
- Shape: string

Optional initiator-generated correlation id echoed back in the response.
