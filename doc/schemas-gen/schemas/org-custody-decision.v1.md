# Org Custody Decision v1

Source schema: [`doc/schemas/org-custody-decision.v1.schema.json`](../../schemas/org-custody-decision.v1.schema.json)

Signed quorum bundle authorizing one organization-scoped Agora authority action under an org-custody-policy.v1 threshold rule. It is carried inline with the key-delegation proof so verifiers can fail closed without an extra network lookup.

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
| [`schema`](#field-schema) | `yes` | const: `org-custody-decision.v1` |  |
| [`decision/id`](#field-decision-id) | `yes` | string |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`org/id`](#field-org-id) | `yes` | string |  |
| [`purpose`](#field-purpose) | `yes` | enum: `agora-authority` |  |
| [`topic/key`](#field-topic-key) | `yes` | string |  |
| [`target/record_digest`](#field-target-record-digest) | `yes` | string | Digest of the target Agora record with the embedded org custody decision removed from signature.key/delegation, avoiding recursive self-reference. |
| [`delegation/id`](#field-delegation-id) | `no` | string |  |
| [`decided-at`](#field-decided-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | unspecified |  |
| [`signatures`](#field-signatures) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `org-custody-decision.v1`

<a id="field-decision-id"></a>
## `decision/id`

- Required: `yes`
- Shape: string

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-org-id"></a>
## `org/id`

- Required: `yes`
- Shape: string

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: enum: `agora-authority`

<a id="field-topic-key"></a>
## `topic/key`

- Required: `yes`
- Shape: string

<a id="field-target-record-digest"></a>
## `target/record_digest`

- Required: `yes`
- Shape: string

Digest of the target Agora record with the embedded org custody decision removed from signature.key/delegation, avoiding recursive self-reference.

<a id="field-delegation-id"></a>
## `delegation/id`

- Required: `no`
- Shape: string

<a id="field-decided-at"></a>
## `decided-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: unspecified

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
