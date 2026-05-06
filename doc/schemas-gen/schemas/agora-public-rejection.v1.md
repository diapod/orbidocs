# Agora Public Rejection v1

Source schema: [`doc/schemas/agora-public-rejection.v1.schema.json`](../../schemas/agora-public-rejection.v1.schema.json)

Redacted public policy-decision receipt for an Agora admission rejection that already targeted a public surface. This is not the operator-local rejection feed and must not expose passport ids, participant ids denied by policy, delegation internals, or revocation-source details.

## Governing Basis

- [`doc/project/60-solutions/008-agora/008-agora.md`](../../project/60-solutions/008-agora/008-agora.md)
- [`doc/project/60-solutions/021-agora-authority/021-agora-authority.md`](../../project/60-solutions/021-agora-authority/021-agora-authority.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-008-org-subject-rollout.md`](../../project/50-requirements/requirements-008-org-subject-rollout.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

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
| [`schema`](#field-schema) | `yes` | const: `agora-public-rejection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`rejection/id`](#field-rejection-id) | `yes` | string |  |
| [`relay/id`](#field-relay-id) | `yes` | string |  |
| [`target`](#field-target) | `yes` | object |  |
| [`decision`](#field-decision) | `yes` | object |  |
| [`policy`](#field-policy) | `yes` | object |  |
| [`observed_at`](#field-observed-at) | `yes` | ref: `#/$defs/rfc3339` |  |
| [`notes`](#field-notes) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`rfc3339`](#def-rfc3339) | string |  |
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-public-rejection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-rejection-id"></a>
## `rejection/id`

- Required: `yes`
- Shape: string

<a id="field-relay-id"></a>
## `relay/id`

- Required: `yes`
- Shape: string

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: object

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: object

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: object

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: ref: `#/$defs/rfc3339`

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-rfc3339"></a>
## `$defs.rfc3339`

- Shape: string

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
