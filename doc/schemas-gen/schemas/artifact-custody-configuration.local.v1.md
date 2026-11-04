# Artifact-custody-configuration.local.v1

Source schema: [`doc/schemas/artifact-custody-configuration.local.v1.schema.json`](../../schemas/artifact-custody-configuration.local.v1.schema.json)

Resolved P091 custody setting. Factory values are host-owned; source admission forbids operator replacement. Adoption and host ceilings are complete declarations.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`factory`](#field-factory) | `yes` | ref: `artifact-custody-policy.v1.schema.json#/properties/limits` |  |
| [`host-ceilings`](#field-host-ceilings) | `yes` | ref: `artifact-custody-policy.v1.schema.json#/properties/limits` |  |
| [`adoption`](#field-adoption) | `yes` | ref: `artifact-custody-policy.v1.schema.json` |  |
## Field Semantics

<a id="field-factory"></a>
## `factory`

- Required: `yes`
- Shape: ref: `artifact-custody-policy.v1.schema.json#/properties/limits`

<a id="field-host-ceilings"></a>
## `host-ceilings`

- Required: `yes`
- Shape: ref: `artifact-custody-policy.v1.schema.json#/properties/limits`

<a id="field-adoption"></a>
## `adoption`

- Required: `yes`
- Shape: ref: `artifact-custody-policy.v1.schema.json`
