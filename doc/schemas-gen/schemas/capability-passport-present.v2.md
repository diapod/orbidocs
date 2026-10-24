# Capability Passport Present v2

Source schema: [`doc/schemas/capability-passport-present.v2.schema.json`](../../schemas/capability-passport-present.v2.schema.json)

Bounded V2 Messaging presentation; attached status is observation evidence, never authority. Canonical presentation limit: 65536 bytes. Typed admission must preserve signed subdocuments exactly as JSON values; forms that would normalize signed arrays/defaults/fields are refused.

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
| [`schema`](#field-schema) | `yes` | const: `capability-passport-present.v2` |  |
| [`passport`](#field-passport) | `yes` | ref: `capability-passport.v2.schema.json` |  |
| [`issuance/status`](#field-issuance-status) | `no` | ref: `issuance-revocation-status.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-present.v2`

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: ref: `capability-passport.v2.schema.json`

<a id="field-issuance-status"></a>
## `issuance/status`

- Required: `no`
- Shape: ref: `issuance-revocation-status.v1.schema.json`
