# Sensorium Terminal Event v1

Source schema: [`doc/schemas/sensorium-terminal-event.v1.schema.json`](../../schemas/sensorium-terminal-event.v1.schema.json)

Bounded append-only terminal event. PTY output carries exact bytes; accepted input never carries input content.

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
| [`command/ref`](#field-command-ref) | `no` | ref: `#/$defs/ref` |  |
| [`event.seq/no`](#field-event-seq-no) | `yes` | integer |  |
| [`event/kind`](#field-event-kind) | `yes` | enum: `output`, `status`, `exit`, `resize`, `input-accepted`, `input-rejected` |  |
| [`bytes/base64`](#field-bytes-base64) | `no` | string |  |
| [`bytes/sha256`](#field-bytes-sha256) | `no` | string |  |
| [`bytes/count`](#field-bytes-count) | `no` | integer |  |
| [`status`](#field-status) | `no` | enum: `open`, `running`, `waiting-for-input`, `completed`, `failed`, `timed-out`, `terminated`, `closed` |  |
| [`exit/code`](#field-exit-code) | `no` | integer |  |
| [`rows`](#field-rows) | `no` | integer |  |
| [`cols`](#field-cols) | `no` | integer |  |
| [`reason/code`](#field-reason-code) | `no` | string |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

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

<a id="field-command-ref"></a>
## `command/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-event-seq-no"></a>
## `event.seq/no`

- Required: `yes`
- Shape: integer

<a id="field-event-kind"></a>
## `event/kind`

- Required: `yes`
- Shape: enum: `output`, `status`, `exit`, `resize`, `input-accepted`, `input-rejected`

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `no`
- Shape: string

<a id="field-bytes-sha256"></a>
## `bytes/sha256`

- Required: `no`
- Shape: string

<a id="field-bytes-count"></a>
## `bytes/count`

- Required: `no`
- Shape: integer

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: enum: `open`, `running`, `waiting-for-input`, `completed`, `failed`, `timed-out`, `terminated`, `closed`

<a id="field-exit-code"></a>
## `exit/code`

- Required: `no`
- Shape: integer

<a id="field-rows"></a>
## `rows`

- Required: `no`
- Shape: integer

<a id="field-cols"></a>
## `cols`

- Required: `no`
- Shape: integer

<a id="field-reason-code"></a>
## `reason/code`

- Required: `no`
- Shape: string

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
