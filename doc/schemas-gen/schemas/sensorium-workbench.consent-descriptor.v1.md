# Sensorium-workbench.consent-descriptor.v1

Source schema: [`doc/schemas/sensorium-workbench.consent-descriptor.v1.schema.json`](../../schemas/sensorium-workbench.consent-descriptor.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench.consent-descriptor.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`reason/code`](#field-reason-code) | `yes` | ref: `#/$defs/token` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`root/ref`](#field-root-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`relative/path`](#field-relative-path) | `yes` | string |  |
| [`argv`](#field-argv) | `yes` | array |  |
| [`profile/ref`](#field-profile-ref) | `no` | ref: `#/$defs/ref` |  |
| [`timeout_ms`](#field-timeout-ms) | `yes` | integer |  |
| [`output/max-bytes`](#field-output-max-bytes) | `yes` | integer |  |
| [`egress`](#field-egress) | `yes` | enum: `none`, `denied` |  |
| [`credential/env`](#field-credential-env) | `yes` | enum: `none`, `denied` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`token`](#def-token) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench.consent-descriptor.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-root-ref"></a>
## `root/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-relative-path"></a>
## `relative/path`

- Required: `yes`
- Shape: string

<a id="field-argv"></a>
## `argv`

- Required: `yes`
- Shape: array

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-timeout-ms"></a>
## `timeout_ms`

- Required: `yes`
- Shape: integer

<a id="field-output-max-bytes"></a>
## `output/max-bytes`

- Required: `yes`
- Shape: integer

<a id="field-egress"></a>
## `egress`

- Required: `yes`
- Shape: enum: `none`, `denied`

<a id="field-credential-env"></a>
## `credential/env`

- Required: `yes`
- Shape: enum: `none`, `denied`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string
