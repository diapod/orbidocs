# Offer Catalog Status Response v1

Source schema: [`doc/schemas/offer-catalog-status-response.v1.schema.json`](../../schemas/offer-catalog-status-response.v1.schema.json)

Shared replay/status response for offer-catalog middleware surfaces.

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
| [`schema`](#field-schema) | `yes` | string |  |
| [`enabled`](#field-enabled) | `yes` | boolean |  |
| [`source_mode`](#field-source-mode) | `no` | string |  |
| [`base_url`](#field-base-url) | `no` | string |  |
| [`topic_key`](#field-topic-key) | `no` | string |  |
| [`record_kind`](#field-record-kind) | `no` | string |  |
| [`limit`](#field-limit) | `no` | integer |  |
| [`trust_level`](#field-trust-level) | `no` | string |  |
| [`cursor`](#field-cursor) | `no` | string \| null |  |
| [`last_replay_started_at`](#field-last-replay-started-at) | `no` | string \| null |  |
| [`last_replay_finished_at`](#field-last-replay-finished-at) | `no` | string \| null |  |
| [`last_error`](#field-last-error) | `no` | string \| null |  |
| [`records_seen`](#field-records-seen) | `no` | integer |  |
| [`records_applied`](#field-records-applied) | `no` | integer |  |
| [`records_skipped`](#field-records-skipped) | `no` | integer |  |
| [`cursor_pruned_at`](#field-cursor-pruned-at) | `no` | string \| null |  |
| [`last_query_attestation`](#field-last-query-attestation) | `no` | object \| null |  |
| [`updated_at`](#field-updated-at) | `no` | string \| null |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: string

<a id="field-enabled"></a>
## `enabled`

- Required: `yes`
- Shape: boolean

<a id="field-source-mode"></a>
## `source_mode`

- Required: `no`
- Shape: string

<a id="field-base-url"></a>
## `base_url`

- Required: `no`
- Shape: string

<a id="field-topic-key"></a>
## `topic_key`

- Required: `no`
- Shape: string

<a id="field-record-kind"></a>
## `record_kind`

- Required: `no`
- Shape: string

<a id="field-limit"></a>
## `limit`

- Required: `no`
- Shape: integer

<a id="field-trust-level"></a>
## `trust_level`

- Required: `no`
- Shape: string

<a id="field-cursor"></a>
## `cursor`

- Required: `no`
- Shape: string | null

<a id="field-last-replay-started-at"></a>
## `last_replay_started_at`

- Required: `no`
- Shape: string | null

<a id="field-last-replay-finished-at"></a>
## `last_replay_finished_at`

- Required: `no`
- Shape: string | null

<a id="field-last-error"></a>
## `last_error`

- Required: `no`
- Shape: string | null

<a id="field-records-seen"></a>
## `records_seen`

- Required: `no`
- Shape: integer

<a id="field-records-applied"></a>
## `records_applied`

- Required: `no`
- Shape: integer

<a id="field-records-skipped"></a>
## `records_skipped`

- Required: `no`
- Shape: integer

<a id="field-cursor-pruned-at"></a>
## `cursor_pruned_at`

- Required: `no`
- Shape: string | null

<a id="field-last-query-attestation"></a>
## `last_query_attestation`

- Required: `no`
- Shape: object | null

<a id="field-updated-at"></a>
## `updated_at`

- Required: `no`
- Shape: string | null
