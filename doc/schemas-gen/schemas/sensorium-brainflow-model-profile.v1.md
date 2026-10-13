# Sensorium-brainflow-model-profile.v1

Source schema: [`doc/schemas/sensorium-brainflow-model-profile.v1.schema.json`](../../schemas/sensorium-brainflow-model-profile.v1.schema.json)

Declarative model x transport profile. Native key is selected by the exact package, never supplied as a public board-id override. Candidate profiles grant no readiness or authority; exact metadata and observed activity are independent qualification gates. No AUX modes, arbitrary config commands or streamers in this slice. P096-004 built-ins also supply a readable version/form and per-stream continuity policy. Optional lab observations are scoped activity evidence, never active-channel guarantees, heart-rate inference or qualification; units unknown until P096-007b.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-model-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`model`](#field-model) | `yes` | enum: `synthetic`, `muse-2` |  |
| [`transport`](#field-transport) | `yes` | enum: `synthetic`, `ble` |  |
| [`board/key`](#field-board-key) | `yes` | enum: `SYNTHETIC_BOARD`, `MUSE_2_BOARD` |  |
| [`metadata/build`](#field-metadata-build) | `yes` | object |  |
| [`verification`](#field-verification) | `yes` | enum: `candidate`, `metadata-verified`, `qualified` |  |
| [`modes`](#field-modes) | `yes` | array |  |
| [`binding/assurance`](#field-binding-assurance) | `yes` | const: `operator-confirmed-selector` |  |
| [`quality`](#field-quality) | `yes` | const: `unknown` |  |
| [`profile/version`](#field-profile-version) | `no` | string |  |
| [`display/name`](#field-display-name) | `no` | string |  |
| [`form`](#field-form) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-model-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: enum: `synthetic`, `muse-2`

<a id="field-transport"></a>
## `transport`

- Required: `yes`
- Shape: enum: `synthetic`, `ble`

<a id="field-board-key"></a>
## `board/key`

- Required: `yes`
- Shape: enum: `SYNTHETIC_BOARD`, `MUSE_2_BOARD`

<a id="field-metadata-build"></a>
## `metadata/build`

- Required: `yes`
- Shape: object

<a id="field-verification"></a>
## `verification`

- Required: `yes`
- Shape: enum: `candidate`, `metadata-verified`, `qualified`

<a id="field-modes"></a>
## `modes`

- Required: `yes`
- Shape: array

<a id="field-binding-assurance"></a>
## `binding/assurance`

- Required: `yes`
- Shape: const: `operator-confirmed-selector`

<a id="field-quality"></a>
## `quality`

- Required: `yes`
- Shape: const: `unknown`

<a id="field-profile-version"></a>
## `profile/version`

- Required: `no`
- Shape: string

<a id="field-display-name"></a>
## `display/name`

- Required: `no`
- Shape: string

<a id="field-form"></a>
## `form`

- Required: `no`
- Shape: object
