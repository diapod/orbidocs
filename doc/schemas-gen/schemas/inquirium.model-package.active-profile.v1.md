# Inquirium Model Package Active Profile v1

Source schema: [`doc/schemas/inquirium.model-package.active-profile.v1.schema.json`](../../schemas/inquirium.model-package.active-profile.v1.schema.json)

Generation-counted pointer to one verified active local model package profile and its rollback predecessor.

## Governing Basis

- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/066-inquirium-assistant-channel.md`](../../project/40-proposals/066-inquirium-assistant-channel.md)

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.active-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | string |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`package/ref`](#field-package-ref) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`receipt/ref`](#field-receipt-ref) | `yes` | string |  |
| [`asset/refs`](#field-asset-refs) | `yes` | array |  |
| [`activated-at`](#field-activated-at) | `yes` | string |  |
| [`conformance/report-ref`](#field-conformance-report-ref) | `yes` | string |  |
| [`rollback`](#field-rollback) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.active-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: string

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: string

<a id="field-receipt-ref"></a>
## `receipt/ref`

- Required: `yes`
- Shape: string

<a id="field-asset-refs"></a>
## `asset/refs`

- Required: `yes`
- Shape: array

<a id="field-activated-at"></a>
## `activated-at`

- Required: `yes`
- Shape: string

<a id="field-conformance-report-ref"></a>
## `conformance/report-ref`

- Required: `yes`
- Shape: string

<a id="field-rollback"></a>
## `rollback`

- Required: `no`
- Shape: object
