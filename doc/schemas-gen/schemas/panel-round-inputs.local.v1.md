# Panel-round-inputs.local.v1

Source schema: [`doc/schemas/panel-round-inputs.local.v1.schema.json`](../../schemas/panel-round-inputs.local.v1.schema.json)

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
| [`candidates`](#field-candidates) | `yes` | array |  |
| [`certificate`](#field-certificate) | `yes` | ref: `panel-vrf-certificate.local.v1.schema.json` |  |
| [`heartbeat`](#field-heartbeat) | `yes` | object |  |
| [`heartbeat/class`](#field-heartbeat-class) | `yes` | const: `local-heartbeat` |  |
| [`heartbeat/cutoff-at`](#field-heartbeat-cutoff-at) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | ref: `panel-policy.local.v1.schema.json` |  |
## Field Semantics

<a id="field-candidates"></a>
## `candidates`

- Required: `yes`
- Shape: array

<a id="field-certificate"></a>
## `certificate`

- Required: `yes`
- Shape: ref: `panel-vrf-certificate.local.v1.schema.json`

<a id="field-heartbeat"></a>
## `heartbeat`

- Required: `yes`
- Shape: object

<a id="field-heartbeat-class"></a>
## `heartbeat/class`

- Required: `yes`
- Shape: const: `local-heartbeat`

<a id="field-heartbeat-cutoff-at"></a>
## `heartbeat/cutoff-at`

- Required: `yes`
- Shape: string

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: ref: `panel-policy.local.v1.schema.json`
