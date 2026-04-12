# Capability Passport Present v1

Source schema: [`doc/schemas/capability-passport-present.v1.schema.json`](../../schemas/capability-passport-present.v1.schema.json)

Wire envelope used to present a capability passport during a peer protocol exchange. The `passport` field carries the full signed `capability-passport.v1` artifact; the outer `schema` field identifies this envelope format.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/60-solutions/capability-advertisement.md`](../../project/60-solutions/capability-advertisement.md)
- [`doc/project/60-solutions/node.md`](../../project/60-solutions/node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport-present.v1` | Schema discriminator. Must equal `capability-passport-present.v1`. |
| [`passport`](#field-passport) | `yes` | object | The complete signed capability passport. Must conform to `capability-passport.v1`. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-present.v1`

Schema discriminator. Must equal `capability-passport-present.v1`.

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: object

The complete signed capability passport. Must conform to `capability-passport.v1`.
