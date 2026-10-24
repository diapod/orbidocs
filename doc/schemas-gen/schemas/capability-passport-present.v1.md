# Capability Passport Present v1

Source schema: [`doc/schemas/capability-passport-present.v1.schema.json`](../../schemas/capability-passport-present.v1.schema.json)

Wire presentation retaining the complete signed passport proof. For V2 Messaging receive consent only, an optional bounded signed issuance status permits verification against an independently admitted local root without status acquisition. Unsupported consumers must not claim offline acceptance.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/60-solutions/007-capability-advertisement/007-capability-advertisement.md`](../../project/60-solutions/007-capability-advertisement/007-capability-advertisement.md)
- [`doc/project/60-solutions/000-node/000-node.md`](../../project/60-solutions/000-node/000-node.md)

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
| [`schema`](#field-schema) | `yes` | const: `capability-passport-present.v1` | Schema discriminator. Must equal `capability-passport-present.v1`. |
| [`passport`](#field-passport) | `yes` | unspecified |  |
| [`issuance/status`](#field-issuance-status) | `no` | unspecified | Exact signed status artifact for a V2 Messaging receive-consent handoff. Its serialized bytes are limited to 65536 by the carrier. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-present.v1`

Schema discriminator. Must equal `capability-passport-present.v1`.

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: unspecified

<a id="field-issuance-status"></a>
## `issuance/status`

- Required: `no`
- Shape: unspecified

Exact signed status artifact for a V2 Messaging receive-consent handoff. Its serialized bytes are limited to 65536 by the carrier.
