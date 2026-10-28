# Association-room-proposal.v2

Source schema: [`doc/schemas/association-room-proposal.v2.schema.json`](../../schemas/association-room-proposal.v2.schema.json)

Aggregate proposal referencing a contextual first-threshold record. No participant addresses, enrollment or room creation authority. Later loss of basis is shown by the local current-result annotation, without replacing this immutable record.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `association-room-proposal.v2` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`proposal/id`](#field-proposal-id) | `yes` | string |  |
| [`threshold/id`](#field-threshold-id) | `yes` | string |  |
| [`threshold/record-id`](#field-threshold-record-id) | `yes` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `association-room-proposal.v2`

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

<a id="field-proposal-id"></a>
## `proposal/id`

- Required: `yes`
- Shape: string

<a id="field-threshold-id"></a>
## `threshold/id`

- Required: `yes`
- Shape: string

<a id="field-threshold-record-id"></a>
## `threshold/record-id`

- Required: `yes`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string
