# Participant Bind v1

Source schema: [`doc/schemas/participant-bind.v1.schema.json`](../../schemas/participant-bind.v1.schema.json)

Schema seed for a participant-scoped authorization artifact carried over an already established encrypted node-to-node session. This artifact remains above `peer-handshake.v1` and is intended for later hosted-user or multi-participant flows.

## Governing Basis

- [`doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`](../../project/40-proposals/007-pod-identity-and-tenancy-model.md)
- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`bind/id`](#field-bind-id) | `yes` | string | Stable identifier of the bind artifact. |
| [`bound-at`](#field-bound-at) | `yes` | string | Timestamp when the participant asserted this bind over the active channel. |
| [`participant/id`](#field-participant-id) | `yes` | string | Participation-role identity that is being authorized over the already established node-to-node session. |
| [`via/node-id`](#field-via-node-id) | `yes` | string | Hosting or serving node through which the participant speaks. |
| [`session/id`](#field-session-id) | `yes` | string | Reference to the live encrypted node-to-node session or equivalent channel context. |
| [`participant/key/alg`](#field-participant-key-alg) | `yes` | enum: `ed25519` | Verification algorithm for the participant proof material. |
| [`participant/key/public`](#field-participant-key-public) | `yes` | string | Public verification key backing the participant role in the bound context. |
| [`proof/participant-signature`](#field-proof-participant-signature) | `yes` | ref: `#/$defs/signature` | Participant-side proof over the bind payload. |
| [`proof/node-attestation`](#field-proof-node-attestation) | `no` | ref: `#/$defs/signature` | Optional future-facing node-side hosting attestation over the same bind context. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation policy annotations that do not change the core bind semantics. |

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

<a id="field-bind-id"></a>
## `bind/id`

- Required: `yes`
- Shape: string

Stable identifier of the bind artifact.

<a id="field-bound-at"></a>
## `bound-at`

- Required: `yes`
- Shape: string

Timestamp when the participant asserted this bind over the active channel.

<a id="field-participant-id"></a>
## `participant/id`

- Required: `yes`
- Shape: string

Participation-role identity that is being authorized over the already established node-to-node session.

<a id="field-via-node-id"></a>
## `via/node-id`

- Required: `yes`
- Shape: string

Hosting or serving node through which the participant speaks.

<a id="field-session-id"></a>
## `session/id`

- Required: `yes`
- Shape: string

Reference to the live encrypted node-to-node session or equivalent channel context.

<a id="field-participant-key-alg"></a>
## `participant/key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Verification algorithm for the participant proof material.

<a id="field-participant-key-public"></a>
## `participant/key/public`

- Required: `yes`
- Shape: string

Public verification key backing the participant role in the bound context.

<a id="field-proof-participant-signature"></a>
## `proof/participant-signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

Participant-side proof over the bind payload.

<a id="field-proof-node-attestation"></a>
## `proof/node-attestation`

- Required: `no`
- Shape: ref: `#/$defs/signature`

Optional future-facing node-side hosting attestation over the same bind context.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation policy annotations that do not change the core bind semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
