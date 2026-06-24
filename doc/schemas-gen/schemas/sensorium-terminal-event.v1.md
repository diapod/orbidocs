# Sensorium Terminal Event v1

Source schema: [`doc/schemas/sensorium-terminal-event.v1.schema.json`](../../schemas/sensorium-terminal-event.v1.schema.json)

Append-only terminal event emitted by a Workbench PTY/session resource.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-terminal-event.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`terminal.session/ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`command/id`](#field-command-id) | `no` | ref: `#/$defs/ref` |  |
| [`event.seq/no`](#field-event-seq-no) | `yes` | integer |  |
| [`event/kind`](#field-event-kind) | `yes` | enum: `stdout`, `stderr`, `status`, `exit`, `signal`, `resize`, `input-accepted`, `input-rejected` |  |
| [`bytes/sha256`](#field-bytes-sha256) | `no` | string |  |
| [`bytes/count`](#field-bytes-count) | `no` | integer |  |
| [`exit/code`](#field-exit-code) | `no` | integer |  |
| [`status`](#field-status) | `no` | enum: `running`, `done`, `failed`, `maybe-hung`, `waiting-for-input`, `no-progress` |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`capture/ref`](#field-capture-ref) | `no` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-terminal-event.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-terminal-session-ref"></a>
## `terminal.session/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-command-id"></a>
## `command/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-event-seq-no"></a>
## `event.seq/no`

- Required: `yes`
- Shape: integer

<a id="field-event-kind"></a>
## `event/kind`

- Required: `yes`
- Shape: enum: `stdout`, `stderr`, `status`, `exit`, `signal`, `resize`, `input-accepted`, `input-rejected`

<a id="field-bytes-sha256"></a>
## `bytes/sha256`

- Required: `no`
- Shape: string

<a id="field-bytes-count"></a>
## `bytes/count`

- Required: `no`
- Shape: integer

<a id="field-exit-code"></a>
## `exit/code`

- Required: `no`
- Shape: integer

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: enum: `running`, `done`, `failed`, `maybe-hung`, `waiting-for-input`, `no-progress`

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-capture-ref"></a>
## `capture/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
