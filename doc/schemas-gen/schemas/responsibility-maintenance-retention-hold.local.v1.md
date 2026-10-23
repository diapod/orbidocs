# Responsibility-maintenance-retention-hold.local.v1

Source schema: [`doc/schemas/responsibility-maintenance-retention-hold.local.v1.schema.json`](../../schemas/responsibility-maintenance-retention-hold.local.v1.schema.json)

Draft local maintenance contract. Shape validation grants no authority and does not open D7.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `responsibility-maintenance-retention-hold.local.v1` |  |
| [`hold/id`](#field-hold-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/id`](#field-host-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`holder/kind`](#field-holder-kind) | `yes` | enum: `operation`, `alert`, `report` |  |
| [`holder/ref`](#field-holder-ref) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`target/digest`](#field-target-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`requirement`](#field-requirement) | `yes` | enum: `resident`, `retrievable-evidence` |  |
| [`action`](#field-action) | `yes` | enum: `acquire`, `release` |  |
| [`predecessor/digest`](#field-predecessor-digest) | `yes` | unspecified |  |
| [`reason/ref`](#field-reason-ref) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time` |  |
| [`safety`](#field-safety) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-maintenance-retention-hold.local.v1`

<a id="field-hold-id"></a>
## `hold/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-holder-kind"></a>
## `holder/kind`

- Required: `yes`
- Shape: enum: `operation`, `alert`, `report`

<a id="field-holder-ref"></a>
## `holder/ref`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-target-digest"></a>
## `target/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-requirement"></a>
## `requirement`

- Required: `yes`
- Shape: enum: `resident`, `retrievable-evidence`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `acquire`, `release`

<a id="field-predecessor-digest"></a>
## `predecessor/digest`

- Required: `yes`
- Shape: unspecified

<a id="field-reason-ref"></a>
## `reason/ref`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time`

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety`
