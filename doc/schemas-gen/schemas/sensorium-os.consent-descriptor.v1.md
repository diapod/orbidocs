# Sensorium-os.consent-descriptor.v1

Source schema: [`doc/schemas/sensorium-os.consent-descriptor.v1.schema.json`](../../schemas/sensorium-os.consent-descriptor.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`](../../project/40-proposals/048-sensorium-os-connector-action-classes.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-os.consent-descriptor.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`reason/code`](#field-reason-code) | `yes` | ref: `#/$defs/token` |  |
| [`action/id`](#field-action-id) | `yes` | ref: `#/$defs/token` |  |
| [`action/class`](#field-action-class) | `yes` | enum: `read-only-spawn`, `allowlisted-script`, `scoped-fs-write`, `egress-network-spawn`, `artifact-producing-spawn`, `composed-spawn`, `operator-gated-spawn` |  |
| [`executable/summary`](#field-executable-summary) | `yes` | string |  |
| [`argv/shape`](#field-argv-shape) | `yes` | object |  |
| [`parameters/schema-ref`](#field-parameters-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`result/contract`](#field-result-contract) | `yes` | object |  |
| [`result/pointer-fields`](#field-result-pointer-fields) | `yes` | array |  |
| [`sensitivity`](#field-sensitivity) | `yes` | string |  |
| [`limits`](#field-limits) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`token`](#def-token) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-os.consent-descriptor.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-action-id"></a>
## `action/id`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-action-class"></a>
## `action/class`

- Required: `yes`
- Shape: enum: `read-only-spawn`, `allowlisted-script`, `scoped-fs-write`, `egress-network-spawn`, `artifact-producing-spawn`, `composed-spawn`, `operator-gated-spawn`

<a id="field-executable-summary"></a>
## `executable/summary`

- Required: `yes`
- Shape: string

<a id="field-argv-shape"></a>
## `argv/shape`

- Required: `yes`
- Shape: object

<a id="field-parameters-schema-ref"></a>
## `parameters/schema-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-result-contract"></a>
## `result/contract`

- Required: `yes`
- Shape: object

<a id="field-result-pointer-fields"></a>
## `result/pointer-fields`

- Required: `yes`
- Shape: array

<a id="field-sensitivity"></a>
## `sensitivity`

- Required: `yes`
- Shape: string

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string
