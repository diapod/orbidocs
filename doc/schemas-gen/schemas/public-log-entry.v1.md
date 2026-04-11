# Public Log Entry v1

Source schema: [`doc/schemas/public-log-entry.v1.schema.json`](../../schemas/public-log-entry.v1.schema.json)

Machine-readable schema for a single public log entry carried inside an `agora-record.v1` envelope when `content/schema = public-log-entry.v1`. Intended for structured, machine-readable event logs that should be publicly citeable (workflow runs, build events, operator announcements, public health checks). Not a replacement for private telemetry or audit trails. The envelope is the sole source of truth for schema identity: this object does NOT carry a `schema` discriminator, because the envelope's `content/schema` field already names the contract.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`](../../project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`event`](#field-event) | `yes` | string | Machine-readable event label. Applications SHOULD namespace labels by subsystem, for example `workflow.fan-out.dispatched`, `build.stage.completed`, `operator.announcement.posted`. |
| [`level`](#field-level) | `no` | enum: `debug`, `info`, `notice`, `warn`, `error`, `critical` | Severity of the log entry. Defaults to `info` when absent. |
| [`message`](#field-message) | `no` | string | Optional human-readable description of the event. Structured attributes belong in `attributes`, not in the message. |
| [`attributes`](#field-attributes) | `no` | object | Optional structured attributes describing the event. Keys SHOULD be stable across a given event label so that consumers can query and aggregate. |
| [`correlation/run-id`](#field-correlation-run-id) | `no` | string | Optional correlation handle grouping multiple log entries under a single logical run (for example a workflow run id). |
| [`correlation/step-id`](#field-correlation-step-id) | `no` | string | Optional correlation handle for a step within a run. |
## Field Semantics

<a id="field-event"></a>
## `event`

- Required: `yes`
- Shape: string

Machine-readable event label. Applications SHOULD namespace labels by subsystem, for example `workflow.fan-out.dispatched`, `build.stage.completed`, `operator.announcement.posted`.

<a id="field-level"></a>
## `level`

- Required: `no`
- Shape: enum: `debug`, `info`, `notice`, `warn`, `error`, `critical`

Severity of the log entry. Defaults to `info` when absent.

<a id="field-message"></a>
## `message`

- Required: `no`
- Shape: string

Optional human-readable description of the event. Structured attributes belong in `attributes`, not in the message.

<a id="field-attributes"></a>
## `attributes`

- Required: `no`
- Shape: object

Optional structured attributes describing the event. Keys SHOULD be stable across a given event label so that consumers can query and aggregate.

<a id="field-correlation-run-id"></a>
## `correlation/run-id`

- Required: `no`
- Shape: string

Optional correlation handle grouping multiple log entries under a single logical run (for example a workflow run id).

<a id="field-correlation-step-id"></a>
## `correlation/step-id`

- Required: `no`
- Shape: string

Optional correlation handle for a step within a run.
