# Routing Subject Binding v1

Source schema: [`doc/schemas/routing-subject-binding.v1.schema.json`](../../schemas/routing-subject-binding.v1.schema.json)

Public or presentable binding between a privacy-preserving routing subject and a node that can receive direct delivery, contact, or inbox artifacts for that subject. It is intentionally not a root participant locator.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`](../../project/40-proposals/054-user-maintained-federated-seed-directory.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `routing-subject-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/id`](#field-binding-id) | `yes` | string |  |
| [`routing-subject/id`](#field-routing-subject-id) | `yes` | string | Public routing subject. It may be derived from or delegated by a participant privately, but this artifact does not reveal that root relationship. |
| [`node/id`](#field-node-id) | `yes` | string |  |
| [`disclosure/mode`](#field-disclosure-mode) | `no` | enum: `public-unlinked`, `participant-disclosed`, `org-disclosed`, `present-on-demand` |  |
| [`purposes`](#field-purposes) | `yes` | array |  |
| [`encryption/key/alg`](#field-encryption-key-alg) | `yes` | string |  |
| [`encryption/key/public`](#field-encryption-key-public) | `yes` | string |  |
| [`valid/from`](#field-valid-from) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`scope/federation-id`](#field-scope-federation-id) | `no` | string |  |
| [`scope/topic-patterns`](#field-scope-topic-patterns) | `no` | ref: `#/$defs/stringList` |  |
| [`scope/content-schemas`](#field-scope-content-schemas) | `no` | ref: `#/$defs/stringList` |  |
| [`proof/routing-subject-signature`](#field-proof-routing-subject-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`proof/node-acceptance-signature`](#field-proof-node-acceptance-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`stringList`](#def-stringlist) | array |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `routing-subject-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-id"></a>
## `binding/id`

- Required: `yes`
- Shape: string

<a id="field-routing-subject-id"></a>
## `routing-subject/id`

- Required: `yes`
- Shape: string

Public routing subject. It may be derived from or delegated by a participant privately, but this artifact does not reveal that root relationship.

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

<a id="field-disclosure-mode"></a>
## `disclosure/mode`

- Required: `no`
- Shape: enum: `public-unlinked`, `participant-disclosed`, `org-disclosed`, `present-on-demand`

<a id="field-purposes"></a>
## `purposes`

- Required: `yes`
- Shape: array

<a id="field-encryption-key-alg"></a>
## `encryption/key/alg`

- Required: `yes`
- Shape: string

<a id="field-encryption-key-public"></a>
## `encryption/key/public`

- Required: `yes`
- Shape: string

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-scope-federation-id"></a>
## `scope/federation-id`

- Required: `no`
- Shape: string

<a id="field-scope-topic-patterns"></a>
## `scope/topic-patterns`

- Required: `no`
- Shape: ref: `#/$defs/stringList`

<a id="field-scope-content-schemas"></a>
## `scope/content-schemas`

- Required: `no`
- Shape: ref: `#/$defs/stringList`

<a id="field-proof-routing-subject-signature"></a>
## `proof/routing-subject-signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-proof-node-acceptance-signature"></a>
## `proof/node-acceptance-signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-stringlist"></a>
## `$defs.stringList`

- Shape: array

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
