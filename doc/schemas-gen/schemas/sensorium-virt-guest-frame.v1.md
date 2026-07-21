# Sensorium Virt Guest Frame v1

Source schema: [`doc/schemas/sensorium-virt-guest-frame.v1.schema.json`](../../schemas/sensorium-virt-guest-frame.v1.schema.json)

Bounded generation-, plan-, image-, and boot-bound frame for the Workbench guest channel.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-guest-frame.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`frame/kind`](#field-frame-kind) | `yes` | enum: `handshake`, `operation`, `chunk`, `result`, `quiesce`, `shutdown` |  |
| [`environment/ref`](#field-environment-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`image/manifest-digest`](#field-image-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`guest-agent/protocol-version`](#field-guest-agent-protocol-version) | `yes` | const: `1` |  |
| [`guest/cid`](#field-guest-cid) | `yes` | integer |  |
| [`boot/nonce`](#field-boot-nonce) | `yes` | string |  |
| [`operation/id`](#field-operation-id) | `no` | ref: `#/$defs/ref` |  |
| [`operation/kind`](#field-operation-kind) | `no` | enum: `spawn-process`, `open-pty`, `terminal-input`, `terminal-resize`, `terminal-signal`, `file-snapshot`, `file-read`, `patch-stage`, `artifact-export`, `quiesce`, `shutdown` |  |
| [`sequence`](#field-sequence) | `yes` | integer |  |
| [`deadline-at`](#field-deadline-at) | `yes` | string |  |
| [`chunk/index`](#field-chunk-index) | `no` | integer |  |
| [`chunk/count`](#field-chunk-count) | `no` | integer |  |
| [`payload/length`](#field-payload-length) | `yes` | integer |  |
| [`payload/digest`](#field-payload-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`payload/base64`](#field-payload-base64) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "frame/kind": {
      "enum": [
        "operation",
        "chunk",
        "result"
      ]
    }
  },
  "required": [
    "frame/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "operation/id",
    "operation/kind"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "frame/kind": {
      "const": "chunk"
    }
  },
  "required": [
    "frame/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "chunk/index",
    "chunk/count",
    "payload/base64"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-guest-frame.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-frame-kind"></a>
## `frame/kind`

- Required: `yes`
- Shape: enum: `handshake`, `operation`, `chunk`, `result`, `quiesce`, `shutdown`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-image-manifest-digest"></a>
## `image/manifest-digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-guest-agent-protocol-version"></a>
## `guest-agent/protocol-version`

- Required: `yes`
- Shape: const: `1`

<a id="field-guest-cid"></a>
## `guest/cid`

- Required: `yes`
- Shape: integer

<a id="field-boot-nonce"></a>
## `boot/nonce`

- Required: `yes`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-operation-kind"></a>
## `operation/kind`

- Required: `no`
- Shape: enum: `spawn-process`, `open-pty`, `terminal-input`, `terminal-resize`, `terminal-signal`, `file-snapshot`, `file-read`, `patch-stage`, `artifact-export`, `quiesce`, `shutdown`

<a id="field-sequence"></a>
## `sequence`

- Required: `yes`
- Shape: integer

<a id="field-deadline-at"></a>
## `deadline-at`

- Required: `yes`
- Shape: string

<a id="field-chunk-index"></a>
## `chunk/index`

- Required: `no`
- Shape: integer

<a id="field-chunk-count"></a>
## `chunk/count`

- Required: `no`
- Shape: integer

<a id="field-payload-length"></a>
## `payload/length`

- Required: `yes`
- Shape: integer

<a id="field-payload-digest"></a>
## `payload/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-payload-base64"></a>
## `payload/base64`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
