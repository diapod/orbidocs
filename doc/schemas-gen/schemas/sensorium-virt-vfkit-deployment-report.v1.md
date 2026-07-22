# Sensorium Virt Vfkit Deployment Report v1

Source schema: [`doc/schemas/sensorium-virt-vfkit-deployment-report.v1.schema.json`](../../schemas/sensorium-virt-vfkit-deployment-report.v1.schema.json)

Closed, metadata-only evidence report for one real vfkit full-system deployment run.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-vfkit-deployment-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`measurements`](#field-measurements) | `yes` | object |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
| [`backend/id`](#field-backend-id) | `yes` | const: `vfkit-system.v1` |  |
| [`backend/binary-digest`](#field-backend-binary-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | const: `macos-vz-arm64.v1` |  |
| [`image/manifest-digest`](#field-image-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`image/manifest-file-digest`](#field-image-manifest-file-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`image/artifact-digest`](#field-image-artifact-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`firmware/digest`](#field-firmware-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`guest-agent/digest`](#field-guest-agent-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-vfkit-deployment-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

<a id="field-checks"></a>
## `checks`

- Required: `yes`
- Shape: array

<a id="field-measurements"></a>
## `measurements`

- Required: `yes`
- Shape: object

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object

<a id="field-backend-id"></a>
## `backend/id`

- Required: `yes`
- Shape: const: `vfkit-system.v1`

<a id="field-backend-binary-digest"></a>
## `backend/binary-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: const: `macos-vz-arm64.v1`

<a id="field-image-manifest-digest"></a>
## `image/manifest-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-image-manifest-file-digest"></a>
## `image/manifest-file-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-image-artifact-digest"></a>
## `image/artifact-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-firmware-digest"></a>
## `firmware/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-guest-agent-digest"></a>
## `guest-agent/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
