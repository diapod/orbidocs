# Responsibility-maintenance-report.local.v2

Source schema: [`doc/schemas/responsibility-maintenance-report.local.v2.schema.json`](../../schemas/responsibility-maintenance-report.local.v2.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `responsibility-maintenance-report.local.v2` |  |
| [`profile`](#field-profile) | `yes` | const: `responsibility.maintenance-shadow.v2` |  |
| [`scope`](#field-scope) | `yes` | const: `inactive-maintenance-and-shadow-only` |  |
| [`run/id`](#field-run-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`bindings`](#field-bindings) | `yes` | ref: `responsibility-maintenance-bindings.local.v2.schema.json` |  |
| [`cases`](#field-cases) | `yes` | array |  |
| [`exclusions`](#field-exclusions) | `yes` | const: `['v2-authoritative-reads', 'v2-participant-writers', 'lifecycle-suspension-runtime', 'D7-opening', 'encrypted-backup-restore', 'distributed-clone-fencing', 'general-case-retention', 'full-P051-010', 'full-P051-006-007-008-015-016', 'federation', 'real-participant-sanctions', 'release-readiness']` |  |
| [`safety`](#field-safety) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety` |  |
| [`capture`](#field-capture) | `no` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Artifact` | Required by the Q qualifier. Optional only for historical pre-run draft conformance examples. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-maintenance-report.local.v2`

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: const: `responsibility.maintenance-shadow.v2`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: const: `inactive-maintenance-and-shadow-only`

<a id="field-run-id"></a>
## `run/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-bindings"></a>
## `bindings`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-bindings.local.v2.schema.json`

<a id="field-cases"></a>
## `cases`

- Required: `yes`
- Shape: array

<a id="field-exclusions"></a>
## `exclusions`

- Required: `yes`
- Shape: const: `['v2-authoritative-reads', 'v2-participant-writers', 'lifecycle-suspension-runtime', 'D7-opening', 'encrypted-backup-restore', 'distributed-clone-fencing', 'general-case-retention', 'full-P051-010', 'full-P051-006-007-008-015-016', 'federation', 'real-participant-sanctions', 'release-readiness']`

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety`

<a id="field-capture"></a>
## `capture`

- Required: `no`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Artifact`

Required by the Q qualifier. Optional only for historical pre-run draft conformance examples.
