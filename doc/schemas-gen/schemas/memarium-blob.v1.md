# Memarium Blob v1

Source schema: [`doc/schemas/memarium-blob.v1.schema.json`](../../schemas/memarium-blob.v1.schema.json)

Machine-readable schema for a signed, content-addressed Memarium-native artifact envelope. It is used for artifacts that are not Agora records but still need byte-identical custody and transfer, including small out-of-band passport handoffs, encrypted notes, action-trace archives, backup bundles, and INAC payloads.

## Governing Basis

- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)
- [`doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`](../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md)
- [`doc/project/60-solutions/002-memarium/002-memarium.md`](../../project/60-solutions/002-memarium/002-memarium.md)

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
| [`schema`](#field-schema) | `yes` | const: `memarium-blob.v1` | Schema discriminator. MUST be the literal string `memarium-blob.v1`. |
| [`blob/id`](#field-blob-id) | `yes` | string | Content-addressed identifier of this blob envelope. Computed from canonical bytes of the envelope without `blob/id` and `signature`, using the same sha256 base64url convention as Agora records and capability artifacts. |
| [`blob/content-type`](#field-blob-content-type) | `yes` | string | IANA-style media type or Orbiplex-registered kind label used by receivers to select a handler. The substrate treats it as an opaque dispatch hint. |
| [`blob/payload`](#field-blob-payload) | `yes` | unspecified | Payload carried inline for tiny control-plane handoffs or referenced by content hash and stream id for side-loaded binary-frame transfer. |
| [`blob/encryption`](#field-blob-encryption) | `yes` | unspecified | `none` for plaintext custody or an encryption descriptor. Encrypted blobs make the receiver a byte custodian, not necessarily a reader. |
| [`author/participant-id`](#field-author-participant-id) | `yes` | string | Author identity. Accepts participant and nym DID keys as described by the identity and pseudonymization proposals. |
| [`authored/at`](#field-authored-at) | `yes` | string | Wall-clock timestamp asserted by the author at blob creation. |
| [`author/attestation-ref`](#field-author-attestation-ref) | `no` | string | Optional reference to an attestation artifact supporting the author's authority or context. |
| [`author/nym-certificate-ref`](#field-author-nym-certificate-ref) | `no` | string | Optional reference to a nym certificate when the author identity is pseudonymous. |
| [`classification`](#field-classification) | `no` | object | Optional classification label carried with the blob for downstream custody and egress decisions. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` | Ed25519 signature over canonical envelope bytes with `signature` removed, using signing domain `memarium.blob.v1`. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`inlinePayload`](#def-inlinepayload) | object |  |
| [`referencedPayload`](#def-referencedpayload) | object |  |
| [`encryption`](#def-encryption) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `memarium-blob.v1`

Schema discriminator. MUST be the literal string `memarium-blob.v1`.

<a id="field-blob-id"></a>
## `blob/id`

- Required: `yes`
- Shape: string

Content-addressed identifier of this blob envelope. Computed from canonical bytes of the envelope without `blob/id` and `signature`, using the same sha256 base64url convention as Agora records and capability artifacts.

<a id="field-blob-content-type"></a>
## `blob/content-type`

- Required: `yes`
- Shape: string

IANA-style media type or Orbiplex-registered kind label used by receivers to select a handler. The substrate treats it as an opaque dispatch hint.

<a id="field-blob-payload"></a>
## `blob/payload`

- Required: `yes`
- Shape: unspecified

Payload carried inline for tiny control-plane handoffs or referenced by content hash and stream id for side-loaded binary-frame transfer.

<a id="field-blob-encryption"></a>
## `blob/encryption`

- Required: `yes`
- Shape: unspecified

`none` for plaintext custody or an encryption descriptor. Encrypted blobs make the receiver a byte custodian, not necessarily a reader.

<a id="field-author-participant-id"></a>
## `author/participant-id`

- Required: `yes`
- Shape: string

Author identity. Accepts participant and nym DID keys as described by the identity and pseudonymization proposals.

<a id="field-authored-at"></a>
## `authored/at`

- Required: `yes`
- Shape: string

Wall-clock timestamp asserted by the author at blob creation.

<a id="field-author-attestation-ref"></a>
## `author/attestation-ref`

- Required: `no`
- Shape: string

Optional reference to an attestation artifact supporting the author's authority or context.

<a id="field-author-nym-certificate-ref"></a>
## `author/nym-certificate-ref`

- Required: `no`
- Shape: string

Optional reference to a nym certificate when the author identity is pseudonymous.

<a id="field-classification"></a>
## `classification`

- Required: `no`
- Shape: object

Optional classification label carried with the blob for downstream custody and egress decisions.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

Ed25519 signature over canonical envelope bytes with `signature` removed, using signing domain `memarium.blob.v1`.

## Definition Semantics

<a id="def-inlinepayload"></a>
## `$defs.inlinePayload`

- Shape: object

<a id="def-referencedpayload"></a>
## `$defs.referencedPayload`

- Shape: object

<a id="def-encryption"></a>
## `$defs.encryption`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
