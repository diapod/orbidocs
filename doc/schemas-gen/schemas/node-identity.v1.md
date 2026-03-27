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
| [`node/id`](#field-node-id) | `yes` | string | Stable Node identifier derived from the public key and persisted across restarts until explicit rotation. In v1 this MUST be `node:did:key:z<base58btc(0xed01 \|\| raw_ed25519_public_key)>`. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the local identity was first created. |
| [`identity/status`](#field-identity-status) | `no` | enum: `active` | Local lifecycle state of the identity material. In the MVP runtime only `active` has semantics; future states such as rotation or retirement are deferred. |
| [`key/alg`](#field-key-alg) | `yes` | enum: `ed25519` | Public-key algorithm used to derive `node/id` and sign networking artifacts. |
| [`key/public`](#field-key-public) | `yes` | string | Canonical did:key fingerprint payload used by peers to validate signed advertisements and handshakes. In v1 this is the base58btc multibase Ed25519 public-key fingerprint without the `node:did:key:` prefix. |
| [`key/storage-ref`](#field-key-storage-ref) | `yes` | string | Local secret-storage reference to the corresponding private key material. In the MVP baseline this MUST use the `local-file:` scheme, for example `local-file:identity/node-signing-key.v1.json`. |
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

Stable Node identifier derived from the public key and persisted across restarts until explicit rotation. In v1 this MUST be `node:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the local identity was first created.

<a id="field-identity-status"></a>
## `identity/status`

- Required: `no`
- Shape: enum: `active`

Local lifecycle state of the identity material. In the MVP runtime only `active` has semantics; future states such as rotation or retirement are deferred.

<a id="field-key-alg"></a>
## `key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Public-key algorithm used to derive `node/id` and sign networking artifacts.

<a id="field-key-public"></a>
## `key/public`

- Required: `yes`
- Shape: string

Canonical did:key fingerprint payload used by peers to validate signed advertisements and handshakes. In v1 this is the base58btc multibase Ed25519 public-key fingerprint without the `node:did:key:` prefix.

<a id="field-key-storage-ref"></a>
## `key/storage-ref`

- Required: `yes`
- Shape: string

Local secret-storage reference to the corresponding private key material. In the MVP baseline this MUST use the `local-file:` scheme, for example `local-file:identity/node-signing-key.v1.json`.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local annotations that do not change networking semantics.
