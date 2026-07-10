# Artifact Delivery Envelope v1

Source schema: [`doc/schemas/artifact-delivery-envelope.v1.schema.json`](../../schemas/artifact-delivery-envelope.v1.schema.json)

Host capability request for Artifact Delivery. The envelope carries one artifact descriptor, one delivery plan, optional policy, and optional idempotency key. Host config resolves route refs, defaults, groups, and transport adapters.

## Governing Basis

- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)
- [`doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`](../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

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
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-envelope.v1` |  |
| [`component/id`](#field-component-id) | `yes` | string |  |
| [`artifact`](#field-artifact) | `yes` | ref: `#/$defs/artifact` |  |
| [`classification`](#field-classification) | `no` | ref: `classification.v1.schema.json` |  |
| [`causal/context`](#field-causal-context) | `no` | ref: `causal-context.v1.schema.json` | Optional upstream P081 causal context. The receiving host derives its own Artifact Delivery operation context from this evidence. |
| [`delivery/plan`](#field-delivery-plan) | `yes` | ref: `#/$defs/deliveryPlan` |  |
| [`policy`](#field-policy) | `no` | ref: `#/$defs/policy` |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifact`](#def-artifact) | object |  |
| [`deliveryPlan`](#def-deliveryplan) | object |  |
| [`stage`](#def-stage) | object |  |
| [`selector`](#def-selector) | unspecified |  |
| [`inac_authorization`](#def-inac-authorization) | object |  |
| [`capability_filters`](#def-capability-filters) | object |  |
| [`policy`](#def-policy) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-envelope.v1`

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: string

<a id="field-artifact"></a>
## `artifact`

- Required: `yes`
- Shape: ref: `#/$defs/artifact`

<a id="field-classification"></a>
## `classification`

- Required: `no`
- Shape: ref: `classification.v1.schema.json`

<a id="field-causal-context"></a>
## `causal/context`

- Required: `no`
- Shape: ref: `causal-context.v1.schema.json`

Optional upstream P081 causal context. The receiving host derives its own Artifact Delivery operation context from this evidence.

<a id="field-delivery-plan"></a>
## `delivery/plan`

- Required: `yes`
- Shape: ref: `#/$defs/deliveryPlan`

<a id="field-policy"></a>
## `policy`

- Required: `no`
- Shape: ref: `#/$defs/policy`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-artifact"></a>
## `$defs.artifact`

- Shape: object

<a id="def-deliveryplan"></a>
## `$defs.deliveryPlan`

- Shape: object

<a id="def-stage"></a>
## `$defs.stage`

- Shape: object

<a id="def-selector"></a>
## `$defs.selector`

- Shape: unspecified

<a id="def-inac-authorization"></a>
## `$defs.inac_authorization`

- Shape: object

<a id="def-capability-filters"></a>
## `$defs.capability_filters`

- Shape: object

<a id="def-policy"></a>
## `$defs.policy`

- Shape: object
