# Whisper Trace Publish Request v1

Source schema: [`doc/schemas/whisper-trace-publish-request.v1.schema.json`](../../schemas/whisper-trace-publish-request.v1.schema.json)

Idempotent sender-local request to validate, sign, and dispatch one complete Whisper trace through Agora or AD/INAC according to its disclosure posture.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-trace-publish-request.v1` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `whisper-trace.v1.schema.json#/$defs/ref` |  |
| [`trace`](#field-trace) | `yes` | ref: `whisper-trace.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-trace-publish-request.v1`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json#/$defs/ref`

<a id="field-trace"></a>
## `trace`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json`
