# Agora Record Authoring Profile v1

Source schema: [`doc/schemas/agora-record-authoring.v1.schema.json`](../../schemas/agora-record-authoring.v1.schema.json)

Creation-only constraints for new Agora records; not a discriminator or a retroactive signed-ingress/replay gate. Semantic ResourceRef validation and the 48 KiB emitted-envelope budget apply before signing.

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`record/about`](#field-record-about) | `no` | array |  |
## Field Semantics

<a id="field-record-about"></a>
## `record/about`

- Required: `no`
- Shape: array
