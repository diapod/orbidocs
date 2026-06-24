# Sensorium Terminal Input v1

Source schema: [`doc/schemas/sensorium-terminal-input.v1.schema.json`](../../schemas/sensorium-terminal-input.v1.schema.json)

Bounded raw input event to an existing PTY session. Operator-only in the MVP policy.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-terminal-input.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`input/id`](#field-input-id) | `yes` | ref: `#/$defs/ref` |  |
| [`terminal.session/ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`input/kind`](#field-input-kind) | `yes` | enum: `raw-pty-bytes` |  |
| [`bytes/base64`](#field-bytes-base64) | `yes` | string |  |
| [`bytes/sha256`](#field-bytes-sha256) | `yes` | string |  |
| [`operator-only`](#field-operator-only) | `no` | const: `True` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-terminal-input.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-input-id"></a>
## `input/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-terminal-session-ref"></a>
## `terminal.session/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-input-kind"></a>
## `input/kind`

- Required: `yes`
- Shape: enum: `raw-pty-bytes`

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `yes`
- Shape: string

<a id="field-bytes-sha256"></a>
## `bytes/sha256`

- Required: `yes`
- Shape: string

<a id="field-operator-only"></a>
## `operator-only`

- Required: `no`
- Shape: const: `True`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
