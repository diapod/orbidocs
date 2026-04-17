# Node Address Attestation v1

Source schema: [`doc/schemas/node-address-attestation.v1.schema.json`](../../schemas/node-address-attestation.v1.schema.json)

Fallback signed-evidence artifact for a single normalized Node address claim. Seed Directory remains the trusted primary source for node address resolution; this artifact carries bounded evidence that may help a receiver make a local degraded-mode dial decision when Seed Directory is unavailable. It belongs to the broader Orbiplex signed-credential/passport family but is intentionally not encoded as `capability-passport.v1`: capability passports grant authority, while address attestations carry freshness-bound evidence about observed reachability. The signed address claim is the deterministic canonical JSON of `{target/node-id, endpoint}`; evidence signatures bind to `claim/digest` and their own freshness metadata.

## Governing Basis

- [`doc/project/40-proposals/043-node-address-attestation-fallback.md`](../../project/40-proposals/043-node-address-attestation-fallback.md)
- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)
- [`doc/project/50-requirements/requirements-014.md`](../../project/50-requirements/requirements-014.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `node-address-attestation.v1` | Schema discriminator. MUST be exactly `node-address-attestation.v1`. |
| [`attestation/id`](#field-attestation-id) | `yes` | string | Stable identifier for this assembled evidence packet. Recommended construction: `attestation:node-address:<claim-digest-suffix>:<unix-nanos-or-random>`. |
| [`target/node-id`](#field-target-node-id) | `yes` | string | Node whose endpoint is being attested. MUST match the node id in the embedded or referenced `node-advertisement.v1` when that advertisement is available. |
| [`endpoint`](#field-endpoint) | `yes` | ref: `#/$defs/normalizedEndpoint` | Normalized endpoint claim being attested. The claim digest is computed from canonical JSON containing only `target/node-id` and this normalized endpoint object. Receivers MUST normalize before digest comparison; raw endpoint URLs from advertisements are not authoritative for digesting. |
| [`claim/digest`](#field-claim-digest) | `yes` | ref: `#/$defs/sha256Digest` | Digest of the normalized address claim: `sha256:<base64url-no-pad>` over canonical JSON `{ "target/node-id": ..., "endpoint": ... }`. Every evidence entry MUST repeat this same digest. |
| [`node-advertisement`](#field-node-advertisement) | `no` | object | Optional full `node-advertisement.v1` payload for the target node. Its own signature remains governed by `node-advertisement.v1`; this attestation does not reinterpret that signature. |
| [`node-advertisement/ref`](#field-node-advertisement-ref) | `no` | string | Optional content-addressed reference to the target node advertisement when the full advertisement is not embedded. |
| [`advertisement/digest`](#field-advertisement-digest) | `yes` | ref: `#/$defs/sha256Digest` | Digest of the target `node-advertisement.v1` payload or referenced blob. Used for deduplication and for checking that peer evidence refers to the same signed advertisement. |
| [`observed/at`](#field-observed-at) | `yes` | string | Timestamp at which the assembler most recently observed or accepted any evidence in this packet. Informational for ordering; freshness is enforced from each evidence entry and the envelope `expires/at`. |
| [`expires/at`](#field-expires-at) | `yes` | string | Timestamp after which this assembled packet MUST be treated as expired. It SHOULD NOT exceed the earliest authoritative expiry among the evidence entries that make the packet useful under local policy. |
| [`evidence`](#field-evidence) | `yes` | array | Signed evidence entries for this address claim. Unknown evidence kinds are not allowed in v1; new authority-bearing evidence classes require a new schema version or a formally registered extension. |
| [`assembler/node-id`](#field-assembler-node-id) | `no` | string | Optional node that assembled the evidence packet. The assembler is a courier/curator, not an authority, unless it also appears as a valid evidence signer. |
| [`signature`](#field-signature) | `no` | ref: `#/$defs/ed25519Signature` | Optional envelope signature by `assembler/node-id` over the deterministic canonical JSON of the attestation with `signature` omitted. This proves packet assembly integrity, not address authority. Receivers MUST evaluate `evidence[]` independently. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation-local annotations. MUST NOT alter core evidence semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string | `sha256:` followed by unpadded base64url-encoded SHA-256 bytes. |
| [`normalizedEndpoint`](#def-normalizedendpoint) | object | Canonical endpoint descriptor used for address-claim hashing. It intentionally avoids storing a raw URL as the semantic claim because equivalent URLs can differ textually. |
| [`evidenceEntry`](#def-evidenceentry) | object | Signed evidence statement for one normalized address claim. The signature covers the evidence statement without the `signature` field and binds the signer, claim digest, evidence kind, and freshness window. |
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature object used by envelope and evidence signatures. |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "description": "The attestation must carry either a full target node advertisement or a content-addressed reference to one.",
  "oneOf": [
    {
      "required": [
        "node-advertisement"
      ]
    },
    {
      "required": [
        "node-advertisement/ref"
      ]
    }
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `node-address-attestation.v1`

Schema discriminator. MUST be exactly `node-address-attestation.v1`.

<a id="field-attestation-id"></a>
## `attestation/id`

- Required: `yes`
- Shape: string

Stable identifier for this assembled evidence packet. Recommended construction: `attestation:node-address:<claim-digest-suffix>:<unix-nanos-or-random>`.

<a id="field-target-node-id"></a>
## `target/node-id`

- Required: `yes`
- Shape: string

Node whose endpoint is being attested. MUST match the node id in the embedded or referenced `node-advertisement.v1` when that advertisement is available.

<a id="field-endpoint"></a>
## `endpoint`

- Required: `yes`
- Shape: ref: `#/$defs/normalizedEndpoint`

Normalized endpoint claim being attested. The claim digest is computed from canonical JSON containing only `target/node-id` and this normalized endpoint object. Receivers MUST normalize before digest comparison; raw endpoint URLs from advertisements are not authoritative for digesting.

<a id="field-claim-digest"></a>
## `claim/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

Digest of the normalized address claim: `sha256:<base64url-no-pad>` over canonical JSON `{ "target/node-id": ..., "endpoint": ... }`. Every evidence entry MUST repeat this same digest.

<a id="field-node-advertisement"></a>
## `node-advertisement`

- Required: `no`
- Shape: object

Optional full `node-advertisement.v1` payload for the target node. Its own signature remains governed by `node-advertisement.v1`; this attestation does not reinterpret that signature.

<a id="field-node-advertisement-ref"></a>
## `node-advertisement/ref`

- Required: `no`
- Shape: string

Optional content-addressed reference to the target node advertisement when the full advertisement is not embedded.

<a id="field-advertisement-digest"></a>
## `advertisement/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

Digest of the target `node-advertisement.v1` payload or referenced blob. Used for deduplication and for checking that peer evidence refers to the same signed advertisement.

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

Timestamp at which the assembler most recently observed or accepted any evidence in this packet. Informational for ordering; freshness is enforced from each evidence entry and the envelope `expires/at`.

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

Timestamp after which this assembled packet MUST be treated as expired. It SHOULD NOT exceed the earliest authoritative expiry among the evidence entries that make the packet useful under local policy.

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array

Signed evidence entries for this address claim. Unknown evidence kinds are not allowed in v1; new authority-bearing evidence classes require a new schema version or a formally registered extension.

<a id="field-assembler-node-id"></a>
## `assembler/node-id`

- Required: `no`
- Shape: string

Optional node that assembled the evidence packet. The assembler is a courier/curator, not an authority, unless it also appears as a valid evidence signer.

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: ref: `#/$defs/ed25519Signature`

Optional envelope signature by `assembler/node-id` over the deterministic canonical JSON of the attestation with `signature` omitted. This proves packet assembly integrity, not address authority. Receivers MUST evaluate `evidence[]` independently.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation-local annotations. MUST NOT alter core evidence semantics.

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string

`sha256:` followed by unpadded base64url-encoded SHA-256 bytes.

<a id="def-normalizedendpoint"></a>
## `$defs.normalizedEndpoint`

- Shape: object

Canonical endpoint descriptor used for address-claim hashing. It intentionally avoids storing a raw URL as the semantic claim because equivalent URLs can differ textually.

<a id="def-evidenceentry"></a>
## `$defs.evidenceEntry`

- Shape: object

Signed evidence statement for one normalized address claim. The signature covers the evidence statement without the `signature` field and binds the signer, claim digest, evidence kind, and freshness window.

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature object used by envelope and evidence signatures.
