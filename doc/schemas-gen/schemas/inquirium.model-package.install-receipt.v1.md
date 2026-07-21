# Inquirium Model Package Install Receipt v1

Source schema: [`doc/schemas/inquirium.model-package.install-receipt.v1.schema.json`](../../schemas/inquirium.model-package.install-receipt.v1.schema.json)

Immutable lifecycle fact for one admitted local model package installation.

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.install-receipt.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`receipt/ref`](#field-receipt-ref) | `yes` | string |  |
| [`package/ref`](#field-package-ref) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `installed`, `verified`, `failed`, `removed` |  |
| [`authority/ref`](#field-authority-ref) | `yes` | string |  |
| [`asset/refs`](#field-asset-refs) | `yes` | array |  |
| [`installed-at`](#field-installed-at) | `yes` | string |  |
| [`verified-at`](#field-verified-at) | `no` | string |  |
| [`finished-at`](#field-finished-at) | `no` | string |  |
| [`failure/code`](#field-failure-code) | `no` | string |  |
| [`trace/ref`](#field-trace-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.install-receipt.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-receipt-ref"></a>
## `receipt/ref`

- Required: `yes`
- Shape: string

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `installed`, `verified`, `failed`, `removed`

<a id="field-authority-ref"></a>
## `authority/ref`

- Required: `yes`
- Shape: string

<a id="field-asset-refs"></a>
## `asset/refs`

- Required: `yes`
- Shape: array

<a id="field-installed-at"></a>
## `installed-at`

- Required: `yes`
- Shape: string

<a id="field-verified-at"></a>
## `verified-at`

- Required: `no`
- Shape: string

<a id="field-finished-at"></a>
## `finished-at`

- Required: `no`
- Shape: string

<a id="field-failure-code"></a>
## `failure/code`

- Required: `no`
- Shape: string

<a id="field-trace-ref"></a>
## `trace/ref`

- Required: `yes`
- Shape: string
