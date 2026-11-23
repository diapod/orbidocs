# Whisper-source-exact-use.v1

Source schema: [`doc/schemas/whisper-source-exact-use.v1.schema.json`](../../schemas/whisper-source-exact-use.v1.schema.json)

Closed tuple vocabulary for exact v4 grants. A profile must separately authorize each complete use.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`record/kind`](#field-record-kind) | `yes` | string |  |
| [`content/schema`](#field-content-schema) | `yes` | string |  |
| [`topic/key`](#field-topic-key) | `yes` | string | Exact Agora topic key with a 512-byte UTF-8 limit and no surrounding whitespace. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `federation-scoped`, `cross-federation`, `public-aggregate-only`, `single-audience` |  |
| [`signing/use`](#field-signing-use) | `yes` | enum: `publication`, `embargo-manifest`, `embargo-audience-manifest` |  |
## Field Semantics

<a id="field-record-kind"></a>
## `record/kind`

- Required: `yes`
- Shape: string

<a id="field-content-schema"></a>
## `content/schema`

- Required: `yes`
- Shape: string

<a id="field-topic-key"></a>
## `topic/key`

- Required: `yes`
- Shape: string

Exact Agora topic key with a 512-byte UTF-8 limit and no surrounding whitespace.

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: enum: `federation-scoped`, `cross-federation`, `public-aggregate-only`, `single-audience`

<a id="field-signing-use"></a>
## `signing/use`

- Required: `yes`
- Shape: enum: `publication`, `embargo-manifest`, `embargo-audience-manifest`
