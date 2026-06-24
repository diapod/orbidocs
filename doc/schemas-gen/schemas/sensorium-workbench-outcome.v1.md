# Sensorium Workbench Outcome v1

Source schema: [`doc/schemas/sensorium-workbench-outcome.v1.schema.json`](../../schemas/sensorium-workbench-outcome.v1.schema.json)

Metadata-only audit fact linking Workbench directives, grants, sessions, waits, artifacts, and terminal status.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-outcome.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`outcome/ref`](#field-outcome-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`directive/ref`](#field-directive-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`grant/ref`](#field-grant-ref) | `no` | ref: `#/$defs/ref` |  |
| [`correlation/id`](#field-correlation-id) | `no` | ref: `#/$defs/ref` |  |
| [`terminal.session/ref`](#field-terminal-session-ref) | `no` | ref: `#/$defs/ref` |  |
| [`environment/ref`](#field-environment-ref) | `no` | ref: `#/$defs/ref` |  |
| [`wait/ref`](#field-wait-ref) | `no` | ref: `#/$defs/ref` |  |
| [`watch/ref`](#field-watch-ref) | `no` | ref: `#/$defs/ref` |  |
| [`probe/ref`](#field-probe-ref) | `no` | ref: `#/$defs/ref` |  |
| [`artifact/refs`](#field-artifact-refs) | `no` | array |  |
| [`status`](#field-status) | `yes` | enum: `completed`, `refused`, `failed`, `timed-out`, `cancelled`, `degraded` |  |
| [`duration_ms`](#field-duration-ms) | `no` | integer |  |
| [`byte_counts`](#field-byte-counts) | `no` | object |  |
| [`diagnostics`](#field-diagnostics) | `no` | array |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-outcome.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-outcome-ref"></a>
## `outcome/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-directive-ref"></a>
## `directive/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-grant-ref"></a>
## `grant/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-terminal-session-ref"></a>
## `terminal.session/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-wait-ref"></a>
## `wait/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-watch-ref"></a>
## `watch/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-probe-ref"></a>
## `probe/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-artifact-refs"></a>
## `artifact/refs`

- Required: `no`
- Shape: array

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `completed`, `refused`, `failed`, `timed-out`, `cancelled`, `degraded`

<a id="field-duration-ms"></a>
## `duration_ms`

- Required: `no`
- Shape: integer

<a id="field-byte-counts"></a>
## `byte_counts`

- Required: `no`
- Shape: object

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
