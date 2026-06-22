# Artifact Delivery Admission Response v1

Source schema: [`doc/schemas/artifact-delivery-admission-response.v1.schema.json`](../../schemas/artifact-delivery-admission-response.v1.schema.json)

Response returned by an Artifact Delivery acceptor after admission or fail-closed rejection of an artifact.

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
| [`status`](#field-status) | `yes` | enum: `accepted`, `already-present`, `rejected`, `retryable` |  |
| [`acceptor/id`](#field-acceptor-id) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string \| null |  |
| [`artifact/ref`](#field-artifact-ref) | `no` | string |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`diagnostic`](#field-diagnostic) | `no` | object |  |
## Field Semantics

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `already-present`, `rejected`, `retryable`

<a id="field-acceptor-id"></a>
## `acceptor/id`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string | null

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `no`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-diagnostic"></a>
## `diagnostic`

- Required: `no`
- Shape: object
