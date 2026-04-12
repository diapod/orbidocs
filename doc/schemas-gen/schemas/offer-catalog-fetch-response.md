# Offer Catalog Fetch Response

Source schema: [`doc/schemas/offer-catalog-fetch-response.schema.json`](../../schemas/offer-catalog-fetch-response.schema.json)

Peer message payload carried by `offer-catalog.fetch.response`.

## Governing Basis

- [`doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`](../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md)
- [`doc/project/40-proposals/027-middleware-peer-message-dispatch.md`](../../project/40-proposals/027-middleware-peer-message-dispatch.md)
- [`doc/project/60-solutions/node.md`](../../project/60-solutions/node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`offers`](#field-offers) | `no` | array | Zero or more `service-offer-relay.v1` envelopes returned by the responder. |
| [`node_id`](#field-node-id) | `no` | string | Responder Node id. |
| [`responded_at`](#field-responded-at) | `no` | string | RFC 3339 timestamp when the responder produced this payload. |
| [`query_id`](#field-query-id) | `no` | string | Optional correlation id echoed from the request. |
| [`error`](#field-error) | `no` | object \| string \| null | Optional error payload. `null` means the response is successful. |
## Field Semantics

<a id="field-offers"></a>
## `offers`

- Required: `no`
- Shape: array

Zero or more `service-offer-relay.v1` envelopes returned by the responder.

<a id="field-node-id"></a>
## `node_id`

- Required: `no`
- Shape: string

Responder Node id.

<a id="field-responded-at"></a>
## `responded_at`

- Required: `no`
- Shape: string

RFC 3339 timestamp when the responder produced this payload.

<a id="field-query-id"></a>
## `query_id`

- Required: `no`
- Shape: string

Optional correlation id echoed from the request.

<a id="field-error"></a>
## `error`

- Required: `no`
- Shape: object | string | null

Optional error payload. `null` means the response is successful.
