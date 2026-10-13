# Sensorium-device-discovery-result.v1

Source schema: [`doc/schemas/sensorium-device-discovery-result.v1.schema.json`](../../schemas/sensorium-device-discovery-result.v1.schema.json)

Caller-private final replacement snapshot after confirmed own-session cleanup. Limit/deadline completion is partial. Watchdog timeout, provider failure, refusal and uncertain cleanup are not partial success. Zero results describes only this observation scope/window. Encoded vector max32KiB; disclosed count equals vector length; all candidates share operation/caller/profile/scope. Host performs cross-field checks before disclosure.

## Governing Basis

- [`doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`](../../project/40-proposals/045-sensorium-local-enaction-stratum.md)
- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-device-discovery-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`reason`](#field-reason) | `yes` | enum: `window-completed`, `limit-reached`, `deadline-reached` |  |
| [`partial`](#field-partial) | `yes` | boolean |  |
| [`candidates`](#field-candidates) | `yes` | array |  |
| [`candidates/disclosed`](#field-candidates-disclosed) | `yes` | integer |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "reason": {
      "const": "window-completed"
    }
  },
  "required": [
    "reason"
  ]
}
```

Then:

```json
{
  "properties": {
    "partial": {
      "const": false
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-device-discovery-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: enum: `window-completed`, `limit-reached`, `deadline-reached`

<a id="field-partial"></a>
## `partial`

- Required: `yes`
- Shape: boolean

<a id="field-candidates"></a>
## `candidates`

- Required: `yes`
- Shape: array

<a id="field-candidates-disclosed"></a>
## `candidates/disclosed`

- Required: `yes`
- Shape: integer
