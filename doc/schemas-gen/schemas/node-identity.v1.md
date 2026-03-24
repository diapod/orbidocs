# Node Identity v1

Source schema: [`doc/schemas/node-identity.v1.schema.json`](../../schemas/node-identity.v1.schema.json)

Machine-readable schema for the persisted local identity of a network-participating Orbiplex Node.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/60-solutions/node.md`](../../project/60-solutions/node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`node/id`](#field-node-id) | `yes` | string | Stable Node identifier derived from the public key and persisted across restarts until explicit rotation. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the local identity was first created. |
| [`identity/status`](#field-identity-status) | `no` | enum: `active`, `rotating` | Local lifecycle state of the identity material. |
| [`key/alg`](#field-key-alg) | `yes` | enum: `ed25519` | Public-key algorithm used to derive `node/id` and sign networking artifacts. |
| [`key/public`](#field-key-public) | `yes` | string | Public key material used by peers to validate signed advertisements and handshakes. |
| [`key/storage-ref`](#field-key-storage-ref) | `no` | string | Local secure-storage or keystore reference to the corresponding private key material. This is the preferred target shape once key resolution is split from the identity record. |
| [`private_key_base64`](#field-private-key-base64) | `no` | string | Inline base64url-encoded private key material. This is allowed as a bootstrap-compatible shape for early Node implementations, but should later give way to `key/storage-ref`. |
| [`federation/default-id`](#field-federation-default-id) | `no` | string | Optional default federation binding used by higher layers. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local annotations that do not change networking semantics. |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

Stable Node identifier derived from the public key and persisted across restarts until explicit rotation.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the local identity was first created.

<a id="field-identity-status"></a>
## `identity/status`

- Required: `no`
- Shape: enum: `active`, `rotating`

Local lifecycle state of the identity material.

<a id="field-key-alg"></a>
## `key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Public-key algorithm used to derive `node/id` and sign networking artifacts.

<a id="field-key-public"></a>
## `key/public`

- Required: `yes`
- Shape: string

Public key material used by peers to validate signed advertisements and handshakes.

<a id="field-key-storage-ref"></a>
## `key/storage-ref`

- Required: `no`
- Shape: string

Local secure-storage or keystore reference to the corresponding private key material. This is the preferred target shape once key resolution is split from the identity record.

<a id="field-private-key-base64"></a>
## `private_key_base64`

- Required: `no`
- Shape: string

Inline base64url-encoded private key material. This is allowed as a bootstrap-compatible shape for early Node implementations, but should later give way to `key/storage-ref`.

<a id="field-federation-default-id"></a>
## `federation/default-id`

- Required: `no`
- Shape: string

Optional default federation binding used by higher layers.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local annotations that do not change networking semantics.
