# Seed Directory Trust v1

Source schema: [`doc/schemas/seed-directory-trust.v1.schema.json`](../../schemas/seed-directory-trust.v1.schema.json)

Local trust registry for Seed Directory endpoints. This artifact records which user-maintained or federation-endorsed Seed Directory instances a node or deployment may query, and how much local trust weight each directory receives. It is not a global registry of true directories; it is local policy input.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`](../../project/40-proposals/054-user-maintained-federated-seed-directory.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `seed-directory-trust.v1` | Schema discriminator. |
| [`directories`](#field-directories) | `yes` | array | Trusted or candidate Seed Directory entries evaluated by local policy. |
| [`policy/id`](#field-policy-id) | `no` | string | Optional local policy identifier for operator diagnostics and future query attestations. |
| [`issued-at`](#field-issued-at) | `no` | string | Optional timestamp when this local trust registry was produced. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`directory`](#def-directory) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `seed-directory-trust.v1`

Schema discriminator.

<a id="field-directories"></a>
## `directories`

- Required: `yes`
- Shape: array

Trusted or candidate Seed Directory entries evaluated by local policy.

<a id="field-policy-id"></a>
## `policy/id`

- Required: `no`
- Shape: string

Optional local policy identifier for operator diagnostics and future query attestations.

<a id="field-issued-at"></a>
## `issued-at`

- Required: `no`
- Shape: string

Optional timestamp when this local trust registry was produced.

## Definition Semantics

<a id="def-directory"></a>
## `$defs.directory`

- Shape: object
