# Sensorium Workbench Environment v1

Source schema: [`doc/schemas/sensorium-workbench-environment.v1.schema.json`](../../schemas/sensorium-workbench-environment.v1.schema.json)

Workbench environment descriptor for an allowlisted host-local workspace or managed virtual executor.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-environment.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`workspace/ref`](#field-workspace-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend`](#field-backend) | `yes` | enum: `host-local-workspace`, `fixture-virtual-workspace`, `container`, `microvm` |  |
| [`roots`](#field-roots) | `yes` | array |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `remote-sandbox` |  |
| [`egress`](#field-egress) | `no` | enum: `none`, `allowlisted`, `unrestricted` |  |
| [`status`](#field-status) | `yes` | enum: `allocating`, `ready`, `draining`, `closed`, `failed`, `expired` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`limits`](#field-limits) | `no` | object |  |
| [`cleanup/status`](#field-cleanup-status) | `no` | enum: `not-needed`, `pending`, `completed`, `failed`, `quarantined` |  |
| [`executor`](#field-executor) | `yes` | object |  |
| [`teardown/policy`](#field-teardown-policy) | `yes` | enum: `not-applicable`, `delete-managed-copy`, `provider-managed` |  |
| [`artifact/export-policy`](#field-artifact-export-policy) | `yes` | enum: `unsupported`, `explicit` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-environment.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend"></a>
## `backend`

- Required: `yes`
- Shape: enum: `host-local-workspace`, `fixture-virtual-workspace`, `container`, `microvm`

<a id="field-roots"></a>
## `roots`

- Required: `yes`
- Shape: array

<a id="field-locality"></a>
## `locality`

- Required: `yes`
- Shape: enum: `local-only`, `remote-sandbox`

<a id="field-egress"></a>
## `egress`

- Required: `no`
- Shape: enum: `none`, `allowlisted`, `unrestricted`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `allocating`, `ready`, `draining`, `closed`, `failed`, `expired`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-limits"></a>
## `limits`

- Required: `no`
- Shape: object

<a id="field-cleanup-status"></a>
## `cleanup/status`

- Required: `no`
- Shape: enum: `not-needed`, `pending`, `completed`, `failed`, `quarantined`

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: object

<a id="field-teardown-policy"></a>
## `teardown/policy`

- Required: `yes`
- Shape: enum: `not-applicable`, `delete-managed-copy`, `provider-managed`

<a id="field-artifact-export-policy"></a>
## `artifact/export-policy`

- Required: `yes`
- Shape: enum: `unsupported`, `explicit`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
