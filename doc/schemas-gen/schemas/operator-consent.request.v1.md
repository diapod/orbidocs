# Operator-consent.request.v1

Source schema: [`doc/schemas/operator-consent.request.v1.schema.json`](../../schemas/operator-consent.request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`](../../project/40-proposals/048-sensorium-os-connector-action-classes.md)

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
| [`schema`](#field-schema) | `yes` | const: `operator-consent.request.v1` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `#/$defs/token` |  |
| [`source/component`](#field-source-component) | `yes` | ref: `#/$defs/ref` |  |
| [`requested/by`](#field-requested-by) | `yes` | ref: `#/$defs/ref` |  |
| [`requester/ref`](#field-requester-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operation/digest`](#field-operation-digest) | `yes` | ref: `#/$defs/sha256` |  |
| [`workspace/ref`](#field-workspace-ref) | `no` | ref: `#/$defs/ref` |  |
| [`root/ref`](#field-root-ref) | `no` | ref: `#/$defs/ref` |  |
| [`descriptor`](#field-descriptor) | `yes` | object | Adapter-specific redacted consent descriptor. Concrete descriptors are typed by their own schema. |
| [`options`](#field-options) | `yes` | array |  |
| [`default/on-timeout`](#field-default-on-timeout) | `yes` | const: `deny` |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`metadata`](#field-metadata) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`token`](#def-token) | string |  |
| [`sha256`](#def-sha256) | string |  |
| [`scope`](#def-scope) | enum: `deny`, `allow-once`, `remember-exact-argv`, `remember-argv-prefix`, `remember-action-catalog-entry` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-consent.request.v1`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-source-component"></a>
## `source/component`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-requested-by"></a>
## `requested/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-requester-ref"></a>
## `requester/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operation-digest"></a>
## `operation/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256`

<a id="field-workspace-ref"></a>
## `workspace/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-root-ref"></a>
## `root/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-descriptor"></a>
## `descriptor`

- Required: `yes`
- Shape: object

Adapter-specific redacted consent descriptor. Concrete descriptors are typed by their own schema.

<a id="field-options"></a>
## `options`

- Required: `yes`
- Shape: array

<a id="field-default-on-timeout"></a>
## `default/on-timeout`

- Required: `yes`
- Shape: const: `deny`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-metadata"></a>
## `metadata`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-sha256"></a>
## `$defs.sha256`

- Shape: string

<a id="def-scope"></a>
## `$defs.scope`

- Shape: enum: `deny`, `allow-once`, `remember-exact-argv`, `remember-argv-prefix`, `remember-action-catalog-entry`
