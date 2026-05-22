# Relationship Policy Decision v1

Source schema: [`doc/schemas/relationship-policy-decision.v1.schema.json`](../../schemas/relationship-policy-decision.v1.schema.json)

Host-bound decision for a concrete relationship-derived policy evaluation. This is the only relationship policy object returned to middleware.

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
| [`schema`](#field-schema) | `yes` | const: `relationship-policy-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`decision/id`](#field-decision-id) | `yes` | string |  |
| [`predicate/ref`](#field-predicate-ref) | `yes` | string |  |
| [`candidate/ref`](#field-candidate-ref) | `no` | string \| null |  |
| [`decision`](#field-decision) | `yes` | enum: `allow`, `deny`, `quarantine`, `require-operator` |  |
| [`reason/code`](#field-reason-code) | `yes` | enum: `matched`, `no-binding`, `no-membership`, `status-mismatch`, `scope-conflict`, `expired-evidence`, `caller-not-authorized`, `operator-approval-required`, `policy-denied` |  |
| [`action/kind`](#field-action-kind) | `yes` | ref: `relationship-policy-predicate.v1.schema.json#/$defs/action_kind` |  |
| [`effect/scope`](#field-effect-scope) | `yes` | ref: `relationship-policy-predicate.v1.schema.json#/$defs/effect_scope` |  |
| [`evidence/ref`](#field-evidence-ref) | `yes` | array |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`decided/by`](#field-decided-by) | `yes` | string |  |
| [`decided/at`](#field-decided-at) | `yes` | string |  |
| [`tx/id`](#field-tx-id) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `relationship-policy-decision.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-decision-id"></a>
## `decision/id`

- Required: `yes`
- Shape: string

<a id="field-predicate-ref"></a>
## `predicate/ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-ref"></a>
## `candidate/ref`

- Required: `no`
- Shape: string | null

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `allow`, `deny`, `quarantine`, `require-operator`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: enum: `matched`, `no-binding`, `no-membership`, `status-mismatch`, `scope-conflict`, `expired-evidence`, `caller-not-authorized`, `operator-approval-required`, `policy-denied`

<a id="field-action-kind"></a>
## `action/kind`

- Required: `yes`
- Shape: ref: `relationship-policy-predicate.v1.schema.json#/$defs/action_kind`

<a id="field-effect-scope"></a>
## `effect/scope`

- Required: `yes`
- Shape: ref: `relationship-policy-predicate.v1.schema.json#/$defs/effect_scope`

<a id="field-evidence-ref"></a>
## `evidence/ref`

- Required: `yes`
- Shape: array

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-decided-by"></a>
## `decided/by`

- Required: `yes`
- Shape: string

<a id="field-decided-at"></a>
## `decided/at`

- Required: `yes`
- Shape: string

<a id="field-tx-id"></a>
## `tx/id`

- Required: `yes`
- Shape: string
