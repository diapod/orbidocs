# Org Custody Policy v1

Source schema: [`doc/schemas/org-custody-policy.v1.schema.json`](../../schemas/org-custody-policy.v1.schema.json)

Public policy artifact describing which participants or keys may authorize organization-scoped Agora authority actions, and whether authorization is any-authorized or threshold-based. The artifact is referenced by an Agora authority root via custody_policy_ref and is evaluated fail-closed by the local relay.

## Governing Basis

- [`doc/project/60-solutions/008-agora/008-agora.md`](../../project/60-solutions/008-agora/008-agora.md)
- [`doc/project/60-solutions/008-agora/008-agora-dir-simplify-impl.md`](../../project/60-solutions/008-agora/008-agora-dir-simplify-impl.md)

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
| [`schema`](#field-schema) | `yes` | const: `org-custody-policy.v1` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string | Stable local or federated reference used by authority roots. |
| [`org/id`](#field-org-id) | `yes` | string | Organization identity governed by this policy. |
| [`accepted/delegation_schema`](#field-accepted-delegation-schema) | `yes` | const: `key-delegation.v1` | Delegation proof schema accepted by M2b Agora authority checks. |
| [`rules`](#field-rules) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`rule`](#def-rule) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `org-custody-policy.v1`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

Stable local or federated reference used by authority roots.

<a id="field-org-id"></a>
## `org/id`

- Required: `yes`
- Shape: string

Organization identity governed by this policy.

<a id="field-accepted-delegation-schema"></a>
## `accepted/delegation_schema`

- Required: `yes`
- Shape: const: `key-delegation.v1`

Delegation proof schema accepted by M2b Agora authority checks.

<a id="field-rules"></a>
## `rules`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-rule"></a>
## `$defs.rule`

- Shape: object
