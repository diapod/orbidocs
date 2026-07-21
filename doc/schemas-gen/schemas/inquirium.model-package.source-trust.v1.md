# Inquirium Model Package Source Trust v1

Source schema: [`doc/schemas/inquirium.model-package.source-trust.v1.schema.json`](../../schemas/inquirium.model-package.source-trust.v1.schema.json)

Operator-signed, revocable local authority for one model-package source boundary.

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.source-trust.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`trust/ref`](#field-trust-ref) | `yes` | string |  |
| [`scope`](#field-scope) | `yes` | const: `local-model-provisioning` |  |
| [`mode`](#field-mode) | `yes` | enum: `one_shot`, `durable` |  |
| [`target`](#field-target) | `yes` | unspecified |  |
| [`operator/ref`](#field-operator-ref) | `yes` | string |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
| [`granted-at`](#field-granted-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`revoked-at`](#field-revoked-at) | `no` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "mode": {
      "const": "one_shot"
    }
  },
  "required": [
    "mode"
  ]
}
```

Then:

```json
{
  "required": [
    "expires-at"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.source-trust.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-trust-ref"></a>
## `trust/ref`

- Required: `yes`
- Shape: string

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: const: `local-model-provisioning`

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `one_shot`, `durable`

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: unspecified

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: string

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `yes`
- Shape: string

<a id="field-granted-at"></a>
## `granted-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

<a id="field-revoked-at"></a>
## `revoked-at`

- Required: `no`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
