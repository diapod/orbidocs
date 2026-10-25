# Whisper-source-descriptor.v1

Source schema: [`doc/schemas/whisper-source-descriptor.v1.schema.json`](../../schemas/whisper-source-descriptor.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-source-descriptor.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/start`](#field-epoch-start) | `yes` | string |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`source/derivation`](#field-source-derivation) | `yes` | const: `issuer-derived-v1` |  |
| [`status/min-revision`](#field-status-min-revision) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-source-descriptor.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

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

<a id="field-epoch-start"></a>
## `epoch/start`

- Required: `yes`
- Shape: string

<a id="field-epoch-end"></a>
## `epoch/end`

- Required: `yes`
- Shape: string

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-source-derivation"></a>
## `source/derivation`

- Required: `yes`
- Shape: const: `issuer-derived-v1`

<a id="field-status-min-revision"></a>
## `status/min-revision`

- Required: `yes`
- Shape: integer
