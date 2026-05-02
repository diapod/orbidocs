# Seed Capability Registration v1

Source schema: [`doc/schemas/seed-capability-registration.v1.schema.json`](../../schemas/seed-capability-registration.v1.schema.json)

Accepted Seed Directory capability-registration fact carried as the `content` of an `agora-record.v1` envelope when `record/kind = seed.capability-registration.accepted`. This is not a raw client request. It is the domain fact emitted after Seed Directory policy has accepted a capability passport for a target node and capability id.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/60-solutions/008-agora/008-agora.md`](../../project/60-solutions/008-agora/008-agora.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `seed-capability-registration.v1` | Schema discriminator for the accepted capability-registration fact. |
| [`node/id`](#field-node-id) | `yes` | string | Target node for which the capability passport was accepted. Must match `passport.node_id`. |
| [`capability/id`](#field-capability-id) | `yes` | string | Capability id under which the passport was accepted. Must match `passport.capability_id`. |
| [`passport`](#field-passport) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `seed-capability-registration.v1`

Schema discriminator for the accepted capability-registration fact.

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

Target node for which the capability passport was accepted. Must match `passport.node_id`.

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

Capability id under which the passport was accepted. Must match `passport.capability_id`.

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: object
