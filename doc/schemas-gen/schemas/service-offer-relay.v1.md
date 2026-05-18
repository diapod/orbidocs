# Service Offer Relay v1

Source schema: [`doc/schemas/service-offer-relay.v1.schema.json`](../../schemas/service-offer-relay.v1.schema.json)

Wire envelope for one provider-signed `service-offer.v1` propagated across one offer-catalog relay boundary. The relay metadata is transport-facing; the embedded offer remains the accountable marketplace artifact.

## Governing Basis

- [`doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [`doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`](../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md)
- [`doc/project/60-solutions/000-node/000-node.md`](../../project/60-solutions/000-node/000-node.md)

## Project Lineage

### Requirements

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`relay/id`](#field-relay-id) | `yes` | string | Stable relay-scoped identifier for this propagated offer. |
| [`relay/origin-node-id`](#field-relay-origin-node-id) | `yes` | string | Node that first emitted this relay envelope. |
| [`relay/hops`](#field-relay-hops) | `yes` | integer | Relay hop count. Relays must drop envelopes whose hop count would exceed 3. |
| [`relay/do-not-forward`](#field-relay-do-not-forward) | `no` | boolean | Advisory request asking downstream relays not to forward this envelope further. |
| [`relay/intended-node-id`](#field-relay-intended-node-id) | `no` | string | Optional future-facing hint naming the Node that may relay the offer onward on the publisher's behalf. |
| [`relay/relayed-at`](#field-relay-relayed-at) | `yes` | string | Timestamp of the most recent relay step. |
| [`offer`](#field-offer) | `yes` | ref: `service-offer.v1.schema.json` | Embedded provider-signed standing service offer. |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-relay-id"></a>
## `relay/id`

- Required: `yes`
- Shape: string

Stable relay-scoped identifier for this propagated offer.

<a id="field-relay-origin-node-id"></a>
## `relay/origin-node-id`

- Required: `yes`
- Shape: string

Node that first emitted this relay envelope.

<a id="field-relay-hops"></a>
## `relay/hops`

- Required: `yes`
- Shape: integer

Relay hop count. Relays must drop envelopes whose hop count would exceed 3.

<a id="field-relay-do-not-forward"></a>
## `relay/do-not-forward`

- Required: `no`
- Shape: boolean

Advisory request asking downstream relays not to forward this envelope further.

<a id="field-relay-intended-node-id"></a>
## `relay/intended-node-id`

- Required: `no`
- Shape: string

Optional future-facing hint naming the Node that may relay the offer onward on the publisher's behalf.

<a id="field-relay-relayed-at"></a>
## `relay/relayed-at`

- Required: `yes`
- Shape: string

Timestamp of the most recent relay step.

<a id="field-offer"></a>
## `offer`

- Required: `yes`
- Shape: ref: `service-offer.v1.schema.json`

Embedded provider-signed standing service offer.
