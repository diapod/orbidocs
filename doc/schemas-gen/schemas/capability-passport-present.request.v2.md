# Capability Passport Present Request v2

Source schema: [`doc/schemas/capability-passport-present.request.v2.schema.json`](../../schemas/capability-passport-present.request.v2.schema.json)

Bounded exact-passport peer renewal request; legacy unschematized V1 request is unchanged.

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)

## Project Lineage

### Requirements

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
| [`schema`](#field-schema) | `yes` | const: `capability-passport-present.request.v2` |  |
| [`passport/id`](#field-passport-id) | `yes` | string |  |
| [`status/acquisition`](#field-status-acquisition) | `yes` | enum: `cached-only`, `allow-owned-fetch` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-present.request.v2`

<a id="field-passport-id"></a>
## `passport/id`

- Required: `yes`
- Shape: string

<a id="field-status-acquisition"></a>
## `status/acquisition`

- Required: `yes`
- Shape: enum: `cached-only`, `allow-owned-fetch`
