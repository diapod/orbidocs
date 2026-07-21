# Sensorium Virt Recovery Record v1

Source schema: [`doc/schemas/sensorium-virt-recovery-record.v1.schema.json`](../../schemas/sensorium-virt-recovery-record.v1.schema.json)

Host-private durable identity used to recover or quarantine one Sensorium Virt environment.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-recovery-record.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recovery/ref`](#field-recovery-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`image/manifest-digest`](#field-image-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`backend/id`](#field-backend-id) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/version`](#field-backend-version) | `yes` | string |  |
| [`backend/binary-digest`](#field-backend-binary-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`lifecycle/status`](#field-lifecycle-status) | `yes` | enum: `allocating`, `ready`, `draining`, `closed`, `failed`, `expired`, `quarantined` |  |
| [`process`](#field-process) | `no` | object |  |
| [`control-socket`](#field-control-socket) | `no` | object |  |
| [`boot/nonce`](#field-boot-nonce) | `no` | string |  |
| [`working-storage`](#field-working-storage) | `yes` | object |  |
| [`resource/identities`](#field-resource-identities) | `yes` | array |  |
| [`quarantine/reason`](#field-quarantine-reason) | `no` | string |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "lifecycle/status": {
      "const": "quarantined"
    }
  },
  "required": [
    "lifecycle/status"
  ]
}
```

Then:

```json
{
  "required": [
    "quarantine/reason"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-recovery-record.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recovery-ref"></a>
## `recovery/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-image-manifest-digest"></a>
## `image/manifest-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-backend-id"></a>
## `backend/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-version"></a>
## `backend/version`

- Required: `yes`
- Shape: string

<a id="field-backend-binary-digest"></a>
## `backend/binary-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-lifecycle-status"></a>
## `lifecycle/status`

- Required: `yes`
- Shape: enum: `allocating`, `ready`, `draining`, `closed`, `failed`, `expired`, `quarantined`

<a id="field-process"></a>
## `process`

- Required: `no`
- Shape: object

<a id="field-control-socket"></a>
## `control-socket`

- Required: `no`
- Shape: object

<a id="field-boot-nonce"></a>
## `boot/nonce`

- Required: `no`
- Shape: string

<a id="field-working-storage"></a>
## `working-storage`

- Required: `yes`
- Shape: object

<a id="field-resource-identities"></a>
## `resource/identities`

- Required: `yes`
- Shape: array

<a id="field-quarantine-reason"></a>
## `quarantine/reason`

- Required: `no`
- Shape: string

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
