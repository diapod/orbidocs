# Panel-signed-command.local.v1

Source schema: [`doc/schemas/panel-signed-command.local.v1.schema.json`](../../schemas/panel-signed-command.local.v1.schema.json)

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
| [`command`](#field-command) | `yes` | ref: `panel-command.local.v1.schema.json` |  |
| [`algorithm`](#field-algorithm) | `yes` | const: `ed25519+domain-v1` |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-command"></a>
## `command`

- Required: `yes`
- Shape: ref: `panel-command.local.v1.schema.json`

<a id="field-algorithm"></a>
## `algorithm`

- Required: `yes`
- Shape: const: `ed25519+domain-v1`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
