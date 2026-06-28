# Relationship Class v1

Source schema: [`doc/schemas/relationship-class.v1.schema.json`](../../schemas/relationship-class.v1.schema.json)

Operator-defined local relationship class definition. A class is policy metadata and never authority by itself.

## Governing Basis

- [`doc/project/40-proposals/065-local-relationship-layer.md`](../../project/40-proposals/065-local-relationship-layer.md)
- [`doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)

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
| [`schema`](#field-schema) | `yes` | const: `relationship-class.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`class/id`](#field-class-id) | `yes` | ref: `#/$defs/class_id` |  |
| [`class/state`](#field-class-state) | `yes` | enum: `active`, `archived` |  |
| [`display/label`](#field-display-label) | `yes` | string |  |
| [`description`](#field-description) | `no` | string |  |
| [`default/status`](#field-default-status) | `yes` | enum: `active`, `pending-outgoing`, `pending-incoming`, `blocked`, `revoked` |  |
| [`grant-policy/default-allowlist`](#field-grant-policy-default-allowlist) | `no` | array | Capabilities host policy may consider for members. This is not an automatic grant. |
| [`grant-policy/suggested-defaults`](#field-grant-policy-suggested-defaults) | `no` | array | Suggested capabilities requiring explicit operator confirmation. |
| [`grant-allowlist`](#field-grant-allowlist) | `no` | array |  |
| [`verification/required`](#field-verification-required) | `no` | array |  |
| [`privacy/profile`](#field-privacy-profile) | `yes` | enum: `sealed-only`, `operator-visible-summary`, `public-aggregate` |  |
| [`retention/profile-ref`](#field-retention-profile-ref) | `no` | string | Optional reference to a host-owned Local Relationship retention profile. Absence means inherit `local-relationship/default`; inline retention windows or deletion rules are not part of relationship-class.v1. |
| [`policy/refs`](#field-policy-refs) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`class_id`](#def-class-id) | string |  |
| [`capability_id`](#def-capability-id) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `relationship-class.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-class-id"></a>
## `class/id`

- Required: `yes`
- Shape: ref: `#/$defs/class_id`

<a id="field-class-state"></a>
## `class/state`

- Required: `yes`
- Shape: enum: `active`, `archived`

<a id="field-display-label"></a>
## `display/label`

- Required: `yes`
- Shape: string

<a id="field-description"></a>
## `description`

- Required: `no`
- Shape: string

<a id="field-default-status"></a>
## `default/status`

- Required: `yes`
- Shape: enum: `active`, `pending-outgoing`, `pending-incoming`, `blocked`, `revoked`

<a id="field-grant-policy-default-allowlist"></a>
## `grant-policy/default-allowlist`

- Required: `no`
- Shape: array

Capabilities host policy may consider for members. This is not an automatic grant.

<a id="field-grant-policy-suggested-defaults"></a>
## `grant-policy/suggested-defaults`

- Required: `no`
- Shape: array

Suggested capabilities requiring explicit operator confirmation.

<a id="field-grant-allowlist"></a>
## `grant-allowlist`

- Required: `no`
- Shape: array

<a id="field-verification-required"></a>
## `verification/required`

- Required: `no`
- Shape: array

<a id="field-privacy-profile"></a>
## `privacy/profile`

- Required: `yes`
- Shape: enum: `sealed-only`, `operator-visible-summary`, `public-aggregate`

<a id="field-retention-profile-ref"></a>
## `retention/profile-ref`

- Required: `no`
- Shape: string

Optional reference to a host-owned Local Relationship retention profile. Absence means inherit `local-relationship/default`; inline retention windows or deletion rules are not part of relationship-class.v1.

<a id="field-policy-refs"></a>
## `policy/refs`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-class-id"></a>
## `$defs.class_id`

- Shape: string

<a id="def-capability-id"></a>
## `$defs.capability_id`

- Shape: string
