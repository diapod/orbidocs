# Sensorium File Read Result v1

Source schema: [`doc/schemas/sensorium-file-read-result.v1.schema.json`](../../schemas/sensorium-file-read-result.v1.schema.json)

Bounded file read result. Large or sensitive contents should be returned as artifact references.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-file-read-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`read/ref`](#field-read-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`address`](#field-address) | `yes` | ref: `sensorium-relative-path-address.v1.schema.json` |  |
| [`result/kind`](#field-result-kind) | `yes` | enum: `inline-text`, `inline-base64`, `artifact-ref`, `refused` |  |
| [`text`](#field-text) | `no` | string |  |
| [`bytes/base64`](#field-bytes-base64) | `no` | string |  |
| [`artifact/ref`](#field-artifact-ref) | `no` | ref: `#/$defs/ref` |  |
| [`size/bytes`](#field-size-bytes) | `yes` | integer |  |
| [`content/sha256`](#field-content-sha256) | `yes` | string |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-file-read-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-read-ref"></a>
## `read/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-address"></a>
## `address`

- Required: `yes`
- Shape: ref: `sensorium-relative-path-address.v1.schema.json`

<a id="field-result-kind"></a>
## `result/kind`

- Required: `yes`
- Shape: enum: `inline-text`, `inline-base64`, `artifact-ref`, `refused`

<a id="field-text"></a>
## `text`

- Required: `no`
- Shape: string

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `no`
- Shape: string

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-size-bytes"></a>
## `size/bytes`

- Required: `yes`
- Shape: integer

<a id="field-content-sha256"></a>
## `content/sha256`

- Required: `yes`
- Shape: string

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
