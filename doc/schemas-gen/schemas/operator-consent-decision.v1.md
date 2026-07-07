# Operator-consent-decision.v1

Source schema: [`doc/schemas/operator-consent-decision.v1.schema.json`](../../schemas/operator-consent-decision.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `operator-consent-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`approval/ref`](#field-approval-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operator/ref`](#field-operator-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`consent/decision`](#field-consent-decision) | `yes` | enum: `pending`, `granted`, `denied`, `expired`, `revoked` |  |
| [`consent/scope`](#field-consent-scope) | `yes` | ref: `#/$defs/scope` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | ref: `#/$defs/ref` |  |
| [`delta/digest`](#field-delta-digest) | `yes` | ref: `#/$defs/sha256` |  |
| [`provenance`](#field-provenance) | `yes` | object |  |

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
- Shape: const: `operator-consent-decision.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-approval-ref"></a>
## `approval/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-consent-decision"></a>
## `consent/decision`

- Required: `yes`
- Shape: enum: `pending`, `granted`, `denied`, `expired`, `revoked`

<a id="field-consent-scope"></a>
## `consent/scope`

- Required: `yes`
- Shape: ref: `#/$defs/scope`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-delta-digest"></a>
## `delta/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256`

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
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
