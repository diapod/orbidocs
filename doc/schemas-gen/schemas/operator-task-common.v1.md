# P094 Operator Task Pack Common Contract v1

Source schema: [`doc/schemas/operator-task-common.v1.schema.json`](../../schemas/operator-task-common.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string | Logical `prefix:name` reference. Never a POSIX or Windows filesystem path, URL path, or shell text. |
| [`digest`](#def-digest) | string |  |
| [`counter`](#def-counter) | integer |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`name`](#def-name) | string |  |
| [`capabilityId`](#def-capabilityid) | string |  |
| [`exactRef`](#def-exactref) | object |  |
| [`refs`](#def-refs) | array |  |
| [`hilMode`](#def-hilmode) | enum: `each-step`, `each-mutation` |  |
| [`runtimeNetwork`](#def-runtimenetwork) | enum: `none`, `isolated` |  |
| [`impactClass`](#def-impactclass) | enum: `research`, `experimental`, `test`, `production`, `critical` |  |
| [`bindingState`](#def-bindingstate) | enum: `enabled`, `paused` |  |
| [`stage`](#def-stage) | enum: `package`, `binding`, `environment`, `deliberation`, `effects`, `verification`, `rollback`, `publication` |  |
| [`refusalStage`](#def-refusalstage) | enum: `package`, `binding`, `environment`, `deliberation`, `effects`, `verification`, `rollback`, `publication`, `run` |  |
| [`stageState`](#def-stagestate) | enum: `ready`, `degraded`, `blocked`, `not-applicable`, `not-evaluated` |  |
| [`retryClass`](#def-retryclass) | enum: `terminal`, `after-operator-action`, `after-deferred-operation`, `after-owner-reconcile`, `transient` |  |
| [`nextAction`](#def-nextaction) | enum: `activate-package`, `create-binding`, `edit-binding`, `grant-capability`, `grant-interface`, `inspect-attention-budget`, `inspect-capability`, `inspect-deliberation`, `inspect-effects`, `inspect-environment`, `inspect-package`, `inspect-verification`, `none`, `prepare-environment`, `rebind-operator`, `resolve-binding-sources`, `resume-binding`, `retry-verification`, `review-profile-change`, `run-conformance`, `start-new-run` |  |
| [`refusalCode`](#def-refusalcode) | enum: `package/not-active`, `package/conformance-missing`, `package/profile-digest-mismatch`, `operator/binding-lost`, `local-binding/missing`, `local-binding/incomplete`, `local-binding/outside-package-ceiling`, `local-binding/profile-changed`, `local-binding/conflict`, `local-binding/paused`, `environment/image-mismatch`, `environment/prepared-system-unavailable`, `environment/runtime-egress-denied`, `environment/impact-class-exceeded`, `environment/not-contained`, `deliberation/flow-unavailable`, `capability/missing`, `capability/revoked`, `workbench/command-profile-missing`, `workbench/effect-mode-missing`, `interface/grant-missing`, `hil/attention-unavailable`, `verifier/unavailable`, `verifier/effect-mode-missing`, `rollback/unavailable`, `rollback/destroy-unconfirmed`, `publication/policy-missing`, `publication/disabled`, `offer/withdrawal-pending`, `package/generation-stale`, `plan/unknown-action-kind`, `plan/outside-profile`, `plan/first-step-not-observation`, `plan/recovery-class-not-admitted`, `plan/changed-replay`, `workbench/patch-outside-policy`, `interface/lease-lost`, `hil/denied`, `hil/expired`, `verifier/check-missing`, `verifier/mutation-not-admitted`, `verifier/timeout`, `run/cancelled`, `run/budget-exhausted` | Closed P094 refusal vocabulary; the proposal's refusal table is the source of truth and a drift check keeps them equal. |
| [`stepClass`](#def-stepclass) | enum: `observation`, `contained-mutation` | Version 1 admits only these classes; other effects refuse with plan/recovery-class-not-admitted. |
| [`effectSource`](#def-effectsource) | enum: `owner-enforced`, `missing-source-default` |  |
| [`argvAtom`](#def-argvatom) | string |  |
| [`arguments`](#def-arguments) | array |  |
| [`deliberationLimits`](#def-deliberationlimits) | object |  |
| [`candidateStep`](#def-candidatestep) | unspecified |  |
| [`planStep`](#def-planstep) | unspecified | Host-validated step. In Version 1 a mutation is always contained and always needs HIL, and only an owner-enforced source can yield observation. |
| [`stageReport`](#def-stagereport) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

Logical `prefix:name` reference. Never a POSIX or Windows filesystem path, URL path, or shell text.

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-counter"></a>
## `$defs.counter`

- Shape: integer

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-name"></a>
## `$defs.name`

- Shape: string

<a id="def-capabilityid"></a>
## `$defs.capabilityId`

- Shape: string

<a id="def-exactref"></a>
## `$defs.exactRef`

- Shape: object

<a id="def-refs"></a>
## `$defs.refs`

- Shape: array

<a id="def-hilmode"></a>
## `$defs.hilMode`

- Shape: enum: `each-step`, `each-mutation`

<a id="def-runtimenetwork"></a>
## `$defs.runtimeNetwork`

- Shape: enum: `none`, `isolated`

<a id="def-impactclass"></a>
## `$defs.impactClass`

- Shape: enum: `research`, `experimental`, `test`, `production`, `critical`

<a id="def-bindingstate"></a>
## `$defs.bindingState`

- Shape: enum: `enabled`, `paused`

<a id="def-stage"></a>
## `$defs.stage`

- Shape: enum: `package`, `binding`, `environment`, `deliberation`, `effects`, `verification`, `rollback`, `publication`

<a id="def-refusalstage"></a>
## `$defs.refusalStage`

- Shape: enum: `package`, `binding`, `environment`, `deliberation`, `effects`, `verification`, `rollback`, `publication`, `run`

<a id="def-stagestate"></a>
## `$defs.stageState`

- Shape: enum: `ready`, `degraded`, `blocked`, `not-applicable`, `not-evaluated`

<a id="def-retryclass"></a>
## `$defs.retryClass`

- Shape: enum: `terminal`, `after-operator-action`, `after-deferred-operation`, `after-owner-reconcile`, `transient`

<a id="def-nextaction"></a>
## `$defs.nextAction`

- Shape: enum: `activate-package`, `create-binding`, `edit-binding`, `grant-capability`, `grant-interface`, `inspect-attention-budget`, `inspect-capability`, `inspect-deliberation`, `inspect-effects`, `inspect-environment`, `inspect-package`, `inspect-verification`, `none`, `prepare-environment`, `rebind-operator`, `resolve-binding-sources`, `resume-binding`, `retry-verification`, `review-profile-change`, `run-conformance`, `start-new-run`

<a id="def-refusalcode"></a>
## `$defs.refusalCode`

- Shape: enum: `package/not-active`, `package/conformance-missing`, `package/profile-digest-mismatch`, `operator/binding-lost`, `local-binding/missing`, `local-binding/incomplete`, `local-binding/outside-package-ceiling`, `local-binding/profile-changed`, `local-binding/conflict`, `local-binding/paused`, `environment/image-mismatch`, `environment/prepared-system-unavailable`, `environment/runtime-egress-denied`, `environment/impact-class-exceeded`, `environment/not-contained`, `deliberation/flow-unavailable`, `capability/missing`, `capability/revoked`, `workbench/command-profile-missing`, `workbench/effect-mode-missing`, `interface/grant-missing`, `hil/attention-unavailable`, `verifier/unavailable`, `verifier/effect-mode-missing`, `rollback/unavailable`, `rollback/destroy-unconfirmed`, `publication/policy-missing`, `publication/disabled`, `offer/withdrawal-pending`, `package/generation-stale`, `plan/unknown-action-kind`, `plan/outside-profile`, `plan/first-step-not-observation`, `plan/recovery-class-not-admitted`, `plan/changed-replay`, `workbench/patch-outside-policy`, `interface/lease-lost`, `hil/denied`, `hil/expired`, `verifier/check-missing`, `verifier/mutation-not-admitted`, `verifier/timeout`, `run/cancelled`, `run/budget-exhausted`

Closed P094 refusal vocabulary; the proposal's refusal table is the source of truth and a drift check keeps them equal.

<a id="def-stepclass"></a>
## `$defs.stepClass`

- Shape: enum: `observation`, `contained-mutation`

Version 1 admits only these classes; other effects refuse with plan/recovery-class-not-admitted.

<a id="def-effectsource"></a>
## `$defs.effectSource`

- Shape: enum: `owner-enforced`, `missing-source-default`

<a id="def-argvatom"></a>
## `$defs.argvAtom`

- Shape: string

<a id="def-arguments"></a>
## `$defs.arguments`

- Shape: array

<a id="def-deliberationlimits"></a>
## `$defs.deliberationLimits`

- Shape: object

<a id="def-candidatestep"></a>
## `$defs.candidateStep`

- Shape: unspecified

<a id="def-planstep"></a>
## `$defs.planStep`

- Shape: unspecified

Host-validated step. In Version 1 a mutation is always contained and always needs HIL, and only an owner-enforced source can yield observation.

<a id="def-stagereport"></a>
## `$defs.stageReport`

- Shape: object
