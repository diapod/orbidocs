# Sensorium Workbench Patch Stage Result v1

Source schema: [`doc/schemas/sensorium-workbench-patch-stage-result.v1.schema.json`](../../schemas/sensorium-workbench-patch-stage-result.v1.schema.json)

Content-bound receipt for patch bytes staged inside one Workbench guest generation without applying them.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-patch-stage-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`stage/ref`](#field-stage-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`stage/status`](#field-stage-status) | `yes` | const: `staged` |  |
| [`address`](#field-address) | `yes` | object |  |
| [`content/sha256`](#field-content-sha256) | `yes` | string |  |
| [`content/length`](#field-content-length) | `yes` | integer |  |
| [`target/existed`](#field-target-existed) | `yes` | boolean |  |
| [`retention/policy`](#field-retention-policy) | `yes` | const: `environment-state-until-teardown` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-patch-stage-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-stage-ref"></a>
## `stage/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-stage-status"></a>
## `stage/status`

- Required: `yes`
- Shape: const: `staged`

<a id="field-address"></a>
## `address`

- Required: `yes`
- Shape: object

<a id="field-content-sha256"></a>
## `content/sha256`

- Required: `yes`
- Shape: string

<a id="field-content-length"></a>
## `content/length`

- Required: `yes`
- Shape: integer

<a id="field-target-existed"></a>
## `target/existed`

- Required: `yes`
- Shape: boolean

<a id="field-retention-policy"></a>
## `retention/policy`

- Required: `yes`
- Shape: const: `environment-state-until-teardown`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string
