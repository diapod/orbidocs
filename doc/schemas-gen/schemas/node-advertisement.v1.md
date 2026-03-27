# Node Advertisement v1

Source schema: [`doc/schemas/node-advertisement.v1.schema.json`](../../schemas/node-advertisement.v1.schema.json)

Machine-readable schema for signed endpoint advertisements exchanged during Node discovery. In v1 the signed surface is the deterministic CBOR image of the whole advertisement payload excluding only the `signature` field itself. Transport-mutable per-hop metadata, if introduced later, must remain outside this semantic payload.

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
| [`advertisement/id`](#field-advertisement-id) | `yes` | string | Stable identifier of this signed endpoint advertisement. |
| [`node/id`](#field-node-id) | `yes` | string | Node addressed by this advertisement. In v1 this MUST use the canonical `node:did:key:z...` format. |
| [`sequence/no`](#field-sequence-no) | `yes` | integer | Monotonic per-node advertisement sequence number inside the signed payload. In v1 discovery state keeps only the latest advertisement per `node/id`, so higher sequence numbers supersede older ones. |
| [`advertised-at`](#field-advertised-at) | `yes` | string | Timestamp when the advertisement was published. This is part of the signed payload. |
| [`expires-at`](#field-expires-at) | `yes` | string | Timestamp after which this advertisement must be treated as stale. This is part of the signed payload. |
| [`key/alg`](#field-key-alg) | `yes` | enum: `ed25519` | Algorithm of the key used to sign this advertisement. |
| [`key/public`](#field-key-public) | `yes` | string | Canonical did:key fingerprint payload corresponding to `node/id`. |
| [`federation/id`](#field-federation-id) | `no` | string | Optional federation scope advertised for bootstrap policy decisions. |
| [`endpoints`](#field-endpoints) | `yes` | array | Currently valid live endpoints exposed by the Node. Receivers first filter unsupported transports and then use endpoint priority as the sender-side preference hint among compatible endpoints. |
| [`transports/supported`](#field-transports-supported) | `yes` | array | Baseline transport profiles currently supported by the Node. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation-local annotations that do not change core discovery semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`endpoint`](#def-endpoint) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-advertisement-id"></a>
## `advertisement/id`

- Required: `yes`
- Shape: string

Stable identifier of this signed endpoint advertisement.

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

Node addressed by this advertisement. In v1 this MUST use the canonical `node:did:key:z...` format.

<a id="field-sequence-no"></a>
## `sequence/no`

- Required: `yes`
- Shape: integer

Monotonic per-node advertisement sequence number inside the signed payload. In v1 discovery state keeps only the latest advertisement per `node/id`, so higher sequence numbers supersede older ones.

<a id="field-advertised-at"></a>
## `advertised-at`

- Required: `yes`
- Shape: string

Timestamp when the advertisement was published. This is part of the signed payload.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

Timestamp after which this advertisement must be treated as stale. This is part of the signed payload.

<a id="field-key-alg"></a>
## `key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Algorithm of the key used to sign this advertisement.

<a id="field-key-public"></a>
## `key/public`

- Required: `yes`
- Shape: string

Canonical did:key fingerprint payload corresponding to `node/id`.

<a id="field-federation-id"></a>
## `federation/id`

- Required: `no`
- Shape: string

Optional federation scope advertised for bootstrap policy decisions.

<a id="field-endpoints"></a>
## `endpoints`

- Required: `yes`
- Shape: array

Currently valid live endpoints exposed by the Node. Receivers first filter unsupported transports and then use endpoint priority as the sender-side preference hint among compatible endpoints.

<a id="field-transports-supported"></a>
## `transports/supported`

- Required: `yes`
- Shape: array

Baseline transport profiles currently supported by the Node.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation-local annotations that do not change core discovery semantics.

## Definition Semantics

<a id="def-endpoint"></a>
## `$defs.endpoint`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
