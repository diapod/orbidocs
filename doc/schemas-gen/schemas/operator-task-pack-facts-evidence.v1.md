# Operator Task Pack Facts Evidence v1

Source schema: [`doc/schemas/operator-task-pack-facts-evidence.v1.schema.json`](../../schemas/operator-task-pack-facts-evidence.v1.schema.json)

Host evidence that the pack facts of one task profile bound by one P085 package were recomputed from owner sources at conformance, rather than taken from the author. It binds the exact package, profile and host action-semantics map, and lists every recomputed asset digest with the rule that produced it. It carries no asset bytes, secrets or local paths. P085 stores it as domain conformance evidence addressed by SHA-256 over its JCS v1 canonical JSON; a passing result is required before the package's conformance report can be recorded, and a revised host map makes it stale.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

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
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-pack-facts-evidence.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `yes` | string | P085 package artifact digest in its lowercase hex form; it is not interchangeable with the base64url content addresses below. |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/revision`](#field-task-profile-revision) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`action-semantics/ref`](#field-action-semantics-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`action-semantics/revision`](#field-action-semantics-revision) | `yes` | integer |  |
| [`action-semantics/digest`](#field-action-semantics-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`sources`](#field-sources) | `yes` | array |  |
| [`admitted-actions`](#field-admitted-actions) | `yes` | array |  |
| [`required-capability/ids`](#field-required-capability-ids) | `yes` | array |  |
| [`result`](#field-result) | `yes` | enum: `passed`, `failed` |  |
| [`mismatches`](#field-mismatches) | `yes` | array |  |
| [`evaluated-at`](#field-evaluated-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`refusal-coverage`](#field-refusal-coverage) | `no` | object | Registered refusal codes the profile's refusal corpus names and those it does not, in refusal-table order (`P094-010e`). Recorded, never required. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`slot`](#def-slot) | enum: `thematic-profile`, `catalog/offer-template`, `catalog/taxonomy`, `deliberation/inference-flow`, `deliberation/agent-policy`, `environment/image-variants`, `environment/prepared-system`, `workbench/command-profiles`, `workbench/patch-policy`, `interfaces/observation-descriptors`, `interfaces/actuation-descriptors`, `experiment/input-schema`, `experiment/candidate-schema`, `verifier`, `verifier/command-profile`, `verifier/result-schema`, `rollback`, `resource-envelope`, `refusal-corpus` |  |
| [`source`](#def-source) | object |  |
| [`action`](#def-action) | object |  |
| [`mismatch`](#def-mismatch) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "result": {
      "const": "passed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "mismatches": {
      "maxItems": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "result": {
      "const": "failed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "mismatches": {
      "minItems": 1
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-pack-facts-evidence.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `yes`
- Shape: string

P085 package artifact digest in its lowercase hex form; it is not interchangeable with the base64url content addresses below.

<a id="field-task-profile-ref"></a>
## `task-profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-revision"></a>
## `task-profile/revision`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-action-semantics-ref"></a>
## `action-semantics/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-action-semantics-revision"></a>
## `action-semantics/revision`

- Required: `yes`
- Shape: integer

<a id="field-action-semantics-digest"></a>
## `action-semantics/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-sources"></a>
## `sources`

- Required: `yes`
- Shape: array

<a id="field-admitted-actions"></a>
## `admitted-actions`

- Required: `yes`
- Shape: array

<a id="field-required-capability-ids"></a>
## `required-capability/ids`

- Required: `yes`
- Shape: array

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: enum: `passed`, `failed`

<a id="field-mismatches"></a>
## `mismatches`

- Required: `yes`
- Shape: array

<a id="field-evaluated-at"></a>
## `evaluated-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-refusal-coverage"></a>
## `refusal-coverage`

- Required: `no`
- Shape: object

Registered refusal codes the profile's refusal corpus names and those it does not, in refusal-table order (`P094-010e`). Recorded, never required.

## Definition Semantics

<a id="def-slot"></a>
## `$defs.slot`

- Shape: enum: `thematic-profile`, `catalog/offer-template`, `catalog/taxonomy`, `deliberation/inference-flow`, `deliberation/agent-policy`, `environment/image-variants`, `environment/prepared-system`, `workbench/command-profiles`, `workbench/patch-policy`, `interfaces/observation-descriptors`, `interfaces/actuation-descriptors`, `experiment/input-schema`, `experiment/candidate-schema`, `verifier`, `verifier/command-profile`, `verifier/result-schema`, `rollback`, `resource-envelope`, `refusal-corpus`

<a id="def-source"></a>
## `$defs.source`

- Shape: object

<a id="def-action"></a>
## `$defs.action`

- Shape: object

<a id="def-mismatch"></a>
## `$defs.mismatch`

- Shape: object
