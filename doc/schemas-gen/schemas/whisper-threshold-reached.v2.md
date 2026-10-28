# Whisper-threshold-reached.v2

Source schema: [`doc/schemas/whisper-threshold-reached.v2.schema.json`](../../schemas/whisper-threshold-reached.v2.schema.json)

First contextual-source threshold claim. Frozen signed basis is historical; current eligibility and later source revocation are separate local facts. Distinct nym/node counts are never substituted for sources.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-threshold-reached.v2` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`threshold/id`](#field-threshold-id) | `yes` | string |  |
| [`topic/class`](#field-topic-class) | `yes` | string |  |
| [`signal/similarity-key`](#field-signal-similarity-key) | `yes` | string |  |
| [`sources/distinct-count`](#field-sources-distinct-count) | `yes` | integer |  |
| [`threshold/minimum`](#field-threshold-minimum) | `yes` | const: `2` |  |
| [`status/revision`](#field-status-revision) | `yes` | integer |  |
| [`status/digest`](#field-status-digest) | `yes` | string |  |
| [`basis/record-ids`](#field-basis-record-ids) | `yes` | array |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-threshold-reached.v2`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-epoch-end"></a>
## `epoch/end`

- Required: `yes`
- Shape: string

<a id="field-threshold-id"></a>
## `threshold/id`

- Required: `yes`
- Shape: string

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

<a id="field-signal-similarity-key"></a>
## `signal/similarity-key`

- Required: `yes`
- Shape: string

<a id="field-sources-distinct-count"></a>
## `sources/distinct-count`

- Required: `yes`
- Shape: integer

<a id="field-threshold-minimum"></a>
## `threshold/minimum`

- Required: `yes`
- Shape: const: `2`

<a id="field-status-revision"></a>
## `status/revision`

- Required: `yes`
- Shape: integer

<a id="field-status-digest"></a>
## `status/digest`

- Required: `yes`
- Shape: string

<a id="field-basis-record-ids"></a>
## `basis/record-ids`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string
