# Peer Status v1

Source schema: [`doc/schemas/peer-status.v1.schema.json`](../../schemas/peer-status.v1.schema.json)

Operator-facing local read model for one peer's transport temperature, lifecycle, and quality-governor state.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `peer-status.v1` |  |
| [`node_id`](#field-node-id) | `yes` | string |  |
| [`display_name`](#field-display-name) | `yes` | string \| null |  |
| [`selected_endpoint_url`](#field-selected-endpoint-url) | `yes` | string \| null |  |
| [`temperature`](#field-temperature) | `yes` | enum: `cold`, `warm`, `hot`, `blocked` |  |
| [`lifecycle`](#field-lifecycle) | `yes` | enum: `idle`, `dialing`, `connected`, `cooldown`, `blocked` |  |
| [`quality_status`](#field-quality-status) | `yes` | enum: `healthy`, `degraded`, `capability_limited`, `cooling_down`, `benchlisted`, `blocked` |  |
| [`score`](#field-score) | `yes` | integer |  |
| [`supported_capabilities`](#field-supported-capabilities) | `yes` | array |  |
| [`missing_capabilities`](#field-missing-capabilities) | `yes` | array |  |
| [`capability_missing_count`](#field-capability-missing-count) | `yes` | integer |  |
| [`failure_count`](#field-failure-count) | `yes` | integer |  |
| [`replay_incidents`](#field-replay-incidents) | `yes` | integer |  |
| [`cooldown_remaining_ms`](#field-cooldown-remaining-ms) | `yes` | integer \| null |  |
| [`blocked_remaining_ms`](#field-blocked-remaining-ms) | `yes` | integer \| null |  |
| [`last_failure_reason`](#field-last-failure-reason) | `yes` | string \| null |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `peer-status.v1`

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

<a id="field-display-name"></a>
## `display_name`

- Required: `yes`
- Shape: string | null

<a id="field-selected-endpoint-url"></a>
## `selected_endpoint_url`

- Required: `yes`
- Shape: string | null

<a id="field-temperature"></a>
## `temperature`

- Required: `yes`
- Shape: enum: `cold`, `warm`, `hot`, `blocked`

<a id="field-lifecycle"></a>
## `lifecycle`

- Required: `yes`
- Shape: enum: `idle`, `dialing`, `connected`, `cooldown`, `blocked`

<a id="field-quality-status"></a>
## `quality_status`

- Required: `yes`
- Shape: enum: `healthy`, `degraded`, `capability_limited`, `cooling_down`, `benchlisted`, `blocked`

<a id="field-score"></a>
## `score`

- Required: `yes`
- Shape: integer

<a id="field-supported-capabilities"></a>
## `supported_capabilities`

- Required: `yes`
- Shape: array

<a id="field-missing-capabilities"></a>
## `missing_capabilities`

- Required: `yes`
- Shape: array

<a id="field-capability-missing-count"></a>
## `capability_missing_count`

- Required: `yes`
- Shape: integer

<a id="field-failure-count"></a>
## `failure_count`

- Required: `yes`
- Shape: integer

<a id="field-replay-incidents"></a>
## `replay_incidents`

- Required: `yes`
- Shape: integer

<a id="field-cooldown-remaining-ms"></a>
## `cooldown_remaining_ms`

- Required: `yes`
- Shape: integer | null

<a id="field-blocked-remaining-ms"></a>
## `blocked_remaining_ms`

- Required: `yes`
- Shape: integer | null

<a id="field-last-failure-reason"></a>
## `last_failure_reason`

- Required: `yes`
- Shape: string | null
