# Responsibility-maintenance-grant.local.v1

Source schema: [`doc/schemas/responsibility-maintenance-grant.local.v1.schema.json`](../../schemas/responsibility-maintenance-grant.local.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `responsibility-maintenance-grant.local.v1` |  |
| [`host/id`](#field-host-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`operator/binding`](#field-operator-binding) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding` |  |
| [`capability/id`](#field-capability-id) | `yes` | enum: `responsibility.maintenance.inspect`, `responsibility.maintenance.prepare`, `responsibility.maintenance.abandon`, `responsibility.maintenance.verify`, `responsibility.maintenance.reconcile`, `responsibility.maintenance.compact` |  |
| [`grant/id`](#field-grant-id) | `yes` | enum: `grant/responsibility.maintenance.inspect`, `grant/responsibility.maintenance.prepare`, `grant/responsibility.maintenance.abandon`, `grant/responsibility.maintenance.verify`, `grant/responsibility.maintenance.reconcile`, `grant/responsibility.maintenance.compact` |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time` |  |
| [`expires-at`](#field-expires-at) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time` |  |
| [`safety`](#field-safety) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-maintenance-grant.local.v1`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-operator-binding"></a>
## `operator/binding`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: enum: `responsibility.maintenance.inspect`, `responsibility.maintenance.prepare`, `responsibility.maintenance.abandon`, `responsibility.maintenance.verify`, `responsibility.maintenance.reconcile`, `responsibility.maintenance.compact`

<a id="field-grant-id"></a>
## `grant/id`

- Required: `yes`
- Shape: enum: `grant/responsibility.maintenance.inspect`, `grant/responsibility.maintenance.prepare`, `grant/responsibility.maintenance.abandon`, `grant/responsibility.maintenance.verify`, `grant/responsibility.maintenance.reconcile`, `grant/responsibility.maintenance.compact`

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time`

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety`
