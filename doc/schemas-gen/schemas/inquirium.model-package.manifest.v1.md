# Inquirium Model Package Manifest v1

Source schema: [`doc/schemas/inquirium.model-package.manifest.v1.schema.json`](../../schemas/inquirium.model-package.manifest.v1.schema.json)

Content-addressed manifest for one operator-admissible local model runtime and its assets.

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.manifest.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `#/$defs/packageRef` |  |
| [`package/version`](#field-package-version) | `yes` | ref: `#/$defs/label` |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`authority/mode`](#field-authority-mode) | `yes` | enum: `distributor_signed`, `operator_endorsed` |  |
| [`platform`](#field-platform) | `yes` | unspecified |  |
| [`runtime`](#field-runtime) | `yes` | object |  |
| [`model`](#field-model) | `yes` | object |  |
| [`resource-requirements`](#field-resource-requirements) | `yes` | object |  |
| [`provenance`](#field-provenance) | `yes` | object |  |
| [`assets`](#field-assets) | `yes` | array |  |
| [`signatures`](#field-signatures) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`label`](#def-label) | string |  |
| [`digest`](#def-digest) | string |  |
| [`assetRef`](#def-assetref) | string |  |
| [`packageRef`](#def-packageref) | string |  |
| [`httpPath`](#def-httppath) | string |  |
| [`source`](#def-source) | unspecified |  |
| [`asset`](#def-asset) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.manifest.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `#/$defs/packageRef`

<a id="field-package-version"></a>
## `package/version`

- Required: `yes`
- Shape: ref: `#/$defs/label`

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-authority-mode"></a>
## `authority/mode`

- Required: `yes`
- Shape: enum: `distributor_signed`, `operator_endorsed`

<a id="field-platform"></a>
## `platform`

- Required: `yes`
- Shape: unspecified

<a id="field-runtime"></a>
## `runtime`

- Required: `yes`
- Shape: object

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: object

<a id="field-resource-requirements"></a>
## `resource-requirements`

- Required: `yes`
- Shape: object

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: object

<a id="field-assets"></a>
## `assets`

- Required: `yes`
- Shape: array

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-label"></a>
## `$defs.label`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-assetref"></a>
## `$defs.assetRef`

- Shape: string

<a id="def-packageref"></a>
## `$defs.packageRef`

- Shape: string

<a id="def-httppath"></a>
## `$defs.httpPath`

- Shape: string

<a id="def-source"></a>
## `$defs.source`

- Shape: unspecified

<a id="def-asset"></a>
## `$defs.asset`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
