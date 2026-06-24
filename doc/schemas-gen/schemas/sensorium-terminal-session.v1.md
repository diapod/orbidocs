# Sensorium Terminal Session v1

Source schema: [`doc/schemas/sensorium-terminal-session.v1.schema.json`](../../schemas/sensorium-terminal-session.v1.schema.json)

Bounded PTY/session descriptor owned by Sensorium Workbench.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-terminal-session.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`terminal.session/ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`command.profile/ref`](#field-command-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`status`](#field-status) | `yes` | enum: `created`, `running`, `idle`, `closing`, `closed`, `failed`, `quarantined` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`caps`](#field-caps) | `yes` | ref: `sensorium-pty-resource-caps.v1.schema.json` |  |
| [`created_at`](#field-created-at) | `no` | string |  |
| [`last_event.seq/no`](#field-last-event-seq-no) | `no` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-terminal-session.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-terminal-session-ref"></a>
## `terminal.session/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-command-profile-ref"></a>
## `command.profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `created`, `running`, `idle`, `closing`, `closed`, `failed`, `quarantined`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-caps"></a>
## `caps`

- Required: `yes`
- Shape: ref: `sensorium-pty-resource-caps.v1.schema.json`

<a id="field-created-at"></a>
## `created_at`

- Required: `no`
- Shape: string

<a id="field-last-event-seq-no"></a>
## `last_event.seq/no`

- Required: `no`
- Shape: integer

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
