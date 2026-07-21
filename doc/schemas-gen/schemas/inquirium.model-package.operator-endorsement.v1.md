# Inquirium Model Package Operator Endorsement v1

Source schema: [`doc/schemas/inquirium.model-package.operator-endorsement.v1.schema.json`](../../schemas/inquirium.model-package.operator-endorsement.v1.schema.json)

Node- and profile-scoped operator endorsement for an otherwise unsigned local model package manifest.

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.operator-endorsement.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`endorsement/ref`](#field-endorsement-ref) | `yes` | string |  |
| [`package/ref`](#field-package-ref) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`node/ref`](#field-node-ref) | `yes` | string |  |
| [`profile/ref`](#field-profile-ref) | `yes` | string |  |
| [`operator/ref`](#field-operator-ref) | `yes` | string |  |
| [`question/ref`](#field-question-ref) | `yes` | string |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
| [`endorsed-at`](#field-endorsed-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.operator-endorsement.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-endorsement-ref"></a>
## `endorsement/ref`

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

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: string

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: string

<a id="field-question-ref"></a>
## `question/ref`

- Required: `yes`
- Shape: string

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `yes`
- Shape: string

<a id="field-endorsed-at"></a>
## `endorsed-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
