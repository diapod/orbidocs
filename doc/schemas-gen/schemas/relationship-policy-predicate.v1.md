# Relationship Policy Predicate v1

Source schema: [`doc/schemas/relationship-policy-predicate.v1.schema.json`](../../schemas/relationship-policy-predicate.v1.schema.json)

Declarative relationship-derived policy requirement. Predicates are conditions the host evaluates; they are not authority grants.

## Governing Basis

- [`doc/project/40-proposals/065-local-relationship-layer.md`](../../project/40-proposals/065-local-relationship-layer.md)
- [`doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
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
| [`schema`](#field-schema) | `yes` | const: `relationship-policy-predicate.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`predicate/id`](#field-predicate-id) | `yes` | string |  |
| [`predicate/kind`](#field-predicate-kind) | `yes` | enum: `operator-relationship-class` |  |
| [`local/operator-ref`](#field-local-operator-ref) | `no` | string |  |
| [`remote/operator-binding-ref`](#field-remote-operator-binding-ref) | `no` | string |  |
| [`required/class-ids`](#field-required-class-ids) | `yes` | array | Match succeeds when the candidate membership is in any of these classes. Order is irrelevant; presence in the list is enough. This is how composable trust gradation predicates are expressed without introducing a linear-ordering operator. |
| [`required/status`](#field-required-status) | `yes` | ref: `relationship-membership-fact.v1.schema.json#/$defs/membership_status` |  |
| [`action/kind`](#field-action-kind) | `yes` | ref: `#/$defs/action_kind` |  |
| [`effect/scope`](#field-effect-scope) | `yes` | ref: `#/$defs/effect_scope` |  |
| [`ttl`](#field-ttl) | `no` | integer |  |
| [`failure/mode`](#field-failure-mode) | `yes` | enum: `deny`, `require-operator`, `quarantine` |  |
| [`declared/by`](#field-declared-by) | `yes` | string |  |
| [`limits`](#field-limits) | `no` | ref: `#/$defs/limits` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`action_kind`](#def-action-kind) | string |  |
| [`effect_scope`](#def-effect-scope) | string |  |
| [`limits`](#def-limits) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `relationship-policy-predicate.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-predicate-id"></a>
## `predicate/id`

- Required: `yes`
- Shape: string

<a id="field-predicate-kind"></a>
## `predicate/kind`

- Required: `yes`
- Shape: enum: `operator-relationship-class`

<a id="field-local-operator-ref"></a>
## `local/operator-ref`

- Required: `no`
- Shape: string

<a id="field-remote-operator-binding-ref"></a>
## `remote/operator-binding-ref`

- Required: `no`
- Shape: string

<a id="field-required-class-ids"></a>
## `required/class-ids`

- Required: `yes`
- Shape: array

Match succeeds when the candidate membership is in any of these classes. Order is irrelevant; presence in the list is enough. This is how composable trust gradation predicates are expressed without introducing a linear-ordering operator.

<a id="field-required-status"></a>
## `required/status`

- Required: `yes`
- Shape: ref: `relationship-membership-fact.v1.schema.json#/$defs/membership_status`

<a id="field-action-kind"></a>
## `action/kind`

- Required: `yes`
- Shape: ref: `#/$defs/action_kind`

<a id="field-effect-scope"></a>
## `effect/scope`

- Required: `yes`
- Shape: ref: `#/$defs/effect_scope`

<a id="field-ttl"></a>
## `ttl`

- Required: `no`
- Shape: integer

<a id="field-failure-mode"></a>
## `failure/mode`

- Required: `yes`
- Shape: enum: `deny`, `require-operator`, `quarantine`

<a id="field-declared-by"></a>
## `declared/by`

- Required: `yes`
- Shape: string

<a id="field-limits"></a>
## `limits`

- Required: `no`
- Shape: ref: `#/$defs/limits`

## Definition Semantics

<a id="def-action-kind"></a>
## `$defs.action_kind`

- Shape: string

<a id="def-effect-scope"></a>
## `$defs.effect_scope`

- Shape: string

<a id="def-limits"></a>
## `$defs.limits`

- Shape: object
