# Client Instance Attachment v1

Source schema: [`doc/schemas/client-instance-attachment.v1.schema.json`](../../schemas/client-instance-attachment.v1.schema.json)

Machine-readable schema for the first pod-layer artifact that attaches a concrete client instance to a live serving-node session using an embedded participant bind. This remains above `peer-handshake.v1` and is intended for post-MVP thin-client or hosted-user flows.

## Governing Basis

- [`doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`](../../project/40-proposals/006-pod-access-layer-for-thin-clients.md)
- [`doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`](../../project/40-proposals/007-pod-identity-and-tenancy-model.md)
- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/schemas/participant-bind.v1.schema.json`](../../schemas/participant-bind.v1.schema.json)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`attachment/id`](#field-attachment-id) | `yes` | string | Stable identifier of this client-instance attachment artifact. |
| [`attached-at`](#field-attached-at) | `yes` | string | Timestamp when the client instance was attached to the serving node. |
| [`profile/type`](#field-profile-type) | `yes` | enum: `pod-client`, `hybrid` | Participation profile used by this attached client surface. |
| [`serving-node/id`](#field-serving-node-id) | `yes` | string | Serving node that hosts the attachment. |
| [`pod-user/id`](#field-pod-user-id) | `no` | string | Hosted-user identity when the attachment belongs to a later pod tenancy. In early post-MVP deployments this may still coincide with a participant-style role. |
| [`client-instance/id`](#field-client-instance-id) | `yes` | string | Concrete client, device, or install instance being attached. |
| [`models/local?`](#field-models-local) | `no` | boolean | Whether the attached client keeps substantive local execution responsibilities. |
| [`session/state`](#field-session-state) | `yes` | enum: `attaching`, `attached`, `degraded`, `suspended` | Operational state of the attached client session. |
| [`export/capable?`](#field-export-capable) | `yes` | boolean | Whether the attachment contract claims user export capability. |
| [`migration/allowed?`](#field-migration-allowed) | `yes` | boolean | Whether the attachment contract claims that migration away from the serving node is allowed. |
| [`participant-bind`](#field-participant-bind) | `yes` | ref: `participant-bind.v1.schema.json` | Participant-scoped bind proving who is speaking over the already established node-to-node session. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional hosting or federation policy annotations that do not change the core attachment semantics. |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-attachment-id"></a>
## `attachment/id`

- Required: `yes`
- Shape: string

Stable identifier of this client-instance attachment artifact.

<a id="field-attached-at"></a>
## `attached-at`

- Required: `yes`
- Shape: string

Timestamp when the client instance was attached to the serving node.

<a id="field-profile-type"></a>
## `profile/type`

- Required: `yes`
- Shape: enum: `pod-client`, `hybrid`

Participation profile used by this attached client surface.

<a id="field-serving-node-id"></a>
## `serving-node/id`

- Required: `yes`
- Shape: string

Serving node that hosts the attachment.

<a id="field-pod-user-id"></a>
## `pod-user/id`

- Required: `no`
- Shape: string

Hosted-user identity when the attachment belongs to a later pod tenancy. In early post-MVP deployments this may still coincide with a participant-style role.

<a id="field-client-instance-id"></a>
## `client-instance/id`

- Required: `yes`
- Shape: string

Concrete client, device, or install instance being attached.

<a id="field-models-local"></a>
## `models/local?`

- Required: `no`
- Shape: boolean

Whether the attached client keeps substantive local execution responsibilities.

<a id="field-session-state"></a>
## `session/state`

- Required: `yes`
- Shape: enum: `attaching`, `attached`, `degraded`, `suspended`

Operational state of the attached client session.

<a id="field-export-capable"></a>
## `export/capable?`

- Required: `yes`
- Shape: boolean

Whether the attachment contract claims user export capability.

<a id="field-migration-allowed"></a>
## `migration/allowed?`

- Required: `yes`
- Shape: boolean

Whether the attachment contract claims that migration away from the serving node is allowed.

<a id="field-participant-bind"></a>
## `participant-bind`

- Required: `yes`
- Shape: ref: `participant-bind.v1.schema.json`

Participant-scoped bind proving who is speaking over the already established node-to-node session.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional hosting or federation policy annotations that do not change the core attachment semantics.
