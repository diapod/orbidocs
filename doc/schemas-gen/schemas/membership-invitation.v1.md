# Membership Invitation v1

Source schema: [`doc/schemas/membership-invitation.v1.schema.json`](../../schemas/membership-invitation.v1.schema.json)

Append-only invitation fact for entering a bounded Orbiplex influence surface. An invitation creates a traceable entry path; it does not itself grant authority.

## Governing Basis

- [`P051`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`Membership Policy`](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invitation/id`](#field-invitation-id) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`issuer/subject`](#field-issuer-subject) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`invitee/subject`](#field-invitee-subject) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`invitee/anchor-ref`](#field-invitee-anchor-ref) | `no` | string | Optional invitee anchor when the future subject id is not known yet. |
| [`entry/profile`](#field-entry-profile) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class` |  |
| [`scopes`](#field-scopes) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/scopes` |  |
| [`sponsorship/required`](#field-sponsorship-required) | `no` | boolean |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`status`](#field-status) | `yes` | enum: `issued`, `accepted`, `expired`, `revoked` |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invitation-id"></a>
## `invitation/id`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-issuer-subject"></a>
## `issuer/subject`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-invitee-subject"></a>
## `invitee/subject`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-invitee-anchor-ref"></a>
## `invitee/anchor-ref`

- Required: `no`
- Shape: string

Optional invitee anchor when the future subject id is not known yet.

<a id="field-entry-profile"></a>
## `entry/profile`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class`

<a id="field-scopes"></a>
## `scopes`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/scopes`

<a id="field-sponsorship-required"></a>
## `sponsorship/required`

- Required: `no`
- Shape: boolean

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `issued`, `accepted`, `expired`, `revoked`

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions`
