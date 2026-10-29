# Nym-source-status-result.local.v1

Source schema: [`doc/schemas/nym-source-status-result.local.v1.schema.json`](../../schemas/nym-source-status-result.local.v1.schema.json)

A current verified snapshot for the selected purpose or explicit pending refresh. Availability is not certificate eligibility, admission or emission authority.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-source-status-result.local.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`purpose`](#field-purpose) | `yes` | enum: `collection`, `first-emission` |  |
| [`state`](#field-state) | `yes` | enum: `available`, `pending` |  |
| [`status`](#field-status) | `no` | ref: `nym-source-status.v1.schema.json` |  |
| [`status/digest`](#field-status-digest) | `no` | string |  |
| [`reason`](#field-reason) | `no` | enum: `status-unavailable`, `status-stale` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-source-status-result.local.v1`

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

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: enum: `collection`, `first-emission`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `available`, `pending`

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: ref: `nym-source-status.v1.schema.json`

<a id="field-status-digest"></a>
## `status/digest`

- Required: `no`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: enum: `status-unavailable`, `status-stale`
