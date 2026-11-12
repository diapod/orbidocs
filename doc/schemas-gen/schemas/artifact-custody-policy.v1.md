# Artifact-custody-policy.v1

Source schema: [`doc/schemas/artifact-custody-policy.v1.schema.json`](../../schemas/artifact-custody-policy.v1.schema.json)

Complete inactive-by-default P091 policy declaration. The factory digest covers normative factory fields only; admission and current host ceilings are separate.

## Governing Basis

- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-custody-policy.v1` |  |
| [`enabled`](#field-enabled) | `yes` | boolean |  |
| [`factory-digest`](#field-factory-digest) | `yes` | string |  |
| [`limits`](#field-limits) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-custody-policy.v1`

<a id="field-enabled"></a>
## `enabled`

- Required: `yes`
- Shape: boolean

<a id="field-factory-digest"></a>
## `factory-digest`

- Required: `yes`
- Shape: string

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object
