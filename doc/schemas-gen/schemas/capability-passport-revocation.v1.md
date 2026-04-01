# Capability Passport Revocation v1

Source schema: [`doc/schemas/capability-passport-revocation.v1.schema.json`](../../schemas/capability-passport-revocation.v1.schema.json)

Signed revocation artifact that invalidates a previously issued `capability-passport.v1`. Two signing authorities are recognised: the original issuer (sovereign operator who granted the capability) and the subject node (self-revocation by the node whose capability is being withdrawn). The `signed_by` field discriminates between the two paths. The Seed Directory appends accepted revocations to its append-only revocation log; consumers MUST poll `GET /revocations?since=` and immediately invalidate any cached passport whose `passport_id` appears in the log.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)

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
| [`schema`](#field-schema) | `yes` | const: `capability-passport-revocation.v1` | Schema discriminator. MUST be exactly `capability-passport-revocation.v1`. |
| [`revocation_id`](#field-revocation-id) | `yes` | string | Stable unique identifier for this revocation record. MUST use the `passport-revocation:` prefix. |
| [`passport_id`](#field-passport-id) | `yes` | string | Identifier of the `capability-passport.v1` being revoked. MUST use the `passport:capability:` prefix and MUST match an existing passport known to the verifying party. |
| [`node_id`](#field-node-id) | `yes` | string | Node whose delegated capability is being revoked. MUST match the `node_id` in the original passport. |
| [`capability_id`](#field-capability-id) | `yes` | string | Bare kebab-case capability identifier being revoked (e.g. `network-ledger`). MUST match the `capability_id` in the original passport. |
| [`revoked_at`](#field-revoked-at) | `yes` | string | RFC 3339 timestamp at which the revocation was declared. The Seed Directory MUST store this timestamp in the revocation log entry. |
| [`signed_by`](#field-signed-by) | `yes` | enum: `issuer`, `subject` | Who signed this revocation. `issuer` — the sovereign operator participant who originally issued the passport (uses `issuer/participant_id`). `subject` — the target node revoking its own capability using its node key (no `issuer/participant_id`; the signer public key is derived from `node_id`). |
| [`issuer/participant_id`](#field-issuer-participant-id) | `no` | string | Canonical `participant:did:key:z...` identifier of the revoking participant. REQUIRED when `signed_by == "issuer"` and MUST match `issuer/participant_id` in the original passport. MUST NOT be present when `signed_by == "subject"`. |
| [`reason`](#field-reason) | `no` | string | Optional human-readable note explaining why the passport was revoked (e.g. `operator key rotation`, `node decommissioned`). Not machine-interpreted; informational only. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/ed25519Signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional informational annotations. MUST NOT alter revocation semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature over the deterministic canonical JSON of the revocation artifact with the `signature` field omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. For `signed_by == "issuer"` the signing key belongs to `issuer/participant_id`; for `signed_by == "subject"` the signing key belongs to the node identified by `node_id`. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "signed_by": {
      "const": "issuer"
    }
  },
  "required": [
    "signed_by"
  ]
}
```

Then:

```json
{
  "required": [
    "issuer/participant_id"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "signed_by": {
      "const": "subject"
    }
  },
  "required": [
    "signed_by"
  ]
}
```

Then:

```json
{
  "properties": {
    "issuer/participant_id": false
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-revocation.v1`

Schema discriminator. MUST be exactly `capability-passport-revocation.v1`.

<a id="field-revocation-id"></a>
## `revocation_id`

- Required: `yes`
- Shape: string

Stable unique identifier for this revocation record. MUST use the `passport-revocation:` prefix.

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string

Identifier of the `capability-passport.v1` being revoked. MUST use the `passport:capability:` prefix and MUST match an existing passport known to the verifying party.

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

Node whose delegated capability is being revoked. MUST match the `node_id` in the original passport.

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: string

Bare kebab-case capability identifier being revoked (e.g. `network-ledger`). MUST match the `capability_id` in the original passport.

<a id="field-revoked-at"></a>
## `revoked_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which the revocation was declared. The Seed Directory MUST store this timestamp in the revocation log entry.

<a id="field-signed-by"></a>
## `signed_by`

- Required: `yes`
- Shape: enum: `issuer`, `subject`

Who signed this revocation. `issuer` — the sovereign operator participant who originally issued the passport (uses `issuer/participant_id`). `subject` — the target node revoking its own capability using its node key (no `issuer/participant_id`; the signer public key is derived from `node_id`).

<a id="field-issuer-participant-id"></a>
## `issuer/participant_id`

- Required: `no`
- Shape: string

Canonical `participant:did:key:z...` identifier of the revoking participant. REQUIRED when `signed_by == "issuer"` and MUST match `issuer/participant_id` in the original passport. MUST NOT be present when `signed_by == "subject"`.

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

Optional human-readable note explaining why the passport was revoked (e.g. `operator key rotation`, `node decommissioned`). Not machine-interpreted; informational only.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/ed25519Signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional informational annotations. MUST NOT alter revocation semantics.

## Definition Semantics

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature over the deterministic canonical JSON of the revocation artifact with the `signature` field omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. For `signed_by == "issuer"` the signing key belongs to `issuer/participant_id`; for `signed_by == "subject"` the signing key belongs to the node identified by `node_id`.
