# Sensorium-brainflow-status.v1

Source schema: [`doc/schemas/sensorium-brainflow-status.v1.schema.json`](../../schemas/sensorium-brainflow-status.v1.schema.json)

Separate declaration/admission, process and acquisition evidence; no selectors, subject IDs, samples, exception text or inferred electrode contact quality. Cleanup uncertainty holds the claim and forbids reassignment/restart. Profile-present is not readiness or qualification. Acquisition phases match P096 section 6. Claim/fence/disposal facts are separate fields; idle, blocked and failed require proven disposal. No worker assertion establishes host authority.

## Governing Basis

- [`doc/project/40-proposals/096-sensorium-brainflow-connector.md`](../../project/40-proposals/096-sensorium-brainflow-connector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)
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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`instance/ref`](#field-instance-ref) | `yes` | object |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`configuration/state`](#field-configuration-state) | `yes` | enum: `declared`, `admitted`, `resolved`, `refused` |  |
| [`supervisor/state`](#field-supervisor-state) | `yes` | enum: `configured`, `starting`, `ready`, `stopped`, `failed` |  |
| [`acquisition/state`](#field-acquisition-state) | `yes` | enum: `idle`, `preparing`, `streaming`, `reconnecting`, `stopping`, `cleanup-uncertain`, `blocked`, `failed` |  |
| [`source/generation`](#field-source-generation) | `yes` | integer |  |
| [`quality`](#field-quality) | `yes` | const: `unknown` |  |
| [`reason/code`](#field-reason-code) | `yes` | enum: `none`, `admission-required`, `metadata-mismatch`, `ambiguous-binding`, `device-not-advertising-or-busy`, `claim-conflict`, `consent-required`, `consent-expired`, `revoked`, `stopped`, `cleanup-unproven`, `runtime-mismatch`, `package-refused` |  |
| [`claim/state`](#field-claim-state) | `yes` | enum: `none`, `held`, `cleanup-hold`, `released` |  |
| [`fence/state`](#field-fence-state) | `yes` | enum: `open`, `closed` |  |
| [`terminal/pending`](#field-terminal-pending) | `yes` | enum: `none`, `idle`, `blocked`, `failed` |  |
| [`reason/retryable`](#field-reason-retryable) | `yes` | boolean |  |
| [`session/epoch`](#field-session-epoch) | `yes` | string \| null |  |
| [`health/aggregate`](#field-health-aggregate) | `yes` | enum: `healthy`, `degraded`, `unavailable` |  |
| [`streams/health`](#field-streams-health) | `yes` | array |  |
| [`acquisition/class`](#field-acquisition-class) | `yes` | enum: `synthetic`, `real-device` |  |
| [`control/available`](#field-control-available) | `yes` | boolean |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-instance-ref"></a>
## `instance/ref`

- Required: `yes`
- Shape: object

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-configuration-state"></a>
## `configuration/state`

- Required: `yes`
- Shape: enum: `declared`, `admitted`, `resolved`, `refused`

<a id="field-supervisor-state"></a>
## `supervisor/state`

- Required: `yes`
- Shape: enum: `configured`, `starting`, `ready`, `stopped`, `failed`

<a id="field-acquisition-state"></a>
## `acquisition/state`

- Required: `yes`
- Shape: enum: `idle`, `preparing`, `streaming`, `reconnecting`, `stopping`, `cleanup-uncertain`, `blocked`, `failed`

<a id="field-source-generation"></a>
## `source/generation`

- Required: `yes`
- Shape: integer

<a id="field-quality"></a>
## `quality`

- Required: `yes`
- Shape: const: `unknown`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: enum: `none`, `admission-required`, `metadata-mismatch`, `ambiguous-binding`, `device-not-advertising-or-busy`, `claim-conflict`, `consent-required`, `consent-expired`, `revoked`, `stopped`, `cleanup-unproven`, `runtime-mismatch`, `package-refused`

<a id="field-claim-state"></a>
## `claim/state`

- Required: `yes`
- Shape: enum: `none`, `held`, `cleanup-hold`, `released`

<a id="field-fence-state"></a>
## `fence/state`

- Required: `yes`
- Shape: enum: `open`, `closed`

<a id="field-terminal-pending"></a>
## `terminal/pending`

- Required: `yes`
- Shape: enum: `none`, `idle`, `blocked`, `failed`

<a id="field-reason-retryable"></a>
## `reason/retryable`

- Required: `yes`
- Shape: boolean

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: string | null

<a id="field-health-aggregate"></a>
## `health/aggregate`

- Required: `yes`
- Shape: enum: `healthy`, `degraded`, `unavailable`

<a id="field-streams-health"></a>
## `streams/health`

- Required: `yes`
- Shape: array

<a id="field-acquisition-class"></a>
## `acquisition/class`

- Required: `yes`
- Shape: enum: `synthetic`, `real-device`

<a id="field-control-available"></a>
## `control/available`

- Required: `yes`
- Shape: boolean
