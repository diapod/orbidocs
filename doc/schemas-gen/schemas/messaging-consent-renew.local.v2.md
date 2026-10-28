# Messaging Consent Renew Local v2

Source schema: [`doc/schemas/messaging-consent-renew.local.v2.schema.json`](../../schemas/messaging-consent-renew.local.v2.schema.json)

Host-only preflight request; a waiting response may carry signed status activation time as retry/at.

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

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`request`](#def-request) | object |  |
| [`result`](#def-result) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-request"></a>
## `$defs.request`

- Shape: object

<a id="def-result"></a>
## `$defs.result`

- Shape: object
