# Weak-signal-whisper-draft.local.v2

Source schema: [`doc/schemas/weak-signal-whisper-draft.local.v2.schema.json`](../../schemas/weak-signal-whisper-draft.local.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/078-weak-signal-harvester.md`](../../project/40-proposals/078-weak-signal-harvester.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

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
| [`schema`](#field-schema) | `yes` | const: `weak-signal-whisper-draft.local.v2` |  |
| [`draft/id`](#field-draft-id) | `yes` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`finding/id`](#field-finding-id) | `yes` | string |  |
| [`source/finding-digest`](#field-source-finding-digest) | `yes` | string |  |
| [`source/review-ref`](#field-source-review-ref) | `yes` | string |  |
| [`source/review-digest`](#field-source-review-digest) | `yes` | string |  |
| [`status`](#field-status) | `yes` | const: `draft` |  |
| [`publication/state`](#field-publication-state) | `yes` | const: `not-published` |  |
| [`summary/redacted`](#field-summary-redacted) | `yes` | string |  |
| [`topic/class`](#field-topic-class) | `yes` | string |  |
| [`signal/polarity`](#field-signal-polarity) | `yes` | enum: `problem`, `idea` |  |
| [`source/class`](#field-source-class) | `yes` | const: `derived-local` |  |
| [`origin`](#field-origin) | `yes` | ref: `whisper-origin.v1.schema.json` |  |
| [`custody/claims`](#field-custody-claims) | `yes` | array |  |
| [`privacy/review-required`](#field-privacy-review-required) | `yes` | const: `True` |  |
| [`next/gate`](#field-next-gate) | `yes` | const: `whisper-publication-review-v3` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `weak-signal-whisper-draft.local.v2`

<a id="field-draft-id"></a>
## `draft/id`

- Required: `yes`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-finding-id"></a>
## `finding/id`

- Required: `yes`
- Shape: string

<a id="field-source-finding-digest"></a>
## `source/finding-digest`

- Required: `yes`
- Shape: string

<a id="field-source-review-ref"></a>
## `source/review-ref`

- Required: `yes`
- Shape: string

<a id="field-source-review-digest"></a>
## `source/review-digest`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `draft`

<a id="field-publication-state"></a>
## `publication/state`

- Required: `yes`
- Shape: const: `not-published`

<a id="field-summary-redacted"></a>
## `summary/redacted`

- Required: `yes`
- Shape: string

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

<a id="field-signal-polarity"></a>
## `signal/polarity`

- Required: `yes`
- Shape: enum: `problem`, `idea`

<a id="field-source-class"></a>
## `source/class`

- Required: `yes`
- Shape: const: `derived-local`

<a id="field-origin"></a>
## `origin`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json`

<a id="field-custody-claims"></a>
## `custody/claims`

- Required: `yes`
- Shape: array

<a id="field-privacy-review-required"></a>
## `privacy/review-required`

- Required: `yes`
- Shape: const: `True`

<a id="field-next-gate"></a>
## `next/gate`

- Required: `yes`
- Shape: const: `whisper-publication-review-v3`
