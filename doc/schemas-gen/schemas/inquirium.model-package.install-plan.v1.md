# Inquirium Model Package Install Plan v1

Source schema: [`doc/schemas/inquirium.model-package.install-plan.v1.schema.json`](../../schemas/inquirium.model-package.install-plan.v1.schema.json)

Deterministic and inert preview of model-package installation work; this contract cannot report executed effects.

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
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.install-plan.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | string |  |
| [`package/ref`](#field-package-ref) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`target-profile/ref`](#field-target-profile-ref) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `ready`, `blocked` |  |
| [`blockers`](#field-blockers) | `yes` | array |  |
| [`steps`](#field-steps) | `yes` | array |  |
| [`effects/executed`](#field-effects-executed) | `yes` | const: `False` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`assetRef`](#def-assetref) | string |  |
| [`blocker`](#def-blocker) | object |  |
| [`step`](#def-step) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "ready"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "properties": {
    "blockers": {
      "maxItems": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "blocked"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "properties": {
    "blockers": {
      "minItems": 1
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.install-plan.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-plan-ref"></a>
## `plan/ref`

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

<a id="field-target-profile-ref"></a>
## `target-profile/ref`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ready`, `blocked`

<a id="field-blockers"></a>
## `blockers`

- Required: `yes`
- Shape: array

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array

<a id="field-effects-executed"></a>
## `effects/executed`

- Required: `yes`
- Shape: const: `False`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-assetref"></a>
## `$defs.assetRef`

- Shape: string

<a id="def-blocker"></a>
## `$defs.blocker`

- Shape: object

<a id="def-step"></a>
## `$defs.step`

- Shape: object
