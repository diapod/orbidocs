# Inquirium Model Package Provider Key Endorsement v1

Source schema: [`doc/schemas/inquirium.model-package.provider-key-endorsement.v1.schema.json`](../../schemas/inquirium.model-package.provider-key-endorsement.v1.schema.json)

Federation-root-signed, expiring trust statement for one provider release public key. Verification may project the exact key into distributor trust but never authorizes a release, source, install, or activation by itself.

## Governing Basis

- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/066-inquirium-assistant-channel.md`](../../project/40-proposals/066-inquirium-assistant-channel.md)
- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.provider-key-endorsement.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`endorsement/ref`](#field-endorsement-ref) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`federation-root/version`](#field-federation-root-version) | `yes` | integer |  |
| [`federation-root/digest`](#field-federation-root-digest) | `yes` | string |  |
| [`provider/ref`](#field-provider-ref) | `yes` | string |  |
| [`purpose`](#field-purpose) | `yes` | const: `model-package-distribution` |  |
| [`key/id`](#field-key-id) | `yes` | string |  |
| [`public/key`](#field-public-key) | `yes` | string |  |
| [`endorser/subject-ref`](#field-endorser-subject-ref) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | string |  |
| [`signatures`](#field-signatures) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.provider-key-endorsement.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-endorsement-ref"></a>
## `endorsement/ref`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-federation-root-version"></a>
## `federation-root/version`

- Required: `yes`
- Shape: integer

<a id="field-federation-root-digest"></a>
## `federation-root/digest`

- Required: `yes`
- Shape: string

<a id="field-provider-ref"></a>
## `provider/ref`

- Required: `yes`
- Shape: string

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `model-package-distribution`

<a id="field-key-id"></a>
## `key/id`

- Required: `yes`
- Shape: string

<a id="field-public-key"></a>
## `public/key`

- Required: `yes`
- Shape: string

<a id="field-endorser-subject-ref"></a>
## `endorser/subject-ref`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: string

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
