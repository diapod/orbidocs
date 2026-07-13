# Whisper Trace Consent Request v1

Source schema: [`doc/schemas/whisper-trace-consent-request.v1.schema.json`](../../schemas/whisper-trace-consent-request.v1.schema.json)

Sender-local request for operator consent to disclose exact inline artifact bytes in a Whisper trace. It describes disclosure intent, not a publishable trace and not a granted consent fact.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-trace-consent-request.v1` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `whisper-trace.v1.schema.json#/$defs/ref` | Participant, nym, or other locally authorized subject on whose behalf inline content would be disclosed. |
| [`trace/kind`](#field-trace-kind) | `yes` | ref: `whisper-trace.v1.schema.json#/properties/trace~1kind` |  |
| [`artifact`](#field-artifact) | `yes` | ref: `whisper-trace.v1.schema.json#/$defs/artifact` |  |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | ref: `whisper-trace.v1.schema.json#/properties/disclosure~1scope` |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "properties": {
    "artifact": {
      "required": [
        "bytes/base64"
      ],
      "properties": {
        "size/bytes": {
          "maximum": 32768
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-trace-consent-request.v1`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json#/$defs/ref`

Participant, nym, or other locally authorized subject on whose behalf inline content would be disclosed.

<a id="field-trace-kind"></a>
## `trace/kind`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json#/properties/trace~1kind`

<a id="field-artifact"></a>
## `artifact`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json#/$defs/artifact`

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: ref: `whisper-trace.v1.schema.json#/properties/disclosure~1scope`
