# Panel-input-statement.local.v1

Source schema: [`doc/schemas/panel-input-statement.local.v1.schema.json`](../../schemas/panel-input-statement.local.v1.schema.json)

Explicit synthetic local candidate input. Signature and publication do not grant admission; host binding, input owner, test allowlist and CAS remain mandatory.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`statement`](#field-statement) | `yes` | object |  |
| [`algorithm`](#field-algorithm) | `yes` | const: `ed25519+domain-v1` |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-statement"></a>
## `statement`

- Required: `yes`
- Shape: object

<a id="field-algorithm"></a>
## `algorithm`

- Required: `yes`
- Shape: const: `ed25519+domain-v1`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
