# Relationship Policy Candidate v1

Source schema: [`doc/schemas/relationship-policy-candidate.v1.schema.json`](../../schemas/relationship-policy-candidate.v1.schema.json)

Host-internal eligibility read model produced while evaluating relationship-derived policy. A candidate is diagnostic input, not authority.

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
| [`schema`](#field-schema) | `yes` | const: `relationship-policy-candidate.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`candidate/id`](#field-candidate-id) | `yes` | string |  |
| [`predicate/ref`](#field-predicate-ref) | `yes` | string |  |
| [`contact/ref`](#field-contact-ref) | `yes` | string |  |
| [`class/id`](#field-class-id) | `yes` | ref: `relationship-class.v1.schema.json#/$defs/class_id` |  |
| [`relationship/fact-id`](#field-relationship-fact-id) | `yes` | string |  |
| [`local/operator-ref`](#field-local-operator-ref) | `yes` | string |  |
| [`remote/operator-ref`](#field-remote-operator-ref) | `no` | string |  |
| [`participant/ref`](#field-participant-ref) | `no` | string |  |
| [`node/ref`](#field-node-ref) | `no` | string |  |
| [`node-operator-binding/ref`](#field-node-operator-binding-ref) | `no` | string |  |
| [`evidence/ref`](#field-evidence-ref) | `yes` | array |  |
| [`action/kind`](#field-action-kind) | `yes` | ref: `relationship-policy-predicate.v1.schema.json#/$defs/action_kind` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`candidate/effects`](#field-candidate-effects) | `yes` | array |  |
| [`limits`](#field-limits) | `yes` | ref: `relationship-policy-predicate.v1.schema.json#/$defs/limits` |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`decision/hint`](#field-decision-hint) | `yes` | enum: `eligible`, `quarantine`, `deny` |  |
| [`as-of-tx/id`](#field-as-of-tx-id) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`candidate_effect`](#def-candidate-effect) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `relationship-policy-candidate.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-candidate-id"></a>
## `candidate/id`

- Required: `yes`
- Shape: string

<a id="field-predicate-ref"></a>
## `predicate/ref`

- Required: `yes`
- Shape: string

<a id="field-contact-ref"></a>
## `contact/ref`

- Required: `yes`
- Shape: string

<a id="field-class-id"></a>
## `class/id`

- Required: `yes`
- Shape: ref: `relationship-class.v1.schema.json#/$defs/class_id`

<a id="field-relationship-fact-id"></a>
## `relationship/fact-id`

- Required: `yes`
- Shape: string

<a id="field-local-operator-ref"></a>
## `local/operator-ref`

- Required: `yes`
- Shape: string

<a id="field-remote-operator-ref"></a>
## `remote/operator-ref`

- Required: `no`
- Shape: string

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `no`
- Shape: string

<a id="field-node-ref"></a>
## `node/ref`

- Required: `no`
- Shape: string

<a id="field-node-operator-binding-ref"></a>
## `node-operator-binding/ref`

- Required: `no`
- Shape: string

<a id="field-evidence-ref"></a>
## `evidence/ref`

- Required: `yes`
- Shape: array

<a id="field-action-kind"></a>
## `action/kind`

- Required: `yes`
- Shape: ref: `relationship-policy-predicate.v1.schema.json#/$defs/action_kind`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-effects"></a>
## `candidate/effects`

- Required: `yes`
- Shape: array

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `relationship-policy-predicate.v1.schema.json#/$defs/limits`

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-decision-hint"></a>
## `decision/hint`

- Required: `yes`
- Shape: enum: `eligible`, `quarantine`, `deny`

<a id="field-as-of-tx-id"></a>
## `as-of-tx/id`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-candidate-effect"></a>
## `$defs.candidate_effect`

- Shape: object
