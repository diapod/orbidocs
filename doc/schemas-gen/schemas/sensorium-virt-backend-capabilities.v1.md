# Sensorium Virt Backend Capabilities v1

Source schema: [`doc/schemas/sensorium-virt-backend-capabilities.v1.schema.json`](../../schemas/sensorium-virt-backend-capabilities.v1.schema.json)

Host-attested, closed capability descriptor for one Sensorium Virt backend configuration.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-backend-capabilities.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capabilities/ref`](#field-capabilities-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/id`](#field-backend-id) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/provider`](#field-backend-provider) | `yes` | ref: `#/$defs/token` |  |
| [`backend/version`](#field-backend-version) | `yes` | string |  |
| [`backend/binary-digest`](#field-backend-binary-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `remote-sandbox` |  |
| [`host/architecture`](#field-host-architecture) | `yes` | ref: `#/$defs/architecture` |  |
| [`guest/architecture`](#field-guest-architecture) | `yes` | ref: `#/$defs/architecture` |  |
| [`isolation/class`](#field-isolation-class) | `yes` | enum: `none`, `process-sandbox`, `shared-kernel-container`, `hardware-vm` |  |
| [`system/fidelity`](#field-system-fidelity) | `yes` | enum: `filesystem-view`, `process-runtime`, `shared-kernel-linux`, `full-system-linux` |  |
| [`control`](#field-control) | `yes` | ref: `#/$defs/controlSelection` |  |
| [`boot/modes`](#field-boot-modes) | `yes` | ref: `#/$defs/bootModes` |  |
| [`storage/formats`](#field-storage-formats) | `yes` | ref: `#/$defs/storageFormats` |  |
| [`device/classes`](#field-device-classes) | `yes` | ref: `#/$defs/deviceClasses` |  |
| [`console/mode`](#field-console-mode) | `yes` | enum: `none`, `diagnostic-output-only` |  |
| [`network/profiles`](#field-network-profiles) | `yes` | ref: `#/$defs/networkProfiles` |  |
| [`host-filesystem-sharing/mode`](#field-host-filesystem-sharing-mode) | `yes` | enum: `denied`, `read-only`, `read-write` |  |
| [`credential-injection/mode`](#field-credential-injection-mode) | `yes` | enum: `denied`, `explicit-scoped` |  |
| [`resource-enforcement/classes`](#field-resource-enforcement-classes) | `yes` | ref: `#/$defs/resourceClasses` |  |
| [`lifecycle/operations`](#field-lifecycle-operations) | `yes` | ref: `#/$defs/lifecycleOperations` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`token`](#def-token) | string |  |
| [`digest`](#def-digest) | string |  |
| [`architecture`](#def-architecture) | enum: `x86_64`, `arm64` |  |
| [`controlSelection`](#def-controlselection) | object |  |
| [`bootModes`](#def-bootmodes) | array |  |
| [`storageFormats`](#def-storageformats) | array |  |
| [`deviceClasses`](#def-deviceclasses) | array |  |
| [`networkProfiles`](#def-networkprofiles) | array |  |
| [`resourceClasses`](#def-resourceclasses) | array |  |
| [`lifecycleOperations`](#def-lifecycleoperations) | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-backend-capabilities.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capabilities-ref"></a>
## `capabilities/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-id"></a>
## `backend/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-provider"></a>
## `backend/provider`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-backend-version"></a>
## `backend/version`

- Required: `yes`
- Shape: string

<a id="field-backend-binary-digest"></a>
## `backend/binary-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

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
- Shape: ref: `#/$defs/controlSelection`

<a id="field-boot-modes"></a>
## `boot/modes`

- Required: `yes`
- Shape: ref: `#/$defs/bootModes`

<a id="field-storage-formats"></a>
## `storage/formats`

- Required: `yes`
- Shape: ref: `#/$defs/storageFormats`

<a id="field-device-classes"></a>
## `device/classes`

- Required: `yes`
- Shape: ref: `#/$defs/deviceClasses`

<a id="field-console-mode"></a>
## `console/mode`

- Required: `yes`
- Shape: enum: `none`, `diagnostic-output-only`

<a id="field-network-profiles"></a>
## `network/profiles`

- Required: `yes`
- Shape: ref: `#/$defs/networkProfiles`

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
- Shape: ref: `#/$defs/resourceClasses`

<a id="field-lifecycle-operations"></a>
## `lifecycle/operations`

- Required: `yes`
- Shape: ref: `#/$defs/lifecycleOperations`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-architecture"></a>
## `$defs.architecture`

- Shape: enum: `x86_64`, `arm64`

<a id="def-controlselection"></a>
## `$defs.controlSelection`

- Shape: object

<a id="def-bootmodes"></a>
## `$defs.bootModes`

- Shape: array

<a id="def-storageformats"></a>
## `$defs.storageFormats`

- Shape: array

<a id="def-deviceclasses"></a>
## `$defs.deviceClasses`

- Shape: array

<a id="def-networkprofiles"></a>
## `$defs.networkProfiles`

- Shape: array

<a id="def-resourceclasses"></a>
## `$defs.resourceClasses`

- Shape: array

<a id="def-lifecycleoperations"></a>
## `$defs.lifecycleOperations`

- Shape: array
