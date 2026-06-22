# Middleware Status Response v1

Source schema: [`doc/schemas/middleware-status-response.v1.schema.json`](../../schemas/middleware-status-response.v1.schema.json)

Shared local HTTP health, readiness, and simple status response returned by supervised middleware services.

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
| [`schema`](#field-schema) | `no` | string |  |
| [`status`](#field-status) | `yes` | string |  |
| [`module_id`](#field-module-id) | `no` | string |  |
| [`module_name`](#field-module-name) | `no` | string |  |
| [`description`](#field-description) | `no` | string |  |
| [`data_dir`](#field-data-dir) | `no` | string \| null |  |
| [`db_path`](#field-db-path) | `no` | string \| null |  |
| [`error`](#field-error) | `no` | string \| null |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `no`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: string

<a id="field-module-id"></a>
## `module_id`

- Required: `no`
- Shape: string

<a id="field-module-name"></a>
## `module_name`

- Required: `no`
- Shape: string

<a id="field-description"></a>
## `description`

- Required: `no`
- Shape: string

<a id="field-data-dir"></a>
## `data_dir`

- Required: `no`
- Shape: string | null

<a id="field-db-path"></a>
## `db_path`

- Required: `no`
- Shape: string | null

<a id="field-error"></a>
## `error`

- Required: `no`
- Shape: string | null
