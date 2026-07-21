# Sensorium Virt Image Manifest v1

Source schema: [`doc/schemas/sensorium-virt-image-manifest.v1.schema.json`](../../schemas/sensorium-virt-image-manifest.v1.schema.json)

Digest-pinned logical full-system image and its backend variants.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-image-manifest.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`image/ref`](#field-image-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`userspace/rootfs-digest`](#field-userspace-rootfs-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`sbom/digest`](#field-sbom-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`build-provenance/ref`](#field-build-provenance-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`build-provenance/digest`](#field-build-provenance-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`guest-agent/digest`](#field-guest-agent-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`guest-protocol/schema-set-digest`](#field-guest-protocol-schema-set-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`guest-protocol/version`](#field-guest-protocol-version) | `yes` | const: `1` |  |
| [`variants`](#field-variants) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-image-manifest.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-image-ref"></a>
## `image/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-userspace-rootfs-digest"></a>
## `userspace/rootfs-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-sbom-digest"></a>
## `sbom/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-build-provenance-ref"></a>
## `build-provenance/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-build-provenance-digest"></a>
## `build-provenance/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-guest-agent-digest"></a>
## `guest-agent/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-guest-protocol-schema-set-digest"></a>
## `guest-protocol/schema-set-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-guest-protocol-version"></a>
## `guest-protocol/version`

- Required: `yes`
- Shape: const: `1`

<a id="field-variants"></a>
## `variants`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
