# Participant-restriction-lifecycles.v2

Source schema: [`doc/schemas/participant-restriction-lifecycles.v2.schema.json`](../../schemas/participant-restriction-lifecycles.v2.schema.json)

Draft local contract. Shape validation confers no admission, mandate, application receipt or lifecycle readiness.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md`](../../project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `participant-restriction-lifecycles.v2` |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`lifecycles`](#field-lifecycles) | `yes` | object |  |
| [`quarantine`](#field-quarantine) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `participant-restriction-lifecycles.v2`

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-lifecycles"></a>
## `lifecycles`

- Required: `yes`
- Shape: object

<a id="field-quarantine"></a>
## `quarantine`

- Required: `yes`
- Shape: object
