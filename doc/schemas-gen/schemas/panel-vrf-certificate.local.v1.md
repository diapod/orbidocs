# Panel-vrf-certificate.local.v1

Source schema: [`doc/schemas/panel-vrf-certificate.local.v1.schema.json`](../../schemas/panel-vrf-certificate.local.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `panel-vrf-certificate.local.v1` |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`coordinator/id`](#field-coordinator-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`suite`](#field-suite) | `yes` | const: `ECVRF-EDWARDS25519-SHA512-TAI` |  |
| [`public-key`](#field-public-key) | `yes` | string |  |
| [`valid-from`](#field-valid-from) | `yes` | string |  |
| [`valid-until`](#field-valid-until) | `yes` | string |  |
| [`algorithm`](#field-algorithm) | `yes` | const: `ed25519+domain-v1` |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `panel-vrf-certificate.local.v1`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: string

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: string

<a id="field-coordinator-id"></a>
## `coordinator/id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-suite"></a>
## `suite`

- Required: `yes`
- Shape: const: `ECVRF-EDWARDS25519-SHA512-TAI`

<a id="field-public-key"></a>
## `public-key`

- Required: `yes`
- Shape: string

<a id="field-valid-from"></a>
## `valid-from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid-until`

- Required: `yes`
- Shape: string

<a id="field-algorithm"></a>
## `algorithm`

- Required: `yes`
- Shape: const: `ed25519+domain-v1`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
