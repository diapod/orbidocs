# Nym-case-key-provider.local.v1

Source schema: [`doc/schemas/nym-case-key-provider.local.v1.schema.json`](../../schemas/nym-case-key-provider.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md`](../../project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-case-key-provider.local.v1` |  |
| [`provider/id`](#field-provider-id) | `yes` | string |  |
| [`scope/digest`](#field-scope-digest) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-case-key-provider.local.v1`

<a id="field-provider-id"></a>
## `provider/id`

- Required: `yes`
- Shape: string

<a id="field-scope-digest"></a>
## `scope/digest`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer
