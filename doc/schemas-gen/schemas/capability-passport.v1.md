# Capability Passport v1

Source schema: [`doc/schemas/capability-passport.v1.schema.json`](../../schemas/capability-passport.v1.schema.json)

Signed delegation artifact that grants a named infrastructure capability to a target Node on behalf of a sovereign operator participant. The signed payload is the deterministic canonical JSON of the whole artifact with the `signature` field omitted. Trust derives from local policy recognising the issuer as a sovereign operator, not from the passport alone.

## Governing Basis

- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/20-memos/participant-assurance-levels.md`](../../project/20-memos/participant-assurance-levels.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport.v1` | Schema discriminator. MUST be exactly `capability-passport.v1`. |
| [`passport_id`](#field-passport-id) | `yes` | string | Stable unique identifier for this passport. MUST use the `passport:capability:` prefix. |
| [`node_id`](#field-node-id) | `yes` | string | Target Node receiving the delegated capability. MUST match the `node:did:key:z...` canonical format. |
| [`capability_id`](#field-capability-id) | `yes` | string | Bare kebab-case capability identifier (e.g. `network-ledger`, `seed-directory`, `escrow`). Maps 1:1 to the `core/<id>` or `role/<id>` prefix used in `CapabilityAdvertisementV1`. See Proposal 025 §7 for the naming convention. |
| [`scope`](#field-scope) | `yes` | object | Capability-specific parameters constraining the delegation. MAY be empty (`{}`). Receivers MUST tolerate unknown keys. Capability definitions MAY add required scope fields as those capabilities are specified. |
| [`issued_at`](#field-issued-at) | `yes` | string | RFC 3339 timestamp at which this passport was issued. |
| [`expires_at`](#field-expires-at) | `no` | string \| null | RFC 3339 timestamp after which this passport MUST be treated as expired. `null` means no explicit expiry; receivers SHOULD apply a locally configured maximum TTL. |
| [`issuer/participant_id`](#field-issuer-participant-id) | `yes` | string | Canonical `participant:did:key:z...` identifier of the issuing participant. MUST correspond to a participant whose assurance level is `SovereignOperator` (IAL5) under the receiving Node's local policy. |
| [`issuer/node_id`](#field-issuer-node-id) | `yes` | string | Node on which the issuing participant acted when signing this passport. |
| [`revocation_ref`](#field-revocation-ref) | `yes` | string \| null | Optional reference to an out-of-band revocation endpoint or log for this passport. `null` if no external revocation surface is provided; consumers SHOULD still poll the Seed Directory revocation log. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/ed25519Signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional informational annotations. MUST NOT alter core passport semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature over the deterministic canonical JSON of the passport with the `signature` field omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "passport_id"
  ]
}
```

Then:

```json
{
  "properties": {
    "passport_id": {
      "pattern": "^passport:capability:"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport.v1`

Schema discriminator. MUST be exactly `capability-passport.v1`.

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string

Stable unique identifier for this passport. MUST use the `passport:capability:` prefix.

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

Target Node receiving the delegated capability. MUST match the `node:did:key:z...` canonical format.

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: string

Bare kebab-case capability identifier (e.g. `network-ledger`, `seed-directory`, `escrow`). Maps 1:1 to the `core/<id>` or `role/<id>` prefix used in `CapabilityAdvertisementV1`. See Proposal 025 §7 for the naming convention.

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

Capability-specific parameters constraining the delegation. MAY be empty (`{}`). Receivers MUST tolerate unknown keys. Capability definitions MAY add required scope fields as those capabilities are specified.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which this passport was issued.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `no`
- Shape: string | null

RFC 3339 timestamp after which this passport MUST be treated as expired. `null` means no explicit expiry; receivers SHOULD apply a locally configured maximum TTL.

<a id="field-issuer-participant-id"></a>
## `issuer/participant_id`

- Required: `yes`
- Shape: string

Canonical `participant:did:key:z...` identifier of the issuing participant. MUST correspond to a participant whose assurance level is `SovereignOperator` (IAL5) under the receiving Node's local policy.

<a id="field-issuer-node-id"></a>
## `issuer/node_id`

- Required: `yes`
- Shape: string

Node on which the issuing participant acted when signing this passport.

<a id="field-revocation-ref"></a>
## `revocation_ref`

- Required: `yes`
- Shape: string | null

Optional reference to an out-of-band revocation endpoint or log for this passport. `null` if no external revocation surface is provided; consumers SHOULD still poll the Seed Directory revocation log.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/ed25519Signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional informational annotations. MUST NOT alter core passport semantics.

## Definition Semantics

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature over the deterministic canonical JSON of the passport with the `signature` field omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order.
