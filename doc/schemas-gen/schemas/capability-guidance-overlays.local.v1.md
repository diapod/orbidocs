# Local Capability Guidance Operator Source v1

Source schema: [`doc/schemas/capability-guidance-overlays.local.v1.schema.json`](../../schemas/capability-guidance-overlays.local.v1.schema.json)

One bounded host-local operator source. Entries are keyed by the canonical digest of capability, provider and exact contract binding. The host checks that key, current provider report, local schema digest and examples before use. No entry grants execution authority.

## Governing Basis

- [`doc/project/40-proposals/091-file-backed-configuration-and-explainable-composition.md`](../../project/40-proposals/091-file-backed-configuration-and-explainable-composition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-guidance-overlays.local.v1` |  |
| [`entries`](#field-entries) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-guidance-overlays.local.v1`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: object
