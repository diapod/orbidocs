# Local Capability Guidance Operator Inspection v1

Source schema: [`doc/schemas/capability-guidance-overlay-inspection.local.v1.schema.json`](../../schemas/capability-guidance-overlay-inspection.local.v1.schema.json)

Operator-only effective guidance provenance. The source locator is relative to the private host root and must never enter a model-facing catalog result.

## Governing Basis

- [`doc/project/40-proposals/091-file-backed-configuration-and-explainable-composition.md`](../../project/40-proposals/091-file-backed-configuration-and-explainable-composition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-guidance-overlay-inspection.local.v1` |  |
| [`setting/address`](#field-setting-address) | `yes` | ref: `configuration-common.v1.schema.json#/$defs/settingAddress` |  |
| [`source/provenance`](#field-source-provenance) | `yes` | enum: `none`, `provider-default`, `operator-overlay` |  |
| [`source/locator`](#field-source-locator) | `yes` | string \| null |  |
| [`source-set/revision`](#field-source-set-revision) | `yes` | ref: `configuration-common.v1.schema.json#/$defs/digest` |  |
| [`guidance/digest`](#field-guidance-digest) | `yes` | unspecified |  |
| [`configuration/explain`](#field-configuration-explain) | `yes` | ref: `config-explain.response.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-guidance-overlay-inspection.local.v1`

<a id="field-setting-address"></a>
## `setting/address`

- Required: `yes`
- Shape: ref: `configuration-common.v1.schema.json#/$defs/settingAddress`

<a id="field-source-provenance"></a>
## `source/provenance`

- Required: `yes`
- Shape: enum: `none`, `provider-default`, `operator-overlay`

<a id="field-source-locator"></a>
## `source/locator`

- Required: `yes`
- Shape: string | null

<a id="field-source-set-revision"></a>
## `source-set/revision`

- Required: `yes`
- Shape: ref: `configuration-common.v1.schema.json#/$defs/digest`

<a id="field-guidance-digest"></a>
## `guidance/digest`

- Required: `yes`
- Shape: unspecified

<a id="field-configuration-explain"></a>
## `configuration/explain`

- Required: `yes`
- Shape: ref: `config-explain.response.v1.schema.json`
