# Participant-restriction-lifecycle.v2

Source schema: [`doc/schemas/participant-restriction-lifecycle.v2.schema.json`](../../schemas/participant-restriction-lifecycle.v2.schema.json)

Draft local fixture contract. Shape validation confers no admission, mandate, application receipt or normative ELL2 qualification.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `participant-restriction-lifecycle.v2` |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`original`](#field-original) | `yes` | ref: `participant-restriction-source.v1.schema.json` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
| [`lifecycle`](#field-lifecycle) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `participant-restriction-lifecycle.v2`

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-original"></a>
## `original`

- Required: `yes`
- Shape: ref: `participant-restriction-source.v1.schema.json`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

<a id="field-lifecycle"></a>
## `lifecycle`

- Required: `yes`
- Shape: unspecified
