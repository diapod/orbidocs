# Sensorium Workbench Patch Install Result v1

Source schema: [`doc/schemas/sensorium-workbench-patch-install-result.v1.schema.json`](../../schemas/sensorium-workbench-patch-install-result.v1.schema.json)

Outcome of installing admitted staged files and deletions in a microVM workspace under one pinned patch policy (P094-021b/021g). `applied` preserves the guest commit receipt: every write names its admitted create/modify operation and content digest; a delete carries neither. Missing or substituted receipts are `unknown`, not proof of application. `refused` proves that no file changed; `unknown`, such as `patch-apply-partial`, proves nothing and the environment must be destroyed. The result is kept under its idempotency key, so a patch is never installed twice.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-patch-install-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`result/ref`](#field-result-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`address`](#field-address) | `yes` | ref: `#/$defs/address` |  |
| [`patch-policy/digest`](#field-patch-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `applied`, `refused`, `unknown` |  |
| [`entries`](#field-entries) | `no` | array |  |
| [`error/code`](#field-error-code) | `no` | ref: `#/$defs/code` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
| [`address`](#def-address) | object |  |
| [`code`](#def-code) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "outcome"
  ],
  "properties": {
    "outcome": {
      "const": "applied"
    }
  }
}
```

Then:

```json
{
  "required": [
    "entries"
  ],
  "not": {
    "required": [
      "error/code"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-patch-install-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-result-ref"></a>
## `result/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-address"></a>
## `address`

- Required: `yes`
- Shape: ref: `#/$defs/address`

<a id="field-patch-policy-digest"></a>
## `patch-policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `applied`, `refused`, `unknown`

<a id="field-entries"></a>
## `entries`

- Required: `no`
- Shape: array

<a id="field-error-code"></a>
## `error/code`

- Required: `no`
- Shape: ref: `#/$defs/code`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string

<a id="def-address"></a>
## `$defs.address`

- Shape: object

<a id="def-code"></a>
## `$defs.code`

- Shape: string
