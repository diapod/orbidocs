# Client Instance Detachment v1

Source schema: [`doc/schemas/client-instance-detachment.v1.schema.json`](../../schemas/client-instance-detachment.v1.schema.json)

Machine-readable schema for a pod-layer artifact that detaches a concrete client instance from a serving-node session using the same participant-over-channel boundary as `client-instance-attachment.v1`.

## Governing Basis

- [`doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`](../../project/40-proposals/006-pod-access-layer-for-thin-clients.md)
- [`doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`](../../project/40-proposals/007-pod-identity-and-tenancy-model.md)
- [`doc/schemas/client-instance-attachment.v1.schema.json`](../../schemas/client-instance-attachment.v1.schema.json)
- [`doc/schemas/participant-bind.v1.schema.json`](../../schemas/participant-bind.v1.schema.json)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`detachment/id`](#field-detachment-id) | `yes` | string | Stable identifier of this client-instance detachment artifact. |
| [`detached-at`](#field-detached-at) | `yes` | string | Timestamp when the client instance was detached or invalidated. |
| [`attachment/id`](#field-attachment-id) | `yes` | string | Reference to the earlier attachment artifact being terminated. |
| [`serving-node/id`](#field-serving-node-id) | `yes` | string | Serving node that hosted the attached client session. |
| [`client-instance/id`](#field-client-instance-id) | `yes` | string | Concrete client, device, or install instance being detached. |
| [`detach/reason`](#field-detach-reason) | `yes` | enum: `user-request`, `device-loss`, `session-expired`, `policy`, `migration`, `operator-action` | Coarse detachment reason. It is intentionally bounded and does not require disclosure of detailed operational internals. |
| [`detach/notes`](#field-detach-notes) | `no` | string | Optional operator- or client-facing note describing the detachment in more detail. |
| [`participant-bind`](#field-participant-bind) | `yes` | ref: `participant-bind.v1.schema.json` | Participant-scoped bind reused to prove whose session context is being detached. |
| [`proof/node-attestation`](#field-proof-node-attestation) | `no` | ref: `#/$defs/signature` | Optional future-facing serving-node attestation over the detachment artifact. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation policy annotations that do not change the core detachment semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-detachment-id"></a>
## `detachment/id`

- Required: `yes`
- Shape: string

Stable identifier of this client-instance detachment artifact.

<a id="field-detached-at"></a>
## `detached-at`

- Required: `yes`
- Shape: string

Timestamp when the client instance was detached or invalidated.

<a id="field-attachment-id"></a>
## `attachment/id`

- Required: `yes`
- Shape: string

Reference to the earlier attachment artifact being terminated.

<a id="field-serving-node-id"></a>
## `serving-node/id`

- Required: `yes`
- Shape: string

Serving node that hosted the attached client session.

<a id="field-client-instance-id"></a>
## `client-instance/id`

- Required: `yes`
- Shape: string

Concrete client, device, or install instance being detached.

<a id="field-detach-reason"></a>
## `detach/reason`

- Required: `yes`
- Shape: enum: `user-request`, `device-loss`, `session-expired`, `policy`, `migration`, `operator-action`

Coarse detachment reason. It is intentionally bounded and does not require disclosure of detailed operational internals.

<a id="field-detach-notes"></a>
## `detach/notes`

- Required: `no`
- Shape: string

Optional operator- or client-facing note describing the detachment in more detail.

<a id="field-participant-bind"></a>
## `participant-bind`

- Required: `yes`
- Shape: ref: `participant-bind.v1.schema.json`

Participant-scoped bind reused to prove whose session context is being detached.

<a id="field-proof-node-attestation"></a>
## `proof/node-attestation`

- Required: `no`
- Shape: ref: `#/$defs/signature`

Optional future-facing serving-node attestation over the detachment artifact.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation policy annotations that do not change the core detachment semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
