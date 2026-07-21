# Sensorium Virt Environment Plan v1

Source schema: [`doc/schemas/sensorium-virt-environment-plan.v1.schema.json`](../../schemas/sensorium-virt-environment-plan.v1.schema.json)

Host-normalized immutable allocation plan for a Sensorium Virt environment.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-environment-plan.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/capabilities-ref`](#field-backend-capabilities-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/capabilities-digest`](#field-backend-capabilities-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`backend/id`](#field-backend-id) | `yes` | ref: `#/$defs/ref` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`image/ref`](#field-image-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`image/variant-ref`](#field-image-variant-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`image/manifest-digest`](#field-image-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `remote-sandbox` |  |
| [`host/architecture`](#field-host-architecture) | `yes` | ref: `#/$defs/architecture` |  |
| [`guest/architecture`](#field-guest-architecture) | `yes` | ref: `#/$defs/architecture` |  |
| [`isolation/class`](#field-isolation-class) | `yes` | enum: `none`, `process-sandbox`, `shared-kernel-container`, `hardware-vm` |  |
| [`system/fidelity`](#field-system-fidelity) | `yes` | enum: `filesystem-view`, `process-runtime`, `shared-kernel-linux`, `full-system-linux` |  |
| [`control`](#field-control) | `yes` | ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/controlSelection` |  |
| [`boot/mode`](#field-boot-mode) | `yes` | enum: `none`, `efi`, `direct-kernel` |  |
| [`storage/format`](#field-storage-format) | `yes` | enum: `directory-copy`, `raw`, `kernel-initrd-rootfs` |  |
| [`device/classes`](#field-device-classes) | `yes` | ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/deviceClasses` |  |
| [`console/mode`](#field-console-mode) | `yes` | enum: `none`, `diagnostic-output-only` |  |
| [`network/profile`](#field-network-profile) | `yes` | enum: `none`, `isolated`, `egress-allowlisted` |  |
| [`host-filesystem-sharing/mode`](#field-host-filesystem-sharing-mode) | `yes` | enum: `denied`, `read-only`, `read-write` |  |
| [`credential-injection/mode`](#field-credential-injection-mode) | `yes` | enum: `denied`, `explicit-scoped` |  |
| [`resource-enforcement/classes`](#field-resource-enforcement-classes) | `yes` | ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/resourceClasses` |  |
| [`lifecycle/operations`](#field-lifecycle-operations) | `yes` | ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/lifecycleOperations` |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`operational/context-candidate-digest`](#field-operational-context-candidate-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`operational/context-policy-ref`](#field-operational-context-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`attached-resource-contexts`](#field-attached-resource-contexts) | `yes` | array |  |
| [`limits`](#field-limits) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`architecture`](#def-architecture) | enum: `x86_64`, `arm64` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-environment-plan.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-capabilities-ref"></a>
## `backend/capabilities-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-capabilities-digest"></a>
## `backend/capabilities-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-backend-id"></a>
## `backend/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-image-ref"></a>
## `image/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-image-variant-ref"></a>
## `image/variant-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-image-manifest-digest"></a>
## `image/manifest-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-locality"></a>
## `locality`

- Required: `yes`
- Shape: enum: `local-only`, `remote-sandbox`

<a id="field-host-architecture"></a>
## `host/architecture`

- Required: `yes`
- Shape: ref: `#/$defs/architecture`

<a id="field-guest-architecture"></a>
## `guest/architecture`

- Required: `yes`
- Shape: ref: `#/$defs/architecture`

<a id="field-isolation-class"></a>
## `isolation/class`

- Required: `yes`
- Shape: enum: `none`, `process-sandbox`, `shared-kernel-container`, `hardware-vm`

<a id="field-system-fidelity"></a>
## `system/fidelity`

- Required: `yes`
- Shape: enum: `filesystem-view`, `process-runtime`, `shared-kernel-linux`, `full-system-linux`

<a id="field-control"></a>
## `control`

- Required: `yes`
- Shape: ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/controlSelection`

<a id="field-boot-mode"></a>
## `boot/mode`

- Required: `yes`
- Shape: enum: `none`, `efi`, `direct-kernel`

<a id="field-storage-format"></a>
## `storage/format`

- Required: `yes`
- Shape: enum: `directory-copy`, `raw`, `kernel-initrd-rootfs`

<a id="field-device-classes"></a>
## `device/classes`

- Required: `yes`
- Shape: ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/deviceClasses`

<a id="field-console-mode"></a>
## `console/mode`

- Required: `yes`
- Shape: enum: `none`, `diagnostic-output-only`

<a id="field-network-profile"></a>
## `network/profile`

- Required: `yes`
- Shape: enum: `none`, `isolated`, `egress-allowlisted`

<a id="field-host-filesystem-sharing-mode"></a>
## `host-filesystem-sharing/mode`

- Required: `yes`
- Shape: enum: `denied`, `read-only`, `read-write`

<a id="field-credential-injection-mode"></a>
## `credential-injection/mode`

- Required: `yes`
- Shape: enum: `denied`, `explicit-scoped`

<a id="field-resource-enforcement-classes"></a>
## `resource-enforcement/classes`

- Required: `yes`
- Shape: ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/resourceClasses`

<a id="field-lifecycle-operations"></a>
## `lifecycle/operations`

- Required: `yes`
- Shape: ref: `sensorium-virt-backend-capabilities.v1.schema.json#/$defs/lifecycleOperations`

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-operational-context-candidate-digest"></a>
## `operational/context-candidate-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-operational-context-policy-ref"></a>
## `operational/context-policy-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-attached-resource-contexts"></a>
## `attached-resource-contexts`

- Required: `yes`
- Shape: array

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-architecture"></a>
## `$defs.architecture`

- Shape: enum: `x86_64`, `arm64`
