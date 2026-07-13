# Whisper Trace Publish Result v1

Source schema: [`doc/schemas/whisper-trace-publish-result.v1.schema.json`](../../schemas/whisper-trace-publish-result.v1.schema.json)

Metadata-only result of an accepted Whisper trace publication. It deliberately excludes inline artifact bytes.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-trace-publish-result.v1` |  |
| [`status`](#field-status) | `yes` | const: `accepted` |  |
| [`record/id`](#field-record-id) | `yes` | string |  |
| [`delivery`](#field-delivery) | `yes` | object | Transport-owned AD result. Consumers must not infer trace semantics from carrier diagnostics. |
| [`trace/metadata`](#field-trace-metadata) | `yes` | ref: `#/$defs/trace_metadata` |  |
| [`trace/view`](#field-trace-view) | `no` | object | Optional sender-local metadata read model created after durable publication accounting. |
| [`privacy/findings`](#field-privacy-findings) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`privacy_finding`](#def-privacy-finding) | object |  |
| [`trace_metadata`](#def-trace-metadata) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-trace-publish-result.v1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `accepted`

<a id="field-record-id"></a>
## `record/id`

- Required: `yes`
- Shape: string

<a id="field-delivery"></a>
## `delivery`

- Required: `yes`
- Shape: object

Transport-owned AD result. Consumers must not infer trace semantics from carrier diagnostics.

<a id="field-trace-metadata"></a>
## `trace/metadata`

- Required: `yes`
- Shape: ref: `#/$defs/trace_metadata`

<a id="field-trace-view"></a>
## `trace/view`

- Required: `no`
- Shape: object

Optional sender-local metadata read model created after durable publication accounting.

<a id="field-privacy-findings"></a>
## `privacy/findings`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-privacy-finding"></a>
## `$defs.privacy_finding`

- Shape: object

<a id="def-trace-metadata"></a>
## `$defs.trace_metadata`

- Shape: object
