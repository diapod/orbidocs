# Sensorium Actuation Bridge Response v1

Source schema: [`doc/schemas/sensorium-actuation.bridge.response.v1.schema.json`](../../schemas/sensorium-actuation.bridge.response.v1.schema.json)

Fail-closed response from the sensorium-actuation-core companion process.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-actuation.bridge.response.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | enum: `ok`, `refused` |  |
| [`result`](#field-result) | `no` | object |  |
| [`diagnostics`](#field-diagnostics) | `yes` | array |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "ok"
    }
  }
}
```

Then:

```json
{
  "required": [
    "result"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "refused"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "diagnostics": {
      "minItems": 1
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-actuation.bridge.response.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ok`, `refused`

<a id="field-result"></a>
## `result`

- Required: `no`
- Shape: object

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `yes`
- Shape: array
