# Sensorium Brain Flow Qualification Tuple v1

Source schema: [`doc/schemas/sensorium-brainflow-qualification-tuple.v1.schema.json`](../../schemas/sensorium-brainflow-qualification-tuple.v1.schema.json)

Draft exact deployment and measurement conditions embedded under qualification/tuple in a class-specific acceptance report. This tuple is data, not a qualification verdict. Unknown fields must use tagged evidence states. Never include physical serials, advertised names, human identity or host-private paths; use evidence-local controller aliases. The qualifier binds evidence class, candidate, reports and executable digest separately.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-qualification-tuple.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`model`](#field-model) | `yes` | object |  |
| [`host`](#field-host) | `yes` | object |  |
| [`transport`](#field-transport) | `yes` | object |  |
| [`build`](#field-build) | `yes` | object |  |
| [`acquisition/mode`](#field-acquisition-mode) | `yes` | string |  |
| [`streams`](#field-streams) | `yes` | array |  |
| [`permissions`](#field-permissions) | `yes` | object |  |
| [`concurrency`](#field-concurrency) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`exactRef`](#def-exactref) | object |  |
| [`evidenceValue`](#def-evidencevalue) | unspecified |  |
| [`binaryBuild`](#def-binarybuild) | object |  |
| [`rational`](#def-rational) | object |  |
| [`observedRate`](#def-observedrate) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-qualification-tuple.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: object

<a id="field-host"></a>
## `host`

- Required: `yes`
- Shape: object

<a id="field-transport"></a>
## `transport`

- Required: `yes`
- Shape: object

<a id="field-build"></a>
## `build`

- Required: `yes`
- Shape: object

<a id="field-acquisition-mode"></a>
## `acquisition/mode`

- Required: `yes`
- Shape: string

<a id="field-streams"></a>
## `streams`

- Required: `yes`
- Shape: array

<a id="field-permissions"></a>
## `permissions`

- Required: `yes`
- Shape: object

<a id="field-concurrency"></a>
## `concurrency`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-exactref"></a>
## `$defs.exactRef`

- Shape: object

<a id="def-evidencevalue"></a>
## `$defs.evidenceValue`

- Shape: unspecified

<a id="def-binarybuild"></a>
## `$defs.binaryBuild`

- Shape: object

<a id="def-rational"></a>
## `$defs.rational`

- Shape: object

<a id="def-observedrate"></a>
## `$defs.observedRate`

- Shape: unspecified
