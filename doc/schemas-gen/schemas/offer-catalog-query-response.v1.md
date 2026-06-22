# Offer Catalog Query Response v1

Source schema: [`doc/schemas/offer-catalog-query-response.v1.schema.json`](../../schemas/offer-catalog-query-response.v1.schema.json)

Shared response shape for local and shared offer-catalog query endpoints.

## Governing Basis

- [`doc/project/40-proposals/068-api-surface-projection.md`](../../project/40-proposals/068-api-surface-projection.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema_version`](#field-schema-version) | `no` | string |  |
| [`capability_id`](#field-capability-id) | `no` | string |  |
| [`offers`](#field-offers) | `yes` | array |  |
| [`local_offers`](#field-local-offers) | `no` | array |  |
| [`observed_offers`](#field-observed-offers) | `no` | array |  |
| [`counts`](#field-counts) | `no` | object |  |
| [`message`](#field-message) | `no` | string \| null |  |
## Field Semantics

<a id="field-schema-version"></a>
## `schema_version`

- Required: `no`
- Shape: string

<a id="field-capability-id"></a>
## `capability_id`

- Required: `no`
- Shape: string

<a id="field-offers"></a>
## `offers`

- Required: `yes`
- Shape: array

<a id="field-local-offers"></a>
## `local_offers`

- Required: `no`
- Shape: array

<a id="field-observed-offers"></a>
## `observed_offers`

- Required: `no`
- Shape: array

<a id="field-counts"></a>
## `counts`

- Required: `no`
- Shape: object

<a id="field-message"></a>
## `message`

- Required: `no`
- Shape: string | null
