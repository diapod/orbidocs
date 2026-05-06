# Reputation Snapshot v1

Source schema: [`doc/schemas/reputation-snapshot.v1.schema.json`](../../schemas/reputation-snapshot.v1.schema.json)

Authority-published advisory reputation snapshot. It is a domain payload that may be carried by Agora records, files, or future reputation APIs; M3 projects community trust inputs from these records, but runtime authorization must not depend on community-trusted until a later evaluator and anti-gaming policy are explicitly designed.

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
| [`schema`](#field-schema) | `yes` | const: `reputation-snapshot.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`snapshot/id`](#field-snapshot-id) | `yes` | string |  |
| [`snapshot/period`](#field-snapshot-period) | `yes` | object |  |
| [`issuer`](#field-issuer) | `yes` | ref: `#/$defs/identityRef` |  |
| [`method/ref`](#field-method-ref) | `no` | string | Policy or method identifier used to compute the snapshot. |
| [`entries`](#field-entries) | `yes` | array |  |
| [`computed_at`](#field-computed-at) | `yes` | ref: `#/$defs/rfc3339` |  |
| [`valid_until`](#field-valid-until) | `no` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`rfc3339`](#def-rfc3339) | string |  |
| [`identityRef`](#def-identityref) | object |  |
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `reputation-snapshot.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-snapshot-id"></a>
## `snapshot/id`

- Required: `yes`
- Shape: string

<a id="field-snapshot-period"></a>
## `snapshot/period`

- Required: `yes`
- Shape: object

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: ref: `#/$defs/identityRef`

<a id="field-method-ref"></a>
## `method/ref`

- Required: `no`
- Shape: string

Policy or method identifier used to compute the snapshot.

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

<a id="field-computed-at"></a>
## `computed_at`

- Required: `yes`
- Shape: ref: `#/$defs/rfc3339`

<a id="field-valid-until"></a>
## `valid_until`

- Required: `no`
- Shape: unspecified

## Definition Semantics

<a id="def-rfc3339"></a>
## `$defs.rfc3339`

- Shape: string

<a id="def-identityref"></a>
## `$defs.identityRef`

- Shape: object

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
