# Agora-admission-source-policy.v1

Source schema: [`doc/schemas/agora-admission-source-policy.v1.schema.json`](../../schemas/agora-admission-source-policy.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)

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

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`clock-authority`](#def-clock-authority) | object |  |
| [`schema`](#def-schema) | const: `agora-admission-source-policy.v1` |  |
| [`profile-digest`](#def-profile-digest) | ref: `#/$defs/digest` |  |
| [`receipt-profile`](#def-receipt-profile) | const: `full-record` |  |
| [`receipt-key-window-seconds`](#def-receipt-key-window-seconds) | integer |  |
| [`receipt-commit-budget-seconds`](#def-receipt-commit-budget-seconds) | const: `5` |  |
| [`clock-skew-seconds`](#def-clock-skew-seconds) | integer |  |
## Field Semantics

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-clock-authority"></a>
## `$defs.clock-authority`

- Shape: object

<a id="def-schema"></a>
## `$defs.schema`

- Shape: const: `agora-admission-source-policy.v1`

<a id="def-profile-digest"></a>
## `$defs.profile-digest`

- Shape: ref: `#/$defs/digest`

<a id="def-receipt-profile"></a>
## `$defs.receipt-profile`

- Shape: const: `full-record`

<a id="def-receipt-key-window-seconds"></a>
## `$defs.receipt-key-window-seconds`

- Shape: integer

<a id="def-receipt-commit-budget-seconds"></a>
## `$defs.receipt-commit-budget-seconds`

- Shape: const: `5`

<a id="def-clock-skew-seconds"></a>
## `$defs.clock-skew-seconds`

- Shape: integer
